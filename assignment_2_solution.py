from assignment_2_lib import take_a_photo, drive

# TODO: add imports and functions
import cv2
import numpy as np


def is_blue(color):
    tmp = (color[0]/255, color[1]/255, color[2]/255)
    #print(tmp)
    return (tmp[1]+tmp[2] < tmp[0]-0.25)


def forward_distance(photo):
    focal_length = 211000
    buffor = 0#100
    best_height = 0
    for x in range(0, photo.shape[0]):
        if not is_blue(photo[photo.shape[0]//2, photo.shape[1]//2]): raise ValueError
        bottom = photo.shape[1]//2
        top = photo.shape[1]//2
        while bottom > 0           and is_blue(photo[x, bottom]): bottom -= 1
        while top < photo.shape[1] and is_blue(photo[x, top   ]): top    += 1
        height = top-bottom+1
        if height > best_height: best_height = height
    result = focal_length//best_height#-buffor
    print(f'Estimated distance={result} (from height={best_height}) assuming focal length={focal_length} and buffor={buffor}')
    if height > 100:
        cv2.imshow('vis', photo)
        cv2.waitKey()
        cv2.destroyAllWindows()
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
