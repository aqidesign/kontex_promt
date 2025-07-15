import json
import os

class KontextTemplateNode:
    """
    Kontext提示词模板节点
    基于kontext训练数据的ComfyUI提示词模板
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入 - 简洁实用设计"""
        return {
            "required": {
                "template": ([
                    # 物体操作
                    "移除物体",
                    "添加物体", 
                    "替换物体",
                    "复制物体",
                    
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
                    
                    # 环境变换
                    "改变背景",
                    "添加天气效果",
                    "改变时间",
                    
                    # 颜色调整
                    "黑白照片",
                    "复古色调",
                    
                    # 文字操作
                    "添加文字",
                    "移除文字",
                    "修改文字"
                ],),
                "target": ("STRING", {"default": "", "placeholder": "目标对象/位置/数值"}),
            },
            "optional": {
                "custom_prompt": ("STRING", {"default": "", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
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
    
    def generate_prompt(self, template, target="", custom_prompt=""):
        """生成提示词 - 简洁实用的模板映射"""
        if custom_prompt.strip():
            return (custom_prompt,)
        
        # 简洁的模板映射 - 单参数设计
        template_map = {
            # 物体操作
            "移除物体": f"Remove {target}" if target else "Remove the main object",
            "添加物体": f"Add {target}" if target else "Add an object",
            "替换物体": f"Replace with {target}" if target else "Replace the object",
            "复制物体": f"Duplicate {target}" if target else "Duplicate the object",
            
            # 风格转换
            "动漫风格": f"Transform into anime style {target}" if target else "Transform into anime style",
            "真实照片": f"Convert to realistic photo {target}" if target else "Convert to realistic photo",
            "油画风格": f"Render as oil painting {target}" if target else "Render as oil painting",
            "水彩风格": f"Apply watercolor style {target}" if target else "Apply watercolor style",
            "素描风格": f"Transform to sketch {target}" if target else "Transform to sketch",
            "赛博朋克": f"Apply cyberpunk aesthetic {target}" if target else "Apply cyberpunk aesthetic",
            "复古风格": f"Apply vintage style {target}" if target else "Apply vintage style",
            
            # 角色操作
            "改变表情": f"Change expression to {target}" if target else "Change the expression",
            "改变姿势": f"Change pose to {target}" if target else "Change the pose",
            "添加服装": f"Add {target} clothing" if target else "Add clothing",
            "改变发型": f"Change hairstyle to {target}" if target else "Change the hairstyle",
            
            # 环境变换
            "改变背景": f"Change background to {target}" if target else "Change the background",
            "添加天气效果": f"Add {target} weather effect" if target else "Add weather effect",
            "改变时间": f"Change time to {target}" if target else "Change the time of day",
            
            # 颜色调整
            "黑白照片": f"Convert to black and white {target}" if target else "Convert to black and white",
            "复古色调": f"Apply vintage tone {target}" if target else "Apply vintage tone",
            
            # 文字操作
            "添加文字": f"Add text '{target}'" if target else "Add text",
            "移除文字": "Remove all text from the image",
            "修改文字": f"Change text to '{target}'" if target else "Modify the text"
        }
        
        prompt = template_map.get(template, template)
        return (prompt,)

# 节点注册 - 仅保留主提示词模板节点
NODE_CLASS_MAPPINGS = {
    "KontextTemplateNode": KontextTemplateNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KontextTemplateNode": "Kontext 提示词模板",
}