from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import requests, re, html, json
from datetime import datetime

root=Path('/Users/romanselyanchyn/Library/CloudStorage/Dropbox/00-QPIT/Q-fellowship/QENERGY-STUDENT-SITE-REMAKE')
base='https://q-pit.kyushu-u.ac.jp/fellow-ship-en/'
for p in ['data','assets/photos/2025','assets/photos/2024','assets/photos/2023','assets/photos/2022','assets/photos/2021','students/2025','students/2024','students/2023','students/2022','students/2021']:
    (root/p).mkdir(parents=True, exist_ok=True)

def fetch(url):
    r=requests.get(url,timeout=30,headers={'User-Agent':'Mozilla/5.0 Hermes local prototype scraper for Kyushu Q-PIT'})
    r.raise_for_status()
    return r.text

def strip_tags(s):
    s=re.sub(r'<(script|style).*?</\1>',' ',s,flags=re.S|re.I)
    s=re.sub(r'<br\s*/?>','\n',s,flags=re.I)
    s=re.sub(r'</(p|div|li|td|th|tr|h\d)>','\n',s,flags=re.I)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'[ \t\r\f\v]+',' ',s)
    s=re.sub(r'\n\s*\n+','\n',s)
    return s.strip()

def attr(tag, name):
    m=re.search(name+r'\s*=\s*(["\'])(.*?)\1',tag,flags=re.I|re.S)
    return html.unescape(m.group(2)) if m else ''

def filename_from_url(url, fallback='file'):
    path=unquote(urlparse(url).path)
    name=Path(path).name or fallback
    name=re.sub(r'[^A-Za-z0-9._-]+','-',name)
    return name

def download(url, destdir):
    if not url: return ''
    name=filename_from_url(url)
    dest=Path(destdir)/name
    if dest.exists() and dest.stat().st_size>0: return str(dest.relative_to(root))
    try:
        r=requests.get(url,timeout=30,headers={'User-Agent':'Mozilla/5.0'})
        r.raise_for_status(); dest.write_bytes(r.content)
        return str(dest.relative_to(root))
    except Exception:
        return ''

def extract_sections(top_html):
    hs=list(re.finditer(r'<h([23])[^>]*>(.*?)</h\1>', top_html, flags=re.S|re.I))
    sections=[]
    for i,m in enumerate(hs):
        title=strip_tags(m.group(2))
        start=m.end(); end=hs[i+1].start() if i+1<len(hs) else len(top_html)
        block=top_html[start:end]
        sections.append((title,block))
    return sections

def links_from_block(block):
    links=[]
    for am in re.finditer(r'<a\b([^>]*)>(.*?)</a>',block,flags=re.S|re.I):
        atag,inner=am.group(1),am.group(2)
        href=urljoin(base, attr(atag,'href'))
        im=re.search(r'<img\b([^>]*)>',inner,flags=re.S|re.I)
        img=urljoin(base, attr(im.group(1),'src')) if im else ''
        alt=attr(im.group(1),'alt') if im else ''
        text=strip_tags(inner)
        links.append({'text':text,'href':href,'img':img,'alt':alt})
    return links

def names_from_body(block_or_text):
    txt=strip_tags(block_or_text)
    return [x.strip() for x in txt.split('\n') if x.strip()]

html_top=fetch(base)
sections=extract_sections(html_top)
section_map={title:{'body':strip_tags(block),'links':links_from_block(block)} for title,block in sections}
cohort_sections={}
for title,data in section_map.items():
    m=re.search(r'(Students|Fellows) in (20\d\d)', title)
    if m:
        cohort_sections[m.group(2)]=data

public={}
for year,data in cohort_sections.items():
    body_names=[x for x in names_from_body(data['body']) if len(x)<80 and not x.startswith('HOME')]
    links=[l for l in data['links'] if l.get('href')]
    seen=set(); clean=[]
    for l in links:
        key=l['href']
        if key in seen and not l.get('img'): continue
        seen.add(key); clean.append(l)
    students=[]
    for i,l in enumerate(clean):
        name=(body_names[i] if i < len(body_names) and not re.fullmatch(r'20\d\d', body_names[i]) else '') or l.get('text') or l.get('alt') or filename_from_url(l.get('href',''))
        img_local=download(l.get('img'), root/f'assets/photos/{year}') if l.get('img') else ''
        students.append({'name':name,'href':l['href'],'image_url':l.get('img',''),'image_local':img_local,'alt':l.get('alt','')})
    public[year]=students

