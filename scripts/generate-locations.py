#!/usr/bin/env python3
"""Generate SEO location landing pages for lift chair rentals."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "locations"
CONFIG_PATH = ROOT / "site.config.json"

MD_COUNTIES = [
    "Allegany County",
    "Anne Arundel County",
    "Baltimore County",
    "Baltimore City",
    "Calvert County",
    "Caroline County",
    "Carroll County",
    "Cecil County",
    "Charles County",
    "Dorchester County",
    "Frederick County",
    "Garrett County",
    "Harford County",
    "Howard County",
    "Kent County",
    "Montgomery County",
    "Prince George's County",
    "Queen Anne's County",
    "Somerset County",
    "St. Mary's County",
    "Talbot County",
    "Washington County",
    "Wicomico County",
    "Worcester County",
]

VA_COUNTIES = [
    "Accomack County",
    "Albemarle County",
    "Alleghany County",
    "Amelia County",
    "Amherst County",
    "Appomattox County",
    "Arlington County",
    "Augusta County",
    "Bath County",
    "Bedford County",
    "Bland County",
    "Botetourt County",
    "Brunswick County",
    "Buchanan County",
    "Buckingham County",
    "Campbell County",
    "Caroline County",
    "Carroll County",
    "Charles City County",
    "Charlotte County",
    "Chesterfield County",
    "Clarke County",
    "Craig County",
    "Culpeper County",
    "Cumberland County",
    "Dickenson County",
    "Dinwiddie County",
    "Essex County",
    "Fairfax County",
    "Fauquier County",
    "Floyd County",
    "Fluvanna County",
    "Franklin County",
    "Frederick County",
    "Giles County",
    "Gloucester County",
    "Goochland County",
    "Grayson County",
    "Greene County",
    "Greensville County",
    "Halifax County",
    "Hanover County",
    "Henrico County",
    "Henry County",
    "Highland County",
    "Isle of Wight County",
    "James City County",
    "King and Queen County",
    "King George County",
    "King William County",
    "Lancaster County",
    "Lee County",
    "Loudoun County",
    "Louisa County",
    "Lunenburg County",
    "Madison County",
    "Mathews County",
    "Mecklenburg County",
    "Middlesex County",
    "Montgomery County",
    "Nelson County",
    "New Kent County",
    "Northampton County",
    "Northumberland County",
    "Nottoway County",
    "Orange County",
    "Page County",
    "Patrick County",
    "Pittsylvania County",
    "Powhatan County",
    "Prince Edward County",
    "Prince George County",
    "Prince William County",
    "Pulaski County",
    "Rappahannock County",
    "Richmond County",
    "Roanoke County",
    "Rockbridge County",
    "Rockingham County",
    "Russell County",
    "Scott County",
    "Shenandoah County",
    "Smyth County",
    "Southampton County",
    "Spotsylvania County",
    "Stafford County",
    "Surry County",
    "Sussex County",
    "Tazewell County",
    "Warren County",
    "Washington County",
    "Westmoreland County",
    "Wise County",
    "Wythe County",
    "York County",
]

VA_CITIES = [
    "Alexandria",
    "Bristol",
    "Buena Vista",
    "Charlottesville",
    "Chesapeake",
    "Colonial Heights",
    "Covington",
    "Danville",
    "Emporia",
    "Fairfax",
    "Falls Church",
    "Franklin",
    "Fredericksburg",
    "Galax",
    "Hampton",
    "Harrisonburg",
    "Hopewell",
    "Lexington",
    "Lynchburg",
    "Manassas",
    "Manassas Park",
    "Martinsville",
    "Newport News",
    "Norfolk",
    "Norton",
    "Petersburg",
    "Poquoson",
    "Portsmouth",
    "Radford",
    "Richmond",
    "Roanoke",
    "Salem",
    "Staunton",
    "Suffolk",
    "Virginia Beach",
    "Waynesboro",
    "Williamsburg",
    "Winchester",
]


def slugify(text: str) -> str:
    text = text.lower().replace("&", "and").replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_locations() -> list[dict]:
    locations = [
        {
            "name": "Washington, DC",
            "short": "Washington, DC",
            "state": "DC",
            "state_name": "Washington, DC",
            "kind": "city",
            "slug": "washington-dc",
        }
    ]

    for name in MD_COUNTIES:
        short = name.replace(" County", "").replace(" City", " City")
        locations.append(
            {
                "name": name,
                "short": short,
                "state": "MD",
                "state_name": "Maryland",
                "kind": "city" if "City" in name else "county",
                "slug": f"{slugify(name)}-md",
            }
        )

    for name in VA_COUNTIES:
        short = name.replace(" County", "")
        locations.append(
            {
                "name": name,
                "short": short,
                "state": "VA",
                "state_name": "Virginia",
                "kind": "county",
                "slug": f"{slugify(name)}-va",
            }
        )

    for name in VA_CITIES:
        locations.append(
            {
                "name": name,
                "short": name,
                "state": "VA",
                "state_name": "Virginia",
                "kind": "city",
                "slug": f"{slugify(name)}-va",
            }
        )

    return locations


def page_html(loc: dict) -> str:
    place = loc["name"]
    short = loc["short"]
    state = loc["state"]
    label = f"{place}, {state}" if state != "DC" else place
    in_place = place if state == "DC" else f"{place}, {state}"

    title = f"District Medical Rentals | Rent a lift chair in {in_place} delivered to you"
    description = (
        f"Lift chair rental in {in_place}. District Medical Rentals delivers medical-grade "
        f"lift chairs and electronic medical beds for post-surgery recovery at home."
    )
    h1 = f"Rent a lift chair in {in_place} — delivered to you"
    lead = (
        f"Medical-grade lift chair and electronic bed rentals in {in_place}. "
        "Clean equipment for safer recovery at home."
    )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{description}" />
    <meta name="robots" content="index,follow" />
    <link rel="canonical" href="../locations/{loc['slug']}.html" />
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Sora:wght@500;600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="icon" href="../favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" sizes="32x32" href="../images/favicon-32.png" />
    <link rel="apple-touch-icon" href="../apple-touch-icon.png" />
    <link rel="stylesheet" href="../styles.css" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "District Medical Rentals",
        "description": "{description}",
        "url": "../locations/{loc['slug']}.html",
        "telephone": "+1-917-346-5309",
        "areaServed": "{label}",
        "makesOffer": {{
          "@type": "Offer",
          "itemOffered": {{
            "@type": "Service",
            "name": "Lift chair rental in {in_place}",
            "areaServed": "{label}"
          }}
        }}
      }}
    </script>
  </head>
  <body>
    <header class="site-header">
      <div class="header-inner">
        <a class="brand" href="../index.html">District Medical Rentals</a>
        <nav class="nav" aria-label="Primary">
          <a href="../index.html">Home</a>
          <a href="../about.html">About</a>
          <a href="../rates.html">Rates</a>
          <a href="../contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main id="main">
      <section class="hero" id="top" aria-labelledby="hero-heading">
        <div class="hero-media" role="img" aria-label="Medical-grade lift chair rental in {in_place}">
          <img
            src="../images/hero-lift-chair.png"
            alt="Woman standing from a medical-grade power lift recliner with a cane at home"
            width="1200"
            height="1600"
          />
        </div>
        <div class="hero-copy">
          <img
            class="hero-logo"
            src="../images/logo.png"
            alt="District Medical Supplies"
            width="280"
            height="320"
          />
          <p class="delivery-kicker hero-kicker">Lift chair rental · {short}</p>
          <h1 id="hero-heading">{h1}</h1>
          <p class="hero-lead">{lead}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="../contact.html">Book Now</a>
          </div>
        </div>
      </section>

      <section class="quote-band" aria-label="Why rent with us">
        <blockquote>
          <p>
            Save on expensive medical equipment—borrow clean, medical-grade lift chairs with easy
            delivery in {in_place}.
          </p>
        </blockquote>
      </section>

      <section class="section" id="products" aria-labelledby="products-heading">
        <div class="section-intro">
          <h2 id="products-heading">Lift chair &amp; bed rentals in {short}</h2>
          <p>
            We deliver medical-grade equipment across {loc['state_name']}—including {place}—
            so you can recover safely at home without buying.
          </p>
        </div>

        <div class="product-grid">
          <article class="product">
            <div class="product-visual product-visual-chairs">
              <img
                src="../images/lift-chair-1.png"
                alt="Man using a medical-grade lift chair to stand safely at home"
                width="900"
                height="600"
              />
              <img
                src="../images/lift-chair-2.png"
                alt="Woman standing with help from a gray power lift recliner"
                width="900"
                height="1200"
              />
              <img
                src="../images/lift-chair-3.png"
                alt="Couple at home with a reclined medical-grade lift chair"
                width="900"
                height="600"
              />
            </div>
            <div class="product-copy">
              <h3>Medical-grade lift chairs</h3>
              <p>
                Power lift chairs that help you stand and sit safely—ideal after surgery or for
                limited mobility. Available for rental delivery in {in_place}.
              </p>
            </div>
          </article>

          <article class="product">
            <div class="product-visual">
              <img
                src="../images/medical-bed-1.png"
                alt="Caregiver helping a patient in an adjustable electronic medical bed at home"
                width="900"
                height="600"
              />
              <img
                src="../images/medical-bed-2.png"
                alt="Woman sitting up in a home medical bed with a visitor beside her"
                width="900"
                height="600"
              />
            </div>
            <div class="product-copy">
              <h3>Electronic medical beds</h3>
              <p>
                Adjustable beds that raise the head and feet for comfort and safer rest during
                recovery. Delivered to homes in {in_place}.
              </p>
            </div>
          </article>
        </div>
      </section>

      <section class="section delivery-section" id="service-area" aria-labelledby="area-heading">
        <div class="delivery-layout">
          <div class="delivery-copy">
            <p class="delivery-kicker">Serving {short}</p>
            <h2 id="area-heading">Lift chair rental delivered in {in_place}</h2>
            <p>
              District Medical Rentals helps families and individuals in {in_place} recover
              comfortably at home with reliable medical-grade lift chair and bed rentals.
            </p>
            <h3 class="delivery-serving">Also serving Virginia, Maryland &amp; Washington, DC</h3>
            <p class="delivery-outside">
              Outside this area?
              <a href="tel:+19173465309">Call us at 917-346-5309</a>
              — we may still be able to help.
            </p>
            <p class="delivery-outside">
              <a href="../locations.html">Browse all delivery locations</a>
            </p>
          </div>
        </div>
      </section>

      <section class="section faq-section" id="faq" aria-labelledby="faq-heading">
        <div class="section-intro">
          <h2 id="faq-heading">Common questions</h2>
        </div>
        <div class="faq-list">
          <details class="faq-item">
            <summary>Can I rent a lift chair in {in_place}?</summary>
            <p>
              Yes. We deliver medical-grade lift chairs and electronic medical beds to
              {in_place}. Call 917-346-5309 or book online.
            </p>
          </details>
          <details class="faq-item">
            <summary>Do your rental chairs help you stand while recovering?</summary>
            <p>
              Yes. Our medical-grade lift chairs gently help you stand up and sit down for safer
              recovery at home.
            </p>
          </details>
          <details class="faq-item">
            <summary>Why rent a lift chair after surgery?</summary>
            <p>
              Get the support you need in {short} without buying an expensive chair. We deliver
              clean equipment and pick it up when you’re done.
            </p>
          </details>
          <details class="faq-item">
            <summary>What’s your pricing?</summary>
            <p>
              Medical-grade lift chairs are <strong>$125 per week</strong>. Medical rental beds
              are <strong>$240 per week</strong>. See our
              <a href="../rates.html">rates page</a>.
            </p>
          </details>
          <details class="faq-item">
            <summary>How do I book delivery in {short}?</summary>
            <p>
              Call <a href="tel:+19173465309">917-346-5309</a> or use our
              <a href="../contact.html">contact form</a>. We’ll confirm what you need and your
              drop-off details.
            </p>
          </details>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <img class="footer-logo" src="../images/logo.png" alt="District Medical Supplies" width="120" height="136" />
      <p class="footer-brand">District Medical Rentals</p>
      <p>Lift chair rental in {in_place} — delivered for home recovery.</p>
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


def locations_index_html(locations: list[dict]) -> str:
    groups = {"DC": [], "MD": [], "VA": []}
    for loc in locations:
        groups[loc["state"]].append(loc)

    def links(items: list[dict]) -> str:
        return "\n".join(
            f'          <li><a href="locations/{loc["slug"]}.html">Lift chair rental in {loc["name"]}'
            + (f', {loc["state"]}' if loc["state"] != "DC" else "")
            + "</a></li>"
            for loc in items
        )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta
      name="description"
      content="Lift chair rental delivery locations across Washington DC, Maryland, and Virginia — District Medical Rentals."
    />
    <title>Lift Chair Rental Locations | District Medical Rentals</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Sora:wght@500;600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="icon" href="favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png" />
    <link rel="apple-touch-icon" href="apple-touch-icon.png" />
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="header-inner">
        <a class="brand brand-with-logo" href="index.html">
          <img class="header-logo" src="images/logo.png" alt="" width="72" height="82" />
          <span>District Medical Rentals</span>
        </a>
        <nav class="nav" aria-label="Primary">
          <a href="index.html">Home</a>
          <a href="about.html">About</a>
          <a href="rates.html">Rates</a>
          <a href="contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main id="main" class="page page-centered">
      <header class="page-header">
        <h1>Lift chair rental locations</h1>
        <p>
          Find District Medical Rentals delivery pages for counties and cities across Washington,
          DC, Maryland, and Virginia.
        </p>
      </header>

      <section class="about-block location-group">
        <h2>Washington, DC</h2>
        <ul class="location-list">
{links(groups["DC"])}
        </ul>
      </section>

      <section class="about-block location-group">
        <h2>Maryland</h2>
        <ul class="location-list">
{links(groups["MD"])}
        </ul>
      </section>

      <section class="about-block location-group">
        <h2>Virginia</h2>
        <ul class="location-list">
{links(groups["VA"])}
        </ul>
      </section>
    </main>

    <footer class="site-footer">
      <img class="footer-logo" src="images/logo.png" alt="District Medical Supplies" width="120" height="136" />
      <p class="footer-brand">District Medical Rentals</p>
      <p>Medical-grade lift chairs and beds delivered in DC, Maryland, and Virginia.</p>
      <p><a href="tel:+19173465309">917-346-5309</a></p>
      <nav class="footer-nav" aria-label="Footer">
        <a href="index.html">Home</a>
        <a href="about.html">About</a>
        <a href="rates.html">Rates</a>
        <a href="contact.html">Contact</a>
        <a href="locations.html">Locations</a>
        <a href="privacy.html">Privacy Policy</a>
      </nav>
    </footer>

    <a class="sticky-call" href="contact.html">Book Now</a>
  </body>
</html>
"""


