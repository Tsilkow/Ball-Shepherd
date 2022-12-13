from assignment_2_lib import take_a_photo, drive

# TODO: add imports and functions
import cv2
import numpy as np


def is_blue(color):
    tmp = (color[0]/255, color[1]/255, color[2]/255)
    #print(tmp)
    return (tmp[1]+tmp[2] < tmp[0]-0.25)


def forward_distance(photo):
    focal_length = 311200
    buffor = 2000

    hsv_photo = cv2.cvtColor(photo[:420, :], cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(hsv_photo, np.array([105, 100,  50]), np.array([135, 255, 255]))
    # mask_2 = cv2.inRange(hsv_photo, np.array([165, 100,  50]), np.array([179, 255, 255]))
    mask = mask_1# + mask_2
    center = (np.argmax(np.sum(mask, axis=0)), np.argmax(np.sum(mask, axis=1)))
    
    left  = center[1]
    right = center[1]
    while left  > 0              and mask[center[0], left ] > 0: left  -= 1
    while right < photo.shape[1] and mask[center[0], right] > 0: right += 1
    if left == right: return 0
    width = right-left+1
    result = int(round(focal_length/width))-buffor
    #print(f'Estimated distance={result} (from width={width}) assuming focal length={focal_length} and buffor={buffor}')
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
