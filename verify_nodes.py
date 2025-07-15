#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证所有ComfyUI节点是否正确加载
"""

import sys
import os
import json

def verify_nodes():
    """验证节点"""
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== 验证ComfyUI Kontext节点 ===\n")
    
    try:
        # 测试导入
        import importlib.util
        
        # 测试kontext_node模块
        spec = importlib.util.spec_from_file_location("kontext_node", "kontext_node.py")
        kontext_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kontext_module)
        
        print("[OK] 节点加载成功!")
        
        # 显示所有节点
        if hasattr(kontext_module, 'NODE_CLASS_MAPPINGS'):
            mappings = kontext_module.NODE_CLASS_MAPPINGS
            print(f"[INFO] 共找到 {len(mappings)} 个节点:")
            
            for name, cls in mappings.items():
                print(f"   - {name}: {cls.__name__}")
                
                # 检查类是否有INPUT_TYPES方法
                if hasattr(cls, 'INPUT_TYPES'):
                    input_types = cls.INPUT_TYPES()
                    print(f"     输入参数: {list(input_types.get('required', {}).keys())}")
                
        # 检查JSON文件是否存在
        json_files = ['templates.json', 'user_templates.json']
        for json_file in json_files:
            if os.path.exists(json_file):
                print(f"[OK] {json_file} 文件存在")
                
                # 验证JSON格式
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"   [INFO] 包含 {len(data.get('categories', {}))} 个类别")
                except Exception as e:
                    print(f"   [ERROR] JSON格式错误: {e}")
            else:
                print(f"[WARNING] {json_file} 文件不存在")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verify_nodes()