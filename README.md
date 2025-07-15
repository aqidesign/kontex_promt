# Kontext ComfyUI 节点

基于 kontext 图像编辑 AI 模型训练数据的 ComfyUI 提示词模板节点。

## 功能特点

- **7大类别模板**：物体操作、风格转换、角色操作、环境变换、文字操作、颜色调整、镜头操作
- **动态参数**：支持自定义参数输入
- **中文支持**：包含中英文对照的提示词
- **易于扩展**：可通过修改 JSON 文件添加新模板
- **1026个模板**：基于真实训练数据整理

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

## 故障排除

### 问题1：节点不显示
- 确保文件放在正确的 `custom_nodes` 目录
- 检查 ComfyUI 控制台是否有错误信息

### 问题2：模板加载失败
- 检查 `templates.json` 文件是否存在且格式正确
- 确保 JSON 文件使用 UTF-8 编码

### 问题3：参数不生效
- 检查参数是否与模板要求的名称匹配
- 确保参数值不为空

## 更新日志

### v1.0.0
- 初始版本发布
- 包含7大类别1026个模板
- 支持中英文提示词
- 基于kontext真实训练数据整理

## 数据来源

本项目基于kontext图像编辑AI模型的训练提示词进行整理和分类，原始数据包含1026个真实使用场景的提示词。