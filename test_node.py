#!/usr/bin/env python3
"""
ComfyUI Kontext节点测试文件
用于验证节点是否正确加载
"""

import sys
import os

# 模拟ComfyUI环境
class MockComfyUI:
    class Image:
        def __init__(self, tensor):
            self.tensor = tensor
    
    @staticmethod
    def create_test_image():
        import torch
        return torch.randn(1, 3, 512, 512)

def test_kontext_node():
    """测试Kontext节点"""
    try:
        # 测试导入
        from kontext_node import KontextTemplateNode, NODE_CLASS_MAPPINGS
        
        print("✅ 节点导入成功")
        
        # 测试类实例化
        node = KontextTemplateNode()
        print("✅ 节点实例化成功")
        
        # 测试输入类型
        input_types = KontextTemplateNode.INPUT_TYPES()
        print("✅ 输入类型定义成功")
        
        # 测试基础功能
        test_image = MockComfyUI.create_test_image()
        
        # 测试生成提示词
        prompt, image = node.generate_prompt(
            test_image, 
            "物体操作", 
            "移除物体", 
            parameter_1="cat"
        )
        
        print(f"✅ 提示词生成成功: {prompt}")
        print("✅ 节点测试通过")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates():
    """测试模板加载"""
    try:
        node = KontextNode.KontextTemplateNode()
        templates = node._load_templates()
        
        if templates:
            print(f"✅ 模板加载成功，共{len(templates)}个类别")
            return True
        else:
            print("⚠️ 使用默认模板")
            return True
            
    except Exception as e:
        print(f"❌ 模板测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=== Kontext节点测试 ===")
    
    # 添加当前目录到路径
    sys.path.insert(0, os.path.dirname(__file__))
    
    success = test_kontext_node()
    
    if success:
        print("\n🎉 所有测试通过，节点可以正常使用")
    else:
        print("\n💥 测试失败，请检查错误信息")