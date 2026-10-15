#!/usr/bin/env python3
"""Draw the server-rack SVGs for the profile README (banner, homelab, stack).

Edit the text in banner(), homelab() and stack(), then rebuild:

    pip install fonttools brotli
    mkdir -p /tmp/rack-fonts && cd /tmp/rack-fonts
    curl -LO https://github.com/google/fonts/raw/main/ofl/barlowsemicondensed/BarlowSemiCondensed-Bold.ttf
    curl -LO https://github.com/google/fonts/raw/main/ofl/barlowsemicondensed/BarlowSemiCondensed-Medium.ttf
    curl -LO https://github.com/google/fonts/raw/main/apache/permanentmarker/PermanentMarker-Regular.ttf
    python assets/src/rack.py /tmp/rack-fonts assets

Barlow is OFL and Permanent Marker is Apache 2.0; an ASCII subset of each is embedded in the SVGs.
"""
import base64
import io
import math
import random
import sys
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR, OUT_DIR = sys.argv[1], sys.argv[2]

FONTS = {
    "label": ("Rack Label", "BarlowSemiCondensed-Bold.ttf", "'Arial Narrow',Arial,sans-serif"),
    "silk": ("Rack Silk", "BarlowSemiCondensed-Medium.ttf", "Arial,sans-serif"),
    "hand": ("Rack Hand", "PermanentMarker-Regular.ttf", "'Marker Felt','Comic Sans MS',cursive"),
}
TT = {k: TTFont(f"{FONT_DIR}/{v[1]}") for k, v in FONTS.items()}
ASCII = "".join(chr(c) for c in range(32, 127))

W = 846      # GitHub renders profile README images 846px wide on desktop
U = 64       # one rack unit
RW = 36      # rail width
HOLE_X = 24  # square hole centre, from the outer edge
NUM_X = 8    # U number centre, from the outer edge
EAR_X0 = 15  # equipment ears cover the holes but not the numbers
EAR_W = 37

C = dict(
    rack="#0c0d0f", rail="#2a2d32", rail_lo="#16171a", hole="#050506", rail_num="#7c8189",
    steel="#2a2d32", steel_hi="#3e434a", steel_lo="#131416", ear="#25282c",
    paint="#ECEAE2", ink="#141414", masking="#E0D0AA", sharpie="#1b1b1e",
    white="#F1F0E9", yellow="#F2C744", green="#82C97E", black="#1c1c1c",
    led_green="#46E07D", led_amber="#FFB21E", led_off="#3a3c3f",
)


def metric(font, key):
    tt = TT[font]
    return getattr(tt["OS/2"], key, 0) / tt["head"].unitsPerEm


def measure(font, s, size, ls=0.0):
    tt = TT[font]
    cmap, hmtx, upm = tt.getBestCmap(), tt["hmtx"], tt["head"].unitsPerEm
    return sum(hmtx[cmap.get(ord(ch), ".notdef")][0] for ch in s) / upm * size + ls * len(s)


def woff2(font):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.notdef_outline = True
    f = subset.load_font(f"{FONT_DIR}/{FONTS[font][1]}", opts)
    sub = subset.Subsetter(opts)
    sub.populate(text=ASCII)  # all of ASCII, so the text stays editable by hand
    sub.subset(f)
    buf = io.BytesIO()
    subset.save_font(f, buf, opts)
    return base64.b64encode(buf.getvalue()).decode()


CAP = {k: (metric(k, "sCapHeight") or 0.7) for k in FONTS}


