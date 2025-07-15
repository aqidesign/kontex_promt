import json
import os

class KontextTemplateNode:
    """
    Kontext提示词模板节点
    基于kontext训练数据的ComfyUI提示词模板
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入 - 简化设计"""
        return {
            "required": {
                "image": ("IMAGE",),
                "template": ([
                    # 物体操作
                    "移除物体",
                    "添加物体", 
                    "替换物体",
                    "复制物体",
                    "移动物体",
                    
                    # 风格转换
                    "动漫风格",
                    "真实照片",
                    "油画风格",
                    "水彩风格",
                    "素描风格",
                    "赛博朋克",
                    "复古风格",
                    
                    # 角色操作
                    "改变表情",
                    "改变姿势",
                    "添加服装",
                    "改变发型",
                    "角色年轻化",
                    "角色老龄化",
                    
                    # 环境变换
                    "改变背景",
                    "添加天气效果",
                    "改变时间",
                    "添加光源",
                    "改变季节",
                    
                    # 颜色调整
                    "调整亮度",
                    "调整对比度",
                    "调整饱和度",
                    "黑白照片",
                    "复古色调",
                    
                    # 镜头操作
                    "放大",
                    "缩小",
                    "旋转",
                    "翻转",
                    "移动视角",
                    
                    # 文字操作
                    "添加文字",
                    "移除文字",
                    "修改文字",
                    "翻译文字"
                ],),
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
    
    def generate_prompt(self, image, template, parameter_1="", parameter_2="", custom_prompt=""):
        """生成提示词 - 基于模板名称直接生成"""
        if custom_prompt.strip():
            return (custom_prompt, image)
        
        # 完整的模板映射
        template_map = {
            # 物体操作
            "移除物体": f"Remove {parameter_1}" if parameter_1 else "Remove the main object",
            "添加物体": f"Add {parameter_1} to the image" if parameter_1 else "Add an object",
            "替换物体": f"Replace {parameter_1} with {parameter_2}" if parameter_1 and parameter_2 else f"Replace {parameter_1}" if parameter_1 else "Replace the object",
            "复制物体": f"Duplicate {parameter_1} in the image" if parameter_1 else "Duplicate the object",
            "移动物体": f"Move {parameter_1} to {parameter_2}" if parameter_1 and parameter_2 else f"Move {parameter_1}" if parameter_1 else "Move the object",
            
            # 风格转换
            "动漫风格": "Transform this into anime art style",
            "真实照片": "Convert this to a realistic photograph",
            "油画风格": "Render this as an oil painting",
            "水彩风格": "Convert this to watercolor painting style",
            "素描风格": "Transform this into pencil sketch style",
            "赛博朋克": "Apply cyberpunk aesthetic with neon lights and futuristic elements",
            "复古风格": f"Apply vintage {parameter_1} style filter" if parameter_1 else "Apply vintage retro style",
            
            # 角色操作
            "改变表情": f"Change the expression to {parameter_1}" if parameter_1 else "Change the facial expression",
            "改变姿势": f"Change the pose to {parameter_1}" if parameter_1 else "Change the pose",
            "添加服装": f"Add {parameter_1} clothing" if parameter_1 else "Add clothing",
            "改变发型": f"Change hairstyle to {parameter_1}" if parameter_1 else "Change the hairstyle",
            "角色年轻化": f"Make the subject look {parameter_1} years younger" if parameter_1 else "Make the subject look younger",
            "角色老龄化": f"Make the subject look {parameter_1} years older" if parameter_1 else "Make the subject look older",
            
            # 环境变换
            "改变背景": f"Change the background to {parameter_1}" if parameter_1 else "Change the background",
            "添加天气效果": f"Add {parameter_1} weather effect" if parameter_1 else "Add weather effect",
            "改变时间": f"Change the time to {parameter_1}" if parameter_1 else "Change the time of day",
            "添加光源": f"Add {parameter_1} lighting" if parameter_1 else "Add lighting effect",
            "改变季节": f"Change the season to {parameter_1}" if parameter_1 else "Change the season",
            
            # 颜色调整
            "调整亮度": f"Adjust brightness to {parameter_1}" if parameter_1 else "Adjust brightness",
            "调整对比度": f"Adjust contrast to {parameter_1}" if parameter_1 else "Adjust contrast",
            "调整饱和度": f"Adjust saturation to {parameter_1}" if parameter_1 else "Adjust saturation",
            "黑白照片": "Convert to black and white",
            "复古色调": "Apply vintage color tone",
            
            # 镜头操作
            "放大": f"Zoom in by {parameter_1}" if parameter_1 else "Zoom in",
            "缩小": f"Zoom out by {parameter_1}" if parameter_1 else "Zoom out",
            "旋转": f"Rotate by {parameter_1} degrees" if parameter_1 else "Rotate the image",
            "翻转": f"Flip {parameter_1}" if parameter_1 else "Flip the image",
            "移动视角": f"Move viewpoint to {parameter_1}" if parameter_1 else "Change viewpoint",
            
            # 文字操作
            "添加文字": f"Add text '{parameter_1}'" if parameter_1 else "Add text",
            "移除文字": "Remove all text from the image",
            "修改文字": f"Change text to '{parameter_1}'" if parameter_1 else "Modify the text",
            "翻译文字": f"Translate text to {parameter_1}" if parameter_1 else "Translate the text"
        }
        
        prompt = template_map.get(template, template)
        return (prompt, image)

# 节点注册 - 仅保留主提示词模板节点
NODE_CLASS_MAPPINGS = {
    "KontextTemplateNode": KontextTemplateNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KontextTemplateNode": "Kontext 提示词模板",
}