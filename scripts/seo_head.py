#!/usr/bin/env python3
"""Shared SEO <head> tags and JSON-LD for District Medical Rentals pages.

Run directly to refresh the SEO block in the hand-written top-level pages:
    python3 scripts/seo_head.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "site.config.json"

BUSINESS_NAME = "District Medical Rentals"
PHONE = "+1-917-346-5309"
THEME_COLOR = "#0b3a66"


def base_url() -> str:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))["baseUrl"].rstrip("/")
    return "https://YOUR_USERNAME.github.io/district-medical-rentals"


def abs_url(path: str) -> str:
    return f"{base_url()}/{path.lstrip('/')}"


def offer(name: str, price: int) -> dict:
    return {
        "@type": "Offer",
        "itemOffered": {"@type": "Service", "name": name},
        "priceCurrency": "USD",
        "price": f"{price}.00",
        "priceSpecification": {
            "@type": "UnitPriceSpecification",
            "price": f"{price}.00",
            "priceCurrency": "USD",
            "unitText": "week",
            "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "WEE"},
            "description": (
                "Starting weekly rate. Discounts on rentals longer than 4 weeks; save 10% when "
                "renting two or more items together. No deposit."
            ),
        },
    }


def business_entity() -> dict:
    return {
        "@type": "MedicalBusiness",
        "@id": abs_url("#business"),
        "name": BUSINESS_NAME,
        "url": abs_url(""),
        "logo": abs_url("images/logo.png"),
        "image": abs_url("images/og-image.jpg"),
        "telephone": PHONE,
        "priceRange": "$$",
        "description": (
            "Medical-grade lift chairs, sit-to-stand patient lifts, and electronic medical beds "
            "delivered to homes in Washington DC, Maryland, and Virginia."
        ),
        "areaServed": [
            {"@type": "City", "name": "Washington, DC"},
            {"@type": "State", "name": "Maryland"},
            {"@type": "State", "name": "Virginia"},
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Home recovery equipment rentals",
            "itemListElement": [
                offer("Medical-grade lift chair rental", 125),
                offer("Sit-to-stand patient lift rental", 140),
                offer("Hospital bed rental", 240),
            ],
        },
    }


def website_entity() -> dict:
    return {
        "@type": "WebSite",
        "@id": abs_url("#website"),
        "url": abs_url(""),
        "name": BUSINESS_NAME,
        "publisher": {"@id": abs_url("#business")},
    }


def breadcrumb(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": abs_url(path)}
            for i, (name, path) in enumerate(items, start=1)
        ],
    }


def _clean(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return re.sub(r"\s+([.,])", r"\1", text)


def faq_entity(page_html: str) -> dict | None:
    pairs = re.findall(
        r'<details class="faq-item">\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>',
        page_html,
        re.S,
    )
    if not pairs:
        return None
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": _clean(q),
                "acceptedAnswer": {"@type": "Answer", "text": _clean(a)},
            }
            for q, a in pairs
        ],
    }


def jsonld(graph: list[dict]) -> str:
    data = {"@context": "https://schema.org", "@graph": [g for g in graph if g]}
    body = json.dumps(data, indent=2, ensure_ascii=False)
    body = "\n".join("      " + line for line in body.splitlines())
    return f'    <script type="application/ld+json">\n{body}\n    </script>'


def head_block(
    *,
    title: str,
    description: str,
    path: str,
    graph: list[dict],
    robots: str = "index,follow",
) -> str:
    url = abs_url(path)
    t = html.escape(title, quote=True)
    d = html.escape(description, quote=True)
    image = abs_url("images/og-image.jpg")
    lines = [
        "    <!-- seo:start -->",
        f"    <title>{t}</title>",
        f'    <meta name="description" content="{d}" />',
        f'    <meta name="robots" content="{robots}" />',
        f'    <link rel="canonical" href="{url}" />',
        f'    <meta name="theme-color" content="{THEME_COLOR}" />',
        '    <meta property="og:type" content="website" />',
        f'    <meta property="og:site_name" content="{BUSINESS_NAME}" />',
        '    <meta property="og:locale" content="en_US" />',
        f'    <meta property="og:title" content="{t}" />',
        f'    <meta property="og:description" content="{d}" />',
        f'    <meta property="og:url" content="{url}" />',
        f'    <meta property="og:image" content="{image}" />',
        '    <meta property="og:image:width" content="1200" />',
        '    <meta property="og:image:height" content="630" />',
        f'    <meta property="og:image:alt" content="{BUSINESS_NAME} logo over a lift chair" />',
        '    <meta name="twitter:card" content="summary_large_image" />',
        f'    <meta name="twitter:title" content="{t}" />',
        f'    <meta name="twitter:description" content="{d}" />',
        f'    <meta name="twitter:image" content="{image}" />',
        jsonld(graph),
        "    <!-- seo:end -->",
    ]
    return "\n".join(lines)


PAGES = {
    "index.html": {
        "title": "Lift Chair & Medical Bed Rentals in DC, MD & VA | District Medical Rentals",
        "description": (
            "Rent medical-grade lift chairs, sit-to-stand lifts, and electronic medical beds delivered to your home in "
            "Washington DC, Maryland, and Virginia. Lift chairs from $125/week. Call 917-346-5309."
        ),
        "path": "",
        "crumbs": None,
        "business": True,
    },
    "about.html": {
        "title": "About Us | Home Recovery Equipment Rentals in DC, MD & VA",
        "description": (
            "District Medical Rentals is a local DC-area team renting clean, medical-grade lift "
            "chairs, sit-to-stand lifts, and electronic medical beds for recovery at home in Maryland, Virginia, and DC."
        ),
        "path": "about.html",
        "crumbs": [("Home", ""), ("About", "about.html")],
    },
    "rates.html": {
        "title": "Lift Chair, Sit-to-Stand & Medical Bed Rental Prices | District Medical Rentals",
        "description": (
            "Lift recliners from $125/week, sit-to-stand lifts from $140/week, hospital beds from $240/week. "
            "Save 10% when you rent two or more. No deposit. Delivery in DC, Maryland, and Virginia."
        ),
        "path": "rates.html",
        "crumbs": [("Home", ""), ("Rates", "rates.html")],
        "business": True,
    },
    "contact.html": {
        "title": "Book a Lift Chair, Sit-to-Stand Lift, or Medical Bed | District Medical Rentals",
        "description": (
            "Request a lift chair, sit-to-stand patient lift, or medical bed rental delivered in DC, Maryland, or Virginia. "
            "Send a quick form or call 917-346-5309 and we’ll confirm your delivery."
        ),
        "path": "contact.html",
        "crumbs": [("Home", ""), ("Contact", "contact.html")],
    },
    "privacy.html": {
        "title": "Privacy Policy | District Medical Rentals",
        "description": (
            "How District Medical Rentals collects, uses, and protects the information you share "
            "when requesting a lift chair or medical bed rental."
        ),
        "path": "privacy.html",
        "crumbs": [("Home", ""), ("Privacy Policy", "privacy.html")],
    },
}


def build_graph(page_html: str, *, business: bool, crumbs) -> list[dict]:
    graph: list[dict] = []
    if business:
        graph += [business_entity(), website_entity()]
    if crumbs:
        graph.append(breadcrumb(crumbs))
    graph.append(faq_entity(page_html))
    return graph


def apply(page_html: str, block: str) -> str:
    """Replace the existing SEO block (or the old title/description tags) with `block`."""
    if "<!-- seo:start -->" in page_html:
        return re.sub(r"    <!-- seo:start -->.*?<!-- seo:end -->", lambda _: block, page_html, flags=re.S)
    page_html = re.sub(r'\s*<meta\s+name="description"\s+content="[^"]*"\s*/>', "", page_html, flags=re.S)
    page_html = re.sub(r'\s*<meta name="robots"[^>]*/>', "", page_html)
    page_html = re.sub(r'\s*<link rel="canonical"[^>]*/>', "", page_html)
    page_html = re.sub(r"\s*<title>.*?</title>", "", page_html, flags=re.S)
    page_html = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", page_html, flags=re.S)
    return re.sub(
        r'(<meta name="viewport"[^>]*/>)',
        lambda m: m.group(1) + "\n" + block,
        page_html,
        count=1,
    )


def main() -> None:
    for name, cfg in PAGES.items():
        path = ROOT / name
        src = path.read_text(encoding="utf-8")
        graph = build_graph(src, business=cfg.get("business", False), crumbs=cfg["crumbs"])
        block = head_block(
            title=cfg["title"], description=cfg["description"], path=cfg["path"], graph=graph
        )
        path.write_text(apply(src, block), encoding="utf-8")
        print(f"SEO head updated: {name}")


if __name__ == "__main__":
    main()
