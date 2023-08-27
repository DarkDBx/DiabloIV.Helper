from ctypes import windll, c_ulong, c_ushort, c_long, c_short, POINTER, Structure, Union, byref, pointer, sizeof
from functools import wraps
from inspect import getcallargs
from time import sleep
from pytweening import easeOutQuad
from numpy import int32, int64, float32, float64
from numpy import random as nprandom
from random import random, randint, uniform
from math import dist, factorial
from win32con import WHEEL_DELTA, MOUSEEVENTF_WHEEL
from win32api import mouse_event


SendInput = windll.user32.SendInput
MapVirtualKey = windll.user32.MapVirtualKeyW


# Constants for failsafe check and pause
FAILSAFE = True
FAILSAFE_POINTS = [(0, 0)]
PAUSE = 0.1  # Tenth-second pause by default.


# Constants for the mouse button names
LEFT = "left"
MIDDLE = "middle"
RIGHT = "right"
PRIMARY = "primary"
SECONDARY = "secondary"


# Mouse Scan Code Mappings
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_RIGHTCLICK = MOUSEEVENTF_RIGHTDOWN + MOUSEEVENTF_RIGHTUP
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MIDDLECLICK = MOUSEEVENTF_MIDDLEDOWN + MOUSEEVENTF_MIDDLEUP


# KeyBdInput Flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004


# MapVirtualKey Map Types
MAPVK_VK_TO_CHAR = 2
MAPVK_VK_TO_VSC = 0
MAPVK_VSC_TO_VK = 1
MAPVK_VSC_TO_VK_EX = 3


# Keyboard Scan Code Mappings
KEYBOARD_MAPPING = {
    'escape': 0x01,
    'esc': 0x01,
    'f1': 0x3B,
    'f2': 0x3C,
    'f3': 0x3D,
    'f4': 0x3E,
    'f5': 0x3F,
    'f6': 0x40,
    'f7': 0x41,
    'f8': 0x42,
    'f9': 0x43,
    'f10': 0x44,
    'f11': 0x57,
    'f12': 0x58,
    'printscreen': 0xB7,
    'prntscrn': 0xB7,
    'prtsc': 0xB7,
    'prtscr': 0xB7,
    'scrolllock': 0x46,
    'pause': 0xC5,
    '`': 0x29,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    '-': 0x0C,
    '=': 0x0D,
    'backspace': 0x0E,
    'insert': 0xD2 + 1024,
    'home': 0xC7 + 1024,
    'pageup': 0xC9 + 1024,
    'pagedown': 0xD1 + 1024,
    # numpad
    'numlock': 0x45,
    'divide': 0xB5 + 1024,
    'multiply': 0x37,
    'subtract': 0x4A,
    'add': 0x4E,
    'decimal': 0x53,
    'numpadenter': 0x9C + 1024,
    'numpad1': 0x4F,
    'numpad2': 0x50,
    'numpad3': 0x51,
    'numpad4': 0x4B,
    'numpad5': 0x4C,
    'numpad6': 0x4D,
    'numpad7': 0x47,
    'numpad8': 0x48,
    'numpad9': 0x49,
    'numpad0': 0x52,
    # end numpad
    'tab': 0x0F,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    '[': 0x1A,
    ']': 0x1B,
    '\\': 0x2B,
    'del': 0xD3 + 1024,
    'delete': 0xD3 + 1024,
    'end': 0xCF + 1024,
    'capslock': 0x3A,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    ';': 0x27,
    "'": 0x28,
    'enter': 0x1C,
    'return': 0x1C,
    'shift': 0x2A,
    'shiftleft': 0x2A,
    'z': 0x2C,
    'x': 0x2D,
    'c': 0x2E,
    'v': 0x2F,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    ',': 0x33,
    '.': 0x34,
    '/': 0x35,
    'shiftright': 0x36,
    'ctrl': 0x1D,
    'ctrlleft': 0x1D,
    'win': 0xDB + 1024,
    'winleft': 0xDB + 1024,
    'alt': 0x38,
    'altleft': 0x38,
    ' ': 0x39,
    'space': 0x39,
    'altright': 0xB8 + 1024,
    'winright': 0xDC + 1024,
    'apps': 0xDD + 1024,
    'ctrlright': 0x9D + 1024,
    # arrow key scancodes can be different depending on the hardware,
    # so I think the best solution is to look it up based on the virtual key
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeya?redirectedfrom=MSDN
    'up': MapVirtualKey(0x26, MAPVK_VK_TO_VSC),
    'left': MapVirtualKey(0x25, MAPVK_VK_TO_VSC),
    'down': MapVirtualKey(0x28, MAPVK_VK_TO_VSC),
    'right': MapVirtualKey(0x27, MAPVK_VK_TO_VSC),
    'OEM_1':0xBA,  # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key
    'OEM_PLUS':0xBB,  # For any country/region, the '+' key
    'OEM_COMMA':0xBC,  # For any country/region, the ',' key
    'OEM_MINUS':0xBD,  # For any country/region, the '-' key
    'OEM_PERIOD':0xBE,  # For any country/region, the '.' key
    'OEM_2':0xBF,  # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key =
    'OEM_3':0xC0,  # Used for miscellaneous characters; it can vary by keyboard. = For the US standard keyboard, the '`~' key
    # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key
    'OEM_4':0xDB,
    'OEM_5':0xDC,  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the '\|' key
    'OEM_6':0xDD,  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the ']}' key
    'OEM_7':0xDE  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the 'single-quote/double-quote' key
}


