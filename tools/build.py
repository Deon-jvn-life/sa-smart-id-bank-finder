import json,re,os,html as H
D="21 October 2026"
BASE="https://sa-smart-id-bank-finder.vercel.app"
SITE_NAME="Smart ID at the Bank (SA)"
# Optional search-console tokens. Leave a value empty to omit that meta tag.
GOOGLE_SITE_VERIFICATION=""
MSVALIDATE_01=""
DISCLAIMER="For general information only. This independent site is not affiliated with any government, bank or agency. Information can change and may contain errors; always confirm with the official source before you act. Nothing here is legal, financial or professional advice, and we accept no liability for decisions made using it."
DISCLAIMER_SHORT="For general information only. This independent site is not affiliated with any government, bank or agency."
RELATED_GUIDE="https://sa-passport-id-usa-guide-w1ab.vercel.app/"
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.abspath(os.path.join(HERE,"..","site"))
S=dict(
 locator="https://myhomeaffairsonline.dha.gov.za/partner-branch",
 api="https://myhomeaffairsonline.dha.gov.za/api/civics/search-partner?partner_id=",
 digital="https://www.dha.gov.za/index.php/id-smart-card/banks-digital",
 legacy="https://www.dha.gov.za/index.php/id-smart-card/bank-branches",
 fees="https://www.dha.gov.za/index.php/fees",
 travel="https://www.dha.gov.za/index.php/civic-services/travel-documents",
 sidpdf="https://www.dha.gov.za/files/Brochures/SmartIDrequirements.pdf",
 iddocs="https://www.dha.gov.za/index.php/civic-services/identity-documents",
 idapply="https://www.gov.za/services/services-residents/citizenship/personal-identification/apply-for-identity-document",
 idact="https://www.gov.za/sites/default/files/gcis_document/201409/a68-97.pdf",
 idactpage="https://www.gov.za/documents/identification-act",
 idamd="https://www.gov.za/documents/identification-amendment-act",
 aff="https://www.gov.za/faq/justice-and-crime-prevention/what-affidavit",
 vuku="https://www.vukuzenzele.gov.za/smart-id-card-here",
 dupid="https://www.dha.gov.za/index.php/notices/273-duplicate-ids",
 tic2011="https://www.gov.za/news/media-statements/minister-dlamini-zuma-directs-delinking-temporary-identity-certificates",
 golive="https://www.gov.za/news/media-statements/home-affairs-first-bank-branches-go-live-under-new-digital-partnership-model",
 absams="https://www.gov.za/news/media-statements/home-affairs-expanding-smart-id-access-digital-partnership-absa-22-jul-2026",
 locms="https://www.gov.za/news/media-statements/minister-leon-schreiber-launches-new-home-affairs-online-services-03-aug-2026",
 capms="https://www.gov.za/news/media-statements/home-affairs-and-capitec-partner-enable-smart-id-and-passport-applications",
 fnbsbms="https://www.gov.za/news/media-statements/home-affairs-partners-fnb-and-standard-bank-smart-id-and-passport",
 cap="https://www.capitecbank.co.za/blog/articles/best-way-to-bank/smart-id-at-our-branches/",
 caploc="https://www.capitecbank.co.za/branches/",
 sb="https://www.standardbank.co.za/southafrica/personal/products-and-services/ways-to-bank/self-service-banking/get-your-smart-id-or-passport",
 sbnews="https://www.standardbank.co.za/southafrica/news-and-media/newsroom/standard-bank-and-home-affairs-expand-smart-id-services-through-bank-branches",
 fnb="https://www.fnb.co.za/ways-to-bank/branch.html",
 absa="https://www.absa.co.za/personal/smart-id/",
 ned="https://personal.nedbank.co.za/learn/blog/apply-for-a-smart-id-online.html",
 babs="https://www.dha.gov.za/index.php/notices/1557-branch-appointment-booking-system-babs-available-offices",
 babsmove="https://services.dha.gov.za/",
 mhao="https://myhomeaffairsonline.dha.gov.za/",
 mhaofaq="https://myhomeaffairsonline.dha.gov.za/faq",
 mhaoreg="https://myhomeaffairsonline.dha.gov.za/registration",
 ehowto="https://ehome.dha.gov.za/ehomeaffairsv3/Content/HowToGuide.pdf",
 festive="https://www.dha.gov.za/index.php/statements-speeches/1982-home-affairs-extends-operating-hours-for-the-festive-season",
 dhacontact="https://www.dha.gov.za/index.php/77-contacts",
 capnews="https://www.capitecbank.co.za/blog/news/2026/capitec-smart-id-launch/",
 idwait="https://www.gov.za/news/media-statements/implement-amendments-birth-and-deaths-registration-act-media-briefing-home",
 ar2324="https://www.dha.gov.za/images/AnnualReports/Annual-Report_2023-2024.pdf",
 gtb="https://www.dha.gov.za/index.php/contact-us/bank-branches/98-gauteng-banks",
 ecb="https://www.dha.gov.za/index.php/contact-us/bank-branches/97-eastern-cape-banks",
 fsb="https://www.dha.gov.za/index.php/contact-us/bank-branches/103-free-state-banks",
 kznb="https://www.dha.gov.za/index.php/contact-us/bank-branches/102-kwazulu-natal-banks",
 limb="https://www.dha.gov.za/index.php/contact-us/bank-branches/100-limpopo-banks",
 mpub="https://www.dha.gov.za/index.php/contact-us/bank-branches/101-mpumalanga-banks",
 nwb="https://www.dha.gov.za/index.php/contact-us/bank-branches/104-north-west-banks",
 ncb="https://www.dha.gov.za/index.php/contact-us/bank-branches/99-northern-cape-banks",
 wcb="https://www.dha.gov.za/index.php/contact-us/bank-branches/96-western-cape-banks",
)
def src(*k): return ' <span class="src">[' + ', '.join(f'<a href="{S[x]}" rel="noopener">source</a>' for x in k) + ']</span>'
PROV=["Eastern Cape","Free State","Gauteng","KwaZulu-Natal","Limpopo","Mpumalanga","North West","Northern Cape","Western Cape"]
slug=lambda s:re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
BANKS=[(1,"Capitec","capitec"),(2,"Standard Bank","standard-bank"),(3,"FNB","fnb"),(4,"Absa","absa"),(None,"Nedbank","nedbank")]
dp={}
for pid,name,sl in BANKS:
    if pid: dp[sl]=json.load(open(os.path.join(HERE,f'p{pid}.json')))['branches']
def normprov(p):
    p=p.strip(); m={'kwazulu natal':'KwaZulu-Natal','kwazulu-natal':'KwaZulu-Natal'}
    return m.get(p.lower(),p)
leg=[]
for o in json.load(open(os.path.join(HERE,'legacy.json'))):
    if o['name'].startswith('There are'): continue
    city=o['city'].split('it. ')[-1].strip()
    name=re.sub(r'\s*-\s*(Gauteng|Western Cape|Western cape|Eastern Cape|Limpopo|Mpumalanga|Kwazulu-Natal|Kwazulu Natal|Northern Cape)( Acting)?\s*$','',o['name']).strip(' -')
    if name=="FNB PORTSIDE": city="Cape Town"
    pv=[p for p in PROV if slug(p) in o['page'].replace('kwazulu-natal','kwazulu-natal')]
    pv=[p for p in PROV if slug(p)+'-banks' in o['page']][0]
    leg.append(dict(name=name.title().replace('Fnb','FNB').replace('Absa Bank','Absa').replace("'S ","'s "),city=city,phone=o['phone'],prov=pv,page=o['page']))
CSS="""*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1d2433;background:#f7f8fa}
header{background:#0b5d3b;color:#fff;padding:14px 16px}header a{color:#fff;text-decoration:none;font-weight:600}nav{margin-top:6px;font-size:14px}nav a{color:#d9f2e6;margin-right:12px;font-weight:400;display:inline-block}
main{max-width:960px;margin:0 auto;padding:16px}h1{font-size:1.6rem;line-height:1.25}h2{font-size:1.25rem;margin-top:1.8em}h3{font-size:1.05rem;margin-top:1.4em}
.card{background:#fff;border:1px solid #e3e6ea;border-radius:10px;padding:14px 16px;margin:12px 0}.note{background:#fff8e1;border-color:#f3d27a}
.src{font-size:12px;color:#5a6472}.src a{color:#5a6472}a{color:#0b5d3b}table{border-collapse:collapse;width:100%;background:#fff;font-size:14px}
th,td{border:1px solid #e3e6ea;padding:6px 8px;text-align:left;vertical-align:top}th{background:#eef2f0}.wrap{overflow-x:auto}
.checked{font-size:13px;color:#5a6472;margin:0 0 8px}.disclaimer{font-size:13.5px;line-height:1.45;background:#eef2f0;border:1px solid #d5ddd8;border-radius:8px;padding:8px 10px;margin:0 0 12px}footer{max-width:960px;margin:24px auto;padding:16px;font-size:13px;color:#5a6472}footer p{margin:0 0 8px}
input{width:100%;padding:8px;font-size:15px;border:1px solid #cdd3da;border-radius:6px;margin:8px 0}ul.grid{columns:2;padding-left:18px}@media(max-width:600px){ul.grid{columns:1}}"""
PATHS=[]
META_WARNINGS=[]
_MONTHS={m:f"{i:02d}" for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}
def iso_date(s):
    d,m,y=s.split()
    return f"{y}-{_MONTHS[m]}-{int(d):02d}"
def check_meta(path,title,desc):
    if not 50<=len(title)<=60:
        META_WARNINGS.append(path)
        print(f"WARNING title length {len(title)} (want 50 to 60) {path}: {title}")
    if not 120<=len(desc)<=160:
        META_WARNINGS.append(path)
        print(f"WARNING description length {len(desc)} (want 120 to 160) {path}: {desc}")
def canonical_for(path):
    if path=='index.html': return BASE+'/'
    if path.endswith('/index.html'): return BASE+'/'+path[:path.rfind('/')+1]
    return BASE+'/'+path
def plain_text(s):
    s=re.sub(r'\s*<span class="src">.*?</span>','',s,flags=re.S)
    s=re.sub(r'<[^>]+>','',s)
    s=H.unescape(s)
    s=re.sub(r'\s+',' ',s)
    s=re.sub(r'\s+([.,;:])',r'\1',s)
    return s.strip()
def json_ld(obj):
    raw=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
    return raw.replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def org_node():
    return {"@type":"Organization","name":SITE_NAME,"url":BASE+"/","logo":{"@type":"ImageObject","url":BASE+"/apple-touch-icon.png"}}
def crumb_trail(path):
    items=[("Home",BASE+"/")]
    if path=='index.html': return items
    if path=='404.html':
        items.append(("Page not found",canonical_for(path)))
        return items
    rel=path[:-len('/index.html')] if path.endswith('/index.html') else path[:-5]
    if rel.startswith('provinces/') and rel!='provinces':
        items.append(("Provinces",BASE+"/provinces/"))
        prov=next(p for p in PROV if slug(p)==rel.split('/')[-1])
        items.append((prov,BASE+"/"+rel+"/"))
        return items
    if rel.startswith('banks/'):
        name=next(n for _,n,s in BANKS if s==rel.split('/')[-1])
        items.append((name,BASE+"/"+rel+"/"))
        return items
    labels={"fees-and-documents":"Fees and documents","booking-and-walk-ins":"Booking and walk-ins","lost-or-stolen-smart-id":"Lost or stolen ID","first-smart-id-at-16":"First ID at 16","collecting-smart-id-or-passport":"Collect your ID","provinces":"Provinces","disclaimer":"Disclaimer"}
    items.append((labels[rel],BASE+"/"+rel+"/"))
    return items
def clean_href(url):
    if re.match(r'^[a-z][a-z0-9+.-]*:',url) or url.startswith('#') or url.startswith('//'): return url
    parts=[p for p in url.split('/') if p not in ('','.','..')]
    if not parts or parts==['index.html']: return '/'
    if parts[-1]=='index.html':
        parts=parts[:-1]
        return '/' if not parts else '/'+'/'.join(parts)+'/'
    if '.' in parts[-1]: return '/'+'/'.join(parts)
    return '/'+'/'.join(parts)+'/'
def clean_links(html):
    return re.sub(r'href="([^"]*)"',lambda m:'href="%s"'%clean_href(m.group(1)),html)
def bank_title(name):
    titled=f"{name} Smart ID and passport branches: walk-in, fees, rules"
    if 50<=len(titled)<=60: return titled
    return f"{name} Smart ID branches: walk-in, fees, rules"
def bank_desc(name):
    return f"{name} Smart ID and passport branch service: walk-in or booking, client requirement, fees and branch list. Sourced from DHA."
def province_title(name):
    # Same pattern as "Smart ID at banks in Gauteng: Capitec, FNB, Absa branches".
    # Longer province names drop "at" so the title stays within 50 to 60 characters.
    exact=f"Smart ID at banks in {name}: Capitec, FNB, Absa branches"
    if 50<=len(exact)<=60: return exact
    return f"Smart ID banks in {name}: Capitec, FNB, Absa branches"
def province_desc(name):
    return f"Bank branches in {name} for a Smart ID, from the DHA Digital Partnership locator and the older eHomeAffairs lists. Confirm the branch before you go."
