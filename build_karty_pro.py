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
  --radius: 12px;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.22);
}
body.theme-moss {
  --bg-main: #0c1211; --bg-card: #121a18; --bg-card-hover: #17211f; --bg-surface: #1b2624;
  --border-color: rgba(167, 210, 198, 0.1); --border-highlight: rgba(167, 210, 198, 0.22);
  --accent: #52b79a; --accent-hover: #3ea386; --accent-soft: rgba(82, 183, 154, 0.14);
  --text-main: #e3ece9; --text-muted: #849993;
}
body.theme-midnight {
  --bg-main: #0b101b; --bg-card: #111827; --bg-card-hover: #162033; --bg-surface: #1b273d;
  --border-color: rgba(147, 179, 230, 0.11); --border-highlight: rgba(147, 179, 230, 0.22);
  --accent: #6da3e8; --accent-hover: #538dd8; --accent-soft: rgba(109, 163, 232, 0.14);
  --text-main: #e2e9f4; --text-muted: #8293ad;
}
body.theme-amber {
  --bg-main: #13100d; --bg-card: #1b1612; --bg-card-hover: #221c17; --bg-surface: #29221c;
  --border-color: rgba(224, 184, 138, 0.11); --border-highlight: rgba(224, 184, 138, 0.22);
  --accent: #d49b5a; --accent-hover: #be8442; --accent-soft: rgba(212, 155, 90, 0.14);
  --text-main: #efe7de; --text-muted: #9e8f80;
}
body.theme-heather {
  --bg-main: #120e14; --bg-card: #19141c; --bg-card-hover: #211a25; --bg-surface: #271f2c;
  --border-color: rgba(196, 167, 210, 0.11); --border-highlight: rgba(196, 167, 210, 0.24);
  --accent: #a67db8; --accent-hover: #9167a3; --accent-soft: rgba(166, 125, 184, 0.14);
  --text-main: #ece5ef; --text-muted: #988b9e;
}
body.theme-lichen {
  --bg-main: #10120c; --bg-card: #171a12; --bg-card-hover: #1e2218; --bg-surface: #252a1d;
  --border-color: rgba(188, 201, 148, 0.11); --border-highlight: rgba(188, 201, 148, 0.24);
  --accent: #95a864; --accent-hover: #809350; --accent-soft: rgba(149, 168, 100, 0.14);
  --text-main: #e9ece2; --text-muted: #8f9682;
}
body.theme-mono {
  --bg-main: #0c0d0f; --bg-card: #131518; --bg-card-hover: #191c20; --bg-surface: #1f2328;
  --border-color: rgba(203, 213, 225, 0.1); --border-highlight: rgba(203, 213, 225, 0.2);
  --accent: #a8b5c4; --accent-hover: #c4ceda; --accent-soft: rgba(168, 181, 196, 0.14);
  --text-main: #e6eaef; --text-muted: #87919e;
}
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
.pro-pill.hearts { color: #e88d8d; border-color: rgba(232, 141, 141, 0.25); }
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

/* Mobile compact heatmap (7-day week bar) */
.pro-week-strip { display: none; }
@media (max-width: 640px) {
  header { flex-wrap: wrap; gap: 6px; padding: 8px 10px; }
  .pro-pill { padding: 2px 7px; font-size: 0.7rem; }
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
    <span class="pro-pill hearts" id="proHeartsPill" title="Životy (doplňují se časem nebo tréninkem)">Životy: 5/5</span>
    <span class="pro-pill level" id="proLevelPill" title="Vaše úroveň">Lv. 1</span>
    <span class="pro-pill streak" id="proStreakPill" title="Denní série">Série: 0 d</span>
    <span class="pro-pill points" id="proPointsPill" title="Body">0 b.</span>
    <span class="pro-pill boost" id="proBoostPill" style="display:none;">2x Boost</span>
    <button class="btn btn-sm" id="btnProSound" title="Zvukové efekty">Zvuk: Zap</button>
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
      <button class="btn btn-sm" id="btnProHeartPractice" style="display:none;">Trénink pro obnovení životů (+2)</button>
    </div>
"""

PRO_MODALS_HTML = r"""
<!-- PRO SHOP & MILESTONES MODAL -->
<div class="modal-overlay" id="shopModal">
  <div class="modal-content" style="max-width:520px; max-height:88dvh; overflow-y:auto;">
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
          <div class="shop-item-title">Doplnit životy (5/5)</div>
          <div class="shop-item-desc">Okamžitě obnoví všechny životy na maximum.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyHearts">Koupit (300 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Streak Freeze (max. 3)</div>
          <div class="shop-item-desc">Automaticky ochrání sérii, pokud některý den vynecháte.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyFreeze">Koupit (500 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">2x Body Boost (15 min)</div>
          <div class="shop-item-desc">Zdvojnásobí body ze všech karet po dobu 15 minut.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyBoost">Koupit (400 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Obnovení série (max. 3 dny zpět)</div>
          <div class="shop-item-desc">Zpětně zachrání nejbližší vynechaný den za poslední 3 dny.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyRepair">Koupit (800 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Tajemná truhla</div>
          <div class="shop-item-desc">Náhodná odměna: +200 až +700 bodů, Freeze nebo 2x Boost.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyMystery">Otevřít (450 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Balíček 3x Streak Freeze</div>
          <div class="shop-item-desc">Doplní zásobu Freeze na 3/3 se slevou.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyShieldPack">Koupit (1250 b.)</button>
      </div>
    </div>

    <h4 style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Vzhled aplikace (1500 b.)</h4>
    <div class="shop-grid" id="shopThemesList" style="margin-bottom:14px;"></div>

    <h4 style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Nastavitelné milníky série</h4>
    <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:10px;" id="shopMilestonesList"></div>
    <div style="display:grid; grid-template-columns:70px 1fr 74px auto; gap:6px; align-items:center;">
      <input type="number" id="inpNewMsDays" min="1" max="3650" value="50" style="background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:6px 8px; border-radius:6px; font-size:0.82rem;">
      <input type="text" id="inpNewMsReward" placeholder="Odměna (např. Volný večer)" style="background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:6px 8px; border-radius:6px; font-size:0.82rem;">
      <input type="number" id="inpNewMsBonus" min="0" max="10000" value="250" style="background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); padding:6px 8px; border-radius:6px; font-size:0.82rem;">
      <button class="btn btn-sm btn-primary" id="btnAddMilestone">Přidat</button>
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

<div class="pro-toast" id="proToast"></div>
"""

PRO_JS = r"""
// --- KARTY PRO DUOLINGO ENGINE ---
const PRO_STORAGE_KEY = "karty_pro_profile_v1";
const PRO_THEMES = [
  { id: "default", name: "Lesní houbař (výchozí)", cost: 0 },
  { id: "moss", name: "Hluboký mech", cost: 1500 },
  { id: "lichen", name: "Kůra a lišejník", cost: 1500 },
  { id: "amber", name: "Teplý jantar", cost: 1500 },
  { id: "midnight", name: "Půlnoční modř", cost: 1500 },
  { id: "heather", name: "Vřesoviště", cost: 1500 },
  { id: "mono", name: "Břidlicový monochrom", cost: 1500 }
];

function getDefaultProProfile() {
  return {
    points: 0,
    xp: 0,
    hearts: 5,
    lastHeartRegen: Date.now(),
    freezes: 1,
    frozenDates: [],
    dailyGoal: 20,
    lessonLength: 12,
    boostUntil: 0,
    unlockedThemes: ["default"],
    activeTheme: "default",
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
    const prof = {
      ...def,
      ...parsed,
      frozenDates: Array.isArray(parsed.frozenDates) ? parsed.frozenDates : [],
      unlockedThemes: Array.isArray(parsed.unlockedThemes) ? parsed.unlockedThemes : ["default"],
      milestones: Array.isArray(parsed.milestones) && parsed.milestones.length > 0 ? parsed.milestones : def.milestones,
      dailyBonusDates: Array.isArray(parsed.dailyBonusDates) ? parsed.dailyBonusDates : []
    };
    // Regen +1 heart every 30 min
    if (prof.hearts < 5) {
      const elapsed = Date.now() - (prof.lastHeartRegen || Date.now());
      const gained = Math.floor(elapsed / (30 * 60 * 1000));
      if (gained > 0) {
        prof.hearts = Math.min(5, prof.hearts + gained);
        prof.lastHeartRegen = Date.now();
        localStorage.setItem(PRO_STORAGE_KEY, JSON.stringify(prof));
      }
    } else {
      prof.lastHeartRegen = Date.now();
    }
    return prof;
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
  document.body.classList.remove("theme-moss", "theme-midnight", "theme-amber", "theme-heather", "theme-lichen", "theme-mono");
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
let _lessonStats = { reviewed: 0, mistakes: 0, xp: 0, isHeartTraining: false };

function _hashDateSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

function getDailyQuestsState(prof, todayCount) {
  const todayStr = getLocalDateString();
  if (!prof.dailyQuests || prof.dailyQuests.date !== todayStr) {
    prof.dailyQuests = {
      date: todayStr, maxCombo: 0, cleanCount: 0, easyCount: 0, goodCount: 0, hardCount: 0, typeCount: 0, xpToday: 0,
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
    { id: "q_combo4", title: "Dosáhni Combo 4x", cur: dq.maxCombo || 0, target: 4, reward: 30 },
    { id: "q_combo8", title: "Dosáhni Combo 8x", cur: dq.maxCombo || 0, target: 8, reward: 55 },
    { id: "q_combo12", title: "Dosáhni Combo 12x", cur: dq.maxCombo || 0, target: 12, reward: 80 },
    { id: "q_clean10", title: "10 karet bez tlačítka Znovu", cur: dq.cleanCount || 0, target: 10, reward: 45 },
    { id: "q_clean20", title: "20 karet bez tlačítka Znovu", cur: dq.cleanCount || 0, target: 20, reward: 75 },
    { id: "q_easy5", title: "Ohodnoť 5 karet jako Snadné", cur: dq.easyCount || 0, target: 5, reward: 35 },
    { id: "q_good12", title: "Ohodnoť 12 karet jako Dobré", cur: dq.goodCount || 0, target: 12, reward: 40 },
    { id: "q_hard4", title: "Ohodnoť 4 karty jako Těžké", cur: dq.hardCount || 0, target: 4, reward: 35 },
    { id: "q_type5", title: "5 karet ve vepisovacím režimu", cur: dq.typeCount || 0, target: 5, reward: 45 },
    { id: "q_type10", title: "10 karet ve vepisovacím režimu", cur: dq.typeCount || 0, target: 10, reward: 65 },
    { id: "q_xp120", title: "Nasbírej dnes 120 XP", cur: dq.xpToday || 0, target: 120, reward: 50 },
    { id: "q_xp250", title: "Nasbírej dnes 250 XP", cur: dq.xpToday || 0, target: 250, reward: 85 }
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
  const elHearts = document.getElementById("proHeartsPill");
  const elLevel = document.getElementById("proLevelPill");
  const elStreak = document.getElementById("proStreakPill");
  const elPoints = document.getElementById("proPointsPill");
  const elBoost = document.getElementById("proBoostPill");
  const elSound = document.getElementById("btnProSound");
  const elHeartBtn = document.getElementById("btnProHeartPractice");
  if (elHearts) elHearts.innerText = `Životy: ${prof.hearts}/5`;
  if (elLevel) elLevel.innerText = `Lv. ${lv.level}`;
  if (elStreak) elStreak.innerText = `Série: ${streak} d`;
  if (elPoints) elPoints.innerText = `${prof.points} b.`;
  if (elBoost) elBoost.style.display = (prof.boostUntil > Date.now()) ? "inline-flex" : "none";
  if (elSound) elSound.innerText = prof.soundEnabled === false ? "Zvuk: Vyp" : "Zvuk: Zap";
  if (elHeartBtn) elHeartBtn.style.display = prof.hearts < 5 ? "inline-flex" : "none";

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

// Wrap startStudy for Hearts check, Lesson slicing (10-15 cards), and Lesson stats
const _origStartStudyPro = startStudy;
startStudy = async function(deckId, quickMode = false, subdeckFilter = null, keepExtra = false, sliceRange = null) {
  const prof = loadProProfile();
  if (!quickMode && !_lessonStats.isHeartTraining && prof.hearts <= 0) {
    if (confirm("Došly vám životy (0/5)! Chcete spustit krátký trénink pro obnovení +2 životů? (Nebo si je můžete doplnit v Obchodě.)")) {
      _lessonStats = { reviewed: 0, mistakes: 0, xp: 0, isHeartTraining: true };
      await _origStartStudyPro(deckId, true, subdeckFilter, keepExtra);
      if (studyQueue.length > 5) studyQueue = studyQueue.slice(0, 5);
      return;
    }
    return;
  }
  _lessonStartMs = Date.now();
  if (!_lessonStats.isHeartTraining) {
    _lessonStats = { reviewed: 0, mistakes: 0, xp: 0, isHeartTraining: false };
  }
  await _origStartStudyPro(deckId, quickMode, subdeckFilter, keepExtra);
  if (sliceRange && Array.isArray(sliceRange)) {
    const [sStart, sEnd] = sliceRange;
    const sliced = currentDeck.cards.slice(sStart, sEnd);
    if (sliced.length > 0) {
      studyQueue = sliced;
      currentIndex = 0;
      loadCard(0);
    }
  } else if (!quickMode && !_lessonStats.isHeartTraining && prof.lessonLength > 0 && studyQueue.length > prof.lessonLength) {
    studyQueue = studyQueue.slice(0, prof.lessonLength);
    sessionStats.newCount = studyQueue.filter(c => !getCardSrsObj(c).due || getCardSrsObj(c).due === 0).length;
    sessionStats.dueCount = studyQueue.length - sessionStats.newCount;
    loadCard(0);
  }
};

// Wrap rateCard for Hearts, >=1 day scoring, Quests, Mascot, and Repair Round
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
    sessionCombo = 0;
    _lessonStats.mistakes++;
    prof.dailyQuests.cleanCount = 0;
    if (!_lessonStats.isHeartTraining && prof.hearts > 0) {
      prof.hearts--;
      prof.lastHeartRegen = Date.now();
    }
    playProTone("again");
    setMascotState("encourage", "Nevadí, opravíme na konci lekce!");
    const comboEl = document.getElementById("proComboBadge");
    if (comboEl) { comboEl.style.display = "none"; comboEl.classList.remove("hot"); }
    saveProProfile(prof);
    showProToast("Chyba (-1 život). Karta se vrátí v opravném kole.");
    await updateProHud();
    return;
  }

  if (ratingKey === "good" || ratingKey === "easy") {
    sessionCombo++;
    prof.dailyQuests.maxCombo = Math.max(prof.dailyQuests.maxCombo || 0, sessionCombo);
    setMascotState("happy", sessionCombo >= 4 ? `Skvělá série ${sessionCombo}x!` : "Výborně!");
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

// Wrap showFinishedView for Lesson Summary + Heart Training Reward
const _origShowFinishedPro = showFinishedView;
showFinishedView = function() {
  _origShowFinishedPro();
  const prof = loadProProfile();
  if (_lessonStats.isHeartTraining) {
    prof.hearts = Math.min(5, prof.hearts + 2);
    _lessonStats.isHeartTraining = false;
    saveProProfile(prof);
    updateProHud();
    showProToast("Trénink dokončen! +2 životy obnoveny.");
  }
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
    btn.innerText = c.title || extractTargetAnswer(c, true) || "Pojem";
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
    btn.innerText = extractTargetAnswer(c, false);
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

// Mobile Swipe Gestures (left = Again, right = Easy)
(function bindSwipeGestures() {
  const box = document.getElementById("flashcardBox");
  if (!box) return;
  let startX = 0, startY = 0;
  box.addEventListener("touchstart", (e) => {
    if (e.touches.length !== 1) return;
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
  }, { passive: true });
  box.addEventListener("touchend", (e) => {
    if (!isCardFlipped || e.changedTouches.length !== 1) return;
    const dx = e.changedTouches[0].clientX - startX;
    const dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) > 90 && Math.abs(dx) > Math.abs(dy) * 1.8) {
      if (dx < 0) rateCard("again");
      else rateCard("easy");
    }
  }, { passive: true });
})();

// Heart Recovery Button
document.getElementById("btnProHeartPractice").onclick = async () => {
  const decks = await dbGetAllDecks();
  if (!decks || decks.length === 0) { alert("Nemáte žádný balíček."); return; }
  _lessonStats = { reviewed: 0, mistakes: 0, xp: 0, isHeartTraining: true };
  await _origStartStudyPro(decks[0].id, true, null, false);
  if (studyQueue.length > 5) studyQueue = studyQueue.slice(0, 5);
  loadCard(0);
};

// Shop & Sound Modal Listeners
async function renderShopModal() {
  const { prof, streak } = await computeProStreakAndFreeze();
  document.getElementById("shopBalanceVal").innerText = `${prof.points} b.`;
  document.getElementById("selProDailyGoal").value = String(prof.dailyGoal || 20);
  document.getElementById("selProLessonLen").value = String(prof.lessonLength ?? 12);

  const themesBox = document.getElementById("shopThemesList");
  themesBox.innerHTML = "";
  PRO_THEMES.forEach(th => {
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
        <button class="btn btn-sm ${isActive ? "" : "btn-primary"} btn-buy-theme">${isActive ? "Aktivní" : (unlocked ? "Použít" : `Koupit (${th.cost} b.)`)}</button>
      </div>
    `;
    const prevBtn = row.querySelector(".btn-preview-theme");
    if (prevBtn) prevBtn.onclick = () => { applyProTheme(th.id); showProToast(`Náhled motivu: ${th.name}`); };
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

document.getElementById("btnProSound").onclick = async () => {
  const p = loadProProfile(); p.soundEnabled = (p.soundEnabled === false); saveProProfile(p);
  if (p.soundEnabled) playProTone("good"); await updateProHud();
};
document.getElementById("btnOpenShop").onclick = async () => { await renderShopModal(); document.getElementById("shopModal").classList.add("active"); };
document.getElementById("shopModalClose").onclick = () => { applyProTheme(loadProProfile().activeTheme); document.getElementById("shopModal").classList.remove("active"); };
document.getElementById("shopModal").addEventListener("click", (e) => {
  if (e.target.id === "shopModal") { applyProTheme(loadProProfile().activeTheme); document.getElementById("shopModal").classList.remove("active"); }
});
document.getElementById("selProDailyGoal").onchange = async (e) => { const p = loadProProfile(); p.dailyGoal = parseInt(e.target.value, 10) || 20; saveProProfile(p); await updateProHud(); };
document.getElementById("selProLessonLen").onchange = async (e) => { const p = loadProProfile(); p.lessonLength = parseInt(e.target.value, 10); saveProProfile(p); };
document.getElementById("btnBuyHearts").onclick = async () => {
  const p = loadProProfile(); if (p.hearts >= 5) { alert("Životy už máte plné (5/5)."); return; }
  if (p.points < 300) { alert("Potřebujete alespoň 300 bodů."); return; }
  p.points -= 300; p.hearts = 5; saveProProfile(p); showProToast("Životy doplněny na 5/5!"); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyFreeze").onclick = async () => {
  const p = loadProProfile(); if (p.freezes >= 3) { alert("Máte již plnou zásobu (3/3)."); return; }
  if (p.points < 500) { alert("Potřebujete alespoň 500 bodů."); return; }
  p.points -= 500; p.freezes++; saveProProfile(p); showProToast("Zakoupen Streak Freeze!"); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyBoost").onclick = async () => {
  const p = loadProProfile(); if (p.points < 400) { alert("Potřebujete alespoň 400 bodů."); return; }
  p.points -= 400; p.boostUntil = Date.now() + 15 * 60 * 1000; saveProProfile(p); showProToast("Aktivován 2x Body Boost na 15 min!"); await updateProHud(); await renderShopModal();
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
  if (p.points < 800) { alert("Potřebujete alespoň 800 bodů."); return; }
  p.points -= 800; p.frozenDates.push(targetDay); saveProProfile(p); showProToast(`Série opravena pro den ${targetDay}!`); await renderHeatmap(); await renderShopModal();
};
document.getElementById("btnBuyMystery").onclick = async () => {
  const p = loadProProfile(); if (p.points < 450) { alert("Potřebujete alespoň 450 bodů."); return; }
  p.points -= 450;
  const roll = Math.random();
  let msg = "";
  if (roll < 0.25 && p.freezes < 3) { p.freezes++; msg = "Tajemná truhla: 1x Streak Freeze!"; }
  else if (roll < 0.5) { p.boostUntil = Date.now() + 15 * 60 * 1000; msg = "Tajemná truhla: 2x Body Boost!"; }
  else { const w = [200, 350, 500, 700][Math.floor(Math.random() * 4)]; p.points += w; msg = `Tajemná truhla: +${w} bodů!`; }
  saveProProfile(p); launchConfetti(); playProTone("level"); showProToast(msg); await updateProHud(); await renderShopModal();
};
document.getElementById("btnBuyShieldPack").onclick = async () => {
  const p = loadProProfile(); if (p.freezes >= 3) { alert("Zásobu Freeze už máte plnou (3/3)."); return; }
  if (p.points < 1250) { alert("Potřebujete alespoň 1250 bodů."); return; }
  p.points -= 1250; p.freezes = 3; saveProProfile(p); showProToast("Zásoba Streak Freeze doplněna na 3/3!"); await updateProHud(); await renderShopModal();
};
document.getElementById("btnAddMilestone").onclick = async () => {
  const days = parseInt(document.getElementById("inpNewMsDays").value, 10);
  const title = document.getElementById("inpNewMsReward").value.trim() || `Milník ${days} dní`;
  const bonus = Math.max(0, parseInt(document.getElementById("inpNewMsBonus").value, 10) || 0);
  if (!days || days < 1) { alert("Zadejte platný počet dní."); return; }
  const p = loadProProfile();
  p.milestones.push({ id: "m_" + Date.now(), days, title, bonusPoints: bonus, claimed: false });
  saveProProfile(p); document.getElementById("inpNewMsReward").value = ""; await renderShopModal();
};

window.addEventListener("DOMContentLoaded", () => {
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
        '''        <div class="mode-toggle-group" style="width:100%; display:grid; grid-template-columns:1fr 1fr 1fr;">
          <button class="btn-mode-tgl active" id="btnModeFlip" title="Režim otáčení karty">Otáčecí</button>
          <button class="btn-mode-tgl" id="btnModeType" title="Režim vepisování z klávesnice">Vepisovací</button>
          <button class="btn-mode-tgl" id="btnModeQuiz" title="Kvízový výběr ze 4 možností">Výběr ze 4</button>
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
              <button class="btn btn-sm" id="btnTypeHint" style="padding:0 12px;" title="Odhalit další písmeno">Nápověda</button>
              <button class="btn btn-primary" id="btnCheckType" style="padding:0 20px;">Ověřit</button>
            </div>
            <div class="type-hint-box" id="typeHintDisplay" style="display:none;"></div>
            <div class="type-diff-display" id="typeDiffDisplay" style="display:none;">
              <!-- Character diff result -->
            </div>
          </div>

          <!-- QUIZ 4-CHOICE AREA -->
          <div class="quiz-grid" id="quizArea" style="display:none;"></div>''',
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
        const p = loadProProfile();
        if (p.hearts > 0) { p.hearts--; saveProProfile(p); updateProHud(); }
        showProToast("Špatná volba (-1 život)");
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
  const quizArea = document.getElementById("quizArea");
  if (hintBox) { hintBox.style.display = "none"; hintBox.innerText = ""; }
  if (cardStudyMode === "type") {
    typeArea.style.display = "flex";
    if (quizArea) quizArea.style.display = "none";
    typeInput.value = "";
    typeDiff.style.display = "none";
    typeDiff.innerHTML = "";
    btnFlip.style.display = "none";
    setTimeout(() => typeInput.focus(), 50);
  } else if (cardStudyMode === "quiz") {
    typeArea.style.display = "none";
    if (quizArea) { quizArea.style.display = "grid"; renderQuizOptions(currentCard, isReverse); }
    btnFlip.style.display = "none";
  } else {
    typeArea.style.display = "none";
    if (quizArea) quizArea.style.display = "none";
    btnFlip.style.display = "block";
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

function setStudyModeUi(mode) {
  cardStudyMode = mode;
  btnModeFlip.classList.toggle("active", mode === "flip");
  btnModeType.classList.toggle("active", mode === "type");
  if (btnModeQuiz) btnModeQuiz.classList.toggle("active", mode === "quiz");
  loadCard(currentIndex);
}
btnModeFlip.onclick = () => setStudyModeUi("flip");
btnModeType.onclick = () => setStudyModeUi("type");
if (btnModeQuiz) btnModeQuiz.onclick = () => setStudyModeUi("quiz");

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
    const raw = (isCardFlipped && aEl && aEl.innerText.trim()) ? aEl.innerText.trim() : (qEl ? qEl.innerText.trim() : "");
    if (!raw) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(raw);
    u.lang = selTtsLang ? selTtsLang.value : "en-US";
    window.speechSynthesis.speak(u);
  };
}''',
    ),
]

for idx, (tgt, repl) in enumerate(PRO_PATCHES):
    assert tgt in html, f"PRO_PATCH {idx} target not found!"
    html = html.replace(tgt, repl, 1)

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully generated pro/index.html ({len(html.encode('utf-8'))} bytes)")
