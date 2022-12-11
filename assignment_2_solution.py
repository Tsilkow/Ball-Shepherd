from assignment_2_lib import take_a_photo, drive

# TODO: add imports and functions
import cv2
import numpy as np


def is_blue(color):
    tmp = (color[0]/255, color[1]/255, color[2]/255)
    #print(tmp)
    return (tmp[1]+tmp[2] < tmp[0]-0.25)


# Distance estimation is achieved by finding a blue ball on the vertical line going through
# the middle of the photo and then measuring its width at its widest point. Then distance is
# estimated by a matched parameter encompassing focal_length, step to distance ratio and
# small effects of the simulation. Buffor is subtracted from final prediciton to better fit
# the data
def forward_distance(photo):
    focal_length = 230000
    buffor = 300
    biggest_width = 0
    for x in range(0, photo.shape[0]):
        if not is_blue(photo[photo.shape[0]//2, photo.shape[1]//2]): raise ValueError
        bottom = photo.shape[1]//2
        top = photo.shape[1]//2
        while bottom > 0           and is_blue(photo[x, bottom]): bottom -= 1
        while top < photo.shape[1] and is_blue(photo[x, top   ]): top    += 1
        width = top-bottom+1
        if width > biggest_width: biggest_width = width
    if biggest_width == 0: return 0
    result = int(round(focal_length/biggest_width))-buffor
    #print(f'Estimated distance={result} (from width={best_width}) assuming focal length={focal_length} and buffor={buffor}')
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
