from time import sleep
from pytweening import easeOutQuad
from typing import List, Tuple, Optional, Iterable
from numbers import Real
import numpy as np
from numpy import random as nprandom
from random import random, randint, uniform
from math import dist, factorial
from pydirectinput import position, moveTo
from win32con import WHEEL_DELTA, MOUSEEVENTF_WHEEL
from win32api import mouse_event

from helper import logging_helper

Point = Tuple[float, float]


def mouseScroll(clicks: int = 0, delta_x: int = 0, delta_y: int = 0, delay_between_ticks: float = 0.0) -> None:
    """
    Simulate mouse wheel scroll. `clicks` positive = forward, negative = backward.
    Each click corresponds to WHEEL_DELTA (120).
    """
    try:
        if clicks == 0:
            return
        increment = WHEEL_DELTA if clicks > 0 else -WHEEL_DELTA
        for _ in range(abs(int(clicks))):
            mouse_event(MOUSEEVENTF_WHEEL, int(delta_x), int(delta_y), int(increment), 0)
            if delay_between_ticks:
                sleep(float(delay_between_ticks))
    except Exception as ex:
        logging_helper.log_debug(f"mouseScroll failed: {ex}")


def isNumeric(val) -> bool:
    """True wenn val eine reelle Zahl (inkl. numpy-Zahlen) ist."""
    return isinstance(val, Real) or isinstance(val, (np.integer, np.floating))


def isListOfPoints(l) -> bool:
    """Validiert eine Liste von (x,y)-Punkten."""
    if not isinstance(l, (list, tuple)):
        return False
    try:
        def isPoint(p):
            return isinstance(p, (list, tuple)) and len(p) == 2 and isNumeric(p[0]) and isNumeric(p[1])
        return all(isPoint(p) for p in l)
    except Exception:
        return False


class BezierCurve:
    @staticmethod
    def binomial(n: int, k: int) -> float:
        """Returns the binomial coefficient "n choose k" """
        n, k = int(n), int(k)
        if k < 0 or k > n:
            return 0.0
        return factorial(n) / float(factorial(k) * factorial(n - k))

    @staticmethod
    def bernsteinPolynomialPoint(x: float, i: int, n: int) -> float:
        """Calculate the i-th component of a bernstein polynomial of degree n"""
        return BezierCurve.binomial(n, i) * (x ** i) * ((1 - x) ** (n - i))

    @staticmethod
    def bernsteinPolynomial(points: List[Point]):
        """
        Given list of control points, returns a function, which given t in [0,1] returns
        a point in the bezier curve described by these points
        """
        def bern(t: float) -> Point:
            n = len(points) - 1
            x = y = 0.0
            for i, point in enumerate(points):
                bp = BezierCurve.bernsteinPolynomialPoint(t, i, n)
                x += float(point[0]) * bp
                y += float(point[1]) * bp
            return x, y
        return bern

    @staticmethod
    def curvePoints(n: int, points: List[Point]) -> List[Point]:
        """
        Given list of control points, returns n points in the bezier curve described by these points.
        n must be >= 2.
        """
        n = max(2, int(n))
        if not isListOfPoints(points):
            raise ValueError("points must be a list of 2D points")
        res: List[Point] = []
        bern = BezierCurve.bernsteinPolynomial(points)
        for i in range(n):
            t = i / (n - 1)
            res.append(bern(t))
        return res


