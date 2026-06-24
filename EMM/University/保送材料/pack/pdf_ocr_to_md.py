import fitz  # PyMuPDF
import re
import os
from rapidocr_onnxruntime import RapidOCR

def extract_and_format_pdf(pdf_path, output_md_path):
    print(f"正在处理: {pdf_path}")
    print("初始化 OCR 模型 (首次运行可能需要下载模型)...")
    ocr = RapidOCR()
    
    doc = fitz.open(pdf_path)
    all_text = ""
    
    for page_num in range(len(doc)):
        print(f"正在提取第 {page_num + 1}/{len(doc)} 页...")
        page = doc[page_num]
        
        # 将页面渲染为高分辨率图像，以提高 OCR 准确率（缩放系数为 2 或 3）
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # 转换为 numpy 格式供 OCR 读取
        img_data = pix.tobytes("png")
        
        # 运行 OCR
        result, _ = ocr(img_data)
        
        if result:
            # result 格式: [[box, text, confidence], ...]
            for line in result:
                all_text += line[1] + "\n"
        all_text += "\n---PAGE_BREAK---\n\n"
        
    print("OCR 提取完成，开始解析格式并去除姓名...")

    # ==========================
    # 启发式解析并生成 Markdown
    # ==========================
    
    # 匹配“姓名”、“院校”、“专业”等字段
    # 因为不同的问卷格式不同，这里的正则做了基础兼容，您可能需要根据真实输出微调
    lines = all_text.split('\n')
    
    formatted_md = ""
    current_university = ""
    
    # 模拟简单的状态机进行文字提取
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            continue
            
        # 匹配大学/院校名称
        # 如果包含“大学”、“学院”或者“院校：”
        univ_match = re.search(r'(报考院校|录取院校|学校)[:：]?\s*(.*?大学|.*?学院)', line_clean)
        if univ_match:
            univ = univ_match.group(2).strip()
            if univ and univ != current_university:
                current_university = univ
                formatted_md += f"\n## {current_university}\n\n"
                continue
                
        # 匹配姓名与专业 (例如: 姓名：张三  专业：计算机科学)
        name_major_match = re.search(r'姓名[:：]?\s*[\u4e00-\u9fa5]{2,4}\s*(专业|录取专业|报考专业)[:：]?\s*(.*)', line_clean)
        if name_major_match:
            major = name_major_match.group(2).strip()
            formatted_md += f"- **考生** **{major}**\n"
            continue
            
        # 匹配单纯的姓名
        name_match = re.search(r'姓名[:：]?\s*([\u4e00-\u9fa5]{2,4})', line_clean)
        if name_match:
            line_clean = line_clean.replace(name_match.group(1), "考生")
            # 如果这一行本来是用来标明人的，我们可以尝试把它转化为 `- **考生**`
            formatted_md += f"- **考生**\n"
            continue
            
        # 匹配单纯的专业
        major_match = re.search(r'(专业|录取专业)[:：]?\s*(.*)', line_clean)
        if major_match:
            major = major_match.group(2).strip()
            if major:
                formatted_md += f"  - **专业**: **{major}**\n"
            continue
            
        # 匹配面试问题 (题号如 1. 2. 3. 或者 Q1: )
        q_match = re.match(r'^(\d+[\.、：:]|Q\d+[:：])\s*(.*)', line_clean)
        if q_match:
            formatted_md += f"  {q_match.group(1)} {q_match.group(2)}\n"
            continue
            
        # 其他内容（如面试形式、总结等）直接追加
        if "PAGE_BREAK" not in line_clean and len(line_clean) > 2:
            formatted_md += f"  > {line_clean}\n"
            
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(formatted_md)
        
    print(f"处理完成，保存至 -> {output_md_path}")


if __name__ == "__main__":
    base_dir = r"D:\Work\mkdocs\docs\EMM\University\保送材料\pack"
    pdfs = [
        "18-19聯校保送生問卷.pdf",
        "19-20聯校保送問卷.pdf",
        "20-21聯校保送問卷.pdf"
    ]
    
    for pdf in pdfs:
        pdf_path = os.path.join(base_dir, pdf)
        md_path = os.path.join(base_dir, pdf.replace(".pdf", "_转录.md"))
        if os.path.exists(pdf_path):
            extract_and_format_pdf(pdf_path, md_path)
        else:
            print(f"未找到文件: {pdf_path}")
