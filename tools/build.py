import json,re,os,html as H
D="21 October 2026"
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
.checked{font-size:13px;color:#5a6472;margin:0 0 8px}footer{max-width:960px;margin:24px auto;padding:16px;font-size:13px;color:#5a6472}
input{width:100%;padding:8px;font-size:15px;border:1px solid #cdd3da;border-radius:6px;margin:8px 0}ul.grid{columns:2;padding-left:18px}@media(max-width:600px){ul.grid{columns:1}}"""
PATHS=[]
def page(path,title,body,desc):
    PATHS.append(path)
    depth=path.count('/')
    r='../'*depth
    navl=f'<a href="{r}index.html">Home</a><a href="{r}fees-and-documents/index.html">Fees and documents</a><a href="{r}booking-and-walk-ins/index.html">Booking and walk-ins</a>'+''.join(f'<a href="{r}banks/{s}/index.html">{n}</a>' for _,n,s in BANKS)+f'<a href="{r}provinces/index.html">Provinces</a>'
    h=f'''<!doctype html><html lang="en-ZA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{H.escape(title)}</title><meta name="description" content="{H.escape(desc)}"><style>{CSS}</style><script defer src="/_vercel/insights/script.js"></script></head><body>
<header><a href="{r}index.html">Smart ID at the Bank (SA)</a><nav>{navl}</nav></header><main><p class="checked">Last checked: {D}</p>{body}</main>
<footer>Independent, unofficial guide. Not affiliated with the Department of Home Affairs (DHA) or any bank. Facts are taken only from official DHA, gov.za and bank pages, linked next to each fact. Rules change often: always confirm on the official source before you travel. DHA contact centre: 0800 60 11 90 {src('fnb')}. Last checked: {D}.</footer></body></html>'''
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
("Can I apply for my first ID (turning 16) at a bank?",f"Not at Digital Partnership branches: DHA says first-time ID applications must be done at a Home Affairs office{src('digital')}. Standard Bank lists first-time ID issuing through its online eHomeAffairs route{src('sb')}."),
("Can children apply at bank branches?",f"DHA Digital Partnership FAQ: no, children must apply at a Home Affairs office{src('digital')}. FNB (eHomeAffairs route): both parents must accompany a child for a passport, one parent for a Smart ID{src('fnb')}."),
("What do I bring?",f"DHA Digital Partnership FAQ: you do not need to bring any documents{src('digital')}. For eHomeAffairs bookings, FNB says bring original identity documents{src('fnb')}; Nedbank says bring your booking confirmation and ID book or card{src('ned')}. See <a href=\"fees-and-documents/index.html\">Fees and documents</a>.")]
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
<p><a href="booking-and-walk-ins/index.html">How to book, and where a walk-in is accepted</a>.</p></div>
<h2>Banks at a glance</h2>{banktbl}
<p>Total Digital Partnership branches in the DHA locator on {D}: <strong>{total}</strong>{src('locator')}. The locator is updated by DHA as branches join{src('locms')}.</p>
<h2>Branches by province</h2><ul class="grid">'''+''.join(f'<li><a href="provinces/{slug(p)}/index.html">{p}</a> ({sum(1 for s in dp for b in dp[s] if b["province"]==p)} Digital Partnership, {sum(1 for l in leg if l["prov"]==p)} eHomeAffairs)</li>' for p in PROV)+f'''</ul>
<h2>What is available at bank branches</h2><div class="card"><p>Available under the Digital Partnership: Smart ID re-issues (lost, stolen, damaged) and green ID book to Smart ID replacements{src('digital')}.</p>
<p>Not yet available there: passport applications (phase 1), first-time IDs (for example turning 16), late birth registration, name changes, amendments to personal details, complex civic services{src('digital')}. DHA has said passports and first-time Smart IDs will be added later{src('absams')}.</p></div>
<h2>Short FAQ</h2>'''+''.join(f'<div class="card"><strong>{q}</strong><p>{a}</p></div>' for q,a in faq)
page('index.html',"Smart ID and passport at SA bank branches: sourced guide",body,"Which South African bank branches offer Smart ID and passport services, walk-in or booking, fees, documents. Sourced from DHA and bank pages.")
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
<p>How to make the booking, and where walk-ins are accepted: <a href="../booking-and-walk-ins/index.html">Booking and walk-ins</a>.</p></div>
<div class="card"><strong>At a Home Affairs office (DHA Smart ID brochure)</strong><ul>
<li>First issue, youth 16 and older: birth certificate; certified copy of a parent, legal guardian or informant ID; death certificate if parents deceased; proof of residence where available{src('sidpdf')}.</li>
<li>First Smart ID, pensioners 60 and older and other citizens: green barcoded ID (or affidavit if lost); proof of residence where available; marriage certificate if married; divorce decree if divorced{src('sidpdf')}.</li></ul></div>
<h2>Age rules</h2><div class="card"><ul>
<li>Ordinary tourist and maxi passports: citizens 16 or older, valid 10 years; 13 working days turnaround{src('travel')}.</li>
<li>Minor tourist passport: 15 or younger, valid 5 years; 18 working days turnaround{src('travel')}.</li>
<li>A person 16 or older must first apply for an identity document before applying for a passport{src('travel')}.</li>
<li>For children's passports, both parents and the children must be present (exceptions apply){src('travel')}.</li>
<li>Digital Partnership bank branches: children cannot apply; first-time IDs must go to a Home Affairs office{src('digital')}.</li>
<li>Standard Bank online route: South African citizens 16 and older{src('sb')}.</li></ul></div>'''
page('fees-and-documents/index.html',"Smart ID and passport fees, documents and age rules (DHA)",fb,"DHA fees for Smart ID and passports, documents to bring and age rules, with sources.")
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
    b=f'<h1>{n}: Smart ID and passport at branches</h1><div class="card">{info[s]}</div><p>Booking steps for this bank, and how they differ from a Home Affairs office appointment (BABS): <a href="../../booking-and-walk-ins/index.html">Booking and walk-ins</a>.</p>'
    if s in dp:
        b+=f'<h2>{n} Digital Partnership branches ({len(dp[s])}){src("locator")}</h2><p>Data from the DHA partner branch locator on {D}. Confirm before visiting.</p>{FILTER}{dptable(dp[s],showprov=True)}'
    lg=[l for l in leg if l['name'].upper().startswith(n.upper().split()[0])]
    if lg:
        b+=f'<h2>{n} eHomeAffairs bank branches listed by DHA{src("legacy")}</h2><p>Booking required; DHA states no walk-ins.</p><div class="wrap"><table><tr><th>Branch</th><th>City</th><th>Province</th><th>Phone (as listed)</th></tr>'+''.join(f'<tr><td>{H.escape(l["name"])}</td><td>{H.escape(l["city"])}</td><td>{l["prov"]}</td><td>{l["phone"]}</td></tr>' for l in lg)+'</table></div>'
    page(f'banks/{s}/index.html',f"{n} Smart ID and passport branches: walk-in, fees, rules",b,f"{n} Smart ID and passport branch service: walk-in or booking, client requirement, fees, branch list. Sourced.")
# PROVINCES
pi='<h1>Branches by province</h1><ul>'+''.join(f'<li><a href="{slug(p)}/index.html">{p}</a></li>' for p in PROV)+'</ul>'
page('provinces/index.html',"Smart ID bank branches by province",pi,"Bank branches offering Smart ID services, per South African province.")
PROVBANK={'Eastern Cape':'ecb','Free State':'fsb','Gauteng':'gtb','KwaZulu-Natal':'kznb','Limpopo':'limb','Mpumalanga':'mpub','North West':'nwb','Northern Cape':'ncb','Western Cape':'wcb'}
for p in PROV:
    rows=[b for s in dp for b in dp[s] if b['province']==p]
    b=f'<h1>Smart ID bank branches in {p}</h1><p>{len(rows)} Digital Partnership branches listed in the DHA locator on {D}{src("locator")}. These handle Smart ID re-issues and green ID book conversions{src("digital")}. Check each <a href="../../index.html">bank\'s rules</a> (most require you to be a client).</p>{FILTER}{dptable(rows,showbank=True)}'
    lg=[l for l in leg if l['prov']==p]
    b+=f'<h2>eHomeAffairs bank branches in {p}{src("legacy")}</h2>'
    if lg: b+=f'<p>Apply and book online first. DHA\'s {p} bank-branch page says no walk-ins are allowed at banks{src(PROVBANK[p])}. See <a href="../../booking-and-walk-ins/index.html">Booking and walk-ins</a>.</p><div class="wrap"><table><tr><th>Branch</th><th>City</th><th>Phone (as listed)</th></tr>'+''.join(f'<tr><td>{H.escape(l["name"])}</td><td>{H.escape(l["city"])}</td><td>{l["phone"]}</td></tr>' for l in lg)+'</table></div>'
    else: b+='<p>DHA lists none for this province.</p>'
    page(f'provinces/{slug(p)}/index.html',f"Smart ID bank branches in {p}",b,f"Bank branches in {p} offering Smart ID services, sourced from DHA.")
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
<p>DHA's Digital Partnership page and the partner-branch page both say that, unlike the traditional process, customers do not need to log on to eHomeAffairs to make bookings or payments. You apply through the bank's app, website or branch, then visit a participating branch for identity verification, fingerprints and a photograph. The application goes to Home Affairs for verification, processing and production. You collect the card at the branch you selected, or have it delivered where the bank offers that. Which banks offer delivery: not stated by source{src('digital','locator')}.</p>
<p>DHA says this bank service is currently available for green ID book holders converting to a Smart ID card, re-issues for existing Smart ID card holders, and permanent residents and naturalised citizens from visa-exempt countries (initial phase). The same page, under who can apply, says the first phase focuses on South African citizens converting from the green ID book, re-issues for existing Smart ID card holders, and naturalised citizens and qualifying permanent residents with green ID books{src('digital')}.</p>
<p>Not yet available at these bank branches, on that page: passport applications during phase 1, first-time IDs (for example turning 16), late registration of birth, name changes, amendments to personal details, and complex civic services. Clients who need those must visit a Home Affairs office. DHA also says children cannot apply at these bank branches{src('digital')}.</p>
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
<p>Branch lists and client rules: <a href="../banks/capitec/index.html">Capitec</a>, <a href="../banks/standard-bank/index.html">Standard Bank</a>, <a href="../banks/fnb/index.html">FNB</a>, <a href="../banks/absa/index.html">Absa</a>, <a href="../banks/nedbank/index.html">Nedbank</a>, and <a href="../provinces/index.html">provinces</a>. What to pay and what to carry: <a href="../fees-and-documents/index.html">Fees and documents</a>.</p>'''
page('booking-and-walk-ins/index.html',"Booking a Smart ID: BABS, bank branches and walk-ins",bb,"How to book a South African Smart ID: BABS for Home Affairs offices, eHomeAffairs for older bank branches, and walk-in rules at Digital Partnership banks. Each fact links to an official source.")
def sitemap_loc(path):
    if path=='index.html': return 'https://sa-smart-id-bank-finder.vercel.app/'
    return 'https://sa-smart-id-bank-finder.vercel.app/'+path[:path.rfind('/')+1]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for pth in PATHS:
    sm+=f'  <url><loc>{sitemap_loc(pth)}</loc></url>\n'
sm+='</urlset>\n'
assert '\u2014' not in sm and '\u2013' not in sm
open(f'{OUT}/sitemap.xml','w').write(sm)
robots='User-agent: *\nAllow: /\n\nSitemap: https://sa-smart-id-bank-finder.vercel.app/sitemap.xml\n'
assert '\u2014' not in robots and '\u2013' not in robots
open(f'{OUT}/robots.txt','w').write(robots)
print(total,len(leg),len(PATHS))

