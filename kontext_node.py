import json
import os

class KontextTemplateNode:
    """
    Kontext提示词模板节点
    基于kontext训练数据的ComfyUI提示词模板
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入"""
        return {
            "required": {
                "image": ("IMAGE",),
                "category": (["物体操作", "风格转换", "角色操作", "环境变换", "文字操作", "颜色调整", "镜头操作"],),
                "template": (["移除物体", "添加物体", "替换物体", "动漫风格", "真实照片", "油画风格"],),
                "parameter_1": ("STRING", {"default": ""}),
                "parameter_2": ("STRING", {"default": ""}),
            },
            "optional": {
                "custom_prompt": ("STRING", {"default": "", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("prompt", "image")
    FUNCTION = "generate_prompt"
    CATEGORY = "kontext"
    
    def __init__(self):
        self.templates_path = os.path.join(os.path.dirname(__file__), "templates.json")
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """加载模板配置"""
        try:
            with open(self.templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._get_default_templates()
    
    def _get_default_templates(self):
        """默认模板配置"""
        return {
            "object_manipulation": {
                "name": "物体操作",
                "templates": [
                    {"prompt": "Remove {object}", "name": "移除物体"},
                    {"prompt": "Add {object}", "name": "添加物体"},
                    {"prompt": "Replace {old} with {new}", "name": "替换物体"}
                ]
            },
            "style_transfer": {
                "name": "风格转换", 
                "templates": [
                    {"prompt": "Turn this into anime artwork", "name": "动漫风格"},
                    {"prompt": "Make this into a real photo", "name": "真实照片"},
                    {"prompt": "Turn this into an oil painting", "name": "油画风格"}
                ]
            }
        }
    
    def generate_prompt(self, image, category, template, parameter_1="", parameter_2="", custom_prompt=""):
        """生成提示词"""
        if custom_prompt.strip():
            return (custom_prompt, image)
        
        # 简化处理
        prompt_map = {
            "移除物体": f"Remove {parameter_1}" if parameter_1 else "Remove object",
            "添加物体": f"Add {parameter_1}" if parameter_1 else "Add object",
            "替换物体": f"Replace {parameter_1} with {parameter_2}" if parameter_1 and parameter_2 else "Replace object",
            "动漫风格": "Turn this into anime artwork",
            "真实照片": "Make this into a real photo",
            "油画风格": "Turn this into an oil painting"
        }
        
        prompt = prompt_map.get(template, template)
        return (prompt, image)

# 节点注册 - 确保所有节点都被正确注册
NODE_CLASS_MAPPINGS = {
    "KontextTemplateNode": KontextTemplateNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KontextTemplateNode": "Kontext 提示词模板",
}

# 从template_manager导入更多节点
try:
    import importlib.util
    import os
    
    # 获取当前目录
    current_dir = os.path.dirname(__file__)
    template_manager_path = os.path.join(current_dir, "template_manager.py")
    
    if os.path.exists(template_manager_path):
        spec = importlib.util.spec_from_file_location("template_manager", template_manager_path)
        template_manager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(template_manager)
        
        if hasattr(template_manager, 'MANAGER_CLASS_MAPPINGS'):
            NODE_CLASS_MAPPINGS.update(template_manager.MANAGER_CLASS_MAPPINGS)
            NODE_DISPLAY_NAME_MAPPINGS.update(template_manager.MANAGER_DISPLAY_MAPPINGS)
        elif hasattr(template_manager, 'NODE_CLASS_MAPPINGS'):
            NODE_CLASS_MAPPINGS.update(template_manager.NODE_CLASS_MAPPINGS)
            NODE_DISPLAY_NAME_MAPPINGS.update(template_manager.NODE_DISPLAY_NAME_MAPPINGS)
    
except Exception as e:
    print(f"Warning: Could not load template manager nodes: {e}")