class Doc:
    def __init__(self, h, title, desc, seed):
        self.h, self.title, self.desc = h, title, desc
        self.out, self.defs, self.css = [], [], []
        self.fonts = set()
        self.rng = random.Random(seed)
        self.blinks = []

    def add(self, s):
        self.out.append(s)

    def text(self, s, font, x, y, size, fill, anchor="start", ls=0.0, rot=0.0, opacity=None):
        self.fonts.add(font)
        a = f'class="f-{font}" x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"'
        if anchor != "start":
            a += f' text-anchor="{anchor}"'
        if ls:
            a += f' letter-spacing="{ls}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        if rot:
            a += f' transform="rotate({rot:.2f} {x:.1f} {y:.1f})"'
        self.add(f"<text {a}>{escape(s)}</text>")

    def blink(self):
        """Inline style for an LED that flickers on its own irregular rhythm."""
        if not self.blinks:
            for i in range(6):
                frames, p = ["0%,100%{opacity:1}"], self.rng.uniform(4, 14)
                while p < 88:
                    w = self.rng.uniform(1.5, 5)
                    frames.append(f"{p:.1f}%{{opacity:.12}}{p + w:.1f}%{{opacity:1}}")
                    p += w + self.rng.uniform(5, 30)
                self.css.append(f"@keyframes k{i}{{{''.join(frames)}}}")
                self.blinks.append(f"k{i}")
            self.css.append("@media (prefers-reduced-motion:reduce){.led{animation:none!important}}")
        k = self.rng.choice(self.blinks)
        dur, delay = self.rng.uniform(0.9, 3.8), self.rng.uniform(0, 3)
        return f' class="led" style="animation:{k} {dur:.2f}s steps(1,end) -{delay:.2f}s infinite"'

    def svg(self):
        css = []
        for k in sorted(self.fonts):
            fam, _, fallback = FONTS[k]
            css.append(f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{woff2(k)}) format('woff2')}}")
            css.append(f".f-{k}{{font-family:'{fam}',{fallback}}}")
        css += self.css
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{self.h}" viewBox="0 0 {W} {self.h}" role="img" aria-labelledby="t d">\n'
            f'<title id="t">{escape(self.title)}</title>\n<desc id="d">{escape(self.desc)}</desc>\n'
            f'<style>{"".join(css)}</style>\n'
            f'<defs><clipPath id="frame"><rect width="{W}" height="{self.h}" rx="8"/></clipPath>{"".join(self.defs)}</defs>\n'
            f'<g clip-path="url(#frame)">\n' + "\n".join(self.out) + "\n</g>\n</svg>\n"
        )


# ---------------------------------------------------------------- parts

def rack(d, top_u, top_y):
    """Rack interior and rails. U `top_u` has its top edge at `top_y`; numbers count down the page."""
    d.add(f'<rect width="{W}" height="{d.h}" fill="{C["rack"]}"/>')
    for x0 in (0, W - RW):
        d.add(f'<rect x="{x0}" width="{RW}" height="{d.h}" fill="{C["rail"]}"/>')
        edge = x0 + RW - 0.5 if x0 == 0 else x0 + 0.5
        d.add(f'<line x1="{edge}" x2="{edge}" y2="{d.h}" stroke="{C["rail_lo"]}"/>')
    k = math.floor(-top_y / U) - 1
    while top_y + k * U < d.h:
        top = top_y + k * U
        for x, nx in ((HOLE_X, NUM_X), (W - HOLE_X, W - NUM_X)):
            d.add(f'<line x1="{nx - 5}" x2="{nx + 5}" y1="{top + 0.5}" y2="{top + 0.5}" stroke="{C["rail_lo"]}"/>')
            for f in (0.143, 0.5, 0.857):
                y = top + f * U
                d.add(f'<rect x="{x - 3.5}" y="{y - 3.5:.1f}" width="7" height="7" rx="1" fill="{C["hole"]}"/>')
            d.text(str(top_u - k), "silk", nx, top + U / 2 + 3.2, 9, C["rail_num"], anchor="middle")
        k += 1


def screw(d, cx, cy, r=6.5):
    a = d.rng.uniform(0, 90)
    d.add(f'<circle cx="{cx}" cy="{cy:.1f}" r="{r}" fill="#4b5057" stroke="#121315"/>')
    d.add(f'<circle cx="{cx}" cy="{cy - 0.6:.1f}" r="{r - 1.7}" fill="#3c4047"/>')
    s = r - 2.4
    d.add(f'<g transform="rotate({a:.0f} {cx} {cy:.1f})" stroke="#151618" stroke-width="1.6" stroke-linecap="round">'
          f'<line x1="{cx - s:.1f}" y1="{cy:.1f}" x2="{cx + s:.1f}" y2="{cy:.1f}"/>'
          f'<line x1="{cx}" y1="{cy - s:.1f}" x2="{cx}" y2="{cy + s:.1f}"/></g>')