def page(path,title,body,desc,checked=None,faq=None,article=True,sitemap=True,robots=None):
    when=checked or D
    check_meta(path,title,desc)
    if sitemap: PATHS.append((path,iso_date(when)))
    canonical=canonical_for(path)
    navl='<a href="/">Home</a><a href="/fees-and-documents/">Fees and documents</a><a href="/booking-and-walk-ins/">Booking and walk-ins</a><a href="/lost-or-stolen-smart-id/">Lost or stolen ID</a><a href="/first-smart-id-at-16/">First ID at 16</a><a href="/collecting-smart-id-or-passport/">Collect your ID</a>'+''.join(f'<a href="/banks/{s}/">{n}</a>' for _,n,s in BANKS)+'<a href="/provinces/">Provinces</a>'
    graph=[]
    if path=='index.html':
        graph.append({"@type":"WebSite","name":SITE_NAME,"url":BASE+"/","description":desc,"inLanguage":"en-ZA"})
        graph.append(org_node())
    if article:
        graph.append({"@type":"Article","headline":title,"description":desc,"datePublished":iso_date(when),"dateModified":iso_date(when),"inLanguage":"en-ZA","mainEntityOfPage":canonical,"image":BASE+"/og.png","author":org_node(),"publisher":org_node()})
    crumbs=crumb_trail(path)
    graph.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i,"name":name,"item":url} for i,(name,url) in enumerate(crumbs,1)]})
    if faq:
        graph.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":plain_text(a)}} for q,a in faq]})
    head=['<!doctype html><html lang="en-ZA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
        f'<title>{H.escape(title)}</title>',
        f'<meta name="description" content="{H.escape(desc)}">',
        f'<link rel="canonical" href="{canonical}">']
    if robots: head.append(f'<meta name="robots" content="{H.escape(robots)}">')
    if GOOGLE_SITE_VERIFICATION: head.append(f'<meta name="google-site-verification" content="{H.escape(GOOGLE_SITE_VERIFICATION)}">')
    if MSVALIDATE_01: head.append(f'<meta name="msvalidate.01" content="{H.escape(MSVALIDATE_01)}">')
    og_type="website" if path in ("index.html","404.html") else "article"
    head+=[
        f'<meta property="og:title" content="{H.escape(title)}">',
        f'<meta property="og:description" content="{H.escape(desc)}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:url" content="{canonical}">',
        f'<meta property="og:site_name" content="{H.escape(SITE_NAME)}">',
        '<meta property="og:locale" content="en_ZA">',
        f'<meta property="og:image" content="{BASE}/og.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="Smart ID at the Bank, South Africa">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{H.escape(title)}">',
        f'<meta name="twitter:description" content="{H.escape(desc)}">',
        f'<meta name="twitter:image" content="{BASE}/og.png">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        f'<script type="application/ld+json">{json_ld({"@context":"https://schema.org","@graph":graph})}</script>',
        f'<style>{CSS}</style><script defer src="/_vercel/insights/script.js"></script></head><body>']
    h=''.join(head)+f'''
<header><a href="/">{SITE_NAME}</a><nav>{navl}</nav></header><main><p class="disclaimer">{H.escape(DISCLAIMER_SHORT)} <a href="/disclaimer/">Disclaimer</a>.</p><p class="checked">Last checked: {when}</p>{body}</main>
<footer><p>{H.escape(DISCLAIMER)}</p><p><a href="/disclaimer/">Disclaimer</a></p><p>Related guides: <a href="{RELATED_GUIDE}">Passport and ID guide for South Africans in the USA</a>.</p><p>Independent, unofficial guide. Not affiliated with the Department of Home Affairs (DHA) or any bank. Facts are taken only from official DHA, gov.za and bank pages, linked next to each fact. Rules change often: always confirm on the official source before you travel. DHA contact centre: 0800 60 11 90 {src('fnb')}. Last checked: {when}.</p></footer></body></html>'''
    h=clean_links(h)
    assert '\u2014' not in h and '\u2013' not in h, path
    os.makedirs(os.path.dirname(f'{OUT}/{path}') or OUT,exist_ok=True); open(f'{OUT}/{path}','w').write(h)
def dptable(rows,showprov=False,showbank=False):
    t='<div class="wrap"><table><tr>'+('<th>Bank</th>' if showbank else '')+'<th>Branch</th><th>Address line</th><th>City</th>'+('<th>Province</th>' if showprov else '')+'<th>Postal code</th></tr>'
    for b in sorted(rows,key=lambda x:(x.get('_bank',''),x['city'],x['branchName'])):
        t+='<tr>'+(f"<td>{b['_bank']}</td>" if showbank else '')+f"<td>{H.escape(b['branchName'])}</td><td>{H.escape(b['suburb'])}</td><td>{H.escape(b['city'])}</td>"+(f"<td>{b['province']}</td>" if showprov else '')+f"<td>{b['postal_code']}</td></tr>"
    return t+'</table></div>'
FILTER='''<input id="q" placeholder="Filter by town, mall or branch name" oninput="var v=this.value.toLowerCase();document.querySelectorAll('table tr').forEach(function(r,i){if(r.querySelector('td'))r.style.display=r.textContent.toLowerCase().indexOf(v)>-1?'':'none'})">'''
for pid,n,s in BANKS:
    if s in dp:
        for b in dp[s]: b['_bank']=n; b['province']=normprov(b['province'])
counts={s:len(v) for s,v in dp.items()}
total=sum(counts.values())
# HOME
faq=[("Can I get a passport at a bank branch?",f"Under the DHA Digital Partnership (walk-in model), passports are listed as not yet available in phase 1{src('digital')}. Some banks still run the older eHomeAffairs model, where you apply and pay online, book, then visit a branch with DHA staff. Standard Bank and FNB describe passports through that route{src('sb','fnb')}."),
("Do I need an appointment?",f"Depends on the route. DHA says Capitec and Standard Bank allow walk-ins without an appointment at Digital Partnership branches{src('digital')}. FNB says no appointment is needed to replace a Smart ID{src('fnb')}. Absa offers booking online, in its app, or walking in{src('absa')}. DHA's Gauteng bank-branch page says no walk-ins are allowed at banks{src('gtb')}. Steps, and how BABS differs from a bank visit: <a href=\"booking-and-walk-ins/index.html\">Booking and walk-ins</a>."),
("Do I need to bank there?",f"Per the current bank pages: Capitec (pay with a Capitec account, can open one in branch){src('cap')}, Standard Bank (yes){src('sb')}, FNB (active, funded transactional account for Smart ID replacement){src('fnb')}, Absa (Cheque or Savings account){src('absa')}. Nedbank: payment is described through Nedbank Money app or Online Banking; other options not stated by source{src('ned')}."),
("What does it cost?",f"DHA fee for a Smart ID re-issue is R140{src('fees')}. DHA says banks may charge a convenience fee{src('digital')}. Capitec states R150 total (R140 DHA plus R10 service fee){src('cap')}. FNB states it charges no additional fees{src('fnb')}. Standard Bank said it will not charge during the launch phase{src('sbnews')}. Absa and Nedbank extra fee: not stated by source."),
("Can I apply for my first ID (turning 16) at a bank?",f"Not at Digital Partnership branches: DHA says first-time ID applications must be done at a Home Affairs office{src('digital')}. Standard Bank lists first-time ID issuing through its online eHomeAffairs route{src('sb')}. Documents, a parent, and the fee: <a href=\"first-smart-id-at-16/index.html\">First Smart ID at 16</a>."),
("Can children apply at bank branches?",f"DHA Digital Partnership FAQ: no, children must apply at a Home Affairs office{src('digital')}. FNB (eHomeAffairs route): both parents must accompany a child for a passport, one parent for a Smart ID{src('fnb')}. The first-ID rules: <a href=\"first-smart-id-at-16/index.html\">First Smart ID at 16</a>."),
("What do I bring?",f"DHA Digital Partnership FAQ: you do not need to bring any documents{src('digital')}. For eHomeAffairs bookings, FNB says bring original identity documents{src('fnb')}; Nedbank says bring your booking confirmation and ID book or card{src('ned')}. See <a href=\"fees-and-documents/index.html\">Fees and documents</a>. A lost, stolen or damaged card, and where an affidavit or a police report is stated: <a href=\"lost-or-stolen-smart-id/index.html\">Replacing a lost or stolen Smart ID</a>."),
("How do I collect it once it is ready?",f"At a Home Affairs office, the identity documents page says a Smart ID is collected at the modernised office you chose, and that DHA uses the cellphone number from the application for progress and collection updates{src('iddocs')}. The Digital Partnership page says you collect at the bank branch where you applied, and the partner bank communicates the details{src('digital')}. The partner-branch page also says the document can be delivered where the bank offers that{src('locator')}. Who may collect, what to bring, and any deadline: <a href=\"collecting-smart-id-or-passport/index.html\">Collecting a Smart ID or passport</a>.")]
banktbl='<div class="wrap"><table><tr><th>Bank</th><th>Digital Partnership branches (DHA locator)</th><th>Walk-in or booking</th><th>Must be a client?</th><th>Extra bank fee</th></tr>'
rowsb=[("Capitec","capitec",f"Walk-in{src('digital')}",f"Yes, pay from a Capitec account (can open one in branch){src('cap')}",f"R10 (R150 total){src('cap')}"),
("Standard Bank","standard-bank",f"Walk-in in branch; booking for eHomeAffairs route{src('sb')}",f"Yes{src('sb')}",f"None during launch phase{src('sbnews')}"),
("FNB","fnb",f"Smart ID replacement: no appointment. eHomeAffairs route: booking{src('fnb')}",f"Yes, active funded transactional account (Smart ID replacement){src('fnb')}",f"None{src('fnb')}"),
("Absa","absa",f"Book online, in app, or walk in{src('absa')}",f"Yes, Cheque or Savings account{src('absa')}","Not stated by source"),
("Nedbank","nedbank",f"Booking via eHomeAffairs{src('ned')}; DHA's Gauteng bank-branch page says no walk-ins at banks{src('gtb')}",f"Payment described via Nedbank app or Online Banking{src('ned')}; other options not stated by source","Not stated by source")]
for n,s,w,c,f in rowsb:
    cnt=f"{counts[s]}{src('locator')}" if s in counts else f"Not listed in DHA locator{src('locator')}"
    banktbl+=f'<tr><td><a href="banks/{s}/index.html">{n}</a></td><td>{cnt}</td><td>{w}</td><td>{c}</td><td>{f}</td></tr>'
