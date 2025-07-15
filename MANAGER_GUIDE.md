# 模板管理节点使用指南

本文档详细介绍如何使用 **Kontext 模板管理** 和 **Kontext 模板选择器** 两个高级节点。

## 🎯 功能概述

- **Kontext 模板管理**: 动态管理提示词模板（添加/修改/删除/导入/导出）
- **Kontext 模板选择器**: 动态获取模板列表并选择使用

## 📋 节点位置

在ComfyUI节点列表中查找：
- `kontext` 类别下
- 或搜索 "Kontext"

## 🔧 Kontext 模板管理节点

### 输入参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| **action** | 下拉选择 | 是 | 操作类型 | add/update/delete/list/export/import |
| **category** | 文本 | 是 | 模板类别 | user_custom |
| **template_name** | 文本 | 是 | 模板名称 | 我的自定义模板 |
| **prompt** | 多行文本 | 可选 | 提示词模板 | "将{object}变成{style}风格" |
| **description** | 文本 | 可选 | 模板描述 | 自定义物体风格转换 |
| **parameters** | 多行文本 | 可选 | 参数列表 | object,style |
| **file_path** | 文本 | 可选 | 文件路径 | C:/templates/my_templates.json |
| **old_name** | 文本 | 可选 | 原名称（更新用） | 旧模板名称 |

### 操作说明

#### 1. 添加新模板 (add)

**场景**: 添加自定义提示词模板

**步骤**:
1. 设置 `action = add`
2. 设置 `category = user_custom` （或新建类别）
3. 设置 `template_name` = 模板显示名称
4. 设置 `prompt` = 包含参数的提示词
5. 设置 `parameters` = 参数列表（逗号分隔）
6. 执行节点

**示例**:
```
action: add
category: user_custom
template_name: 复古照片
prompt: Turn this into vintage photo from {year} with {color} tone
description: 创建复古风格照片
parameters: year,color
```

#### 2. 更新模板 (update)

**场景**: 修改现有模板

**步骤**:
1. 设置 `action = update`
2. 设置 `category` = 模板所在类别
3. 设置 `old_name` = 原模板名称
4. 设置 `template_name` = 新模板名称（如不变则与old_name相同）
5. 修改其他参数

**示例**:
```
action: update
category: user_custom
old_name: 复古照片
template_name: 复古照片增强
prompt: Turn this into vintage photo from {year} with {color} tone and {effect} effect
parameters: year,color,effect
```

#### 3. 删除模板 (delete)

**场景**: 移除不需要的模板

**步骤**:
1. 设置 `action = delete`
2. 设置 `category` = 模板所在类别
3. 设置 `template_name` = 要删除的模板名称

#### 4. 列出模板 (list)

**场景**: 查看所有可用模板

**步骤**:
1. 设置 `action = list`
2. 其他参数可留空
3. 节点返回JSON格式的所有模板列表

#### 5. 导出模板 (export)

**场景**: 备份模板到文件

**步骤**:
1. 设置 `action = export`
2. 设置 `file_path` = 导出文件路径（.json格式）

**示例**:
```
action: export
file_path: C:/Users/YourName/Documents/kontext_backup.json
```

#### 6. 导入模板 (import)

**场景**: 从文件恢复模板

**步骤**:
1. 设置 `action = import`
2. 设置 `file_path` = 导入文件路径

**示例**:
```
action: import
file_path: C:/Users/YourName/Documents/kontext_backup.json
```

## 🔍 Kontext 模板选择器节点

### 输入参数

| 参数 | 类型 | 说明 | 选项 |
|---|---|---|---|
| **category** | 下拉选择 | 模板类别 | all/object_manipulation/style_transfer/character_manipulation/environment_change/text_manipulation/color_adjustment/camera_operations/user_custom |

### 输出

| 输出 | 类型 | 说明 |
|---|---|---|
| **template_names** | 列表 | 模板名称列表 |
| **templates_json** | 字符串 | 完整模板数据（JSON格式） |

### 使用示例

#### 获取所有模板
```
category: all
```
返回所有类别的模板列表

#### 获取特定类别模板
```
category: style_transfer
```
仅返回风格转换类别的模板

#### 获取用户自定义模板
```
category: user_custom
```
返回用户通过模板管理节点添加的自定义模板

## 🧩 完整工作流示例

### 场景：创建并使用自定义模板

#### 步骤1：添加自定义模板
```
[模板管理节点]
action: add
category: user_custom
template_name: 赛博朋克风格
prompt: Transform this into cyberpunk style with {color} neon lights and {mood} atmosphere
description: 赛博朋克风格转换
parameters: color,mood
```

#### 步骤2：获取模板列表
```
[模板选择器节点]
category: user_custom
```

#### 步骤3：使用模板
将模板选择器连接到其他节点，使用返回的模板名称

## 📁 文件位置

- **默认模板**: `templates.json`（1026个预设模板）
- **用户模板**: `user_templates.json`（用户自定义模板）

## ⚠️ 注意事项

1. **参数格式**: 参数列表使用英文逗号分隔
2. **模板名称**: 不要重复相同类别下的模板名称
3. **文件路径**: Windows使用正斜杠或双反斜杠
4. **备份**: 定期导出模板以防丢失
5. **类别**: 建议使用`user_custom`存放自定义模板

## 🐛 常见问题

### Q: 模板添加后在哪里查看？
A: 使用模板选择器节点，设置category为对应类别即可查看

### Q: 可以修改预设模板吗？
A: 不建议直接修改预设模板，可以在user_custom类别中创建修改版本

### Q: 如何分享给其他用户？
A: 使用export功能导出为.json文件，其他用户用import导入

### Q: 模板不生效怎么办？
A: 检查：
- 参数是否正确填写
- 模板名称是否正确
- JSON格式是否正确
- 重启ComfyUI刷新缓存

## 🎯 最佳实践

1. **命名规范**: 自定义模板使用清晰的名称
2. **参数设计**: 参数名称要直观，如`{object}`, `{style}`, `{color}`
3. **分类管理**: 按功能分类管理模板
4. **定期备份**: 重要模板定期导出备份
5. **测试模板**: 添加后先测试再正式使用