def unit(d, y, n_u, face=None, hi=None, lo=None, ear=None):
    face, hi, lo, ear = face or C["steel"], hi or C["steel_hi"], lo or C["steel_lo"], ear or C["ear"]
    h = n_u * U
    x0, x1 = EAR_X0, W - EAR_X0
    d.add(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" fill="{face}"/>')
    for ex in (x0, x1 - EAR_W):
        d.add(f'<rect x="{ex}" y="{y}" width="{EAR_W}" height="{h}" fill="{ear}"/>')
        seam = ex + EAR_W - 0.5 if ex == x0 else ex + 0.5
        d.add(f'<line x1="{seam}" x2="{seam}" y1="{y}" y2="{y + h}" stroke="{lo}" opacity=".7"/>')
    d.add(f'<line x1="{x0}" x2="{x1}" y1="{y + 0.5}" y2="{y + 0.5}" stroke="{hi}"/>')
    d.add(f'<line x1="{x0}" x2="{x1}" y1="{y + h - 0.5}" y2="{y + h - 0.5}" stroke="{lo}"/>')
    rows = [y + U / 2] if n_u == 1 else [y + U / 2, y + h - U / 2]
    for cy in rows:
        screw(d, HOLE_X, cy)
        screw(d, W - HOLE_X, cy)


def tape_size(text, size, ls, padx=None):
    padx = size * 0.5 if padx is None else padx
    return measure("label", text, size, ls) + 2 * padx, round(size * 1.4)


def tape(d, text, size, color, cx=None, cy=0, left=None, rot=0.0, ls=0.5, ink=None, padx=None):
    """A strip of label-maker tape. Returns its width."""
    w, h = tape_size(text, size, ls, padx)
    if left is not None:
        cx = left + w / 2
    x, y = cx - w / 2, cy - h / 2
    d.add(f'<g transform="rotate({rot:.2f} {cx:.1f} {cy:.1f})">')
    d.add(f'<rect x="{x + 0.6:.1f}" y="{y + 1.8:.1f}" width="{w:.1f}" height="{h}" rx="2.5" fill="#000" opacity=".5"/>')
    d.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="2.5" fill="{color}"/>')
    d.add(f'<rect x="{x + 2:.1f}" y="{y + 1:.1f}" width="{w - 4:.1f}" height="1" fill="#fff" opacity=".35"/>')
    d.text(text, "label", cx + ls / 2, cy + size * CAP["label"] / 2, size, ink or C["ink"], anchor="middle", ls=ls)
    d.add("</g>")
    return w


def masking(d, text, cx, cy, size, rot):
    """Torn masking tape with sharpie on it."""
    w, h = measure("hand", text, size) + size * 1.4, size * 1.8
    x, y, r = cx - w / 2, cy - h / 2, d.rng
    n = 7
    right = [(x + w + r.uniform(-3, 3), y + h * i / n) for i in range(n + 1)]
    left = [(x + r.uniform(-3, 3), y + h * (n - i) / n) for i in range(n + 1)]
    pts = [(x + 2, y + r.uniform(-0.6, 0.6))] + right + [(x + w - 2, y + h)] + left
    poly = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    d.add(f'<g transform="rotate({rot:.2f} {cx:.1f} {cy:.1f})">')
    d.add(f'<polygon points="{poly}" fill="#000" opacity=".45" transform="translate(0.8 1.8)"/>')
    d.add(f'<polygon points="{poly}" fill="{C["masking"]}"/>')
    d.text(text, "hand", cx, cy + size * CAP["hand"] / 2, size, C["sharpie"], anchor="middle")
    d.add("</g>")


def led(d, cx, cy, color, blink=True, r=2.2):
    cls = d.blink() if blink else ""
    d.add(f'<g{cls}><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 2.8:.1f}" fill="{color}" opacity=".18"/>'
          f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"/></g>')


def arrow(d, x0, y0, x1, y1):
    """A paint-pen arrow, drawn a little unevenly."""
    r = d.rng
    mx, my = (x0 + x1) / 2 + r.uniform(-2, 2), (y0 + y1) / 2 + r.uniform(-5, 5)
    d.add(f'<path d="M {x0:.1f} {y0:.1f} Q {mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{C["paint"]}" stroke-width="2.4" stroke-linecap="round"/>')
    a = math.atan2(y1 - my, x1 - mx)
    for s in (1, -1):
        b = a + math.pi - s * math.radians(r.uniform(26, 34))
        L = r.uniform(7, 9)
        d.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x1 + L * math.cos(b):.1f}" y2="{y1 + L * math.sin(b):.1f}" stroke="{C["paint"]}" stroke-width="2.4" stroke-linecap="round"/>')


# ---------------------------------------------------------------- units

CABLES = {  # boot / cable colour, darker edge
    "blue": ("#2E6AD1", "#1c4590"), "yellow": ("#E2B320", "#9c7b10"), "red": ("#C63D35", "#87251f"),
    "gray": ("#8E939A", "#5c6168"), "green": ("#2F9A58", "#1d6a3b"),
}


def switch(d, y):
    unit(d, y, 1, face="#d5d6d1", hi="#ecede8", lo="#97988f", ear="#c9cac4")
    tape(d, "SW-01", 13, C["black"], cx=98, cy=y + 32, rot=-0.8, ls=1, ink="#f1f1ec")
    pitch, pw, ph, py = 31, 23, 18, y + 16
    plugged = {0: "blue", 1: "blue", 2: "yellow", 3: "blue", 5: "gray", 6: "blue", 8: "red",
               9: "blue", 10: "gray", 13: "green", 14: "blue"}
    ports = []
    for i in range(16):
        px = 166 + i * pitch + (8 if i >= 8 else 0)
        ports.append(px)
        d.add(f'<path d="M {px} {py} h {pw} v 13 h -6 v 5 h -11 v -5 h -6 z" fill="#1b1c1e" stroke="#7f817b" stroke-width=".8"/>')
        on = i in plugged
        led(d, px + 5, py + ph + 9, C["led_green"] if on else C["led_off"], blink=on, r=1.8)
        led(d, px + pw - 5, py + ph + 9, C["led_amber"] if on and i % 3 else C["led_off"], blink=False, r=1.8)
    for j in range(2):
        sx = 704 + j * 40
        d.add(f'<rect x="{sx}" y="{y + 20}" width="30" height="15" rx="1.5" fill="#2b2c2e" stroke="#85877f" stroke-width=".8"/>')
        d.add(f'<rect x="{sx + 4}" y="{y + 25}" width="22" height="5" fill="#141516"/>')
        led(d, sx + 15, y + 44, C["led_off"], blink=False, r=1.8)
    # cables run up out of the frame toward a bundle above the rack
    for i, colour in plugged.items():
        fill, edge = CABLES[colour]
        px = ports[i]
        cx = px + pw / 2
        d.add(f'<rect x="{px - 2}" y="{py - 3}" width="{pw + 4}" height="{ph + 3}" rx="2" fill="{edge}"/>')
        d.add(f'<rect x="{px - 1}" y="{py - 2}" width="{pw + 2}" height="{ph}" rx="2" fill="{fill}"/>')
        d.add(f'<rect x="{px + 4}" y="{py + 3}" width="{pw - 8}" height="4" rx="1" fill="#000" opacity=".22"/>')
        ex = cx + (430 - cx) * 0.42 + d.rng.uniform(-14, 14)
        path = f"M {cx:.1f} {py - 2} C {cx:.1f} {py - 24}, {ex:.1f} {y - 6}, {ex:.1f} -12"
        d.add(f'<path d="{path}" fill="none" stroke="{edge}" stroke-width="7" stroke-linecap="round"/>')
        d.add(f'<path d="{path}" fill="none" stroke="{fill}" stroke-width="5" stroke-linecap="round"/>')
        d.add(f'<path d="{path}" fill="none" stroke="#fff" stroke-width="1.2" opacity=".2" transform="translate(-1.2 0)"/>')


def server(d, y):
    unit(d, y, 4)
    for hx in (EAR_X0 + 12, W - EAR_X0 - 12 - 13):  # pull handles on the ears
        d.add(f'<rect x="{hx}" y="{y + 70}" width="13" height="116" rx="6.5" fill="#1c1e21" stroke="#41454c" stroke-width="1.5"/>')

    tape(d, "JACOB PUGH", 62, C["white"], left=78, cy=y + 80, rot=-1.1, ls=2)
    tape(d, "INFRASTRUCTURE & AUTOMATION", 19, C["yellow"], left=84, cy=y + 151, rot=0.7, ls=1.2)

    # front panel: power, activity LEDs, ID, USB
    pcx, pcy = 92, y + 211
    d.add(f'<circle cx="{pcx}" cy="{pcy}" r="13" fill="#17181b" stroke="#0e0f10"/>')
    d.add(f'<circle cx="{pcx}" cy="{pcy}" r="16" fill="{C["led_green"]}" opacity=".08"/>')
    d.add(f'<circle cx="{pcx}" cy="{pcy}" r="10.5" fill="none" stroke="{C["led_green"]}" stroke-width="1.8"/>')
    d.add(f'<circle cx="{pcx}" cy="{pcy}" r="8" fill="#363a40"/>')
    d.add(f'<path d="M {pcx - 2.7} {pcy - 2.4} A 3.8 3.8 0 1 0 {pcx + 2.7} {pcy - 2.4} M {pcx} {pcy - 5} V {pcy - 0.6}" fill="none" stroke="#c4c8ce" stroke-width="1.3" stroke-linecap="round"/>')
    for lx, label, colour in ((128, "HDD", C["led_amber"]), (152, "NET", C["led_green"])):
        led(d, lx, pcy - 5, colour, r=2)
        d.text(label, "silk", lx, pcy + 12, 9, "#8a8f96", anchor="middle", ls=0.6)
    d.add(f'<circle cx="178" cy="{pcy - 5}" r="5" fill="#2a3644" stroke="#10151b"/>')
    d.text("ID", "silk", 178, pcy + 12, 9, "#8a8f96", anchor="middle", ls=0.6)
    d.add(f'<rect x="200" y="{pcy - 9}" width="22" height="9" rx="1" fill="#0d0e10" stroke="#4a4f56"/>')
    d.add(f'<rect x="203" y="{pcy - 7}" width="16" height="3" fill="#3b78d1"/>')
    d.text("USB", "silk", 211, pcy + 12, 9, "#8a8f96", anchor="middle", ls=0.6)

    masking(d, "do not unplug!", 352, y + 206, 20, -4.2)

    for row in range(2):  # intake vents along the bottom
        for i in range(25):
            vx = 64 + i * 17 + (8 if row else 0)
            d.add(f'<rect x="{vx}" y="{y + 233 + row * 8}" width="10" height="3.5" rx="1.75" fill="#141518"/>')

    # nine 3.5" bays, two of them blanks
    d.defs.append('<pattern id="mesh" width="5" height="5" patternUnits="userSpaceOnUse">'
                  '<rect width="5" height="5" fill="#24272c"/><circle cx="2.5" cy="2.5" r="1.25" fill="#0b0c0e"/></pattern>')
    bx0, by0, bw, bh, g = 504, y + 20, 88, 68, 6
    for idx in range(9):
        r, c = divmod(idx, 3)
        x, yy = bx0 + c * (bw + g), by0 + r * (bh + g)
        if idx in (5, 7):
            d.add(f'<rect x="{x}" y="{yy}" width="{bw}" height="{bh}" rx="2.5" fill="#222428" stroke="#0f1012"/>')
            for k in range(1, 5):
                d.add(f'<line x1="{x + 8}" x2="{x + bw - 8}" y1="{yy + k * bh / 5:.1f}" y2="{yy + k * bh / 5:.1f}" stroke="#18191c" stroke-width="2"/>')
            continue
        d.add(f'<rect x="{x}" y="{yy}" width="{bw}" height="{bh}" rx="2.5" fill="#1d1f23" stroke="#0f1012"/>')
        d.add(f'<rect x="{x + 6}" y="{yy + 7}" width="58" height="{bh - 14}" rx="1.5" fill="url(#mesh)"/>')
        d.add(f'<rect x="{x + 68}" y="{yy + 5}" width="15" height="{bh - 10}" rx="2" fill="#34383e"/>')
        d.add(f'<rect x="{x + 73.5}" y="{yy + 27}" width="4" height="16" rx="1" fill="#1a1b1e"/>')
        led(d, x + 75.5, yy + 13, C["led_green"], r=1.9)


def banner():
    d = Doc(380, "Jacob Pugh",
            "The front of a server rack. A label-maker label on a server reads JACOB PUGH, a yellow label under it "
            "reads INFRASTRUCTURE & AUTOMATION, and a strip of masking tape says do not unplug. "
            "Patch cables run from the switch above it up out of the frame.", seed="banner")
    rack(d, top_u=42, top_y=-24)
    server(d, 104)
    switch(d, 40)  # last, so its cables hang in front of everything
    return d


def homelab():
    stages = [("GIT", "one repo"), ("GITHUB ACTIONS", "plan on PR"), ("OPENTOFU", "proxmox VMs"),
              ("ANSIBLE", "OS + tailscale"), ("K3S", "3 nodes"), ("FLUX", "gitops + sops")]
    d = Doc(172, "Homelab pipeline",
            "Labels on a rack panel, joined by hand-drawn arrows: GIT (one repo), GITHUB ACTIONS (plan on PR), "
            "OPENTOFU (proxmox VMs), ANSIBLE (OS + tailscale), K3S (3 nodes), FLUX (gitops + sops).", seed="homelab")
    rack(d, top_u=32, top_y=-42)
    y = 22
    unit(d, y, 2)
    size, ls = 17, 0.8
    widths = [tape_size(t, size, ls)[0] for t, _ in stages]
    left, right = 74, W - 74
    gap = (right - left - sum(widths)) / (len(stages) - 1)
    x, spans = left, []
    for (t, note), w in zip(stages, widths):
        cx, cy = x + w / 2, y + 50 + d.rng.uniform(-2, 2)
        tape(d, t, size, C["white"], cx=cx, cy=cy, rot=d.rng.uniform(-1.6, 1.6), ls=ls)
        half = measure("hand", note, 14) / 2 + 4
        nx = min(max(cx, EAR_X0 + EAR_W + 14 + half), W - EAR_X0 - EAR_W - 14 - half)  # keep notes off the ears
        d.text(note, "hand", nx, y + 101, 14, C["paint"], anchor="middle", rot=d.rng.uniform(-2.5, 2.5))
        spans.append((x, x + w, cy))
        x += w + gap
    for (_, r0, y0), (l1, _, y1) in zip(spans, spans[1:]):
        arrow(d, r0 + 9, y0 + d.rng.uniform(-2, 2), l1 - 9, y1 + d.rng.uniform(-2, 2))
    return d


def stack():
    groups = [
        ("infra", C["white"], ["PROXMOX", "ROCKY LINUX", "DEBIAN", "ARCH", "OPENTOFU", "TERRAFORM", "ANSIBLE",
                               "K3S", "KUBERNETES", "FLUX", "DOCKER", "TAILSCALE", "NGINX", "CADDY", "GITHUB ACTIONS"]),
        ("cloud + data", C["yellow"], ["GCP", "AZURE", "FIREBASE", "POSTGRES", "NEO4J", "SALESFORCE"]),
        ("code", C["green"], ["PYTHON", "C# / .NET", "TYPESCRIPT", "JAVA", "BASH", "NEXT.JS", "REACT", "FLUTTER"]),
    ]
    size, ls, hgap, pitch, group_gap = 15, 0.7, 11, 38, 12
    x0, x1 = 198, W - 64

    def wrap(items, limit):
        out, row, used = [], [], 0
        for t, w in items:
            if row and used + w > limit:
                out.append(row)
                row, used = [], 0
            row.append((t, w))
            used += w + hgap
        return out + [row]

    rows = []  # (group index, [(text, width)])
    for gi, (_, _, names) in enumerate(groups):
        items = [(t, tape_size(t, size, ls)[0]) for t in names]
        need = len(wrap(items, x1 - x0))
        limit = sum(w + hgap for _, w in items) / need  # shortest width that still fits in `need` rows
        while len(wrap(items, limit)) > need:
            limit += 4
        rows += [(gi, row) for row in wrap(items, limit)]
    content = len(rows) * pitch + (len(groups) - 1) * group_gap
    n_u = math.ceil((content + 36) / U)

    names = " ".join(t for _, _, items in groups for t in items)
    d = Doc(22 + n_u * U + 20 + 16, "Stack", "Label-maker labels on a rack panel: " + names, seed="stack")
    rack(d, top_u=24, top_y=-42)
    y = 22
    unit(d, y, n_u)
    cy = y + (n_u * U - content) / 2 + pitch / 2
    last = None
    for gi, row in rows:
        if last is not None and gi != last:
            cy += group_gap
        if gi != last:
            d.text(groups[gi][0], "hand", 68, cy + 7, 19, C["paint"], rot=d.rng.uniform(-4, -1.5))
        x = x0
        for t, w in row:
            tape(d, t, size, groups[gi][1], left=x, cy=cy + d.rng.uniform(-1.5, 1.5), rot=d.rng.uniform(-1.5, 1.5), ls=ls)
            x += w + hgap
        last = gi
        cy += pitch
    # bottom of the rack
    base = 22 + n_u * U + 20
    d.add(f'<rect y="{base}" width="{W}" height="16" fill="#1d1f22"/>')
    d.add(f'<line x2="{W}" y1="{base + 0.5}" y2="{base + 0.5}" stroke="#34373c"/>')
    return d


for name, make in (("banner", banner), ("homelab", homelab), ("stack", stack)):
    with open(f"{OUT_DIR}/{name}.svg", "w") as fh:
        fh.write(make().svg())
    print("wrote", name)
