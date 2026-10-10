"""
Joshua Baller — Selected Portfolios (one-page gateway PDF)
Editable source. Edit the CONFIG block, then run:  python3 build_portfolio_gateway.py

- Replace the three *_URL placeholders with real portfolio links.
- Point each image slot at an exported PNG/JPG of the artwork. If a file is
  missing, a labeled placeholder is drawn instead.
- Optional "crop" per slot = (left, top, right, bottom) as 0–1 fractions of the
  source image, used to pull the visual application out of a busy page.
- fit: "cover" fills the slot (crops edges); "contain" keeps the whole asset
  uncropped and centred on a neutral bed.
"""
import os, io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader, simpleSplit

# ───────────────────────── CONFIG ─────────────────────────
OUT = "Joshua_Baller_Selected_Portfolios.pdf"
FONT_DIR = "inter/extras/ttf"
PPI = 150

BRANDING_PORTFOLIO_URL      = "https://drive.google.com/file/d/1nbz-2EZG-4Goj-G-L_njkj0Jlnt62MLH/view?usp=sharing"
PRESENTATION_PORTFOLIO_URL  = "https://drive.google.com/file/d/1yVroiQ2rTMrIW6OhgdXgeHQ7R5eB4bjh/view?usp=sharing"
SOCIAL_CAMPAIGN_PORTFOLIO_URL = "https://drive.google.com/file/d/1niZ-RM92YBTyM1elVjxVlBRXOak-WtKt/view?usp=sharing"

EMAIL = "hello@joshuaballer.com"
SITE = "joshuaballer.com"
LOCATION = "Metro Manila, Philippines"

ASSETS = "assets"  # folder holding exported artwork
COLUMNS = [
    dict(
        title="Branding Projects",
        desc="Brand identities, visual systems, and web applications for startups across technology, healthcare, and SaaS.",
        link="View branding portfolio \u2197",
        url=BRANDING_PORTFOLIO_URL,
        layout="hero_two",          # one dominant image + two supporting crops
        fit="cover",
        slots=[
            dict(file="branding_crosby.png",     label="Crosby",     note="Brand application", crop=None),
            dict(file="branding_renumerate.png", label="Renumerate", note="Poster mockup",     crop=(0.0625, 0.13, 0.646, 0.859)),
            dict(file="branding_revin.png",      label="Revin",      note="Billboard mockup",  crop=None),
        ],
    ),
    dict(
        title="Presentation Designs",
        desc="Four concepts covering investor pitches, business reviews, product launches, and marketing strategy.",
        link="View presentation portfolio \u2197",
        url=PRESENTATION_PORTFOLIO_URL,
        layout="grid_2x2",          # four covers, uncropped
        fit="contain",
        slots=[
            dict(file="pres_relay.png",   label="Relay",   note="Presentation PDF · p.1", crop=None),
            dict(file="pres_signal.png",  label="Signal",  note="Presentation PDF · p.1", crop=None),
            dict(file="pres_briefly.png", label="Briefly", note="Presentation PDF · p.1", crop=None),
            dict(file="pres_forma.png",   label="Forma",   note="Presentation PDF · p.1", crop=None),
        ],
    ),
    dict(
        title="Social Media Campaign",
        desc="A unified campaign concept spanning feed posts, carousels, educational content, Stories, and motion.",
        link="View campaign case study \u2197",
        url=SOCIAL_CAMPAIGN_PORTFOLIO_URL,
        layout="portrait_stack",   # 4:5 launch post + 16:9 promo + 1:1 frame, all at true proportions
        fit="contain",              # keep proportions; never cut headlines/faces
        slots=[
            dict(file="campaign_launch.png", label="Launch feed post",    note="1080 x 1350", crop=None),
            dict(file="campaign_promo.png",  label="Promo thumbnail",     note="1280 x 720",  crop=None),
            dict(file="campaign_motion.png", label="Animated-post frame", note="1080 x 1080", crop=None, bg="sample"),
        ],
    ),
]
# ──────────────────────────────────────────────────────────

