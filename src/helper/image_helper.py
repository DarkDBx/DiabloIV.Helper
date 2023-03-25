import win32gui
import cv2
import numpy
import math
import pyautogui
from PIL import ImageGrab

from helper import process_helper


class ImageHelper:
    def __init__(self):
        self.hwnd = process_helper.procHelp.get_hwnd()

    def get_pixel_color(self, debug :bool =False):
        """Get the color of per cursor selected pixel"""
        x, y = win32gui.GetCursorPos()
        r, g, b = pyautogui.screenshot().getpixel((x, y))
        if debug: print(r, g, b)
        return x, y, r, g, b

    def pixel_matches_color(self, x, y, exR, exG, exB, tolerance=0):
        r, g, b = pyautogui.screenshot().getpixel((x, y))
        if (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance):
            return True
        return False

    def pixel_color(self, x, y):
        r, g, b = pyautogui.screenshot().getpixel((x, y))
        return r,g,b
        
    def calculate_distance(self):
        location = self.get_img(50,200,1850,1000, '.\\assets\\target.png')
        if location != (-1, -1):
            dist = math.sqrt((location[1] - 960)**2 + (location[2] - 740)**2)
            return dist

    def __screen_grab(self, x,y,w,h):
        bbox = (x,y,w,h)
        img = ImageGrab.grab(bbox)
        return img

    def __template_matching(self, src, template, method):
        result = cv2.matchTemplate(src, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        location = [0, 0]
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            location = min_loc
        else:
            location = max_loc
        return location

    def __get_great_majority(self, list):
        '''Get the most frequently repeated key value in the list'''
        dict = {}
        for v in list:
            if v in dict.keys():
                dict[v] += 1
            else:
                dict[v] = 1
        key = max(dict, key=dict.get)
        return key, dict[key]

    def get_img(self, x,y,w,h, template, accurate=3):
        '''Search for images in the specified area'''
        image = self.__screen_grab(x,y,w,h)
        src = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        template = cv2.imread(template, 1)
        methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
        locations = []
        for method in methods:
            locations.append(self.__template_matching(src, template, method))
        location, count = self.__get_great_majority(locations)
        if count == accurate:
            return location
        return (-1, -1)
    

imgHelp = ImageHelper

