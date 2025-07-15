#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证节点导入的测试脚本
"""

import sys
import os
import importlib.util

# 模拟ComfyUI环境
def test_comfyui_import():
    """测试节点导入"""
    try:
        # 设置UTF-8编码
        sys.stdout.reconfigure(encoding='utf-8')
        
        print("测试基本导入...")
        
        # 测试kontext_node模块
        spec = importlib.util.spec_from_file_location("kontext_node", "kontext_node.py")
        kontext_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kontext_module)
        
        # 获取节点映射
        if hasattr(kontext_module, 'NODE_CLASS_MAPPINGS'):
            node_mappings = kontext_module.NODE_CLASS_MAPPINGS
            print(f"成功注册 {len(node_mappings)} 个节点")
            for name, cls in node_mappings.items():
                print(f"  - {name}: {cls.__name__}")
        
        return True
    except Exception as e:
        print(f"导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ComfyUI节点测试 ===")
    success = test_comfyui_import()
    if success:
        print("\n所有节点导入成功，可以正常使用ComfyUI！")
    else:
        print("\n节点导入失败，请检查错误信息")