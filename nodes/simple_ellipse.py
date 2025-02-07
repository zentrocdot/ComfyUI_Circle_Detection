#!/usr/bin/python
'''Object detection node.'''
# pylint: disable=too-many-locals
# pylint: disable=bare-except
# pylint: disable=no-member
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-arguments
# pylint: disable=unused-variable
# pylint: disable=too-many-nested-blocks

# Import the Python modules.
from PIL import Image
import numpy as np
import cv2
import torch

# Convert Tensor to PIL function.
def tensor2pil(image):
    '''Tensor to PIL image.'''
    # Return a PIL image.
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor function.
def pil2tensor(image):
    '''PIL image to Tensor.'''
    # Return a tensor.
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# -----------------------
# Function string2tuple()
# -----------------------
def string2tuple(color_str):
    '''String to color tuple.'''
    # Initialise the color tuple.
    color_tuple = (0,0,0)
    try:
        stripStr = str(color_str).replace('(','').replace(')','').strip()
        rgb = stripStr.split(",")
        r, g, b = int(rgb[0].strip()), int(rgb[1].strip()), int(rgb[2].strip())
        color_tuple = (r, g, b)
    except:
        print("ERROR. Could not create color tuple!")
        color_tuple = (128,128,128)
    return color_tuple

# ++++++++++++++++++++++
# Class EllipseDetection
# ++++++++++++++++++++++
class EllipseDetection:
    '''Ellipse detection node.'''

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the node input types.'''
        return {
            "required": {
                "image": ("IMAGE",),
                "number_sections": ("INT", {"default": 1, "min": 1, "max": 256, "step": 1}),
                "div": ("FLOAT", {"default": 0.5, "min": 0, "max": 10, "step": 0.01}),
                "eps": ("FLOAT", {"default": 0.01, "min": 0.01, "max": 10, "step": 0.01}),
                "contour_switch": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "color_tuple_ellipse": ("STRING", {"multiline": False, "default": "(255, 0, 255)"}),
                "thickness": ("INT", {"default": 2, "min": 1, "max": 256}),
                "numbering": ("BOOLEAN", {"default": True, "label_on": "on", "label_off": "off"}),
                "number_size": ("INT", {"default": 1, "min": 1, "max": 256}),
            },
            "optional": {
                "exclude_circles": ("STRING", {"forceInput": True}),
            }
        }

    # Set the ComfyUI related variables.
    RETURN_TYPES = ("IMAGE", "MASK", "MASK",)
    RETURN_NAMES = ("image_output", "standard_mask", "inverted_mask",)
    FUNCTION = "ellipse_detection"
    CATEGORY = "🧬 Circle Detection Nodes"
    DESCRIPTION = "Mathematical ellipse detection using OpenCV."
    OUTPUT_NODE = True

    def detect_ellipse(self, image, thickness, DIV, EPSILON,
                       number_sides, number_size, numbering,
                       color_tuple_ellipse, contour_switch, exlist):
        '''Detect ellipse.'''
        color_ellipse = string2tuple(color_tuple_ellipse)
        # Set PI to 16 places.
        PI = 3.1415926535897932
        # Copy image.
        imgNEW = image.copy()
        # Get the dimensions of the image.
        height, width, channels = imgNEW.shape
        # Calculate the main area.
        main_area = int(height * width)
        # Create a new mask.
        imgMask = np.zeros((height, width, channels), np.uint8)
        # Convert image to grayscale.
        gray = cv2.cvtColor(imgNEW, cv2.COLOR_BGR2GRAY)
        # Convert image to blur.
        blur = cv2.medianBlur(gray, 11)
        # Convert image to binary image.
        _, binary = cv2.threshold(
            blur, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        # Find all the contours in the image.
        contours, _ = cv2.findContours(
            binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        # Print number of contours.
        print("Number contours:", len(contours))
        # Set counter.
        count = 0
        # Loop through the individual contours.
        for cnt in contours:
            # Calculate the area related to the contour.
            area_contour = cv2.contourArea(cnt)
            # Approximate the contour to a polygon.
            perimeter = cv2.arcLength(cnt, True)
            approximation = cv2.approxPolyDP(cnt, EPSILON * perimeter, True)
            # Sort the polygons out.
            if len(approximation) >= number_sides:
                # Get the dimensions of the bounding box.
                x, y, w, h = cv2.boundingRect(approximation)
                # Calculate the inner area.
                area_x = w * h
                # Check area.
                if area_x < main_area:
                    # Calculate area of a ellipse.
                    area_ellipse = (w * h * PI) / 4
                    # Calculate ratio between areas.
                    if area_contour < area_ellipse:
                        ratio = area_contour / area_ellipse
                    else:
                        ratio = area_ellipse / area_contour
                    #print(ratio)
                    if ratio >= DIV:
                        # Increment counter.
                        count += 1
                        # Draw contour.
                        x0 = int(x+0.40*w)
                        y0 = int(y+0.55*h)
                        # Draw allowed ellipses.
                        if count not in exlist:
                            if contour_switch:
                                cv2.drawContours(imgNEW, [cnt], -1, color_ellipse, thickness)
                                cv2.drawContours(imgMask, [cnt], -1, (255, 255, 255), thickness)
                                cv2.fillPoly(imgMask, pts=[cnt], color=(255, 255, 255))
                            else:
                                cv2.drawContours(imgNEW, [approximation], -1, color_ellipse, thickness)
                                cv2.drawContours(imgMask, [approximation], -1, (255, 255, 255), thickness)
                                cv2.fillPoly(imgMask, pts=[approximation], color=(255, 255, 255))
                            if numbering:
                                cv2.putText(imgNEW, str(count), (x0,y0), cv2.FONT_HERSHEY_SIMPLEX, number_size, color_ellipse, thickness, cv2.LINE_AA)
        # Return image
        return imgNEW, imgMask

    def ellipse_detection(self, image, color_tuple_ellipse, thickness,
                          numbering, number_size, eps, div, number_sections,
                          contour_switch, exclude_circles=""):
        '''Main script function.'''
        # Calculate exclude list.
        if exclude_circles != "":
            inlist = exclude_circles.split(",")
            exlist = list(map(str.strip, inlist))
            exlist = list(map(int, exlist))
        else:
            exlist = []
        # Create a PIL image.
        img_input = tensor2pil(image)
        # Create numpy array.
        img_input = np.asarray(img_input)
        # Detect ellipses.
        img_output, maskImage = self.detect_ellipse(
            img_input, thickness, div, eps, number_sections, number_size,
            numbering, color_tuple_ellipse, contour_switch, exlist
        )
        # Create output image.
        img_output = Image.fromarray(img_output)
        # Create tensors.
        image_out = pil2tensor(img_output)
        maskImage = pil2tensor(maskImage)
        # Create the final mask.
        mask = maskImage[:, :, :, 1]
        # Create the final inverted mask.
        invertedmask = 1 - mask
        # Return the return types.
        return (image_out, mask, invertedmask,)
