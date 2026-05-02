import json
import logging
from threading import Thread, Event
from time import time, sleep
from typing import Any, Dict, List, Optional

from pynput import mouse as mo
from pynput import keyboard as ke
from pynput.keyboard import Controller as Controller_k, Key
from pynput.mouse import Controller as Controller_m, Button

from helper import process_helper, mouse_helper
from bot import manager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Default mapping for special keys / buttons (string -> pynput object)
_KEY_MAP: Dict[str, Any] = {
    "Key.tab": Key.tab,
    "Key.caps_lock": Key.caps_lock,
    "Key.shift": Key.shift,
    "Key.ctrl_l": Key.ctrl_l,
    "Key.cmd": Key.cmd,
    "Key.alt_l": Key.alt_l,
    "Key.space": Key.space,
    "Key.alt_gr": Key.alt_gr,
    "Key.ctrl_r": Key.ctrl_r,
    "Key.left": Key.left,
    "Key.up": Key.up,
    "Key.down": Key.down,
    "Key.right": Key.right,
    "Key.shift_r": Key.shift_r,
    "Key.enter": Key.enter,
    "Key.backspace": Key.backspace,
    "Key.esc": Key.esc,
    "Button.left": Button.left,
    "Button.right": Button.right,
    "Button.middle": Button.middle,
}


