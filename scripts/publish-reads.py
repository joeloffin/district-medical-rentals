#!/usr/bin/env python3
"""Publish three recovery reads per day and list them on the About page.

Articles dated today or earlier are written to articles/. Later ones stay
unpublished so Google only sees pages that are actually linked.
"""

from __future__ import annotations

import html
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_head as seo  # noqa: E402
from recovery_reads import ARTICLES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "articles"
ABOUT = ROOT / "about.html"
SITEMAP = ROOT / "sitemap.xml"
START = date(2026, 10, 23)
PER_DAY = 3


def publish_date(index: int) -> date:
    return START + timedelta(days=index // PER_DAY)


def due_articles(today: date) -> list[tuple[date, dict]]:
    published = []
    for index, article in enumerate(ARTICLES):
        day = publish_date(index)
        if day <= today:
            published.append((day, article))
    return published


def page_html(day: date, article: dict, related: list[tuple[date, dict]]) -> str:
    title = article["title"]
    description = article["description"]
    path = f"articles/{article['slug']}.html"
    paragraphs = "\n".join(
        f"        <p>{html.escape(paragraph)}</p>" for paragraph in article["paragraphs"]
    )
    related_links = "\n".join(
        "            <li>\n"
        f'              <a href="{html.escape(item["slug"])}.html">{html.escape(item["title"])}</a>\n'
        "            </li>"
        for _, item in related
        if item["slug"] != article["slug"]
    )
    graph = [
        seo.business_entity(),
        {
            "@type": "Article",
            "headline": title,
            "description": description,
            "datePublished": day.isoformat(),
            "dateModified": day.isoformat(),
            "author": {"@id": seo.abs_url("#business")},
            "publisher": {"@id": seo.abs_url("#business")},
            "mainEntityOfPage": seo.abs_url(path),
            "image": seo.abs_url("images/og-image.jpg"),
        },
        seo.breadcrumb(
            [
                ("Home", ""),
                ("About", "about.html"),
                (title, path),
            ]
        ),
    ]
    head = seo.head_block(title=f"{title} | District Medical Rentals", description=description, path=path, graph=graph)
    pretty_date = f"{day.strftime('%B')} {day.day}, {day.year}"
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
{head}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Sora:wght@500;600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="icon" type="image/png" sizes="192x192" href="https://districtmedicalrentals.com/images/favicon-192.png" />
    <link rel="icon" href="https://districtmedicalrentals.com/favicon.ico" sizes="48x48" />
    <link rel="apple-touch-icon" href="https://districtmedicalrentals.com/apple-touch-icon.png" />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="header-inner">
        <a class="brand brand-with-logo" href="../index.html">
          <img class="header-logo" src="../images/logo.webp" alt="" width="72" height="82" />
          <span>District Medical Rentals</span>
        </a>
        <nav class="nav" aria-label="Primary">
          <a href="../index.html">Home</a>
          <a href="../about.html" aria-current="page">About</a>
          <a href="../rates.html">Rates</a>
          <a href="../contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main id="main" class="page page-centered">
      <header class="page-header">
        <p class="eyebrow">Reads on recovery</p>
        <h1>{html.escape(title)}</h1>
        <p><time datetime="{day.isoformat()}">{pretty_date}</time></p>
      </header>
      <article class="article-body">
{paragraphs}
        <p class="article-note">
          General information for home recovery, not medical advice. Follow the instructions
          from your surgeon or therapist. District Medical Rentals delivers medical-grade lift
          recliners and electronic hospital beds in Washington, DC, Maryland, and Virginia.
        </p>
        <div class="article-links">
          <a class="btn btn-primary" href="../contact.html">Book Now</a>
          <a class="btn btn-outline" href="../rates.html">See rates</a>
        </div>
        <div class="article-note">
          <p>More reads</p>
          <ul class="reads-list">
{related_links}
          </ul>
        </div>
      </article>
    </main>

    <footer class="site-footer">
      <img class="footer-logo" src="../images/logo.webp" alt="District Medical Rentals logo" width="120" height="136" />
      <p class="footer-brand">District Medical Rentals</p>
      <p>Medical-grade lift chairs and beds delivered in DC, Maryland, and Virginia.</p>
      <p><a href="tel:+19173465309">917-346-5309</a></p>
      <nav class="footer-nav" aria-label="Footer">
        <a href="../index.html">Home</a>
        <a href="../about.html">About</a>
        <a href="../rates.html">Rates</a>
        <a href="../contact.html">Contact</a>
        <a href="../locations.html">Locations</a>
        <a href="../privacy.html">Privacy Policy</a>
      </nav>
    </footer>
    <a class="sticky-call" href="../contact.html">Book Now</a>
  </body>
</html>
"""


def about_block(published: list[tuple[date, dict]]) -> str:
    items = []
    for day, article in reversed(published):
        pretty = f"{day.strftime('%B')} {day.day}, {day.year}"
        items.append(
            "            <li>\n"
            f'              <a href="articles/{html.escape(article["slug"])}.html">{html.escape(article["title"])}</a>\n'
            f'              <time datetime="{day.isoformat()}">{pretty}</time>\n'
            "            </li>"
        )
    listing = "\n".join(items)
    return f"""<!-- reads:start -->
        <section class="about-block" id="reads" aria-labelledby="reads-heading">
          <details class="reads-fold">
            <summary id="reads-heading">Reads on recovery</summary>
            <ul class="reads-list">
{listing}
            </ul>
          </details>
        </section>
        <!-- reads:end -->"""


def update_about(published: list[tuple[date, dict]]) -> None:
    text = ABOUT.read_text(encoding="utf-8")
    block = about_block(published)
    updated, count = re.subn(
        r"<!-- reads:start -->.*?<!-- reads:end -->",
        block,
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("Could not find the reads block in about.html")
    ABOUT.write_text(updated, encoding="utf-8")


def update_sitemap(published: list[tuple[date, dict]]) -> None:
    text = SITEMAP.read_text(encoding="utf-8")
    base = seo.base_url()
    existing = set(re.findall(r"<loc>(.*?)</loc>", text))
    inserts = []
    for day, article in published:
        loc = f"{base}/articles/{article['slug']}.html"
        if loc in existing:
            continue
        inserts.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{day.isoformat()}</lastmod>\n"
            "  </url>\n"
        )
    if not inserts:
        return
    if "</urlset>" not in text:
        raise SystemExit("sitemap.xml is missing </urlset>")
    text = text.replace("</urlset>", "".join(inserts) + "</urlset>", 1)
    SITEMAP.write_text(text, encoding="utf-8")


def main() -> None:
    today = date.today()
    published = due_articles(today)
    ARTICLES_DIR.mkdir(exist_ok=True)
    written = 0
    for day, article in published:
        target = ARTICLES_DIR / f"{article['slug']}.html"
        same_day = [(d, item) for d, item in published if d == day]
        target.write_text(page_html(day, article, same_day), encoding="utf-8")
        written += 1
    # Remove anything published ahead of schedule if the clock moved backward.
    live_slugs = {article["slug"] for _, article in published}
    for path in ARTICLES_DIR.glob("*.html"):
        if path.stem not in live_slugs:
            path.unlink()
    update_about(published)
    update_sitemap(published)
    remaining = len(ARTICLES) - len(published)
    print(f"Live recovery reads: {written}. Still scheduled: {remaining}.")


if __name__ == "__main__":
    main()