# C struct redefinitions

PUL = POINTER(c_ulong)


class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class POINT(Structure):
    _fields_ = [("x", c_long),
                ("y", c_long)]


class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]


# Fail Safe and Pause implementation

class FailSafeException(Exception):
    pass


def failSafeCheck():
    if FAILSAFE and tuple(position()) in FAILSAFE_POINTS:
        raise FailSafeException(
            "PyDirectInput fail-safe triggered from mouse moving to a corner of the screen. To disable this " \
            "fail-safe, set pydirectinput.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
        )


def _handlePause(_pause):
    if _pause:
        assert isinstance(PAUSE, int) or isinstance(PAUSE, float)
        sleep(PAUSE)


# direct copy of _genericPyAutoGUIChecks()
def _genericPyDirectInputChecks(wrappedFunction):
    @wraps(wrappedFunction)
    def wrapper(*args, **kwargs):
        funcArgs = getcallargs(wrappedFunction, *args, **kwargs)

        failSafeCheck()
        returnVal = wrappedFunction(*args, **kwargs)
        _handlePause(funcArgs.get("_pause"))
        return returnVal

    return wrapper


# Helper Functions

def _to_windows_coordinates(x=0, y=0):
    display_width, display_height = size()

    # the +1 here prevents exactly mouse movements from sometimes ending up off by 1 pixel
    windows_x = (x * 65536) // display_width + 1
    windows_y = (y * 65536) // display_height + 1

    return windows_x, windows_y


# position() works exactly the same as PyAutoGUI. I've duplicated it here so that moveRel() can use it to calculate
# relative mouse positions.
def position(x=None, y=None):
    cursor = POINT()
    windll.user32.GetCursorPos(byref(cursor))
    return (x if x else cursor.x, y if y else cursor.y)


# size() works exactly the same as PyAutoGUI. I've duplicated it here so that _to_windows_coordinates() can use it 
# to calculate the window size.
def size():
    return (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))


########################################################################################
########################################################################################
# Main Mouse Functions #
########################################################################################

def isNumeric(val):
    return isinstance(val, (float, int, int32, int64, float32, float64))


def isListOfPoints(l):
    if not isinstance(l, list):
        return False
    try:
        isPoint = lambda p: ((len(p) == 2) and isNumeric(p[0]) and isNumeric(p[1]))
        return all(map(isPoint, l))
    except (KeyError, TypeError) as e:
        return False