def extract_detail(url):
    h=fetch(url)
    h1m=re.search(r'<h1[^>]*>(.*?)</h1>',h,flags=re.S|re.I)
    title=strip_tags(h1m.group(1)) if h1m else ''
    rows={}
    for rm in re.finditer(r'<tr[^>]*>(.*?)</tr>',h,flags=re.S|re.I):
        row=rm.group(1)
        cells=re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',row,flags=re.S|re.I)
        if len(cells)>=2:
            k=strip_tags(cells[0]).rstrip(':')
            v=strip_tags(cells[1])
            if k: rows[k]=v
    img=''
    fig=re.search(r'<figure[^>]*>.*?<img\b([^>]*)>',h,flags=re.S|re.I)
    if fig: img=urljoin(url, attr(fig.group(1),'src'))
    yts=[]
    for im in re.finditer(r'<iframe\b([^>]*)>',h,flags=re.S|re.I):
        src=attr(im.group(1),'src')
        if src: yts.append(urljoin(url,src))
    return {'title':title,'rows':rows,'image_url':img,'youtube':yts,'source':url}

for year,students in list(public.items()):
    if year not in ['2021','2022','2023','2024']: continue
    for st in students:
        try:
            d=extract_detail(st['href'])
            st.update(d)
            if d.get('image_url'):
                st['image_local']=download(d['image_url'], root/f'assets/photos/{year}') or st.get('image_local','')
        except Exception as e:
            st['extract_error']=str(e)

(root/'data/public_site_extracted.json').write_text(json.dumps(public,ensure_ascii=False,indent=2))
(root/'data/public_sections_extracted.json').write_text(json.dumps(section_map,ensure_ascii=False,indent=2))

def esc(s): return html.escape(str(s or ''))
def local_img_src(rel, prefix='../../'):
    return prefix + rel if rel else ''

def card_for_student(st, year):
    href=st.get('local_page') or st.get('href') or '#'
    img=local_img_src(st.get('image_local','')) if st.get('image_local') else ''
    rows=st.get('rows',{})
    title=rows.get('Title of the Research') or rows.get('Research theme') or rows.get('研究タイトル') or ''
    aff=rows.get('Affiliation') or ''
    img_html=f'<div class="thumb"><img src="{esc(img)}" alt="{esc(st.get("name"))}"></div>' if img else '<div class="thumb placeholder">PHOTO</div>'
    return f'<a class="card student rich" href="{esc(href)}">{img_html}<span class="tag">{year}</span><div class="name">{esc(st.get("name"))}</div><p class="muted">{esc(aff[:120])}</p><p>{esc(title[:180])}</p></a>'

def detail_page(st, year):
    rows=st.get('rows',{})
    title=rows.get('Name') or st.get('title') or st.get('name')
    research=rows.get('Title of the Research') or rows.get('Research theme') or ''
    outline=rows.get('Outline of Research') or rows.get('Research Outline') or ''
    aff=rows.get('Affiliation') or ''
    img=local_img_src(st.get('image_local','')) if st.get('image_local') else ''
    yt=''.join(f'<li><a href="{esc(u)}">YouTube / embedded video source</a></li>' for u in st.get('youtube',[]))
    portrait = f'<div class="portrait-large"><img src="{esc(img)}" alt="{esc(title)}"></div>' if img else ''
    videos = f'<section><div class="section-head"><h2>Videos</h2></div><div class="card"><ul>{yt}</ul></div></section>' if yt else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} - Q-ENERGY {year}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..600&family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../assets/css/main.css"></head><body><header class="top"><div class="topin"><a class="brand" href="../../index.html">K2-SPRING · Q-ENERGY</a><nav><a href="index.html">{year}</a><a href="../../index.html">Home</a><a href="{esc(st.get('source') or st.get('href'))}">Original</a></nav></div></header><main><section class="hero profile"><div>{portrait}</div><div><div class="eyebrow">Q-ENERGY {'Student' if year in ['2024'] else 'Fellow'} · {year}</div><h1>{esc(title)}</h1><p class="lead">{esc(research)}</p><p class="muted">{esc(aff)}</p><a class="btn alt" href="{esc(st.get('source') or st.get('href'))}">Original public page</a></div></section><section><div class="section-head"><h2>Research outline</h2><span class="muted">extracted from public Q-PIT page</span></div><div class="card"><p>{esc(outline) if outline else 'Source page did not provide a research outline in the standard table format.'}</p></div></section>{videos}</main><footer class="footer"><span>Extracted from public Q-PIT page for local prototype review.</span><span><a href="index.html">Back to {year}</a></span></footer></body></html>'''

