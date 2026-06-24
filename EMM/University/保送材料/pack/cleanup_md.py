import re

with open(r'd:\Work\mkdocs\docs\EMM\University\保送材料\pack\20-21联校保送问卷_重制排版.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Splitting lines to parse the structured content
lines = text.split('\n')

records = []
current_record = None

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    
    # Ignore specific garbage header lines
    if re.search(r'2020-2021年度濠江中學|填寫日期', line):
        continue

    # Matches university names (e.g., 報考大學：北京大學, 报考院校: 清华大学)
    univ_match = re.search(r'(報考大學|报考大学|报考院校|大學|大学|报考学校|學校|学校|報考學校)[:：]\s*(.*)', line)
    
    if univ_match:
        univ_name = univ_match.group(2).strip()
        univ_name = re.sub(r'[_＿]+$', '', univ_name).strip()
        
        # If there's an active record, save it first
        if current_record and current_record['univ']:
            records.append(current_record)
            
        current_record = {'univ': univ_name, 'major': '', 'format': '', 'questions': [], 'buffer': []}
        continue
        
    if not current_record:
        continue
        
    # Matches Major name
    major_match = re.search(r'(專業|专业)[:：]\s*(.*)', line)
    if major_match:
        major_val = major_match.group(2).strip()
        major_val = re.sub(r'^[_＿]+', '', major_val).strip() # clean leading underscores
        current_record['major'] = major_val
        # Sometimes OCR leaves major on the next line if the current line just says "專業："
        continue

    # Check exam format
    fmt_match = re.search(r'(考試形式|考试形式|面试形式)[:：]\s*(.*)', line)
    if fmt_match:
        fmt_val = fmt_match.group(2).strip()
        current_record['format'] = fmt_val
        continue

    # Check numbered questions like "1. ", "2、", "Q1:"
    q_match = re.match(r'^(\d+[\.、：:]|Q\d+[:：])\s*(.*)', line)
    if q_match:
        current_record['questions'].append(line)
        continue

    # Ignore other forms of interference words (OCR artifacts or irrelevant form fields)
    ignore_patterns = r'保送聯校生回答|班级|成績|操行|上學期|希望|答案为|個人面試.*小組面試|口筆試筆試科目|须時：|考試内容|請量详细|自我介绍|（請|）$|时长|候考|抽题|补充志愿|离场'
    if re.search(ignore_patterns, line):
        continue

    # If the major is empty but the following lines contain keywords like "类", "学", "工程", it might be the major pushed to the next line
    if current_record['major'] == '' or current_record['major'] == '_':
        if len(line) < 15 and re.search(r'(类|學|学|工程|管理|技术|科学|教育|语|言|翻译)', line):
            current_record['major'] = line
            continue

    # For any regular text that looks like a continuation of a question, append to the last question
    if current_record['questions']:
        # if it's not a question start but isn't garbage, it might belong to the previous question's answer
        if len(line) > 2 and not re.search(r'^\d', line):
            current_record['questions'][-1] += " " + line

# Add the final record
if current_record and current_record['univ']:
    records.append(current_record)

out_md = []
for r in records:
    if not r['univ']:
        continue
    
    out_md.append(f"## {r['univ']}")
    
    # Process major
    major = r['major'].replace('_', '').strip()
    if major:
        out_md.append(f"**{major}**")
    else:
        out_md.append(f"**未注明专业**")
        
    # Process format
    fmt = r['format'].replace('口', ' ').strip() # Often checkboxes "口" are OCR'd as text
    if not fmt:
        fmt = "暂无说明"
    out_md.append(f"考试形式：{fmt}")
    
    # Process questions
    for q in r['questions']:
        out_md.append(q)
        
    out_md.append("") # Empty line between records

with open(r'd:\Work\mkdocs\docs\EMM\University\保送材料\pack\20-21联校保送问卷_终版格式.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_md))

print(f"Total structured interviews extracted: {len(records)}")
