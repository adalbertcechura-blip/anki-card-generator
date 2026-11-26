# -*- coding: utf-8 -*-
"""
Generates the private Duolingo-inspired gamified version (pro/index.html)
from Karty.html without modifying the public Karty.html / index.html.
"""
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRO_DIR = os.path.join(BASE_DIR, "pro")
SRC_HTML = os.path.join(BASE_DIR, "Karty.html")
OUT_HTML = os.path.join(PRO_DIR, "index.html")

os.makedirs(PRO_DIR, exist_ok=True)

icon_src = os.path.join(BASE_DIR, "ikona.png")
icon_dst = os.path.join(PRO_DIR, "ikona.png")
if os.path.exists(icon_src):
    shutil.copy2(icon_src, icon_dst)

with open(SRC_HTML, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace(
    "<title>Karty – Chytrý přehrávač kartiček</title>",
    "<title>Karty Pro – Studijní aréna</title>",
)

PRO_CSS = r"""
/* --- KARTY PRO FOREST-MUSHROOM & DUOLINGO-STYLE DESIGN SYSTEM --- */
:root {
  --bg-main: #12100d;
  --bg-card: #191611;
  --bg-card-hover: #211d17;
  --bg-surface: #25211a;
  --border-color: rgba(188, 174, 146, 0.12);
  --border-highlight: rgba(125, 168, 114, 0.28);
  --accent: #6ea065;
  --accent-hover: #5b8b53;
  --accent-soft: rgba(110, 160, 101, 0.14);
  --text-main: #eae4d7;
  --text-muted: #989080;
  --cnt-new: #8ab4a8;
  --cnt-learn: #d48c6a;
  --cnt-rev: #6ea065;
  --hm-1: #2f422b;
  --hm-2: #44663e;
  --hm-3: #5b8853;
  --hm-4: #79b070;
  --radius: 12px;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.22);
}
.anki-count-new { color: var(--cnt-new) !important; }
.anki-count-learn { color: var(--cnt-learn) !important; }
.anki-count-rev { color: var(--cnt-rev) !important; }
.hm-cell.l1 { background: var(--hm-1) !important; }
.hm-cell.l2 { background: var(--hm-2) !important; }
.hm-cell.l3 { background: var(--hm-3) !important; }
.hm-cell.l4 { background: var(--hm-4) !important; }
body.theme-moss {
  --bg-main: #0c1211; --bg-card: #121a18; --bg-card-hover: #17211f; --bg-surface: #1b2624;
  --border-color: rgba(167, 210, 198, 0.1); --border-highlight: rgba(167, 210, 198, 0.22);
  --accent: #52b79a; --accent-hover: #3ea386; --accent-soft: rgba(82, 183, 154, 0.14);
  --text-main: #e3ece9; --text-muted: #849993;
  --cnt-new: #7dd3fc; --cnt-learn: #e09f7d; --cnt-rev: #52b79a;
  --hm-1: #163d33; --hm-2: #215e4e; --hm-3: #318771; --hm-4: #52b79a;
}
body.theme-midnight {
  --bg-main: #0b101b; --bg-card: #111827; --bg-card-hover: #162033; --bg-surface: #1b273d;
  --border-color: rgba(147, 179, 230, 0.11); --border-highlight: rgba(147, 179, 230, 0.22);
  --accent: #6da3e8; --accent-hover: #538dd8; --accent-soft: rgba(109, 163, 232, 0.14);
  --text-main: #e2e9f4; --text-muted: #8293ad;
  --cnt-new: #93c5fd; --cnt-learn: #e5989b; --cnt-rev: #6da3e8;
  --hm-1: #1a2c4a; --hm-2: #274473; --hm-3: #3b68ab; --hm-4: #6da3e8;
}
body.theme-amber {
  --bg-main: #13100d; --bg-card: #1b1612; --bg-card-hover: #221c17; --bg-surface: #29221c;
  --border-color: rgba(224, 184, 138, 0.11); --border-highlight: rgba(224, 184, 138, 0.22);
  --accent: #d49b5a; --accent-hover: #be8442; --accent-soft: rgba(212, 155, 90, 0.14);
  --text-main: #efe7de; --text-muted: #9e8f80;
  --cnt-new: #e5c185; --cnt-learn: #d97c6c; --cnt-rev: #d49b5a;
  --hm-1: #3b2a19; --hm-2: #5c4024; --hm-3: #8c6236; --hm-4: #d49b5a;
}
body.theme-heather {
  --bg-main: #120e14; --bg-card: #19141c; --bg-card-hover: #211a25; --bg-surface: #271f2c;
  --border-color: rgba(196, 167, 210, 0.11); --border-highlight: rgba(196, 167, 210, 0.24);
  --accent: #a67db8; --accent-hover: #9167a3; --accent-soft: rgba(166, 125, 184, 0.14);
  --text-main: #ece5ef; --text-muted: #988b9e;
  --cnt-new: #c4b5fd; --cnt-learn: #e598b2; --cnt-rev: #a67db8;
  --hm-1: #2e2038; --hm-2: #4b335c; --hm-3: #724d8c; --hm-4: #a67db8;
}
body.theme-lichen {
  --bg-main: #10120c; --bg-card: #171a12; --bg-card-hover: #1e2218; --bg-surface: #252a1d;
  --border-color: rgba(188, 201, 148, 0.11); --border-highlight: rgba(188, 201, 148, 0.24);
  --accent: #95a864; --accent-hover: #809350; --accent-soft: rgba(149, 168, 100, 0.14);
  --text-main: #e9ece2; --text-muted: #8f9682;
  --cnt-new: #b7c98b; --cnt-learn: #d48c6a; --cnt-rev: #95a864;
  --hm-1: #2a331b; --hm-2: #44522a; --hm-3: #687d40; --hm-4: #95a864;
}
body.theme-mono {
  --bg-main: #0c0d0f; --bg-card: #131518; --bg-card-hover: #191c20; --bg-surface: #1f2328;
  --border-color: rgba(203, 213, 225, 0.1); --border-highlight: rgba(203, 213, 225, 0.2);
  --accent: #a8b5c4; --accent-hover: #c4ceda; --accent-soft: rgba(168, 181, 196, 0.14);
  --text-main: #e6eaef; --text-muted: #87919e;
  --cnt-new: #cbd5e1; --cnt-learn: #94a3b8; --cnt-rev: #e2e8f0;
  --hm-1: #23272e; --hm-2: #3b424d; --hm-3: #646f80; --hm-4: #a8b5c4;
}
body.theme-ocean {
  --bg-main: #061822; --bg-card: rgba(11, 31, 44, 0.84); --bg-card-hover: rgba(17, 43, 59, 0.92); --bg-surface: rgba(21, 53, 71, 0.88);
  --border-color: rgba(56, 189, 248, 0.24); --border-highlight: rgba(56, 189, 248, 0.45);
  --accent: #38bdf8; --accent-hover: #0ea5e9; --accent-soft: rgba(56, 189, 248, 0.18);
  --text-main: #e0f2fe; --text-muted: #7dd3fc;
  --cnt-new: #7dd3fc; --cnt-learn: #fb7185; --cnt-rev: #38bdf8;
  --hm-1: #0c3347; --hm-2: #0369a1; --hm-3: #0ea5e9; --hm-4: #38bdf8;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 500' preserveAspectRatio='none'%3E%3Ccircle cx='960' cy='110' r='54' fill='%237dd3fc' fill-opacity='0.22'/%3E%3Cpath fill='%230284c7' fill-opacity='0.25' d='M0,330Q200,260 400,320T800,310T1200,330L1200,500L0,500Z'/%3E%3Cpath fill='%2338bdf8' fill-opacity='0.22' d='M0,375Q180,320 360,375T720,370T1080,375L1200,385L1200,500L0,500Z'/%3E%3Cpath fill='%230ea5e9' fill-opacity='0.18' d='M0,425Q240,385 480,425T960,420T1200,435L1200,500L0,500Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom center; background-size: cover; background-attachment: fixed;
}
body.theme-desert {
  --bg-main: #1c100a; --bg-card: rgba(36, 22, 14, 0.84); --bg-card-hover: rgba(45, 29, 20, 0.92); --bg-surface: rgba(56, 36, 25, 0.88);
  --border-color: rgba(245, 158, 11, 0.24); --border-highlight: rgba(245, 158, 11, 0.45);
  --accent: #f59e0b; --accent-hover: #d97706; --accent-soft: rgba(245, 158, 11, 0.18);
  --text-main: #fef3c7; --text-muted: #d6a87c;
  --cnt-new: #fde68a; --cnt-learn: #f87171; --cnt-rev: #f59e0b;
  --hm-1: #451a03; --hm-2: #92400e; --hm-3: #d97706; --hm-4: #fbbf24;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 500' preserveAspectRatio='none'%3E%3Ccircle cx='940' cy='120' r='62' fill='%23fbbf24' fill-opacity='0.28'/%3E%3Cpath fill='%23d97706' fill-opacity='0.24' d='M0,320Q280,210 580,305T1200,280L1200,500L0,500Z'/%3E%3Cpath fill='%23b45309' fill-opacity='0.22' d='M0,380Q380,295 780,375T1200,350L1200,500L0,500Z'/%3E%3Cpath fill='%2392400e' fill-opacity='0.20' d='M0,435Q320,390 660,435T1200,425L1200,500L0,500Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom center; background-size: cover; background-attachment: fixed;
}
body.theme-rainforest {
  --bg-main: #061810; --bg-card: rgba(11, 32, 22, 0.84); --bg-card-hover: rgba(17, 46, 32, 0.92); --bg-surface: rgba(22, 59, 41, 0.88);
  --border-color: rgba(52, 211, 153, 0.24); --border-highlight: rgba(52, 211, 153, 0.45);
  --accent: #10b981; --accent-hover: #059669; --accent-soft: rgba(16, 185, 129, 0.18);
  --text-main: #d1fae5; --text-muted: #6ee7b7;
  --cnt-new: #6ee7b7; --cnt-learn: #fb923c; --cnt-rev: #10b981;
  --hm-1: #064e3b; --hm-2: #047857; --hm-3: #10b981; --hm-4: #34d399;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500' preserveAspectRatio='none'%3E%3Cpath fill='%2310b981' fill-opacity='0.20' d='M0,500 C35,340 110,250 230,210 C150,290 120,390 115,500 Z M800,500 C750,320 670,240 550,200 C640,285 680,390 695,500 Z'/%3E%3Cpath fill='%23059669' fill-opacity='0.18' d='M120,500 C170,380 250,310 340,290 C260,360 220,430 210,500 Z M680,500 C630,380 550,315 460,295 C540,360 580,430 590,500 Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom center; background-size: cover; background-attachment: fixed;
}
body.theme-space {
  --bg-main: #060514; --bg-card: rgba(14, 12, 34, 0.84); --bg-card-hover: rgba(23, 20, 61, 0.92); --bg-surface: rgba(30, 26, 74, 0.88);
  --border-color: rgba(167, 139, 250, 0.25); --border-highlight: rgba(167, 139, 250, 0.48);
  --accent: #a78bfa; --accent-hover: #8b5cf6; --accent-soft: rgba(167, 139, 250, 0.18);
  --text-main: #ede9fe; --text-muted: #a5b4fc;
  --cnt-new: #c4b5fd; --cnt-learn: #f472b6; --cnt-rev: #a78bfa;
  --hm-1: #2e1065; --hm-2: #5b21b6; --hm-3: #7c3aed; --hm-4: #a78bfa;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3Ccircle cx='90' cy='90' r='2.5' fill='%23fff' fill-opacity='0.55'/%3E%3Ccircle cx='210' cy='50' r='2' fill='%23fff' fill-opacity='0.45'/%3E%3Ccircle cx='350' cy='110' r='1.8' fill='%23fff' fill-opacity='0.4'/%3E%3Ccircle cx='660' cy='110' r='44' fill='%23a78bfa' fill-opacity='0.24'/%3E%3Cellipse cx='660' cy='110' rx='78' ry='16' transform='rotate(-18 660 110)' fill='none' stroke='%23c4b5fd' stroke-opacity='0.38' stroke-width='3'/%3E%3Ccircle cx='140' cy='350' r='2.4' fill='%23fff' fill-opacity='0.45'/%3E%3Ccircle cx='510' cy='380' r='2' fill='%23fff' fill-opacity='0.45'/%3E%3Ccircle cx='280' cy='250' r='1.5' fill='%23c4b5fd' fill-opacity='0.4'/%3E%3Ccircle cx='730' cy='310' r='2.2' fill='%23fff' fill-opacity='0.45'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: center; background-size: cover; background-attachment: fixed;
}
body.theme-lofi {
  --bg-main: #130d1d; --bg-card: rgba(27, 20, 41, 0.84); --bg-card-hover: rgba(37, 27, 56, 0.92); --bg-surface: rgba(47, 34, 71, 0.88);
  --border-color: rgba(244, 114, 182, 0.24); --border-highlight: rgba(244, 114, 182, 0.45);
  --accent: #f472b6; --accent-hover: #ec4899; --accent-soft: rgba(244, 114, 182, 0.18);
  --text-main: #fce7f3; --text-muted: #d8b4fe;
  --cnt-new: #d8b4fe; --cnt-learn: #fb7185; --cnt-rev: #f472b6;
  --hm-1: #500724; --hm-2: #9d174d; --hm-3: #db2777; --hm-4: #f472b6;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500' preserveAspectRatio='none'%3E%3Ccircle cx='640' cy='105' r='48' fill='%23f472b6' fill-opacity='0.24'/%3E%3Ccircle cx='150' cy='350' r='70' fill='%23a855f7' fill-opacity='0.18'/%3E%3Cpath fill='%23f472b6' fill-opacity='0.18' d='M0,410L120,350L240,390L380,320L540,375L680,335L800,365L800,500L0,500Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom center; background-size: cover; background-attachment: fixed;
}
body.theme-cottage {
  --bg-main: #181710; --bg-card: rgba(34, 32, 22, 0.85); --bg-card-hover: rgba(44, 42, 29, 0.92); --bg-surface: rgba(54, 51, 35, 0.88);
  --border-color: rgba(190, 209, 138, 0.24); --border-highlight: rgba(190, 209, 138, 0.44);
  --accent: #a3be67; --accent-hover: #8ca850; --accent-soft: rgba(163, 190, 103, 0.18);
  --text-main: #f3f0e0; --text-muted: #bdb79c;
  --cnt-new: #d9e3b3; --cnt-learn: #d98b6c; --cnt-rev: #a3be67;
  --hm-1: #2f3818; --hm-2: #4f5e28; --hm-3: #768c3d; --hm-4: #a3be67;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500' preserveAspectRatio='none'%3E%3Cpath fill='%23a3be67' fill-opacity='0.18' d='M0,430Q250,360 520,415T800,390L800,500L0,500Z'/%3E%3Ccircle cx='120' cy='410' r='26' fill='%23d49b5a' fill-opacity='0.25'/%3E%3Crect x='113' y='410' width='14' height='36' rx='4' fill='%23f3f0e0' fill-opacity='0.22'/%3E%3Cpath fill='%23a3be67' fill-opacity='0.24' d='M660,500 C660,410 700,350 750,320 C720,390 710,450 710,500 Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom center; background-size: cover; background-attachment: fixed;
}
body.theme-cats {
  --bg-main: #181214; --bg-card: rgba(34, 25, 28, 0.85); --bg-card-hover: rgba(45, 33, 37, 0.92); --bg-surface: rgba(54, 40, 45, 0.88);
  --border-color: rgba(244, 162, 158, 0.24); --border-highlight: rgba(244, 162, 158, 0.45);
  --accent: #f4a29e; --accent-hover: #e58782; --accent-soft: rgba(244, 162, 158, 0.18);
  --text-main: #fdf2f2; --text-muted: #d6b2b0;
  --cnt-new: #fbcfe8; --cnt-learn: #fb7185; --cnt-rev: #f4a29e;
  --hm-1: #4c1d24; --hm-2: #88333f; --hm-3: #c45a68; --hm-4: #f4a29e;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3Cg fill='%23f4a29e' fill-opacity='0.24'%3E%3Cpath d='M560,480 C560,415 595,380 620,380 C645,380 680,415 680,480 Z'/%3E%3Ccircle cx='620' cy='355' r='34'/%3E%3Cpolygon points='592,335 586,295 612,324'/%3E%3Cpolygon points='648,335 654,295 628,324'/%3E%3Cpath d='M676,465 Q730,445 725,395' fill='none' stroke='%23f4a29e' stroke-opacity='0.24' stroke-width='12' stroke-linecap='round'/%3E%3Ccircle cx='140' cy='410' r='10'/%3E%3Ccircle cx='122' cy='394' r='5'/%3E%3Ccircle cx='140' cy='386' r='5'/%3E%3Ccircle cx='158' cy='394' r='5'/%3E%3C/g%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom right; background-size: cover; background-attachment: fixed;
}
body.theme-mountains {
  --bg-main: #09131a; --bg-card: rgba(14, 28, 38, 0.84); --bg-card-hover: rgba(20, 40, 54, 0.92); --bg-surface: rgba(25, 49, 66, 0.88);
  --border-color: rgba(125, 211, 252, 0.22); --border-highlight: rgba(125, 211, 252, 0.44);
  --accent: #67e8f9; --accent-hover: #22d3ee; --accent-soft: rgba(103, 232, 249, 0.16);
  --text-main: #ecfeff; --text-muted: #99d5e2;
  --cnt-new: #a5f3fc; --cnt-learn: #fda4af; --cnt-rev: #67e8f9;
  --hm-1: #0e3a46; --hm-2: #155e75; --hm-3: #0891b2; --hm-4: #67e8f9;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 500' preserveAspectRatio='none'%3E%3Ccircle cx='220' cy='100' r='36' fill='%23ecfeff' fill-opacity='0.22'/%3E%3Cpolygon fill='%230891b2' fill-opacity='0.26' points='0,500 220,230 440,500'/%3E%3Cpolygon fill='%2322d3ee' fill-opacity='0.22' points='300,500 620,160 940,500'/%3E%3Cpolygon fill='%2306b6d4' fill-opacity='0.24' points='720,500 980,210 1200,500'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom center; background-size: cover; background-attachment: fixed;
}
body.theme-sakura {
  --bg-main: #180f16; --bg-card: rgba(34, 21, 31, 0.85); --bg-card-hover: rgba(46, 28, 42, 0.92); --bg-surface: rgba(56, 35, 51, 0.88);
  --border-color: rgba(249, 168, 212, 0.24); --border-highlight: rgba(249, 168, 212, 0.45);
  --accent: #f9a8d4; --accent-hover: #f472b6; --accent-soft: rgba(249, 168, 212, 0.18);
  --text-main: #fdf2f8; --text-muted: #e5b3d1;
  --cnt-new: #fbcfe8; --cnt-learn: #fb7185; --cnt-rev: #f9a8d4;
  --hm-1: #500724; --hm-2: #9d174d; --hm-3: #ec4899; --hm-4: #f9a8d4;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3Cpath d='M0,120 Q220,150 380,80' fill='none' stroke='%239d174d' stroke-opacity='0.35' stroke-width='10' stroke-linecap='round'/%3E%3Ccircle cx='120' cy='115' r='16' fill='%23f9a8d4' fill-opacity='0.28'/%3E%3Ccircle cx='210' cy='130' r='19' fill='%23f472b6' fill-opacity='0.24'/%3E%3Ccircle cx='310' cy='95' r='15' fill='%23f9a8d4' fill-opacity='0.28'/%3E%3Ccircle cx='520' cy='210' r='6' fill='%23f9a8d4' fill-opacity='0.25'/%3E%3Ccircle cx='630' cy='290' r='7' fill='%23f472b6' fill-opacity='0.24'/%3E%3Ccircle cx='430' cy='340' r='5' fill='%23f9a8d4' fill-opacity='0.25'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: top left; background-size: cover; background-attachment: fixed;
}
body.theme-lighthouse {
  --bg-main: #08101c; --bg-card: rgba(13, 22, 38, 0.85); --bg-card-hover: rgba(19, 32, 54, 0.92); --bg-surface: rgba(24, 40, 68, 0.88);
  --border-color: rgba(250, 204, 21, 0.22); --border-highlight: rgba(250, 204, 21, 0.44);
  --accent: #facc15; --accent-hover: #eab308; --accent-soft: rgba(250, 204, 21, 0.16);
  --text-main: #fefce8; --text-muted: #93c5fd;
  --cnt-new: #93c5fd; --cnt-learn: #fb7185; --cnt-rev: #facc15;
  --hm-1: #3b2f06; --hm-2: #71590b; --hm-3: #b58d12; --hm-4: #facc15;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 500' preserveAspectRatio='none'%3E%3Cpolygon fill='%23facc15' fill-opacity='0.14' points='760,175 180,60 180,290'/%3E%3Crect x='740' y='175' width='40' height='155' fill='%23e2e8f0' fill-opacity='0.25'/%3E%3Crect x='745' y='150' width='30' height='25' fill='%23facc15' fill-opacity='0.45'/%3E%3Cpolygon fill='%231e293b' fill-opacity='0.55' points='620,500 710,330 840,330 920,500'/%3E%3Cpath fill='%2338bdf8' fill-opacity='0.18' d='M0,430Q250,395 500,430T1000,425L1000,500L0,500Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: bottom center; background-size: cover; background-attachment: fixed;
}
.theme-preview-bar {
  position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%);
  z-index: 400; display: none; flex-direction: column; align-items: center; gap: 8px;
  width: min(340px, calc(100vw - 24px)); text-align: center;
  background: var(--bg-card); border: 1px solid var(--accent);
  border-radius: 14px; padding: 12px 14px; box-shadow: 0 10px 28px rgba(0,0,0,0.6);
  backdrop-filter: blur(8px);
}
.theme-preview-bar.active { display: flex; }
#btnHelp, header .nav-actions { display: none !important; }
body.studying-active .pro-hud { display: none !important; }
header {
  background: var(--bg-main);
  border-bottom: 1px solid var(--border-color);
  padding: 10px 14px;
}
.heatmap-container, .deck-list, .drop-zone, .flashcard, .modal-content {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.drop-zone {
  border-style: dashed;
  border-color: var(--border-highlight);
}
.pro-hud {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.pro-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 999px;
  padding: 3px 9px;
  font-size: 0.74rem;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
}
.pro-pill.points { color: var(--accent); border-color: var(--border-highlight); }
.pro-pill.boost { color: var(--accent); background: var(--accent-soft); border-color: var(--border-highlight); }
.pro-pill.level, .pro-pill.streak { color: var(--text-main); }

/* Tactile 3D Duolingo-inspired buttons */
.btn, .btn-flip, .btn-rate {
  border-radius: 10px;
  transition: transform 0.08s ease, background 0.15s ease, border-color 0.15s ease !important;
}
.btn-primary, .btn-flip {
  border-bottom: 4px solid rgba(0, 0, 0, 0.35) !important;
}
.btn-rate {
  border-bottom-width: 4px !important;
}
.btn:active, .btn-flip:active, .btn-rate:active {
  transform: translateY(2px);
  border-bottom-width: 2px !important;
}

/* Pro Dashboard & Mascot */
.pro-dashboard {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 12px 14px;
  display: grid;
  grid-template-columns: auto 1fr 1fr;
  align-items: center;
  gap: 14px;
  box-shadow: var(--shadow);
}
.pro-mascot-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}
.pro-mascot-svg {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  transition: transform 0.25s ease;
}
.pro-mascot-svg.bounce {
  animation: mascotBounce 0.45s ease;
}
@keyframes mascotBounce {
  0%, 100% { transform: translateY(0) scale(1); }
  45% { transform: translateY(-5px) scale(1.06); }
}
.pro-dash-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.pro-dash-top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-main);
}
.pro-bar-track {
  width: 100%;
  height: 6px;
  background: var(--bg-surface);
  border-radius: 999px;
  overflow: hidden;
}
.pro-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.pro-bar-xp { background: var(--accent); opacity: 0.65; }
.pro-bar-goal { background: var(--accent); }

.pro-quests-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}
.pro-quest-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 9px 11px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.76rem;
  color: var(--text-main);
}
.pro-quest-card.ready {
  border-color: var(--accent);
  background: var(--accent-soft);
}
.pro-quest-card.done {
  border-color: var(--border-highlight);
  opacity: 0.78;
}

.pro-combo-badge {
  display: none;
  align-items: center;
  padding: 2px 9px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--accent);
  background: var(--accent-soft);
  border: 1px solid var(--border-highlight);
  animation: popIn 0.2s ease;
}
.pro-combo-badge.hot {
  animation: comboPulse 0.9s infinite ease-in-out;
}
@keyframes comboPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.07); }
}
@keyframes popIn {
  from { transform: scale(0.88); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.pro-confetti-piece {
  position: fixed;
  width: 7px;
  height: 7px;
  top: -12px;
  z-index: 500;
  pointer-events: none;
  border-radius: 2px;
  animation: confettiFall 1.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}
@keyframes confettiFall {
  0% { transform: translateY(0) rotate(0deg); opacity: 0.95; }
  100% { transform: translateY(100vh) rotate(540deg); opacity: 0; }
}
.hm-cell.frozen {
  background: var(--accent) !important;
  opacity: 0.55;
}
.pro-toast {
  position: fixed;
  bottom: 84px;
  left: 50%;
  transform: translateX(-50%) translateY(14px);
  background: var(--bg-surface);
  border: 1px solid var(--border-highlight);
  color: var(--text-main);
  padding: 7px 14px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  z-index: 300;
  opacity: 0;
  pointer-events: none;
  transition: all 0.22s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
  white-space: nowrap;
}
.pro-toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
.shop-grid { display: flex; flex-direction: column; gap: 8px; }
.shop-item {
  display: flex; justify-content: space-between; align-items: center; gap: 10px;
  background: var(--bg-surface); border: 1px solid var(--border-color);
  border-radius: 10px; padding: 10px 12px;
}
.shop-item-info { display: flex; flex-direction: column; gap: 2px; }
.shop-item-title { font-weight: 600; font-size: 0.88rem; color: var(--text-main); }
.shop-item-desc { font-size: 0.75rem; color: var(--text-muted); }
.milestone-row {
  display: flex; justify-content: space-between; align-items: center; gap: 8px;
  padding: 7px 10px; border-radius: 8px; background: var(--bg-surface);
  border: 1px solid var(--border-color); font-size: 0.8rem;
}
.milestone-row.claimed { border-color: var(--border-highlight); background: var(--accent-soft); }

/* Language & Interactive Modes */
.cloze-blank {
  display: inline-block; padding: 1px 8px; border-radius: 6px;
  background: var(--accent-soft); border: 1px dashed var(--border-highlight);
  color: var(--accent); font-weight: 700;
}
.cloze-reveal {
  display: inline-block; padding: 1px 6px; border-radius: 6px;
  background: var(--accent-soft); color: var(--accent); font-weight: 700;
}
.quiz-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px;
}
.quiz-option {
  background: var(--bg-surface); color: var(--text-main);
  border: 1px solid var(--border-color); border-bottom: 3px solid rgba(0,0,0,0.3);
  border-radius: 10px; padding: 11px 14px; font-size: 0.94rem;
  font-weight: 600; text-align: left; cursor: pointer; transition: all 0.12s ease;
}
.quiz-option:hover:not(:disabled) { border-color: var(--accent); background: var(--bg-card-hover); }
.quiz-option.correct { background: rgba(110, 160, 101, 0.25); border-color: var(--accent); color: var(--text-main); }
.quiz-option.wrong { background: rgba(220, 90, 90, 0.22); border-color: #d86565; color: #f5b5b5; }
.card-audio-player { width: 100%; max-width: 340px; height: 36px; margin: 6px auto; display: block; }
.type-hint-box {
  font-size: 0.86rem; color: var(--accent); font-family: monospace;
  letter-spacing: 0.08em; padding: 4px 8px; background: var(--accent-soft); border-radius: 6px;
}

/* Matching Pairs Grid */
.match-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
.match-col { display: flex; flex-direction: column; gap: 8px; }
.match-btn {
  background: var(--bg-surface); color: var(--text-main); border: 1px solid var(--border-color);
  border-bottom: 3px solid rgba(0,0,0,0.28); border-radius: 10px; padding: 10px 12px;
  font-size: 0.88rem; font-weight: 600; text-align: left; cursor: pointer;
}
.match-btn.selected { border-color: var(--accent); background: var(--accent-soft); }
.match-btn.matched { opacity: 0.4; pointer-events: none; border-color: var(--accent); }
.match-btn.err { border-color: #d86565; background: rgba(220, 90, 90, 0.2); }

/* Skill Path Nodes */
.skill-path-list { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 8px 0; }
.skill-node {
  width: min(260px, 100%); display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; border-radius: 14px; background: var(--bg-surface);
  border: 1px solid var(--border-color); border-bottom: 4px solid rgba(0,0,0,0.32);
  cursor: pointer; transition: transform 0.1s ease;
}
.skill-node:nth-child(odd) { transform: translateX(-14px); }
.skill-node:nth-child(even) { transform: translateX(14px); }
.skill-node.completed { border-color: var(--accent); background: var(--accent-soft); }

/* Mini-games Hub & Arenas */
.games-menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
.game-tile {
  background: var(--bg-surface); border: 1px solid var(--border-color);
  border-bottom: 3px solid rgba(0,0,0,0.3); border-radius: 12px;
  padding: 12px; text-align: left; cursor: pointer; color: var(--text-main);
  display: flex; flex-direction: column; gap: 4px;
}
.game-tile:hover { border-color: var(--accent); background: var(--bg-card-hover); }
.boss-hp-track {
  width: 100%; height: 12px; background: var(--bg-main);
  border-radius: 999px; overflow: hidden; border: 1px solid var(--border-color);
}
.boss-hp-fill { height: 100%; background: #c96464; transition: width 0.25s ease; }
.gravity-arena {
  position: relative; width: 100%; height: 260px;
  background: var(--bg-main); border: 1px solid var(--border-color);
  border-radius: 10px; overflow: hidden; margin-bottom: 10px;
}
.gravity-meteor {
  position: absolute; left: 50%; transform: translateX(-50%);
  background: var(--bg-surface); border: 1px solid var(--accent);
  color: var(--text-main); padding: 8px 14px; border-radius: 10px;
  font-weight: 700; font-size: 0.95rem; white-space: nowrap; max-width: 90%;
  overflow: hidden; text-overflow: ellipsis;
}
.scramble-bank, .scramble-answer {
  display: flex; flex-wrap: wrap; gap: 8px; min-height: 44px;
  padding: 8px; border-radius: 10px; background: var(--bg-main);
  border: 1px solid var(--border-color); margin-bottom: 10px;
}
.scramble-chip {
  background: var(--bg-surface); color: var(--text-main);
  border: 1px solid var(--border-highlight); border-bottom: 3px solid rgba(0,0,0,0.3);
  border-radius: 8px; padding: 6px 12px; font-weight: 600; cursor: pointer;
}
.timed-match-grid {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; margin-top: 8px;
}
.match-btn.has-img, .quiz-option.has-img {
  padding: 6px; display: flex; align-items: center; justify-content: center; min-height: 110px;
}
.game-card-img {
  width: 100%; max-height: 120px; border-radius: 8px; object-fit: cover; pointer-events: none; display: block;
}
.game-card-img-lg {
  max-width: 100%; max-height: 240px; border-radius: 10px; object-fit: contain; pointer-events: none; display: block; margin: 0 auto;
}
.game-card-img-meteor {
  max-width: 180px; max-height: 110px; border-radius: 8px; object-fit: cover; pointer-events: none; display: block;
}
@media (max-width: 520px) {
  .games-menu-grid { grid-template-columns: 1fr; }
  .timed-match-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .milestone-add-grid { grid-template-columns: 64px minmax(0, 1fr) !important; }
}
.shop-item, .milestone-row { min-width: 0; }
.shop-item-info { min-width: 0; }
.shop-item .btn-sm { white-space: nowrap; flex-shrink: 0; }

/* Mobile compact heatmap (7-day week bar) */
.pro-week-strip { display: none; }
@media (max-width: 640px) {
  html { font-size: 19px; }
  body { font-size: 1rem; }
  header { flex-wrap: nowrap; justify-content: space-between; gap: 6px; padding: 8px 10px; }
  header .logo { font-size: 17px; white-space: nowrap; flex-shrink: 0; }
  .pro-hud { flex-wrap: nowrap; gap: 4px; overflow-x: auto; scrollbar-width: none; -ms-overflow-style: none; }
  .pro-hud::-webkit-scrollbar { display: none; }
  .pro-pill { padding: 3px 6px; font-size: 12px; white-space: nowrap; flex-shrink: 0; }
  .pro-hud .btn-sm { padding: 4px 8px; font-size: 12px; white-space: nowrap; flex-shrink: 0; }
  .card-text, .flashcard-content, .card-question, .card-answer { font-size: 15px !important; line-height: 1.48 !important; }
  .card-answer h2, .card-question h2 { font-size: 19px !important; }
  .card-answer h3, .card-question h3 { font-size: 16px !important; }
  .deck-item-name { font-size: 1.05rem; }
  .deck-stats { font-size: 0.92rem; }
  .pro-quest-card { font-size: 0.9rem; }
  .study-controls { margin-top: 6px !important; gap: 4px !important; }
  .btn-flip { font-size: 14px !important; padding: 9px 10px !important; border-bottom-width: 2px !important; }
  .btn-side-peek { font-size: 13px !important; padding: 6px 10px !important; }
  .rating-grid { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; gap: 4px !important; }
  .btn-rate {
    font-size: 13px !important; padding: 6px 2px !important; min-height: 0 !important;
    display: flex; flex-direction: column-reverse; align-items: center; justify-content: center; gap: 1px;
    border-bottom-width: 2px !important;
  }
  .btn-rate .interval { font-size: 11px !important; opacity: 0.85; }
  .quiz-option, .match-btn { font-size: 0.96rem; padding: 10px 10px; }
  .pro-dashboard { grid-template-columns: 1fr; gap: 8px; padding: 10px 12px; }
  .pro-quests-strip { grid-template-columns: 1fr; gap: 6px; }
  .quiz-grid { grid-template-columns: 1fr; }
  .heatmap-container.mobile-collapsed .heatmap-scroll-area,
  .heatmap-container.mobile-collapsed .heatmap-stats-bar { display: none; }
  .pro-week-strip { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
  .pro-week-days { display: flex; gap: 6px; }
  .pro-week-dot {
    width: 24px; height: 24px; border-radius: 6px; font-size: 0.68rem; font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center;
    background: var(--bg-surface); color: var(--text-muted); border: 1px solid var(--border-color);
  }
  .pro-week-dot.active { background: var(--accent); color: #12100d; border-color: var(--accent); }
  .pro-week-dot.frozen { background: var(--accent-soft); color: var(--accent); border-color: var(--border-highlight); }
}
"""

PRO_HEADER_HUD = r"""  <div class="pro-hud" id="proHud">
    <span class="pro-pill level" id="proLevelPill" title="Vaše úroveň">Lv. 1</span>
    <span class="pro-pill streak" id="proStreakPill" title="Denní série">Série: 0 d</span>
    <span class="pro-pill points" id="proPointsPill" title="Body">0 b.</span>
    <span class="pro-pill boost" id="proBoostPill" style="display:none;">2x Boost</span>
    <button class="btn btn-sm" id="btnOpenGames" title="Minihry s kartičkami">Minihry</button>
    <button class="btn btn-sm btn-primary" id="btnOpenShop">Obchod</button>
  </div>"""

PRO_DASHBOARD_HTML = r"""
    <div class="pro-dashboard" id="proDashboard">
      <div class="pro-mascot-wrap">
        <svg class="pro-mascot-svg" id="proMascotSvg" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="32" cy="44" rx="11" ry="13" fill="var(--bg-surface)" stroke="var(--border-highlight)" stroke-width="2.5"/>
          <path d="M10 31C10 18 20 10 32 10C44 10 54 18 54 31C54 34 50 36 32 36C14 36 10 34 10 31Z" fill="var(--accent)" stroke="var(--border-highlight)" stroke-width="2"/>
          <circle cx="27" cy="42" r="2.2" fill="var(--text-main)"/>
          <circle cx="37" cy="42" r="2.2" fill="var(--text-main)"/>
          <path id="proMascotMouth" d="M28 48Q32 51 36 48" stroke="var(--text-main)" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <div style="font-size:0.78rem; color:var(--text-muted); max-width:130px;" id="proMascotMsg">Připraven na lekci?</div>
      </div>
      <div class="pro-dash-block">
        <div class="pro-dash-top">
          <span id="proDashRank">Úroveň 1 – Začátečník</span>
          <span id="proDashXpText" style="color:var(--text-muted); font-size:0.76rem;">0 / 45 XP</span>
        </div>
        <div class="pro-bar-track"><div class="pro-bar-fill pro-bar-xp" id="proDashXpBar" style="width:0%;"></div></div>
      </div>
      <div class="pro-dash-block">
        <div class="pro-dash-top">
          <span>Dnešní cíl (min. 1 den)</span>
          <span id="proDashGoalText" style="color:var(--text-muted); font-size:0.76rem;">0 / 20</span>
        </div>
        <div class="pro-bar-track"><div class="pro-bar-fill pro-bar-goal" id="proDashGoalBar" style="width:0%;"></div></div>
      </div>
    </div>
    <div class="pro-quests-strip" id="proQuestsStrip"></div>
"""

PRO_EXTRA_BAR_HTML = r"""
    <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
      <button class="btn btn-sm btn-primary" id="btnProNewCard">+ Nová karta / Rychlý import</button>
    </div>
"""

PRO_MODALS_HTML = r"""
<!-- PRO SHOP & MILESTONES MODAL -->
<div class="modal-overlay" id="shopModal">
  <div class="modal-content" style="width:min(520px, calc(100vw - 16px)); max-width:100%; max-height:88dvh; overflow-y:auto; overflow-x:hidden; box-sizing:border-box;">
    <div class="modal-header">
      <div class="modal-title">Obchod, série a milníky</div>
      <button class="modal-close" id="shopModalClose">&times;</button>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; padding:10px 12px; background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); margin-bottom:12px; flex-wrap:wrap;">
      <div>
        <div style="font-size:0.8rem; color:var(--text-muted);">Dostupné body</div>
        <div id="shopBalanceVal" style="font-size:1.25rem; font-weight:800; color:var(--accent);">0 b.</div>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <label for="selProDailyGoal" style="font-size:0.82rem; color:var(--text-muted);">Denní cíl:</label>
        <select id="selProDailyGoal" class="select-sm">
          <option value="10">10 / den</option>
          <option value="20">20 / den</option>
          <option value="30">30 / den</option>
          <option value="50">50 / den</option>
        </select>
        <label for="selProLessonLen" style="font-size:0.82rem; color:var(--text-muted);">Lekce:</label>
        <select id="selProLessonLen" class="select-sm">
          <option value="10">10 karet</option>
          <option value="12">12 karet</option>
          <option value="15">15 karet</option>
          <option value="0">Vše</option>
        </select>
      </div>
    </div>

    <h4 style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Vylepšení</h4>
    <div class="shop-grid" style="margin-bottom:14px;">
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Streak Freeze (max. 3)</div>
          <div class="shop-item-desc">Automaticky ochrání sérii, pokud některý den vynecháte.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyFreeze">1200 b.</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">2x Body Boost (15 min)</div>
          <div class="shop-item-desc">Zdvojnásobí body ze všech karet po dobu 15 minut.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyBoost">1000 b.</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Obnovení série (max. 3 dny zpět)</div>
          <div class="shop-item-desc">Zpětně zachrání nejbližší vynechaný den za poslední 3 dny.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyRepair">2000 b.</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Tajemná truhla</div>
          <div class="shop-item-desc">Náhodná odměna: +450 až +1700 bodů, Freeze nebo 2x Boost.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyMystery">1100 b.</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Balíček 3x Streak Freeze</div>
          <div class="shop-item-desc">Doplní zásobu Freeze na 3/3 se slevou.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyShieldPack">3000 b.</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Power-up: Zmrazení času</div>
          <div class="shop-item-desc">Zastaví odpočet ve Spojovačce nebo pád v Meteoritech na 10 s.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyTimeFreeze">600 b.</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Power-up: Nápověda 50:50</div>
          <div class="shop-item-desc">Odstraní 2 špatné možnosti v kvízovém režimu (Výběr ze 4).</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyFifty">500 b.</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Power-up: Štít Comba</div>
          <div class="shop-item-desc">Automaticky ochrání vaše Combo při jedné chybě.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyComboShield">750 b.</button>
      </div>
    </div>

    <h4 style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Vzhled aplikace (Monochrom 1500 b. · Minimalistické 3000 b. · Pro 5500 b.)</h4>
    <div class="shop-grid" id="shopThemesList" style="margin-bottom:14px;"></div>

    <h4 style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Nastavitelné milníky série</h4>
    <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:10px;" id="shopMilestonesList"></div>
    <div class="milestone-add-grid" style="display:grid; grid-template-columns:60px minmax(0,1fr) 68px auto; gap:6px; align-items:center;">
      <input type="number" id="inpNewMsDays" min="1" max="3650" value="50" style="min-width:0; width:100%; box-sizing:border-box; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:6px 8px; border-radius:6px; font-size:0.82rem;">
      <input type="text" id="inpNewMsReward" placeholder="Odměna (např. Volný večer)" style="min-width:0; width:100%; box-sizing:border-box; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:6px 8px; border-radius:6px; font-size:0.82rem;">
      <input type="number" id="inpNewMsBonus" min="0" max="10000" value="250" style="min-width:0; width:100%; box-sizing:border-box; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:6px 8px; border-radius:6px; font-size:0.82rem;">
      <button class="btn btn-sm btn-primary" id="btnAddMilestone" style="width:100%;">Přidat</button>
    </div>
  </div>
</div>

<!-- MATCHING PAIRS MODAL -->
<div class="modal-overlay" id="matchModal">
  <div class="modal-content" style="max-width:560px;">
    <div class="modal-header">
      <div class="modal-title" id="matchModalTitle">Párování dvojic</div>
      <button class="modal-close" id="matchModalClose">&times;</button>
    </div>
    <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:8px;" id="matchStatusText">Spojte pojmy vlevo se správnými odpověďmi vpravo.</div>
    <div class="match-columns">
      <div class="match-col" id="matchLeftCol"></div>
      <div class="match-col" id="matchRightCol"></div>
    </div>
    <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:12px;">
      <button class="btn btn-sm btn-primary" id="btnMatchNextRound">Další kolo</button>
    </div>
  </div>
</div>

<!-- SKILL PATH MODAL -->
<div class="modal-overlay" id="skillPathModal">
  <div class="modal-content" style="max-width:440px; max-height:85dvh; overflow-y:auto;">
    <div class="modal-header">
      <div class="modal-title" id="skillPathTitle">Cesta lekcí</div>
      <button class="modal-close" id="skillPathClose">&times;</button>
    </div>
    <div class="skill-path-list" id="skillPathList"></div>
  </div>
</div>

<!-- CARD EDITOR MODAL -->
<div class="modal-overlay" id="cardEditorModal">
  <div class="modal-content" style="max-width:480px;">
    <div class="modal-header">
      <div class="modal-title">Upravit kartu</div>
      <button class="modal-close" id="cardEditorClose">&times;</button>
    </div>
    <div style="display:flex; flex-direction:column; gap:10px;">
      <label style="font-size:0.82rem; color:var(--text-muted);">Název / pojem:<input type="text" id="edCardTitle" style="width:100%; margin-top:4px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:7px; border-radius:6px;"></label>
      <label style="font-size:0.82rem; color:var(--text-muted);">Líc (otázka):<textarea id="edCardFront" rows="3" style="width:100%; margin-top:4px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:7px; border-radius:6px;"></textarea></label>
      <label style="font-size:0.82rem; color:var(--text-muted);">Rub (odpověď):<textarea id="edCardBack" rows="4" style="width:100%; margin-top:4px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:7px; border-radius:6px;"></textarea></label>
      <button class="btn btn-primary" id="btnSaveCardEdit">Uložit změny</button>
    </div>
  </div>
</div>

<!-- QUICK CREATE / TEXT IMPORT MODAL -->
<div class="modal-overlay" id="quickImportModal">
  <div class="modal-content" style="max-width:500px;">
    <div class="modal-header">
      <div class="modal-title">Nová karta / Rychlý textový import</div>
      <button class="modal-close" id="quickImportClose">&times;</button>
    </div>
    <div style="display:flex; flex-direction:column; gap:10px;">
      <label style="font-size:0.82rem; color:var(--text-muted);">Cílový balíček:
        <select id="selQuickDeckTarget" class="select-sm" style="width:100%; margin-top:4px;"></select>
      </label>
      <input type="text" id="inpQuickNewDeckName" placeholder="Název nového balíčku..." style="background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:7px; border-radius:6px;">
      <label style="font-size:0.82rem; color:var(--text-muted);">Řádky ve formátu <strong>otázka ; odpověď</strong> (lze použít i {{c1::doplňovačku}}):
        <textarea id="txtQuickImportLines" rows="6" placeholder="dog ; pes&#10;cat ; kočka&#10;I {{c1::am}} a student ; am" style="width:100%; margin-top:4px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:7px; border-radius:6px;"></textarea>
      </label>
      <button class="btn btn-primary" id="btnRunQuickImport">Přidat kartičky</button>
    </div>
  </div>
</div>

<!-- MINI-GAMES HUB MODAL -->
<div class="modal-overlay" id="gamesModal">
  <div class="modal-content" style="max-width:660px; max-height:90dvh; overflow-y:auto;">
    <div class="modal-header">
      <div class="modal-title" id="gamesModalTitle">Minihry s kartičkami</div>
      <button class="modal-close" id="gamesModalClose">&times;</button>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:10px; flex-wrap:wrap;">
      <select id="selGameDeck" class="select-sm" style="flex:1;"></select>
      <button class="btn btn-sm" id="btnGameBackMenu" style="display:none;">Zpět na výběr her</button>
    </div>

    <div id="gamesMenuPane">
      <div id="gamesUnlockInfo" style="font-size:0.82rem; color:var(--text-muted); margin-bottom:8px;"></div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px;">
        <label style="font-size:0.78rem; color:var(--text-muted);">Otázka (zadání):
          <select id="selGamePromptField" class="select-sm" style="width:100%; margin-top:3px;"></select>
        </label>
        <label style="font-size:0.78rem; color:var(--text-muted);">Odpověď (cíl):
          <select id="selGameAnswerField" class="select-sm" style="width:100%; margin-top:3px;"></select>
        </label>
      </div>
      <div class="games-menu-grid">
        <button class="game-tile" id="btnStartTimedMatch">
          <strong style="font-size:0.95rem;">Spojovačka na čas (5 kol)</strong>
          <span style="font-size:0.76rem; color:var(--text-muted);">5 zrychlujících se kol, průběžně doplňované dvojice (+35 b.)</span>
        </button>
        <button class="game-tile" id="btnStartBossFight">
          <strong style="font-size:0.95rem;">Karetní souboj (Boss)</strong>
          <span style="font-size:0.76rem; color:var(--text-muted);">Porazte bosse balíčku (100 HP) bez ztráty životů (+20 b.)</span>
        </button>
        <button class="game-tile" id="btnStartGravity">
          <strong style="font-size:0.95rem;">Pád karet (Meteority)</strong>
          <span style="font-size:0.76rem; color:var(--text-muted);">Vyberte odpověď dřív, než karta dopadne (+2 b./karta)</span>
        </button>
        <button class="game-tile" id="btnStartScramble">
          <strong style="font-size:0.95rem;">Skládání slov a vět</strong>
          <span style="font-size:0.76rem; color:var(--text-muted);">Poskládejte rozházená písmena nebo slova (+8 b.)</span>
        </button>
      </div>
    </div>

    <div id="gameTimedMatchPane" style="display:none;">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
        <span id="tmRoundLabel" style="font-weight:700; font-size:0.86rem;">Kolo 1/5 · 0/10</span>
        <span id="tmTimerLabel" style="font-weight:700; color:var(--accent);">Čas: 60 s</span>
        <button class="btn btn-sm" id="btnUseTimeFreezeMatch">Zmrazení času</button>
      </div>
      <div class="timed-match-grid" id="tmGrid"></div>
    </div>

    <div id="gameBossPane" style="display:none;">
      <div style="display:flex; justify-content:space-between; font-size:0.84rem; font-weight:700; margin-bottom:4px;">
        <span id="bossNameLabel">Boss</span>
        <span id="bossHpText">100 / 100 HP</span>
      </div>
      <div class="boss-hp-track" style="margin-bottom:8px;"><div class="boss-hp-fill" id="bossHpBar" style="width:100%;"></div></div>
      <div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:10px;">
        <span id="playerBossHpText" style="color:var(--accent); font-weight:700;">Vaše HP: 5 / 5</span>
        <span id="bossComboText" style="color:var(--text-muted);">Combo: 0x</span>
      </div>
      <div id="bossQuestionBox" style="padding:12px; background:var(--bg-main); border:1px solid var(--border-color); border-radius:10px; font-weight:700; margin-bottom:8px;"></div>
      <div class="quiz-grid" id="bossOptionsGrid"></div>
    </div>

    <div id="gameGravityPane" style="display:none;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span id="gravScoreLabel" style="font-weight:700; color:var(--accent);">Skóre: 0</span>
        <button class="btn btn-sm" id="btnUseTimeFreezeGrav">Zmrazení času</button>
      </div>
      <div class="gravity-arena" id="gravArena">
        <div class="gravity-meteor" id="gravMeteor">...</div>
      </div>
      <div class="quiz-grid" id="gravOptionsGrid"></div>
    </div>

    <div id="gameScramblePane" style="display:none;">
      <div id="scramblePromptBox" style="font-weight:700; margin-bottom:8px;"></div>
      <div class="scramble-answer" id="scrambleAnswerBox"></div>
      <div class="scramble-bank" id="scrambleBankBox"></div>
      <div style="display:flex; justify-content:space-between; gap:8px;">
        <button class="btn btn-sm" id="btnScrambleClear">Vymazat</button>
        <button class="btn btn-sm btn-primary" id="btnScrambleNext">Další slovo</button>
      </div>
    </div>
  </div>
</div>

<!-- CLOUD SYNC MODAL -->
<div class="modal-overlay" id="syncModal">
  <div class="modal-content" style="max-width:460px;">
    <div class="modal-header">
      <div class="modal-title">Synchronizace s telefonem</div>
      <button class="modal-close" id="syncModalClose">&times;</button>
    </div>
    <p style="font-size:0.84rem; color:var(--text-muted); line-height:1.45; margin-bottom:10px;">
      Postup se ukládá do vašeho soukromého <strong>GitHub Gistu</strong> (zdarma, bez serveru). Po nastavení stačí kliknout na tlačítko <strong>Synchronizovat</strong>.
    </p>
    <div style="display:flex; flex-direction:column; gap:8px;">
      <label style="font-size:0.8rem; font-weight:700;">1. GitHub Token (oprávnění <code>gist</code>)</label>
      <div style="display:flex; gap:6px; align-items:center;">
        <input type="password" id="inpSyncToken" placeholder="ghp_..." style="flex:1; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:7px 10px; border-radius:8px; font-size:0.84rem;">
        <a href="https://github.com/settings/tokens/new?description=Karty%20Pro%20Sync&scopes=gist" target="_blank" rel="noopener" class="btn btn-sm">Získat token</a>
      </div>
      <label style="font-size:0.8rem; font-weight:700;">2. Gist ID (nechte prázdné pro automatické vytvoření)</label>
      <input type="text" id="inpSyncGistId" placeholder="automaticky při prvním uložení" style="background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:7px 10px; border-radius:8px; font-size:0.84rem;">
      <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:4px;">
        <button class="btn btn-sm btn-primary" id="btnSyncSaveConnect">Uložit &amp; synchronizovat</button>
        <button class="btn btn-sm" id="btnSyncCopyPair">Kopírovat odkaz pro telefon</button>
        <button class="btn btn-sm btn-danger" id="btnSyncDisconnect" style="margin-left:auto;">Odpojit</button>
      </div>
      <div id="syncStatusMsg" style="font-size:0.8rem; color:var(--text-muted); min-height:18px;"></div>
    </div>
  </div>
</div>

<div class="theme-preview-bar" id="themePreviewBar">
  <span id="themePreviewLabel" style="font-size:0.84rem; font-weight:700;">Náhled motivu</span>
  <button class="btn btn-sm" id="btnPreviewBack">Zpět do obchodu</button>
  <button class="btn btn-sm btn-primary" id="btnPreviewAction">Koupit / Použít</button>
</div>
<div class="pro-toast" id="proToast"></div>
"""

PRO_JS = r"""
// --- KARTY PRO DUOLINGO ENGINE ---
const PRO_STORAGE_KEY = "karty_pro_profile_v1";
const PRO_THEMES = [
  { id: "default", name: "Lesní houbař (výchozí)", cost: 0, cat: "Monochrom" },
  { id: "moss", name: "Hluboký mech", cost: 1500, cat: "Monochrom" },
  { id: "lichen", name: "Kůra a lišejník", cost: 1500, cat: "Monochrom" },
  { id: "amber", name: "Teplý jantar", cost: 1500, cat: "Monochrom" },
  { id: "midnight", name: "Půlnoční modř", cost: 1500, cat: "Monochrom" },
  { id: "heather", name: "Vřesoviště", cost: 1500, cat: "Monochrom" },
  { id: "mono", name: "Břidlicový monochrom", cost: 1500, cat: "Monochrom" },
  { id: "ocean", name: "Moře (vlny)", cost: 3000, cat: "Minimalistické" },
  { id: "desert", name: "Poušť (duny)", cost: 3000, cat: "Minimalistické" },
  { id: "rainforest", name: "Prales (kapradí)", cost: 3000, cat: "Minimalistické" },
  { id: "space", name: "Vesmír (hvězdy a planeta)", cost: 3000, cat: "Minimalistické" },
  { id: "lofi", name: "Lo-fi noc", cost: 3000, cat: "Minimalistické" },
  { id: "cottage", name: "Cottagecore louka", cost: 3000, cat: "Minimalistické" },
  { id: "cats", name: "Kočičky (Cat Café)", cost: 5500, cat: "Pro ilustrované" },
  { id: "mountains", name: "Horské vrcholy (Alpy)", cost: 5500, cat: "Pro ilustrované" },
  { id: "sakura", name: "Japonská Sakura", cost: 5500, cat: "Pro ilustrované" },
  { id: "lighthouse", name: "Maják u útesu", cost: 5500, cat: "Pro ilustrované" }
];

function getDefaultProProfile() {
  return {
    points: 0,
    xp: 0,
    freezes: 1,
    frozenDates: [],
    dailyGoal: 20,
    lessonLength: 0,
    lessonLengthEnabled: false,
    boostUntil: 0,
    unlockedThemes: ["default"],
    activeTheme: "default",
    powerups: { timeFreeze: 1, fiftyFifty: 1, comboShield: 0 },
    milestones: [
      { id: "m7", days: 7, title: "Týden v kuse", bonusPoints: 50, claimed: false },
      { id: "m30", days: 30, title: "Měsíc učení", bonusPoints: 150, claimed: false },
      { id: "m50", days: 50, title: "50 dní odhodlání", bonusPoints: 300, claimed: false },
      { id: "m100", days: 100, title: "Stovka mistrů", bonusPoints: 700, claimed: false }
    ],
    dailyBonusDates: []
  };
}

function loadProProfile() {
  try {
    const raw = localStorage.getItem(PRO_STORAGE_KEY);
    if (!raw) return getDefaultProProfile();
    const parsed = JSON.parse(raw);
    const def = getDefaultProProfile();
    return {
      ...def,
      ...parsed,
      frozenDates: Array.isArray(parsed.frozenDates) ? parsed.frozenDates : [],
      unlockedThemes: Array.isArray(parsed.unlockedThemes) ? parsed.unlockedThemes : ["default"],
      milestones: Array.isArray(parsed.milestones) && parsed.milestones.length > 0 ? parsed.milestones : def.milestones,
      dailyBonusDates: Array.isArray(parsed.dailyBonusDates) ? parsed.dailyBonusDates : []
    };
  } catch (e) {
    return getDefaultProProfile();
  }
}

function saveProProfile(prof) {
  localStorage.setItem(PRO_STORAGE_KEY, JSON.stringify(prof));
}

function showProToast(msg) {
  const el = document.getElementById("proToast");
  if (!el) return;
  el.innerText = msg;
  el.classList.add("show");
  clearTimeout(window._proToastTimer);
  window._proToastTimer = setTimeout(() => el.classList.remove("show"), 2600);
}

function setMascotState(mood, msg) {
  const svg = document.getElementById("proMascotSvg");
  const mouth = document.getElementById("proMascotMouth");
  const msgEl = document.getElementById("proMascotMsg");
  if (msgEl && msg) msgEl.innerText = msg;
  if (mouth) {
    if (mood === "happy") mouth.setAttribute("d", "M26 47Q32 53 38 47");
    else if (mood === "encourage") mouth.setAttribute("d", "M28 50Q32 47 36 50");
    else mouth.setAttribute("d", "M28 48Q32 51 36 48");
  }
  if (svg && mood === "happy") {
    svg.classList.remove("bounce");
    void svg.offsetWidth;
    svg.classList.add("bounce");
  }
}

function applyProTheme(themeId) {
  document.body.classList.remove("theme-moss", "theme-midnight", "theme-amber", "theme-heather", "theme-lichen", "theme-mono", "theme-ocean", "theme-desert", "theme-rainforest", "theme-space", "theme-lofi", "theme-cottage", "theme-cats", "theme-mountains", "theme-sakura", "theme-lighthouse");
  if (themeId && themeId !== "default") document.body.classList.add("theme-" + themeId);
}

function addDaysToDateStr(dateStr, deltaDays) {
  const [y, m, d] = dateStr.split("-").map(Number);
  return getLocalDateString(new Date(y, m - 1, d + deltaDays));
}

function levenshteinDist(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1]
        : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

async function computeProStreakAndFreeze() {
  const prof = loadProProfile();
  const reviews = await dbGetAllReviews();
  const todayStr = getLocalDateString();
  const graduatedByDate = new Map();
  reviews.forEach(r => {
    if (r && r.dateStr && (r.interval || 0) >= 1) {
      graduatedByDate.set(r.dateStr, (graduatedByDate.get(r.dateStr) || 0) + 1);
    }
  });
  const activeSet = new Set(graduatedByDate.keys());
  const frozenSet = new Set(prof.frozenDates);

  const allKnown = Array.from(new Set([...activeSet, ...frozenSet])).sort();
  if (allKnown.length > 0 && prof.freezes > 0) {
    const yesterdayStr = addDaysToDateStr(todayStr, -1);
    let cursor = addDaysToDateStr(allKnown[allKnown.length - 1], 1);
    let safety = 0;
    while (cursor <= yesterdayStr && prof.freezes > 0 && safety < 30) {
      if (!activeSet.has(cursor) && !frozenSet.has(cursor)) {
        prof.freezes--;
        frozenSet.add(cursor);
        prof.frozenDates.push(cursor);
        showProToast(`Streak Freeze ochránil den ${cursor}`);
      }
      cursor = addDaysToDateStr(cursor, 1);
      safety++;
    }
    saveProProfile(prof);
  }

  let streak = 0;
  let checkStr = todayStr;
  if (!activeSet.has(checkStr) && !frozenSet.has(checkStr)) checkStr = addDaysToDateStr(todayStr, -1);
  let guard = 0;
  while ((activeSet.has(checkStr) || frozenSet.has(checkStr)) && guard < 3650) {
    streak++;
    checkStr = addDaysToDateStr(checkStr, -1);
    guard++;
  }

  let msAwarded = false;
  for (const ms of prof.milestones) {
    if (!ms.claimed && streak >= ms.days) {
      ms.claimed = true;
      prof.points += (ms.bonusPoints || 0);
      prof.xp = (prof.xp || 0) + (ms.bonusPoints || 0);
      msAwarded = true;
      launchConfetti();
      playProTone("level");
      showProToast(`Milník ${ms.days} dní splněn: ${ms.title} (+${ms.bonusPoints || 0} b.)`);
    }
  }
  if (msAwarded) saveProProfile(prof);
  const todayCount = graduatedByDate.get(todayStr) || 0;
  return { prof, streak, todayCount, frozenSet, activeSet };
}

function getLevelInfo(xpVal) {
  const xp = Math.max(0, xpVal || 0);
  const level = Math.floor(Math.sqrt(xp / 45)) + 1;
  const curLvXp = Math.pow(level - 1, 2) * 45;
  const nextLvXp = Math.pow(level, 2) * 45;
  const ranks = ["Začátečník", "Stopař", "Sběratel", "Průzkumník", "Znalec", "Mistr", "Velmistr", "Legenda"];
  const rank = ranks[Math.min(ranks.length - 1, Math.floor((level - 1) / 2))];
  const pct = Math.min(100, Math.round(((xp - curLvXp) / Math.max(1, nextLvXp - curLvXp)) * 100));
  return { level, rank, xpInLv: xp - curLvXp, lvSpan: nextLvXp - curLvXp, pct };
}

function launchConfetti() {
  const colors = ["#6ea065", "#d49b5a", "#6da3e8", "#eae4d7", "#a67db8"];
  for (let i = 0; i < 36; i++) {
    const p = document.createElement("div");
    p.className = "pro-confetti-piece";
    p.style.left = Math.random() * 100 + "vw";
    p.style.background = colors[i % colors.length];
    p.style.animationDelay = (Math.random() * 0.35) + "s";
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 2000);
  }
}

function playProTone(kind) {
  const prof = loadProProfile();
  if (prof.soundEnabled === false) return;
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    if (!window._proAudioCtx) window._proAudioCtx = new AudioCtx();
    const ctx = window._proAudioCtx;
    const now = ctx.currentTime;
    const playNote = (freq, startOffset, dur) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, now + startOffset);
      gain.gain.setValueAtTime(0.08, now + startOffset);
      gain.gain.exponentialRampToValueAtTime(0.001, now + startOffset + dur);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now + startOffset);
      osc.stop(now + startOffset + dur);
    };
    if (kind === "good") { playNote(523.25, 0, 0.11); playNote(659.25, 0.08, 0.16); }
    else if (kind === "level") { playNote(523.25, 0, 0.12); playNote(659.25, 0.09, 0.12); playNote(783.99, 0.18, 0.14); playNote(1046.5, 0.28, 0.28); }
    else if (kind === "again") { playNote(310, 0, 0.14); }
  } catch (e) {}
}

let sessionCombo = 0;
let _lessonStartMs = Date.now();
let _lessonStats = { reviewed: 0, mistakes: 0, xp: 0 };

function _hashDateSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

function getDailyQuestsState(prof, todayCount) {
  const todayStr = getLocalDateString();
  if (!prof.dailyQuests || prof.dailyQuests.date !== todayStr) {
    prof.dailyQuests = {
      date: todayStr, maxCombo: 0, cleanCount: 0, easyCount: 0, goodCount: 0, hardCount: 0, typeCount: 0, xpToday: 0, minigameCount: 0,
      readyIds: [], claimedIds: []
    };
    saveProProfile(prof);
  }
  const dq = prof.dailyQuests;
  dq.readyIds = dq.readyIds || [];
  dq.claimedIds = dq.claimedIds || [];
  const allDefs = [
    { id: "q_grad10", title: "Dokonči 10 karet (min. 1 den)", cur: todayCount, target: 10, reward: 30 },
    { id: "q_grad25", title: "Dokonči 25 karet (min. 1 den)", cur: todayCount, target: 25, reward: 60 },
    { id: "q_grad40", title: "Dokonči 40 karet (min. 1 den)", cur: todayCount, target: 40, reward: 90 },
    { id: "q_grad60", title: "Dokonči 60 karet (min. 1 den)", cur: todayCount, target: 60, reward: 130 },
    { id: "q_combo4", title: "Dosáhni Combo 4x", cur: dq.maxCombo || 0, target: 4, reward: 30 },
    { id: "q_combo8", title: "Dosáhni Combo 8x", cur: dq.maxCombo || 0, target: 8, reward: 55 },
    { id: "q_combo12", title: "Dosáhni Combo 12x", cur: dq.maxCombo || 0, target: 12, reward: 80 },
    { id: "q_combo15", title: "Dosáhni Combo 15x", cur: dq.maxCombo || 0, target: 15, reward: 100 },
    { id: "q_clean10", title: "10 karet bez tlačítka Znovu", cur: dq.cleanCount || 0, target: 10, reward: 45 },
    { id: "q_clean20", title: "20 karet bez tlačítka Znovu", cur: dq.cleanCount || 0, target: 20, reward: 75 },
    { id: "q_clean30", title: "30 karet bez tlačítka Znovu", cur: dq.cleanCount || 0, target: 30, reward: 110 },
    { id: "q_easy5", title: "Ohodnoť 5 karet jako Snadné", cur: dq.easyCount || 0, target: 5, reward: 35 },
    { id: "q_easy10", title: "Ohodnoť 10 karet jako Snadné", cur: dq.easyCount || 0, target: 10, reward: 65 },
    { id: "q_good12", title: "Ohodnoť 12 karet jako Dobré", cur: dq.goodCount || 0, target: 12, reward: 40 },
    { id: "q_hard4", title: "Ohodnoť 4 karty jako Těžké", cur: dq.hardCount || 0, target: 4, reward: 35 },
    { id: "q_type5", title: "5 karet ve vepisovacím režimu", cur: dq.typeCount || 0, target: 5, reward: 45 },
    { id: "q_type10", title: "10 karet ve vepisovacím režimu", cur: dq.typeCount || 0, target: 10, reward: 65 },
    { id: "q_xp120", title: "Nasbírej dnes 120 XP", cur: dq.xpToday || 0, target: 120, reward: 50 },
    { id: "q_xp250", title: "Nasbírej dnes 250 XP", cur: dq.xpToday || 0, target: 250, reward: 85 },
    { id: "q_xp400", title: "Nasbírej dnes 400 XP", cur: dq.xpToday || 0, target: 400, reward: 120 },
    { id: "q_mini1", title: "Dokonči 1 minihru", cur: dq.minigameCount || 0, target: 1, reward: 70 }
  ];
  let seed = _hashDateSeed(todayStr);
  const pool = [...allDefs];
  for (let i = pool.length - 1; i > 0; i--) {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    const j = seed % (i + 1);
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return { dq, defs: pool.slice(0, 3) };
}

function renderDailyQuests(prof, todayCount) {
  const strip = document.getElementById("proQuestsStrip");
  if (!strip) return;
  const { dq, defs } = getDailyQuestsState(prof, todayCount);
  strip.innerHTML = "";
  defs.forEach(q => {
    const claimed = dq.claimedIds.includes(q.id);
    const ready = !claimed && (dq.readyIds.includes(q.id) || q.cur >= q.target);
    const pct = Math.min(100, Math.round((q.cur / q.target) * 100));
    const card = document.createElement("div");
    card.className = `pro-quest-card ${claimed ? "done" : (ready ? "ready" : "")}`;
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; gap:6px; font-weight:700;">
        <span>${q.title}</span>
        <span style="color:var(--accent);">${claimed ? "Otevřeno" : (ready ? "Truhla!" : `+${q.reward} b.`)}</span>
      </div>
      ${ready
        ? `<button class="btn btn-sm btn-primary btn-open-chest" style="padding:4px 8px; font-size:0.75rem;">Otevřít truhlu s pokladem</button>`
        : `<div class="pro-bar-track" style="height:5px;"><div class="pro-bar-fill pro-bar-goal" style="width:${pct}%;"></div></div>`}
    `;
    const chestBtn = card.querySelector(".btn-open-chest");
    if (chestBtn) {
      chestBtn.onclick = async () => {
        const p = loadProProfile();
        const st = getDailyQuestsState(p, todayCount);
        if (st.dq.claimedIds.includes(q.id)) return;
        st.dq.claimedIds.push(q.id);
        const bonus = q.reward + Math.floor(Math.random() * 25);
        p.points += bonus;
        p.xp = (p.xp || 0) + bonus;
        let extraMsg = `+${bonus} b.`;
        if (Math.random() < 0.2 && p.freezes < 3) { p.freezes++; extraMsg += " a 1x Streak Freeze!"; }
        saveProProfile(p);
        launchConfetti();
        playProTone("level");
        showProToast(`Truhla otevřena: ${extraMsg}`);
        await updateProHud();
      };
    }
    strip.appendChild(card);
  });
}

async function updateProHud() {
  const { prof, streak, todayCount, activeSet, frozenSet } = await computeProStreakAndFreeze();
  applyProTheme(prof.activeTheme);
  const lv = getLevelInfo(prof.xp ?? prof.points);
  const elLevel = document.getElementById("proLevelPill");
  const elStreak = document.getElementById("proStreakPill");
  const elPoints = document.getElementById("proPointsPill");
  const elBoost = document.getElementById("proBoostPill");
  const elSound = document.getElementById("btnProSound");
  if (elLevel) elLevel.innerText = `Lv. ${lv.level}`;
  if (elStreak) elStreak.innerText = `Série: ${streak} d`;
  if (elPoints) elPoints.innerText = `${prof.points} b.`;
  if (elBoost) elBoost.style.display = (prof.boostUntil > Date.now()) ? "inline-flex" : "none";
  if (elSound) elSound.innerText = prof.soundEnabled === false ? "Zvuk: Vyp" : "Zvuk: Zap";

  const elRank = document.getElementById("proDashRank");
  const elXpTxt = document.getElementById("proDashXpText");
  const elXpBar = document.getElementById("proDashXpBar");
  const elGoalTxt = document.getElementById("proDashGoalText");
  const elGoalBar = document.getElementById("proDashGoalBar");
  if (elRank) elRank.innerText = `Úroveň ${lv.level} – ${lv.rank}`;
  if (elXpTxt) elXpTxt.innerText = `${lv.xpInLv} / ${lv.lvSpan} XP`;
  if (elXpBar) elXpBar.style.width = `${lv.pct}%`;
  const goalPct = Math.min(100, Math.round((todayCount / Math.max(1, prof.dailyGoal || 20)) * 100));
  if (elGoalTxt) elGoalTxt.innerText = todayCount >= prof.dailyGoal ? `Splněno (${todayCount}/${prof.dailyGoal})` : `${todayCount} / ${prof.dailyGoal}`;
  if (elGoalBar) elGoalBar.style.width = `${goalPct}%`;
  renderDailyQuests(prof, todayCount);
  renderMobileWeekStrip(activeSet, frozenSet);
}

function renderMobileWeekStrip(activeSet, frozenSet) {
  const hm = document.getElementById("heatmapContainer");
  if (!hm) return;
  let strip = document.getElementById("proWeekStrip");
  if (!strip) {
    strip = document.createElement("div");
    strip.id = "proWeekStrip";
    strip.className = "pro-week-strip";
    hm.classList.add("mobile-collapsed");
    hm.insertBefore(strip, hm.firstChild);
  }
  const dayNames = ["Ne", "Po", "Út", "St", "Čt", "Pá", "So"];
  const todayStr = getLocalDateString();
  let dotsHtml = "";
  for (let i = 6; i >= 0; i--) {
    const dStr = addDaysToDateStr(todayStr, -i);
    const dt = new Date(dStr + "T12:00:00");
    const lbl = dayNames[dt.getDay()];
    const cls = activeSet.has(dStr) ? "active" : (frozenSet.has(dStr) ? "frozen" : "");
    dotsHtml += `<span class="pro-week-dot ${cls}" title="${dStr}">${lbl}</span>`;
  }
  const isCollapsed = hm.classList.contains("mobile-collapsed");
  strip.innerHTML = `
    <div class="pro-week-days">${dotsHtml}</div>
    <button class="btn btn-sm" id="btnToggleFullHeatmap" style="padding:3px 8px; font-size:0.74rem;">${isCollapsed ? "Celý rok" : "Skrýt rok"}</button>
  `;
  strip.querySelector("#btnToggleFullHeatmap").onclick = () => {
    hm.classList.toggle("mobile-collapsed");
    renderMobileWeekStrip(activeSet, frozenSet);
  };
}

// Wrap startStudy for Lesson slicing (10-15 cards) and Lesson stats
const _origStartStudyPro = startStudy;
startStudy = async function(deckId, quickMode = false, subdeckFilter = null, keepExtra = false, sliceRange = null) {
  const prof = loadProProfile();
  _lessonStartMs = Date.now();
  _lessonStats = { reviewed: 0, mistakes: 0, xp: 0 };
  await _origStartStudyPro(deckId, quickMode, subdeckFilter, keepExtra);
  if (sliceRange && Array.isArray(sliceRange)) {
    const [sStart, sEnd] = sliceRange;
    const sliced = currentDeck.cards.slice(sStart, sEnd);
    if (sliced.length > 0) {
      studyQueue = sliced;
      currentIndex = 0;
      loadCard(0);
    }
  } else if (!quickMode && prof.lessonLengthEnabled && prof.lessonLength > 0 && studyQueue.length > prof.lessonLength) {
    studyQueue = studyQueue.slice(0, prof.lessonLength);
    sessionStats.newCount = studyQueue.filter(c => !getCardSrsObj(c).due || getCardSrsObj(c).due === 0).length;
    sessionStats.dueCount = studyQueue.length - sessionStats.newCount;
    loadCard(0);
  }
};

// Wrap rateCard for >=1 day scoring, Quests, Mascot, and Repair Round
const _origRateCardPro = rateCard;
rateCard = async function(ratingKey) {
  const intervals = calcNextIntervals(currentCard);
  const chosen = intervals[ratingKey];
  const isGraduatedForDay = chosen && chosen.ms >= 86400000;

  await _origRateCardPro(ratingKey);
  _lessonStats.reviewed++;

  const prof = loadProProfile();
  const prevLv = getLevelInfo(prof.xp ?? prof.points).level;
  const isBoost = prof.boostUntil > Date.now();
  const todayStr = getLocalDateString();
  if (!prof.dailyQuests || prof.dailyQuests.date !== todayStr) {
    prof.dailyQuests = { date: todayStr, maxCombo: 0, cleanCount: 0, easyCount: 0, goodCount: 0, hardCount: 0, typeCount: 0, xpToday: 0, readyIds: [], claimedIds: [] };
  }

  if (ratingKey === "again") {
    if (prof.powerups && prof.powerups.comboShield > 0 && sessionCombo > 0) {
      prof.powerups.comboShield--;
      showProToast("Štít Comba zachránil vaši sérii!");
    } else {
      sessionCombo = 0;
      const comboEl = document.getElementById("proComboBadge");
      if (comboEl) { comboEl.style.display = "none"; comboEl.classList.remove("hot"); }
      showProToast("Karta se vrátí v opravném kole.");
    }
    _lessonStats.mistakes++;
    prof.dailyQuests.cleanCount = 0;
    playProTone("again");
    setMascotState("encourage", "Nevadí, opravíme na konci lekce!");
    saveProProfile(prof);
    await updateProHud();
    return;
  }

  if (ratingKey === "good" || ratingKey === "easy") {
    sessionCombo++;
    prof.dailyQuests.maxCombo = Math.max(prof.dailyQuests.maxCombo || 0, sessionCombo);
    setMascotState("happy", sessionCombo >= 4 ? `Skvělá série ${sessionCombo}x!` : "Výborně!");
    if (sessionCombo === 8 || sessionCombo === 12) {
      const luckPts = 50 + Math.floor(Math.random() * 101);
      prof.points += luckPts;
      prof.xp = (prof.xp || 0) + luckPts;
      launchConfetti();
      playProTone("level");
      showProToast(`Kartičkové štěstí (${sessionCombo}x Combo): +${luckPts} b.!`);
    }
  } else {
    setMascotState("neutral", "Dobrá práce, pokračuj!");
  }
  if (ratingKey === "easy") prof.dailyQuests.easyCount = (prof.dailyQuests.easyCount || 0) + 1;
  if (ratingKey === "good") prof.dailyQuests.goodCount = (prof.dailyQuests.goodCount || 0) + 1;
  if (ratingKey === "hard") prof.dailyQuests.hardCount = (prof.dailyQuests.hardCount || 0) + 1;
  if (typeof cardStudyMode !== "undefined" && cardStudyMode === "type") {
    prof.dailyQuests.typeCount = (prof.dailyQuests.typeCount || 0) + 1;
  }
  prof.dailyQuests.cleanCount = (prof.dailyQuests.cleanCount || 0) + 1;

  const comboEl = document.getElementById("proComboBadge");
  if (comboEl) {
    if (sessionCombo >= 3) {
      comboEl.style.display = "inline-flex";
      comboEl.innerText = `Combo ${sessionCombo}x`;
      comboEl.classList.toggle("hot", sessionCombo >= 4);
    } else {
      comboEl.style.display = "none";
      comboEl.classList.remove("hot");
    }
  }

  if (!isGraduatedForDay) {
    playProTone("good");
    saveProProfile(prof);
    showProToast("Krok učení (body až po odložení o 1+ den)");
    await updateProHud();
    return;
  }

  playProTone("good");
  const comboBonus = (sessionCombo > 0 && sessionCombo % 5 === 0) ? 5 : 0;
  const basePts = (ratingKey === "good" || ratingKey === "easy") ? 10 : 6;
  const gained = (basePts + comboBonus) * (isBoost ? 2 : 1);
  prof.points += gained;
  prof.xp = (prof.xp ?? prof.points) + gained;
  prof.dailyQuests.xpToday = (prof.dailyQuests.xpToday || 0) + gained;
  _lessonStats.xp += gained;

  const reviews = await dbGetAllReviews();
  const todayCount = reviews.filter(r => r && r.dateStr === todayStr && (r.interval || 0) >= 1).length;
  const { dq, defs } = getDailyQuestsState(prof, todayCount);
  let unlockedChest = false;
  defs.forEach(q => {
    if (!dq.claimedIds.includes(q.id) && !dq.readyIds.includes(q.id) && q.cur >= q.target) {
      dq.readyIds.push(q.id);
      unlockedChest = true;
    }
  });

  const newLv = getLevelInfo(prof.xp).level;
  if (todayCount >= prof.dailyGoal && !prof.dailyBonusDates.includes(todayStr)) {
    prof.dailyBonusDates.push(todayStr);
    prof.points += 30;
    prof.xp += 30;
    launchConfetti();
    playProTone("level");
    showProToast(`Denní cíl splněn! +${gained + 30} b.`);
  } else if (unlockedChest) {
    launchConfetti();
    playProTone("level");
    showProToast("Denní výzva splněna! Čeká na vás truhla s pokladem.");
  } else if (newLv > prevLv) {
    launchConfetti();
    playProTone("level");
    showProToast(`Nová úroveň ${newLv}! (+${gained} b.)`);
  } else {
    showProToast(`+${gained} b.${isBoost ? " (2x)" : ""}`);
  }
  saveProProfile(prof);
  await updateProHud();
};

// Wrap showFinishedView for Lesson Summary
const _origShowFinishedPro = showFinishedView;
showFinishedView = function() {
  _origShowFinishedPro();
  const msgEl = document.getElementById("finishedMsg");
  if (msgEl) {
    const secs = Math.max(1, Math.round((Date.now() - _lessonStartMs) / 1000));
    const acc = _lessonStats.reviewed > 0 ? Math.max(0, Math.round(((_lessonStats.reviewed - _lessonStats.mistakes) / _lessonStats.reviewed) * 100)) : 100;
    msgEl.innerText = `Lekce dokončena! Získáno ${_lessonStats.xp} XP · Přesnost ${acc}% · Čas ${secs} s.`;
  }
  launchConfetti();
  playProTone("level");
};

// Wrap renderHeatmap
const _origRenderHeatmapPro = renderHeatmap;
renderHeatmap = async function() {
  await _origRenderHeatmapPro();
  const { streak, frozenSet } = await computeProStreakAndFreeze();
  document.querySelectorAll(".hm-cell[data-date]").forEach(cell => {
    const d = cell.getAttribute("data-date");
    if (d && frozenSet.has(d) && !cell.classList.contains("l1") && !cell.classList.contains("l2") && !cell.classList.contains("l3") && !cell.classList.contains("l4")) {
      cell.classList.add("frozen");
    }
  });
  const streakEl = document.getElementById("hmCurrentStreak");
  if (streakEl) {
    streakEl.innerText = `${streak} dní`;
    if (streak > 0) streakEl.classList.remove("zero");
  }
  await updateProHud();
};

// Matching Pairs Mini-Game
let _matchDeck = null;
function openMatchingGame(deck) {
  _matchDeck = deck || currentDeck;
  if (!_matchDeck || !_matchDeck.cards || _matchDeck.cards.length < 4) {
    alert("Pro párování potřebujete alespoň 4 karty v balíčku.");
    return;
  }
  renderMatchRound();
  document.getElementById("matchModal").classList.add("active");
}
function renderMatchRound() {
  const leftCol = document.getElementById("matchLeftCol");
  const rightCol = document.getElementById("matchRightCol");
  const statusEl = document.getElementById("matchStatusText");
  leftCol.innerHTML = "";
  rightCol.innerHTML = "";
  const sample = [..._matchDeck.cards].sort(() => Math.random() - 0.5).slice(0, 4);
  const rightItems = [...sample].sort(() => Math.random() - 0.5);
  let selLeft = null;
  let matchedCount = 0;

  sample.forEach(c => {
    const btn = document.createElement("button");
    btn.className = "match-btn";
    btn.innerText = getGamePairForCard(c).prompt;
    btn.onclick = () => {
      leftCol.querySelectorAll(".match-btn").forEach(b => b.classList.remove("selected"));
      btn.classList.add("selected");
      selLeft = { id: c.id, el: btn };
    };
    leftCol.appendChild(btn);
  });

  rightItems.forEach(c => {
    const btn = document.createElement("button");
    btn.className = "match-btn";
    btn.innerText = getGamePairForCard(c).answer;
    btn.onclick = async () => {
      if (!selLeft) return;
      if (selLeft.id === c.id) {
        selLeft.el.classList.remove("selected");
        selLeft.el.classList.add("matched");
        btn.classList.add("matched");
        selLeft = null;
        matchedCount++;
        playProTone("good");
        if (matchedCount === sample.length) {
          const p = loadProProfile();
          p.points += 25;
          p.xp = (p.xp || 0) + 25;
          saveProProfile(p);
          launchConfetti();
          playProTone("level");
          statusEl.innerText = "Vše spárováno! +25 bodů.";
          await updateProHud();
        }
      } else {
        btn.classList.add("err");
        playProTone("again");
        setTimeout(() => btn.classList.remove("err"), 400);
      }
    };
    rightCol.appendChild(btn);
  });
  statusEl.innerText = "Spojte pojmy vlevo se správnými odpověďmi vpravo.";
}
document.getElementById("matchModalClose").onclick = () => document.getElementById("matchModal").classList.remove("active");
document.getElementById("btnMatchNextRound").onclick = renderMatchRound;

// Skill Path Modal
function openSkillPath(deck) {
  document.getElementById("skillPathTitle").innerText = `Cesta lekcí: ${deck.name}`;
  const listEl = document.getElementById("skillPathList");
  listEl.innerHTML = "";
  const chunkSize = 15;
  const totalChunks = Math.max(1, Math.ceil(deck.cards.length / chunkSize));
  for (let i = 0; i < totalChunks; i++) {
    const start = i * chunkSize;
    const end = Math.min(deck.cards.length, start + chunkSize);
    const slice = deck.cards.slice(start, end);
    const doneInSlice = slice.filter(c => (c.interval || 0) >= 1).length;
    const isCompleted = doneInSlice === slice.length && slice.length > 0;
    const node = document.createElement("div");
    node.className = `skill-node ${isCompleted ? "completed" : ""}`;
    node.innerHTML = `
      <div>
        <div style="font-weight:700; font-size:0.9rem;">Lekce ${i + 1}</div>
        <div style="font-size:0.75rem; color:var(--text-muted);">Karty ${start + 1}–${end} (${doneInSlice}/${slice.length} splněno)</div>
      </div>
      <span style="font-weight:700; color:var(--accent);">${isCompleted ? "Hotovo" : "Start"}</span>
    `;
    node.onclick = () => {
      document.getElementById("skillPathModal").classList.remove("active");
      startStudy(deck.id, false, null, false, [start, end]);
    };
    listEl.appendChild(node);
  }
  document.getElementById("skillPathModal").classList.add("active");
}
document.getElementById("skillPathClose").onclick = () => document.getElementById("skillPathModal").classList.remove("active");

// In-App Card Editor
function openCardEditor() {
  if (!currentCard || !currentDeck) return;
  document.getElementById("edCardTitle").value = currentCard.title || "";
  document.getElementById("edCardFront").value = currentCard.front || "";
  document.getElementById("edCardBack").value = currentCard.back || "";
  document.getElementById("cardEditorModal").classList.add("active");
}
document.getElementById("cardEditorClose").onclick = () => document.getElementById("cardEditorModal").classList.remove("active");
document.getElementById("btnSaveCardEdit").onclick = async () => {
  if (!currentCard || !currentDeck) return;
  currentCard.title = document.getElementById("edCardTitle").value.trim() || currentCard.title;
  currentCard.front = document.getElementById("edCardFront").value;
  currentCard.back = document.getElementById("edCardBack").value;
  const orig = currentDeck.cards.find(c => c.id === currentCard.id);
  if (orig) {
    orig.title = currentCard.title;
    orig.front = currentCard.front;
    orig.back = currentCard.back;
  }
  await dbSaveDeck(currentDeck);
  document.getElementById("cardEditorModal").classList.remove("active");
  loadCard(currentIndex);
  showProToast("Karta uložena!");
};

// Quick Card Creator / Text Import (otázka ; odpověď)
document.getElementById("btnProNewCard").onclick = async () => {
  const decks = await dbGetAllDecks();
  const sel = document.getElementById("selQuickDeckTarget");
  sel.innerHTML = `<option value="__new__">+ Vytvořit nový balíček</option>`;
  decks.forEach(d => {
    sel.innerHTML += `<option value="${d.id}">${escapeHtml(d.name)} (${d.cards.length})</option>`;
  });
  document.getElementById("inpQuickNewDeckName").style.display = "block";
  document.getElementById("quickImportModal").classList.add("active");
};
document.getElementById("selQuickDeckTarget").onchange = (e) => {
  document.getElementById("inpQuickNewDeckName").style.display = e.target.value === "__new__" ? "block" : "none";
};
document.getElementById("quickImportClose").onclick = () => document.getElementById("quickImportModal").classList.remove("active");
document.getElementById("btnRunQuickImport").onclick = async () => {
  const targetVal = document.getElementById("selQuickDeckTarget").value;
  const rawLines = document.getElementById("txtQuickImportLines").value.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
  if (rawLines.length === 0) { alert("Zadejte alespoň jeden řádek."); return; }
  const newCards = rawLines.map((line, idx) => {
    const parts = line.split(";");
    const q = (parts[0] || "").trim();
    const a = (parts.slice(1).join(";") || q).trim();
    return {
      id: "q_" + Date.now() + "_" + idx,
      title: q.replace(/\{\{c\d+::([^:}]+).*?\}\}/gi, "$1"),
      front: q,
      back: a,
      answer: a,
      interval: 0, reps: 0, ease: 2.5, due: 0, state: 0
    };
  });
  let deck = null;
  if (targetVal === "__new__") {
    const dName = document.getElementById("inpQuickNewDeckName").value.trim() || "Můj jazykový balíček";
    deck = { id: "deck_" + Date.now(), name: dName, createdAt: Date.now(), cards: newCards, settings: { newCardsPerDay: 20 }, history: [] };
  } else {
    deck = await dbGetDeck(targetVal);
    if (deck) deck.cards.push(...newCards);
  }
  if (deck) {
    await dbSaveDeck(deck);
    document.getElementById("txtQuickImportLines").value = "";
    document.getElementById("quickImportModal").classList.remove("active");
    await loadDeckList();
    showProToast(`Přidáno ${newCards.length} kartiček!`);
  }
};

// Touch swipe rating disabled to prevent accidental card rating while scrolling on mobile.

// Shop & Sound Modal Listeners
async function renderShopModal() {
  const { prof, streak } = await computeProStreakAndFreeze();
  document.getElementById("shopBalanceVal").innerText = `${prof.points} b.`;
  document.getElementById("selProDailyGoal").value = String(prof.dailyGoal || 20);
  document.getElementById("selProLessonLen").value = String(prof.lessonLengthEnabled ? (prof.lessonLength ?? 0) : 0);

  const themesBox = document.getElementById("shopThemesList");
  themesBox.innerHTML = "";
  let lastCat = "";
  PRO_THEMES.forEach(th => {
    if (th.cat && th.cat !== lastCat) {
      lastCat = th.cat;
      const catHdr = document.createElement("div");
      catHdr.style.cssText = "font-size:0.78rem; font-weight:700; color:var(--accent); margin-top:6px; text-transform:uppercase;";
      catHdr.innerText = lastCat;
      themesBox.appendChild(catHdr);
    }
    const unlocked = prof.unlockedThemes.includes(th.id);
    const isActive = prof.activeTheme === th.id;
    const row = document.createElement("div");
    row.className = "shop-item";
    row.innerHTML = `
      <div class="shop-item-info">
        <div class="shop-item-title">${th.name}</div>
        <div class="shop-item-desc">${unlocked ? (isActive ? "Aktivní motiv" : "Odemčeno") : `Cena: ${th.cost} bodů`}</div>
      </div>
      <div style="display:flex; gap:6px; align-items:center;">
        ${!isActive ? `<button class="btn btn-sm btn-preview-theme">Náhled</button>` : ""}
        <button class="btn btn-sm ${isActive ? "" : "btn-primary"} btn-buy-theme">${isActive ? "Aktivní" : (unlocked ? "Použít" : `${th.cost} b.`)}</button>
      </div>
    `;
    const prevBtn = row.querySelector(".btn-preview-theme");
    if (prevBtn) prevBtn.onclick = () => {
      document.getElementById("shopModal").classList.remove("active");
      showView("decks");
      applyProTheme(th.id);
      const bar = document.getElementById("themePreviewBar");
      const lbl = document.getElementById("themePreviewLabel");
      const actBtn = document.getElementById("btnPreviewAction");
      if (lbl) lbl.innerText = `Náhled: ${th.name}`;
      if (actBtn) {
        actBtn.innerText = unlocked ? "Použít motiv" : `${th.cost} b.`;
        actBtn.onclick = async () => {
          const p = loadProProfile();
          if (p.unlockedThemes.includes(th.id)) p.activeTheme = th.id;
          else {
            if (p.points < th.cost) { alert("Nemáte dostatek bodů."); return; }
            p.points -= th.cost; p.unlockedThemes.push(th.id); p.activeTheme = th.id;
          }
          saveProProfile(p);
          bar.classList.remove("active");
          applyProTheme(p.activeTheme);
          await updateProHud();
          showProToast(`Motiv aktivován: ${th.name}`);
        };
      }
      if (bar) bar.classList.add("active");
    };
    row.querySelector(".btn-buy-theme").onclick = async () => {
      const p = loadProProfile();
      if (p.unlockedThemes.includes(th.id)) p.activeTheme = th.id;
      else {
        if (p.points < th.cost) { alert("Nemáte dostatek bodů."); return; }
        p.points -= th.cost; p.unlockedThemes.push(th.id); p.activeTheme = th.id;
      }
      saveProProfile(p); applyProTheme(p.activeTheme); await updateProHud(); await renderShopModal();
    };
    themesBox.appendChild(row);
  });

  const msBox = document.getElementById("shopMilestonesList");
  msBox.innerHTML = "";
  prof.milestones.sort((a, b) => a.days - b.days).forEach(ms => {
    const row = document.createElement("div");
    row.className = `milestone-row ${ms.claimed ? "claimed" : ""}`;
    row.innerHTML = `
      <div><strong>${ms.days} dní</strong> – ${escapeHtml(ms.title)} <span style="color:var(--accent); font-weight:700;">(+${ms.bonusPoints || 0} b.)</span>
      ${ms.claimed ? '<span>[Splněno]</span>' : `<span style="color:var(--text-muted);">(${Math.min(streak, ms.days)}/${ms.days})</span>`}</div>
      <button class="btn btn-sm btn-danger" style="padding:2px 8px;">Smazat</button>
    `;
    row.querySelector("button").onclick = async () => {
      const p = loadProProfile(); p.milestones = p.milestones.filter(x => x.id !== ms.id); saveProProfile(p); await renderShopModal();
    };
    msBox.appendChild(row);
  });
}

document.getElementById("btnPreviewBack").onclick = async () => {
  document.getElementById("themePreviewBar").classList.remove("active");
  applyProTheme(loadProProfile().activeTheme);
  await renderShopModal();
  document.getElementById("shopModal").classList.add("active");
};
const _btnProSoundEl = document.getElementById("btnProSound");
if (_btnProSoundEl) {
  _btnProSoundEl.onclick = async () => {
    const p = loadProProfile(); p.soundEnabled = (p.soundEnabled === false); saveProProfile(p);
    if (p.soundEnabled) playProTone("good"); await updateProHud();
  };
}
document.getElementById("btnOpenShop").onclick = async () => { await renderShopModal(); document.getElementById("shopModal").classList.add("active"); };
document.getElementById("shopModalClose").onclick = () => { applyProTheme(loadProProfile().activeTheme); document.getElementById("shopModal").classList.remove("active"); };
document.getElementById("shopModal").addEventListener("click", (e) => {
  if (e.target.id === "shopModal") { applyProTheme(loadProProfile().activeTheme); document.getElementById("shopModal").classList.remove("active"); }
});
document.getElementById("selProDailyGoal").onchange = async (e) => { const p = loadProProfile(); p.dailyGoal = parseInt(e.target.value, 10) || 20; saveProProfile(p); await updateProHud(); };
document.getElementById("selProLessonLen").onchange = async (e) => { const p = loadProProfile(); const v = parseInt(e.target.value, 10) || 0; p.lessonLength = v; p.lessonLengthEnabled = v > 0; saveProProfile(p); };
document.getElementById("btnBuyFreeze").onclick = async () => {
  const p = loadProProfile(); if (p.freezes >= 3) { alert("Máte již plnou zásobu (3/3)."); return; }
  if (p.points < 1200) { alert("Potřebujete alespoň 1200 bodů."); return; }
  p.points -= 1200; p.freezes++; saveProProfile(p); showProToast("Zakoupen Streak Freeze!"); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyBoost").onclick = async () => {
  const p = loadProProfile(); if (p.points < 1000) { alert("Potřebujete alespoň 1000 bodů."); return; }
  p.points -= 1000; p.boostUntil = Date.now() + 15 * 60 * 1000; saveProProfile(p); showProToast("Aktivován 2x Body Boost na 15 min!"); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyRepair").onclick = async () => {
  const p = loadProProfile();
  const reviews = await dbGetAllReviews();
  const activeDates = new Set(reviews.filter(r => r && r.dateStr && (r.interval || 0) >= 1).map(r => r.dateStr));
  const todayStr = getLocalDateString();
  let targetDay = null;
  for (let d = 1; d <= 3; d++) {
    const c = addDaysToDateStr(todayStr, -d);
    if (!activeDates.has(c) && !p.frozenDates.includes(c)) { targetDay = c; break; }
  }
  if (!targetDay) { alert("Za poslední 3 dny nemáte žádný nechráněný vynechaný den."); return; }
  if (p.points < 2000) { alert("Potřebujete alespoň 2000 bodů."); return; }
  p.points -= 2000; p.frozenDates.push(targetDay); saveProProfile(p); showProToast(`Série opravena pro den ${targetDay}!`); await renderHeatmap(); await renderShopModal();
};
document.getElementById("btnBuyMystery").onclick = async () => {
  const p = loadProProfile(); if (p.points < 1100) { alert("Potřebujete alespoň 1100 bodů."); return; }
  p.points -= 1100;
  const roll = Math.random();
  let msg = "";
  if (roll < 0.25 && p.freezes < 3) { p.freezes++; msg = "Tajemná truhla: 1x Streak Freeze!"; }
  else if (roll < 0.5) { p.boostUntil = Date.now() + 15 * 60 * 1000; msg = "Tajemná truhla: 2x Body Boost!"; }
  else { const w = [450, 800, 1200, 1700][Math.floor(Math.random() * 4)]; p.points += w; msg = `Tajemná truhla: +${w} bodů!`; }
  saveProProfile(p); launchConfetti(); playProTone("level"); showProToast(msg); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyShieldPack").onclick = async () => {
  const p = loadProProfile(); if (p.freezes >= 3) { alert("Zásobu Freeze už máte plnou (3/3)."); return; }
  if (p.points < 3000) { alert("Potřebujete alespoň 3000 bodů."); return; }
  p.points -= 3000; p.freezes = 3; saveProProfile(p); showProToast("Zásoba Streak Freeze doplněna na 3/3!"); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyTimeFreeze").onclick = async () => {
  const p = loadProProfile(); if (p.points < 600) { alert("Potřebujete alespoň 600 bodů."); return; }
  p.points -= 600; p.powerups = p.powerups || {}; p.powerups.timeFreeze = (p.powerups.timeFreeze || 0) + 1;
  saveProProfile(p); showProToast(`Zakoupeno Zmrazení času (celkem ${p.powerups.timeFreeze})`); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyFifty").onclick = async () => {
  const p = loadProProfile(); if (p.points < 500) { alert("Potřebujete alespoň 500 bodů."); return; }
  p.points -= 500; p.powerups = p.powerups || {}; p.powerups.fiftyFifty = (p.powerups.fiftyFifty || 0) + 1;
  saveProProfile(p); showProToast(`Zakoupena Nápověda 50:50 (celkem ${p.powerups.fiftyFifty})`); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyComboShield").onclick = async () => {
  const p = loadProProfile(); if (p.points < 750) { alert("Potřebujete alespoň 750 bodů."); return; }
  p.points -= 750; p.powerups = p.powerups || {}; p.powerups.comboShield = (p.powerups.comboShield || 0) + 1;
  saveProProfile(p); showProToast(`Zakoupen Štít Comba (celkem ${p.powerups.comboShield})`); await updateProHud(); await renderShopModal();
};

function recordMinigameQuestProgress() {
  const p = loadProProfile();
  const todayStr = getLocalDateString();
  if (!p.dailyQuests || p.dailyQuests.date !== todayStr) {
    p.dailyQuests = { date: todayStr, maxCombo: 0, cleanCount: 0, easyCount: 0, goodCount: 0, hardCount: 0, typeCount: 0, xpToday: 0, minigameCount: 0, readyIds: [], claimedIds: [] };
  }
  p.dailyQuests.minigameCount = (p.dailyQuests.minigameCount || 0) + 1;
  saveProProfile(p);
}

// --- MINI-GAMES CONTROLLER ---
function cleanGameLine(raw) {
  return String(raw || "")
    .replace(/!\[\[.*?\]\]/g, "")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/[*_`~]/g, "")
    .replace(/^[A-Za-zÀ-ž0-9\s/()_-]{2,32}:\s+/, "")
    .replace(/\s+/g, " ")
    .trim();
}
function getGamePairForCard(card) {
  let prompt = (card.title || extractTargetAnswer(card, true) || "").trim();
  let answer = (extractTargetAnswer(card, false) || "").trim();
  if (!prompt || !answer || prompt.toLowerCase() === answer.toLowerCase()) {
    const backLines = String(card.back || "")
      .split(/\r?\n/)
      .map(cleanGameLine)
      .filter(l => l && l.length >= 2 && !/^https?:\/\//i.test(l));
    const frontLines = String(card.front || "")
      .split(/\r?\n/)
      .map(cleanGameLine)
      .filter(l => l && l.length >= 2 && !/^https?:\/\//i.test(l));
    if (!prompt) prompt = frontLines[0] || backLines[0] || "Pojem";
    const distinct = backLines.find(l => l.toLowerCase() !== prompt.toLowerCase())
      || frontLines.find(l => l.toLowerCase() !== prompt.toLowerCase());
    if (distinct) {
      answer = distinct.length > 70 ? distinct.slice(0, 67).trim() + "..." : distinct;
    }
  }
  return { prompt: prompt || "Pojem", answer: answer || "Odpověď" };
}
const MIN_SEEN_FOR_GAMES = 10;
function getSeenDeckCards(deck) {
  if (!deck || !Array.isArray(deck.cards)) return [];
  return deck.cards.filter(c => (c.due && c.due > 0) || (c.reps && c.reps > 0) || (c.rev && c.rev.due > 0));
}
let _tmInterval = null, _gravRaf = null, _gravFrozenUntil = 0;
function stopAllMiniGames() {
  if (_tmInterval) { clearInterval(_tmInterval); _tmInterval = null; }
  if (_gravRaf) { cancelAnimationFrame(_gravRaf); _gravRaf = null; }
}
function showGamePane(paneId) {
  stopAllMiniGames();
  ["gamesMenuPane", "gameTimedMatchPane", "gameBossPane", "gameGravityPane", "gameScramblePane"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = id === paneId ? "block" : "none";
  });
  document.getElementById("btnGameBackMenu").style.display = paneId === "gamesMenuPane" ? "none" : "inline-flex";
}
async function updateGamesLockState() {
  const deck = await getSelectedGameDeck();
  const seen = getSeenDeckCards(deck);
  const unlocked = seen.length >= MIN_SEEN_FOR_GAMES;
  const infoEl = document.getElementById("gamesUnlockInfo");
  if (infoEl) {
    infoEl.innerText = unlocked
      ? `Odemčeno! Hraje se pouze z vašich ${seen.length} již viděných karet v tomto balíčku.`
      : `Zamčeno: v tomto balíčku máte zatím viděno ${seen.length} / ${MIN_SEEN_FOR_GAMES} karet. Projděte nejprve alespoň ${MIN_SEEN_FOR_GAMES} karet v učení.`;
    infoEl.style.color = unlocked ? "var(--accent)" : "#fbbf24";
  }
  ["btnStartTimedMatch", "btnStartBossFight", "btnStartGravity", "btnStartScramble"].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) {
      btn.disabled = !unlocked;
      btn.style.opacity = unlocked ? "1" : "0.45";
      btn.style.cursor = unlocked ? "pointer" : "not-allowed";
    }
  });
}
const GAME_FIELDS_KEY = "karty_game_fields_v1";
function extractFirstCardImage(card) {
  const combined = `${card.front || ""}\n${card.back || ""}`;
  const m1 = combined.match(/!\[\[([^\]]+)\]\]/);
  if (m1) return m1[1].split("|")[0].trim();
  const m2 = combined.match(/!\[[^\]]*\]\(([^)]+)\)/);
  if (m2) return m2[1].trim();
  const m3 = combined.match(/<img[^>]+src=["']([^"']+)["']/i);
  if (m3) return m3[1].trim();
  return "";
}
function extractCardLabeledFields(card) {
  const map = {};
  const lines = `${card.front || ""}\n${card.back || ""}`.split(/\r?\n/);
  for (const raw of lines) {
    const plain = raw.replace(/!\[\[.*?\]\]/g, "").replace(/!\[[^\]]*\]\([^)]*\)/g, "").replace(/<[^>]+>/g, " ").replace(/[*_`~]/g, "").trim();
    const m = plain.match(/^([A-Za-zÀ-ž0-9\s/()_-]{2,32}):\s+(.+)$/);
    if (m) {
      const lbl = m[1].trim();
      const val = m[2].replace(/\s+/g, " ").trim();
      if (lbl && val && !map[lbl]) map[lbl] = val;
    }
  }
  return map;
}
function discoverDeckGameFields(deck) {
  if (!deck || !Array.isArray(deck.cards)) return { hasImages: false, labels: [] };
  let hasImages = false;
  const counts = new Map();
  const sample = deck.cards.slice(0, 40);
  for (const c of sample) {
    if (!hasImages && extractFirstCardImage(c)) hasImages = true;
    const flds = extractCardLabeledFields(c);
    for (const k of Object.keys(flds)) counts.set(k, (counts.get(k) || 0) + 1);
  }
  const labels = Array.from(counts.entries()).filter(([, cnt]) => cnt >= 2 || sample.length < 5).map(([k]) => k);
  return { hasImages, labels };
}
function populateGameFieldSelectors(deck) {
  const selP = document.getElementById("selGamePromptField");
  const selA = document.getElementById("selGameAnswerField");
  if (!selP || !selA || !deck) return;
  const { hasImages, labels } = discoverDeckGameFields(deck);
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(GAME_FIELDS_KEY) || "{}"); } catch {}
  const prev = saved[deck.id] || {};

  const buildOpts = (isPrompt) => {
    let html = `<option value="__auto__">Automaticky</option>`;
    if (isPrompt && hasImages) html += `<option value="__image__">Obrázek karty</option>`;
    html += `<option value="__title__">Název karty (title)</option>`;
    labels.forEach(l => { html += `<option value="field:${escapeHtml(l)}">${escapeHtml(l)}</option>`; });
    if (!isPrompt && hasImages) html += `<option value="__image__">Obrázek karty</option>`;
    return html;
  };
  selP.innerHTML = buildOpts(true);
  selA.innerHTML = buildOpts(false);
  if (prev.prompt && Array.from(selP.options).some(o => o.value === prev.prompt)) selP.value = prev.prompt;
  else if (hasImages) selP.value = "__auto__";
  if (prev.answer && Array.from(selA.options).some(o => o.value === prev.answer)) selA.value = prev.answer;

  const saveSel = () => {
    try {
      const cur = JSON.parse(localStorage.getItem(GAME_FIELDS_KEY) || "{}");
      cur[deck.id] = { prompt: selP.value, answer: selA.value };
      localStorage.setItem(GAME_FIELDS_KEY, JSON.stringify(cur));
    } catch {}
  };
  selP.onchange = saveSel;
  selA.onchange = saveSel;
}
function resolveFieldSide(card, spec, fallbackText) {
  if (spec === "__image__") {
    const fn = extractFirstCardImage(card);
    if (fn) return { type: "image", src: fn, key: "img:" + fn };
  }
  if (spec === "__title__") {
    const t = (card.title || extractTargetAnswer(card, true) || fallbackText || "Pojem").trim();
    return { type: "text", text: t, key: t };
  }
  if (spec && spec.startsWith("field:")) {
    const lbl = spec.slice(6);
    const flds = extractCardLabeledFields(card);
    if (flds[lbl]) {
      const v = flds[lbl].length > 70 ? flds[lbl].slice(0, 67).trim() + "..." : flds[lbl];
      return { type: "text", text: v, key: v };
    }
  }
  return { type: "text", text: fallbackText, key: fallbackText };
}
function getSelectedGamePair(card) {
  const autoPair = getGamePairForCard(card);
  const pSpec = document.getElementById("selGamePromptField")?.value || "__auto__";
  const aSpec = document.getElementById("selGameAnswerField")?.value || "__auto__";
  const promptSide = pSpec === "__auto__" ? { type: "text", text: autoPair.prompt, key: autoPair.prompt } : resolveFieldSide(card, pSpec, autoPair.prompt);
  const answerSide = aSpec === "__auto__" ? { type: "text", text: autoPair.answer, key: autoPair.answer } : resolveFieldSide(card, aSpec, autoPair.answer);
  return {
    promptSide,
    answerSide,
    textPrompt: autoPair.prompt,
    textAnswer: answerSide.type === "text" ? answerSide.text : autoPair.answer
  };
}
async function renderGameSideInto(el, sideObj, deckId, imgClass = "game-card-img") {
  el.innerHTML = "";
  if (sideObj.type === "image" && sideObj.src) {
    el.classList.add("has-img");
    const img = document.createElement("img");
    img.className = imgClass;
    img.alt = "obrázek";
    el.appendChild(img);
    try {
      const url = typeof getMediaUrl === "function" ? await getMediaUrl(deckId, sideObj.src) : "";
      img.src = url || sideObj.src;
      if (!url) img.onerror = () => { img.onerror = () => { img.style.display = "none"; el.innerText = "Obrázek"; }; img.src = "media/" + sideObj.src; };
    } catch {
      img.src = sideObj.src;
    }
  } else {
    el.classList.remove("has-img");
    el.innerText = sideObj.text || "";
  }
}

async function openGamesHub(preselectedDeckId = null) {
  const decks = await dbGetAllDecks();
  const sel = document.getElementById("selGameDeck");
  sel.innerHTML = "";
  decks.forEach(d => {
    const seenCnt = getSeenDeckCards(d).length;
    sel.innerHTML += `<option value="${d.id}" ${preselectedDeckId === d.id ? "selected" : ""}>${escapeHtml(d.name)} (viděno ${seenCnt}/${d.cards.length})</option>`;
  });
  showGamePane("gamesMenuPane");
  const curDeck = await getSelectedGameDeck();
  populateGameFieldSelectors(curDeck);
  await updateGamesLockState();
  document.getElementById("gamesModal").classList.add("active");
}
document.getElementById("selGameDeck").onchange = async () => {
  showGamePane("gamesMenuPane");
  const d = await getSelectedGameDeck();
  populateGameFieldSelectors(d);
  await updateGamesLockState();
};
async function getSelectedGameDeck() {
  const id = document.getElementById("selGameDeck").value;
  return id ? await dbGetDeck(id) : null;
}
document.getElementById("btnOpenGames").onclick = () => openGamesHub(currentDeck ? currentDeck.id : null);
document.getElementById("gamesModalClose").onclick = () => { stopAllMiniGames(); document.getElementById("gamesModal").classList.remove("active"); };
document.getElementById("btnGameBackMenu").onclick = () => showGamePane("gamesMenuPane");

// 1. Timed Match (5 rounds, decreasing time, continuous shuffled replacement)
let _tmFreezeUntil = 0;
document.getElementById("btnStartTimedMatch").onclick = async () => {
  const deck = await getSelectedGameDeck();
  const seenCards = getSeenDeckCards(deck);
  if (seenCards.length < MIN_SEEN_FOR_GAMES) { alert(`Pro odemčení miniher musíte v balíčku projít alespoň ${MIN_SEEN_FOR_GAMES} karet.`); return; }
  showGamePane("gameTimedMatchPane");

  const ROUND_TIMES = [60, 50, 40, 32, 25];
  const PAIRS_PER_ROUND = 10;
  const VISIBLE_SLOTS = 5;
  let roundIdx = 0;
  let matchedInRound = 0;
  let timeLeft = ROUND_TIMES[0];
  let first = null;
  let roundLocked = false;
  _tmFreezeUntil = 0;

  const grid = document.getElementById("tmGrid");
  const lbl = document.getElementById("tmTimerLabel");
  const roundLbl = document.getElementById("tmRoundLabel");
  let leftSlots = [];
  let rightSlots = [];

  function pickFreshCard(excludeIds) {
    const avail = seenCards.filter(c => !excludeIds.has(c.id));
    const pool = avail.length > 0 ? avail : seenCards;
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function updateLabels() {
    if (roundLbl) roundLbl.innerText = `Kolo ${roundIdx + 1}/5 · ${matchedInRound}/${PAIRS_PER_ROUND}`;
    if (lbl) lbl.innerText = Date.now() < _tmFreezeUntil ? `Čas: ${timeLeft} s (Zmrazeno)` : `Čas: ${timeLeft} s`;
  }

  function renderGrid() {
    grid.innerHTML = "";
    for (let i = 0; i < VISIBLE_SLOTS; i++) {
      [leftSlots[i], rightSlots[i]].forEach((slot) => {
        const b = document.createElement("button");
        b.className = "match-btn";
        if (!slot) { b.style.visibility = "hidden"; grid.appendChild(b); return; }
        renderGameSideInto(b, slot.sideObj, deck.id, "game-card-img");
        b.onclick = () => handleTileClick(slot, b);
        slot.el = b;
        grid.appendChild(b);
      });
    }
  }

  function dealRound() {
    matchedInRound = 0;
    first = null;
    roundLocked = false;
    timeLeft = ROUND_TIMES[roundIdx];
    const sample = [...seenCards].sort(() => Math.random() - 0.5).slice(0, VISIBLE_SLOTS);
    leftSlots = sample.map(c => ({ id: c.id, side: "L", sideObj: getSelectedGamePair(c).promptSide, el: null }));
    rightSlots = sample.map(c => ({ id: c.id, side: "R", sideObj: getSelectedGamePair(c).answerSide, el: null }));
    leftSlots.sort(() => Math.random() - 0.5);
    rightSlots.sort(() => Math.random() - 0.5);
    updateLabels();
    renderGrid();
  }

  async function handleTileClick(slot, btn) {
    if (roundLocked || btn.classList.contains("matched")) return;
    if (!first) { first = { slot, btn }; btn.classList.add("selected"); return; }
    if (first.btn === btn) { btn.classList.remove("selected"); first = null; return; }
    if (first.slot.side === slot.side) {
      first.btn.classList.remove("selected");
      first = { slot, btn };
      btn.classList.add("selected");
      return;
    }

    if (first.slot.id === slot.id) {
      const aSlot = first.slot, aBtn = first.btn;
      const bSlot = slot, bBtn = btn;
      first = null;
      aBtn.classList.remove("selected");
      aBtn.classList.add("matched");
      bBtn.classList.add("matched");
      matchedInRound++;
      playProTone("good");
      updateLabels();

      if (matchedInRound >= PAIRS_PER_ROUND) {
        roundLocked = true;
        if (roundIdx + 1 < ROUND_TIMES.length) {
          roundIdx++;
          showProToast(`Kolo ${roundIdx}/5 hotovo! Další kolo je rychlejší.`);
          setTimeout(() => dealRound(), 450);
        } else {
          stopAllMiniGames();
          const p = loadProProfile(); p.points += 35; p.xp = (p.xp || 0) + 35; saveProProfile(p);
          recordMinigameQuestProgress();
          launchConfetti(); playProTone("level"); showProToast("Všech 5 kol spojovačky dokončeno! +35 b.");
          await updateProHud(); showGamePane("gamesMenuPane");
        }
        return;
      }

      // Replace matched pair with a fresh shuffled pair
      setTimeout(() => {
        if (roundLocked) return;
        const activeIds = new Set(leftSlots.filter(Boolean).map(s => s.id));
        const nextCard = pickFreshCard(activeIds);
        const pair = getSelectedGamePair(nextCard);
        const lIdx = leftSlots.indexOf(aSlot.side === "L" ? aSlot : bSlot);
        const rIdx = rightSlots.indexOf(aSlot.side === "R" ? aSlot : bSlot);
        if (lIdx >= 0 && rIdx >= 0) {
          const newL = { id: nextCard.id, side: "L", sideObj: pair.promptSide, el: null };
          const newR = { id: nextCard.id, side: "R", sideObj: pair.answerSide, el: null };
          // Swap into random slot positions so new pair is shuffled
          const swapL = Math.floor(Math.random() * VISIBLE_SLOTS);
          const swapR = Math.floor(Math.random() * VISIBLE_SLOTS);
          leftSlots[lIdx] = leftSlots[swapL];
          leftSlots[swapL] = newL;
          rightSlots[rIdx] = rightSlots[swapR];
          rightSlots[swapR] = newR;
          renderGrid();
        }
      }, 220);
    } else {
      const prevB = first.btn; prevB.classList.remove("selected"); prevB.classList.add("err"); btn.classList.add("err");
      first = null; playProTone("again");
      setTimeout(() => { prevB.classList.remove("err"); btn.classList.remove("err"); }, 350);
    }
  }

  dealRound();
  _tmInterval = setInterval(() => {
    if (Date.now() < _tmFreezeUntil) { updateLabels(); return; }
    timeLeft--;
    updateLabels();
    if (timeLeft <= 0) {
      stopAllMiniGames();
      alert(`Čas vypršel v kole ${roundIdx + 1}/5! Zkuste to znovu.`);
      showGamePane("gamesMenuPane");
    }
  }, 1000);
};
document.getElementById("btnUseTimeFreezeMatch").onclick = () => {
  const p = loadProProfile();
  if (!p.powerups || (p.powerups.timeFreeze || 0) <= 0) { alert("Nemáte Zmrazení času (lze koupit v Obchodě)."); return; }
  p.powerups.timeFreeze--; saveProProfile(p); _tmFreezeUntil = Date.now() + 10000; showProToast("Čas zmrazen na 10 s!");
};

// 2. Boss Fight
document.getElementById("btnStartBossFight").onclick = async () => {
  const deck = await getSelectedGameDeck();
  const seenCards = getSeenDeckCards(deck);
  if (seenCards.length < MIN_SEEN_FOR_GAMES) { alert(`Pro odemčení miniher musíte v balíčku projít alespoň ${MIN_SEEN_FOR_GAMES} karet.`); return; }
  showGamePane("gameBossPane");
  let bossHp = 100, playerHp = 5, bossCombo = 0;
  document.getElementById("bossNameLabel").innerText = `Boss: ${deck.name}`;
  function nextBossQ() {
    document.getElementById("bossHpText").innerText = `${bossHp} / 100 HP`;
    document.getElementById("bossHpBar").style.width = `${bossHp}%`;
    document.getElementById("playerBossHpText").innerText = `Vaše HP: ${playerHp} / 5`;
    document.getElementById("bossComboText").innerText = `Combo: ${bossCombo}x`;
    const card = seenCards[Math.floor(Math.random() * seenCards.length)];
    const pair = getSelectedGamePair(card);
    const correctKey = pair.answerSide.key;
    renderGameSideInto(document.getElementById("bossQuestionBox"), pair.promptSide, deck.id, "game-card-img-lg");
    const pool = seenCards.filter(c => c.id !== card.id).sort(() => Math.random() - 0.5);
    const opts = [pair.answerSide];
    const usedKeys = new Set([correctKey]);
    for (const c of pool) {
      const aSide = getSelectedGamePair(c).answerSide;
      if (aSide.key && !usedKeys.has(aSide.key)) { usedKeys.add(aSide.key); opts.push(aSide); if (opts.length >= 4) break; }
    }
    opts.sort(() => Math.random() - 0.5);
    const grid = document.getElementById("bossOptionsGrid");
    grid.innerHTML = "";
    opts.forEach(oSide => {
      const b = document.createElement("button");
      b.className = "quiz-option";
      renderGameSideInto(b, oSide, deck.id, "game-card-img");
      b.onclick = async () => {
        if (oSide.key === correctKey) {
          bossCombo++;
          const dmg = bossCombo >= 3 ? 30 : 20;
          bossHp = Math.max(0, bossHp - dmg);
          playProTone("good");
          if (bossHp <= 0) {
            const p = loadProProfile(); p.points += 20; p.xp = (p.xp || 0) + 20; saveProProfile(p);
            recordMinigameQuestProgress();
            launchConfetti(); playProTone("level"); showProToast("Boss poražen! +20 b.");
            await updateProHud(); showGamePane("gamesMenuPane");
            return;
          }
        } else {
          bossCombo = 0;
          playerHp--;
          playProTone("again");
          if (playerHp <= 0) {
            alert("Prohráli jste souboj s bossem! Zkuste to znovu.");
            showGamePane("gamesMenuPane");
            return;
          }
        }
        nextBossQ();
      };
      grid.appendChild(b);
    });
  }
  nextBossQ();
};

// 3. Gravity / Meteorites
document.getElementById("btnStartGravity").onclick = async () => {
  const deck = await getSelectedGameDeck();
  const seenCards = getSeenDeckCards(deck);
  if (seenCards.length < MIN_SEEN_FOR_GAMES) { alert(`Pro odemčení miniher musíte v balíčku projít alespoň ${MIN_SEEN_FOR_GAMES} karet.`); return; }
  showGamePane("gameGravityPane");
  let score = 0, yPos = 0, lastTs = performance.now();
  _gravFrozenUntil = 0;
  function spawnMeteor() {
    yPos = 0;
    document.getElementById("gravScoreLabel").innerText = `Skóre: ${score}`;
    const card = seenCards[Math.floor(Math.random() * seenCards.length)];
    const pair = getSelectedGamePair(card);
    const correctKey = pair.answerSide.key;
    const meteor = document.getElementById("gravMeteor");
    renderGameSideInto(meteor, pair.promptSide, deck.id, "game-card-img-meteor");
    const pool = seenCards.filter(c => c.id !== card.id).sort(() => Math.random() - 0.5);
    const opts = [pair.answerSide];
    const usedKeys = new Set([correctKey]);
    for (const c of pool) {
      const aSide = getSelectedGamePair(c).answerSide;
      if (aSide.key && !usedKeys.has(aSide.key)) { usedKeys.add(aSide.key); opts.push(aSide); if (opts.length >= 4) break; }
    }
    opts.sort(() => Math.random() - 0.5);
    const grid = document.getElementById("gravOptionsGrid");
    grid.innerHTML = "";
    opts.forEach(oSide => {
      const b = document.createElement("button");
      b.className = "quiz-option";
      renderGameSideInto(b, oSide, deck.id, "game-card-img");
      b.onclick = async () => {
        if (oSide.key === correctKey) {
          score += 2;
          const p = loadProProfile(); p.points += 2; p.xp = (p.xp || 0) + 2; saveProProfile(p);
          playProTone("good"); await updateProHud(); spawnMeteor();
        } else {
          b.classList.add("wrong"); playProTone("again");
        }
      };
      grid.appendChild(b);
    });
  }
  function step(ts) {
    const dt = (ts - lastTs) / 1000;
    lastTs = ts;
    if (Date.now() >= _gravFrozenUntil) {
      const speed = 22 + Math.min(60, score * 0.8);
      yPos += speed * dt;
    }
    const meteor = document.getElementById("gravMeteor");
    if (meteor) meteor.style.top = yPos + "px";
    if (yPos + ((meteor && meteor.offsetHeight) || 36) >= 254) {
      stopAllMiniGames();
      alert(`Konec hry! Celkové skóre: ${score} bodů.`);
      showGamePane("gamesMenuPane");
      return;
    }
    _gravRaf = requestAnimationFrame(step);
  }
  spawnMeteor();
  _gravRaf = requestAnimationFrame(step);
};
document.getElementById("btnUseTimeFreezeGrav").onclick = () => {
  const p = loadProProfile();
  if (!p.powerups || (p.powerups.timeFreeze || 0) <= 0) { alert("Nemáte Zmrazení času."); return; }
  p.powerups.timeFreeze--; saveProProfile(p); _gravFrozenUntil = Date.now() + 8000; showProToast("Pád karet zmrazen na 8 s!");
};

// 4. Word / Sentence Scramble
let _scrPool = [], _scrDeckId = null, _scrTarget = "", _scrBuilt = [];
document.getElementById("btnStartScramble").onclick = async () => {
  const deck = await getSelectedGameDeck();
  _scrPool = getSeenDeckCards(deck);
  _scrDeckId = deck ? deck.id : null;
  if (_scrPool.length < MIN_SEEN_FOR_GAMES) { alert(`Pro odemčení miniher musíte v balíčku projít alespoň ${MIN_SEEN_FOR_GAMES} karet.`); return; }
  showGamePane("gameScramblePane");
  nextScramble();
};
function nextScramble() {
  const card = _scrPool[Math.floor(Math.random() * _scrPool.length)];
  const pair = getSelectedGamePair(card);
  _scrTarget = pair.textAnswer.split(/\s*[;/]\s*/)[0].trim();
  renderGameSideInto(document.getElementById("scramblePromptBox"), pair.promptSide, _scrDeckId, "game-card-img-lg");
  const words = _scrTarget.split(/\s+/).filter(Boolean);
  const tokens = words.length > 1 ? words : _scrTarget.split("");
  const isWordMode = words.length > 1;
  const shuffled = tokens.map((val, idx) => ({ val, idx })).sort(() => Math.random() - 0.5);
  _scrBuilt = [];
  const ansBox = document.getElementById("scrambleAnswerBox");
  const bankBox = document.getElementById("scrambleBankBox");
  const renderScr = () => {
    ansBox.innerHTML = "";
    _scrBuilt.forEach(item => {
      const c = document.createElement("button");
      c.className = "scramble-chip";
      c.innerText = item.val;
      c.onclick = () => { _scrBuilt = _scrBuilt.filter(x => x.idx !== item.idx); renderScr(); };
      ansBox.appendChild(c);
    });
    bankBox.innerHTML = "";
    shuffled.forEach(item => {
      if (_scrBuilt.some(x => x.idx === item.idx)) return;
      const c = document.createElement("button");
      c.className = "scramble-chip";
      c.innerText = item.val;
      c.onclick = async () => {
        _scrBuilt.push(item);
        renderScr();
        const attempt = _scrBuilt.map(x => x.val).join(isWordMode ? " " : "");
        if (attempt.toLowerCase() === _scrTarget.toLowerCase()) {
          const p = loadProProfile(); p.points += 8; p.xp = (p.xp || 0) + 8; saveProProfile(p);
          recordMinigameQuestProgress();
          launchConfetti(); playProTone("level"); showProToast("Složeno správně! +8 b.");
          await updateProHud();
          setTimeout(nextScramble, 600);
        }
      };
      bankBox.appendChild(c);
    });
  };
  document.getElementById("btnScrambleClear").onclick = () => { _scrBuilt = []; renderScr(); };
  renderScr();
}
document.getElementById("btnScrambleNext").onclick = nextScramble;
document.getElementById("btnAddMilestone").onclick = async () => {
  const days = parseInt(document.getElementById("inpNewMsDays").value, 10);
  const title = document.getElementById("inpNewMsReward").value.trim() || `Milník ${days} dní`;
  const bonus = Math.max(0, parseInt(document.getElementById("inpNewMsBonus").value, 10) || 0);
  if (!days || days < 1) { alert("Zadejte platný počet dní."); return; }
  const p = loadProProfile();
  p.milestones.push({ id: "m_" + Date.now(), days, title, bonusPoints: bonus, claimed: false });
  saveProProfile(p); document.getElementById("inpNewMsReward").value = ""; await renderShopModal();
};

// --- ONE-CLICK CLOUD SYNC (GITHUB GIST) ---
const CLOUD_SYNC_KEY = "karty_pro_sync_v1";
function loadSyncConfig() {
  try { return JSON.parse(localStorage.getItem(CLOUD_SYNC_KEY) || "null"); } catch { return null; }
}
function saveSyncConfig(cfg) {
  if (!cfg) localStorage.removeItem(CLOUD_SYNC_KEY);
  else localStorage.setItem(CLOUD_SYNC_KEY, JSON.stringify(cfg));
}
function openSyncModal(msg = "") {
  const cfg = loadSyncConfig() || {};
  document.getElementById("inpSyncToken").value = cfg.token || "";
  document.getElementById("inpSyncGistId").value = cfg.gistId || "";
  document.getElementById("syncStatusMsg").innerText = msg;
  document.getElementById("syncModal").classList.add("active");
}
async function runCloudSync(silentIfUnconfigured = false) {
  const cfg = loadSyncConfig();
  if (!cfg || !cfg.token) {
    if (!silentIfUnconfigured) openSyncModal("Pro první synchronizaci vložte GitHub Token.");
    return;
  }
  const btn = document.getElementById("btnCloudSync");
  const origText = btn ? btn.innerText : "Synchronizovat";
  if (btn) { btn.disabled = true; btn.innerText = "Synchronizuji..."; }
  try {
    let remote = null;
    if (cfg.gistId) {
      const res = await fetch(`https://api.github.com/gists/${encodeURIComponent(cfg.gistId)}`, {
        headers: { Authorization: `Bearer ${cfg.token}`, Accept: "application/vnd.github+json" }
      });
      if (!res.ok) throw new Error(`GitHub Gist HTTP ${res.status}`);
      const gist = await res.json();
      const fileObj = gist.files && gist.files["karty_sync.json"];
      if (fileObj && fileObj.content) {
        try { remote = JSON.parse(fileObj.content); } catch {}
      }
    }

    const localDecks = await dbGetAllDecks();
    const localReviews = await dbGetAllReviews();
    const localProf = loadProProfile();

    // Merge proProfile (including opened chests in dailyQuests and milestones)
    const remProf = (remote && remote.proProfile) || {};
    const lDq = localProf.dailyQuests || {};
    const rDq = remProf.dailyQuests || {};
    let mergedDq = lDq;
    if (rDq.date && (!lDq.date || rDq.date > lDq.date)) {
      mergedDq = { ...rDq };
    } else if (rDq.date && lDq.date && rDq.date === lDq.date) {
      mergedDq = {
        date: lDq.date,
        maxCombo: Math.max(lDq.maxCombo || 0, rDq.maxCombo || 0),
        cleanCount: Math.max(lDq.cleanCount || 0, rDq.cleanCount || 0),
        easyCount: Math.max(lDq.easyCount || 0, rDq.easyCount || 0),
        goodCount: Math.max(lDq.goodCount || 0, rDq.goodCount || 0),
        hardCount: Math.max(lDq.hardCount || 0, rDq.hardCount || 0),
        typeCount: Math.max(lDq.typeCount || 0, rDq.typeCount || 0),
        xpToday: Math.max(lDq.xpToday || 0, rDq.xpToday || 0),
        minigameCount: Math.max(lDq.minigameCount || 0, rDq.minigameCount || 0),
        readyIds: Array.from(new Set([...(lDq.readyIds || []), ...(rDq.readyIds || [])])),
        claimedIds: Array.from(new Set([...(lDq.claimedIds || []), ...(rDq.claimedIds || [])]))
      };
    }
    const msMap = new Map();
    for (const m of (localProf.milestones || [])) { if (m && m.id) msMap.set(m.id, { ...m }); }
    for (const rm of (remProf.milestones || [])) {
      if (!rm || !rm.id) continue;
      const cur = msMap.get(rm.id);
      if (cur) msMap.set(rm.id, { ...cur, claimed: Boolean(cur.claimed || rm.claimed) });
      else msMap.set(rm.id, { ...rm });
    }
    const mergedProf = {
      ...getDefaultProProfile(),
      ...localProf,
      points: Math.max(localProf.points || 0, remProf.points || 0),
      xp: Math.max(localProf.xp || 0, remProf.xp || 0),
      freezes: Math.max(localProf.freezes || 0, remProf.freezes || 0),
      boostUntil: Math.max(localProf.boostUntil || 0, remProf.boostUntil || 0),
      unlockedThemes: Array.from(new Set([...(localProf.unlockedThemes || []), ...(remProf.unlockedThemes || [])])),
      frozenDates: Array.from(new Set([...(localProf.frozenDates || []), ...(remProf.frozenDates || [])])),
      dailyBonusDates: Array.from(new Set([...(localProf.dailyBonusDates || []), ...(remProf.dailyBonusDates || [])])),
      dailyQuests: mergedDq,
      milestones: Array.from(msMap.values()),
      powerups: {
        timeFreeze: Math.max(localProf.powerups?.timeFreeze || 0, remProf.powerups?.timeFreeze || 0),
        fiftyFifty: Math.max(localProf.powerups?.fiftyFifty || 0, remProf.powerups?.fiftyFifty || 0),
        comboShield: Math.max(localProf.powerups?.comboShield || 0, remProf.powerups?.comboShield || 0)
      }
    };
    saveProProfile(mergedProf);

    // Merge decks, opened/seen cards, settings & history
    const normName = (s) => (s || "").toLowerCase().replace(/[_\s]+/g, " ").trim();
    const remDecks = (remote && Array.isArray(remote.decks)) ? remote.decks : [];
    let mergedCardUpdates = 0;
    for (const d of localDecks) {
      const rd = remDecks.find(x => (x.id && x.id === d.id) || normName(x.name) === normName(d.name));
      if (!rd) continue;
      const byId = new Map();
      const byTitle = new Map();
      for (const rc of (rd.cards || [])) {
        if (rc.id) byId.set(rc.id, rc);
        if (rc.title) byTitle.set(rc.title.trim().toLowerCase(), rc);
      }
      let changed = false;
      d.cards = (d.cards || []).map(lc => {
        const rc = (lc.id && byId.get(lc.id)) || (lc.title && byTitle.get(lc.title.trim().toLowerCase()));
        if (!rc) return lc;
        const lLast = lc.lastReview || 0, rLast = rc.lastReview || 0;
        const lReps = lc.reps || 0, rReps = rc.reps || 0;
        const rBetter = rLast > lLast || (rLast === lLast && (rReps > lReps || (rReps === lReps && ((rc.due || 0) > (lc.due || 0) || (rc.state || 0) > (lc.state || 0)))));
        if (rBetter) {
          changed = true; mergedCardUpdates++;
          lc = { ...lc, interval: rc.interval || 0, reps: rc.reps || 0, ease: rc.ease || 2.5, due: rc.due || 0, state: rc.state || 0, lastReview: rc.lastReview || 0 };
        }
        if (rc.rev && (!lc.rev || (rc.rev.lastReview || 0) > (lc.rev.lastReview || 0) || (rc.rev.reps || 0) > (lc.rev.reps || 0) || (rc.rev.due || 0) > (lc.rev.due || 0))) {
          changed = true;
          lc = { ...lc, rev: { ...rc.rev } };
        }
        return lc;
      });
      if (Array.isArray(rd.history) && rd.history.length > 0) {
        const hKey = (h) => `${h.dateStr || ""}|${h.cardId || ""}|${h.timestamp || h.interval || 0}`;
        const localHist = Array.isArray(d.history) ? [...d.history] : [];
        const hSet = new Set(localHist.map(hKey));
        for (const rh of rd.history) {
          const k = hKey(rh);
          if (!hSet.has(k)) { hSet.add(k); localHist.push(rh); changed = true; }
        }
        d.history = localHist;
      }
      if (rd.settings && typeof rd.settings === "object") {
        d.settings = { ...rd.settings, ...(d.settings || {}) };
      }
      if (changed) await dbSaveDeck(d);
    }

    // Merge reviews for heatmap
    const revKey = (r) => `${r.dateStr || ""}|${r.cardId || ""}|${r.deckId || ""}|${r.interval || 0}`;
    const localRevSet = new Set(localReviews.map(revKey));
    const remReviews = (remote && Array.isArray(remote.reviews)) ? remote.reviews : [];
    const mergedReviews = [...localReviews];
    for (const rr of remReviews) {
      const k = revKey(rr);
      if (!localRevSet.has(k)) {
        localRevSet.add(k);
        mergedReviews.push(rr);
        await dbAddReview(rr);
      }
    }

    // Build payload to upload (preserve remote decks not present locally too)
    const exportDecks = localDecks.map(d => ({
      id: d.id, name: d.name,
      settings: d.settings || {},
      history: Array.isArray(d.history) ? d.history.slice(-2000) : [],
      cards: (d.cards || []).map(c => ({
        id: c.id, title: c.title, interval: c.interval || 0, reps: c.reps || 0,
        ease: c.ease || 2.5, due: c.due || 0, state: c.state || 0, lastReview: c.lastReview || 0,
        rev: c.rev || null
      }))
    }));
    for (const rd of remDecks) {
      if (!exportDecks.some(x => (x.id && x.id === rd.id) || normName(x.name) === normName(rd.name))) {
        exportDecks.push(rd);
      }
    }
    const payload = { version: 1, syncedAt: Date.now(), proProfile: mergedProf, decks: exportDecks, reviews: mergedReviews.slice(-4000) };
    const body = { description: "Karty Pro Sync", public: false, files: { "karty_sync.json": { content: JSON.stringify(payload) } } };
    const endpoint = cfg.gistId ? `https://api.github.com/gists/${encodeURIComponent(cfg.gistId)}` : "https://api.github.com/gists";
    const method = cfg.gistId ? "PATCH" : "POST";
    const saveRes = await fetch(endpoint, {
      method,
      headers: { Authorization: `Bearer ${cfg.token}`, Accept: "application/vnd.github+json", "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!saveRes.ok) throw new Error(`Uložení do Gistu selhalo (HTTP ${saveRes.status})`);
    const savedGist = await saveRes.json();
    if (!cfg.gistId && savedGist.id) {
      cfg.gistId = savedGist.id;
      saveSyncConfig(cfg);
      const gi = document.getElementById("inpSyncGistId");
      if (gi) gi.value = savedGist.id;
    }

    if (typeof loadDeckList === "function") await loadDeckList();
    if (typeof renderHeatmap === "function") await renderHeatmap();
    await updateProHud();
    showProToast(`Synchronizováno! (${mergedCardUpdates} aktualizací karet)`);
    const sm = document.getElementById("syncStatusMsg");
    if (sm) sm.innerText = "Hotovo! Postup je synchronizován.";
  } catch (err) {
    console.error(err);
    showProToast("Chyba synchronizace: " + err.message);
    const sm = document.getElementById("syncStatusMsg");
    if (sm) sm.innerText = "Chyba: " + err.message;
  } finally {
    if (btn) { btn.disabled = false; btn.innerText = origText; }
  }
}

document.getElementById("syncModalClose").onclick = () => document.getElementById("syncModal").classList.remove("active");
document.getElementById("syncModal").addEventListener("click", (e) => { if (e.target.id === "syncModal") e.target.classList.remove("active"); });
document.getElementById("btnSyncSaveConnect").onclick = async () => {
  const token = document.getElementById("inpSyncToken").value.trim();
  const gistId = document.getElementById("inpSyncGistId").value.trim();
  if (!token) { alert("Vložte prosím GitHub Token."); return; }
  saveSyncConfig({ token, gistId });
  await runCloudSync(false);
};
document.getElementById("btnSyncCopyPair").onclick = async () => {
  const cfg = loadSyncConfig();
  if (!cfg || !cfg.token || !cfg.gistId) { alert("Nejprve klikněte na 'Uložit & synchronizovat', aby se vytvořilo Gist ID."); return; }
  const pairUrl = `${location.origin}${location.pathname}#sync=${encodeURIComponent(cfg.gistId + ":" + cfg.token)}`;
  try {
    await navigator.clipboard.writeText(pairUrl);
    showProToast("Párovací odkaz zkopírován! Otevřete ho na telefonu.");
  } catch {
    prompt("Zkopírujte tento odkaz a otevřete ho na telefonu:", pairUrl);
  }
};
document.getElementById("btnSyncDisconnect").onclick = () => {
  saveSyncConfig(null);
  document.getElementById("inpSyncToken").value = "";
  document.getElementById("inpSyncGistId").value = "";
  document.getElementById("syncStatusMsg").innerText = "Synchronizace odpojena.";
};

window.addEventListener("DOMContentLoaded", () => {
  if (location.hash && location.hash.startsWith("#sync=")) {
    try {
      const raw = decodeURIComponent(location.hash.slice(6));
      const idx = raw.indexOf(":");
      if (idx > 0) {
        const gistId = raw.slice(0, idx).trim();
        const token = raw.slice(idx + 1).trim();
        if (gistId && token) {
          saveSyncConfig({ gistId, token });
          history.replaceState(null, "", location.pathname + location.search);
          setTimeout(() => runCloudSync(true), 600);
        }
      }
    } catch {}
  }
  const bSync = document.getElementById("btnCloudSync");
  const bSetup = document.getElementById("btnCloudSyncSetup");
  if (bSync) bSync.onclick = () => runCloudSync(false);
  if (bSetup) bSetup.onclick = () => openSyncModal();
  setTimeout(() => { updateProHud(); }, 300);
});
"""

assert "</style>" in html
html = html.replace("</style>", PRO_CSS + "\n</style>", 1)

assert '<div class="nav-actions">' in html
html = html.replace('<div class="nav-actions">', PRO_HEADER_HUD + '\n  <div class="nav-actions">', 1)

assert '<section id="decksView">' in html
html = html.replace('<section id="decksView">', '<section id="decksView">\n' + PRO_DASHBOARD_HTML, 1)

assert '<div class="deck-list" id="deckList">' in html
html = html.replace('<div class="deck-list" id="deckList">', PRO_EXTRA_BAR_HTML + '\n    <div class="deck-list" id="deckList">', 1)

assert '<div class="progress-pills">' in html
html = html.replace('<div class="progress-pills">', '<span class="pro-combo-badge" id="proComboBadge">Combo 3x</span>\n        <div class="progress-pills">', 1)

assert "<!-- HELP MODAL -->" in html
html = html.replace("<!-- HELP MODAL -->", PRO_MODALS_HTML + "\n<!-- HELP MODAL -->", 1)

html = html.replace(
    "      version: 1,\n      exportedAt: Date.now(),",
    "      version: 1,\n      exportedAt: Date.now(),\n      proProfile: loadProProfile(),",
)
html = html.replace(
    "    await loadDeckList();\n    alert(`Synchronizace dokončena!",
    "    if (data.proProfile) {\n      const lp = loadProProfile();\n      const merged = { ...lp, ...data.proProfile, points: Math.max(lp.points || 0, data.proProfile.points || 0), frozenDates: Array.from(new Set([...(lp.frozenDates || []), ...(data.proProfile.frozenDates || [])])) };\n      saveProProfile(merged);\n      await updateProHud();\n    }\n    await loadDeckList();\n    alert(`Synchronizace dokončena!",
)

assert "// Initial boot" in html
html = html.replace("// Initial boot", PRO_JS + "\n// Initial boot", 1)

# --- PRO-ONLY LANGUAGE, MATCHING, SKILL PATH, LEVENSHTEIN & EDITOR PATCHES ---
PRO_PATCHES = [
    (
        '''        <div class="mode-toggle-group" style="width:100%; display:grid; grid-template-columns:1fr 1fr;">
          <button class="btn-mode-tgl active" id="btnModeFlip" title="Režim otáčení karty">Otáčecí</button>
          <button class="btn-mode-tgl" id="btnModeType" title="Režim vepisování z klávesnice">Vepisovací</button>
        </div>''',
        '''        <div class="mode-toggle-group" style="width:100%; display:grid; grid-template-columns:1fr 1fr;">
          <button class="btn-mode-tgl active" id="btnModeFlip" title="Režim otáčení karty">Otáčecí</button>
          <button class="btn-mode-tgl" id="btnModeType" title="Režim vepisování z klávesnice">Vepisovací</button>
          <button class="btn-mode-tgl" id="btnModeQuiz" title="Kvízový výběr ze 4 možností">Výběr ze 4</button>
          <button class="btn-mode-tgl" id="btnModeDictation" title="Poslech a psaní diktátu">Diktát</button>
        </div>''',
    ),
    (
        '''        <label class="switch-label">
          <input type="checkbox" id="chkReverseStudy">
          <span>Otočit směr</span>
        </label>''',
        '''        <label class="switch-label">
          <input type="checkbox" id="chkReverseStudy">
          <span>Otočit směr (oddělený postup)</span>
        </label>
        <label class="switch-label">
          <input type="checkbox" id="chkIgnoreDiacritics">
          <span>Ignorovat diakritiku při psaní</span>
        </label>
        <label class="switch-label">
          <input type="checkbox" id="chkAutoTts">
          <span>Automaticky přečíst kartu</span>
        </label>
        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
          <span style="font-size:0.8rem;">Jazyk čtení (TTS):</span>
          <select id="selTtsLang" class="select-sm">
            <option value="en-US">Angličtina (EN)</option>
            <option value="de-DE">Němčina (DE)</option>
            <option value="es-ES">Španělština (ES)</option>
            <option value="fr-FR">Francouzština (FR)</option>
            <option value="it-IT">Italština (IT)</option>
            <option value="cs-CZ">Čeština (CS)</option>
          </select>
        </div>''',
    ),
    (
        '''        <button class="btn-mode-tgl" id="btnStudyRenameDeck" style="width:100%; border:1px solid var(--border-color); padding:7px 10px;" title="Přejmenovat tento balíček">Přejmenovat balíček</button>''',
        '''        <button class="btn-mode-tgl" id="btnStudyRenameDeck" style="width:100%; border:1px solid var(--border-color); padding:7px 10px;" title="Přejmenovat tento balíček">Přejmenovat balíček</button>
        <button class="btn-mode-tgl" id="btnEditCurrentCard" style="width:100%; border:1px solid var(--border-color); padding:7px 10px;" title="Upravit tuto kartu">Upravit tuto kartu</button>
        <button class="btn-mode-tgl" id="btnOpenMatchFromStudy" style="width:100%; border:1px solid var(--border-color); padding:7px 10px;" title="Procvičit párováním dvojic">Párování dvojic</button>''',
    ),
    (
        '''        <button class="anki-menu-item btn-menu-subdecks">Podbalíčky${groupByField ? " (aktivní)" : ""}</button>''',
        '''        <button class="anki-menu-item btn-menu-skillpath">Cesta lekcí (uzly po 15)</button>
        <button class="anki-menu-item btn-menu-match">Párování dvojic</button>
        <button class="anki-menu-item btn-menu-subdecks">Podbalíčky${groupByField ? " (aktivní)" : ""}</button>''',
    ),
    (
        '''    rowEl.querySelector(".btn-menu-subdecks").onclick = async () => {''',
        '''    rowEl.querySelector(".btn-menu-skillpath").onclick = () => { menuEl.classList.remove("open"); openSkillPath(deck); };
    rowEl.querySelector(".btn-menu-match").onclick = () => { menuEl.classList.remove("open"); openMatchingGame(deck); };
    rowEl.querySelector(".btn-menu-subdecks").onclick = async () => {''',
    ),
    (
        '''          <div class="card-question" id="cardQuestion">
            <!-- Otázka -->
          </div>

          <!-- TYPE-IN INPUT BOX (VISIBLE ONLY IN TYPE MODE) -->
          <div class="type-input-area" id="typeInputArea" style="display:none;">
            <div class="type-input-box">
              <input type="text" id="typeTextInput" class="type-text-input" placeholder="Vepište název / odpověď..." autocomplete="off" autocapitalize="off" spellcheck="false">
              <button class="btn btn-primary" id="btnCheckType" style="padding:0 20px;">Ověřit</button>
            </div>
            <div class="type-diff-display" id="typeDiffDisplay" style="display:none;">
              <!-- Character diff result -->
            </div>
          </div>''',
        '''          <div class="card-question" id="cardQuestion">
            <!-- Otázka -->
          </div>
          <div style="display:flex; justify-content:center; gap:8px; margin-top:4px;">
            <button class="btn btn-sm" id="btnSpeakQuestion" style="font-size:0.78rem; padding:4px 10px;" title="Přečíst text karty nahlas">Přečíst nahlas</button>
          </div>

          <!-- TYPE-IN INPUT BOX (VISIBLE ONLY IN TYPE MODE) -->
          <div class="type-input-area" id="typeInputArea" style="display:none;">
            <div class="type-input-box">
              <input type="text" id="typeTextInput" class="type-text-input" placeholder="Vepište odpověď (více variant oddělte / nebo ;)..." autocomplete="off" autocapitalize="off" spellcheck="false">
              <button class="btn btn-sm" id="btnVoiceInput" style="padding:0 10px;" title="Nadiktovat odpověď hlasem">Mikrofon</button>
              <button class="btn btn-sm" id="btnTypeHint" style="padding:0 12px;" title="Odhalit další písmeno">Nápověda</button>
              <button class="btn btn-primary" id="btnCheckType" style="padding:0 20px;">Ověřit</button>
            </div>
            <div class="type-hint-box" id="typeHintDisplay" style="display:none;"></div>
            <div class="type-diff-display" id="typeDiffDisplay" style="display:none;">
              <!-- Character diff result -->
            </div>
          </div>

          <!-- QUIZ 4-CHOICE AREA -->
          <div style="display:none; flex-direction:column; gap:8px;" id="quizWrapArea">
            <div style="display:flex; justify-content:flex-end;">
              <button class="btn btn-sm" id="btnUseFiftyFifty" style="font-size:0.76rem;">Použít 50:50</button>
            </div>
            <div class="quiz-grid" id="quizArea"></div>
          </div>''',
    ),
    (
        '''  // 1. Nahrazení Obsidian obrázků ![[nazev.jpg]]
  let text = content.replace(/!\\[\\[(.*?)\\]\\]/g, (match, fn) => {
    const cleanFn = fn.trim().split('/').pop().split('\\\\').pop();
    return protectTag(`<img src="" data-src="${cleanFn}" class="card-img-thumb pending-media" alt="${cleanFn}">`);
  });''',
        '''  let text = content.replace(/\\{\\{c\\d+::([^:}]+)(?:::([^}]+))?\\}\\}/gi, (match, ans, hint) => {
    if (typeof window._proClozeMode !== "undefined" && window._proClozeMode === "question") {
      const label = hint ? `[${escapeHtml(hint)}]` : "[...]";
      return protectTag(`<span class="cloze-blank">${label}</span>`);
    }
    return protectTag(`<span class="cloze-reveal">${escapeHtml(ans)}</span>`);
  });
  text = text.replace(/\\[sound:([^\\]]+)\\]/gi, (match, fn) => {
    const cleanFn = fn.trim().split('/').pop().split('\\\\').pop();
    return protectTag(`<audio controls class="card-audio-player pending-audio" data-src="${cleanFn}"></audio>`);
  });
  text = text.replace(/!\\[\\[(.*?)\\]\\]/g, (match, fn) => {
    const cleanFn = fn.trim().split('|')[0].split('/').pop().split('\\\\').pop();
    if (/\\.(mp3|wav|ogg|m4a)$/i.test(cleanFn)) {
      return protectTag(`<audio controls class="card-audio-player pending-audio" data-src="${cleanFn}"></audio>`);
    }
    return protectTag(`<img src="" data-src="${cleanFn}" class="card-img-thumb pending-media" alt="${cleanFn}">`);
  });''',
    ),
    (
        '''    }
  }
}

// --- LIGHTBOX ---''',
        '''    }
  }
  const audios = container.querySelectorAll("audio.pending-audio");
  for (const aud of audios) {
    const filename = aud.getAttribute("data-src");
    if (filename) {
      const url = await getMediaUrl(deckId, filename);
      aud.src = url || filename;
    }
  }
}

// --- LIGHTBOX ---''',
    ),
    (
        "lower.endsWith('.gif')) {",
        "lower.endsWith('.gif') || lower.endsWith('.mp3') || lower.endsWith('.wav') || lower.endsWith('.ogg') || lower.endsWith('.m4a')) {",
    ),
    (
        '''function calcNextIntervals(card, deckArg) {
  const reps = card.reps || 0;
  const ease = card.ease || 2.5;
  const interval = card.interval || 0;
  const state = (typeof card.state === "number") ? card.state : ((!card.due || card.due === 0) ? 0 : (interval < 1 ? 1 : 2));''',
        '''function getCardSrsObj(card) {
  const isRev = document.getElementById("chkReverseStudy") && document.getElementById("chkReverseStudy").checked;
  if (!isRev) return card;
  if (!card.rev) card.rev = { interval: 0, reps: 0, ease: 2.5, due: 0, state: 0 };
  return card.rev;
}

function calcNextIntervals(card, deckArg) {
  const srs = getCardSrsObj(card);
  const reps = srs.reps || 0;
  const ease = srs.ease || 2.5;
  const interval = srs.interval || 0;
  const state = (typeof srs.state === "number") ? srs.state : ((!srs.due || srs.due === 0) ? 0 : (interval < 1 ? 1 : 2));''',
    ),
    (
        '''function extractTargetAnswer(card, isReverse) {
  if (!card) return "";''',
        '''function extractTargetAnswer(card, isReverse) {
  if (!card) return "";
  const rawSide = isReverse ? card.back : card.front;
  const clozeMatch = rawSide && rawSide.match(/\\{\\{c\\d+::([^:}]+)(?:::[^}]+)?\\}\\}/i);
  if (clozeMatch && clozeMatch[1]) return clozeMatch[1].trim();''',
    ),
    (
        '''function compareAnswers(typed, target) {
  const cleanTarget = target.replace(/<[^>]+>/g, '').trim();
  const tTrim = typed.trim();
  const isMatch = tTrim.toLowerCase() === cleanTarget.toLowerCase();

  let diffHtml = "";
  const maxLen = Math.max(tTrim.length, cleanTarget.length);
  for (let i = 0; i < maxLen; i++) {
    const chTyped = tTrim[i] || "";
    const chTarget = cleanTarget[i] || "";

    if (i < tTrim.length && i < cleanTarget.length) {
      if (chTyped.toLowerCase() === chTarget.toLowerCase()) {
        diffHtml += `<span class="diff-char diff-ok">${escapeHtml(chTyped)}</span>`;
      } else {
        diffHtml += `<span class="diff-char diff-err">${escapeHtml(chTyped)}</span>`;
      }
    } else if (i < tTrim.length) {
      diffHtml += `<span class="diff-char diff-err">${escapeHtml(chTyped)}</span>`;
    } else {
      diffHtml += `<span class="diff-char diff-miss">${escapeHtml(chTarget)}</span>`;
    }
  }

  return { isMatch, diffHtml, target: cleanTarget, typed: tTrim };
}''',
        '''function normalizeForCompare(str, ignoreDiacritics) {
  let s = str.trim().toLowerCase();
  if (ignoreDiacritics) s = s.normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
  return s;
}

function compareAnswers(typed, target) {
  const cleanTargetRaw = target.replace(/<[^>]+>/g, '').trim();
  const candidates = cleanTargetRaw.split(/\\s*[;/]\\s*/).map(s => s.trim()).filter(Boolean);
  const list = candidates.length > 0 ? candidates : [cleanTargetRaw];
  const ignoreDia = document.getElementById("chkIgnoreDiacritics") ? document.getElementById("chkIgnoreDiacritics").checked : false;
  const tTrim = typed.trim();
  const tNorm = normalizeForCompare(tTrim, ignoreDia);
  let bestTarget = list[0];
  let isMatch = false;
  let isNearMatch = false;
  for (const cand of list) {
    const cNorm = normalizeForCompare(cand, ignoreDia);
    if (tNorm === cNorm) { bestTarget = cand; isMatch = true; break; }
    if (!isMatch && cNorm.length >= 4 && levenshteinDist(tNorm, cNorm) <= 2) {
      bestTarget = cand;
      isNearMatch = true;
    }
  }
  let diffHtml = "";
  const maxLen = Math.max(tTrim.length, bestTarget.length);
  for (let i = 0; i < maxLen; i++) {
    const chTyped = tTrim[i] || "";
    const chTarget = bestTarget[i] || "";
    if (i < tTrim.length && i < bestTarget.length) {
      diffHtml += normalizeForCompare(chTyped, ignoreDia) === normalizeForCompare(chTarget, ignoreDia)
        ? `<span class="diff-char diff-ok">${escapeHtml(chTyped)}</span>`
        : `<span class="diff-char diff-err">${escapeHtml(chTyped)}</span>`;
    } else if (i < tTrim.length) {
      diffHtml += `<span class="diff-char diff-err">${escapeHtml(chTyped)}</span>`;
    } else {
      diffHtml += `<span class="diff-char diff-miss">${escapeHtml(chTarget)}</span>`;
    }
  }
  return { isMatch, isNearMatch, diffHtml, target: cleanTargetRaw, typed: tTrim };
}

let _hintRevealCount = 0;
function renderQuizOptions(card, isReverse) {
  const quizBox = document.getElementById("quizArea");
  if (!quizBox) return;
  quizBox.innerHTML = "";
  const correctAns = extractTargetAnswer(card, isReverse);
  const pool = (currentDeck && Array.isArray(currentDeck.cards)) ? currentDeck.cards : [];
  const distractors = [];
  const seen = new Set([correctAns.toLowerCase()]);
  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  for (const c of shuffled) {
    if (c.id === card.id) continue;
    const ans = extractTargetAnswer(c, isReverse);
    if (ans && !seen.has(ans.toLowerCase())) {
      seen.add(ans.toLowerCase());
      distractors.push(ans);
      if (distractors.length >= 3) break;
    }
  }
  const options = [correctAns, ...distractors].sort(() => Math.random() - 0.5);
  options.forEach(opt => {
    const btn = document.createElement("button");
    btn.className = "quiz-option";
    btn.innerText = opt;
    btn.onclick = () => {
      quizBox.querySelectorAll(".quiz-option").forEach(b => {
        b.disabled = true;
        if (b.innerText === correctAns) b.classList.add("correct");
      });
      if (opt !== correctAns) {
        btn.classList.add("wrong");
        showProToast("Špatná volba, zkuste si ji zapamatovat.");
      }
      revealAnswer();
    };
    quizBox.appendChild(btn);
  });
}''',
    ),
    (
        '''  qBox.innerHTML = await renderContentToHtml(qContent, currentDeck.id);
  aBox.innerHTML = await renderContentToHtml(aContent, currentDeck.id);''',
        '''  _hintRevealCount = 0;
  window._proClozeMode = "question";
  qBox.innerHTML = await renderContentToHtml(qContent, currentDeck.id);
  window._proClozeMode = "answer";
  aBox.innerHTML = await renderContentToHtml(aContent, currentDeck.id);''',
    ),
    (
        '''  if (cardStudyMode === "type") {
    typeArea.style.display = "flex";
    typeInput.value = "";
    typeDiff.style.display = "none";
    typeDiff.innerHTML = "";
    btnFlip.style.display = "none";
    setTimeout(() => typeInput.focus(), 50);
  } else {
    typeArea.style.display = "none";
    btnFlip.style.display = "block";
  }''',
        '''  const hintBox = document.getElementById("typeHintDisplay");
  const quizWrap = document.getElementById("quizWrapArea");
  if (hintBox) { hintBox.style.display = "none"; hintBox.innerText = ""; }
  qBox.style.opacity = "1";
  if (cardStudyMode === "type" || cardStudyMode === "dictation") {
    typeArea.style.display = "flex";
    if (quizWrap) quizWrap.style.display = "none";
    typeInput.value = "";
    typeDiff.style.display = "none";
    typeDiff.innerHTML = "";
    btnFlip.style.display = "none";
    if (cardStudyMode === "dictation") {
      qBox.innerHTML = `<div style="text-align:center; padding:18px; color:var(--text-muted);">Poslouchejte diktát a napište co slyšíte...</div>`;
      setTimeout(() => { const b = document.getElementById("btnSpeakQuestion"); if (b) b.click(); }, 150);
    }
    setTimeout(() => typeInput.focus(), 50);
  } else if (cardStudyMode === "quiz") {
    typeArea.style.display = "none";
    if (quizWrap) { quizWrap.style.display = "flex"; renderQuizOptions(currentCard, isReverse); }
    btnFlip.style.display = "none";
  } else {
    typeArea.style.display = "none";
    if (quizWrap) quizWrap.style.display = "none";
    btnFlip.style.display = "block";
  }
  const chkAuto = document.getElementById("chkAutoTts");
  if (chkAuto && chkAuto.checked && cardStudyMode !== "dictation") {
    setTimeout(() => { const b = document.getElementById("btnSpeakQuestion"); if (b) b.click(); }, 180);
  }''',
    ),
    (
        '''  typeDiff.innerHTML = `
    <div><strong>Zadáno:</strong> ${result.diffHtml || '<em style="color:#f87171;">(prázdné)</em>'}</div>
    <div><strong>Správně:</strong> <span style="color:#86efac; font-weight:700;">${escapeHtml(result.target)}</span></div>
  `;''',
        '''  let nearMsg = result.isNearMatch ? '<div style="color:#fbbf24; font-weight:700;">Skoro správně! Dej si pozor na překlep.</div>' : '';
  typeDiff.innerHTML = `
    ${nearMsg}
    <div><strong>Zadáno:</strong> ${result.diffHtml || '<em style="color:#f87171;">(prázdné)</em>'}</div>
    <div><strong>Správně:</strong> <span style="color:var(--accent); font-weight:700;">${escapeHtml(result.target)}</span></div>
  `;''',
    ),
    (
        '''    const wasNew = !cardInDeck.due || cardInDeck.due === 0;
    cardInDeck.interval = choice.newInterval;
    cardInDeck.ease = choice.newEase;
    cardInDeck.reps = choice.newReps;
    cardInDeck.due = Date.now() + choice.ms;
    cardInDeck.lastReview = Date.now();
    cardInDeck.state = (typeof choice.newState === "number") ? choice.newState : (ratingKey === "again" ? 1 : 2);''',
        '''    const srsTarget = getCardSrsObj(cardInDeck);
    const wasNew = !srsTarget.due || srsTarget.due === 0;
    srsTarget.interval = choice.newInterval;
    srsTarget.ease = choice.newEase;
    srsTarget.reps = choice.newReps;
    srsTarget.due = Date.now() + choice.ms;
    srsTarget.lastReview = Date.now();
    srsTarget.state = (typeof choice.newState === "number") ? choice.newState : (ratingKey === "again" ? 1 : 2);''',
    ),
    (
        '''const btnModeFlip = document.getElementById("btnModeFlip");
const btnModeType = document.getElementById("btnModeType");

btnModeFlip.onclick = () => {
  cardStudyMode = "flip";
  btnModeFlip.classList.add("active");
  btnModeType.classList.remove("active");
  loadCard(currentIndex);
};

btnModeType.onclick = () => {
  cardStudyMode = "type";
  btnModeType.classList.add("active");
  btnModeFlip.classList.remove("active");
  loadCard(currentIndex);
};''',
        '''const btnModeFlip = document.getElementById("btnModeFlip");
const btnModeType = document.getElementById("btnModeType");
const btnModeQuiz = document.getElementById("btnModeQuiz");
const btnModeDict = document.getElementById("btnModeDictation");

function setStudyModeUi(mode) {
  cardStudyMode = mode;
  btnModeFlip.classList.toggle("active", mode === "flip");
  btnModeType.classList.toggle("active", mode === "type");
  if (btnModeQuiz) btnModeQuiz.classList.toggle("active", mode === "quiz");
  if (btnModeDict) btnModeDict.classList.toggle("active", mode === "dictation");
  loadCard(currentIndex);
}
btnModeFlip.onclick = () => setStudyModeUi("flip");
btnModeType.onclick = () => setStudyModeUi("type");
if (btnModeQuiz) btnModeQuiz.onclick = () => setStudyModeUi("quiz");
if (btnModeDict) btnModeDict.onclick = () => setStudyModeUi("dictation");

const btnFifty = document.getElementById("btnUseFiftyFifty");
if (btnFifty) {
  btnFifty.onclick = () => {
    const p = loadProProfile();
    if (!p.powerups || (p.powerups.fiftyFifty || 0) <= 0) { alert("Nemáte Nápovědu 50:50 (lze koupit v Obchodě)."); return; }
    const isRev = document.getElementById("chkReverseStudy").checked;
    const correctAns = extractTargetAnswer(currentCard, isRev);
    const wrongBtns = Array.from(document.querySelectorAll("#quizArea .quiz-option")).filter(b => b.innerText !== correctAns && !b.disabled);
    if (wrongBtns.length < 2) return;
    p.powerups.fiftyFifty--; saveProProfile(p);
    wrongBtns.slice(0, 2).forEach(b => { b.disabled = true; b.style.opacity = "0.25"; });
    showProToast("Nápověda 50:50 aktivována!");
  };
}

const btnVoice = document.getElementById("btnVoiceInput");
if (btnVoice) {
  btnVoice.onclick = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert("Váš prohlížeč nepodporuje hlasové rozpoznávání."); return; }
    const rec = new SR();
    const selL = document.getElementById("selTtsLang");
    rec.lang = selL ? selL.value : "en-US";
    rec.interimResults = false;
    btnVoice.innerText = "Poslouchám...";
    rec.onresult = (ev) => {
      const txt = ev.results[0][0].transcript;
      document.getElementById("typeTextInput").value = txt;
      btnVoice.innerText = "Mikrofon";
      submitTypeAnswer();
    };
    rec.onerror = () => { btnVoice.innerText = "Mikrofon"; };
    rec.onend = () => { btnVoice.innerText = "Mikrofon"; };
    rec.start();
  };
}

const chkAutoTts = document.getElementById("chkAutoTts");
if (chkAutoTts) {
  chkAutoTts.checked = localStorage.getItem("karty_auto_tts") === "1";
  chkAutoTts.onchange = () => localStorage.setItem("karty_auto_tts", chkAutoTts.checked ? "1" : "0");
}

const btnEditCur = document.getElementById("btnEditCurrentCard");
if (btnEditCur) btnEditCur.onclick = () => { studyOptionsBar.classList.remove("open"); openCardEditor(); };
const btnMatchStudy = document.getElementById("btnOpenMatchFromStudy");
if (btnMatchStudy) btnMatchStudy.onclick = () => { studyOptionsBar.classList.remove("open"); openMatchingGame(currentDeck); };

const btnTypeHint = document.getElementById("btnTypeHint");
if (btnTypeHint) {
  btnTypeHint.onclick = () => {
    if (!currentCard) return;
    const isRev = document.getElementById("chkReverseStudy").checked;
    const ans = extractTargetAnswer(currentCard, isRev).split(/\\s*[;/]\\s*/)[0].trim();
    if (!ans) return;
    _hintRevealCount = Math.min(ans.length, _hintRevealCount + 1);
    let masked = "";
    for (let i = 0; i < ans.length; i++) masked += (i < _hintRevealCount || ans[i] === " ") ? ans[i] : "_";
    const hb = document.getElementById("typeHintDisplay");
    if (hb) { hb.innerText = masked; hb.style.display = "block"; }
  };
}
const selTtsLang = document.getElementById("selTtsLang");
if (selTtsLang) {
  const savedLang = localStorage.getItem("karty_tts_lang");
  if (savedLang) selTtsLang.value = savedLang;
  selTtsLang.onchange = () => localStorage.setItem("karty_tts_lang", selTtsLang.value);
}
const chkIgnoreDia = document.getElementById("chkIgnoreDiacritics");
if (chkIgnoreDia) {
  chkIgnoreDia.checked = localStorage.getItem("karty_ignore_dia") === "1";
  chkIgnoreDia.onchange = () => localStorage.setItem("karty_ignore_dia", chkIgnoreDia.checked ? "1" : "0");
}
const btnSpeakQ = document.getElementById("btnSpeakQuestion");
if (btnSpeakQ) {
  btnSpeakQ.onclick = () => {
    if (!("speechSynthesis" in window)) { alert("Váš prohlížeč nepodporuje čtení textu."); return; }
    const qEl = document.getElementById("cardQuestion");
    const aEl = document.getElementById("cardAnswer");
    const raw = (cardStudyMode === "dictation" || (isCardFlipped && aEl && aEl.innerText.trim()))
      ? (cardStudyMode === "dictation" ? extractTargetAnswer(currentCard, document.getElementById("chkReverseStudy").checked) : aEl.innerText.trim())
      : (qEl ? qEl.innerText.trim() : "");
    if (!raw) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(raw);
    u.lang = selTtsLang ? selTtsLang.value : "en-US";
    window.speechSynthesis.speak(u);
  };
}''',
    ),
    (
        '''        <div class="rating-grid" id="ratingGrid">
          <button class="btn-rate btn-rate-again" id="btnAgain" title="Klávesa 1">
            <span>Znovu (1)</span>
            <span class="interval" id="intAgain">&lt; 10m</span>
          </button>
          <button class="btn-rate btn-rate-hard" id="btnHard" title="Klávesa 2">
            <span>Těžké (2)</span>
            <span class="interval" id="intHard">1 d</span>
          </button>
          <button class="btn-rate btn-rate-good" id="btnGood" title="Klávesa 3">
            <span>Dobré (3)</span>
            <span class="interval" id="intGood">3 d</span>
          </button>
          <button class="btn-rate btn-rate-easy" id="btnEasy" title="Klávesa 4">
            <span>Snadné (4)</span>
            <span class="interval" id="intEasy">7 d</span>
          </button>
        </div>''',
        '''        <div class="rating-grid" id="ratingGrid">
          <button class="btn-rate btn-rate-again" id="btnAgain" title="Klávesa 1">
            <span>Znovu</span>
            <span class="interval" id="intAgain">&lt; 10m</span>
          </button>
          <button class="btn-rate btn-rate-hard" id="btnHard" title="Klávesa 2">
            <span>Těžké</span>
            <span class="interval" id="intHard">1 d</span>
          </button>
          <button class="btn-rate btn-rate-good" id="btnGood" title="Klávesa 3">
            <span>Dobré</span>
            <span class="interval" id="intGood">3 d</span>
          </button>
          <button class="btn-rate btn-rate-easy" id="btnEasy" title="Klávesa 4">
            <span>Snadné</span>
            <span class="interval" id="intEasy">7 d</span>
          </button>
        </div>''',
    ),
    (
        '''        <button class="btn btn-sm" id="btnExportProgress" title="Stáhnout lehký soubor .json s postupem učení pro přenos na jiné zařízení">Export postupu (.json)</button>
        <button class="btn btn-sm" id="btnImportProgress" title="Načíst a sloučit postup učení ze souboru .json">Import postupu (.json)</button>''',
        '''        <button class="btn btn-sm btn-primary" id="btnCloudSync" title="Synchronizovat postup s druhým zařízením jedním kliknutím">Synchronizovat</button>
        <button class="btn btn-sm" id="btnCloudSyncSetup" title="Nastavení synchronizace a odkaz pro telefon">Nastavit sync</button>
        <button class="btn btn-sm" id="btnExportProgress" title="Stáhnout lehký soubor .json s postupem učení pro přenos na jiné zařízení">Export postupu (.json)</button>
        <button class="btn btn-sm" id="btnImportProgress" title="Načíst a sloučit postup učení ze souboru .json">Import postupu (.json)</button>''',
    ),
    (
        '''<button class="btn-flip" id="btnFlip">Zobrazit odpověď (Mezerník / Klepnutí)</button>''',
        '''<button class="btn-flip" id="btnFlip">Zobrazit odpověď</button>''',
    ),
]

for idx, (tgt, repl) in enumerate(PRO_PATCHES):
    assert tgt in html, f"PRO_PATCH {idx} target not found!"
    html = html.replace(tgt, repl, 1)

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully generated pro/index.html ({len(html.encode('utf-8'))} bytes)")
