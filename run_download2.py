import urllib.request
import re
import os
import urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://appl2.dsedj.gov.mo/ChinaUEnrollment/UPublic/EnrollmentBrief.jsp'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
except Exception as e:
    print('Failed to download html:', e)
    exit(1)

output_dir = r'd:\Work\mkdocs\docs\EMM\University\招生简章'
os.makedirs(output_dir, exist_ok=True)
count = 0

existing_files = os.listdir(output_dir)

rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE)
for row in rows:
    cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
    if len(cols) >= 7:
        school_name_raw = re.sub(r'<[^>]+>', '', cols[2])
        # Removing any spaces and newlines e.g. "北京大 学" -> "北京大学"
        school_name = re.sub(r'\s+', '', school_name_raw)
        
        link_match = re.search(r'href=[\"\'](DownloadUniDoc\.jsp[^\"\']*)[\"\']', cols[6], re.IGNORECASE)
        if not link_match:
             link_match = re.search(r'href=[\"\']([^\"\']*\.pdf)[\"\']', cols[6], re.IGNORECASE)
        
        if link_match and school_name:
            already_has = False
            for ef in existing_files:
                if ef.startswith(school_name + '招生简章'):
                    already_has = True
                    break
            
            if already_has:
                # print(f"Already have {school_name}")
                continue
                
            link = link_match.group(1).replace('&amp;', '&')
            full_link = urllib.parse.urljoin(url, link)
            
            try:
                parsed_link = urllib.parse.urlparse(full_link)
                encoded_path = urllib.parse.quote(parsed_link.path)
                encoded_query = urllib.parse.quote(parsed_link.query, safe='=&')
                encoded_url = urllib.parse.urlunparse((parsed_link.scheme, parsed_link.netloc, encoded_path, parsed_link.params, encoded_query, parsed_link.fragment))

                res = urllib.request.urlopen(urllib.request.Request(encoded_url, headers={'User-Agent': 'Mozilla/5.0'}))
                cd = res.headers.get('Content-Disposition', '')
                ext = '.pdf'
                if 'filename=' in cd:
                    filename = cd.split('filename=')[1].strip('\"\'')
                else:
                    parsed = urllib.parse.urlparse(full_link)
                    query = urllib.parse.parse_qs(parsed.query)
                    if 'fileName' in query:
                        ext = os.path.splitext(query['fileName'][0])[1] or '.pdf'
                
                final_name = os.path.join(output_dir, f'{school_name}招生简章{ext}')
                with open(final_name, 'wb') as f:
                    f.write(res.read())
                print(f'Downloaded new: {final_name}')
                existing_files.append(os.path.basename(final_name))
                count += 1
            except Exception as e:
                print(f'Failed {school_name}: {e}')

print(f'Finished! Total {count} new downloaded.')