banktbl+='</table></div>'
body=f'''<h1>Smart ID and passport services at South African bank branches</h1>
<p>A plain, sourced guide to which bank branches can take your Smart ID (and in some cases passport) application, what to bring, and what it costs.</p>
<div class="card"><strong>Two different systems exist.</strong><ol>
<li><strong>DHA Digital Partnership</strong> (since 9 March 2026{src('golive')}): bank staff process the application through a secure link to DHA. Currently for green ID book to Smart ID conversion and Smart ID re-issues only{src('digital')}. DHA's live locator lists the branches{src('locator','locms')}.</li>
<li><strong>Older eHomeAffairs bank branches</strong>: apply and pay online at eHomeAffairs, book a slot, then visit a branch hosting DHA for fingerprints and photo. DHA's Gauteng bank-branch page says no walk-ins are allowed at banks{src('gtb')}.</li></ol>
<p><a href="booking-and-walk-ins/index.html">How to book, and where a walk-in is accepted</a>. <a href="collecting-smart-id-or-passport/index.html">When the document is ready, and who may collect it</a>.</p></div>
<h2>Banks at a glance</h2>{banktbl}
<p>Total Digital Partnership branches in the DHA locator on {D}: <strong>{total}</strong>{src('locator')}. The locator is updated by DHA as branches join{src('locms')}.</p>
<h2>Branches by province</h2><ul class="grid">'''+''.join(f'<li><a href="provinces/{slug(p)}/index.html">{p}</a> ({sum(1 for s in dp for b in dp[s] if b["province"]==p)} Digital Partnership, {sum(1 for l in leg if l["prov"]==p)} eHomeAffairs)</li>' for p in PROV)+f'''</ul>
<h2>What is available at bank branches</h2><div class="card"><p>Available under the Digital Partnership: Smart ID re-issues (lost, stolen, damaged) and green ID book to Smart ID replacements{src('digital')}. What DHA and each bank say about that re-issue: <a href="lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>.</p>
<p>Not yet available there: passport applications (phase 1), first-time IDs (for example turning 16), late birth registration, name changes, amendments to personal details, complex civic services{src('digital')}. DHA has said passports and first-time Smart IDs will be added later{src('absams')}. What a first ID at 16 requires at a Home Affairs office: <a href="first-smart-id-at-16/index.html">First Smart ID at 16</a>.</p></div>
<h2>Short FAQ</h2>'''+''.join(f'<div class="card"><strong>{q}</strong><p>{a}</p></div>' for q,a in faq)
page('index.html',"Smart ID and passport at SA bank branches: sourced guide",body,"Which South African bank branches offer Smart ID and passport services, walk-in or booking, fees, documents. Sourced from DHA and bank pages.",faq=faq)
# FEES
fb=f'''<h1>Fees, documents and age rules</h1>
<h2>DHA fees (tariffs)</h2><div class="wrap"><table><tr><th>Service</th><th>DHA fee</th><th>Source</th></tr>
<tr><td>Identity document: first issue</td><td>Free</td><td>{src('fees')}</td></tr>
<tr><td>Identity document: re-issue (includes Smart ID replacement)</td><td>R140.00</td><td>{src('fees')}</td></tr>
<tr><td>Temporary Identity Certificate</td><td>R70.00</td><td>{src('fees')}</td></tr>
<tr><td>Adult passport (32 pages)</td><td>R600.00</td><td>{src('fees')}</td></tr>
<tr><td>Child passport</td><td>R600.00</td><td>{src('fees')}</td></tr>
<tr><td>Maxi tourist passport (48 pages)</td><td>R1200.00</td><td>{src('fees')}</td></tr>
<tr><td>Tourist passport when previous one is still valid for 6 months or longer</td><td>R1 200</td><td>{src('travel')}</td></tr>
<tr><td>Maxi passport when previous one is still valid for 6 months or longer</td><td>R2 400</td><td>{src('travel')}</td></tr>
<tr><td>Minor passport when previous one is still valid for 6 months or longer</td><td>R1 200</td><td>{src('travel')}</td></tr></table></div>
<p>DHA's fee page is marked "updated August 2026"{src('fees')}. Bank convenience fees are separate; see each bank page. DHA: "Banks may charge a convenience fee"{src('digital')}.</p>
<div class="card note">The DHA Smart ID requirements brochure says first-time Smart ID issue is free for youth 16 and older and for pensioners 60 and older, and R140 for other citizens converting from a green ID book{src('sidpdf')}. Several bank pages charge R140 for green ID book conversions{src('cap','fnb')}. FNB states senior citizens (60+) do not pay for their first Smart ID{src('fnb')}.</div>
<h2>Documents to bring</h2>
<div class="card"><strong>Digital Partnership bank branches (walk-in model)</strong><p>"You do not need to bring any documents."{src('digital')} Capitec: no documents needed, but bring your green ID book if opening an account during the visit{src('cap')}. FNB Smart ID replacement: no documentation needed{src('fnb')}.</p></div>
<div class="card"><strong>eHomeAffairs bank branches (booking model)</strong><p>FNB: bring original identity documents such as green ID book, passport or birth certificate, also when collecting{src('fnb')}. Nedbank: bring your booking confirmation and ID book or card{src('ned')}. Standard Bank: print and keep your booking confirmation letter and reference number, visit with your ID{src('sb')}.</p>
<p>How to make the booking, and where walk-ins are accepted: <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>. When the document is ready, what to bring to collect it, and who may collect: <a href="../collecting-smart-id-or-passport/index.html">Collecting a Smart ID or passport</a>.</p></div>
<div class="card"><strong>At a Home Affairs office (DHA Smart ID brochure)</strong><ul>
<li>First issue, youth 16 and older: birth certificate; certified copy of a parent, legal guardian or informant ID; death certificate if parents deceased; proof of residence where available{src('sidpdf')}.</li>
<li>First Smart ID, pensioners 60 and older and other citizens: green barcoded ID (or affidavit if lost); proof of residence where available; marriage certificate if married; divorce decree if divorced{src('sidpdf')}.</li></ul>
<p>That brochure list is for a first Smart ID. DHA's identity documents page uses a different first-time list, and it says a parent must attend. The comparison, the fee, and which banks take a first ID: <a href="../first-smart-id-at-16/index.html">First Smart ID at 16</a>. Replacing a card that is already lost, stolen or damaged, and where an affidavit or a police report is stated: <a href="../lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>.</p></div>
<h2>Age rules</h2><div class="card"><ul>
<li>Ordinary tourist and maxi passports: citizens 16 or older, valid 10 years; 13 working days turnaround{src('travel')}.</li>
<li>Minor tourist passport: 15 or younger, valid 5 years; 18 working days turnaround{src('travel')}.</li>
<li>A person 16 or older must first apply for an identity document before applying for a passport{src('travel')}.</li>
<li>For children's passports, both parents and the children must be present (exceptions apply){src('travel')}.</li>
<li>Digital Partnership bank branches: children cannot apply; first-time IDs must go to a Home Affairs office{src('digital')}. The document and parent comparison is on <a href="../first-smart-id-at-16/index.html">First Smart ID at 16</a>.</li>
<li>Standard Bank online route: South African citizens 16 and older{src('sb')}.</li></ul></div>'''
page('fees-and-documents/index.html',"Smart ID and passport fees, documents and age rules (DHA)",fb,"DHA fees for Smart ID and passports, documents to bring at a bank or a Home Affairs office, and age rules, each linked to an official source.")
# BANK PAGES
info={
"capitec":(f'''<ul><li>Model: DHA Digital Partnership{src('locator')}. Walk-ins without appointment{src('digital')}.</li>
<li>Services: Smart ID replacements only (lost, stolen, damaged, or green ID book to Smart ID). First-time IDs not available in branch{src('cap')}.</li>
<li>Account: you pay using a Capitec account; if you have none, the branch can help you open one, and it must be active with a positive balance{src('cap')}.</li>
<li>Documents: none needed; bring green ID book if opening an account{src('cap')}.</li>
<li>Cost: R150 total (R140 DHA fee plus R10 service fee){src('cap')}.</li>
<li>Passports: not stated by source as currently available at Capitec branches. A 2025 gov.za statement announced Smart ID and passports at Capitec, open to non-clients{src('capms')}; Capitec's current page requires a Capitec account{src('cap')}.</li>
<li>Capitec branch locator has a Smart ID filter{src('caploc')}.</li></ul>'''),
"standard-bank":(f'''<ul><li>In branch (Digital Partnership): green ID to Smart ID, Smart ID re-issue (lost, stolen, damaged), and Smart ID replacement after a surname change already done at Home Affairs. Walk-ins accepted{src('sb')}.</li>
<li>Online (eHomeAffairs) route: first-time ID, Smart ID replacement and re-issue, first-time passport and passport renewal. Needs a Standard Bank Online Banking profile and country of birth South Africa; pay DHA via Online Banking, then book at a specialised branch{src('sb')}.</li>
<li>Account: yes, you need a Standard Bank account{src('sb')}.</li>
<li>Cost: Standard Bank will not charge customers during the launch phase{src('sbnews')}. DHA fee R140{src('fees')}.</li>
<li>Surname changes: cannot assist; visit Home Affairs{src('sb')}.</li>
<li>Note: a 2025 gov.za statement said services would be open to non-clients{src('fnbsbms')}; Standard Bank's current page requires an account{src('sb')}.</li></ul>'''),
"fnb":(f'''<ul><li>Replace a Smart ID (lost, stolen, damaged) at selected branches, no appointment needed{src('fnb')}.</li>
<li>Apply or renew Smart ID or passport via eHomeAffairs: register and pay (FNB App or online banking, "Government Bills + Smart IDs"), book a slot, visit one of seven FNB branches with DHA representation{src('fnb')}.</li>
<li>FNB eHomeAffairs branches: Lynnwood (Grove Mall), Centurion Lifestyle, 4 Merchant Place, Green Point, Burgersfort, Cornubia, The Glen{src('fnb')}.</li>
<li>Eligibility for Smart ID replacement: FNB customers with an active, funded transactional account; South African citizen (birth or naturalisation) or permanent resident{src('fnb')}.</li>
<li>Payment: no cash; payments cannot be made in branch by cash, debit or credit card{src('fnb')}.</li>
<li>Documents: none needed for Smart ID replacement; bring original identity documents for eHomeAffairs appointments and collection{src('fnb')}.</li>
<li>Cost: Smart ID R140; FNB charges no additional fees{src('fnb')}.</li>
<li>Minors (eHomeAffairs route): passport, both parents; Smart ID, one parent{src('fnb')}.</li></ul>'''),
"absa":(f'''<ul><li>Smart ID renewal at selected branches: book online, in the Absa Banking App (Menu, Government Services), or walk in{src('absa')}.</li>
<li>Account: you must have an Absa Cheque or Savings account{src('absa')}.</li>
<li>Payment: you pay at the branch, not online{src('absa')}.</li>
<li>If booked, bring the SMS or email confirmation{src('absa')}.</li>
<li>Extra Absa fee: not stated by source. DHA fee R140{src('fees')}.</li>
<li>Absa also runs a bank-based Home Affairs mobile unit{src('absams')}.</li>
<li>Passports: not stated by source as currently available at Absa digital branches.</li></ul>'''),
"nedbank":(f'''<ul><li>Not listed in the DHA Digital Partnership locator on {D}{src('locator')}.</li>
<li>Nedbank hosts DHA officials at participating branches (eHomeAffairs model): apply online, upload documents, pay online with Nedbank, book a date, then visit for biometrics{src('ned')}.</li>
<li>Bring your booking confirmation and ID book or card{src('ned')}. DHA: no walk-ins at eHomeAffairs bank branches{src('legacy')}.</li>
<li>Collection: SMS when ready, collect at the branch you selected{src('ned')}.</li>
<li>Children under 18: different requirements; Nedbank refers you to DHA{src('ned')}.</li>
<li>Must you be a Nedbank client? Payment is described via Nedbank Money app or Online Banking; whether other payers are accepted is not stated by source.</li>
<li>Passports: Nedbank says DHA officials issue IDs and passports at these branches{src('ned')}.</li>
<li>Extra Nedbank fee: not stated by source.</li></ul>
<h2>Nedbank branches (per Nedbank)</h2><div class="wrap"><table><tr><th>Branch</th><th>City</th><th>Address</th></tr>
<tr><td>Nedbank Arcadia Pretoria</td><td>Pretoria</td><td>Shop 25, Nedbank Plaza, Beatrix Street</td></tr>
<tr><td>Nedbank Sandown</td><td>Sandown</td><td>Shop L05, Lower Ground, Block, 135 Rivonia Road</td></tr>
<tr><td>Nedbank St Georges Mall</td><td>Cape Town</td><td>Shop 3 The Box, St Georges Mall c/o Riebeeck Street</td></tr>
<tr><td>Nedbank Nelspruit</td><td>Nelspruit</td><td>Shop 1, Nedbank Centre, 30 Brown Street</td></tr>
<tr><td>Nedbank Durban North</td><td>Durban</td><td>57 Adelaide Tambo Drive</td></tr>
<tr><td>Nedbank Lakeview Office Park</td><td>Roodepoort</td><td>16 Constantia Blvd, Constantia Kloof</td></tr></table></div>'''),
}
for pid,n,s in BANKS:
    b=f'<h1>{n}: Smart ID and passport at branches</h1><div class="card">{info[s]}</div><p>Booking steps for this bank, and how they differ from a Home Affairs office appointment (BABS): <a href="../../booking-and-walk-ins/index.html">Booking and walk-ins</a>. Replacing a lost or stolen card, and where a source mentions an affidavit or the police: <a href="../../lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>. A first Smart ID at 16, and whether this bank states that it takes one: <a href="../../first-smart-id-at-16/index.html">First Smart ID at 16</a>. When the document is ready, what this bank says about collection: <a href="../../collecting-smart-id-or-passport/index.html">Collecting a Smart ID or passport</a>.</p>'
    if s in dp:
        b+=f'<h2>{n} Digital Partnership branches ({len(dp[s])}){src("locator")}</h2><p>Data from the DHA partner branch locator on {D}. Confirm before visiting.</p>{FILTER}{dptable(dp[s],showprov=True)}'
    lg=[l for l in leg if l['name'].upper().startswith(n.upper().split()[0])]
    if lg:
        b+=f'<h2>{n} eHomeAffairs bank branches listed by DHA{src("legacy")}</h2><p>Booking required; DHA states no walk-ins.</p><div class="wrap"><table><tr><th>Branch</th><th>City</th><th>Province</th><th>Phone (as listed)</th></tr>'+''.join(f'<tr><td>{H.escape(l["name"])}</td><td>{H.escape(l["city"])}</td><td>{l["prov"]}</td><td>{l["phone"]}</td></tr>' for l in lg)+'</table></div>'
    page(f'banks/{s}/index.html',bank_title(n),b,bank_desc(n))
# PROVINCES
pi='<h1>Branches by province</h1><ul>'+''.join(f'<li><a href="{slug(p)}/index.html">{p}</a></li>' for p in PROV)+'</ul>'
page('provinces/index.html',"Smart ID at banks by province: Capitec, FNB, Absa branches",pi,"Smart ID bank branches in every South African province, from the DHA Digital Partnership locator and the older eHomeAffairs lists. Confirm before you travel.")
PROVBANK={'Eastern Cape':'ecb','Free State':'fsb','Gauteng':'gtb','KwaZulu-Natal':'kznb','Limpopo':'limb','Mpumalanga':'mpub','North West':'nwb','Northern Cape':'ncb','Western Cape':'wcb'}
for p in PROV:
    rows=[b for s in dp for b in dp[s] if b['province']==p]
    b=f'<h1>Smart ID bank branches in {p}</h1><p>{len(rows)} Digital Partnership branches listed in the DHA locator on {D}{src("locator")}. These handle Smart ID re-issues and green ID book conversions{src("digital")}. Check each <a href="../../index.html">bank\'s rules</a> (most require you to be a client).</p>{FILTER}{dptable(rows,showbank=True)}'
    lg=[l for l in leg if l['prov']==p]
    b+=f'<h2>eHomeAffairs bank branches in {p}{src("legacy")}</h2>'
    if lg: b+=f'<p>Apply and book online first. DHA\'s {p} bank-branch page says no walk-ins are allowed at banks{src(PROVBANK[p])}. See <a href="../../booking-and-walk-ins/index.html">Booking and walk-ins</a>.</p><div class="wrap"><table><tr><th>Branch</th><th>City</th><th>Phone (as listed)</th></tr>'+''.join(f'<tr><td>{H.escape(l["name"])}</td><td>{H.escape(l["city"])}</td><td>{l["phone"]}</td></tr>' for l in lg)+'</table></div>'
    else: b+='<p>DHA lists none for this province.</p>'
    page(f'provinces/{slug(p)}/index.html',province_title(p),b,province_desc(p))
