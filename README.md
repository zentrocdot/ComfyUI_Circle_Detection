# ComfyUI Circle Detection Node [![Copus - Post](https://img.shields.io/badge/Copus-Post-00aaee)](https://www.copus.io/work/93ba7f55a26845cd9666854a750a80f1) [![ComfyUI - Homepage](https://img.shields.io/badge/ComfyUI-Homepage-aa00ee)](https://github.com/comfyanonymous/ComfyUI)

> [!IMPORTANT]  
> <p align="justify">🚧 This documentation is still under construction. 
> Please note also that the node is not catching all errors e.g. on wrong
> settings. This is on my to-do list.</p>

## Introduction

<p align="justify">Next to AI mathematical methods can be used for the detection
of objects like a circle. This node is using Hough's Circle Transform for the
detection of circles in an given image. The advantage of mathematical methods is 
that the recognised circles can be virtually predicted. I utilise this to create
circle masks.</p>

## Goal of the Circle Detection Node

<p align="justify">To explain the goal is best done using an example. Take the 
office under the sea. If I want to move this office in outer space, I have to
exchange the content seen in the portholes. By use of the node this can easily
done.</p>

![ComfyUI_00429_ (Kopie)](https://github.com/user-attachments/assets/cd32605f-402c-4d87-b20b-ab9881b0a4c3)

*Figure 1: Original image*

Applying the node and inpainting one gets.

![ComfyUI_temp_jgphx_00003_](https://github.com/user-attachments/assets/09dabbf0-8e59-4610-98c6-e5a344954748)

*Figure 2: Inpainted image*

## Usage

After installation the node can be find in the node menu

* Add Node > 🧬 Circle Detection Nodes > 🔬 Circle Detection

For showing data one can use following node

* Add Node > 🧬 Circle Detection Nodes > 📄 Show Data
For the input of data one can use following node

* Add Node > 🧬 Circle Detection Nodes > ✏️ Input Data


<p align="justify">The first node is the node for the circle detection.
The second node is for viewing data from the circle detection node.</p>

## What the Node Does

### Node Input / Output

The input of the node is an image. The output of the node is

- NODE INPUT
  + image 
- NODE OUTPUT
  + image_output
  + image_mask
  + mask
  + data
  + help

For showing the data one needs a text/string output node.
The help output can be shown with an text/string ouptput node. 

> [!NOTE]  
> <p align="justify">help is a feature that should make it in
> the future easier to work with the node without visiting this
> documentation.</p>

### Settings

#### List of Settings

- threshold_canny_edge
- threshold_circle_center
- minR
- maxR
- dp
- minDist
- color_tuple_cicles
- color_tuple_bg
- color_tuple_fg
- thickness
- show_circle_center
- numbering
- number_size

#### Preview of Settings

![Bildschirmfoto vom 2025-02-06 16-41-25](https://github.com/user-attachments/assets/9e6bd8f5-b4c3-44ca-956b-f0a6bccba17f)

*Figure 2: Circle detection node*

#### Setting color_tuple_cicles

<p align="justify">color_tiple_circle sets the color of the circle which marks the setected circle.</p>

#### Setting exclude_circles   

<p align="justify">As I wrote earlier mathematical methods produce on each run the same results. One can take advantage of this.
After first run one can exclude circles which were detected in the first run.</p>

## Version Previews

version 0.0.0.4

![Bildschirmfoto vom 2025-02-06 14-52-46](https://github.com/user-attachments/assets/fd4189a4-e853-4513-ba46-e439c072f778)

*Figure 3: Preview of workflow using the circle detection node* 

version 0.0.0.3

![Bildschirmfoto vom 2025-02-04 16-19-47](https://github.com/user-attachments/assets/ae0fc9e5-9af6-4ab7-9e50-9403b470670f)

*Figure 4: Preview of workflow using the circle detection node* 

version 0.0.0.2

![Bildschirmfoto vom 2025-02-03 20-06-43](https://github.com/user-attachments/assets/80c6c715-3f73-4478-a3aa-ee6cd5f9f82d)

*Figure 5: Preview of workflow using the circle detection node* 

version 0.0.0.1

![Bildschirmfoto vom 2025-02-02 22-08-34](https://github.com/user-attachments/assets/60386026-9e15-4508-b6d9-dade02bb44d7)

*Figure 6: Preview of workflow using the circle detection node* 

## Installation

Use the ComfyUI Manager for the installation of the node.

You can also move int the directory ComfyUI/custom_nodes

<code>git clone https://github.com/zentrocdot/ComfyUI_Circle_Detection</code>

# Example

<img src="./images/ComfyUI_0001.jpeg" alt="button panel" width="512">
<p><i>Figure 7: Original image</i></p>

<img src="./images/ComfyUI_0002.jpeg" alt="button panel" width="512">
<p><i>Figure 8: Image with circles detected</i></p>

# To-Do

Troubleshooting in the node programming and sanitizing up the code.

## Remarks

<p align="justify">The first image created is the one, where on can see, which circles are found. The seond image looks like a mask, but it is not for the moment. 
It is still an blank image, where the found circles are filled drawn. This changed in version 0.0.0.3.</p>

## Open Issues

<p align="justify">It is unclear, if the JavaScript event trigger for updating the Show Data window will work.</p>

## References

[1] https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html

[2] https://github.com/exectails/comfyui-et_infoutils

[3] https://github.com/rgthree/rgthree-comfy

[4] https://github.com/pythongosssss/ComfyUI-Custom-Scripts
