from assignment_2_lib import take_a_photo, drive

# TODO: add imports and functions
import cv2
import numpy as np


def is_blue(color):
    tmp = (color[0]/255, color[1]/255, color[2]/255)
    #print(tmp)
    return (tmp[1]+tmp[2] < tmp[0]-0.25)


def forward_distance(photo):
    print(photo.shape)
    best_height = 0
    for x in range(photo.shape[0]):
        if not is_blue(photo[x, photo.shape[1]//2]): continue
        #print(f'There\'s a blue pixel at ({x}, 0)): {photo[x, photo.shape[1]//2]}')
        #photo[x, photo.shape[1]//2] = np.array([255, 0, 0, 255])
        bottom = photo.shape[1]//2
        top = photo.shape[1]//2
        while bottom > 0           and is_blue(photo[x, bottom]): bottom -= 1
        while top < photo.shape[1] and is_blue(photo[x, top   ]): top    += 1
        #photo[x, bottom:top] = np.array([255, 0, 0, 255])
        height = top-bottom+1
        #print(f'At x={x} heighest centered blue segment with top at {top} and bottom at {bottom} has height= {height}.')
        if height > best_height: best_height = height
    result = 207500//best_height
    print(result)
    return result


def find_a_ball(car):
    # TODO: you should write this function using
    # - take_a_photo(car)
    # - drive(car, forward, direction)
    pass


def move_a_ball(car):
    # TODO: you should write this function using
    # - take_a_photo(car)
    # - drive(car, forward, direction)
    pass