W, H = 1920, 1080
M = 90
GUTTER = 32
BG, INK, MUTED, RULE = (HexColor(c) for c in ("#F5F5F2", "#202020", "#70706C", "#DDDDD7"))
SLOT_BG = HexColor("#EAEAE5")

pdfmetrics.registerFont(TTFont("Inter", f"{FONT_DIR}/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Medium", f"{FONT_DIR}/Inter-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SemiBold", f"{FONT_DIR}/Inter-SemiBold.ttf"))

def Y(top):  # convert top-based y to reportlab bottom-based
    return H - top

def text(c, s, x, top, font, size, color, anchor="left", tracking=0):
    c.setFillColor(color)
    c.setFont(font, size)
    t = c.beginText()
    t.setTextOrigin(x if anchor == "left" else x - pdfmetrics.stringWidth(s, font, size) - tracking * (len(s) - 1), Y(top))
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.textOut(s)
    c.drawText(t)
    return pdfmetrics.stringWidth(s, font, size) + tracking * (len(s) - 1)

def paragraph(c, s, x, top, width, font, size, leading, color):
    lines = simpleSplit(s, font, size, width)
    for i, ln in enumerate(lines):
        text(c, ln, x, top + i * leading, font, size, color)
    return len(lines)

def link(c, url, x, top, w, h):
    c.linkURL(url, (x, Y(top + h), x + w, Y(top)), relative=0, thickness=0)

def prepared_image(path, box_w, box_h, fit, crop):
    im = Image.open(path).convert("RGB")
    if crop:
        l, t, r, b = crop
        im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    if fit == "cover":
        target = box_w / box_h
        if im.width / im.height > target:
            nw = int(im.height * target); off = (im.width - nw) // 2
            im = im.crop((off, 0, off + nw, im.height))
        else:
            nh = int(im.width / target); off = (im.height - nh) // 2
            im = im.crop((0, off, im.width, off + nh))
        dw, dh = box_w, box_h
    else:
        s = min(box_w / im.width, box_h / im.height)
        dw, dh = im.width * s, im.height * s
    px_w = max(1, int(dw / 72 * PPI)); px_h = max(1, int(dh / 72 * PPI))
    if im.width > px_w:
        im = im.resize((px_w, px_h), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=85, optimize=True); buf.seek(0)
    return ImageReader(buf), dw, dh

def slot(c, x, top, w, h, spec, fit):
    path = os.path.join(ASSETS, spec["file"])
    bed = SLOT_BG
    if spec.get("bg") == "sample" and os.path.exists(path):
        r, g_, b = Image.open(path).convert("RGB").getpixel((4, 4))
        bed = HexColor("#%02X%02X%02X" % (r, g_, b))
    c.setFillColor(bed)
    c.rect(x, Y(top + h), w, h, stroke=0, fill=1)
    if os.path.exists(path):
        img, dw, dh = prepared_image(path, w, h, fit, spec.get("crop"))
        c.drawImage(img, x + (w - dw) / 2, Y(top + (h - dh) / 2 + dh), dw, dh)
    else:
        cx, cy = x + w / 2, top + h / 2
        c.setStrokeColor(HexColor("#C9C9C3")); c.setLineWidth(1); c.setDash(4, 4)
        c.rect(x + 0.5, Y(top + h) + 0.5, w - 1, h - 1, stroke=1, fill=0)
        c.setDash()
        size = 17 if w > 200 else 14
        lw = pdfmetrics.stringWidth(spec["label"], "Inter-Medium", size)
        text(c, spec["label"], cx - lw / 2, cy - 2, "Inter-Medium", size, MUTED)
        nw = pdfmetrics.stringWidth(spec["note"], "Inter", size - 4)
        text(c, spec["note"], cx - nw / 2, cy + size + 2, "Inter", size - 4, HexColor("#9A9A95"))

