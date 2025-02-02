#!/usr/bin/python

import numpy as np
import cv2
import torch
from PIL import Image, ImageDraw, ImageFont

# Tensor to PIL
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class CircleDetection:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    #RETURN_NAMES = ("IMAGE",)
    #FUNCTION = "draw_overlay_text"
    FUNCTION = "circle_detection"
    CATEGORY = "🧩 Tutorial Nodes"

    def draw_circles(self, img, detected_circles):
        COLOR_TUPLE = (255, 0, 255)
        THICKNESS = 5
        # Declare local variables.
        a, b, r = 0, 0, 0
        # Draw detected circles.
        if detected_circles is not None:
            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
            # loop over the detected circles.
            for pnt in detected_circles[0, :]:
                # Get the circle data.
                a, b, r = pnt[0], pnt[1], pnt[2]
                # Draw the circumference of the circle.
                cv2.circle(img, (a, b), r, COLOR_TUPLE, THICKNESS)
                # Draw a small circle of radius 1 to show the center.
                cv2.circle(img, (a, b), 1, COLOR_TUPLE, 3)
                # Print dimensions and radius.
                #print("x:", a, "y", b, "r:", r)
        # Return image, co-ordinates and radius.
        return img, (a, b, r)

    def pre_img(self, img):
        '''Preprocess image.'''
        # Set some file names.
        #img_1st = "gray_original.jpg"
        #img_2nd = "gray_blurred.jpg"
        # Convert image to grayscale.
        gray_org = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Write image to file.
        #if debug:
        #    cv2.imwrite(img_1st, gray_org)
        # Blur image using a 3x3 kernel.
        kernel = (3, 3)
        gray_blur = cv2.blur(gray_org, kernel)
        # Write image to file.
        #if debug:
        #    cv2.imwrite(img_2nd, gray_blur)
        # Return blurred gray image.
        return gray_blur

    def detect_circles(self, gray_blur):
        '''Detect circles.'''
        # Set some global variables. Circle Detection.
        MINR = 1
        MAXR = 512
        THRESHOLD_CANNY_EDGE = 50
        THRESHOLD_CIRCLE_CENTER = 30
        DP = 1
        # Declare global variables
        # Get rows and columns from shape and calculate min dist.
        rows = gray_blur.shape[0]
        columns = gray_blur.shape[1]
        # Print rows and columns:
        #if debug:
        #    print("rows:", rows, "columns:", columns)
        # Calculate value of minDist.
        min_dist = int(((rows + columns) / 2) / 8)
        # Print rows and columns:
        #if debug:
        #    print("minDist:", min_dist)
        # Apply a Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blur,
                       cv2.HOUGH_GRADIENT, dp=DP, minDist=min_dist,
                       param1=THRESHOLD_CANNY_EDGE,
                       param2=THRESHOLD_CIRCLE_CENTER,
                       minRadius=MINR, maxRadius=MAXR)
        # Print detected data.
        #if debug:
        #    print("Detected circles:", detected_circles)
        # Return detected_circles.
        return detected_circles

    def post_img(self, img, detected_circles):
        '''Postprocess image.'''
        # Draw circles.
        img, (a, b, r) = draw_circles(img, detected_circles)
        # Print dimensions and radius.
        #print("a:", a, "b:", b, "r:", r)
        # Return image and tuple.
        return img, (a, b, r)

    def circle_detection(self, image):
        '''Main script function.'''
        # Read image.
        #img_input = cv2.imread(fn, cv2.IMREAD_COLOR)
        # Preprocess image.
        gray_blur = pre_img(img_input)
        # Process image. Detect circles.
        detected_circles = detect_circles(gray_blur)
        # Postrocess image.
        img_output, _ = post_img(img_input, detected_circles)
        # Write image.
        #cv2.imwrite("detected_circle.jpg", img_output)
        # Return None.
        return (image_out,)

    def draw_overlay_text(self, image_width, image_height, text,
                   font_size, font_color, background_color):
        # Create a new PIL image
        new_img = Image.new("RGBA", (image_width, image_height), background_color)
        draw = ImageDraw.Draw(new_img)
        # Define font
        font = ImageFont.truetype("arial.ttf", size=font_size)
        # Get the image center
        image_center_x = image_width/2
        image_center_y = image_height/2
        # Draw the text, mm = text center
        draw.text((image_center_x, image_center_y), text, fill=font_color, font=font, anchor="mm")
        # Convert the PIL image to a torch tensor
        image_out = pil2tensor(new_img)
        return (image_out,)