class BezierCurve():
    @staticmethod
    def binomial(n, k):
        """Returns the binomial coefficient "n choose k" """
        return factorial(n) / float(factorial(k) * factorial(n - k))


    @staticmethod
    def bernsteinPolynomialPoint(x, i, n):
        """Calculate the i-th component of a bernstein polynomial of degree n"""
        return BezierCurve.binomial(n, i) * (x ** i) * ((1 - x) ** (n - i))


    @staticmethod
    def bernsteinPolynomial(points):
        """
        Given list of control points, returns a function, which given a point [0,1] returns
        a point in the bezier curve described by these points
        """
        def bern(t):
            n = len(points) - 1
            x = y = 0
            for i, point in enumerate(points):
                bern = BezierCurve.bernsteinPolynomialPoint(t, i, n)
                x += point[0] * bern
                y += point[1] * bern
            return x, y
        return bern


    @staticmethod
    def curvePoints(n, points):
        """
        Given list of control points, returns n points in the bezier curve,
        described by these points
        """
        curvePoints = []
        bernstein_polynomial = BezierCurve.bernsteinPolynomial(points)
        for i in range(n):
            t = i / (n - 1)
            curvePoints += bernstein_polynomial(t),
        return curvePoints


class HumanCurve():
    """
    Generates a human-like mouse curve starting at given source point,
    and finishing in a given destination point
    """
    def __init__(self, fromPoint, toPoint, **kwargs):
        self.fromPoint = fromPoint
        self.toPoint = toPoint
        self.points = self.generateCurve(**kwargs)


    def generateCurve(self, **kwargs):
        """
        Generates a curve according to the parameters specified below.
        You can override any of the below parameters. If no parameter is
        passed, the default value is used.
        """
        offsetBoundaryX = kwargs.get("offsetBoundaryX", 100)
        offsetBoundaryY = kwargs.get("offsetBoundaryY", 100)
        leftBoundary = kwargs.get("leftBoundary", min(self.fromPoint[0], self.toPoint[0])) - offsetBoundaryX
        rightBoundary = kwargs.get("rightBoundary", max(self.fromPoint[0], self.toPoint[0])) + offsetBoundaryX
        downBoundary = kwargs.get("downBoundary", min(self.fromPoint[1], self.toPoint[1])) - offsetBoundaryY
        upBoundary = kwargs.get("upBoundary", max(self.fromPoint[1], self.toPoint[1])) + offsetBoundaryY
        knotsCount = kwargs.get("knotsCount", 2)
        distortionMean = kwargs.get("distortionMean", 1)
        distortionStdev = kwargs.get("distortionStdev", 1)
        distortionFrequency = kwargs.get("distortionFrequency", 0.4)
        tween = kwargs.get("tweening", easeOutQuad)
        targetPoints = kwargs.get("targetPoints", 10)

        internalKnots = self.generateInternalKnots(leftBoundary,rightBoundary, \
            downBoundary, upBoundary, knotsCount)
        points = self.generatePoints(internalKnots)
        points = self.distortPoints(points, distortionMean, distortionStdev, distortionFrequency)
        points = self.tweenPoints(points, tween, targetPoints)
        return points


    def generateInternalKnots(self, \
        leftBoundary, rightBoundary, \
        downBoundary, upBoundary,\
        knotsCount):
        """
        Generates the internal knots used during generation of bezier curvePoints
        or any interpolation function. The points are taken at random from
        a surface delimited by given boundaries.
        Exactly knotsCount internal knots are randomly generated.
        """
        if not (isNumeric(leftBoundary) and isNumeric(rightBoundary) and
            isNumeric(downBoundary) and isNumeric(upBoundary)):
            raise ValueError("Boundaries must be numeric")
        if not isinstance(knotsCount, int) or knotsCount < 0:
            raise ValueError("knotsCount must be non-negative integer")
        if leftBoundary > rightBoundary:
            raise ValueError("leftBoundary must be less than or equal to rightBoundary")
        if downBoundary > upBoundary:
            raise ValueError("downBoundary must be less than or equal to upBoundary")

        knotsX = nprandom.choice(range(leftBoundary, rightBoundary), size=knotsCount)
        knotsY = nprandom.choice(range(downBoundary, upBoundary), size=knotsCount)
        knots = list(zip(knotsX, knotsY))
        return knots


    def generatePoints(self, knots):
        """
        Generates bezier curve points on a curve, according to the internal
        knots passed as parameter.
        """
        if not isListOfPoints(knots):
            raise ValueError("knots must be valid list of points")

        midPtsCnt = max( \
            abs(self.fromPoint[0] - self.toPoint[0]), \
            abs(self.fromPoint[1] - self.toPoint[1]), \
            2)
        knots = [self.fromPoint] + knots + [self.toPoint]
        return BezierCurve.curvePoints(midPtsCnt, knots)


    def distortPoints(self, points, distortionMean, distortionStdev, distortionFrequency):
        """
        Distorts the curve described by (x,y) points, so that the curve is
        not ideally smooth.
        Distortion happens by randomly, according to normal distribution,
        adding an offset to some of the points.
        """
        if not(isNumeric(distortionMean) and isNumeric(distortionStdev) and \
               isNumeric(distortionFrequency)):
            raise ValueError("Distortions must be numeric")
        if not isListOfPoints(points):
            raise ValueError("points must be valid list of points")
        if not (0 <= distortionFrequency <= 1):
            raise ValueError("distortionFrequency must be in range [0,1]")

        distorted = []
        for i in range(1, len(points)-1):
            x,y = points[i]
            delta = nprandom.normal(distortionMean, distortionStdev) if \
                random() < distortionFrequency else 0
            distorted += (x,y+delta),
        distorted = [points[0]] + distorted + [points[-1]]
        return distorted


    def tweenPoints(self, points, tween, targetPoints):
        """
        Chooses a number of points(targetPoints) from the list(points)
        according to tweening function(tween).
        This function in fact controls the velocity of mouse movement
        """
        if not isListOfPoints(points):
            raise ValueError("points must be valid list of points")
        if not isinstance(targetPoints, int) or targetPoints < 2:
            raise ValueError("targetPoints must be an integer greater or equal to 2")

        # tween is a function that takes a float 0..1 and returns a float 0..1
        res = []
        for i in range(targetPoints):
            index = int(tween(float(i)/(targetPoints-1)) * (len(points)-1))
            res += points[index],
        return res


