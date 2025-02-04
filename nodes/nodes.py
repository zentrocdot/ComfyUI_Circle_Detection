#!/usr/bin/python
'''Object detection node.'''
# pylint: disable=no-member
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=bare-except

# Import the Python modules.
import numpy as np
import cv2
import torch
from PIL import Image

# Tensor to PIL function.
def tensor2pil(image):
    '''Tensor to PIL image.'''
    # Return PIL image.
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor function.
def pil2tensor(image):
    '''PIL image to tensor.'''
    # Return tensor.
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class CircleDetection:
    '''Circle detection node.'''

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the input types.'''
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold_canny_edge": ("FLOAT", {"default": 50, "min": 0, "max": 2048}),
                "threshold_circle_center": ("FLOAT", {"default": 30, "min": 0, "max": 2048}),
                "minR": ("INT", {"default": 1, "min": 0, "max": 2048}),
                "maxR": ("INT", {"default": 512, "min": 0, "max": 2048}),
                "dp": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1000.0}),
                "minDist": ("FLOAT", {"default": 20.0, "min": 0.0, "max": 2048.0}),
                "color_tuple_circle": ("STRING", {"multiline": False, "default": "(255, 0, 255)"}),
                "color_tuple_bg": ("STRING", {"multiline": False, "default": "(255, 0, 0)"}),
                "color_tuple_fg": ("STRING", {"multiline": False, "default": "(0, 0, 255)"}),
                "thickness": ("INT", {"default": 2, "min": 0, "max": 256}),
                "exclude_circles": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "MASK", "STRING", "STRING")
    RETURN_NAMES = ("image_output", "image_mask", "mask", "data", "help")
    FUNCTION = "circle_detection"
    CATEGORY = "🧬 Circle Detection Nodes"
    OUTPUT_NODE = True

    def draw_circles(self, img, detected_circles, debug, color_tuple_str, color_tuple_bg, color_tuple_fg, thickness, exlist):
        '''Draw circles.'''
        def string2tuple(color_str):
            color_tuple = (0,0,0)
            try:
                stripStr = str(color_str).replace('(','').replace(')','').strip()
                rgb = stripStr.split(",")
                r, g, b = int(rgb[0].strip()), int(rgb[1].strip()), int(rgb[2].strip())
                color_tuple = (r, g, b)
            except:
                print("ERROR. Could not create color tuple!")
            return color_tuple
        # Create the color tuples.
        color_tuple = string2tuple(color_tuple_str)
        color_tuple_bg = string2tuple(color_tuple_bg)
        color_tuple_fg = string2tuple(color_tuple_fg)
        # Get dimension of iage.
        height, width, channels = img.shape
        blank_image = np.zeros((height, width, channels), np.uint8)
        maskImage = blank_image.copy()
        r_bg, g_bg, b_bg = color_tuple_bg
        blank_image[:,0:width] = (r_bg, g_bg, b_bg)
        # Set out string.
        outstr = ""
        # Copy image to a new image.
        newImg = img.copy()
        # Declare local variables.
        a, b, r = 0, 0, 0
        # Draw detected circles.
        if detected_circles is not None:
            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
            print(detected_circles)
            # Loop over the detected circles.
            count = 0
            for pnt in detected_circles[0, :]:
                count += 1
                if count not in exlist:
                    # Get the circle data.
                    a, b, r = pnt[0], pnt[1], pnt[2]
                    # Draw the circumference of the circle.
                    cv2.circle(newImg, (a, b), r, color_tuple, thickness)
                    cv2.putText(newImg, str(count), (a,b), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 4)
                    cv2.circle(blank_image, (a, b), r, color_tuple_fg, -1)
                    cv2.circle(maskImage, (a, b), r, (255,255,255), -1)
                    # Draw a small circle of radius 1 to show the center.
                    cv2.circle(newImg, (a, b), 1, color_tuple, 3)
                    # Print dimensions and radius.
                    if debug:
                        print("No.:", count, "x:", a, "y", b, "r:", r)
                        outstr = outstr + "No. " + str(count) + " x: " + str(a) + " y: " + str(b) + " r: " + str(r) + "\n"
        # Return image, co-ordinates and radius.
        return newImg, (a, b, r), outstr, blank_image, maskImage

    def pre_img(self, img):
        '''Preprocess image.'''
        # Convert image to grayscale.
        gray_org = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Blur image using a 3x3 kernel.
        kernel = (3, 3)
        gray_blur = cv2.blur(gray_org, kernel)
        # Return blurred gray image.
        return gray_blur

    def detect_circles(self, gray_blur, threshold_canny_edge, threshold_circle_center, minR, maxR, minDist, dp, debug):
        '''Detect circles.'''
        # Apply a Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blur,
                       cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist,
                       param1=threshold_canny_edge,
                       param2=threshold_circle_center,
                       minRadius=minR, maxRadius=maxR)
        # Print detected data.
        if debug:
            print("Detected circles:", detected_circles)
        # Return detected_circles.
        return detected_circles

    def post_img(self, img, detected_circles, debug, color_tuple, color_tuple_bg, color_tuple_fg, thickness, exlist):
        '''Postprocess image.'''
        # Draw circles.
        img, (a, b, r), outstr, blank_image, maskImage  = self.draw_circles(img, detected_circles, debug, color_tuple, color_tuple_bg, color_tuple_fg, thickness, exlist)
        # Return image and tuple.
        return img, (a, b, r), outstr, blank_image, maskImage

    def circle_detection(self, image, threshold_canny_edge, threshold_circle_center, minR, maxR, minDist, dp,
                         color_tuple_circle, color_tuple_bg, color_tuple_fg, thickness, exclude_circles):
        '''Main script function.'''
        if exclude_circles != "":
            inlist = exclude.split(",")
            exlist = list(map(str.strip, inlist))
            exlist = list(map(int, exlist))
        else:
            exlist = []
        # Print detection parameters.
        print("Threshold canny edge:", threshold_canny_edge)
        print("Threshold circle center:", threshold_circle_center)
        print("minR:", minR)
        print("maxR:", maxR)
        print("minDist:", minDist)
        print("dp:", dp)
        # Set the debug flag.
        debug = True
        # Create PIL image.
        img_input = tensor2pil(image)
        # Create numpy array.
        img_input = np.asarray(img_input)
        # Preprocess image.
        gray_blur = self.pre_img(img_input)
        # Process image. Detect circles.
        detected_circles = self.detect_circles(gray_blur, threshold_canny_edge, threshold_circle_center, minR, maxR, minDist, dp, debug)
        # Postrocess image.
        img_output, _, out_string, blank_image, maskImage = self.post_img(img_input, detected_circles, debug, color_tuple_circle, color_tuple_bg, color_tuple_fg, thickness, exlist)
        # Create output image.
        img_output = Image.fromarray(img_output)
        # Create tensor.
        image_out = pil2tensor(img_output)
        blank_image = pil2tensor(blank_image)
        maskImage = pil2tensor(maskImage)
        # Return None.
        channel = "red"
        channels = ["red", "green", "blue", "alpha"]
        mask = maskImage[:, :, :, channels.index(channel)]
        help_str = "threshold 100 → accurate recognition\n" + \
        "dp > 1.0 for deformed circles\n" + \
        "minDist → max(width, height) / 8\n" + \
        "minR → minimum radius in detection\n" + \
        "maxR → maximum radius in detection"
        # Return the return types.
        return (image_out, blank_image, mask, out_string, help_str)
