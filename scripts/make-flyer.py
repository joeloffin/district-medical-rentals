#!/usr/bin/env python3
"""One-page hospital flyer for District Medical Rentals."""

from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "flyers" / "fonts"
OUT = ROOT / "flyers" / "district-medical-rentals-flyer.pdf"
PREVIEW = ROOT / "flyers" / "district-medical-rentals-flyer.png"

W, H = 2550, 3300
NAVY = (11, 58, 102)
DEEP = (7, 42, 75)
CYAN = (61, 189, 236)
MID = (23, 137, 184)
INK_BLUE = (18, 135, 180)
SOFT = (238, 248, 253)
WHITE = (255, 255, 255)
INK = (10, 39, 68)
MUTED = (72, 98, 122)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def display(size, weight=800):
    return font(f"Sora-{weight}.ttf", size)


def body(size, weight=500):
    return font(f"DMSans-{weight}.ttf", size)


def text_width(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, width):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            trial = word if not line else f"{line} {word}"
            if text_width(draw, trial, fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_center(draw, text, y, fnt, fill, box_width=W, box_left=0):
    draw.text((box_left + (box_width - text_width(draw, text, fnt)) / 2, y), text, font=fnt, fill=fill)


def cover(path, w, h):
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - w) // 2
    top = max(0, (im.height - h) // 3)
    return im.crop((left, top, left + w, top + h))


def rounded_paste(base, im, xy, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), radius=radius, fill=255)
    base.paste(im, xy, mask)


def h_gradient(w, h):
    small_w = 640
    band = Image.new("RGB", (small_w, 8))
    px = band.load()
    for x in range(small_w):
        t = x / (small_w - 1)
        if t < 0.45:
            u = t / 0.45
            color = tuple(round(NAVY[i] + (MID[i] - NAVY[i]) * u) for i in range(3))
        else:
            u = (t - 0.45) / 0.55
            color = tuple(round(MID[i] + (CYAN[i] - MID[i]) * u) for i in range(3))
        for y in range(8):
            px[x, y] = color
    return band.resize((w, h), Image.Resampling.BILINEAR)


def stroke_icon(draw_fn, size=150):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pad = 18
    d.ellipse((pad, pad, size - pad, size - pad), fill=SOFT)
    draw_fn(d, size)
    return im


def icon_shield(d, size):
    s = size / 24
    ox, oy = size * 0.30, size * 0.28
    pts = [
        (12 * s + ox * 0, 4 * s),
        (18 * s, 6.4 * s),
        (18 * s, 10.5 * s),
        (15.5 * s, 15.2 * s),
        (12 * s, 17.6 * s),
        (8.5 * s, 15.2 * s),
        (6 * s, 10.5 * s),
        (6 * s, 6.4 * s),
    ]
    # Recenter the glyph in the circle.
    shift = size * 0.18
    pts = [(x + shift * 0.15, y + shift * 0.35) for x, y in pts]
    d.line(pts + [pts[0]], fill=INK_BLUE, width=7, joint="curve")
    check = [(8.6 * s + 8, 12.2 * s + 8), (11 * s + 8, 14.6 * s + 8), (15.6 * s + 8, 9.4 * s + 8)]
    d.line(check, fill=INK_BLUE, width=7, joint="curve")


def icon_spark(d, size):
    def star(cx, cy, r):
        d.line([(cx, cy - r), (cx, cy + r)], fill=INK_BLUE, width=6)
        d.line([(cx - r, cy), (cx + r, cy)], fill=INK_BLUE, width=6)
        d.line([(cx - r * 0.7, cy - r * 0.7), (cx + r * 0.7, cy + r * 0.7)], fill=INK_BLUE, width=5)
        d.line([(cx + r * 0.7, cy - r * 0.7), (cx - r * 0.7, cy + r * 0.7)], fill=INK_BLUE, width=5)

    star(size * 0.46, size * 0.46, 28)
    star(size * 0.70, size * 0.66, 14)


