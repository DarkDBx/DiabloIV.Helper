from time import sleep
from pytweening import easeOutQuad
from numpy import int32, int64, float32, float64
from numpy import random as nprandom
from random import random, randint
from math import dist, factorial
from pydirectinput import position, moveRel, moveTo
from win32con import WHEEL_DELTA, MOUSEEVENTF_WHEEL
from win32api import mouse_event


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