def move_smooth(x, y, absolute=True, duration=0, randomize=4, delay_factor=[0.4, 0.6]):
    """
    Moves the mouse. If `absolute`, to position (x, y), otherwise move relative
    to the current position. If `duration` is non-zero, animates the movement.
    """
    x = int(x)
    y = int(y)
    from_point = position()
    distance = dist((x, y), from_point)
    offsetBoundaryX = max(10, int(0.08 * distance))
    offsetBoundaryY = max(10, int(0.08 * distance))
    targetPoints = min(6, max(3, int(0.004 * distance)))

    if not absolute:
        x = from_point[0] + x
        y = from_point[1] + y

    if type(randomize) is int:
        randomize = int(randomize)
        if randomize > 0:
            x = int(x) + randint(-randomize, +randomize)
            y = int(y) + randint(-randomize, +randomize)
    else:
        randomize = (int(randomize[0]), int(randomize[1]))
        if randomize[1] > 0 and randomize[0] > 0:
            x = int(x) + randint(-randomize[0], +randomize[0])
            y = int(y) + randint(-randomize[1], +randomize[1])
            
    human_curve = HumanCurve(from_point, (x, y), offsetBoundaryX=offsetBoundaryX, offsetBoundaryY=offsetBoundaryY, targetPoints=targetPoints)
    #duration = min(0.5, max(0.05, distance * 0.0004) * uniform(delay_factor[0], delay_factor[1]))
    delta = duration / len(human_curve.points)

    if duration:
        start_x = from_point[0]
        start_y = from_point[1]
        dx = x - start_x
        dy = y - start_y

        if dx == 0 and dy == 0:
            sleep(duration)
        else:
            for point in human_curve.points:
                moveRel(int(point[0]), int(point[1]), duration=delta)
    else:
        for point in human_curve.points:
            moveTo(int(point[0]), int(point[1]), duration=delta)


