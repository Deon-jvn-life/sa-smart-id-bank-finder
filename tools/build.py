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
main{max-width:960px;margin:0 auto;padding:16px}h1{font-size:1.6rem;line-height:1.25}h2{font-size:1.25rem;margin-top:1.8em}
.card{background:#fff;border:1px solid #e3e6ea;border-radius:10px;padding:14px 16px;margin:12px 0}.note{background:#fff8e1;border-color:#f3d27a}
.src{font-size:12px;color:#5a6472}.src a{color:#5a6472}a{color:#0b5d3b}table{border-collapse:collapse;width:100%;background:#fff;font-size:14px}
th,td{border:1px solid #e3e6ea;padding:6px 8px;text-align:left;vertical-align:top}th{background:#eef2f0}.wrap{overflow-x:auto}
.checked{font-size:13px;color:#5a6472;margin:0 0 8px}footer{max-width:960px;margin:24px auto;padding:16px;font-size:13px;color:#5a6472}
input{width:100%;padding:8px;font-size:15px;border:1px solid #cdd3da;border-radius:6px;margin:8px 0}ul.grid{columns:2;padding-left:18px}@media(max-width:600px){ul.grid{columns:1}}"""
def page(path,title,body,desc):
    depth=path.count('/')
    r='../'*depth
    navl=f'<a href="{r}index.html">Home</a><a href="{r}fees-and-documents/index.html">Fees and documents</a>'+''.join(f'<a href="{r}banks/{s}/index.html">{n}</a>' for _,n,s in BANKS)+f'<a href="{r}provinces/index.html">Provinces</a>'
    h=f'''<!doctype html><html lang="en-ZA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{H.escape(title)}</title><meta name="description" content="{H.escape(desc)}"><style>{CSS}</style></head><body>
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
("Do I need an appointment?",f"Depends on the model. DHA says Capitec and Standard Bank allow walk-ins without an appointment at Digital Partnership branches{src('digital')}. FNB says no appointment is needed to replace a Smart ID{src('fnb')}. Absa offers booking online, in its app, or walking in{src('absa')}. For the older eHomeAffairs bank branches, DHA states no walk-ins are allowed{src('legacy')}."),
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
("Nedbank","nedbank",f"Booking via eHomeAffairs{src('ned')}; DHA: no walk-ins at eHomeAffairs bank branches{src('legacy')}",f"Payment described via Nedbank app or Online Banking{src('ned')}; other options not stated by source","Not stated by source")]
for n,s,w,c,f in rowsb:
    cnt=f"{counts[s]}{src('locator')}" if s in counts else f"Not listed in DHA locator{src('locator')}"
    banktbl+=f'<tr><td><a href="banks/{s}/index.html">{n}</a></td><td>{cnt}</td><td>{w}</td><td>{c}</td><td>{f}</td></tr>'
banktbl+='</table></div>'
body=f'''<h1>Smart ID and passport services at South African bank branches</h1>
<p>A plain, sourced guide to which bank branches can take your Smart ID (and in some cases passport) application, what to bring, and what it costs.</p>
<div class="card"><strong>Two different systems exist.</strong><ol>
<li><strong>DHA Digital Partnership</strong> (since 9 March 2026{src('golive')}): bank staff process the application through a secure link to DHA. Currently for green ID book to Smart ID conversion and Smart ID re-issues only{src('digital')}. DHA's live locator lists the branches{src('locator','locms')}.</li>
<li><strong>Older eHomeAffairs bank branches</strong>: apply and pay online at eHomeAffairs, book a slot, then visit a branch hosting DHA for fingerprints and photo. DHA states no walk-ins are allowed at these{src('legacy')}.</li></ol></div>
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
<div class="card"><strong>eHomeAffairs bank branches (booking model)</strong><p>FNB: bring original identity documents such as green ID book, passport or birth certificate, also when collecting{src('fnb')}. Nedbank: bring your booking confirmation and ID book or card{src('ned')}. Standard Bank: print and keep your booking confirmation letter and reference number, visit with your ID{src('sb')}.</p></div>
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
    b=f'<h1>{n}: Smart ID and passport at branches</h1><div class="card">{info[s]}</div>'
    if s in dp:
        b+=f'<h2>{n} Digital Partnership branches ({len(dp[s])}){src("locator")}</h2><p>Data from the DHA partner branch locator on {D}. Confirm before visiting.</p>{FILTER}{dptable(dp[s],showprov=True)}'
    lg=[l for l in leg if l['name'].upper().startswith(n.upper().split()[0])]
    if lg:
        b+=f'<h2>{n} eHomeAffairs bank branches listed by DHA{src("legacy")}</h2><p>Booking required; DHA states no walk-ins.</p><div class="wrap"><table><tr><th>Branch</th><th>City</th><th>Province</th><th>Phone (as listed)</th></tr>'+''.join(f'<tr><td>{H.escape(l["name"])}</td><td>{H.escape(l["city"])}</td><td>{l["prov"]}</td><td>{l["phone"]}</td></tr>' for l in lg)+'</table></div>'
    page(f'banks/{s}/index.html',f"{n} Smart ID and passport branches: walk-in, fees, rules",b,f"{n} Smart ID and passport branch service: walk-in or booking, client requirement, fees, branch list. Sourced.")
# PROVINCES
pi='<h1>Branches by province</h1><ul>'+''.join(f'<li><a href="{slug(p)}/index.html">{p}</a></li>' for p in PROV)+'</ul>'
page('provinces/index.html',"Smart ID bank branches by province",pi,"Bank branches offering Smart ID services, per South African province.")
for p in PROV:
    rows=[b for s in dp for b in dp[s] if b['province']==p]
    b=f'<h1>Smart ID bank branches in {p}</h1><p>{len(rows)} Digital Partnership branches listed in the DHA locator on {D}{src("locator")}. These handle Smart ID re-issues and green ID book conversions{src("digital")}. Check each <a href="../../index.html">bank\'s rules</a> (most require you to be a client).</p>{FILTER}{dptable(rows,showbank=True)}'
    lg=[l for l in leg if l['prov']==p]
    b+=f'<h2>eHomeAffairs bank branches in {p}{src("legacy")}</h2>'
    if lg: b+='<p>Apply and book online first. DHA: no walk-ins.</p><div class="wrap"><table><tr><th>Branch</th><th>City</th><th>Phone (as listed)</th></tr>'+''.join(f'<tr><td>{H.escape(l["name"])}</td><td>{H.escape(l["city"])}</td><td>{l["phone"]}</td></tr>' for l in lg)+'</table></div>'
    else: b+='<p>DHA lists none for this province.</p>'
    page(f'provinces/{slug(p)}/index.html',f"Smart ID bank branches in {p}",b,f"Bank branches in {p} offering Smart ID services, sourced from DHA.")
open(f'{OUT}/robots.txt','w').write('User-agent: *\nAllow: /\n')
print(total,len(leg))
