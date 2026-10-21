# District Medical Rentals

Website for District Medical Rentals — medical-grade lift chairs and electronic medical beds delivered across Washington, DC, Maryland, and Virginia.

## Pages

- `index.html` — Home
- `about.html` — Company story, values, and how renting works
- `rates.html` — Weekly pricing
- `contact.html` — Contact form with notes
- `privacy.html` — Privacy Policy
- `locations.html` — Index of all local SEO landing pages
- `locations/*.html` — Lift chair rental pages by county/city (generated)
- `sitemap.xml` / `robots.txt` — SEO crawl files

## Generate location SEO pages

```bash
python3 scripts/generate-locations.py
```

Set your live site URL in `site.config.json` (`baseUrl`) before deploying so the sitemap is correct.

## SEO tags and structured data

Titles, descriptions, canonical URLs, social share tags, and JSON-LD for the top-level pages live in
`scripts/seo_head.py`. After editing page titles, FAQs, or prices, refresh everything with:

```bash
python3 scripts/seo_head.py && python3 scripts/generate-locations.py
```

## Open locally

Open `index.html` in a browser, or from this folder run:

```bash
python3 -m http.server 5173
```

Then visit [http://localhost:5173](http://localhost:5173).

## Contact

Phone on site: **917-346-5309**

Rental requests from the contact form are emailed to **offin.joel@gmail.com** via [FormSubmit](https://formsubmit.co) (standard form POST).

**First-time setup:** submit the form once from `http://localhost:...` (not a `file://` page), then check that inbox (and spam) for FormSubmit’s activation email and confirm it. After that, new requests go straight to Gmail.
