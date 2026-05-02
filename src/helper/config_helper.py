from typing import Any, Dict, Optional
from yaml import safe_load, safe_dump
from pathlib import Path
from io import open
import tempfile
import os

from helper import logging_helper

class ConfigError(Exception):
    """Spezielle Ausnahme fuer Konfigurationsfehler."""
    pass

def get_file_path() -> str:
    """
    Bestimmt den absoluten Pfad zur Konfigurationsdatei.
    Erwartet die Datei unter <project_root>/config/config.yml.
    """
    base_dir = Path(__file__).resolve().parents[1].parent  # zwei Ebenen hoch: src/helper -> src -> project root
    config_dir = base_dir / "config"
    return str(config_dir / "config.yml")

def ensure_config_exists(default: Optional[Dict[str, Any]] = None) -> None:
    """
    Stellt sicher, dass die Konfigurationsdatei existiert. Legt bei Bedarf ein Verzeichnis an
    und schreibt eine Default-Konfiguration (leeres Dict oder uebergebenes Default).
    """
    config_path = Path(get_file_path())
    try:
        if not config_path.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)
            data = default or {}
            write_config(data)
            logging_helper.log_info(f"Created default config at {config_path}")
    except Exception as ex:
        logging_helper.log_error(f"Failed to ensure config exists: {ex}")
        raise ConfigError(f"Failed to ensure config exists: {ex}")

def read_config() -> Dict[str, Any]:
    """
    Liest die YAML-Konfiguration und gibt sie als Dictionary zurueck.
    Falls Datei fehlt, wird eine ConfigError ausgeloest.
    Leere oder ungueltige YAML-Inhalte fuehren zu einem leeren Dict.
    """
    config_path = Path(get_file_path())
    if not config_path.exists():
        raise ConfigError(f"Configuration file not found at: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf8') as infile:
            data = safe_load(infile) or {}
            if not isinstance(data, dict):
                logging_helper.log_debug(f"Config file parsed to {type(data).__name__}, coercing to dict.")
                return {}
            return data
    except ConfigError:
        raise
    except Exception as ex:
        logging_helper.log_error(f"Failed to read config: {ex}")
        raise ConfigError(f"Failed to read config: {ex}")

def write_config(data: Dict[str, Any]) -> None:
    """
    Schreibt die komplette Konfiguration atomar in die config.yml.
    Verwendet einen tempor�ren File und os.replace um teilgeschriebene Dateien zu vermeiden.
    """
    config_path = Path(get_file_path())
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # safe_dump verwendet Standard-YAML-Dump, ensure unicode support
        yaml_text = safe_dump(data, default_flow_style=False, allow_unicode=True)
        # atomarer Schreibvorgang
        dirpath = str(config_path.parent)
        with tempfile.NamedTemporaryFile('w', delete=False, dir=dirpath, encoding='utf8') as tf:
            tf.write(yaml_text)
            temp_name = tf.name
        os.replace(temp_name, str(config_path))
        logging_helper.log_debug(f"Wrote config to {config_path}")
    except Exception as ex:
        logging_helper.log_error(f"Failed to write config: {ex}")
        # Versuche tempor�re Datei zu entfernen, wenn vorhanden
        try:
            if 'temp_name' in locals() and os.path.exists(temp_name):
                os.remove(temp_name)
        except Exception:
            pass
        raise ConfigError(f"Failed to write config: {ex}")

def save_config(item: str, value: Any) -> None:
    """
    Setzt oder aktualisiert einen einzelnen Key in der Konfiguration und schreibt die Datei.
    Beispiel: save_config('evade', 'space')
    """
    try:
        cfg = read_config()
    except ConfigError:
        cfg = {}
    if not isinstance(cfg, dict):
        cfg = {}
    cfg[item] = value
    write_config(cfg)

def get_config_value(key: str, default: Any = None) -> Any:
    """
    Liefert einen Konfigurationswert. Unterstuetzt verschachtelte Keys mit Punkt-Notation:
    z.B. get_config_value('graphics.fullscreen', False)
    """
    try:
        cfg = read_config()
    except ConfigError:
        return default

    if '.' in key:
        parts = key.split('.')
        cursor = cfg
        for p in parts:
            if isinstance(cursor, dict) and p in cursor:
                cursor = cursor[p]
            else:
                return default
        return cursor
    return cfg.get(key, default)