class Record:
    """
    Aufnahme von Maus- und Tastaturaktionen.
    Speichert Ereignisse intern als Liste von dicts:
      {
        "time": float,  # Sek. seit start
        "type": "click" | "scroll" | "key",
        # click:
        "button": "Button.left", "pressed": True/False, "x": int, "y": int
        # scroll:
        "dx": int, "dy": int, "x": int, "y": int
        # key:
        "key": "a" or "Key.enter", "pressed": True/False, "is_char": True/False
      }
    """

    def __init__(self) -> None:
        self.history_raw: List[Dict[str, Any]] = []
        self._stop_event = Event()
        self._record_thread: Optional[Thread] = None

        # listeners will be created on start to avoid stale state
        self.k_listener: Optional[ke.Listener] = None
        self.m_listener: Optional[mo.Listener] = None

        self.st_tm: float = 0.0

    # Listener callbacks -------------------------------------------------
    def _on_click(self, x: int, y: int, button: Any, pressed: bool) -> None:
        ev = {
            "time": time() - self.st_tm,
            "type": "click",
            "button": str(button),
            "pressed": bool(pressed),
            "x": int(x),
            "y": int(y),
        }
        self.history_raw.append(ev)

    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        ev = {
            "time": time() - self.st_tm,
            "type": "scroll",
            "dx": int(dx),
            "dy": int(dy),
            "x": int(x),
            "y": int(y),
        }
        self.history_raw.append(ev)

    def _on_press(self, key: Any) -> None:
        try:
            key_str = key.char
            is_char = True
        except AttributeError:
            key_str = str(key)
            is_char = False
        ev = {
            "time": time() - self.st_tm,
            "type": "key",
            "key": key_str,
            "pressed": True,
            "is_char": bool(is_char),
        }
        self.history_raw.append(ev)

    def _on_release(self, key: Any) -> None:
        try:
            key_str = key.char
            is_char = True
        except AttributeError:
            key_str = str(key)
            is_char = False
        ev = {
            "time": time() - self.st_tm,
            "type": "key",
            "key": key_str,
            "pressed": False,
            "is_char": bool(is_char),
        }
        self.history_raw.append(ev)

    # Recording control -------------------------------------------------
    def prepare_record_start(self) -> None:
        """Starte die Aufnahme in einem separaten Thread (non-blocking)."""
        if self._record_thread and self._record_thread.is_alive():
            logger.debug("Record.prepare_record_start: already recording")
            return
        self._stop_event.clear()
        self._record_thread = Thread(target=self._record_loop, daemon=True)
        self._record_thread.start()
        logger.debug("Record.prepare_record_start: recording thread started")

    def _record_loop(self) -> None:
        """Thread-Funktion: bringt Fenster in Vordergrund und startet Listener; blockiert bis stop."""
        try:
            proc = process_helper.ProcessHelper()
            proc.set_foreground_window()
        except Exception as ex:
            logger.debug(f"Record._record_loop: set_foreground_window failed: {ex}")

        self.st_tm = time()
        # create listeners
        self.m_listener = mo.Listener(on_click=self._on_click, on_scroll=self._on_scroll)
        self.k_listener = ke.Listener(on_press=self._on_press, on_release=self._on_release)

        # start listeners
        self.m_listener.start()
        self.k_listener.start()
        logger.debug("Record._record_loop: listeners started")
        # wait until stop requested
        self._stop_event.wait()
        # once stop requested, stop listeners
        try:
            if self.m_listener and self.m_listener.running:
                self.m_listener.stop()
                self.m_listener.join(timeout=1.0)
        except Exception:
            logger.debug("Record._record_loop: m_listener stop/join failed")
        try:
            if self.k_listener and self.k_listener.running:
                self.k_listener.stop()
                self.k_listener.join(timeout=1.0)
        except Exception:
            logger.debug("Record._record_loop: k_listener stop/join failed")
        logger.debug("Record._record_loop: listeners stopped")

    def record_stop(self) -> List[Dict[str, Any]]:
        """Stoppe Aufnahme, bereinige und liefere eine JSON-kompatible Event-Liste zur�ck."""
        if not self._record_thread:
            logger.debug("Record.record_stop: no active recording thread")
            return []

        # Signal for thread to stop
        self._stop_event.set()
        # Ensure thread finishes
        self._record_thread.join(timeout=2.0)

        # Normalize / dedupe consecutive equal events (except timestamps)
        cleaned: List[Dict[str, Any]] = []
        for ev in self.history_raw:
            if not cleaned or {k: v for k, v in ev.items() if k != "time"} != {
                k: v for k, v in cleaned[-1].items() if k != "time"
            }:
                cleaned.append(ev)

        # Save normalized history back and return
        self.history_raw = cleaned
        logger.debug(f"Record.record_stop: recorded {len(self.history_raw)} events")
        return list(self.history_raw)

    def save(self, path: str) -> None:
        """Save current recording to `path` as JSON."""
        try:
            with open(path, "w", encoding="utf8") as f:
                json.dump(self.history_raw, f, ensure_ascii=False, indent=2)
            logger.info(f"Recording saved to {path}")
        except Exception as ex:
            logger.error(f"Failed to save recording to {path}: {ex}")
            raise

    @staticmethod
    def load(path: str) -> List[Dict[str, Any]]:
        """Load a recording file and return event list (may be old tuple-format or new dict-format)."""
        try:
            with open(path, "r", encoding="utf8") as f:
                data = json.load(f)
        except Exception as ex:
            logger.error(f"Failed to load recording {path}: {ex}")
            raise

        # If old tuple-like format is detected, try to convert to dict format for compatibility
        if data and isinstance(data, list) and isinstance(data[0], list) or (data and isinstance(data[0], tuple)):
            converted: List[Dict[str, Any]] = []
            for t in data:
                # keep best-effort conversion based on observed tuple shapes
                try:
                    if len(t) >= 5 and isinstance(t[1], str) and t[1].startswith("Button."):
                        converted.append({
                            "time": float(t[0]),
                            "type": "click",
                            "button": t[1],
                            "pressed": bool(t[2]),
                            "x": int(t[3]),
                            "y": int(t[4]),
                        })
                    elif len(t) >= 5 and t[1] == "scroll":
                        converted.append({
                            "time": float(t[0]),
                            "type": "scroll",
                            "dy": int(t[2]),
                            "dx": 0,
                            "x": int(t[3]),
                            "y": int(t[4]),
                        })
                    elif len(t) >= 5 and t[1] == "key":
                        # old key format used (time, "key", keychar/str, pressed, is_char)
                        converted.append({
                            "time": float(t[0]),
                            "type": "key",
                            "key": t[2],
                            "pressed": bool(t[3]),
                            "is_char": bool(t[4]),
                        })
                    else:
                        logger.debug(f"Unknown tuple format while loading recording: {t}")
                except Exception:
                    logger.debug("Failed to convert old tuple event, skipping")
            return converted
        return data