PROVLINKS=' '.join(f'<a href="{S[k]}" rel="noopener">{label}</a>' for k,label in [('ecb','Eastern Cape'),('fsb','Free State'),('gtb','Gauteng'),('kznb','KwaZulu-Natal'),('limb','Limpopo'),('mpub','Mpumalanga'),('nwb','North West'),('ncb','Northern Cape'),('wcb','Western Cape')])
bb=f'''<h1>Booking a Smart ID: BABS, bank branches and walk-ins</h1>
<p>A common question is whether a Smart ID at a bank is booked on DHA's Branch Appointment Booking System (BABS), and whether a walk-in is accepted. Official pages describe three different ways to apply. This page says which way books a Home Affairs office, which way books a bank, and what each official page says about walk-ins. Fees, documents and age rules are on <a href="../fees-and-documents/index.html">Fees and documents</a>. Branch lists are on the <a href="../banks/capitec/index.html">bank</a> and <a href="../provinces/index.html">province</a> pages.</p>
<div class="card note"><strong>BABS does not book a bank branch.</strong>
<p>DHA's BABS notice answers the difference in its own words: eHomeAffairs "allows the client to make a booking, upload documents and make payment then be processed at the Banks", while BABS "provides a client with an opportunity to book a time slot to get in the office." Both let you book a time slot for an application{src('babs')}.</p>
<p>The older address <a href="{S['babsmove']}" rel="noopener">services.dha.gov.za</a> says the Branch Appointment Booking System has moved, and that it is now on MyHomeAffairsOnline. The button on that page goes to <a href="{S['mhao']}" rel="noopener">myhomeaffairsonline.dha.gov.za</a>{src('babsmove')}.</p></div>
<h2>Which route to use</h2>
<div class="wrap"><table><tr><th>Where you will go</th><th>What DHA or the bank says to use</th><th>Walk-in</th></tr>
<tr><td>A Home Affairs office, for a Smart ID or passport</td><td>BABS, now opened from My Home Affairs Online. The portal offers "Book a DHA Branch Appointment" for visiting Department of Home Affairs branches{src('mhao','babsmove')}.</td><td>The BABS notice says people without a booking are served as walk-ins, and booked clients are prioritised{src('babs')}. See the walk-in section below for the other official wordings, and the dates they apply to.</td></tr>
<tr><td>A Digital Partnership bank branch, for a green ID book conversion or a Smart ID re-issue</td><td>The bank's own channel. DHA says you do not log on to eHomeAffairs to make bookings or payments{src('digital','locator')}.</td><td>DHA says Capitec and Standard Bank allow walk-ins without an appointment{src('digital')}. FNB and Absa state their own rules below. BABS is not named on the Digital Partnership page{src('digital')}.</td></tr>
<tr><td>An older Home Affairs-enabled bank office (eHomeAffairs)</td><td>Register, apply, upload, pay, then book on eHomeAffairs. The official how-to says a booking is a prerequisite at a Home Affairs enabled bank office{src('ehowto')}.</td><td>DHA's Gauteng bank-branch page says no walk-ins are allowed at banks, and that you can visit only after an online application and a booked visit. The same sentence on the other eight province pages is quoted below, with each page linked{src('gtb')}.</td></tr>
</table></div>
<h2>Book a Home Affairs office visit (BABS)</h2>
<div class="card"><p>The notice defines BABS as a system that lets clients make an electronic booking for selected services at the Department of Home Affairs{src('babs')}. The 2023/24 annual report says BABS is accessed through the Home Affairs website and gives citizens the option to book a date and time for a Home Affairs visit, with emphasis on Smart ID card and passport applications, and that the system is linked to the National Population Register for additional security{src('ar2324')}.</p>
<p>On My Home Affairs Online, booking a branch appointment requires you to be logged in{src('mhaofaq')}. Creating a profile asks for an email address, and the registration page says that email address cannot be updated, so it must be correct before you submit{src('mhaoreg')}. Forgotten-password reset is offered from the login page by email{src('mhaofaq')}. The click-by-click screens after login (which offices and times the form offers on a given day): not stated by source.</p></div>
<h3>What the BABS notice says the steps are</h3>
<div class="card"><ul>
<li>The notice says there are three main steps. The first is entering your South African ID number. After that, the notice asks for full name and surname, cellphone number, and email address (optional){src('babs')}.</li>
<li>The third step: not stated by source. The published text ends after those personal details.</li>
<li>To start, the notice says visit www.dha.gov.za and click on BABS{src('babs')}. That is the older instruction. The current services.dha.gov.za page says BABS has moved to MyHomeAffairsOnline{src('babsmove')}.</li>
<li>Booked clients are serviced at dedicated counters and are prioritised over people without a booking{src('babs')}.</li>
<li>The system sends an SMS or email reminder 3 days before the appointment{src('babs')}.</li>
<li>An appointment can be cancelled after you receive booking confirmation. The notice says the system lets clients cancel or reschedule, and that slots are shown so a client can select a new date{src('babs')}. My Home Affairs Online says you may cancel an appointment if you are logged in{src('mhaofaq')}.</li>
<li>Appointments are not transferable. You cannot give your slot to a friend or relative{src('babs')}.</li>
<li>ID numbers are used to verify clients when they book, which DHA says is to stop agents blocking slots and selling them. DHA asks clients to report agents trying to sell places in the queue{src('babs')}.</li>
<li>If the office is offline on the day, the notice says you can select another date and time. Booked clients who were not served are prioritised when the system was down{src('babs')}.</li>
<li>The notice says the booking system is currently only available in English. Whether the My Home Affairs Online screens are still English only: not stated by source.</li>
</ul></div>
<h3>Who can book, and for which services</h3>
<div class="card"><p>The BABS notice says the system only allows clients with valid RSA ID numbers to make bookings, and that services on the booking system are for smart ID cards and passports{src('babs')}. It says a death certificate or a full birth certificate does not need a booking, because those services are not on the booking system{src('babs')}.</p>
<p>The My Home Affairs Online FAQ, on the portal that services.dha.gov.za now points to, says a person who is not a South African citizen may book a branch appointment and must provide a passport number{src('mhaofaq','babsmove')}. The notice and the FAQ do not say the same thing about who can book. Neither page explains the difference. Use the live portal for the rule it enforces on the day you book.</p>
<p>The notice says that in the near future, selected Home Affairs offices will process smart ID and passport applications only for clients who have booked. Whether that appointment-only rule is already in force: not stated by source. The date of the notice: not stated by source{src('babs')}.</p></div>
<h3>Walk-ins at Home Affairs offices</h3>
<div class="card"><ul>
<li>BABS notice: people without bookings are served as walk-ins. A booking is advisable so that you are guaranteed the service in your time slot, provided the system is up{src('babs')}.</li>
<li>People without internet access may still walk in. They can also be helped to book if they agree to come on a different day{src('babs')}.</li>
<li>2023/24 annual report: "Walk-ins are not replaced by BABS." The report says all offices continue to accommodate walk-ins so that no citizen is turned away. It also says BABS had been rolled out to 198 modernised offices, with over 1.5 million booking appointments honoured during 2023/24. The office count on {D}: not stated by source{src('ar2324')}.</li>
<li>For 8 to 19 December 2025 and 5 to 16 January 2026, DHA said clients should book application or collection appointments on BABS before visiting, and that those without a booking may still visit offices as walk-ins. On those days, offices equipped for Smart ID cards and passports closed at 18:00 instead of 16:00. Whether those hours, or that collection-booking advice, apply on other dates: not stated by source{src('festive')}.</li>
<li>The eHomeAffairs how-to says you do not need a booking to give biometrics at a Home Affairs office{src('ehowto')}. The BABS notice says a person without a booking is still served, and that a booked client is prioritised{src('babs')}.</li>
</ul>
<p>The BABS notice publishes a list of offices by province. When that list was last updated: not stated by source. This page does not copy it out as a current directory. Open the notice for the names it prints{src('babs')}.</p>
<p>For help, the notice gives the Home Affairs Contact Centre, 0800 60 11 90{src('babs')}.</p></div>
<h2>At a bank: do not start with BABS</h2>
<p>DHA's Digital Partnership page and the partner-branch page both say that, unlike the traditional process, customers do not need to log on to eHomeAffairs to make bookings or payments. You apply through the bank's app, website or branch, then visit a participating branch for identity verification, fingerprints and a photograph. The application goes to Home Affairs for verification, processing and production{src('digital','locator')}. Those two pages do not use the same sentence for collection or delivery. The comparison is on <a href="../collecting-smart-id-or-passport/index.html">Collecting a Smart ID or passport</a>.</p>
<p>DHA says this bank service is currently available for green ID book holders converting to a Smart ID card, re-issues for existing Smart ID card holders, and permanent residents and naturalised citizens from visa-exempt countries (initial phase). The same page, under who can apply, says the first phase focuses on South African citizens converting from the green ID book, re-issues for existing Smart ID card holders, and naturalised citizens and qualifying permanent residents with green ID books{src('digital')}. What those re-issues require when the card is lost or stolen: <a href="../lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>.</p>
<p>Not yet available at these bank branches, on that page: passport applications during phase 1, first-time IDs (for example turning 16), late registration of birth, name changes, amendments to personal details, and complex civic services. Clients who need those must visit a Home Affairs office. DHA also says children cannot apply at these bank branches{src('digital')}. Documents and who must attend for a first ID at 16: <a href="../first-smart-id-at-16/index.html">First Smart ID at 16</a>.</p>
<h3>Capitec</h3>
<div class="card"><p>DHA says Capitec allows customer walk-ins without an appointment at participating branches, and that no existing documents are needed{src('digital')}. Capitec's own article (dated 11/03/2026 on the page) describes an in-person replacement visit: photo, fingerprints and signature captured in branch. An appointment rule on Capitec's article: not stated by source{src('cap')}.</p>
<p>Capitec says you pay from a Capitec account. If you do not have one, the branch can help you open one, and it must be active with a positive balance before the Smart ID application continues. Bring the green ID book only if you are opening an account during the visit. Total cost on that page: R150 (R140 DHA fee plus R10 service fee). First-time IDs are not available in branch{src('cap')}.</p>
<p>Capitec does not describe a BABS booking or an eHomeAffairs booking for this visit. Branch list: <a href="../banks/capitec/index.html">Capitec</a>.</p></div>
<h3>Standard Bank</h3>
<div class="card"><p><strong>In branch.</strong> Standard Bank says it takes walk-in applications. Services it names: green ID to Smart ID, Smart ID re-issue (lost, stolen or damaged), and Smart ID replacement after a surname change that Home Affairs has already done. Fingerprints and photo are taken in branch. You pay at the branch. You collect from that branch{src('sb')}.</p>
<p><strong>Online.</strong> Standard Bank's steps{src('sb')}:</p>
<ol>
<li>You need a Standard Bank Online Banking profile, and your country of birth must be South Africa.</li>
<li>Visit the Home Affairs website, complete the application and submit it.</li>
<li>Pay Home Affairs in Online Banking: Transact, then My Bills under Pay, then Billing beneficiaries, then Dept of Home Affairs.</li>
<li>Once payment has been received, the Home Affairs system lets you make an appointment at a specialised branch.</li>
<li>Print and keep the booking confirmation letter and reference number.</li>
<li>Visit that branch on the appointment date with your ID, for fingerprints and a photo.</li>
<li>Home Affairs sends an SMS when the Smart ID or passport is ready. Collect it at the branch you selected.</li>
</ol>
<p>Online services Standard Bank names: first-time ID, green ID to Smart ID, Smart ID re-issue, Smart ID replacement after a surname change already done at Home Affairs, first-time passport and passport renewal{src('sb')}.</p>
<p>Standard Bank does not call this appointment BABS. Whether the online appointment step is BABS or eHomeAffairs: not stated by source. Standard Bank says it does not control client bookings made online, DHA turnaround, collection dates or cancellation notifications, and it gives the DHA number 0800 601 190 for complaints about the service{src('sb')}. Branch lists: <a href="../banks/standard-bank/index.html">Standard Bank</a>.</p></div>
<h3>FNB</h3>
<div class="card"><p><strong>Replace a lost, stolen or damaged Smart ID.</strong> FNB says no appointment is needed. Visit a selected branch, have fingerprints and a photo taken, and approve payment in the FNB App or online banking. FNB says payments cannot be made in branch by cash, debit card or credit card. On the same page FNB also says you do not need to bring documentation for a Smart ID in branch, and, in the replace steps, to visit with your original identity document. Both sentences are on FNB's page{src('fnb')}. Cost stated there: Smart ID R140, and FNB charges no additional fee. Senior citizens (60 and older) do not pay for their first Smart ID, as FNB states it{src('fnb')}.</p>
<p><strong>Apply or renew a Smart ID or passport.</strong> FNB's steps, which it names as eHomeAffairs{src('fnb')}:</p>
<ol>
<li>On dha.gov.za, select Smart ID Card and Apply Online Now. Complete registration, then approve payment in the FNB App or online banking: Pay, then Government Bills + Smart IDs.</li>
<li>Log in to eHomeAffairs, select an FNB branch, then a date and time.</li>
<li>Visit one of the seven FNB branches with DHA representation. Bring original identity documents (green ID book, passport or birth certificate).</li>
<li>An SMS arrives when the document is ready. Bring original identity documents when you collect it.</li>
</ol>
<p>A walk-in for this eHomeAffairs route: not stated by source. For a minor, FNB says both parents accompany the child for a passport, and one parent for a Smart ID{src('fnb')}. FNB's eHomeAffairs help line, as printed there, is the DHA call centre 0800 60 11 90{src('fnb')}. Branches: <a href="../banks/fnb/index.html">FNB</a>.</p></div>
<h3>Absa</h3>
<div class="card"><p>Absa says you can book online, book in the Absa Banking App, or walk into a selected branch. You must have an Absa Cheque or Savings account. You pay at the branch, not online. If you booked, bring the SMS or email confirmation{src('absa')}.</p>
<p>Absa's online booking steps{src('absa')}:</p>
<ol>
<li>Go to the secure booking portal (the link is on Absa's Smart ID page).</li>
<li>Type in your ID number.</li>
<li>Choose SMS, email, or both, for the booking confirmation.</li>
<li>Pick a branch and an appointment time.</li>
<li>Tap Submit.</li>
</ol>
<p>In the Absa Banking App: log in, open Menu, tap Government Services, and follow the prompts{src('absa')}. Whether Absa's portal is BABS: not stated by source. DHA's fee, as Absa states it, is R140, paid at the appointment. Any extra Absa fee: not stated by source. Branches: <a href="../banks/absa/index.html">Absa</a>.</p></div>
<h3>Nedbank</h3>
<div class="card"><p>Nedbank describes the eHomeAffairs route, not a walk-in and not BABS. Its steps{src('ned')}:</p>
<ol>
<li>On eHomeAffairs, create a new application or continue a saved one.</li>
<li>Complete the online form.</li>
<li>Upload the documents the form asks for.</li>
<li>Pay online with Nedbank. Nedbank says you need your profile number (Money app: top of the screen under More; Online Banking: your initials at the top right) and that the bank user ID for Nedbank is 1. Then release the payment under Pay, Government payments. Amount and reference are prepopulated.</li>
<li>Select a date and a participating Nedbank branch. On that date you visit in person for fingerprints and a photo. Bring the booking confirmation and your ID book or card. Nedbank says requirements differ for children under 18 and refers you to DHA. Those child requirements: not stated by source.</li>
<li>When the card is ready, an SMS is sent. Collect it at the branch you selected.</li>
</ol>
<p>A walk-in without that booking: not stated by source. Nedbank says it is subletting space to DHA officials, who issue IDs and passports, and that Nedbank is not otherwise involved{src('ned')}. Branches: <a href="../banks/nedbank/index.html">Nedbank</a>.</p></div>
<h2>eHomeAffairs steps for a bank office</h2>
<p>DHA's "How to use eHomeAffairs" guide is the department's own sequence for a Smart ID card and/or passport application that can end at a bank office{src('ehowto')}. FNB and Nedbank point customers at this channel by name{src('fnb','ned')}. The guide's order is:</p>
<ol>
<li>Register a profile: personal details, a password, and security questions.</li>
<li>Enter the verification OTP from SMS to confirm your cellphone number.</li>
<li>Log in.</li>
<li>Enter the logon OTP from SMS.</li>
<li>Complete the application. You can capture one for yourself or for a minor directly related to you, which the guide describes as typically a minor passport. Fields highlighted in red are mandatory.</li>
<li>Submit.</li>
<li>Upload supporting documents if the form lists any. Originals must be presented at the branch or bank office.</li>
<li>Pay online. Submitting the payment is only an instruction to your bank. You then log on to internet banking to authorise it. Bank payment verification may take a few minutes. A payment guide can be requested from your bank.</li>
<li>Book at a Home Affairs enabled bank office. The guide says a booking is a prerequisite for biometrics at that bank office. It also says you do not need a booking to give biometrics at a Home Affairs office.</li>
<li>Print the confirmation letter. Take the barcoded confirmation letter, and your ID book if you have it, to the branch or bank office. Use Download Confirmation, save the file, and open it as a PDF.</li>
</ol>
<div class="card"><strong>No walk-ins on the older bank lists</strong>
<p>DHA's bank-branch page for every province uses the same sentence: "NO Walk-in's are allowed at BANKS. You can ONLY visit a bank branch once you have made an online application and booked your visit." The pages are {PROVLINKS}.</p>
<p>Those pages are the older lists (they are linked from DHA's <a href="{S['legacy']}" rel="noopener">bank branches</a> page, which itself says to apply online and book). They are not the Digital Partnership locator. The Digital Partnership page is a separate page, and it is the one that says Capitec and Standard Bank allow walk-ins without an appointment{src('digital','legacy')}.</p>
<p>The Gauteng list includes Discovery Bank Sandton as well as Absa and FNB offices. Discovery's own booking steps: not stated by source{src('gtb')}.</p></div>
<h2>Walk-ins in one place</h2>
<div class="wrap"><table><tr><th>Route</th><th>What the source says</th></tr>
<tr><td>Home Affairs office (BABS)</td><td>Walk-ins are served. Booked clients are prioritised. A booking is not described as the only way in{src('babs','ar2324','ehowto')}.</td></tr>
<tr><td>Capitec, Digital Partnership</td><td>DHA: walk-in, no appointment{src('digital')}. An appointment rule on Capitec's own article: not stated by source{src('cap')}.</td></tr>
<tr><td>Standard Bank, in branch</td><td>Walk-in applications are accepted{src('sb')}.</td></tr>
<tr><td>Standard Bank, online</td><td>You visit on the appointment date after payment. A walk-in for this online route: not stated by source{src('sb')}.</td></tr>
<tr><td>FNB, Smart ID replacement</td><td>No appointment needed{src('fnb')}.</td></tr>
<tr><td>FNB, eHomeAffairs</td><td>Book a branch, date and time. A walk-in for this route: not stated by source{src('fnb')}.</td></tr>
<tr><td>Absa</td><td>Book online, book in the app, or walk in{src('absa')}.</td></tr>
<tr><td>Nedbank, eHomeAffairs</td><td>Select a date, then visit. A walk-in without that booking: not stated by source{src('ned')}.</td></tr>
<tr><td>Older DHA bank-branch lists</td><td>No walk-ins. Online application and a booked visit first{src('gtb')}.</td></tr>
</table></div>
<p>Branch lists and client rules: <a href="../banks/capitec/index.html">Capitec</a>, <a href="../banks/standard-bank/index.html">Standard Bank</a>, <a href="../banks/fnb/index.html">FNB</a>, <a href="../banks/absa/index.html">Absa</a>, <a href="../banks/nedbank/index.html">Nedbank</a>, and <a href="../provinces/index.html">provinces</a>. What to pay and what to carry: <a href="../fees-and-documents/index.html">Fees and documents</a>. After the application: <a href="../collecting-smart-id-or-passport/index.html">Collecting a Smart ID or passport</a>.</p>'''
page('booking-and-walk-ins/index.html',"Booking a Smart ID: BABS, bank branches and walk-ins",bb,"How to book a South African Smart ID: BABS for Home Affairs offices, eHomeAffairs for older bank branches, and walk-in rules at Digital Partnership banks.")
# LOST OR STOLEN
ls=f'''<h1>Replacing a lost or stolen Smart ID</h1>
<p>This page compares what official DHA, gov.za and bank pages say about replacing an identity document that has been lost, stolen or damaged, including a police report or an affidavit only where that page states it. The tariff list is on <a href="../fees-and-documents/index.html">Fees and documents</a>. Booking a Home Affairs office, and how a bank visit differs, is on <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>. Branch lists are on the <a href="../banks/capitec/index.html">bank</a> pages and the <a href="../provinces/index.html">province</a> pages.</p>
<div class="card note"><strong>DHA publishes two document rules for the same kind of re-issue.</strong>
<p>The civic identity documents page says that replacing a Smart ID card requires a copy of the old, lost or damaged card, or an affidavit{src('iddocs')}. The Digital Partnership page says you do not need to bring any documents, and it names Smart ID re-issues for a lost, stolen or damaged card as a service at participating bank branches{src('digital')}. Neither page explains the difference.</p></div>
<h2>What the identity documents page requires</h2>
<div class="card"><p>DHA's identity documents page says identity documents are issued to South African citizens and permanent residence permit holders from the age of 16. It says Smart ID cards can only be applied for at modernised offices, and that those offices include banks, DHA offices in malls, and mobile offices. A date on the page: not stated by source{src('iddocs')}.</p>
<p>Under first-time applicants, the page adds that if you are in position of an ID book, your application is a re-issue. Documents for a first Smart ID at 16, who must attend, and how that list differs from the brochure, are on <a href="../first-smart-id-at-16/index.html">First Smart ID at 16</a>. The brochure list is also on <a href="../fees-and-documents/index.html">Fees and documents</a>{src('iddocs','sidpdf')}.</p>
<p>For a re-issue of a Smart ID card, the page lists{src('iddocs')}:</p>
<ul>
<li>Replacing a green barcoded ID book with a Smart ID card: a copy of the green barcoded identity document, or an affidavit if that identity document is lost.</li>
<li>Replacing a Smart ID card: a copy of the old, lost or damaged card, or an affidavit. The sentence on the page is printed as "an affidavitis required".</li>
<li>A marriage certificate if your status has changed.</li>
<li>A divorce decree if you are divorced.</li>
<li>The fee for the re-issue is R140.00.</li>
</ul>
<p>Those bullets use "lost" and "damaged". The word "stolen" is not in them. A police station, a case number, and the words the affidavit must contain: not stated by source{src('iddocs')}.</p>
<p>People of 60 and older who are converting from a green barcoded ID book to a Smart ID card: the page says that conversion is free. A free re-issue of a Smart ID card that was lost, stolen or damaged, because the holder is 60 or older: not stated by source{src('iddocs')}.</p>
<p>The same page has a separate list for a green ID book at offices that do not offer Smart ID cards. It says provide an affidavit where the green barcoded ID book has been lost or damaged, a certified copy of the marriage certificate if you are married and want to assume a spouse's surname, and a fee of R140.00. Stolen, in that bullet: not stated by source{src('iddocs')}.</p></div>
<div class="card"><p>The gov.za service page says you can apply to re-issue an ID if the ID book has been lost, stolen or damaged, and for the surname changes it names. An affidavit on that page: not stated by source. The page still says the green ID book is being replaced over eight years starting in 2014, so an application now will not necessarily produce an ID card, and that someone who already has an ID will be invited to apply for the card. The current identity documents page and the Digital Partnership page both describe Smart ID applications as available{src('idapply','iddocs','digital')}.</p>
<p>For a name change, the Digital Partnership page says name changes and amendments to personal details are not yet available at those bank branches, and that those clients must visit a Home Affairs office{src('digital')}. Standard Bank says it cannot assist with a surname change{src('sb')}.</p></div>
<h2>What the bank partnership page requires</h2>
<div class="card"><p>DHA's Digital Partnership page lists Smart ID card re-issues (lost, stolen or damaged) and green ID book to Smart ID card replacements as the services available at participating branches. Passport applications in phase 1, first-time IDs (for example turning 16), late registration of birth, name changes, amendments to personal details, and complex civic services are not yet available there{src('digital')}.</p>
<ul>
<li>Documents: "You do not need to bring any documents." The same page says Capitec and Standard Bank allow walk-ins without an appointment, and that no existing documents are needed{src('digital')}.</li>
<li>A police report or an affidavit for this bank visit: not stated by source{src('digital')}.</li>
<li>The applicant must attend in person so that biometrics can be captured. Someone else applying on your behalf: the page says no{src('digital')}.</li>
<li>Children applying for a first ID or any other document: the page says they must apply at a Home Affairs office{src('digital')}.</li>
<li>DHA fee: R140 for a Smart ID card. Banks may charge a convenience fee{src('digital')}.</li>
<li>Time in the branch: it differs by bank, and the page says services will take approximately 15 minutes. How long the card then takes to be produced: not stated by source{src('digital')}.</li>
<li>Collection: at the bank branch where the application was made. The partner bank communicates the collection details. Delivery on this page: not stated by source{src('digital')}. The partner-branch page uses a different collection sentence{src('locator')}. Notice, what to bring, who may collect, and any deadline: <a href="../collecting-smart-id-or-passport/index.html">Collecting a Smart ID or passport</a>.</li>
</ul>
<p>How to use a walk-in branch, and how that differs from BABS or eHomeAffairs: <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>.</p></div>
<h2>Affidavit and police reporting</h2>
<p>Only the sources in this table mention an affidavit, the police, or both. Where a source is silent, the cell says so.</p>
<div class="wrap"><table><tr><th>Source</th><th>What it states</th><th>What it does not state</th></tr>
<tr><td>DHA identity documents page</td><td>An affidavit if the green ID is lost and you are converting it to a Smart ID. For a Smart ID card re-issue, a copy of the old, lost or damaged card, or an affidavit. For a green ID book re-issue at an office without Smart ID cards, an affidavit if that book is lost or damaged{src('iddocs')}.</td><td>Police, a case number, and the contents of the affidavit: not stated by source. The word stolen, in these bullets: not stated by source.</td></tr>
<tr><td>DHA Digital Partnership page</td><td>Lost, stolen or damaged Smart ID re-issues are offered at participating branches, and you do not need to bring any documents{src('digital')}.</td><td>A police report or an affidavit: not stated by source.</td></tr>
<tr><td>DHA Smart ID brochure</td><td>For a first Smart ID, pensioners of 60 and older and other citizens: the green barcoded ID, or an affidavit if that identity document is lost{src('sidpdf')}.</td><td>A police report for someone who already holds a Smart ID card: not stated by source. The full first-issue list is on <a href="../fees-and-documents/index.html">Fees and documents</a>.</td></tr>
<tr><td>gov.za, what an affidavit is</td><td>An affidavit is a written statement under oath. Affidavits are often required when replacing lost or stolen documents, and the examples given are an ID and a passport. An affidavit can be made at any police station, where an officer provides a standard form{src('aff')}.</td><td>That DHA requires one for every Smart ID re-issue: not stated by source. A case number: not stated by source. A date on the page: not stated by source.</td></tr>
<tr><td>Nedbank Smart ID page</td><td>If you lose your ID card, report it to the police as lost and apply to DHA for a new card. You pay the cost. Budget for a temporary ID if you will need one while you wait{src('ned')}.</td><td>An affidavit: not stated by source. The word stolen, in that answer: not stated by source. The rand amount: not stated by source.</td></tr>
<tr><td>Capitec, Standard Bank, FNB and Absa Smart ID pages</td><td>See the bank section below for the replacement each page does describe.</td><td>A police report or an affidavit: not stated by source{src('cap','sb','fnb','absa')}.</td></tr>
<tr><td>Vuk'uzenzele, August 2013</td><td>If you lose the ID after you have applied for a Smart ID card, provide a police case number and an affidavit, and pay the prescribed fee for the new card{src('vuku')}.</td><td>This answer is about losing the document after the application, and the page is dated August 2013. The current identity documents page and the Digital Partnership page do not repeat a police case number for an ordinary re-issue{src('iddocs','digital')}.</td></tr>
<tr><td>DHA duplicate identity numbers notice</td><td>For the people named on that notice, if the identity document is lost, attach an affidavit from the police. The notice is about two or more identity numbers, or people sharing one number, and it said those cases were to be resolved by the end of October 2013{src('dupid')}.</td><td>An ordinary Smart ID re-issue in 2026: not stated by source. The notice is a different process.</td></tr>
</table></div>
<h2>Fee, and a temporary certificate</h2>
<div class="card"><p>The DHA fees page, marked updated August 2026, lists identity document re-issuing at R140.00. The identity documents page states the same R140.00 for a Smart ID card re-issue and for a green ID book re-issue{src('fees','iddocs')}.</p>
<p>The fees page also names cases where a re-issue is free: the forename was repeated as the surname because the department did not insist on a surname at the first application, and a new identity document for a former TBVC citizen that replaces an old document classifying that person as a non-South African citizen. Lost, stolen and damaged do not appear in that free-of-charge sentence{src('fees')}.</p>
<p>On the same fees page, a lost, damaged or stolen passport, child passport, maxi passport or document for travel purposes is charged at double the current tariff for that document, unless it was stolen, lost or damaged through no negligence of the holder, in which case the normal fee applies. That double tariff is the passport line. The identity document re-issue line remains R140.00{src('fees')}.</p>
<p>Bank amounts stated on each bank's own page are in the table below. The wider tariff list, including a first issue at no charge, is on <a href="../fees-and-documents/index.html">Fees and documents</a>.</p></div>
<div class="card"><strong>Temporary Identity Certificate</strong>
<p>The identity documents page says a Temporary Identification Certificate, valid for two months, can be issued at R70.00, and that the application is subject to positive verification of your fingerprints. It does not say a bank branch issues it, and it does not say every lost or stolen Smart ID must have one{src('iddocs')}.</p>
<p>The gov.za service page describes a temporary identity certificate for a different situation: the identity document application will not be finished in time to vote. The fee there is R70, and the items listed are an ID number for verification and 2 ID photos. Two months, and fingerprint verification: not stated on that page{src('idapply')}.</p>
<p>A statement of 18 May 2011 says temporary identification certificates are issued when citizens have lost or misplaced their IDs while waiting for a new ID, and that the usual practice was to apply for the certificate at the same time as the new ID. The fee printed on that 2011 statement is R140. The current fees page, updated August 2026, lists the certificate at R70.00{src('tic2011','fees')}.</p>
<p>Nedbank tells you to budget for a temporary ID if you will need one. The amount, and whether the Nedbank visit issues it: not stated by source{src('ned')}.</p></div>
<h2>What each bank says</h2>
<div class="wrap"><table><tr><th>Bank</th><th>Lost, stolen or damaged</th><th>Documents that bank states</th><th>Police or affidavit</th><th>Fee that bank states</th></tr>
<tr><td><a href="../banks/capitec/index.html">Capitec</a></td><td>Smart ID replacements include a lost, stolen or damaged Smart ID card, and replacing a green ID book. First-time IDs are not available in branch{src('cap')}.</td><td>No documents. Bring the green ID book only if you open an account during the visit. The visit is in person, for a photo, fingerprints and a signature{src('cap')}.</td><td>Not stated by source.</td><td>R150 in total: R140 DHA fee plus R10 service fee. You pay from a Capitec account{src('cap')}.</td></tr>
<tr><td><a href="../banks/standard-bank/index.html">Standard Bank</a></td><td>In branch and online: re-issue for a lost, stolen or damaged ID. A later answer on the same page also includes destroyed{src('sb')}.</td><td>In branch, under "What you'll need": green barcoded ID or driver's licence. Online: the payment and booking reference, and the visit step says to come with your ID. DHA's partnership page says no existing documents are needed for a Standard Bank walk-in{src('sb','digital')}.</td><td>Not stated by source.</td><td>R140 DHA fee. Standard Bank says it is currently not charging a convenience fee. You need a Standard Bank account{src('sb')}.</td></tr>
<tr><td><a href="../banks/fnb/index.html">FNB</a></td><td>Replace a lost, stolen or damaged Smart ID at selected branches. No appointment for that replacement{src('fnb')}.</td><td>The replace steps say to visit with your original identity document. A later point on the same page says you do not need to bring documentation for a Smart ID in branch. When you collect, bring original identity documents{src('fnb')}.</td><td>Not stated by source.</td><td>Smart ID R140. FNB charges no additional fee. Payment is approved in the FNB App or online banking, not in cash, debit card or credit card in the branch{src('fnb')}.</td></tr>
<tr><td><a href="../banks/absa/index.html">Absa</a></td><td>The page says renew your Smart ID, book online, book in the app, or walk in. Lost, stolen or damaged: not stated by source{src('absa')}.</td><td>If you booked, bring the SMS or email confirmation. Any other document: not stated by source{src('absa')}.</td><td>Not stated by source.</td><td>DHA fee of R140, paid at the branch. An extra Absa fee: not stated by source. You need an Absa Cheque or Savings account{src('absa')}.</td></tr>
<tr><td><a href="../banks/nedbank/index.html">Nedbank</a></td><td>If you lose the card, report it to the police as lost and apply to DHA for a new card. The page also says you do not renew an ID card unless you lose or damage it. Stolen, in the lose answer: not stated by source{src('ned')}.</td><td>The eHomeAffairs visit says bring the booking confirmation and your ID book or card, and upload the documents the form asks for. A separate lost-card document list: not stated by source{src('ned')}.</td><td>Report the lost card to the police. An affidavit: not stated by source{src('ned')}.</td><td>You will have to pay the cost. The amount: not stated by source. DHA's re-issue tariff is R140.00{src('ned','fees')}.</td></tr>
</table></div>
<h3>Capitec</h3>
<div class="card"><p>Capitec's article dated 11/03/2026 on the page says the in-branch service is for Smart ID replacements: a lost, stolen or damaged Smart ID card, or a green ID book replaced with a Smart ID card. You pay from a Capitec account. If you have no account, the branch can help you open one, and it must be active with a positive balance before the application continues. If the stolen card was your only identity document, what Capitec then accepts in order to open the account: not stated by source{src('cap')}.</p>
<p>Branches and the account rule: <a href="../banks/capitec/index.html">Capitec</a>.</p></div>
<h3>Standard Bank</h3>
<div class="card"><p>In branch, Standard Bank takes walk-ins for a lost, stolen or damaged re-issue, a green ID conversion, and a Smart ID after a surname change that Home Affairs has already done. You pay at the branch and collect from that branch. Online, the same lost, stolen or damaged re-issue is listed, together with a first-time ID and passports, and you visit on the appointment date{src('sb')}.</p>
<p>Standard Bank says the card typically takes up to 4 weeks, that timelines may be affected by other factors, and that you collect your own ID at the same branch. You have 12 months from the ready notification. After that, the ID is sent back to DHA and it may be destroyed, and a new application is required if it is destroyed{src('sb')}. That 12 month window is Standard Bank's answer. What the other banks, and the current DHA pages, do and do not say about a deadline is on <a href="../collecting-smart-id-or-passport/index.html">Collecting a Smart ID or passport</a>. Steps for the online booking are on <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>. Branches: <a href="../banks/standard-bank/index.html">Standard Bank</a>.</p></div>
<h3>FNB</h3>
<div class="card"><p>FNB separates a lost, stolen or damaged replacement, which needs no appointment, from an eHomeAffairs application for a Smart ID or passport, which is booked. The replacement is for FNB customers with an active, funded transactional account, who are South African citizens by birth or naturalisation, or permanent residents. Senior citizens of 60 and older do not pay for their first Smart ID, which is how FNB states that exemption. A free replacement of a lost Smart ID because the holder is 60 or older: not stated by source{src('fnb')}.</p>
<p>Branches: <a href="../banks/fnb/index.html">FNB</a>.</p></div>
<h3>Absa</h3>
<div class="card"><p>Absa's Smart ID page describes renewal: book on Absa's portal, book in the Absa Banking App under Menu then Government Services, or walk into a selected branch. It states the R140 DHA fee, paid at the appointment. It does not state that renewal covers a lost, stolen or damaged card, and it does not state a police report or an affidavit{src('absa')}.</p>
<p>Branches: <a href="../banks/absa/index.html">Absa</a>.</p></div>
<h3>Nedbank</h3>
<div class="card"><p>Nedbank's lost-card answer sends you to the police and then to DHA. It does not say the eHomeAffairs appointment at a Nedbank branch is that application. Nedbank says it sublets space to DHA officials, who issue IDs and passports, and that Nedbank is not otherwise involved{src('ned')}.</p>
<p>The eHomeAffairs steps, for an application generally, are: create or continue an application, complete the form, upload documents, pay online with Nedbank, choose a date and a participating branch, then visit for fingerprints and a photo. At that step, Nedbank says the requirements differ for children under 18 and refers you to DHA. Later on the same page, under applying at the DHA, Nedbank states a birth certificate, proof of address, and a parent or guardian if the applicant is younger than 18. That later list is compared on <a href="../first-smart-id-at-16/index.html">First Smart ID at 16</a>{src('ned')}.</p>
<p>Branches: <a href="../banks/nedbank/index.html">Nedbank</a>.</p></div>
<p>Back to the <a href="../index.html">home page</a>, <a href="../fees-and-documents/index.html">fees and documents</a>, and <a href="../booking-and-walk-ins/index.html">booking and walk-ins</a>.</p>'''
page('lost-or-stolen-smart-id/index.html',"Replacing a lost or stolen Smart ID: DHA and bank rules",ls,"What DHA and each bank say about replacing a lost, stolen or damaged Smart ID, including a police report or affidavit only where an official source states it.",checked="22 October 2026")
# FIRST SMART ID AT 16
ft=f'''<h1>First Smart ID at 16</h1>
<p>This page is for a first identity document from age 16: who must apply, what to carry, who must come along, what it costs, and whether a bank branch can take it. DHA publishes more than one list, and the lists do not match. The cells below keep each list with the page it comes from. Tariffs in one table are on <a href="../fees-and-documents/index.html">Fees and documents</a>. Booking a Home Affairs office, which is not the same as a bank visit, is on <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>. A card you already had, including a green ID book converted to a Smart ID: <a href="../lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>.</p>
<div class="card note"><strong>Already holding a green ID book is not this application.</strong>
<p>On the identity documents page, the first-time Smart ID heading says that if you are in position of an ID book, your application is a re-issue{src('iddocs')}. That page then lists a copy of the green ID, or an affidavit if it is lost, and a fee of R140.00. People of 60 and older who are converting a green ID book to a Smart ID card are free on that page{src('iddocs')}. This page does not repeat those re-issue rules.</p></div>
<h2>Who must apply, and from what age</h2>
<div class="card"><ul>
<li>The Identification Act, 1997 (Act 68 of 1997) applies to South African citizens and to persons who are lawfully and permanently resident in the Republic. Section 15(1) says any such person who has attained the age of 16 years shall apply for an identity card, in the prescribed form and within the prescribed period{src('idact')}.</li>
<li>The gov.za page for that Act lists one amendment: the Identification Amendment Act 28 of 2000. That Act replaces the definition of identity card, and the transitional section on green bar-coded identity documents. It does not amend section 15{src('idactpage','idamd')}.</li>
<li>How many days the prescribed period is: not stated in the Act. The name or number of the prescribed form: not stated in the Act{src('idact')}.</li>
<li>Section 17(2): if a Home Affairs officer learns that a person covered by the Act has attained 16 and has not complied with section 15(1), that officer shall take the prescribed steps so that the person applies without delay. What those steps are: not stated in the Act{src('idact')}.</li>
<li>Section 18(2)(c): a person who without lawful cause refuses to comply with section 10 (fingerprints) or with section 15(1) is guilty of an offence, and is liable on conviction to a fine or to imprisonment for a period not exceeding five years. The rand amount of that fine: not stated in the Act{src('idact')}.</li>
<li>DHA's identity documents page cites the same Act and says an identity document is issued as soon as a person is eligible, from 16 years old and above. It says identity documents are issued to South African citizens and permanent residence permit holders from the age of 16{src('iddocs')}.</li>
<li>The gov.za service page says that if you are 16 years and older, you may apply for an identity document. It says you will need an ID to register for matric exams, to get a driving licence, or to open a bank account{src('idapply')}.</li>
<li>Applying before the 16th birthday: not stated by these sources. Each of them starts at 16, or at having attained 16.</li>
<li>An upper age, after which someone who never applied may no longer apply: not stated by these sources. Section 15(1) has no upper age in its text{src('idact')}.</li>
</ul>
<p>The gov.za service page still says the green ID book is being replaced over eight years starting in 2014, so an application now will not necessarily produce an ID card. The identity documents page says a Smart ID card can be applied for at a modernised office{src('idapply','iddocs')}. The two pages do not explain the difference.</p></div>
<h2>Where the application is made</h2>
<div class="card"><p>The identity documents page says Smart ID cards can only be applied for at modernised offices, including banks, DHA offices in malls, and mobile offices{src('iddocs')}. The Digital Partnership page is the current bank walk-in service, and it says a first ID is not part of that service. First-time ID applications, and the example it gives is turning 16, are not yet available at those branches. The answer on the same page to "Can I apply for a first-time ID at a bank branch?" is no: first-time ID applications must be done at a Home Affairs office. Children applying for a first ID, or for any other document, must also apply at a Home Affairs office{src('digital')}.</p>
<p>A gov.za statement of 22 July 2026 says the Digital Partnership will continue to expand before the end of the year to include adult and minor passports and first-time Smart ID card applications{src('absams')}. The Digital Partnership page still lists first-time IDs as not yet available. This page was checked on 23 October 2026{src('digital')}.</p>
<p>The office visit itself can be booked on BABS, which DHA describes as a time slot to get into the office, not as a bank booking. Walk-in wording for offices, and the bank routes, are on <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>{src('babs')}.</p>
<p>People living abroad: the identity documents page says they can apply for ID books at a South African mission or consulate, and that the application is sent to Head Office in Pretoria. A first Smart ID card at a mission: not stated in that sentence. Delivery from abroad takes longer than a local application, because of the logistics{src('iddocs')}.</p>
<p>Collection, on that page: a green ID book is collected from the office where the application was made. A Smart ID card is collected at the modernised office you chose when you applied. Specify that office before the application is closed. DHA sends progress and collection messages to the cellphone number captured on the application{src('iddocs')}. What to bring, who may collect, a bank collection, and any deadline: <a href="../collecting-smart-id-or-passport/index.html">Collecting a Smart ID or passport</a>.</p></div>
<h2>Which banks say they take a first ID</h2>
<p>DHA's partnership rule is in the first row. Each bank row is that bank's own page, which is not always the same rule. Branch lists are on the bank pages linked in the table.</p>
<div class="wrap"><table><tr><th>Route</th><th>First-time ID</th><th>Parent or guardian</th><th>Fee that source states</th></tr>
<tr><td>DHA Digital Partnership branches</td><td>No. First-time applications, for example turning 16, must be done at a Home Affairs office. Children must apply at a Home Affairs office{src('digital')}.</td><td>Who attends at the Home Affairs office: not stated by source.</td><td>That page states a DHA fee of R140 for a Smart ID card, and says banks may charge a convenience fee. A separate first-time fee: not stated by source. The same page says the first-time service is not available at the branch{src('digital')}.</td></tr>
<tr><td><a href="../banks/capitec/index.html">Capitec</a></td><td>Not available in branch yet. The in-branch service is a Smart ID replacement: lost, stolen or damaged, or a green ID book replaced with a Smart ID. The article is dated 11/03/2026 on the page{src('cap')}.</td><td>Not stated by source.</td><td>The R150 on that page (R140 DHA fee plus R10) is for the replacement it does offer. A first-time fee: not stated by source{src('cap')}.</td></tr>
<tr><td><a href="../banks/standard-bank/index.html">Standard Bank</a>, in branch</td><td>Who can apply in branch: South African citizens who currently hold a green ID book, or who need a reissue of a Smart ID. A first-time ID is not in that sentence. If you are not eligible, Standard Bank says visit a Home Affairs branch. The same page says you need a Standard Bank account before a smart ID application, and that answer is not limited to the online route{src('sb')}.</td><td>Not stated by source.</td><td>A separate first-issue amount: not stated by source. The cost answer says applicants are charged a R140 DHA fee, and that Standard Bank is currently not charging a convenience fee. It does not mention a free first issue{src('sb')}.</td></tr>
<tr><td><a href="../banks/standard-bank/index.html">Standard Bank</a>, online</td><td>First-time ID issuing is listed. Who can apply online: South African citizens who are 16 years and older. The online steps say you need an Online Banking profile, and that your country of birth must be South Africa. The visit step says to come with your ID. What that visit requires if the applicant does not yet have an identity document: not stated by source{src('sb')}.</td><td>Not stated by source.</td><td>The same cost answer: a R140 DHA fee, and no convenience fee in the current wording. A free first issue: not stated by source{src('sb')}.</td></tr>
<tr><td><a href="../banks/fnb/index.html">FNB</a>, replacement</td><td>Lost, stolen or damaged Smart ID. A first ID at 16: not stated by source{src('fnb')}.</td><td>Not stated by source.</td><td>Smart ID R140, and FNB charges no additional fee. Senior citizens of 60 and older do not pay for their first Smart ID, which is how FNB states that exemption. A free first issue at 16: not stated by source{src('fnb')}.</td></tr>
<tr><td><a href="../banks/fnb/index.html">FNB</a>, eHomeAffairs</td><td>FNB says you can apply for a Smart ID or passport on this route, and it asks who visits for a minor's application. The words "first time" and "turning 16": not stated by source. Bring original identity documents, and the examples are a green ID book, a passport, or a birth certificate{src('fnb')}.</td><td>For a minor: one parent must accompany the child for a Smart ID, and both parents for a passport. The age FNB uses for "minor": not stated by source{src('fnb')}.</td><td>FNB points you to the DHA tariff page. An amount on FNB's page for a first ID: not stated by source{src('fnb')}.</td></tr>
<tr><td><a href="../banks/absa/index.html">Absa</a></td><td>The page describes renewal of a Smart ID. A first-time ID, age 16, and a parent: not stated by source{src('absa')}.</td><td>Not stated by source.</td><td>R140 to renew, paid at the branch. A first-issue fee: not stated by source{src('absa')}.</td></tr>
<tr><td><a href="../banks/nedbank/index.html">Nedbank</a></td><td>Under "How to get your new ID card at the DHA", a citizen takes the barcoded green ID book and, if applying for the first time, also a birth certificate and proof of address. A permanent resident takes the barcoded green ID book and, if applying for the first time, also a permanent residence certificate and proof of address. A separate sentence says you qualify for an ID card if you are 16 or older and a South African citizen who was born in SA. DHA's identity documents page does not add "born in SA", and it includes permanent residence permit holders{src('ned','iddocs')}.</td><td>If you are younger than 18, a parent or guardian must accompany you. That sentence is in the citizen paragraph. The permanent resident paragraph does not repeat it. Whether a permanent resident younger than 18 must also be accompanied: not stated by source{src('ned')}.</td><td>The amount for this first application: not stated by source. DHA's first-issue tariff is free{src('ned','fees')}.</td></tr>
</table></div>
<div class="card"><p>The eHomeAffairs how-to says you can capture an application for yourself, or for a minor directly related to you, which it describes as typically a minor passport. A first Smart ID for a 16-year-old captured by a parent on that form: not stated by source{src('ehowto')}.</p>
<p>Nedbank also says that at the branch appointment the requirements differ for children under 18, and it refers you to DHA for those requirements. Photos for the ID card: Nedbank says you do not bring them, because the image is captured on site{src('ned')}.</p></div>
<h2>Documents on the DHA lists</h2>
<p>Use the column for the place you are actually going. The identity documents page and the brochure are both DHA, and they are not the same list. Neither page says which list an office will follow if you arrive with the other one.</p>
<div class="wrap"><table><tr><th>Item</th><th>Identity documents page: first Smart ID</th><th>Brochure: youth 16 and above, first Smart ID</th><th>ID book, where the office does not offer Smart ID cards</th></tr>
<tr><td>Birth record</td><td>A certified copy of a birth certificate{src('iddocs')}.</td><td>Birth certificate. The word certified: not stated by source{src('sidpdf')}.</td><td>A certified copy of your birth certificate or reference book{src('iddocs')}.</td></tr>
<tr><td>Parent, guardian or informant</td><td>A certified copy of the parents, informant or legal guardian's ID. Who attends is in the next section{src('iddocs')}.</td><td>A certified copy of one of the parent, legal guardian or informant's identity document{src('sidpdf')}.</td><td>Not stated under that heading{src('iddocs')}.</td></tr>
<tr><td>If a parent has died</td><td>The page lists "Certified copies of a death certificate and (in cases where a parent is deceased)", and a certified ID copy of the deceased parent. The death-certificate bullet is printed with that unfinished "and"{src('iddocs')}.</td><td>Death certificate or certified copy if parents are deceased{src('sidpdf')}.</td><td>Not stated under that heading{src('iddocs')}.</td></tr>
<tr><td>Where you live</td><td>Proof of residence on the first-time Smart ID list: not stated by source{src('iddocs')}.</td><td>Proof of residence where it is available, or provide the residential address{src('sidpdf')}.</td><td>Not stated under that heading{src('iddocs')}.</td></tr>
<tr><td>Photographs</td><td>Not stated on this list{src('iddocs')}.</td><td>Not stated on this list{src('sidpdf')}.</td><td>Two identical colour photographs, and a full set of fingerprints in an applicable form{src('iddocs')}.</td></tr>
<tr><td>Payment</td><td>No payment is required{src('iddocs')}.</td><td>Free of charge{src('sidpdf')}.</td><td>A fee under that first-time heading: not stated by source. The fees page lists the first identity document as free{src('iddocs','fees')}.</td></tr>
</table></div>
<div class="card"><p>Nedbank's DHA paragraph, which is not a DHA page, adds a birth certificate and proof of address for a citizen's first application, and it also tells the citizen to take the barcoded green ID book. A certified copy: not stated by source{src('ned')}.</p>
<p>Naturalised citizens and permanent residence permit holders: the identity documents page puts that list under the ID book heading, not under the Smart ID heading. It asks for the original naturalisation certificate and a copy, the original permanent residence certificate and a copy, and the original exemption certificate and a copy. Home Affairs certifies the copies. If a certificate cannot be furnished, you must apply for a reprint before the ID book application. Whether those originals are also required for a first Smart ID: not stated under the Smart ID heading{src('iddocs')}.</p></div>
<h2>Who must come with the applicant</h2>
<div class="card"><ul>
<li>Identity documents page, first Smart ID: the applicant must be accompanied by their parent or parents where the parents are alive. It can be one parent, in person. Where the parents are deceased, an informant or a legal guardian should accompany the applicant. The page uses "must" for living parents and "should" for the informant or guardian{src('iddocs')}.</li>
<li>The same bullets do not state an age at which a first-time applicant no longer needs that person. A 16-year-old and an older first-time applicant are not split{src('iddocs')}.</li>
<li>A rule that the parent must sign the form: not stated on the identity documents page or in the brochure{src('iddocs','sidpdf')}.</li>
<li>Brochure, youth 16 and above: the list includes a parent, legal guardian or informant's identity document. That someone must attend with the applicant: not stated by source{src('sidpdf')}.</li>
<li>ID book heading: a parent in attendance: not stated under that heading{src('iddocs')}.</li>
<li>FNB, for a minor's application on the eHomeAffairs route: one parent for a Smart ID, both parents for a passport. FNB's age for "minor": not stated by source{src('fnb')}.</li>
<li>Nedbank: if you are younger than 18, a parent or guardian must accompany you. That sentence sits in the citizen paragraph{src('ned')}.</li>
<li>Capitec, Standard Bank and Absa: a parent for a first ID: not stated by source{src('cap','sb','absa')}.</li>
<li>Digital Partnership: children cannot apply at those branches. Who attends at the Home Affairs office: not restated there{src('digital')}.</li>
</ul></div>
<h2>What it costs</h2>
<div class="wrap"><table><tr><th>Source</th><th>First identity document</th><th>What it does not say</th></tr>
<tr><td>DHA fees page, marked updated August 2026</td><td>Issuing of the first identity document: free. Re-issuing: R140.00, with two free exceptions that are not a first issue at 16 (a forename repeated as a surname, and a former TBVC document){src('fees')}.</td><td>An age limit on the free first issue: not stated on that row.</td></tr>
<tr><td>Identity documents page</td><td>First-time Smart ID: no payment. Re-issue of a Smart ID card: R140.00. Converting a green ID book at 60 or older: free{src('iddocs')}.</td><td>A free re-issue of a lost Smart ID because the holder is 16, or because the holder is 60: not stated. Lost and stolen re-issues are on <a href="../lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>.</td></tr>
<tr><td>Smart ID brochure</td><td>Youth who are 16 and above, first Smart ID: free. Pensioners who are 60 and above, first Smart ID: free. Other citizens, first Smart ID: R140.00. The pensioner list and the other-citizens list both start with the green bar-coded ID, or an affidavit if it is lost, not with a birth certificate{src('sidpdf')}.</td><td>The brochure does not say that "youth 16 and above" stops at 17, 18, or any later birthday.</td></tr>
<tr><td>gov.za service page</td><td>If the ID is issued and the personal information has errors, Home Affairs will replace it free of charge{src('idapply')}.</td><td>That sentence is about errors on an ID you have received. It is not the first-issue tariff.</td></tr>
</table></div>
<div class="card"><p>The brochure's free category is worded "youth who are 16 years and above". The fees page's free row is "Issuing of first document", with no later age on that row. A cutoff after which a first issue starts to cost R140: not stated by source{src('sidpdf','fees','iddocs')}.</p>
<p>A separate first-time fee, or a bank convenience fee, for a first ID at a Digital Partnership branch: not stated by source. That page says the first-time service is not available there, states R140 for a Smart ID card, and says banks may charge a convenience fee{src('digital')}. Standard Bank's cost answer says applicants are charged a R140 DHA fee and that Standard Bank is currently not charging a convenience fee. It does not mention the free first issue{src('sb')}.</p>
<p>The fees page also lists a frame of four black and white photos taken for ID applications at R40.00, and a temporary identity certificate at R70.00{src('fees')}. Whether a modernised office charges the photo frame for a first Smart ID: not stated by source. The temporary certificate is described on <a href="../lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>.</p></div>
<h2>Photographs and fingerprints</h2>
<div class="card"><ul>
<li>The Act says a person of 16 or older shall, at their own expense, furnish two prescribed copies of a recent photograph when applying for an identity card, and shall have fingerprints taken so that they can be included in the population register. Section 15(2) says those two photographs and the fingerprints accompany the application{src('idact')}.</li>
<li>The ID book list on the identity documents page asks for two identical colour photographs and a full set of fingerprints{src('iddocs')}.</li>
<li>The first-time Smart ID list on that page, and the youth list in the brochure, do not mention photographs{src('iddocs','sidpdf')}.</li>
<li>On the travel documents page, the passport document list says two colour photographs are not needed at Smart ID card offices, because the ID image is captured digitally. That sentence is in the passport section{src('travel')}.</li>
<li>Nedbank, for an ID card application: do not bring photos. The image is captured on site at the appointment{src('ned')}.</li>
</ul>
<p>These sources do not say which of those rules a first Smart ID at a modernised office uses on the day you go.</p></div>
<h2>Passport, after the identity document</h2>
<div class="card"><p>The travel documents page says a person aged 16 or older must first apply for an identity document to enable fingerprint registration before applying for a passport{src('travel')}.</p>
<ul>
<li>An ordinary tourist passport and a maxi passport are for citizens 16 or older. A minor tourist passport is for citizens 15 or younger{src('travel')}.</li>
<li>If the passport applicant is under 18, parental consent is required. For a child's passport, both parents and the child must be present, and the page says exceptions apply{src('travel')}.</li>
<li>Those are passport rules. They are not the Smart ID attendance rule on the identity documents page, which says one parent in person can accompany a first Smart ID applicant{src('travel','iddocs')}.</li>
</ul>
<p>Passport fees and the longer document list are on <a href="../fees-and-documents/index.html">Fees and documents</a>.</p></div>
<h2>What these sources do not state</h2>
<div class="card"><ul>
<li>The number of days after the 16th birthday in which the application must be made. The Act says "within the prescribed period" and does not print the number{src('idact')}.</li>
<li>The form number for a first Smart ID. The travel documents page names Form DHA-73 for a passport, not for the identity document{src('travel','iddocs','sidpdf')}.</li>
<li>A school letter, a clinic card, or proof of grade. The gov.za page says an ID is needed to register for matric. It does not say the school must supply a letter for the ID application{src('idapply')}.</li>
<li>A police report for a first ID: not stated by source{src('iddocs','sidpdf')}.</li>
<li>Which of the two DHA document lists an office will accept if you bring only one of them{src('iddocs','sidpdf')}.</li>
</ul></div>
<p>Back to the <a href="../index.html">home page</a>, <a href="../fees-and-documents/index.html">fees and documents</a>, <a href="../booking-and-walk-ins/index.html">booking and walk-ins</a>, and the bank pages: <a href="../banks/capitec/index.html">Capitec</a>, <a href="../banks/standard-bank/index.html">Standard Bank</a>, <a href="../banks/fnb/index.html">FNB</a>, <a href="../banks/absa/index.html">Absa</a>, <a href="../banks/nedbank/index.html">Nedbank</a>.</p>'''
page('first-smart-id-at-16/index.html',"First Smart ID at 16: documents, parents, fees and banks",ft,"First South African Smart ID at 16: DHA document lists, who must attend, the free first issue, and which banks do not take a first-time applicant.",checked="23 October 2026")
col=f'''<h1>Collecting a Smart ID or passport</h1>
<p>This page is for the step after you have applied: how the Department of Home Affairs (DHA) or the bank tells you a Smart ID or passport is ready, where and when you collect it, what to bring, who may collect it, and any deadline a source states. How to apply is on <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>. Tariffs and the application document lists are on <a href="../fees-and-documents/index.html">Fees and documents</a>. A card that was lost or stolen: <a href="../lost-or-stolen-smart-id/index.html">Replacing a lost or stolen Smart ID</a>. A first identity document from age 16: <a href="../first-smart-id-at-16/index.html">First Smart ID at 16</a>.</p>
<div class="card note"><strong>Do not copy one bank's collection rule onto another route.</strong>
<p>The Digital Partnership page says you collect at the bank branch where the application was made, and that the partner bank communicates the collection details. Delivery is not in that answer{src('digital')}. The partner-branch page says you collect from your selected branch, or have the document delivered where the bank offers that{src('locator')}. Only Standard Bank states that you must collect your own ID, and only Standard Bank states a 12 month collection window{src('sb')}. Where another source is silent, this page says so.</p></div>
<h2>At a Home Affairs office</h2>
<div class="card"><ul>
<li>A green barcoded ID book can only be collected from the office where the application was made{src('iddocs')}.</li>
<li>A Smart ID card is collected at the preferred modernised office you chose when you applied. Modernised offices, on that page, include banks, DHA offices in malls, and mobile offices{src('iddocs')}.</li>
<li>Specify the office of collection before the application transaction is closed or submitted. The page prints that as a warning{src('iddocs')}.</li>
<li>DHA uses the cellphone number you provided during the application to send updates about progress and the readiness for collection{src('iddocs')}.</li>
<li>The word SMS, an email, how many messages, and what the message says: not stated by source{src('iddocs')}.</li>
<li>What to bring to that collection, who may collect for you, a fee for collecting, and a deadline after which the document is sent away or destroyed: not stated by source{src('iddocs')}.</li>
</ul>
<p>People living abroad can apply for ID books at a South African mission or consulate. Applications are sent to Head Office in Pretoria, and delivery takes longer than a local application because of the logistics. That sentence is about ID books. A Smart ID card collected at a mission: not stated in that sentence{src('iddocs')}.</p>
<p>Public office hours on the DHA contacts page: Monday to Friday, 8:00 to 15:30. Every last Wednesday of the month, 9:00 to 15:30. The page calls these the hours offices are open to the public. A collection-only counter, or a different collection time: not stated on that page. The enquiry number printed there is 0800 60 11 90{src('dhacontact')}.</p></div>
<h2>The two DHA sentences for a bank</h2>
<div class="wrap"><table><tr><th>DHA page</th><th>What it says about collection</th><th>What it does not say</th></tr>
<tr><td>Digital Partnership with banks</td><td>Collections are at the bank branch where the application was made. Collection details will be communicated by the partner bank. The page prints that word as "partnerd bank". Updates about the Smart ID card application come directly from the bank, through its usual service channels{src('digital')}.</td><td>Delivery, the name of the channel (SMS, app or email), what to bring, who may collect, a production time, and a deadline: not stated by source. The "about 15 minutes" on that page is the time in the branch, and the page says it differs by bank. Passport applications during phase 1 are listed as not yet available, so this collection answer is not describing a passport{src('digital')}.</td></tr>
<tr><td>Apply through a partner branch</td><td>Updates come directly from your bank, through its usual channels. Collect the document from your selected branch, or have it delivered, where offered by the bank. The how-it-works steps sit under both the Smart ID re-issue section and the passport section{src('locator')}.</td><td>Which banks offer delivery, the channel name, what to bring, who may collect, a production time, and a deadline: not stated by source. The passport section on this page is for a standard or maxi passport, for South African citizens aged 18 and older, and for naturalised citizens aged 18 and older. A minor passport: not stated in that list{src('locator')}.</td></tr>
</table></div>
<p>Branch opening days, on the Digital Partnership page: refer to your bank and the participating branches. A collection-only time: not stated by source{src('digital')}.</p>
<h2>What each bank says</h2>
<p>Each row is that bank's own page. A blank in real life is not filled from another row. Branch lists stay on the bank pages.</p>
<div class="wrap"><table><tr><th>Route</th><th>How you are told</th><th>Where</th><th>What to bring when you collect</th><th>Who may collect</th><th>Deadline that source states</th></tr>
<tr><td><a href="../banks/capitec/index.html">Capitec</a>, article dated 11/03/2026</td><td>Not stated by source.</td><td>Not stated by source.</td><td>Not stated by source. Documents for the application itself: none, unless you are opening an account{src('cap')}.</td><td>Not stated by source.</td><td>Not stated by source. Time in the branch: normally a few minutes. How long until the card is ready: not stated by source{src('cap')}.</td></tr>
<tr><td><a href="../banks/capitec/index.html">Capitec</a>, news article dated 09/03/2026</td><td>A notification when the ID is ready. SMS, app or email: not stated by source{src('capnews')}.</td><td>Collect it from the branch{src('capnews')}.</td><td>Not stated by source.</td><td>Not stated by source.</td><td>Not stated by source. The application on a self-service terminal: less than five minutes. How long until the ID is ready: not stated by source{src('capnews')}.</td></tr>
<tr><td><a href="../banks/standard-bank/index.html">Standard Bank</a>, in branch</td><td>The ready-for-collection answer says you receive SMS updates every step of the process. That answer does not say the sender is Home Affairs, and it does not split in-branch from online{src('sb')}.</td><td>Once the smart ID is ready, collect it from the branch. A separate line says pick up the smart ID from the branch where you applied. The delivery answer says the same branch. The introduction says collect the document at one of the specialised branches. All four sentences are on the page{src('sb')}.</td><td>Not stated by source. "Your green barcoded ID or your driver's licence" is under what you need for the in-branch application, not under collection{src('sb')}.</td><td>No. You need to collect your own ID. The question on the page is about the ID{src('sb')}.</td><td>Up to 4 weeks to process the smart ID. Other factors may affect the timelines. Then 12 months from the notification that the ID is ready at the branch. After that it is sent back to DHA and it may be destroyed. A new application is required if it is destroyed. A passport is not in the in-branch service list, and a passport deadline: not stated by source{src('sb')}.</td></tr>
<tr><td><a href="../banks/standard-bank/index.html">Standard Bank</a>, online</td><td>Home Affairs sends an SMS when the smart ID or passport is ready. The same page's FAQ also gives the "SMS updates every step" answer for the smart ID{src('sb')}.</td><td>Collect the smart ID or passport at the selected branch. The online branch heading says those branches are where you give fingerprints and a photo, and where you collect the smart ID or passport{src('sb')}.</td><td>Not stated for the collection visit. The appointment visit says to come with your ID{src('sb')}.</td><td>The "collect your own ID" answer is not limited to the in-branch route. A passport collected by someone else: not stated by source{src('sb')}.</td><td>The 4 week answer and the 12 month answer are worded for the smart ID. A passport deadline: not stated by source. Standard Bank says it does not control DHA turnaround times or collection dates, and it gives 0800 601 190 for complaints about the service{src('sb')}.</td></tr>
<tr><td><a href="../banks/fnb/index.html">FNB</a>, Smart ID replacement</td><td>An SMS or an in-app notification when the Smart ID is ready for collection, or "ready to collect". Both wordings are on the page{src('fnb')}.</td><td>The collect step does not name the branch or a Home Affairs office{src('fnb')}.</td><td>Original identity documents. The same page says you do not need to bring documentation when applying for a Smart ID in branch. The collect step is the one that asks for original identity documents{src('fnb')}.</td><td>Not stated by source.</td><td>Not stated by source. The in-branch process takes about 10 minutes. How long until the card is ready: not stated by source. "When can I visit the branch?" is answered Monday to Saturday during branch operating hours. A collection-only window: not stated by source{src('fnb')}.</td></tr>
<tr><td><a href="../banks/fnb/index.html">FNB</a>, eHomeAffairs</td><td>An SMS when the Smart ID or passport is ready for collection. An in-app notice in that collect step: not stated by source{src('fnb')}.</td><td>The collect step does not name the branch or a Home Affairs office{src('fnb')}.</td><td>Original identity documents. The examples on the same page (green ID book, passport or birth certificate) are in the visit step, and the collect step does not repeat them{src('fnb')}.</td><td>Not stated by source.</td><td>Not stated by source. FNB's eHomeAffairs help line, as printed there, is 0800 60 11 90{src('fnb')}.</td></tr>
<tr><td><a href="../banks/absa/index.html">Absa</a></td><td>A message that the card is ready: not stated by source. The SMS or email on this page is the booking confirmation{src('absa')}.</td><td>Not stated by source.</td><td>Not stated by source. If you booked, bring the confirmation to the appointment. That sentence is the appointment, not a collection{src('absa')}.</td><td>Not stated by source.</td><td>Not stated by source.</td></tr>
<tr><td><a href="../banks/nedbank/index.html">Nedbank</a></td><td>An SMS when the smart ID card is ready. Who sends the SMS: not stated by source. A passport-ready message: not stated in that step{src('ned')}.</td><td>Collect the card at the branch you selected{src('ned')}.</td><td>Not stated for the collection visit. The appointment step says bring the booking confirmation and your ID book or card{src('ned')}.</td><td>Not stated by source.</td><td>Not stated by source. Nedbank says DHA officials issue IDs and passports at these branches, and that Nedbank is not otherwise involved. A passport collection place: not stated in the collect step, which says "card"{src('ned')}.</td></tr>
</table></div>
<div class="card"><p>Standard Bank's home-delivery answer is no: you collect the ID at the same branch where the application was made. The question is about the smart ID. A passport delivered to a home address: not stated in that answer{src('sb')}. Capitec, FNB, Absa and Nedbank: home delivery on their Smart ID pages: not stated by source{src('cap','fnb','absa','ned')}.</p>
<p>Walk-in application hours at Standard Bank: refer to the selected branch. That answer is about applying, not a separate collection window{src('sb')}.</p></div>
<h2>A passport, as distinct from the Smart ID</h2>
<div class="card"><ul>
<li>The travel documents page gives issuance turnaround, not a collection appointment and not a destruction deadline: 13 working days for an ordinary tourist passport and for a maxi passport, and 18 working days for a minor tourist passport. Where you collect the passport: not stated on that page{src('travel')}.</li>
<li>On that page, an application inside South Africa can be submitted at a Home Affairs front office with live capture, at participating banks, or through eHomeAffairs. The application must be made in person. Collection in person, and collection by someone else: not stated by source{src('travel')}.</li>
<li>The Digital Partnership page still lists a passport application during phase 1 as not yet available at those bank branches{src('digital')}.</li>
<li>The partner-branch page lists an adult standard or maxi passport, from age 18, for citizens and for naturalised citizens, and its collect-or-deliver step is the step quoted above{src('locator')}.</li>
<li>A gov.za statement of 9 March 2026 says that throughout 2026 the Digital Partnership will also enable passport services and courier delivery{src('golive')}.</li>
<li>A gov.za statement of 22 July 2026 says the partnership will continue to expand before the end of the year to include adult and minor passports, first-time Smart ID card applications, and, as the next major milestone, home delivery of identity documents to citizens' homes{src('absams')}.</li>
<li>This page was checked on 24 October 2026. On that date the Digital Partnership page still listed phase 1 passports as not yet available, and the partner-branch page already listed adult passports and delivery where the bank offers it. Neither page explains the difference{src('digital','locator')}.</li>
<li>Standard Bank's online route names first-time passport issuing and passport renewal, an SMS from Home Affairs, and collection at the selected branch{src('sb')}. FNB's eHomeAffairs collect step names the Smart ID or the passport, and original identity documents{src('fnb')}. Capitec's two articles, and Absa's Smart ID page: a passport collection: not stated by source{src('cap','capnews','absa')}.</li>
</ul>
<p>Passport fees are on <a href="../fees-and-documents/index.html">Fees and documents</a>.</p></div>
<h2>Older statements about a deadline</h2>
<div class="card"><p>A Home Affairs media briefing dated 19 August 2011 said that, at the end of July 2011, 610 655 IDs were still to be collected, and that a further 269 940 IDs were awaiting destruction at Head Office after applicants had not collected them for twelve months. It told people to collect from the office of application. Those figures are the briefing's figures for July 2011. The current identity documents page and the Digital Partnership page do not state a 12 month rule, and they do not repeat those counts{src('idwait','iddocs','digital')}.</p>
<p>Standard Bank's 12 month answer is the only current bank page in this set that states a collection window, and it states it for the ID{src('sb')}.</p></div>
<div class="card"><p>A DHA statement published on 4 December 2025 extended office hours on 8 to 19 December 2025 and 5 to 16 January 2026, by two hours a day, for applications and collections. On those days, offices equipped for Smart ID cards and passports would close at 18:00 instead of 16:00. Clients were advised to book an application or collection appointment on the Branch Appointment Booking System (BABS) before visiting. People without a booking could still visit as walk-ins. The statement says dedicated counters are offered for collections, in that message to people who had applied for Smart ID cards and passports. Whether those hours, that booking advice, or those counters apply on other dates: not stated by source{src('festive')}. The booking routes are on <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>.</p></div>
<h2>What these sources do not state</h2>
<div class="card"><ul>
<li>One collection rule for every bank. Absa's page does not state collection at all{src('absa')}.</li>
<li>That the Standard Bank 12 month window, or the duty to collect your own ID, applies at Capitec, FNB, Absa, Nedbank, or a Home Affairs office{src('sb','iddocs','digital')}.</li>
<li>A fee charged for the collection visit itself{src('iddocs','digital','fees')}.</li>
<li>Which banks, on 24 October 2026, actually offer the delivery the partner-branch page allows{src('locator','sb')}.</li>
<li>The screen or number you use to ask for a status if no message arrives. The contacts page and FNB print 0800 60 11 90. Standard Bank prints 0800 601 190 and says it does not control collection dates{src('dhacontact','fnb','sb')}.</li>
</ul></div>
<p>Back to the <a href="../index.html">home page</a>, <a href="../fees-and-documents/index.html">fees and documents</a>, <a href="../booking-and-walk-ins/index.html">booking and walk-ins</a>, and the bank pages: <a href="../banks/capitec/index.html">Capitec</a>, <a href="../banks/standard-bank/index.html">Standard Bank</a>, <a href="../banks/fnb/index.html">FNB</a>, <a href="../banks/absa/index.html">Absa</a>, <a href="../banks/nedbank/index.html">Nedbank</a>.</p>'''
page('collecting-smart-id-or-passport/index.html',"Collecting a Smart ID or passport: notice, place, deadline",col,"When a South African Smart ID or passport is ready: how DHA and each bank notify you, where you collect, what to bring, who may collect, and deadlines.",checked="24 October 2026")
disc=f'''<h1>Disclaimer</h1>
<p>{H.escape(DISCLAIMER)}</p>
<h2>Accuracy</h2>
<p>Pages on this site are written from Department of Home Affairs, gov.za and bank pages, and those pages are linked next to the facts. The wording can still be wrong, incomplete or out of date. A branch list, a fee, a document rule or a walk-in rule can change after the Last checked date on a page. Nothing here is a promise that a branch will accept an application on the day you visit.</p>
<h2>No warranty</h2>
<p>The site is general information only. We give no warranty, express or implied, that the pages are accurate, complete, current or fit for any purpose. We do not promise that the site will always be available.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent allowed by law, we accept no liability for any loss, cost or damage arising from using this site, from being unable to use it, or from acting or not acting on anything written here. That includes a decision about a Smart ID, a passport, a bank account, a fee, a booking, or a visit to a branch or an office. If you need advice about your own situation, ask the Department of Home Affairs, the bank, or a qualified professional.</p>
<h2>External links are not endorsed</h2>
<p>Links to official and bank websites are there so you can read the source. We do not control those sites. A link is not an endorsement of the whole site, and it is not an affiliation or a partnership.</p>
<h2>Not affiliated</h2>
<p>This independent site is not affiliated with, endorsed by, or speaking for the Department of Home Affairs, the South African government, any bank, or any other agency. Bank names and Home Affairs are used only to describe services those organisations publish.</p>
<h2>Check official sources</h2>
<p>Always confirm with the official source before you act. Use the source link next to a fact, the Department of Home Affairs website, or the bank page. Where official pages do not say the same thing, this site reports both, and the live official page is the one to follow on the day you apply.</p>
<h2>Contact and corrections</h2>
<p>This site has no contact desk, advice line or user account. It cannot take an application, book a slot, or correct a record at Home Affairs. If a fact looks wrong, open the linked official page and follow that page. Do not send an identity number, a passport number or any other personal document to this site. There is nowhere here that can receive it.</p>'''
page('disclaimer/index.html',"Disclaimer: Smart ID at the Bank, an independent guide",disc,"This independent site is not affiliated with any government, bank or agency. General information only, with no warranty and no liability for how you use it.",checked="24 October 2026")
hubs=[("/","Home"),("/fees-and-documents/","Fees and documents"),("/booking-and-walk-ins/","Booking and walk-ins"),("/lost-or-stolen-smart-id/","Lost or stolen ID"),("/first-smart-id-at-16/","First ID at 16"),("/collecting-smart-id-or-passport/","Collect your ID"),("/banks/capitec/","Capitec"),("/banks/standard-bank/","Standard Bank"),("/banks/fnb/","FNB"),("/banks/absa/","Absa"),("/banks/nedbank/","Nedbank"),("/provinces/","Provinces"),("/disclaimer/","Disclaimer")]
missing='<h1>Page not found</h1><p>That address is not a page on this site. Use the navigation above, or one of these guides.</p><ul>'+''.join(f'<li><a href="{href}">{H.escape(label)}</a></li>' for href,label in hubs)+'</ul>'
page('404.html',"Page not found: Smart ID at South African bank branches",missing,"That address is not a page on this Smart ID bank guide. Open the home page, a bank, a province, or the fees, booking, lost card and first ID guides.",sitemap=False,article=False,robots="noindex")
def sitemap_loc(path):
    if path=='index.html': return BASE+'/'
    return BASE+'/'+path[:path.rfind('/')+1]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for pth,lastmod in PATHS:
    sm+=f'  <url><loc>{sitemap_loc(pth)}</loc><lastmod>{lastmod}</lastmod></url>\n'