# Ignored parameters: duration, tween, logScreenshot
@_genericPyDirectInputChecks
def mouseDown(x=None, y=None, button=PRIMARY, duration=None, tween=None, logScreenshot=None, _pause=True):
    if not x is None or not y is None:
        moveTo(x, y)

    ev = None
    if button == PRIMARY or button == LEFT:
        ev = MOUSEEVENTF_LEFTDOWN
    elif button == MIDDLE:
        ev = MOUSEEVENTF_MIDDLEDOWN
    elif button == SECONDARY or button == RIGHT:
        ev = MOUSEEVENTF_RIGHTDOWN

    if not ev:
        raise ValueError('button arg to _click() must be one of "left", "middle", or "right", not %s' % button)

    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, ev, 0, pointer(extra))
    x = Input(c_ulong(0), ii_)
    SendInput(1, pointer(x), sizeof(x))


# Ignored parameters: duration, tween, logScreenshot
@_genericPyDirectInputChecks
def mouseUp(x=None, y=None, button=PRIMARY, duration=None, tween=None, logScreenshot=None, _pause=True):
    if not x is None or not y is None:
        moveTo(x, y)

    ev = None
    if button == PRIMARY or button == LEFT:
        ev = MOUSEEVENTF_LEFTUP
    elif button == MIDDLE:
        ev = MOUSEEVENTF_MIDDLEUP
    elif button == SECONDARY or button == RIGHT:
        ev = MOUSEEVENTF_RIGHTUP

    if not ev:
        raise ValueError('button arg to _click() must be one of "left", "middle", or "right", not %s' % button)

    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, ev, 0, pointer(extra))
    x = Input(c_ulong(0), ii_)
    SendInput(1, pointer(x), sizeof(x))


# Ignored parameters: duration, tween, logScreenshot
@_genericPyDirectInputChecks
def click(x=None, y=None, clicks=1, interval=0.0, button=PRIMARY, duration=None, tween=None, logScreenshot=None,
          _pause=True):
    if not x is None or not y is None:
        moveTo(x, y)

    ev = None
    if button == PRIMARY or button == LEFT:
        ev = MOUSEEVENTF_LEFTCLICK
    elif button == MIDDLE:
        ev = MOUSEEVENTF_MIDDLECLICK
    elif button == SECONDARY or button == RIGHT:
        ev = MOUSEEVENTF_RIGHTCLICK

    if not ev:
        raise ValueError('button arg to _click() must be one of "left", "middle", or "right", not %s' % button)

    for i in range(clicks):
        failSafeCheck()

        extra = c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, ev, 0, pointer(extra))
        x = Input(c_ulong(0), ii_)
        SendInput(1, pointer(x), sizeof(x))

        sleep(interval)


def leftClick(x=None, y=None, interval=0.1, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, LEFT, duration, tween, logScreenshot, _pause)


def rightClick(x=None, y=None, interval=0.1, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, RIGHT, duration, tween, logScreenshot, _pause)


def middleClick(x=None, y=None, interval=0.1, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, MIDDLE, duration, tween, logScreenshot, _pause)


def doubleClick(x=None, y=None, interval=0.1, button=LEFT, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 2, interval, button, duration, tween, logScreenshot, _pause)