def icon_truck(d, size):
    x, y = 36, 58
    d.rounded_rectangle((x, y, x + 78, y + 52), radius=6, outline=INK_BLUE, width=6)
    d.polygon([(x + 78, y + 14), (x + 108, y + 32), (x + 108, y + 52), (x + 78, y + 52)], outline=INK_BLUE)
    d.line([(x + 78, y + 14), (x + 108, y + 32), (x + 108, y + 52)], fill=INK_BLUE, width=6)
    d.ellipse((x + 16, y + 46, x + 36, y + 66), outline=INK_BLUE, width=6)
    d.ellipse((x + 78, y + 46, x + 98, y + 66), outline=INK_BLUE, width=6)


def icon_tag(d, size):
    x, y = 40, 48
    d.polygon(
        [(x, y + 28), (x, y), (x + 36, y), (x + 92, y + 56), (x + 56, y + 92)],
        outline=INK_BLUE,
    )
    d.line([(x, y + 28), (x, y), (x + 36, y), (x + 92, y + 56), (x + 56, y + 92), (x, y + 28)], fill=INK_BLUE, width=6, joint="curve")
    d.ellipse((x + 16, y + 16, x + 32, y + 32), outline=INK_BLUE, width=6)


def main():
    canvas = Image.new("RGB", (W, H), SOFT)
    draw = ImageDraw.Draw(canvas)
    margin = 70

    draw.rectangle((0, 0, W, 390), fill=WHITE)
    logo = Image.open(ROOT / "images" / "logo.png").convert("RGBA")
    lh = 300
    lw = round(logo.width * lh / logo.height)
    logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo, ((W - lw) // 2, 28), logo)
    draw.rectangle((0, 372, W, 390), fill=CYAN)

    draw.rectangle((0, 390, W, 700), fill=NAVY)
    headline = "HOME RECOVERY EQUIPMENT, DELIVERED"
    hf = display(62, 800)
    if text_width(draw, headline, hf) > W - 120:
        hf = display(54, 800)
    draw_center(draw, headline, 445, hf, WHITE)
    draw_center(draw, "Lift recliners   ·   Sit-to-stand lifts   ·   Hospital beds", 545, display(36, 600), CYAN)
    draw_center(draw, "Washington, DC    ·    Maryland    ·    Virginia", 604, body(42, 500), (230, 246, 252))

    draw_center(draw, "WHAT WE RENT", 740, display(32, 700), INK_BLUE)

    products = [
        (
            ROOT / "images" / "lift-chair-1.webp",
            "Lift recliner",
            "Helps you stand and sit safely after surgery or when mobility is limited.",
        ),
        (
            ROOT / "images" / "sit-to-stand-1.webp",
            "Sit-to-stand lift",
            "Helps a caregiver raise someone from a chair, bed, wheelchair, or toilet.",
        ),
        (
            ROOT / "images" / "medical-bed-1.webp",
            "Hospital bed",
            "Electronic bed that raises the head and knees for safer rest at home.",
        ),
    ]

    gap = 36
    card_w = (W - margin * 2 - gap * 2) // 3
    card_top = 800
    photo_h = 360
    card_h = 720
    title_font = display(72, 800)
    blurb_font = body(42, 700)
    for i, (photo, title, blurb) in enumerate(products):
        x = margin + i * (card_w + gap)
        draw.rounded_rectangle((x, card_top, x + card_w, card_top + card_h), radius=28, fill=WHITE)
        pic = cover(photo, card_w - 28, photo_h)
        rounded_paste(canvas, pic, (x + 14, card_top + 14), 22)
        draw = ImageDraw.Draw(canvas)
        ty = card_top + photo_h + 24
        for line in wrap(draw, title, title_font, card_w - 48):
            draw.text((x + 24, ty), line, font=title_font, fill=NAVY)
            ty += 84
        by = ty + 8
        for line in wrap(draw, blurb, blurb_font, card_w - 48):
            draw.text((x + 24, by), line, font=blurb_font, fill=INK)
            by += 54

    call_top = card_top + card_h + 28
    call_h = 280
    call = h_gradient(W - margin * 2, call_h)
    mask = Image.new("L", call.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, call.width, call.height), radius=28, fill=255)
    canvas.paste(call, (margin, call_top), mask)
    draw = ImageDraw.Draw(canvas)
    call_font = display(72, 700)
    lines = [
        "No need to spend thousands on recovery equipment.",
        "Rent with us instead.",
    ]
    block_h = len(lines) * 90
    cy = call_top + (call_h - block_h) / 2 - 6
    for line in lines:
        draw_center(draw, line, cy, call_font, WHITE)
        cy += 90

    trust = [
        (icon_shield, "Medical-grade", "Equipment built for safe recovery"),
        (icon_spark, "Cleaned & sanitized", "Before every rental"),
        (icon_truck, "Fast delivery", "Same-day & next-day"),
        (icon_tag, "No deposit", "Simple weekly rates"),
    ]
    trust_top = call_top + call_h + 28
    col_w = (W - margin * 2) // 4
    icon_size = 220
    label_font = display(46, 700)
    sub_font = body(34, 500)
    for i, (icon_fn, label, sub) in enumerate(trust):
        cx = margin + i * col_w + col_w // 2
        icon = stroke_icon(icon_fn, 150).resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        canvas.paste(icon, (cx - icon_size // 2, trust_top), icon)
        draw = ImageDraw.Draw(canvas)
        draw_center(draw, label, trust_top + icon_size + 8, label_font, NAVY, col_w, margin + i * col_w)
        sub_lines = wrap(draw, sub, sub_font, col_w - 16)
        sy = trust_top + icon_size + 64
        for line in sub_lines:
            draw_center(draw, line, sy, sub_font, MUTED, col_w, margin + i * col_w)
            sy += 42

    foot = H - 470
    notes = [
        "No deposit required",
        "2-week minimum",
        "Same-day and next-day delivery, even before surgery",
        "One fee for delivery, setup, and pickup",
    ]
    note_font = body(52, 700)
    line_h = 78
    note_h = 48 + len(notes) * line_h
    note_top = trust_top + icon_size + 180
    draw.rounded_rectangle((margin, note_top, W - margin, note_top + note_h), radius=28, fill=WHITE)
    ny = note_top + 32
    for note in notes:
        draw.ellipse((margin + 40, ny + 14, margin + 70, ny + 44), fill=CYAN)
        draw.text((margin + 96, ny), note, font=note_font, fill=INK)
        ny += line_h

    draw.rectangle((0, foot, W, H), fill=DEEP)
    draw.rectangle((0, foot, W, foot + 14), fill=CYAN)
    draw.text((margin, foot + 42), "CALL OR TEXT", font=display(32, 700), fill=CYAN)
    draw.text((margin, foot + 90), "917-346-5309", font=display(96, 800), fill=WHITE)
    draw.text((margin, foot + 198), "Text us for the fastest reply.", font=body(36, 500), fill=(220, 240, 248))
    draw.text((margin, foot + 252), "districtmedicalrentals.com", font=display(92, 700), fill=WHITE)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    qr.add_data("https://districtmedicalrentals.com")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0b3a66", back_color="white").convert("RGB")
    qr_img = qr_img.resize((330, 330), Image.Resampling.NEAREST)
    qx = W - margin - 380
    qy = foot + 55
    pad = Image.new("RGB", (380, 380), WHITE)
    pad.paste(qr_img, (25, 8))
    canvas.paste(pad, (qx, qy))
    label = "Scan to see rates & book"
    lf = display(26, 600)
    draw.text((qx + (380 - text_width(draw, label, lf)) / 2, qy + 338), label, font=lf, fill=NAVY)

    canvas.save(PREVIEW, "PNG", optimize=True)
    canvas.save(OUT, "PDF", resolution=300.0)
    print(OUT)


if __name__ == "__main__":
    main()