class HumanCurve:
    """
    Generates a human-like mouse curve starting at `fromPoint` and finishing at `toPoint`.
    """

    def __init__(self, fromPoint: Point, toPoint: Point, **kwargs):
        self.fromPoint = (float(fromPoint[0]), float(fromPoint[1]))
        self.toPoint = (float(toPoint[0]), float(toPoint[1]))
        self.points = self.generateCurve(**kwargs)

    def generateCurve(self, **kwargs) -> List[Point]:
        offsetBoundaryX = int(kwargs.get("offsetBoundaryX", 100))
        offsetBoundaryY = int(kwargs.get("offsetBoundaryY", 100))
        leftBoundary = int(kwargs.get("leftBoundary", min(self.fromPoint[0], self.toPoint[0])) - offsetBoundaryX)
        rightBoundary = int(kwargs.get("rightBoundary", max(self.fromPoint[0], self.toPoint[0])) + offsetBoundaryX)
        downBoundary = int(kwargs.get("downBoundary", min(self.fromPoint[1], self.toPoint[1])) - offsetBoundaryY)
        upBoundary = int(kwargs.get("upBoundary", max(self.fromPoint[1], self.toPoint[1])) + offsetBoundaryY)
        knotsCount = int(kwargs.get("knotsCount", 2))
        distortionMean = float(kwargs.get("distortionMean", 1.0))
        distortionStdev = float(kwargs.get("distortionStdev", 1.0))
        distortionFrequency = float(kwargs.get("distortionFrequency", 0.4))
        tween = kwargs.get("tweening", easeOutQuad)
        targetPoints = int(kwargs.get("targetPoints", 10))

        # Generate internal knots safely
        internalKnots = self.generateInternalKnots(leftBoundary, rightBoundary,
                                                   downBoundary, upBoundary, knotsCount)
        points = self.generatePoints(internalKnots)
        points = self.distortPoints(points, distortionMean, distortionStdev, distortionFrequency)
        points = self.tweenPoints(points, tween, targetPoints)
        return points

    def generateInternalKnots(self,
                              leftBoundary: int, rightBoundary: int,
                              downBoundary: int, upBoundary: int,
                              knotsCount: int) -> List[Point]:
        """
        Generates internal knots inside the provided boundaries.
        Returns empty list if range is invalid or knotsCount is zero.
        """
        if not (isNumeric(leftBoundary) and isNumeric(rightBoundary) and
                isNumeric(downBoundary) and isNumeric(upBoundary)):
            raise ValueError("Boundaries must be numeric")
        if not isinstance(knotsCount, int) or knotsCount < 0:
            raise ValueError("knotsCount must be non-negative integer")
        if leftBoundary > rightBoundary:
            raise ValueError("leftBoundary must be <= rightBoundary")
        if downBoundary > upBoundary:
            raise ValueError("downBoundary must be <= upBoundary")
        if knotsCount == 0:
            return []

        # If the integer range is too small, fall back to uniform random sampling
        try:
            rng = range(leftBoundary, rightBoundary)
            if len(rng) < 1:
                # fallback: uniform coordinates inside boundary
                xs = [uniform(leftBoundary, rightBoundary) for _ in range(knotsCount)]
                ys = [uniform(downBoundary, upBoundary) for _ in range(knotsCount)]
            else:
                xs = list(nprandom.choice(list(rng), size=knotsCount))
                ys = list(nprandom.choice(list(range(downBoundary, upBoundary)), size=knotsCount)) \
                    if downBoundary < upBoundary else [downBoundary] * knotsCount
        except Exception:
            # fallback robust generation
            xs = [uniform(leftBoundary, rightBoundary) for _ in range(knotsCount)]
            ys = [uniform(downBoundary, upBoundary) for _ in range(knotsCount)]

        knots = list(zip(xs, ys))
        return [(float(x), float(y)) for x, y in knots]

    def generatePoints(self, knots: List[Point]) -> List[Point]:
        """
        Generates bezier curve points from knots (including start/end).
        """
        if not isListOfPoints(knots):
            raise ValueError("knots must be a valid list of points")
        # midPtsCnt scales with the distance between endpoints, min 2
        midPtsCnt = max(
            abs(int(self.fromPoint[0] - self.toPoint[0])),
            abs(int(self.fromPoint[1] - self.toPoint[1])),
            2
        )
        control = [self.fromPoint] + knots + [self.toPoint]
        return BezierCurve.curvePoints(midPtsCnt, control)

    def distortPoints(self, points: List[Point], distortionMean: float, distortionStdev: float,
                      distortionFrequency: float) -> List[Point]:
        """
        Distorts intermediate points with a normal distribution based offset applied on y.
        """
        if not (isNumeric(distortionMean) and isNumeric(distortionStdev) and isNumeric(distortionFrequency)):
            raise ValueError("Distortions must be numeric")
        if not isListOfPoints(points):
            raise ValueError("points must be valid list of points")
        if not (0 <= distortionFrequency <= 1):
            raise ValueError("distortionFrequency must be in range [0,1]")

        if len(points) <= 2:
            return points

        distorted: List[Point] = []
        for i in range(1, len(points) - 1):
            x, y = points[i]
            delta = float(nprandom.normal(distortionMean, distortionStdev)) if random() < distortionFrequency else 0.0
            distorted.append((float(x), float(y + delta)))
        return [points[0]] + distorted + [points[-1]]

    def tweenPoints(self, points: List[Point], tween, targetPoints: int) -> List[Point]:
        """
        Selects targetPoints from points according to tweening function (velocity profile).
        """
        if not isListOfPoints(points):
            raise ValueError("points must be valid list of points")
        if not isinstance(targetPoints, int) or targetPoints < 2:
            raise ValueError("targetPoints must be an integer >= 2")

        res: List[Point] = []
        for i in range(targetPoints):
            idx = int(tween(float(i) / (targetPoints - 1)) * (len(points) - 1))
            res.append(points[idx])
        return res


