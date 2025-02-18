from tkinter import Tk, filedialog
from PIL import Image
import fitz  # PyMuPDF
import cv2
import numpy as np

def select_file(title, filetypes):
    """弹出文件选择对话框"""
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

def select_output_file(title):
    """弹出保存文件对话框"""
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.asksaveasfilename(title=title, defaultextension=".pdf", filetypes=[("PDF 文件", "*.pdf")])
    return file_path

def deskew_image(image):
    """校正图像倾斜"""
    print("[INFO] 正在检测图像倾斜角度...")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    coords = np.column_stack(np.where(binary > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    print(f"[INFO] 检测到的倾斜角度为：{angle:.2f}°")
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    print("[INFO] 图像校正完成！")
    return rotated

def deskew_pdf(input_pdf, output_pdf):
    """校正PDF文件中的页面"""
    print(f"[INFO] 正在打开PDF文件：{input_pdf}")
    pdf_document = fitz.open(input_pdf)
    deskewed_images = []
    for page_num in range(len(pdf_document)):
        print(f"[INFO] 正在处理第 {page_num + 1} 页，共 {len(pdf_document)} 页...")
        page = pdf_document[page_num]
        pix = page.get_pixmap(dpi=300)  # 渲染页面为高分辨率图像
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 转换为 OpenCV 图像格式
        cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        corrected = deskew_image(cv_image)  # 校正倾斜
        deskewed_images.append(Image.fromarray(cv2.cvtColor(corrected, cv2.COLOR_BGR2RGB)))
    print("[INFO] 所有页面校正完成，正在保存校正后的PDF文件...")
    deskewed_images[0].save(output_pdf, save_all=True, append_images=deskewed_images[1:])
    print("[INFO] PDF文件保存完成！")

# 主程序入口
if __name__ == "__main__":
    print("请选择输入的PDF文件...")
    input_pdf = select_file("选择输入PDF文件", [("PDF 文件", "*.pdf")])
    if not input_pdf:
        print("未选择输入文件，程序退出。")
        exit()

    print("请选择输出PDF文件路径...")
    output_pdf = select_output_file("保存输出PDF文件")
    if not output_pdf:
        print("未选择输出文件，程序退出。")
        exit()

    print(f"正在处理文件：{input_pdf}")
    deskew_pdf(input_pdf, output_pdf)
    print(f"处理完成！校正后的PDF保存为：{output_pdf}")