def tripleClick(x=None, y=None, interval=0.1, button=LEFT, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 3, interval, button, duration, tween, logScreenshot, _pause)


def mouseScroll(clicks=0, delta_x=0, delta_y=0, delay_between_ticks=0):
    """
    A positive value indicates that the wheel was rotated forward, away from the user;
    A negative value indicates that the wheel was rotated backward, toward the user.
    One wheel click is defined as WHEEL_DELTA, which is 120.
    """
    if clicks > 0:
        increment = WHEEL_DELTA
    else:
        increment = WHEEL_DELTA * -1

    for _ in range(abs(clicks)):
        mouse_event(MOUSEEVENTF_WHEEL, delta_x, delta_y, increment, 0)
        sleep(delay_between_ticks)


# Ignored parameters: duration, tween, logScreenshot
# PyAutoGUI uses windll.user32.SetCursorPos(x, y) for this, which might still work fine in DirectInput 
# environments.
# Use the relative flag to do a raw win32 api relative movement call (no MOUSEEVENTF_ABSOLUTE flag), which may be more 
# appropriate for some applications. Note that this may produce inexact results depending on mouse movement speed.
@_genericPyDirectInputChecks
def moveTo(x=None, y=None, duration=0.5, tween=None, logScreenshot=False, _pause=True, relative=False):
    if not relative:
        x, y = position(x, y)  # if only x or y is provided, will keep the current position for the other axis
        x, y = _to_windows_coordinates(x, y)
        extra = c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(x, y, 0, (MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE), 0, pointer(extra))
        command = Input(c_ulong(0), ii_)
        SendInput(1, pointer(command), sizeof(command))
        sleep(duration)
    else:
        currentX, currentY = position()
        moveRel(x - currentX, y - currentY, duration=duration)


# Ignored parameters: duration, tween, logScreenshot
# move() and moveRel() are equivalent.
# Use the relative flag to do a raw win32 api relative movement call (no MOUSEEVENTF_ABSOLUTE flag), which may be more 
# appropriate for some applications.
@_genericPyDirectInputChecks
def moveRel(xOffset=None, yOffset=None, duration=0.5, tween=None, logScreenshot=False, _pause=True, relative=True):
    if not relative:
        x, y = position()
        if xOffset is None:
            xOffset = 0
        if yOffset is None:
            yOffset = 0
        moveTo(x + xOffset, y + yOffset, duration=duration)
    else:
        # When using MOUSEEVENTF_MOVE for relative movement the results may be inconsistent.
        # "Relative mouse motion is subject to the effects of the mouse speed and the two-mouse threshold values. A user
        # sets these three values with the Pointer Speed slider of the Control Panel's Mouse Properties sheet. You can 
        # obtain and set these values using the SystemParametersInfo function." 
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
        # https://stackoverflow.com/questions/50601200/pyhon-directinput-mouse-relative-moving-act-not-as-expected
        extra = c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(xOffset, yOffset, 0, MOUSEEVENTF_MOVE, 0, pointer(extra))
        command = Input(c_ulong(0), ii_)
        SendInput(1, pointer(command), sizeof(command))
        sleep(duration)


move = moveRel


# Missing feature: drag functions
def centerMap():
    mouse_event(0x0003, 0, 500, 0, 0)
    sleep(uniform(.2, .4))


########################################################################################
########################################################################################
# Main Keyboard Functions #
########################################################################################

