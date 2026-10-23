# Page backlog

Running list of candidate pages for this site. One useful page per nightly run, and only when official DHA, gov.za, eHomeAffairs or bank pages support it. If a night cannot be sourced properly, record the skip here and do not publish a thin page.

The generator is `tools/build.py`. Pages in `site/` are built from it. Do not hand-edit the HTML.

## Already on the site before 22 October 2026

- Home
- Fees and documents
- Banks: Capitec, Standard Bank, FNB, Absa, Nedbank
- Provinces index and all nine provinces

## Night log

- 22 October 2026: shipped **Booking a Smart ID: BABS, bank branches and walk-ins** at `booking-and-walk-ins/`. Chosen because the site only had a short "do I need an appointment?" answer and did not explain that DHA's Branch Appointment Booking System books a Home Affairs office, while bank visits use either the bank's own Digital Partnership process or eHomeAffairs. Checked against `fees-and-documents`: that page is tariffs, documents and age rules, not the booking steps. Sources were limited to dha.gov.za (including the BABS notice, the Digital Partnership page, the 2023/24 annual report, the December 2025 festive-season statement, and the nine province bank-branch pages), services.dha.gov.za, myhomeaffairsonline.dha.gov.za, the eHomeAffairs how-to PDF, and the five banks' own Smart ID pages.
- 22 October 2026 (night run, logged on the ET date; the generator run fell after midnight UTC on 23 October): shipped **Replacing a lost or stolen Smart ID** at `lost-or-stolen-smart-id/`. Chosen over the 16-year-old page because first-issue documents for youth 16 and older are already on `fees-and-documents`, while no page set out a lost, stolen or damaged re-issue. The civic identity documents page requires a copy of the old, lost or damaged Smart ID card, or an affidavit, and the Digital Partnership page says the same lost, stolen or damaged re-issue needs no documents at a bank. Police reporting is stated by Nedbank (report a lost card to the police), by the August 2013 Vuk'uzenzele answer (a police case number and affidavit if you lose the ID after applying), and by the 2013 duplicate-ID notice (a police affidavit, for that notice only). Capitec, Standard Bank, FNB, Absa, the current identity documents page, and the Digital Partnership page do not state a police report. Checked against `fees-and-documents` (tariffs and the first-issue brochure), `booking-and-walk-ins` (how you book or walk in), and the five bank pages (each bank's own steps): this page only compares the replacement rules. Sources: dha.gov.za identity documents page, fees page, Digital Partnership page, Smart ID requirements brochure, and duplicate-ID notice; gov.za identity-document service page, affidavit FAQ, and the 18 May 2011 temporary identity certificate statement; vukuzenzele.gov.za August 2013 Smart ID FAQ; Capitec, Standard Bank, FNB, Absa and Nedbank Smart ID pages.

## Candidates

### City and metro branch pages

These would group branches already listed on the province pages. Not chosen on 22 October 2026 because a reader can already filter a province page, and no official city-level rule (different from the province) was needed for tonight's gap.

- [ ] Johannesburg
- [ ] Cape Town
- [ ] Durban
- [ ] Pretoria
- [ ] Gqeberha

### How-to pages people keep asking about

- [x] Booking on DHA's Branch Appointment Booking System, versus a bank visit, and whether walk-ins are accepted (22 October 2026)
- [ ] First Smart ID for 16-year-olds, and applications for minors
- [x] Replacing a lost or stolen ID (what DHA and each bank require, including police reporting where a source states it) (22 October 2026)
- [ ] Collecting a Smart ID or passport (who may collect, what to bring, bank versus Home Affairs office)
- [ ] What to bring, and how payment works. Partly covered by fees-and-documents and by the bank pages. Ship a separate page only if a later check finds a recurring question those pages do not answer.

### Per-bank step-by-step pages

The bank pages and the booking page already carry the published steps. A further page is worth doing only if it adds a sourced step those pages do not.

- [ ] Capitec, in-branch visit only
- [ ] Standard Bank, in-branch walk-in versus the online Home Affairs route
- [ ] FNB, Smart ID replacement versus eHomeAffairs
- [ ] Absa, online portal, app and walk-in
- [ ] Nedbank, eHomeAffairs only

## Skipped

None yet.