def write_sitemap(locations: list[dict], base_url: str) -> None:
    base = base_url.rstrip("/")
    urls = [
        "",
        "/about.html",
        "/rates.html",
        "/contact.html",
        "/privacy.html",
        "/locations.html",
    ]
    urls += [f"/locations/{loc['slug']}.html" for loc in locations]

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in urls:
        parts.append("  <url>")
        parts.append(f"    <loc>{base}{path if path else '/'}</loc>")
        parts.append("  </url>")
    parts.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    config = {"baseUrl": "https://YOUR_USERNAME.github.io/district-medical-rentals"}
    if CONFIG_PATH.exists():
        config.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    else:
        CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    locations = build_locations()
    OUT_DIR.mkdir(exist_ok=True)

    # Clear old generated pages
    for old in OUT_DIR.glob("*.html"):
        old.unlink()

    for loc in locations:
        (OUT_DIR / f"{loc['slug']}.html").write_text(page_html(loc), encoding="utf-8")

    (ROOT / "locations.html").write_text(locations_index_html(locations), encoding="utf-8")
    write_sitemap(locations, config["baseUrl"])

    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {config['baseUrl'].rstrip('/')}/sitemap.xml\n",
        encoding="utf-8",
    )

    (ROOT / "locations.json").write_text(
        json.dumps(locations, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Generated {len(locations)} location pages in {OUT_DIR}")
    print(f"Sitemap baseUrl: {config['baseUrl']}")


if __name__ == "__main__":
    main()
