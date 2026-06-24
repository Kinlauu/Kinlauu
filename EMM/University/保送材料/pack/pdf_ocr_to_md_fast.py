import fitz
import re
import os
import concurrent.futures
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()

def process_page(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(1.5, 1.5)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    
    result, _ = ocr(img_data)
    
    text = ""
    if result:
        for line in result:
            text += line[1] + "\n"
    return page_num, text

def extract_and_format_pdf(pdf_path, output_md_path):
    print(f"正在处理: {pdf_path}")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()
    
    all_text_dict = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        futures = {executor.submit(process_page, pdf_path, i): i for i in range(total_pages)}
        
        for future in concurrent.futures.as_completed(futures):
            page_num = futures[future]
            try:
                p_num, text = future.result()
                all_text_dict[p_num] = text
                print(f"完成提取第 {p_num + 1}/{total_pages} 页")
            except Exception as exc:
                print(f"第 {page_num + 1} 页提取产生异常: {exc}")
                all_text_dict[page_num] = ""
            
    print("OCR 提取完成，开始解析格式并去除姓名...")

    all_text = ""
    for i in range(total_pages):
        all_text += all_text_dict.get(i, "") + "\n---PAGE_BREAK---\n\n"

    lines = all_text.split('\n')
    formatted_md = ""
    current_university = ""
    
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        univ_match = re.search(r'(报考院校|录取院校|学校)[:：]?\s*(.*?大学|.*?学院)', line_clean)
        if univ_match:
            univ = univ_match.group(2).strip()
            if univ and univ != current_university:
                current_university = univ
                formatted_md += f"\n## {current_university}\n\n"
                continue
                
        name_major_match = re.search(r'姓名[:：]?\s*[\u4e00-\u9fa5]{2,4}\s*(专业|录取专业|报考专业)[:：]?\s*(.*)', line_clean)
        if name_major_match:
            major = name_major_match.group(2).strip()
            formatted_md += f"- **考生** **{major}**\n"
            continue
            
        name_match = re.search(r'姓名[:：]?\s*([\u4e00-\u9fa5]{2,4})', line_clean)
        if name_match:
            line_clean = line_clean.replace(name_match.group(1), "考生")
            formatted_md += f"- **考生**\n"
            continue
            
        major_match = re.search(r'(专业|录取专业)[:：]?\s*(.*)', line_clean)
        if major_match:
            major = major_match.group(2).strip()
            if major:
                formatted_md += f"  - **专业**: **{major}**\n"
            continue
            
        q_match = re.match(r'^(\d+[\.、：:]|Q\d+[:：])\s*(.*)', line_clean)
        if q_match:
            formatted_md += f"  {q_match.group(1)} {q_match.group(2)}\n"
            continue
            
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
