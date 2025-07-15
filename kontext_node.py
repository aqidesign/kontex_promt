import json
import os
import logging
from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path

class KontextTemplateNode:
    """
    Kontext提示词模板节点
    基于kontext训练数据的ComfyUI提示词模板
    
    该节点提供了丰富的图像编辑提示词模板，支持物体操作、风格转换、
    角色操作、环境变换等多种类型的图像编辑任务。
    """
    
    _template_cache: Optional[Dict[str, Any]] = None
    _logger = logging.getLogger(__name__)
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """定义节点输入类型和选项
        
        Returns:
            Dict[str, Any]: 包含required和optional输入的字典
        """
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
    
    def __init__(self) -> None:
        """初始化节点实例"""
        self.templates_path = Path(__file__).parent / "templates.json"
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """加载模板配置
        
        使用缓存机制提高性能，只在首次加载时读取文件
        
        Returns:
            Dict[str, Any]: 模板配置字典
        """
        if KontextTemplateNode._template_cache is not None:
            return KontextTemplateNode._template_cache
            
        try:
            with open(self.templates_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
                KontextTemplateNode._template_cache = templates
                self._logger.info(f"Successfully loaded templates from {self.templates_path}")
                return templates
        except FileNotFoundError:
            self._logger.warning(f"Template file not found: {self.templates_path}, using default templates")
            return self._get_default_templates()
        except json.JSONDecodeError as e:
            self._logger.error(f"Invalid JSON in template file: {e}")
            return self._get_default_templates()
        except Exception as e:
            self._logger.error(f"Error loading templates: {e}")
            return self._get_default_templates()
    
    def _get_default_templates(self) -> Dict[str, Any]:
        """获取默认模板配置
        
        当templates.json文件不存在或读取失败时使用的后备模板
        
        Returns:
            Dict[str, Any]: 默认模板配置
        """
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
    
    def generate_prompt(self, template: str, target: str = "", custom_prompt: str = "") -> Tuple[str]:
        """生成提示词
        
        Args:
            template: 选择的模板名称
            target: 目标对象/位置/数值参数
            custom_prompt: 自定义提示词（优先使用）
            
        Returns:
            Tuple[str]: 包含生成的提示词的元组
        """
        if custom_prompt.strip():
            self._logger.debug(f"Using custom prompt: {custom_prompt[:50]}...")
            return (custom_prompt,)
        
        # 验证输入参数
        if not self._validate_inputs(template, target):
            self._logger.warning(f"Invalid inputs: template='{template}', target='{target}'")
            return ("Invalid template or parameters",)
        
        # 首先尝试从templates.json中查找模板
        prompt = self._get_prompt_from_templates(template, target)
        if prompt:
            return (prompt,)
        
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
        self._logger.debug(f"Generated prompt for '{template}': {prompt}")
        return (prompt,)
    
    def _get_prompt_from_templates(self, template_name: str, target: str) -> Optional[str]:
        """从templates.json中获取提示词
        
        Args:
            template_name: 模板名称
            target: 目标参数
            
        Returns:
            Optional[str]: 生成的提示词，如果未找到则返回None
        """
        try:
            for category in self.templates.get("categories", {}).values():
                for template in category.get("templates", []):
                    if template.get("name") == template_name:
                        prompt = template.get("prompt", "")
                        parameters = template.get("parameters", [])
                        
                        # 处理多参数模板
                        if parameters:
                            # 简化处理：将target作为第一个参数
                            if len(parameters) == 1:
                                return prompt.format(**{parameters[0]: target})
                            else:
                                # 多参数情况下，使用target填充第一个参数
                                format_dict = {param: target if i == 0 else "" for i, param in enumerate(parameters)}
                                return prompt.format(**format_dict)
                        else:
                            return prompt
        except Exception as e:
            self._logger.error(f"Error processing template '{template_name}': {e}")
            
        return None
    
    def _validate_inputs(self, template: str, target: str) -> bool:
        """验证输入参数
        
        Args:
            template: 模板名称
            target: 目标参数
            
        Returns:
            bool: 输入是否有效
        """
        if not template or not isinstance(template, str):
            return False
            
        # 检查target参数是否过长
        if len(target) > 200:
            self._logger.warning(f"Target parameter too long: {len(target)} characters")
            return False
            
        # 检查是否包含潜在的有害内容
        forbidden_chars = ['<', '>', '"', "'", '\\', '&']
        if any(char in target for char in forbidden_chars):
            self._logger.warning(f"Target contains forbidden characters: {target}")
            return False
            
        return True

# 节点注册 - 仅保留主提示词模板节点
NODE_CLASS_MAPPINGS = {
    "KontextTemplateNode": KontextTemplateNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KontextTemplateNode": "Kontext 提示词模板",
}