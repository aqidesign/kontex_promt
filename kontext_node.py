import json
import os
from typing import Dict, Any, List, Tuple
import torch
import numpy as np
from PIL import Image

class KontextTemplateNode:
    """
    ComfyUI节点：Kontext提示词模板
    基于kontext训练数据创建的提示词模板系统
    """
    
    def __init__(self):
        self.templates_path = os.path.join(os.path.dirname(__file__), "templates.json")
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """加载模板配置文件"""
        try:
            with open(self.templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading templates: {e}")
            return {}
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """定义节点的输入类型"""
        # 获取模板类别
        templates = cls().templates
        categories = list(templates.get('categories', {}).keys())
        
        # 构建类别下拉选项
        category_options = []
        for cat_key, cat_data in templates.get('categories', {}).items():
            category_options.append(f"{cat_data['name']} ({cat_key})")
        
        return {
            "required": {
                "image": ("IMAGE",),
                "category": (category_options, {"default": category_options[0] if category_options else ""}),
                "template": (["请先选择类别"], {"default": "请先选择类别"}),
            },
            "optional": {
                "parameter_1": ("STRING", {"default": "", "multiline": False}),
                "parameter_2": ("STRING", {"default": "", "multiline": False}),
                "parameter_3": ("STRING", {"default": "", "multiline": False}),
                "custom_prompt": ("STRING", {"default": "", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("prompt", "image_preview")
    FUNCTION = "generate_prompt"
    CATEGORY = "kontext"
    
    def generate_prompt(self, image, category, template, parameter_1="", parameter_2="", parameter_3="", custom_prompt="") -> Tuple[str, torch.Tensor]:
        """生成提示词"""
        
        # 如果有自定义提示词，优先使用
        if custom_prompt.strip():
            return (custom_prompt, image)
        
        # 解析类别
        category_key = category.split("(")[-1].rstrip(")")
        
        # 获取模板数据
        templates_data = self.templates.get('categories', {})
        if category_key not in templates_data:
            return ("Error: Invalid category", image)
        
        # 找到选中的模板
        template_list = templates_data[category_key].get('templates', [])
        selected_template = None
        
        for tmpl in template_list:
            if tmpl.get('name') == template:
                selected_template = tmpl
                break
        
        if not selected_template:
            return ("Error: Template not found", image)
        
        # 构建提示词
        prompt_template = selected_template.get('prompt', '')
        parameters = selected_template.get('parameters', [])
        
        # 替换参数
        param_values = [parameter_1, parameter_2, parameter_3]
        final_prompt = prompt_template
        
        for i, param in enumerate(parameters):
            if i < len(param_values) and param_values[i].strip():
                placeholder = "{" + param + "}"
                final_prompt = final_prompt.replace(placeholder, param_values[i])
        
        return (final_prompt, image)
    
    @classmethod
    def get_templates_by_category(cls, category_key: str) -> List[str]:
        """获取指定类别的模板列表"""
        instance = cls()
        templates_data = instance.templates.get('categories', {})
        
        if category_key not in templates_data:
            return []
        
        templates = templates_data[category_key].get('templates', [])
        return [tmpl.get('name', '') for tmpl in templates]

class KontextTemplateSelector:
    """
    辅助节点：模板选择器
    用于动态更新模板列表
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        templates = KontextTemplateNode().templates
        categories = list(templates.get('categories', {}).keys())
        
        category_options = []
        for cat_key, cat_data in templates.get('categories', {}).items():
            category_options.append(f"{cat_data['name']} ({cat_key})")
        
        return {
            "required": {
                "category": (category_options, {"default": category_options[0] if category_options else ""}),
            }
        }
    
    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("templates",)
    FUNCTION = "get_templates"
    CATEGORY = "kontext"
    
    def get_templates(self, category):
        """获取指定类别的模板列表"""
        category_key = category.split("(")[-1].rstrip(")")
        templates = KontextTemplateNode.get_templates_by_category(category_key)
        return (templates,)

# Web UI 更新函数
NODE_CLASS_MAPPINGS = {
    "KontextTemplateNode": KontextTemplateNode,
    "KontextTemplateSelector": KontextTemplateSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KontextTemplateNode": "Kontext 提示词模板",
    "KontextTemplateSelector": "模板选择器",
}