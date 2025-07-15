# -*- coding: utf-8 -*-
import json
import os
from typing import Dict, Any, List

class KontextTemplateManager:
    """
    Kontext模板管理节点
    允许用户动态管理提示词模板，无需修改代码
    """
    
    def __init__(self):
        self.user_templates_path = os.path.join(os.path.dirname(__file__), "user_templates.json")
        self.default_templates_path = os.path.join(os.path.dirname(__file__), "templates.json")
        self.ensure_user_templates()
    
    def ensure_user_templates(self):
        """确保用户模板文件存在"""
        if not os.path.exists(self.user_templates_path):
            self.create_empty_user_templates()
    
    def create_empty_user_templates(self):
        """创建空的用户模板文件"""
        empty_templates = {
            "categories": {
                "user_custom": {
                    "name": "用户自定义",
                    "templates": []
                }
            }
        }
        self.save_user_templates(empty_templates)
    
    def load_user_templates(self) -> Dict:
        """加载用户模板"""
        try:
            with open(self.user_templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading user templates: {e}")
            return {"categories": {}}
    
    def save_user_templates(self, templates: Dict):
        """保存用户模板"""
        try:
            with open(self.user_templates_path, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving user templates: {e}")
    
    def load_default_templates(self) -> Dict:
        """加载默认模板"""
        try:
            with open(self.default_templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading default templates: {e}")
            return {"categories": {}}
    
    def add_template(self, category: str, name: str, prompt: str, description: str = "", parameters: List[str] = None):
        """添加新模板"""
        templates = self.load_user_templates()
        
        if category not in templates["categories"]:
            templates["categories"][category] = {
                "name": category,
                "templates": []
            }
        
        new_template = {
            "id": f"user_{len(templates['categories'][category]['templates'])}",
            "name": name,
            "prompt": prompt,
            "description": description,
            "parameters": parameters or []
        }
        
        templates["categories"][category]["templates"].append(new_template)
        self.save_user_templates(templates)
    
    def update_template(self, category: str, template_name: str, **kwargs):
        """更新现有模板"""
        templates = self.load_user_templates()
        
        if category in templates["categories"]:
            for template in templates["categories"][category]["templates"]:
                if template["name"] == template_name:
                    template.update(kwargs)
                    self.save_user_templates(templates)
                    return True
        return False
    
    def delete_template(self, category: str, template_name: str) -> bool:
        """删除模板"""
        templates = self.load_user_templates()
        
        if category in templates["categories"]:
            original_count = len(templates["categories"][category]["templates"])
            templates["categories"][category]["templates"] = [
                t for t in templates["categories"][category]["templates"]
                if t["name"] != template_name
            ]
            if len(templates["categories"][category]["templates"]) < original_count:
                self.save_user_templates(templates)
                return True
        return False
    
    def get_all_templates(self) -> Dict:
        """获取所有模板（默认+用户）"""
        default_templates = self.load_default_templates()
        user_templates = self.load_user_templates()
        
        # 合并模板
        all_templates = {"categories": {}}
        all_templates["categories"].update(default_templates.get("categories", {}))
        all_templates["categories"].update(user_templates.get("categories", {}))
        
        return all_templates
    
    def export_templates(self, file_path: str):
        """导出模板到文件"""
        templates = self.get_all_templates()
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error exporting templates: {e}")
    
    def import_templates(self, file_path: str) -> bool:
        """从文件导入模板"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
            self.save_user_templates(templates)
            return True
        except Exception as e:
            print(f"Error importing templates: {e}")
            return False


class KontextTemplateManagerNode:
    """
    ComfyUI模板管理节点
    """
    
    def __init__(self):
        self.manager = KontextTemplateManager()
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入"""
        return {
            "required": {
                "action": (["add", "update", "delete", "list", "export", "import"],),
                "category": ("STRING", {"default": "user_custom"}),
                "template_name": ("STRING", {"default": ""}),
            },
            "optional": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "description": ("STRING", {"default": ""}),
                "parameters": ("STRING", {"default": "", "multiline": True}),
                "file_path": ("STRING", {"default": "", "placeholder": "用于导入/导出的文件路径"}),
                "old_name": ("STRING", {"default": "", "placeholder": "更新时原模板名称"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("result", "templates_json")
    FUNCTION = "manage_templates"
    CATEGORY = "kontext"
    
    def manage_templates(self, action, category, template_name, prompt="", description="", parameters="", file_path="", old_name=""):
        """管理模板操作"""
        
        if action == "add":
            if not template_name or not prompt:
                return ("错误：模板名称和提示词不能为空", "")
            
            param_list = [p.strip() for p in parameters.split(",") if p.strip()]
            self.manager.add_template(category, template_name, prompt, description, param_list)
            return (f"成功添加模板：{template_name}", "")
        
        elif action == "update":
            if not template_name or not prompt:
                return ("错误：模板名称和提示词不能为空", "")
            
            param_list = [p.strip() for p in parameters.split(",") if p.strip()]
            success = self.manager.update_template(
                category,
                old_name or template_name,
                name=template_name,
                prompt=prompt,
                description=description,
                parameters=param_list
            )
            return ("模板更新成功" if success else "模板未找到", "")
        
        elif action == "delete":
            if not template_name:
                return ("错误：模板名称不能为空", "")
            
            success = self.manager.delete_template(category, template_name)
            return ("模板删除成功" if success else "模板未找到", "")
        
        elif action == "list":
            templates = self.manager.get_all_templates()
            return (f"当前共有 {len(templates.get('categories', {}))} 个类别", json.dumps(templates, ensure_ascii=False, indent=2))
        
        elif action == "export":
            if not file_path:
                return ("错误：请提供导出文件路径", "")
            
            self.manager.export_templates(file_path)
            return (f"模板已导出到：{file_path}", "")
        
        elif action == "import":
            if not file_path:
                return ("错误：请提供导入文件路径", "")
            
            success = self.manager.import_templates(file_path)
            return ("模板导入成功" if success else "模板导入失败", "")
        
        return ("未知操作", "")


class KontextTemplateSelector:
    """
    动态模板选择节点
    """
    
    def __init__(self):
        self.manager = KontextTemplateManager()
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入"""
        return {
            "required": {
                "category": (["all", "object_manipulation", "style_transfer", "character_manipulation", 
                             "environment_change", "text_manipulation", "color_adjustment", 
                             "camera_operations", "user_custom"],),
            }
        }
    
    RETURN_TYPES = ("LIST", "STRING")
    RETURN_NAMES = ("template_names", "templates_json")
    FUNCTION = "get_templates"
    CATEGORY = "kontext"
    
    def get_templates(self, category):
        """获取模板列表"""
        all_templates = self.manager.get_all_templates()
        
        if category == "all":
            templates = all_templates
        else:
            templates = {"categories": {}}
            if category in all_templates.get("categories", {}):
                templates["categories"][category] = all_templates["categories"][category]
        
        # 提取模板名称
        template_names = []
        for cat_data in templates.get("categories", {}).values():
            for template in cat_data.get("templates", []):
                template_names.append(template.get("name", ""))
        
        return (template_names, json.dumps(templates, ensure_ascii=False, indent=2))


# 节点注册
# 定义节点注册变量
NODE_CLASS_MAPPINGS = {
    "KontextTemplateManager": KontextTemplateManagerNode,
    "KontextTemplateSelector": KontextTemplateSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KontextTemplateManager": "Kontext 模板管理",
    "KontextTemplateSelector": "Kontext 模板选择器",
}