# Kontext ComfyUI 提示词模板

基于 1026 个 kontext 训练提示词整理的 ComfyUI 节点，提供图像编辑提示词模板。

## 🚀 快速开始

### 安装
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/aqidesign/kontex_promt.git
```

### 使用
1. 重启 ComfyUI
2. 添加 "Kontext 提示词模板" 节点
3. 选择模板类别和具体模板
4. 填写参数（可选）
5. 获取生成的提示词

## 安装方法

### 方法1：手动安装
1. 将 `kontext_node.py` 和 `templates.json` 复制到 ComfyUI 的 `custom_nodes` 目录
2. 重启 ComfyUI

### 方法2：Git安装
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/aqidesign/kontex_promt.git
```

## 使用方法

### 基本使用
1. 在 ComfyUI 中找到 `Kontext 提示词模板` 节点
2. 选择模板类别（如"物体操作"、"风格转换"等）
3. 选择具体的模板（如"移除物体"、"动漫风格"等）
4. 根据需要填写参数
5. 节点将输出生成的提示词

### 参数说明
- **image**: 输入图像（用于预览）
- **category**: 模板类别
- **template**: 具体模板
- **parameter_1/2/3**: 模板参数（根据模板需求填写）
- **custom_prompt**: 自定义提示词（优先使用）

### 示例模板

#### 物体操作
- **移除物体**: `Remove {object}` → 移除图像中的指定物体
- **添加物体**: `Add {object} {position}` → 在指定位置添加物体
- **替换物体**: `Replace {old_object} with {new_object}` → 替换物体

#### 风格转换
- **动漫风格**: `Turn this into anime artwork`
- **真实照片**: `Make this into a real photo`
- **油画风格**: `Turn this into an oil painting`
- **梵高风格**: `This image in the style of Van Gogh's "The Starry Night"`

#### 角色操作
- **改变表情**: `Make {subject} {expression}`
- **添加服装**: `Give {subject} {clothing}`
- **改变姿势**: `{subject} is now {action}`
- **角色变换**: `Turn {subject} into {new_form}`

## 模板扩展

要添加新的模板，编辑 `templates.json` 文件：

```json
{
  "categories": {
    "your_category": {
      "name": "你的类别名称",
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

## 注意事项

- 参数区分大小写
- 英文模板需要英文参数
- 某些模板可能不需要参数
- 自定义提示词会覆盖模板选择

## 🛠️ 模板管理功能

### 新增节点
- **Kontext 模板管理**：添加、修改、删除模板
- **Kontext 模板选择器**：动态获取模板列表

### 使用模板管理节点

#### 添加自定义模板
```
动作: add
类别: user_custom
模板名称: 我的模板
提示词: 将{object}变成{style}风格
描述: 自定义物体风格转换
参数: object,style
```

#### 管理现有模板
1. **添加**：创建新的提示词模板
2. **更新**：修改现有模板
3. **删除**：移除不需要的模板
4. **导出**：备份所有模板到文件
5. **导入**：从文件恢复模板

#### 模板文件结构
```
kontex_promt/
├── __init__.py
├── kontext_node.py          # 主节点
├── template_manager.py      # 模板管理节点
├── templates.json           # 默认模板
├── user_templates.json      # 用户自定义模板
└── README.md
```

### 自定义模板示例

#### 添加新模板
在模板管理节点中：
- **动作**: add
- **类别**: user_custom
- **模板名称**: 复古风格
- **提示词**: Turn this into vintage style {year} photo
- **参数**: year

#### 使用自定义模板
1. 在模板管理节点添加模板
2. 在模板选择器中选择"user_custom"类别
3. 选择你创建的模板
4. 填写参数使用

### 模板备份
```bash
# 导出模板
动作: export
文件路径: C:/Users/YourName/Documents/my_templates.json

# 导入模板
动作: import
文件路径: C:/Users/YourName/Documents/my_templates.json
```

## 故障排除

### 节点加载失败 / UTF-8编码问题
**症状**：Import failed, 乱码，节点不显示

**解决**：
1. **Windows用户**：用记事本打开文件，另存为UTF-8格式
2. **VS Code**：点击右下角编码 → 选择"UTF-8"
3. **重新安装**：
   ```bash
   cd ComfyUI/custom_nodes
   rm -rf kontex_promt
   git clone https://github.com/aqidesign/kontex_promt.git
   ```

### 文件结构验证
确保目录结构：
```
kontex_promt/
├── __init__.py
├── kontext_node.py
├── template_manager.py
├── templates.json
├── user_templates.json
└── README.md
```

## 更新日志

### v1.0.0
- 初始版本发布
- 包含7大类别1026个模板
- 支持中英文提示词
- 基于kontext真实训练数据整理

## 数据来源

本项目基于kontext图像编辑AI模型的训练提示词进行整理和分类，原始数据包含1026个真实使用场景的提示词。