def move_smooth(x: float, y: float, absolute: bool = True, duration: float = 0.0,
                randomize: Optional[Iterable[int]] = 4, delay_factor: Tuple[float, float] = (0.0, 0.0)) -> bool:
    """
    Smoothly move the mouse from current position to (x,y).
    - `absolute`: if False, x,y are relative offsets.
    - `duration`: total duration of the movement in seconds (optional).
    - `randomize`: int or (rx,ry) to jitter the destination.
    - `delay_factor`: optional tuple of min/max extra sleep after completed move.
    Returns True on success, False on failure.
    """
    try:
        x, y = int(x), int(y)
        from_point = position()
        if not isinstance(from_point, (list, tuple)) or len(from_point) < 2:
            logging_helper.log_debug("move_smooth: invalid current mouse position")
            return False
        from_x, from_y = int(from_point[0]), int(from_point[1])

        if not absolute:
            x += from_x
            y += from_y

        # Apply randomization
        if isinstance(randomize, int):
            x += randint(-randomize, randomize)
            y += randint(-randomize, randomize)
        elif isinstance(randomize, (tuple, list)) and len(randomize) == 2:
            x += randint(-int(randomize[0]), int(randomize[0]))
            y += randint(-int(randomize[1]), int(randomize[1]))

        # If target is same as current, nothing to do
        if x == from_x and y == from_y:
            return True

        distance_val = dist((from_x, from_y), (x, y))
        # Compute reasonable number of points for the curve
        targetPoints = max(3, min(12, int(max(3, distance_val / 25))))
        offsetBoundaryX = max(5, int(0.08 * distance_val))
        offsetBoundaryY = max(5, int(0.08 * distance_val))

        human_curve = HumanCurve(
            (from_x, from_y),
            (x, y),
            offsetBoundaryX=offsetBoundaryX,
            offsetBoundaryY=offsetBoundaryY,
            knotsCount=2,
            targetPoints=targetPoints,
            tweening=easeOutQuad
        )

        # If duration provided, split evenly; otherwise small random per-step pause
        steps = len(human_curve.points) or 1
        per_step = float(duration / steps) if duration and duration > 0 else 0.0

        for pt in human_curve.points:
            moveTo(int(pt[0]), int(pt[1]), duration=per_step)
            # small random micro pause to simulate human motion when no duration used
            if per_step == 0.0:
                sleep(uniform(0.005, 0.02))

        # optional extra delay after finishing move
        if delay_factor and isinstance(delay_factor, (tuple, list)) and len(delay_factor) == 2:
            extra = uniform(float(delay_factor[0]), float(delay_factor[1]))
            if extra > 0:
                sleep(extra)

        return True
    except Exception as ex:
        logging_helper.log_debug(f"move_smooth failed: {ex}")
        return False