# Ignored parameters: logScreenshot
# Missing feature: auto shift for special characters (ie. '!', '@', '#'...)
@_genericPyDirectInputChecks
def keyDown(key, logScreenshot=None, _pause=True):
    if not key in KEYBOARD_MAPPING or KEYBOARD_MAPPING[key] is None:
        return

    keybdFlags = KEYEVENTF_SCANCODE

    # Init event tracking
    insertedEvents = 0
    expectedEvents = 1

    # arrow keys need the extended key flag
    if key in ['up', 'left', 'down', 'right']:
        keybdFlags |= KEYEVENTF_EXTENDEDKEY
        # if numlock is on and an arrow key is being pressed, we need to send an additional scancode
        # https://stackoverflow.com/questions/14026496/sendinput-sends-num8-when-i-want-to-send-vk-up-how-come
        # https://handmade.network/wiki/2823-keyboard_inputs_-_scancodes,_raw_input,_text_input,_key_names
        if windll.user32.GetKeyState(0x90):
            # We need to press two keys, so we expect to have inserted 2 events when done
            expectedEvents = 2
            hexKeyCode = 0xE0
            extra = c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput(0, hexKeyCode, KEYEVENTF_SCANCODE, 0, pointer(extra))
            x = Input(c_ulong(1), ii_)

            # SendInput returns the number of event successfully inserted into input stream
            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput#return-value
            insertedEvents += SendInput(1, pointer(x), sizeof(x))

    hexKeyCode = KEYBOARD_MAPPING[key]
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, pointer(extra))
    x = Input(c_ulong(1), ii_)
    insertedEvents += SendInput(1, pointer(x), sizeof(x))

    return insertedEvents == expectedEvents


# Ignored parameters: logScreenshot
# Missing feature: auto shift for special characters (ie. '!', '@', '#'...)
@_genericPyDirectInputChecks
def keyUp(key, logScreenshot=None, _pause=True):
    if not key in KEYBOARD_MAPPING or KEYBOARD_MAPPING[key] is None:
        return

    keybdFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP

    # Init event tracking
    insertedEvents = 0
    expectedEvents = 1

    # arrow keys need the extended key flag
    if key in ['up', 'left', 'down', 'right']:
        keybdFlags |= KEYEVENTF_EXTENDEDKEY

    hexKeyCode = KEYBOARD_MAPPING[key]
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, pointer(extra))
    x = Input(c_ulong(1), ii_)

    # SendInput returns the number of event successfully inserted into input stream
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput#return-value
    insertedEvents += SendInput(1, pointer(x), sizeof(x))

    # if numlock is on and an arrow key is being pressed, we need to send an additional scancode
    # https://stackoverflow.com/questions/14026496/sendinput-sends-num8-when-i-want-to-send-vk-up-how-come
    # https://handmade.network/wiki/2823-keyboard_inputs_-_scancodes,_raw_input,_text_input,_key_names
    if key in ['up', 'left', 'down', 'right'] and windll.user32.GetKeyState(0x90):
        # We need to press two keys, so we expect to have inserted 2 events when done
        expectedEvents = 2
        hexKeyCode = 0xE0
        extra = c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, pointer(extra))
        x = Input(c_ulong(1), ii_)
        insertedEvents += SendInput(1, pointer(x), sizeof(x))

    return insertedEvents == expectedEvents


# Ignored parameters: logScreenshot
# nearly identical to PyAutoGUI's implementation
@_genericPyDirectInputChecks
def press(keys, presses=1, interval=0.05, logScreenshot=None, _pause=True):
    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys]  # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
        keys = lowerKeys
    interval = float(interval)

    # We need to press x keys y times, which comes out to x*y presses in total
    expectedPresses = presses * len(keys)
    completedPresses = 0

    for i in range(presses):
        for k in keys:
            failSafeCheck()
            downed = keyDown(k)
            upped = keyUp(k)
            # Count key press as complete if key was "downed" and "upped" successfully
            if downed and upped:
                completedPresses += 1

        sleep(interval)

    return completedPresses == expectedPresses


# Ignored parameters: logScreenshot
# nearly identical to PyAutoGUI's implementation
@_genericPyDirectInputChecks
def typewrite(message, interval=0.05, logScreenshot=None, _pause=True):
    interval = float(interval)
    for c in message:
        if len(c) > 1:
            c = c.lower()
        press(c, _pause=False)
        sleep(interval)
        failSafeCheck()


write = typewrite

# Missing feature: hotkey functions

