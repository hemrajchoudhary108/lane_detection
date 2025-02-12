import cv2
import numpy as np

def region_of_interest(image, vertices):
    mask = np.zeros_like(image)

    if len(image.shape) > 2:
        channel_count = image.shape[2]
        mask_color = (255,) * channel_count
    else:
        mask_color = 255
    
    cv2.fillPoly(mask, vertices, mask_color)
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image

def cal_avg(values):
    """Calculate average value."""
    if not (type(values) == 'NoneType'):
        if len(values) > 0:
            n = len(values)
        else:
            n = 1
        return sum(values) / n

def separate_lines(lines):
    # Seperating left and right lines
    left_lines = []
    right_lines = []
    if lines is None:
        return left_lines, right_lines
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            if slope < 0:
                left_lines.append(line)
            else:
                right_lines.append(line)
    return left_lines, right_lines

def extrapolating_line(lines, lower_bound, upper_bound):
    slopes = []
    consts = []
    if (lines is not None and len(lines) != 0):
        for x1, y1, x2, y2 in lines[0]:
            slope = (y2 - y1) / (x2 - x1)
            const = y1 - slope * x1
            slopes.append(slope)
            consts.append(const)
        avg_slope = cal_avg(slopes)
        avg_const = cal_avg(consts)
        x1 = (lower_bound - avg_const) / avg_slope
        x2 = (upper_bound - avg_const) / avg_slope
        return int(x1), lower_bound, int(x2), upper_bound
        
def draw_con(img, lines):
    """Fill in lane area."""
    points = []
    for x1,y1,x2,y2 in lines[0]:
        points.append([x1,y1])
        points.append([x2,y2])
    for x1,y1,x2,y2 in lines[1]:
        points.append([x2,y2])
        points.append([x1,y1])

    points = np.array([points], dtype = 'int32')        
    cv2.fillPoly(img, points, (0,255,0))

def extrapolate_lane_image(image, lines, lower_bound, upper_bound):

    lane_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    left_lines, right_lines = separate_lines(lines)

    # Extrapolating left line
    left_line = extrapolating_line(left_lines, lower_bound, upper_bound)
    right_line = extrapolating_line(right_lines, lower_bound, upper_bound)

    if (left_line is not None and right_line is not None):
        lines = np.array([[left_line], [right_line]], dtype=np.int32)
        draw_con(lane_image, lines)

    return lane_image

def draw_lines(img, lines, color=[255, 0, 0], thickness = 2):
    """Utility for drawing lines."""
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """Utility for defining Line Segments."""
    lines = cv2.HoughLinesP(
        img, rho, theta, threshold, np.array([]),
        minLineLength = min_line_len, maxLineGap = max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype = np.uint8)
    draw_lines(line_img, lines)
    return line_img, lines

def process_image(image):
    
    # converting to the gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    roi = cv2.inRange(gray_image, 150, 255)
    # Selecting region of interest
    roi_vertices = np.array([[[100, 540], [900, 540], [525, 330], [440, 330]]])
    gray_select_roi = region_of_interest(roi, roi_vertices)

    # applying canny edge
    low_threshold = 50
    high_threshold = 150
    canny_image = cv2.Canny(gray_select_roi, low_threshold, high_threshold)

    # Applying Gaussian blur
    kernel = 5
    gaussian_image = cv2.GaussianBlur(canny_image, (kernel, kernel), 0)

    # Applying Hough Transform
    rho = 1
    theta = np.pi/180
    threshold = 100
    min_line_length = 50
    max_line_gap = 300
    hough, lines = hough_lines(gaussian_image, rho, theta, threshold, min_line_length, max_line_gap)

    # Drawing lines on the image
    lower_bound = 330
    upper_bound = 540
    lane_img = extrapolate_lane_image(image, lines, lower_bound, upper_bound)
    
    # Combining the original image with the lane image
    line_image = cv2.addWeighted(image, 1, lane_img, 0.4, 0.0)

    return line_image