class Replay:
    """
    Replaying events produced by Record (dict-format). Backwards compatibility is handled in load().
    """

    def __init__(self, path: str) -> None:
        try:
            self.recording: List[Dict[str, Any]] = Record.load(path)
        except Exception as ex:
            logger.error(f"Replay.__init__: failed to load recording: {ex}")
            raise

        self.length = len(self.recording)
        self.key_map = dict(_KEY_MAP)  # local copy to allow modifications
        self.keyboard = Controller_k()
        self.mouse = Controller_m()
        # Use Manager (existing class) to keep game loop integration
        try:
            self.robot = manager.Manager()
        except Exception:
            self.robot = None
            logger.debug("Replay: manager.Manager() creation failed; continuing without robot calls")

    def replay_run(self) -> None:
        """Run through the recording once, using recorded timestamps to space actions."""
        try:
            proc = process_helper.ProcessHelper()
            proc.set_foreground_window()
        except Exception as ex:
            logger.debug(f"Replay.replay_run: could not focus window: {ex}")

        prev_time = 0.0
        for ev in self.recording:
            try:
                t = float(ev.get("time", 0.0))
                delta = max(0.0, t - prev_time)
                prev_time = t

                ev_type = ev.get("type")
                x = ev.get("x")
                y = ev.get("y")

                # If coordinates available, move the mouse over the time delta
                if x is not None and y is not None and delta > 0:
                    mouse_helper.move_smooth(int(x), int(y), duration=delta)
                else:
                    # No coords or zero delta -> wait the elapsed time
                    if delta > 0:
                        sleep(delta)

                # Perform the actual event
                if ev_type == "click":
                    btn = ev.get("button")
                    pressed = bool(ev.get("pressed", True))
                    try:
                        btn_obj = self.key_map.get(btn, None) or _KEY_MAP.get(btn)
                        if btn_obj is None:
                            raise KeyError(btn)
                        if pressed:
                            self.mouse.press(btn_obj)
                        else:
                            self.mouse.release(btn_obj)
                    except KeyError:
                        logger.error(f"Unknown button during replay: {btn}")

                elif ev_type == "scroll":
                    dy = int(ev.get("dy", 0))
                    dx = int(ev.get("dx", 0))
                    try:
                        # pynput.mouse.Controller.scroll(dx, dy)
                        self.mouse.scroll(dx, dy)
                    except Exception as ex:
                        logger.debug(f"Scroll action failed: {ex}")

                elif ev_type == "key":
                    key_str = ev.get("key")
                    pressed = bool(ev.get("pressed", True))
                    is_char = bool(ev.get("is_char", False))
                    try:
                        if is_char:
                            if pressed:
                                self.keyboard.press(key_str)
                            else:
                                self.keyboard.release(key_str)
                        else:
                            key_obj = self.key_map.get(key_str, _KEY_MAP.get(key_str))
                            if key_obj is None:
                                raise KeyError(key_str)
                            if pressed:
                                self.keyboard.press(key_obj)
                            else:
                                self.keyboard.release(key_obj)
                    except KeyError:
                        logger.error(f"Unknown key during replay: {key_str}")
                else:
                    logger.error(f"Unknown event type in recording: {ev_type}")

                # Allow integration with the bot/manager loop after each action (non-fatal)
                try:
                    if self.robot is not None:
                        self.robot.game_manager(move=False)
                except Exception:
                    # swallow robot errors to prevent replay interruption
                    logger.debug("Replay: robot.game_manager call failed after action")
            except Exception as ex:
                logger.error(f"Replay: error processing event {ev}: {ex}")

    def add_key_mapping(self, key_str: str, key_obj: Any) -> None:
        """Add or override a key/button mapping used during replay."""
        self.key_map[key_str] = key_obj
        _KEY_MAP[key_str] = key_obj
