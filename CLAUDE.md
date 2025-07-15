# Kontext ComfyUI 项目规则

## 项目结构
```
kontex_promt/
├── __init__.py              # 模块初始化
├── kontext_node.py          # 主提示词模板节点
├── template_manager.py      # 模板管理节点
├── templates.json           # 默认模板配置
├── user_templates.json      # 用户自定义模板
├── README.md               # 项目文档
└── .gitignore             # Git忽略规则
```

## 代码规范

### 文件编码
- 所有Python文件必须使用UTF-8编码
- 文件头部必须包含: `# -*- coding: utf-8 -*-`

### 命名规范
- 类名使用PascalCase: `KontextTemplateNode`
- 函数名使用snake_case: `generate_prompt`
- 常量使用UPPER_SNAKE_CASE: `NODE_CLASS_MAPPINGS`
- 中文显示名使用完整描述: `"Kontext 提示词模板"`

### 节点开发规范

#### 基本结构
```python
class NodeName:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {...},
            "optional": {...}
        }
    
    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("prompt", "image")
    FUNCTION = "function_name"
    CATEGORY = "kontext"
```

#### 输入类型定义
- 使用标准ComfyUI类型: `"STRING"`, `"IMAGE"`, `"INT"`, `"FLOAT"`
- 下拉菜单使用元组: `(["option1", "option2"],)`
- 多行文本: `("STRING", {"multiline": True})`

#### 错误处理
- 所有文件操作必须包含异常处理
- 使用中文错误提示便于用户理解
- 提供降级方案避免节点崩溃

### JSON配置规范

#### templates.json结构
```json
{
  "categories": {
    "category_key": {
      "name": "类别显示名称",
      "templates": [
        {
          "id": "unique_id",
          "name": "模板名称",
          "prompt": "模板提示词 {parameter}",
          "description": "模板描述",
          "parameters": ["parameter"]
        }
      ]
    }
  }
}
```

### 模块导入规范
- 避免相对导入，使用动态导入机制
- 节点注册变量使用唯一命名避免冲突
- 主模块负责统一节点注册

### 文档规范
- 所有公开功能必须有中文说明
- README.md包含完整安装和使用指南
- 提供故障排除方案

### 版本管理
- 主要版本更新必须向后兼容
- 新功能添加不影响现有节点
- 破坏性变更需要明确文档说明

## 开发流程

1. **功能开发**: 在独立分支进行
2. **测试验证**: 使用ComfyUI实际测试
3. **文档更新**: 同步更新README.md
4. **代码审查**: 检查UTF-8编码和异常处理
5. **合并发布**: 确保所有节点正常加载

## 贡献指南

### 添加新模板
1. 在templates.json中添加新类别或模板
2. 确保模板参数与实际使用场景匹配
3. 提供中英文描述
4. 测试模板在实际工作中的效果

### 代码贡献
1. 遵循现有代码风格
2. 添加中文注释
3. 包含异常处理
4. 更新相关文档

## 故障排除

### 常见问题
- **UTF-8编码问题**: 确保所有文件保存为UTF-8格式
- **节点加载失败**: 检查NODE_CLASS_MAPPINGS定义
- **JSON格式错误**: 使用JSON验证工具检查格式

### 调试工具
- 使用`verify_nodes.py`验证节点加载（开发用）
- 检查ComfyUI控制台输出
- 验证templates.json格式正确性