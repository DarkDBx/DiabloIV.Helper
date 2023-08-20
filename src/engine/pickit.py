from logging import info
from time import sleep
from random import randint

from helper import input_helper, image_helper


IMAGE_DIR = ".\\assets\\pickit\\"


def get_ref_location(ref_img):
    x, y = image_helper.locate_needle(IMAGE_DIR + ref_img, loctype='c', region=(400, 50, 1500, 870))

    return x, y


def left_click(self, x=None, y=None, a=-5,b=35,c=-5,d=5):
    '''Randomized left click'''
    if x == None or y == None:
        input_helper.leftClick()
    else:
        ex = randint(a, b)
        fx = x + ex
        ey = randint(c, d)
        fy = y + ey
        input_helper.leftClick(fx, fy)


def pick_it():
    '''Looking for some loot and grab it'''
    item_image_array = [["a.png"], ["e.png"], ["i.png"],
            ["o.png"], ["u.png"], ["ancestral.png"], ["cinder.png"]]
    item_color_array = [[1,4, 248,128,5, 50], [1,4, 216,166,120, 50], [1,4, 234,236,10, 50], [1,4, 215,164,198, 50]]

    for i in range(6):
        x, y = get_ref_location(item_image_array[i][0])

        if (x > -1 and y > -1):
            if i == 6:
                n = range(3, 3)
            elif i == 5:
                n = range(2, 2)
            else:
                n = range(1)

            for j in n:
                color_value = image_helper.pixel_matches_color(x+item_color_array[j][0], 
                        y+item_color_array[j][1], item_color_array[j][2],
                        item_color_array[j][3], item_color_array[j][4], item_color_array[j][5])
                
                if color_value == True:
                    break

    if (x > -1 and y > -1) and color_value == True:
        left_click(x+12,y+3, -2,8,-2,2)
        info('Picked item at coords ' + str(x) + str(y))
        sleep(2)
        return True
    return False

