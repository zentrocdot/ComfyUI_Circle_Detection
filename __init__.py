from .nodes.nodes import *
from .nodes.showdatanodes import *

NODE_CLASS_MAPPINGS = { 
    "🔬 Circle Detection": CircleDetection,
    "🗃 Show Data": ShowData,
    }
    
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

print("\033[34mComfyUI Circle Detection Nodes: \033[92mLoaded\033[0m")
