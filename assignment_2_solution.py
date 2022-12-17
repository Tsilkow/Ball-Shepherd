from assignment_2_lib import take_a_photo, drive
import cv2
import numpy as np


# Helper function for finding visual center of an object
def visual_center(data):
    return int(round(np.average(np.indices(data.shape)[0], weights=data)))


def forward_distance(photo, return_center=False):
    focal_length = 311200 # parameter for estimating proportionality of pixel size to distance
    buffor = 1500 # parameter for keeping safe distance to ball when driving right to it

    # Prepare mask for red color
    hsv_photo = cv2.cvtColor(photo[:420, :], cv2.COLOR_RGB2HSV)
    mask_1 = cv2.inRange(hsv_photo, np.array([  0, 100,  50]), np.array([ 15, 255, 255]))
    mask_2 = cv2.inRange(hsv_photo, np.array([165, 100,  50]), np.array([179, 255, 255]))
    mask = mask_1 + mask_2
    
    # If no red object is visible, return None
    if np.sum(mask) == 0:
        if return_center: return None, None
        else: return None
    center = (visual_center(np.sum(mask, axis=1)), visual_center(np.sum(mask, axis=0)))

    # Find diameter of the ball
    left  = center[1]
    right = center[1]
    while left  > 0              and mask[center[0], left ] > 0: left  -= 1
    while right < photo.shape[1] and mask[center[0], right] > 0: right += 1
    if left == right: return 0
    width = right-left+1

    # Approximate distance
    result = int(round(focal_length/width))-buffor
    if return_center: return result, center[1] - photo.shape[1]//2
    return result


# Helper function for maintaing rhythm of rotating a car in place
def rotate_car(car, forward, clockwise=True):
    drive(car, forward, (forward*2-1) * (clockwise*2-1))
    return not forward


def find_a_ball(car):
    distance_threshold = 130
    centerness_threshold = 50
    
    drive_forward = False
    distance = None
    while True:
        view = take_a_photo(car)
        distance, left_right = forward_distance(view, True)
        if distance == None:
            drive_forward = rotate_car(car, drive_forward)
        elif abs(left_right) > centerness_threshold:
            drive_forward = rotate_car(car, drive_forward, (left_right < 0))
        elif distance > distance_threshold:
            drive(car, True, 0)
        else: break


# Function that returns center between two cylinders of specified colors within view; if it's unable to find two separate cylinders, it returns None
def find_cylinders(view, color):
    number_strips = 12 # parameter for number of strips to splitting the view for instance separation
    
    hsv_view = cv2.cvtColor(view[:420, :], cv2.COLOR_RGB2HSV)
    if color == 'green':
        mask = cv2.inRange(hsv_view, np.array([ 45, 100,  50]), np.array([ 75, 255, 255]))
    elif color == 'blue':
        mask = cv2.inRange(hsv_view, np.array([110, 100,  50]), np.array([140, 255, 255]))
    if np.amax(np.sum(mask, axis=1)) == 0: return None

    # divide the view into strips to find two seperated cylinders
    strip_presence = []
    strip_width = view.shape[1] // number_strips
    divide = None
    for x in range(0, view.shape[1], strip_width):
        strip = mask[:, x:x+strip_width]
        strip_presence.append(np.sum(strip))
        if divide == None and strip_presence[-1] > 0 : divide = -1
        elif divide == -1 and strip_presence[-1] == 0: divide = x+1

    # if unable to seperate color into two cylinders, return None -- as in no valid center
    if divide == -1: return None
    left_field  = np.sum(mask[:, :divide], axis=0)
    right_field = np.sum(mask[:, divide:], axis=0)

    # if less than two cylinders are visible, return None -- as in no valid center
    if np.amax(left_field) == 0 or np.amax(right_field) == 0: return None
    left_cylinder  = visual_center(left_field)
    right_cylinder = divide + visual_center(right_field)
    return int(round((left_cylinder + right_cylinder)/2 - view.shape[1]/2))


def move_a_ball(car):
    centerness_threshold = 50 # threshold for centerness of car's view on target
    forward_every_x_steps = 2 # how many turns to make before driving forward to keep the ball in car's bumper

    # Find the ball and get very close to it
    find_a_ball(car)
    for _ in range(5): drive(car, True, 0)

    steps_since_forward = 0
    # Find the blue cylinders, while keeping ball before the car
    while True:
        view = take_a_photo(car)
        if find_cylinders(view, 'blue') is not None: break
        if steps_since_forward >= forward_every_x_steps:
            drive(car, True, 0)
            steps_since_forward = 0
        else:
            drive(car, True, 1)
            steps_since_forward += 1
            
    # Drive towards the middle between blue cylinders and then green cylinders, while keeping the ball before the car
    while True:
        view = take_a_photo(car)
        left_right = find_cylinders(view, 'blue')
        if left_right == None: left_right = find_cylinders(view, 'green')
        if left_right == None: break
        if abs(left_right) < centerness_threshold or steps_since_forward >= forward_every_x_steps:
            drive(car, True, 0)
            steps_since_forward = 0
        else:
            rotate_car(car, True, (left_right < 0))
            steps_since_forward += 1
