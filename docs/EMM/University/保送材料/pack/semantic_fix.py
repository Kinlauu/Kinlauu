import re

# Simple handcrafted corrections for common Traditional Chinese OCR errors caused by Simplified tuning
replacements = {
    # Common words
    '經清': '經濟', '经清': '经济', 
    '嚴史': '歷史', '严史': '历史',
    '孿': '學', '學篱': '學習', '学篱': '学习', '學鸡': '學習',
    '离生': '醫生', '灕生': '醫生', '床离生': '临床医生',
    '徹台': '手術台', '彻台': '手术台',
    '單會': '單位', '单会': '单位',
    '缺影度': '缺點',
    '道應': '適應', '道应': '适应',
    '麻？': '嗎？', '麻?': '嗎？',
    '口麻': '嗎',
    '闪地': '內地', '内也': '內地',
    '干.': '7.', '十.': '7.',
    '！.': '1.',
    '水塘遠？后': '水塘遠？答',
    '水塘遠？後': '水塘遠？答',
    '怎么鹰': '怎麼辦', '怎鹰': '怎麼辦',
    '！1.': '11.', '!1.': '11.',
    '育.': '體育', '育': '體育',
    '成锁状沉': '成績狀況', '成绩狀沉': '成绩状况',
    '羽毛珠': '羽毛球', '羽毛球': '羽毛球',
    '回棵': '目標', '回标': '目标',
    '！1': '11', '晋': '書',
    '计算机': '計算機',
    '环塊': '環境',
    '与趣': '興趣',
    '计算': '計算',
    '晋': '書',
    
    # 针对20-21联校保送问卷的常见奇怪 OCR mapping 进行直接修正：
    '为甚報經濟不報算机': '為甚麼報經濟不報計算機',
    '计算是偏向能力': '計算機是偏向能力',
    '经清是同时有能力': '經濟是同時有能力',
    '与趣因素': '興趣因素',
    '你為攻读經清備了甚': '你為攻讀經濟準備了甚麼',
    '讀了经濟學的晋': '讀了經濟學的書',
    '以北大 為回棵': '以北大為目標',
    '決定背水一': '決定背水一戰',
    '败在育': '敗在體育',
    '你以後是想做研究方面還是上手彻台的床离生？': '你以後是想做研究方面還是上手術台的臨床醫生？',
    '有了AI，工作单会怎樣呢？': '有了AI，工作單位會怎樣呢？',
    '生活/學鸡': '生活/學習',
    '干.你大學有甚期待和疑問吗？': '7.你大學有甚麼期待和疑問嗎？',
    '你覺得你道應得了麻？': '你覺得你適應得了嗎？',
    '你有甚缺影度？': '你有甚麼缺點？',
    
    # OCR errors for university names & majors
    '床醫學': '臨床醫學',
    '床医学': '临床医学',
}

def correct_text(text):
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    return text

with open(r'd:\Work\mkdocs\docs\EMM\University\保送材料\pack\20-21联校保送问卷_重制排版.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Apply heuristic error correction
text = correct_text(text)

lines = text.split('\n')
records = []
current_record = None

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    
    # Ignore
    if re.search(r'2020-2021年度濠江中學|填寫日期', line):
        continue

    # Univ
    univ_match = re.search(r'(報考大學|报考大学|报考院校|大學|大学|报考学校|學校|学校|報考學校)[:：]\s*(.*)', line)
    if univ_match:
        univ_name = univ_match.group(2).strip()
        univ_name = re.sub(r'[_＿]+$', '', univ_name).strip()
        if current_record and current_record['univ']:
            records.append(current_record)
        current_record = {'univ': univ_name, 'major': '', 'format': '', 'questions': [], 'buffer': []}
        continue
        
    if not current_record:
        continue
        
    # Major
    major_match = re.search(r'(專業|专业)[:：]\s*(.*)', line)
    if major_match:
        major_val = major_match.group(2).strip()
        major_val = re.sub(r'^[_＿]+', '', major_val).strip() 
        current_record['major'] = major_val
        continue

    # Format
    fmt_match = re.search(r'(考試形式|考试形式|面试形式)[:：]\s*(.*)', line)
    if fmt_match:
        fmt_val = fmt_match.group(2).strip()
        current_record['format'] = fmt_val
        continue

    # Question
    q_match = re.match(r'^(\d+[\.、：:]|Q\d+[:：])\s*(.*)', line)
    if q_match:
        current_record['questions'].append(f"{q_match.group(1)} {q_match.group(2)}")
        continue

    # Ignore text
    ignore_patterns = r'保送聯校生回答|班级|班級|成績|操行|上學期|希望|答案为|個人面試.*小組面試|口筆試筆試科目|须時：|須時|考試内容|考试内容|請量详细|自我介绍|（請|）$|时长|候考|抽题|补充志愿|离场|以上答案'
    if re.search(ignore_patterns, line):
        continue

    # Major push
    if current_record['major'] == '' or current_record['major'] == '_':
        if len(line) < 15 and re.search(r'(类|學|学|工程|管理|技术|科学|教育|语|言|翻译)', line):
            current_record['major'] = line
            continue

    if current_record['questions']:
        if len(line) > 2 and not re.search(r'^\d', line):
            current_record['questions'][-1] += " " + line

if current_record and current_record['univ']:
    records.append(current_record)

out_md = []
for r in records:
    if not r['univ']:
        continue
    
    out_md.append(f"## {r['univ']}")
    
    major = r['major'].replace('_', '').strip()
    if major:
        out_md.append(f"**{major}**")
    else: out_md.append(f"**未注明专业**")
        
    fmt = r['format'].replace('口', ' ').strip()
    if not fmt: fmt = "暂无说明"
    out_md.append(f"考试形式：{fmt}")
    
    for q in r['questions']:
        out_md.append(q)
        
    out_md.append("")

with open(r'd:\Work\mkdocs\docs\EMM\University\保送材料\pack\20-21联校保送问卷_繁体语义修正版.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_md))

print(f"Total structured interviews extracted: {len(records)}")
