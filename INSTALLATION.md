# 安装指南 - UTF-8编码特别说明

## 🔧 安装步骤

### 方法1：Git克隆（推荐）
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/aqidesign/kontex_promt.git
```

### 方法2：手动下载
1. 从GitHub下载ZIP文件
2. 解压到 `ComfyUI/custom_nodes/kontex_promt/`
3. **重要**：确保所有文件保持UTF-8编码

## ⚠️ UTF-8编码问题解决

### 问题症状
- 节点加载失败
- 文件显示乱码
- Import failed错误

### 解决方案

#### Windows用户：
1. **使用记事本打开检查**：
   - 右键文件 → 打开方式 → 记事本
   - 如果显示正常，说明编码正确

2. **转换编码**：
   - 用记事本打开每个文件
   - 文件 → 另存为 → 编码选择 "UTF-8"
   - 覆盖原文件

#### VS Code用户：
1. 打开项目文件夹
2. 点击右下角的编码显示（如"UTF-8"或"GB2312"）
3. 选择 "另存为UTF-8"

#### 命令行转换（高级用户）：
```bash
# 在ComfyUI/custom_nodes/kontex_promt目录下
find . -type f -name "*.py" -exec iconv -f GB2312 -t UTF-8 {} -o {}.utf8 \; -exec mv {}.utf8 {} \;
find . -type f -name "*.json" -exec iconv -f GB2312 -t UTF-8 {} -o {}.utf8 \; -exec mv {}.utf8 {} \;
```

## 🔍 验证安装

### 测试节点加载
1. 重启ComfyUI
2. 查看控制台输出，确认无错误
3. 在节点列表中查找 "kontext" 类别

### 测试功能
1. 添加 "Kontext 提示词模板" 节点
2. 选择 "动漫风格" 模板
3. 应该显示提示词 "Turn this into anime artwork"

## 🛠️ 常见问题解决

### 节点不显示
```
[ERROR] Failed to load custom node
```
**解决**：
1. 检查文件编码
2. 确认所有文件在正确的目录
3. 重启ComfyUI

### 乱码问题
```
UnicodeDecodeError: 'gbk' codec can't decode
```
**解决**：
1. 用记事本重新保存为UTF-8
2. 删除并重新克隆仓库

### 路径问题
```
FileNotFoundError: templates.json
```
**解决**：
1. 确保所有文件在同一目录
2. 检查文件权限

## 📁 文件结构验证

确保你的目录结构如下：
```
ComfyUI/custom_nodes/kontex_promt/
├── __init__.py
├── kontext_node.py
├── templates.json
├── requirements.txt
├── README.md
└── INSTALLATION.md
```

## 🔄 重新安装

如果仍有问题：
1. 删除 `kontex_promt` 文件夹
2. 重新git clone
3. 确认所有文件为UTF-8编码
4. 重启ComfyUI

## 📞 技术支持

如果问题持续，请：
1. 检查ComfyUI控制台完整错误信息
2. 确认ComfyUI版本兼容性
3. 在GitHub提交issue