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
2. 选择具体模板（如"移除物体"、"动漫风格"等）
3. 填写target参数（目标对象/位置/数值）
4. 获取生成的英文提示词

### 参数说明
- **template**: 具体模板（18个预设选项）
- **target**: 目标对象/位置/数值（根据模板需求填写）
- **custom_prompt**: 自定义提示词（优先使用）

### 使用示例

#### 物体操作
- **移除物体**: target="桌子" → "Remove 桌子"
- **添加物体**: target="花朵" → "Add 花朵"
- **替换物体**: target="自行车" → "Replace with 自行车"

#### 风格转换
- **动漫风格**: target="高质量" → "Transform into anime style 高质量"
- **赛博朋克**: target="霓虹灯" → "Apply cyberpunk aesthetic 霓虹灯"
- **复古风格**: target="1980年代" → "Apply vintage style 1980年代"

#### 角色操作
- **改变表情**: target="微笑" → "Change expression to 微笑"
- **添加服装**: target="西装" → "Add 西装 clothing"

#### 环境变换
- **改变背景**: target="海滩" → "Change background to 海滩"
- **添加天气效果**: target="雨天" → "Add 雨天 weather effect"

#### 颜色调整
- **黑白照片**: （无需参数）→ "Convert to black and white"
- **复古色调**: target="暖色" → "Apply vintage tone 暖色"

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
├── templates.json
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