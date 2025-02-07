from .nodes.hough_circle import *
from .nodes.showdatanodes import *
from .nodes.inputdatanodes import *
from .nodes.simple_ellipse import *

NODE_CLASS_MAPPINGS = { 
    "🔬 Circle Detection (Hough)": CircleDetection,
    "🔬 Ellipse Detection (Simple)": EllipseDetection,
    "📄 Show Data": ShowData,
    "✏️ Input Data": InputData,
    }
    
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

print("\033[34mComfyUI Circle Detection Nodes: \033[92mLoaded\033[0m")