sm+='</urlset>\n'
assert '\u2014' not in sm and '\u2013' not in sm
open(f'{OUT}/sitemap.xml','w').write(sm)
robots=f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n'
assert '\u2014' not in robots and '\u2013' not in robots
open(f'{OUT}/robots.txt','w').write(robots)
def font_file(bold):
    names=["Inter-Bold.ttf","DejaVuSans-Bold.ttf","NotoSans-Bold.ttf"] if bold else ["Inter-Medium.ttf","Inter-Regular.ttf","DejaVuSans.ttf","NotoSans-Regular.ttf"]
    found={}
    font_root="/usr/share/fonts"
    if os.path.isdir(font_root):
        for root,dirs,files in os.walk(font_root):
            for fn in files: found.setdefault(fn,os.path.join(root,fn))
    for name in names:
        if name in found: return found[name]
    return None
def save_png(path,w,h,rgb_at):
    import struct,zlib
    def chunk(tag,data):
        return struct.pack(">I",len(data))+tag+data+struct.pack(">I",zlib.crc32(tag+data)&0xFFFFFFFF)
    raw=bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w): raw.extend(rgb_at(x,y))
    ihdr=struct.pack(">IIBBBBB",w,h,8,2,0,0,0)
    png=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",ihdr)+chunk(b"IDAT",zlib.compress(bytes(raw),9))+chunk(b"IEND",b"")
    open(path,"wb").write(png)
