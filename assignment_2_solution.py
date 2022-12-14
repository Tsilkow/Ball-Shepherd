from assignment_2_lib import take_a_photo, drive

# TODO: add imports and functions
import cv2
import numpy as np


def forward_distance(photo, return_center=False):
    focal_length = 311200
    buffor = 2000

    hsv_photo = cv2.cvtColor(photo[:420, :], cv2.COLOR_RGB2HSV)
    mask_1 = cv2.inRange(hsv_photo, np.array([  0, 100,  50]), np.array([ 15, 255, 255]))
    mask_2 = cv2.inRange(hsv_photo, np.array([165, 100,  50]), np.array([179, 255, 255]))
    mask = mask_1 + mask_2
    center = (np.argmax(np.sum(mask, axis=1)), np.argmax(np.sum(mask, axis=0)))
    #print(f'center = {center}')
    #mask[center[0], center[1]] = 0
    #cv2.imshow('a', photo[:420, :])
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    if np.sum(mask) == 0:
        if return_center: return None, None
        else: return None
    
    left  = center[1]
    right = center[1]
    #print(f'left, right={left, right}, {mask[left , center[1]]}')
    while left  > 0              and mask[center[0], left ] > 0: left  -= 1
    while right < photo.shape[1] and mask[center[0], right] > 0: right += 1
    #print(f'left, right={left, right}')
    if left == right: return 0
    width = right-left+1
    result = int(round(focal_length/width))-buffor
    #print(f'Estimated distance={result} (from width={width}) assuming focal length={focal_length} and buffor={buffor}')
    if return_center: return result, center[1] - photo.shape[1]//2
    return result


def rotate_car(car, forward, clockwise=True):
    #print(f'forward={forward}, clockwise={clockwise}')
    #print(f'forward={forward}, steer={(forward*2-1) * (clockwise*2-1) * -1}')
    drive(car, forward, (forward*2-1) * (clockwise*2-1) * -1)
    return not forward


def find_a_ball(car):
    distance_threshold = 140
    centerness_threshold = 50
    
    drive_forward = False
    distance = None
    while distance == None or distance > distance_threshold:
        view = take_a_photo(car)
        #cv2.imshow('a', view)
        #cv2.waitKey()
        #cv2.destroyAllWindows()
        distance, left_right = forward_distance(view, True)
        if distance == None:
            #print(f'No ball visible', end='\r')
            drive_forward = rotate_car(car, drive_forward)
        else:
            #print(f'Estimated distance={distance:5}, left_right={left_right:3}', end='\r')
            if abs(left_right) < centerness_threshold: drive(car, True, 0)
            else: rotate_car(car, False, (left_right > 0))
    #print('\n')


def move_a_ball(car):
    # TODO: you should write this function using
    # - take_a_photo(car)
    # - drive(car, forward, direction)
    pass
