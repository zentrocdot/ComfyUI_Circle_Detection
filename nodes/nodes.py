#!/usr/bin/python

import numpy as np
import cv2
import torch
from PIL import Image, ImageDraw, ImageFont

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class CircleDetection:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold_canny_edge": ("INT", {"default": 50, "min": 0, "max": 2048}),
                "threshold_circle_center": ("INT", {"default": 30, "min": 0, "max": 2048}),
                "minR": ("INT", {"default": 1, "min": 0, "max": 2048}),
                "maxR": ("INT", {"default": 512, "min": 0, "max": 2048}),
                "dp": ("FLOAT", {"default": 1, "min": 0, "max": 1000}),
                "minDist": ("INT", {"default": 20, "min": 0, "max": 2048}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    #RETURN_NAMES = ("IMAGE",)
    FUNCTION = "circle_detection"
    #CATEGORY = "🧬 Tutorial Nodes"
    CATEGORY = "🧬 Object Detection Nodes"
    
    def draw_circles(self, img, detected_circles, debug):
        print("*** DRAW CIRCLES ***")
        print(type(img))
        newImg = img.copy()
        print(type(img))
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
                print(a,b,r)
                # Draw the circumference of the circle.
                cv2.circle(newImg, (a, b), r, COLOR_TUPLE, THICKNESS)
                # Draw a small circle of radius 1 to show the center.
                cv2.circle(newImg, (a, b), 1, COLOR_TUPLE, 3)
                # Print dimensions and radius.
                if debug: 
                    print("x:", a, "y", b, "r:", r)
        # Return image, co-ordinates and radius.
        #return img, (a, b, r)
        return newImg, (a, b, r)

    def pre_img(self, img):
        '''Preprocess image.'''
        print("*** PRE ***")
        # Set some file names.
        img_1st = "gray_original.jpg"
        img_2nd = "gray_blurred.jpg"
        # Convert image to grayscale.
        gray_org = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Write image to file.
        #if debug:
        cv2.imwrite(img_1st, gray_org)
        # Blur image using a 3x3 kernel.
        kernel = (3, 3)
        gray_blur = cv2.blur(gray_org, kernel)
        # Write image to file.
        #if debug:
        cv2.imwrite(img_2nd, gray_blur)
        # Return blurred gray image.
        return gray_blur

    def detect_circles(self, gray_blur, threshold_canny_edge, threshold_circle_center, minR, maxR, minDist, dp):
        '''Detect circles.'''
        print("*** DETECT CIRCLES ***")
        # Set some global variables. Circle Detection.
        #MINR = 1
        #MAXR = 512
        #THRESHOLD_CANNY_EDGE = 50
        #THRESHOLD_CIRCLE_CENTER = 30
        #DP = 1
        # Declare global variables
        # Get rows and columns from shape and calculate min dist.
        rows = gray_blur.shape[0]
        columns = gray_blur.shape[1]
        # Print rows and columns:
        #if debug:
        #    print("rows:", rows, "columns:", columns)
        # Calculate value of minDist.
        min_dist = int(((rows + columns) / 2) / 8)
        print(min_dist)
        # Print rows and columns:
        #if debug:
        #    print("minDist:", min_dist)
        # Apply a Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blur,
                       cv2.HOUGH_GRADIENT, dp=dp, minDist=min_dist,
                       param1=threshold_canny_edge,
                       param2=threshold_circle_center,
                       minRadius=minR, maxRadius=maxR)
        # Print detected data.
        #if debug:
        #    print("Detected circles:", detected_circles)
        # Return detected_circles.
        return detected_circles

    def post_img(self, img, detected_circles, debug):
        '''Postprocess image.'''
        print("*** PRE ***")
        # Draw circles.
        img, (a, b, r) = self.draw_circles(img, detected_circles, debug)
        # Return image and tuple.
        return img, (a, b, r)

    def circle_detection(self, image, threshold_canny_edge, threshold_circle_center, minR, maxR, minDist, dp):
        '''Main script function.'''
        print(type(image)) 
        debug = True
        # Read image.
        #img_input = cv2.imread(fn, cv2.IMREAD_COLOR)
        img_input = tensor2pil(image)
        print(type(img_input)) 
        img_input = np.asarray(img_input)
        print(type(img_input))
        # Preprocess image.
        gray_blur = self.pre_img(img_input)
        # Process image. Detect circles.
        detected_circles = self.detect_circles(gray_blur, threshold_canny_edge, threshold_circle_center, minR, maxR, minDist, dp)
        # Postrocess image.
        img_output, _ = self.post_img(img_input, detected_circles, debug)
        print(type(img_output))
        # Write image.
        #cv2.imwrite("detected_circle.jpg", img_output)
        img_output = Image.fromarray(img_output)
        print(type(img_output))
        image_out = pil2tensor(img_output)
        print(type(image_out))
        # Return None.
        return (image_out,)