def write_plain_images():
    green=(11,93,59); white=(255,255,255); mint=(217,242,230)
    def card(w,h,box):
        x0,y0,x1,y1=box
        def rgb(x,y):
            if x0<=x<x1 and y0<=y<y1: return white
            if x<8 or y<8 or x>=w-8 or y>=h-8: return mint
            return green
        return rgb
    save_png(f"{OUT}/og.png",1200,630,card(1200,630,(96,150,460,480)))
    save_png(f"{OUT}/apple-touch-icon.png",180,180,card(180,180,(36,48,144,132)))
def write_images():
    svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="6" fill="#0b5d3b"/>
<rect x="6" y="8" width="20" height="16" rx="2" fill="none" stroke="#ffffff" stroke-width="1.6"/>
<circle cx="12" cy="16" r="2.3" fill="#d9f2e6"/>
<rect x="16" y="13" width="7" height="1.6" rx="0.4" fill="#ffffff"/>
<rect x="16" y="17" width="5.5" height="1.6" rx="0.4" fill="#d9f2e6"/>
</svg>
'''
    assert '\u2014' not in svg and '\u2013' not in svg
    open(f"{OUT}/favicon.svg","w").write(svg)
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("WARNING Pillow is not installed; writing a plain brand image")
        write_plain_images(); return
    bold,medium,regular=font_file(True),font_file(False),font_file(False)
    if not bold or not medium:
        print("WARNING no font found; writing a plain brand image")
        write_plain_images(); return
    bg=(11,93,59); white=(255,255,255); mint=(217,242,230); soft=(232,240,236)
    im=Image.new("RGB",(1200,630),bg)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((48,48,1152,582),radius=28,outline=mint,width=3)
    d.rounded_rectangle((96,150,460,480),radius=22,fill=white)
    d.ellipse((132,206,228,302),fill=bg)
    d.rounded_rectangle((252,222,420,246),radius=6,fill=soft)
    d.rounded_rectangle((252,266,390,286),radius=6,fill=soft)
    d.rounded_rectangle((252,306,360,326),radius=6,fill=soft)
    d.rounded_rectangle((132,390,424,428),radius=8,fill=bg)
    d.text((500,188),"Smart ID",font=ImageFont.truetype(bold,108),fill=white)
    d.text((500,320),"at the Bank",font=ImageFont.truetype(medium,58),fill=mint)
    d.text((500,400),"South Africa",font=ImageFont.truetype(regular,36),fill=mint)
    im.save(f"{OUT}/og.png","PNG")
    ic=Image.new("RGB",(180,180),bg)
    di=ImageDraw.Draw(ic)
    di.rounded_rectangle((28,46,152,134),radius=12,fill=white)
    di.ellipse((44,66,84,106),fill=bg)
    di.rounded_rectangle((94,72,136,84),radius=3,fill=soft)
    di.rounded_rectangle((94,94,128,104),radius=3,fill=soft)
    di.rounded_rectangle((44,112,136,124),radius=3,fill=bg)
    ic.save(f"{OUT}/apple-touch-icon.png","PNG")
write_images()
def png_wh(path):
    with open(path,"rb") as f:
        f.read(16)
        return int.from_bytes(f.read(4),"big"), int.from_bytes(f.read(4),"big")
assert png_wh(f"{OUT}/og.png")==(1200,630)
assert png_wh(f"{OUT}/apple-touch-icon.png")==(180,180)
print(total,len(leg),len(PATHS))
if META_WARNINGS:
    print(f"meta warnings: {len(META_WARNINGS)}")

