import fitz
import re
import os
import concurrent.futures
from paddleocr import PaddleOCR

# Setup paddleocr equipped with traditional Chinese
ocr = PaddleOCR(use_angle_cls=False, lang='chinese_cht', show_log=False)

def process_page(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(1.5, 1.5)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    
    # Save the bytes as temp image or pass bytes directly (PaddleOCR accepts numpy arrays or image paths)
    import numpy as np
    import cv2
    nparr = np.frombuffer(img_data, np.uint8)
    img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    result = ocr.ocr(img_cv2, cls=False)
    
    text = ""
    if result and result[0]:
        for line in result[0]:
            text += line[1][0] + "\n"
    return page_num, text

def format_text(all_text):
    lines = all_text.split('\n')
    formatted_md = ""
    current_university = ""
    current_major = ""
    
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        # Clean irrelevant headers
        line_clean = re.sub(r'2020[-_]?2021年度濠江中學推.*?[保筆].*?問卷', '', line_clean)
        line_clean = re.sub(r'填寫日期[：:]?', '', line_clean)
        
        # sometimes '濠江中学推' might be mis-ocr'd
        line_clean = re.sub(r'.*濠江中學.*問卷', '', line_clean)
        
        line_clean = line_clean.strip()
        if not line_clean:
            continue
            
        # Match University
        univ_match = re.search(r'(報考大學|报考大学|報考院校|报考院校|大學|大学|报考学校|學校|学校|報考學校)[:：]?\s*(.*?大學|.*?大学|.*?學院|.*?学院)', line_clean)
        if univ_match:
            univ = univ_match.group(2).strip()
            univ = re.sub(r'[_＿]+$', '', univ).strip()
            if univ and univ != current_university:
                current_university = univ
                formatted_md += f"\n## {current_university}\n"
            continue
                
        # Match Major
        major_match = re.search(r'(專業|专业|錄取專業|录取专业|報考專業|报考专业|專業名稱|专业名称)[:：]?\s*(.*)', line_clean)
        if major_match:
            major = major_match.group(2).strip()
            if major:
                major = re.sub(r'姓名[:：]?\s*[\u4e00-\u9fa5]{2,4}\s*', '', major).strip()
                major = re.sub(r'[_＿]+$', '', major).strip()
                if major != current_major and major != "":
                    current_major = major
                    formatted_md += f"**{current_major}**\n"
            continue
            
        # Fallback for major string pushed to the next line (e.g. '學類' / '学类')
        if current_major == "" and (len(line_clean) < 15 and re.search(r'(類|类|學|学|工程|管理|技術|技术|科學|科学|教育|語|语|言|翻譯|翻译)', line_clean)):
            current_major = line_clean
            formatted_md += f"**{current_major}**\n"
            continue
            
        # Check Exam Format
        exam_format_match = re.search(r'(考試形式|考试形式|測試形式|测试形式|面試形式|面试形式)[:：]\s*(.*)', line_clean)
        if exam_format_match:
            fmt = exam_format_match.group(2).strip()
            fmt = re.sub(r'口', ' ', fmt).strip() # OCR '口' instead of checkbox
            formatted_md += f"考試形式：{fmt}\n"
            continue
            
        # Ignore Garbage lines
        ignore_patterns = r'保送聯校生回答|班級|班级|成績|成绩|操行|上學期|希望|答案为|個人面試.*小組面試|个人面试.*小组面试|口筆試筆試科目|须時：|須時|考試内容|考试内容|請量详细|自我介绍|（請|）$|时长|时長|候考|抽题|抽題|补充志愿|補充志願|离场|離場'
        if re.search(ignore_patterns, line_clean):
            continue
            
        # Ignore Name
        if re.search(r'姓名[:：]?\s*[\u4e00-\u9fa5]{2,4}', line_clean):
            continue

        # Questions (1. 2. 3.)
        q_match = re.match(r'^(\d+[\.、：:]|Q\d+[:：])\s*(.*)', line_clean)
        if q_match:
            formatted_md += f"{q_match.group(1)} {q_match.group(2)}\n"
            continue
            
        # Other text joining the last question if appropriate
        if "PAGE_BREAK" not in line_clean and len(line_clean) > 2:
            # Check if this line looks like part of an answer
            formatted_md += f"{line_clean}\n"
            
    return formatted_md

def extract_and_format_pdf(pdf_path, output_md_path):
    print(f"正在理: {pdf_path}")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()
    
    all_text_dict = {}
    
    # Process sequentially or mildly parallel to avoid paddleocr crashing on some machines
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_page, pdf_path, i): i for i in range(total_pages)}
        for future in concurrent.futures.as_completed(futures):
            p_num = futures[future]
            try:
                _, text = future.result()
                all_text_dict[p_num] = text
                print(f"完成提取第 {p_num + 1}/{total_pages} 页")
            except Exception as exc:
                print(f"第 {p_num + 1} 页提取异常: {exc}")
                all_text_dict[p_num] = ""
            
    print("OCR 提取完成，開始解析格式...")

    all_text = ""
    for i in range(total_pages):
        all_text += all_text_dict.get(i, "") + "\n\n"

    # Format text according to requirements
    formatted_md = format_text(all_text)
            
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(formatted_md)
        
    print(f"處理完成，保存至 -> {output_md_path}")


if __name__ == "__main__":
    base_dir = r"D:\Work\mkdocs\docs\EMM\University\保送材料\pack"
    pdf_file = "20-21聯校保送問卷.pdf"
    
    pdf_path = os.path.join(base_dir, pdf_file)
    md_path = os.path.join(base_dir, "20-21联校保送问卷_繁体高精版.md")
    
    if os.path.exists(pdf_path):
        extract_and_format_pdf(pdf_path, md_path)
    else:
        print(f"未找到文件: {pdf_path}")
