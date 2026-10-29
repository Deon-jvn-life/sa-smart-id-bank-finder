# Smart ID at the Bank (SA)

Independent, unofficial static guide to Smart ID and passport services at South African bank branches. It covers the Department of Home Affairs (DHA) Digital Partnership walk-in model and the older eHomeAffairs booking model: which banks take applications, which branches, what it costs, what to bring, and age rules. Each fact on the pages links to an official DHA, gov.za, or bank page.

This is not affiliated with DHA or any bank. Rules change often. Confirm on the official source before you travel.

Most pages were last checked on 26 October 2026. That date is baked into the generator. The name or surname change page is marked 27 October 2026. The date of birth or gender page is marked 28 October 2026.

## Pages

Guides, bank pages and province pages, plus `robots.txt`. The generator writes every HTML page. Current guides include fees and documents, booking and walk-ins, a lost or stolen Smart ID, a name or surname change, a date of birth or gender correction, a first Smart ID at 16, collecting a Smart ID or passport, the green ID book, and applying for a passport.

- Home (`site/index.html`)
- Fees and documents
- Bank pages: Capitec, Standard Bank, FNB, Absa, Nedbank
- Provinces index, plus one page for each of the nine provinces

On 26 October 2026 the DHA locator listed 700 Digital Partnership branches: Capitec 373, Standard Bank 157, FNB 140, Absa 30. Nedbank was not in that locator. A gov.za statement the same day said the service was live at 669 bank branches. The statement does not explain the difference.

## Sources

Branch data lives in `tools/`:

- `p1.json` Capitec, `p2.json` Standard Bank, `p3.json` FNB, `p4.json` Absa. Each file is a dump of the DHA partner locator (`https://myhomeaffairsonline.dha.gov.za/api/civics/search-partner?partner_id=` with partner ids 1 to 4). Shape: `{ "branches": [ { "branchName", "suburb", "city", "province", "postal_code", "enabledProducts" } ] }`. On 26 October 2026 every branch had `enabledProducts` set to `RE_ISSUE` only.
- `legacy.json`: older eHomeAffairs bank branches taken from the DHA province branch pages. Shape: a list of `{ "page", "name", "city", "phone" }`.
- Nedbank is not in the locator. Its six branches are written in `tools/build.py` from Nedbank's own page.

Narrative facts (fees, walk-in rules, documents, age limits) come from the official URLs listed in the `S` dictionary at the top of `tools/build.py`: DHA pages, gov.za media statements, and each bank's Smart ID page.

## Layout

- `site/` is the finished static site. Vercel serves this folder as the site root. Page files are generated. Rebuild them instead of editing the HTML by hand.
- `tools/build.py` generates `site/`.
- `tools/p1.json`, `tools/p2.json`, `tools/p3.json`, `tools/p4.json`, and `tools/legacy.json` are the raw branch data.

`build.py` reads those JSON files from its own directory and writes HTML to `site/`. That path is the only change from the original generator, so a rebuild still lands in the folder Vercel publishes.

## Rebuild

Python 3 and the standard library are enough. No packages to install.

From the repository root:

```bash
python3 tools/build.py
```

The script prints the Digital Partnership branch count and the eHomeAffairs branch count. It refuses to write a page that contains an em dash or an en dash.

## Deploy on Vercel

Import this Git repository. Use these settings:

| Setting | Value |
| --- | --- |
| Framework Preset | Other |
| Root Directory | `./` (repository root) |
| Build Command | empty (override on, no command) |
| Output Directory | `site` |
| Install Command | empty |

`vercel.json` sets the same values: `framework` is `null` (Other), `buildCommand` and `installCommand` are empty strings so those steps are skipped, and `outputDirectory` is `site`. With framework Other and no build command, Vercel serves `site/` directly.

Pages link to clean paths such as `/fees-and-documents/`. Each page is still a folder with `index.html`, which is what that path serves.
