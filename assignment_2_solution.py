from assignment_2_lib import take_a_photo, drive

# TODO: add imports and functions
import cv2
import numpy as np


def array_center(data):
    return int(round(np.average(np.indices(data.shape)[0], weights=data)))


def forward_distance(photo, return_center=False):
    focal_length = 311200
    buffor = 2000

    hsv_photo = cv2.cvtColor(photo[:420, :], cv2.COLOR_RGB2HSV)
    mask_1 = cv2.inRange(hsv_photo, np.array([  0, 100,  50]), np.array([ 15, 255, 255]))
    mask_2 = cv2.inRange(hsv_photo, np.array([165, 100,  50]), np.array([179, 255, 255]))
    mask = mask_1 + mask_2
    if np.sum(mask) == 0:
        if return_center: return None, None
        else: return None
    center = (array_center(np.sum(mask, axis=1)), array_center(np.sum(mask, axis=0)))
    # print(f'center = {center}')
    # photo[center[0], center[1]] = 0
    # show_mask(photo)
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
    drive(car, forward, (forward*2-1) * (clockwise*2-1))
    return not forward


def find_a_ball(car):
    distance_threshold = 130
    centerness_threshold = 50
    
    drive_forward = False
    distance = None
    while True:
        view = take_a_photo(car)
        #cv2.imshow('a', view)
        #cv2.waitKey()
        distance, left_right = forward_distance(view, True)
        if distance == None:
            #print(f'No ball visible', end='\r')
            drive_forward = rotate_car(car, drive_forward)
        elif abs(left_right) > centerness_threshold:
            #print(f'Estimated distance={distance:5}, left_right={left_right:3}', end='\r')
            drive_forward = rotate_car(car, drive_forward, (left_right < 0))
        elif distance > distance_threshold:
            #print(f'Estimated distance={distance:5}, left_right={left_right:3}', end='\r')
            drive(car, True, 0)
        else: break
    #print('\n')


def show(car):
    photo = take_a_photo(car)
    cv2.imshow('a', photo)
    cv2.waitKey()


def show_mask(mask):
    cv2.imshow('a', mask)
    cv2.waitKey()


def find_pillars(view, color):
    number_strips = 12
    
    hsv_view = cv2.cvtColor(view[:420, :], cv2.COLOR_RGB2HSV)
    if color == 'green':
        mask = cv2.inRange(hsv_view, np.array([ 45, 100,  50]), np.array([ 75, 255, 255]))
    elif color == 'blue':
        mask = cv2.inRange(hsv_view, np.array([110, 100,  50]), np.array([140, 255, 255]))
    if np.amax(np.sum(mask, axis=1)) == 0: return None

    strip_presence = []
    strip_width = view.shape[1] // number_strips
    divide = None
    for x in range(0, view.shape[1], strip_width):
        strip = mask[:, x:x+strip_width]
        strip_presence.append(np.sum(strip))
        if divide == None and strip_presence[-1] > 0 : divide = -1
        elif divide == -1 and strip_presence[-1] == 0: divide = x+1
    #print(f'divide={divide} | {strip_presence}')
    if divide == -1: return None
    left_field  = np.sum(mask[:, :divide], axis=0)
    right_field = np.sum(mask[:, divide:], axis=0)
    if np.amax(left_field) == 0 or np.amax(right_field) == 0:
        #print(f'left_field={left_field} | right_field={right_field}')
        #show_mask(view)
        return None
    left_pillar  = array_center(left_field)
    right_pillar = divide + array_center(right_field)
    #print(left_pillar, right_pillar)
    view[:, divide] = [0, 0, 0, 255]
    view[:, left_pillar] = [255, 0, 0, 255]
    view[:, right_pillar] = [0, 255, 0, 255]
    view[:, (left_pillar + right_pillar)//2] = [255, 255, 0, 255]
    #show_mask(view)
    #print(int(round((left_pillar + right_pillar)/2 - view.shape[1]/2)))
    return int(round((left_pillar + right_pillar)/2 - view.shape[1]/2))


def move_a_ball(car):
    centerness_threshold = 50
    forward_every_x_steps = 2

    #show(car)
    find_a_ball(car)
    for _ in range(5): drive(car, True, 0)
    while True:
        view = take_a_photo(car)
        #show_mask(view)
        if find_pillars(view, 'blue') is not None: break
        drive(car, True, 1)
        drive(car, True, 0)

    # show(car)
    steps_since_forward = 0
    while True:
        view = take_a_photo(car)
        left_right = find_pillars(view, 'blue')
        # print(f'blue pillars: {left_right}')
        if left_right == None:
            left_right = find_pillars(view, 'green')
            # print(f'green pillars: {left_right}')
        if left_right == None: break
        if abs(left_right) < centerness_threshold or steps_since_forward > forward_every_x_steps:
            drive(car, True, 0)
            steps_since_forward = 0
        else:
            rotate_car(car, True, (left_right < 0))
            steps_since_forward += 1
        # show(car)