for year,students in public.items():
    if year in ['2021','2022','2023','2024']:
        for idx,st in enumerate(students,1):
            slug=re.sub(r'[^a-z0-9]+','-',(st.get('name') or f'student-{idx}').lower()).strip('-') or f'student-{idx}'
            page=f'{slug}.html'
            st['local_page']=page
            (root/f'students/{year}'/page).write_text(detail_page(st,year))
    cards=''.join(card_for_student(st,year) for st in students)
    label='Students' if year in ['2024','2025'] else 'Fellows'
    note='PDF profile links from the public site are preserved.' if year=='2025' else 'Detail pages were generated from public Q-PIT profile tables.'
    (root/f'students/{year}/index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{year} {label} - Q-ENERGY</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..600&family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../assets/css/main.css"></head><body><header class="top"><div class="topin"><a class="brand" href="../../index.html">K2-SPRING · Q-ENERGY</a><nav><a href="../../index.html">Home</a><a href="https://q-pit.kyushu-u.ac.jp/fellow-ship-en/">Original site</a></nav></div></header><main><section class="hero"><div><div class="eyebrow">Q-ENERGY public archive</div><h1>{year}</h1><p class="lead">{label} in {year}. Publicly published information has been extracted into this local prototype.</p><a class="btn alt" href="../../index.html">Back to top</a></div><aside class="hero-card"><div class="metric"><b>{len(students)}</b><span>profiles/cards</span></div><p class="note">{esc(note)}</p></aside></section><section><div class="section-head"><h2>{label} in {year}</h2><span class="muted">public Q-PIT data</span></div><div class="grid people-grid">{cards}</div></section></main><footer class="footer"><span>Local prototype · extracted public information</span><span><a href="../../data/public_site_extracted.json">data JSON</a></span></footer></body></html>''')

css=root/'assets/css/main.css'
cs=css.read_text()
addon='''
.people-grid{grid-template-columns:repeat(3,1fr)}.student.rich{padding:0;overflow:hidden}.thumb{height:230px;background:var(--paper2);overflow:hidden;border-radius:18px 18px 0 0;display:grid;place-items:center;color:var(--muted);font-size:12px;letter-spacing:.15em}.thumb img{width:100%;height:100%;object-fit:cover;display:block}.student.rich .tag,.student.rich .name,.student.rich p{margin-left:18px;margin-right:18px}.student.rich .tag{margin-top:18px}.student.rich p:last-child{padding-bottom:20px}.profile{grid-template-columns:300px 1fr;align-items:center}.portrait-large{aspect-ratio:4/5;border-radius:22px;overflow:hidden;background:var(--paper2);box-shadow:0 35px 80px -55px #000}.portrait-large img{width:100%;height:100%;object-fit:cover}@media(max-width:900px){.people-grid{grid-template-columns:repeat(2,1fr)}.profile{grid-template-columns:1fr}}@media(max-width:560px){.people-grid{grid-template-columns:1fr}.thumb{height:260px}}
'''
if '.people-grid' not in cs:
    css.write_text(cs+'\n'+addon)

prog=root/'PROGRESS.md'
pr=prog.read_text() if prog.exists() else '# Progress\n'
pr += f'''\n\nWeb extraction update {datetime.now().isoformat(timespec='seconds')}\n- Scraped public English Q-PIT cohort sections.\n- Downloaded public portrait images into assets/photos/2021-2025.\n- Generated detail pages for public HTML profile pages in 2021-2024.\n- Preserved 2025 public PDF profile links and portrait cards.\n- Saved extracted data to data/public_site_extracted.json.\n'''
prog.write_text(pr)
print('years', sorted(public.keys()))
print('students/pages generated', sum(len(v) for v in public.values()))
print('json', root/'data/public_site_extracted.json')