def thumbnail(c, x, top, w, h, col):
    g = 8  # inner gap
    s = col["slots"]
    if col["layout"] == "hero_two":
        hero_w = (w - g) * 0.6
        side_w = w - g - hero_w
        side_h = (h - g) / 2
        slot(c, x, top, hero_w, h, s[0], col["fit"])
        slot(c, x + hero_w + g, top, side_w, side_h, s[1], col["fit"])
        slot(c, x + hero_w + g, top + side_h + g, side_w, side_h, s[2], col["fit"])
    elif col["layout"] == "portrait_stack":
        hero_w = h * 4 / 5
        rw = w - g - hero_w
        promo_h = rw * 9 / 16
        sq = h - g - promo_h
        slot(c, x, top, hero_w, h, s[0], col["fit"])
        slot(c, x + hero_w + g, top, rw, promo_h, s[1], col["fit"])
        slot(c, x + hero_w + g, top + promo_h + g, rw, sq, s[2], col["fit"])  # square sits centred on its own cream, so the stack fills the full width
    elif col["layout"] == "grid_2x2":
        cw, ch = (w - g) / 2, (h - g) / 2
        for i, sp in enumerate(s):
            slot(c, x + (i % 2) * (cw + g), top + (i // 2) * (ch + g), cw, ch, sp, col["fit"])

def build():
    c = canvas.Canvas(OUT, pagesize=(W, H), pageCompression=1)
    c.setTitle("Joshua Baller — Selected Portfolios 2026")
    c.setAuthor("Joshua Baller")
    c.setSubject("Brand, Presentation & Campaign Design")
    c.setFillColor(BG); c.rect(0, 0, W, H, stroke=0, fill=1)

    # ── Introduction ──
    text(c, "Joshua Baller", M, M + 24, "Inter-SemiBold", 30, INK)
    text(c, "Selected Portfolios \u00b7 2026", W - M, M + 24, "Inter-Medium", 24, INK, anchor="right")
    text(c, LOCATION, W - M, M + 58, "Inter", 22, MUTED, anchor="right")
    text(c, "Brand, Presentation & Campaign Design", M, M + 118, "Inter-SemiBold", 68, INK, tracking=-1.4)
    paragraph(c, "Multidisciplinary designer with 6+ years of experience in brand identity, web and product design, and marketing communication.",
              M, M + 172, 1060, "Inter", 27, 38, MUTED)

    # ── Portfolio columns ──
    col_w = (W - 2 * M - 2 * GUTTER) / 3
    th_h = (col_w - 8) / 2 * 9 / 16 * 2 + 8  # 2x2 grid of exact 16:9 covers (8 px inner gap)
    th_top = 365
    for i, col in enumerate(COLUMNS):
        x = M + i * (col_w + GUTTER)
        thumbnail(c, x, th_top, col_w, th_h, col)
        link(c, col["url"], x, th_top, col_w, th_h)
        t = th_top + th_h + 48
        text(c, col["title"], x, t, "Inter-SemiBold", 32, INK, tracking=-0.4)
        n = paragraph(c, col["desc"], x, t + 44, col_w, "Inter", 25, 36, MUTED)
        lt = t + 44 + 2 * 36 + 46  # fixed so all three links align
        lw = text(c, col["link"], x, lt, "Inter-Medium", 25, INK)
        c.setStrokeColor(INK); c.setLineWidth(1.2)
        c.line(x, Y(lt + 7), x + lw, Y(lt + 7))
        link(c, col["url"], x - 4, lt - 28, lw + 8, 42)

    # ── Footer ──
    rule_top = H - M - 62
    c.setStrokeColor(RULE); c.setLineWidth(1)
    c.line(M, Y(rule_top), W - M, Y(rule_top))
    ft = H - M - 12
    # email left-aligned, website right-aligned to the outer margin
    for item, url, align in ((EMAIL, "mailto:" + EMAIL, "left"), (SITE, "https://" + SITE, "right")):
        tw = pdfmetrics.stringWidth(item, "Inter-Medium", 22)
        x = M if align == "left" else W - M - tw
        text(c, item, x, ft, "Inter-Medium", 22, INK)
        c.setStrokeColor(INK); c.setLineWidth(1)
        c.line(x, Y(ft + 6), x + tw, Y(ft + 6))
        link(c, url, x - 8, ft - 30, tw + 16, 46)
    c.showPage(); c.save()
    print(f"{OUT}: {os.path.getsize(OUT)/1024:.0f} KB")

if __name__ == "__main__":
    build()
