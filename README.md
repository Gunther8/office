# PDF 纠偏工具

## 简介
本项目是一个用于校正 PDF 文件页面倾斜的工具，基于 Python 开发，使用 OpenCV 进行图像处理，PyMuPDF 进行 PDF 解析。

## 功能特点
- **自动检测页面倾斜角度** 并进行校正
- **支持多页 PDF 处理**
- **高分辨率渲染** 确保校正后 PDF 质量
- **简洁的 GUI 交互** 选择输入和输出文件

## 依赖库
使用本项目前，请确保已安装以下 Python 依赖库：

```sh
pip install opencv-python numpy pymupdf pillow
```

## 使用方法
1. 运行脚本：
   ```sh
   python 1.py
   ```
2. 选择要校正的 PDF 文件。
3. 选择输出 PDF 文件的保存路径。
4. 程序自动处理 PDF 并保存校正后的文件。

## 代码结构
- `select_file(title, filetypes)`: 选择输入文件
- `select_output_file(title)`: 选择输出文件
- `deskew_image(image)`: 纠正图像倾斜
- `deskew_pdf(input_pdf, output_pdf)`: 纠正 PDF 文件中的所有页面
- `main`: 用户交互流程


## 贡献
欢迎提交 PR 或 Issues 提出改进建议！

