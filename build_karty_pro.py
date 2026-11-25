# -*- coding: utf-8 -*-
"""
Generates the private gamified version (pro/index.html) from Karty.html
without modifying the public Karty.html / index.html.
Adds Duolingo-style streak, automatic Streak Freeze, XP/points,
configurable streak milestones with rewards, shop, and unlockable themes.
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

# Update title
html = html.replace(
    "<title>Karty – Chytrý přehrávač kartiček</title>",
    "<title>Karty Pro – Studijní aréna</title>",
)

PRO_CSS = r"""
/* --- KARTY PRO MINIMALIST THEME & GAMIFICATION --- */
:root {
  --bg-main: #0d1015;
  --bg-card: #151a22;
  --bg-card-hover: #1b222c;
  --bg-surface: #1e2530;
  --border-color: #28313e;
  --border-highlight: #3b4758;
  --accent: #10b981;
  --accent-hover: #059669;
  --text-main: #f1f5f9;
  --text-muted: #94a3b8;
}
body.theme-midnight {
  --bg-main: #090e1a;
  --bg-card: #10182b;
  --bg-card-hover: #16213a;
  --bg-surface: #1a2642;
  --border-color: #243459;
  --border-highlight: #3b538a;
  --accent: #38bdf8;
  --accent-hover: #0284c7;
}
body.theme-amber {
  --bg-main: #120f0c;
  --bg-card: #1b1611;
  --bg-card-hover: #241d16;
  --bg-surface: #2a2219;
  --border-color: #3d3124;
  --border-highlight: #614d37;
  --accent: #f59e0b;
  --accent-hover: #d97706;
}
body.theme-mono {
  --bg-main: #09090b;
  --bg-card: #141417;
  --bg-card-hover: #1e1e22;
  --bg-surface: #222227;
  --border-color: #323238;
  --border-highlight: #52525b;
  --accent: #e4e4e7;
  --accent-hover: #ffffff;
}
header {
  background: rgba(13, 16, 21, 0.92);
  padding: 10px 14px;
}
.heatmap-container {
  background: var(--bg-card);
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
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-main);
  white-space: nowrap;
}
.pro-pill.streak { border-color: rgba(245, 158, 11, 0.45); color: #fbbf24; background: rgba(245, 158, 11, 0.1); }
.pro-pill.points { border-color: rgba(16, 185, 129, 0.45); color: #34d399; background: rgba(16, 185, 129, 0.1); }
.pro-pill.freeze { border-color: rgba(56, 189, 248, 0.45); color: #38bdf8; background: rgba(56, 189, 248, 0.1); }
.pro-pill.boost { border-color: rgba(168, 85, 247, 0.55); color: #c084fc; background: rgba(168, 85, 247, 0.12); }
.pro-pill.level { border-color: rgba(250, 204, 21, 0.45); color: #fde047; background: rgba(250, 204, 21, 0.1); }

/* Minimalist tactile 3D buttons */
.btn-primary, .btn-flip {
  border-bottom: 3px solid rgba(0, 0, 0, 0.35) !important;
  transition: transform 0.08s ease, filter 0.12s ease !important;
}
.btn-primary:active, .btn-flip:active {
  transform: translateY(2px);
  border-bottom-width: 1px !important;
}
.btn-rate {
  border-bottom-width: 3px !important;
  transition: transform 0.08s ease, background 0.12s ease !important;
}
.btn-rate:active {
  transform: translateY(2px);
  border-bottom-width: 1px !important;
}

/* Pro Dashboard Card */
.pro-dashboard {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 12px 14px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22);
}
.pro-dash-block {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.pro-dash-top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.82rem;
  font-weight: 700;
}
.pro-bar-track {
  width: 100%;
  height: 9px;
  background: rgba(0, 0, 0, 0.35);
  border-radius: 999px;
  overflow: hidden;
}
.pro-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.pro-bar-xp { background: linear-gradient(90deg, #eab308, #fde047); }
.pro-bar-goal { background: linear-gradient(90deg, #059669, #34d399); }

.pro-quests-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}
.pro-quest-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.78rem;
}
.pro-quest-card.done {
  border-color: rgba(16, 185, 129, 0.55);
  background: rgba(16, 185, 129, 0.08);
}

.pro-combo-badge {
  display: none;
  align-items: center;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 0.74rem;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(90deg, #f97316, #eab308);
  animation: popIn 0.2s ease;
}
@keyframes popIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.pro-confetti-piece {
  position: fixed;
  width: 8px;
  height: 8px;
  top: -12px;
  z-index: 500;
  pointer-events: none;
  border-radius: 2px;
  animation: confettiFall 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}
@keyframes confettiFall {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(540deg); opacity: 0; }
}
.hm-cell.frozen {
  background: #38bdf8 !important;
  box-shadow: 0 0 4px rgba(56, 189, 248, 0.55);
}
.pro-toast {
  position: fixed;
  bottom: 84px;
  left: 50%;
  transform: translateX(-50%) translateY(16px);
  background: var(--bg-surface);
  border: 1px solid var(--accent);
  color: var(--text-main);
  padding: 8px 15px;
  border-radius: 999px;
  font-size: 0.84rem;
  font-weight: 700;
  z-index: 300;
  opacity: 0;
  pointer-events: none;
  transition: all 0.25s ease;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
  white-space: nowrap;
}
.pro-toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
.shop-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.shop-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 9px 12px;
}
.shop-item-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.shop-item-title {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--text-main);
}
.shop-item-desc {
  font-size: 0.76rem;
  color: var(--text-muted);
}
.milestone-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 7px 10px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.22);
  border: 1px solid var(--border-color);
  font-size: 0.82rem;
}
.milestone-row.claimed {
  border-color: rgba(16, 185, 129, 0.5);
  background: rgba(16, 185, 129, 0.08);
}
@media (max-width: 768px) {
  header {
    flex-wrap: wrap;
    gap: 6px;
    padding: 8px 10px;
  }
  .pro-pill {
    padding: 2px 7px;
    font-size: 0.71rem;
  }
  .pro-dashboard {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 10px 12px;
  }
  .pro-quests-strip {
    grid-template-columns: 1fr;
    gap: 6px;
  }
}
"""

PRO_HEADER_HUD = r"""  <div class="pro-hud" id="proHud">
    <span class="pro-pill level" id="proLevelPill" title="Vaše úroveň a hodnost">Lv. 1</span>
    <span class="pro-pill streak" id="proStreakPill" title="Aktuální denní série">Série: 0 d</span>
    <span class="pro-pill points" id="proPointsPill" title="Nasbírané body">Body: 0</span>
    <span class="pro-pill freeze" id="proFreezePill" title="Zásoba Streak Freeze">Freeze: 0/3</span>
    <span class="pro-pill boost" id="proBoostPill" style="display:none;">2x Boost</span>
    <button class="btn btn-sm" id="btnProSound" title="Zapnout/vypnout zvukové efekty">Zvuk: Zap</button>
    <button class="btn btn-sm btn-primary" id="btnOpenShop">Obchod</button>
  </div>"""

PRO_DASHBOARD_HTML = r"""
    <div class="pro-dashboard" id="proDashboard">
      <div class="pro-dash-block">
        <div class="pro-dash-top">
          <span id="proDashRank" style="color:#fde047;">Úroveň 1 – Začátečník</span>
          <span id="proDashXpText" style="color:var(--text-muted); font-size:0.78rem;">0 / 45 XP</span>
        </div>
        <div class="pro-bar-track"><div class="pro-bar-fill pro-bar-xp" id="proDashXpBar" style="width:0%;"></div></div>
      </div>
      <div class="pro-dash-block">
        <div class="pro-dash-top">
          <span style="color:#34d399;">Dnešní cíl (min. 1 den)</span>
          <span id="proDashGoalText" style="color:var(--text-muted); font-size:0.78rem;">0 / 20 karet</span>
        </div>
        <div class="pro-bar-track"><div class="pro-bar-fill pro-bar-goal" id="proDashGoalBar" style="width:0%;"></div></div>
      </div>
    </div>
    <div class="pro-quests-strip" id="proQuestsStrip"></div>
"""

PRO_MODAL_HTML = r"""
<!-- PRO SHOP & MILESTONES MODAL -->
<div class="modal-overlay" id="shopModal">
  <div class="modal-content" style="max-width:520px; max-height:88dvh; overflow-y:auto;">
    <div class="modal-header">
      <div class="modal-title">Obchod, série a milníky</div>
      <button class="modal-close" id="shopModalClose">&times;</button>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; padding:10px 12px; background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); margin-bottom:12px; flex-wrap:wrap;">
      <div>
        <div style="font-size:0.82rem; color:var(--text-muted);">Dostupné body</div>
        <div id="shopBalanceVal" style="font-size:1.3rem; font-weight:800; color:#4ade80;">0</div>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <label for="selProDailyGoal" style="font-size:0.84rem; color:var(--text-muted);">Denní cíl (karet):</label>
        <select id="selProDailyGoal" class="select-sm">
          <option value="10">10 / den</option>
          <option value="20">20 / den</option>
          <option value="30">30 / den</option>
          <option value="50">50 / den</option>
          <option value="100">100 / den</option>
        </select>
      </div>
    </div>

    <h4 style="font-size:0.9rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Vylepšení</h4>
    <div class="shop-grid" style="margin-bottom:16px;">
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Streak Freeze (max. 3)</div>
          <div class="shop-item-desc">Automaticky ochrání vaši sérii, pokud některý den vynecháte.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyFreeze">Koupit (150 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">2x Body Boost (15 min)</div>
          <div class="shop-item-desc">Zdvojnásobí získané body za všechny karty v příštích 15 minutách.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyBoost">Koupit (100 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Oprava včerejší série</div>
          <div class="shop-item-desc">Zpětně doplní včerejší vynechaný den jako zmrazený, pokud jste neměli Freeze.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyRepair">Koupit (400 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Tajemná truhla</div>
          <div class="shop-item-desc">Náhodná odměna: +50 až +250 bodů, Streak Freeze zdarma nebo 2x Boost.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyMystery">Otevřít (120 b.)</button>
      </div>
      <div class="shop-item">
        <div class="shop-item-info">
          <div class="shop-item-title">Balíček 3x Streak Freeze</div>
          <div class="shop-item-desc">Doplní zásobu Freeze na maximum (3/3) se slevou.</div>
        </div>
        <button class="btn btn-sm btn-primary" id="btnBuyShieldPack">Koupit (380 b.)</button>
      </div>
    </div>

    <h4 style="font-size:0.9rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Vzhled aplikace</h4>
    <div class="shop-grid" id="shopThemesList" style="margin-bottom:16px;"></div>

    <h4 style="font-size:0.9rem; color:var(--text-muted); margin-bottom:8px; text-transform:uppercase;">Nastavitelné milníky série</h4>
    <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:10px;" id="shopMilestonesList"></div>
    <div style="display:grid; grid-template-columns:76px 1fr 78px auto; gap:6px; align-items:center; margin-top:6px;">
      <input type="number" id="inpNewMsDays" min="1" max="3650" placeholder="Dní" value="50" style="background:#09090b; border:1px solid #3f3f46; color:#fff; padding:6px 8px; border-radius:6px; font-size:0.84rem;">
      <input type="text" id="inpNewMsReward" placeholder="Odměna (např. Pizza / Volno)" style="background:#09090b; border:1px solid #3f3f46; color:#fff; padding:6px 8px; border-radius:6px; font-size:0.84rem;">
      <input type="number" id="inpNewMsBonus" min="0" max="10000" placeholder="Body" value="250" style="background:#09090b; border:1px solid #3f3f46; color:#fff; padding:6px 8px; border-radius:6px; font-size:0.84rem;">
      <button class="btn btn-sm btn-primary" id="btnAddMilestone">Přidat</button>
    </div>
  </div>
</div>
<div class="pro-toast" id="proToast"></div>
"""

PRO_JS = r"""
// --- KARTY PRO GAMIFICATION ENGINE ---
const PRO_STORAGE_KEY = "karty_pro_profile_v1";
const PRO_THEMES = [
  { id: "default", name: "Nordická břidlice (výchozí)", cost: 0 },
  { id: "midnight", name: "Půlnoční modř", cost: 200 },
  { id: "amber", name: "Teplý jantar", cost: 250 },
  { id: "mono", name: "Čistý monochrom", cost: 300 }
];

function getDefaultProProfile() {
  return {
    points: 0,
    freezes: 1,
    frozenDates: [],
    dailyGoal: 20,
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

function applyProTheme(themeId) {
  document.body.classList.remove("theme-midnight", "theme-amber", "theme-mono");
  if (themeId && themeId !== "default") {
    document.body.classList.add("theme-" + themeId);
  }
}

function addDaysToDateStr(dateStr, deltaDays) {
  const [y, m, d] = dateStr.split("-").map(Number);
  const dt = new Date(y, m - 1, d + deltaDays);
  return getLocalDateString(dt);
}

async function computeProStreakAndFreeze() {
  const prof = loadProProfile();
  const reviews = await dbGetAllReviews();
  const todayStr = getLocalDateString();
  const countsByDate = new Map();
  reviews.forEach(r => {
    if (r && r.dateStr) countsByDate.set(r.dateStr, (countsByDate.get(r.dateStr) || 0) + 1);
  });

  const activeSet = new Set();
  const graduatedByDate = new Map();
  reviews.forEach(r => {
    if (r && r.dateStr && (r.interval || 0) >= 1) {
      graduatedByDate.set(r.dateStr, (graduatedByDate.get(r.dateStr) || 0) + 1);
      activeSet.add(r.dateStr);
    }
  });
  const frozenSet = new Set(prof.frozenDates);

  // Auto-consume Streak Freeze for missed days between last active/frozen day and yesterday
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
  if (!activeSet.has(checkStr) && !frozenSet.has(checkStr)) {
    checkStr = addDaysToDateStr(todayStr, -1);
  }
  let guard = 0;
  while ((activeSet.has(checkStr) || frozenSet.has(checkStr)) && guard < 3650) {
    streak++;
    checkStr = addDaysToDateStr(checkStr, -1);
    guard++;
  }

  // Check milestones
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
  return { prof, streak, todayCount, frozenSet };
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
  const colors = ["#22c55e", "#fde047", "#38bdf8", "#f97316", "#c084fc"];
  for (let i = 0; i < 36; i++) {
    const p = document.createElement("div");
    p.className = "pro-confetti-piece";
    p.style.left = Math.random() * 100 + "vw";
    p.style.background = colors[i % colors.length];
    p.style.animationDelay = (Math.random() * 0.35) + "s";
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 2100);
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
    if (kind === "good") {
      playNote(523.25, 0, 0.11);
      playNote(659.25, 0.08, 0.16);
    } else if (kind === "level") {
      playNote(523.25, 0, 0.12);
      playNote(659.25, 0.09, 0.12);
      playNote(783.99, 0.18, 0.14);
      playNote(1046.5, 0.28, 0.28);
    } else if (kind === "again") {
      playNote(310, 0, 0.14);
    }
  } catch (e) {}
}

let sessionCombo = 0;

async function updateProHud() {
  const { prof, streak, todayCount } = await computeProStreakAndFreeze();
  applyProTheme(prof.activeTheme);
  const lv = getLevelInfo(prof.xp ?? prof.points);
  const elLevel = document.getElementById("proLevelPill");
  const elStreak = document.getElementById("proStreakPill");
  const elPoints = document.getElementById("proPointsPill");
  const elFreeze = document.getElementById("proFreezePill");
  const elBoost = document.getElementById("proBoostPill");
  const elSound = document.getElementById("btnProSound");
  if (elLevel) elLevel.innerText = `Lv. ${lv.level}`;
  if (elStreak) elStreak.innerText = `Série: ${streak} d`;
  if (elPoints) elPoints.innerText = `Body: ${prof.points}`;
  if (elFreeze) elFreeze.innerText = `Freeze: ${prof.freezes}/3`;
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
  if (elGoalTxt) elGoalTxt.innerText = todayCount >= prof.dailyGoal ? `Splněno (${todayCount}/${prof.dailyGoal})` : `${todayCount} / ${prof.dailyGoal} karet`;
  if (elGoalBar) elGoalBar.style.width = `${goalPct}%`;
  renderDailyQuests(prof, todayCount);
}

function getDailyQuestsState(prof, todayCount) {
  const todayStr = getLocalDateString();
  if (!prof.dailyQuests || prof.dailyQuests.date !== todayStr) {
    prof.dailyQuests = { date: todayStr, maxCombo: 0, cleanCount: 0, claimedIds: [] };
    saveProProfile(prof);
  }
  const dq = prof.dailyQuests;
  const defs = [
    { id: "q_grad15", title: "Dokonči 15 karet (min. 1 den)", cur: todayCount, target: 15, reward: 40 },
    { id: "q_combo5", title: "Dosáhni Combo 5x", cur: dq.maxCombo || 0, target: 5, reward: 35 },
    { id: "q_clean10", title: "10 karet bez tlačítka Znovu", cur: dq.cleanCount || 0, target: 10, reward: 50 }
  ];
  return { dq, defs };
}

function renderDailyQuests(prof, todayCount) {
  const strip = document.getElementById("proQuestsStrip");
  if (!strip) return;
  const { dq, defs } = getDailyQuestsState(prof, todayCount);
  strip.innerHTML = "";
  defs.forEach(q => {
    const done = dq.claimedIds.includes(q.id) || q.cur >= q.target;
    const pct = Math.min(100, Math.round((q.cur / q.target) * 100));
    const card = document.createElement("div");
    card.className = `pro-quest-card ${done ? "done" : ""}`;
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; gap:6px; font-weight:700;">
        <span>${q.title}</span>
        <span style="color:${done ? "#34d399" : "#fbbf24"};">${done ? "Splněno" : `+${q.reward} b.`}</span>
      </div>
      <div class="pro-bar-track" style="height:6px;">
        <div class="pro-bar-fill pro-bar-goal" style="width:${pct}%;"></div>
      </div>
    `;
    strip.appendChild(card);
  });
}

async function renderShopModal() {
  const { prof, streak } = await computeProStreakAndFreeze();
  const balEl = document.getElementById("shopBalanceVal");
  if (balEl) balEl.innerText = `${prof.points} b.`;
  const selGoal = document.getElementById("selProDailyGoal");
  if (selGoal) selGoal.value = String(prof.dailyGoal || 20);

  const themesBox = document.getElementById("shopThemesList");
  if (themesBox) {
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
        <button class="btn btn-sm ${isActive ? "" : "btn-primary"}">${isActive ? "Aktivní" : (unlocked ? "Použít" : `Koupit (${th.cost} b.)`)}</button>
      `;
      row.querySelector("button").onclick = async () => {
        const p = loadProProfile();
        if (p.unlockedThemes.includes(th.id)) {
          p.activeTheme = th.id;
        } else {
          if (p.points < th.cost) { alert("Nemáte dostatek bodů."); return; }
          p.points -= th.cost;
          p.unlockedThemes.push(th.id);
          p.activeTheme = th.id;
        }
        saveProProfile(p);
        applyProTheme(p.activeTheme);
        await updateProHud();
        await renderShopModal();
      };
      themesBox.appendChild(row);
    });
  }

  const msBox = document.getElementById("shopMilestonesList");
  if (msBox) {
    msBox.innerHTML = "";
    prof.milestones.sort((a, b) => a.days - b.days).forEach(ms => {
      const row = document.createElement("div");
      row.className = `milestone-row ${ms.claimed ? "claimed" : ""}`;
      row.innerHTML = `
        <div>
          <strong>${ms.days} dní</strong> – ${escapeHtml(ms.title)}
          <span style="color:#4ade80; font-weight:700;">(+${ms.bonusPoints || 0} b.)</span>
          ${ms.claimed ? '<span style="color:#86efac; margin-left:6px;">[Splněno]</span>' : `<span style="color:var(--text-muted); margin-left:6px;">(${Math.min(streak, ms.days)}/${ms.days})</span>`}
        </div>
        <button class="btn btn-sm btn-danger" style="padding:2px 8px;">Smazat</button>
      `;
      row.querySelector("button").onclick = async () => {
        const p = loadProProfile();
        p.milestones = p.milestones.filter(x => x.id !== ms.id);
        saveProProfile(p);
        await renderShopModal();
      };
      msBox.appendChild(row);
    });
  }
}

// Wrap rateCard: award points and daily goal ONLY when card is scheduled for >= 1 full day
const _origRateCardPro = rateCard;
rateCard = async function(ratingKey) {
  const intervals = calcNextIntervals(currentCard);
  const chosen = intervals[ratingKey];
  const isGraduatedForDay = chosen && chosen.ms >= 86400000;

  await _origRateCardPro(ratingKey);

  const prof = loadProProfile();
  const prevLv = getLevelInfo(prof.xp ?? prof.points).level;
  const isBoost = prof.boostUntil > Date.now();
  const todayStr = getLocalDateString();
  if (!prof.dailyQuests || prof.dailyQuests.date !== todayStr) {
    prof.dailyQuests = { date: todayStr, maxCombo: 0, cleanCount: 0, claimedIds: [] };
  }

  if (ratingKey === "again") {
    sessionCombo = 0;
    prof.dailyQuests.cleanCount = 0;
    playProTone("again");
    const comboEl = document.getElementById("proComboBadge");
    if (comboEl) comboEl.style.display = "none";
    saveProProfile(prof);
    showProToast("Opakování za chvíli (body až po odložení o 1+ den)");
    await updateProHud();
    return;
  }

  if (ratingKey === "good" || ratingKey === "easy") {
    sessionCombo++;
    prof.dailyQuests.maxCombo = Math.max(prof.dailyQuests.maxCombo || 0, sessionCombo);
  }
  prof.dailyQuests.cleanCount = (prof.dailyQuests.cleanCount || 0) + 1;

  const comboEl = document.getElementById("proComboBadge");
  if (comboEl) {
    if (sessionCombo >= 3) {
      comboEl.style.display = "inline-flex";
      comboEl.innerText = `Combo ${sessionCombo}x`;
    } else {
      comboEl.style.display = "none";
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

  const reviews = await dbGetAllReviews();
  const todayCount = reviews.filter(r => r && r.dateStr === todayStr && (r.interval || 0) >= 1).length;

  // Check daily quests
  const { dq, defs } = getDailyQuestsState(prof, todayCount);
  let questReward = 0;
  defs.forEach(q => {
    if (!dq.claimedIds.includes(q.id) && q.cur >= q.target) {
      dq.claimedIds.push(q.id);
      questReward += q.reward;
    }
  });
  if (questReward > 0) {
    prof.points += questReward;
    prof.xp += questReward;
    launchConfetti();
    playProTone("level");
  }

  const newLv = getLevelInfo(prof.xp).level;
  if (todayCount >= prof.dailyGoal && !prof.dailyBonusDates.includes(todayStr)) {
    prof.dailyBonusDates.push(todayStr);
    prof.points += 30;
    prof.xp += 30;
    launchConfetti();
    playProTone("level");
    showProToast(`Denní cíl splněn! +${gained + 30 + questReward} b.`);
  } else if (questReward > 0) {
    showProToast(`Denní výzva splněna! +${gained + questReward} b.`);
  } else if (newLv > prevLv) {
    launchConfetti();
    playProTone("level");
    showProToast(`Nová úroveň ${newLv}! (+${gained} b.)`);
  } else if (comboBonus > 0) {
    showProToast(`Skvělé combo ${sessionCombo}x! +${gained} b.`);
  } else {
    showProToast(`+${gained} b.${isBoost ? " (2x)" : ""}`);
  }
  saveProProfile(prof);
  await updateProHud();
};

// Wrap renderHeatmap to highlight frozen days
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

document.getElementById("btnProSound").onclick = async () => {
  const p = loadProProfile();
  p.soundEnabled = (p.soundEnabled === false);
  saveProProfile(p);
  if (p.soundEnabled) playProTone("good");
  await updateProHud();
};

// Shop Modal Listeners
document.getElementById("btnOpenShop").onclick = async () => {
  await renderShopModal();
  document.getElementById("shopModal").classList.add("active");
};
document.getElementById("shopModalClose").onclick = () => document.getElementById("shopModal").classList.remove("active");
document.getElementById("shopModal").addEventListener("click", (e) => {
  if (e.target.id === "shopModal") document.getElementById("shopModal").classList.remove("active");
});
document.getElementById("selProDailyGoal").onchange = async (e) => {
  const p = loadProProfile();
  p.dailyGoal = parseInt(e.target.value, 10) || 20;
  saveProProfile(p);
  await updateProHud();
};
document.getElementById("btnBuyFreeze").onclick = async () => {
  const p = loadProProfile();
  if (p.freezes >= 3) { alert("Máte již plnou zásobu (3/3 Streak Freeze)."); return; }
  if (p.points < 150) { alert("Potřebujete alespoň 150 bodů."); return; }
  p.points -= 150;
  p.freezes++;
  saveProProfile(p);
  showProToast("Zakoupen Streak Freeze!");
  await updateProHud();
  await renderShopModal();
};
document.getElementById("btnBuyBoost").onclick = async () => {
  const p = loadProProfile();
  if (p.points < 100) { alert("Potřebujete alespoň 100 bodů."); return; }
  p.points -= 100;
  p.boostUntil = Date.now() + 15 * 60 * 1000;
  saveProProfile(p);
  showProToast("Aktivován 2x Body Boost na 15 min!");
  await updateProHud();
  await renderShopModal();
};
document.getElementById("btnBuyRepair").onclick = async () => {
  const p = loadProProfile();
  const yesterdayStr = addDaysToDateStr(getLocalDateString(), -1);
  if (p.frozenDates.includes(yesterdayStr)) {
    alert("Včerejší den už je chráněný.");
    return;
  }
  if (p.points < 400) { alert("Potřebujete alespoň 400 bodů."); return; }
  p.points -= 400;
  p.frozenDates.push(yesterdayStr);
  saveProProfile(p);
  showProToast("Včerejší série byla opravena!");
  await renderHeatmap();
  await renderShopModal();
};
document.getElementById("btnBuyMystery").onclick = async () => {
  const p = loadProProfile();
  if (p.points < 120) { alert("Potřebujete alespoň 120 bodů."); return; }
  p.points -= 120;
  const roll = Math.random();
  let msg = "";
  if (roll < 0.25 && p.freezes < 3) {
    p.freezes++;
    msg = "Tajemná truhla: Získali jste 1x Streak Freeze!";
  } else if (roll < 0.5) {
    p.boostUntil = Date.now() + 15 * 60 * 1000;
    msg = "Tajemná truhla: 2x Body Boost na 15 min!";
  } else {
    const winPts = [60, 100, 150, 220][Math.floor(Math.random() * 4)];
    p.points += winPts;
    msg = `Tajemná truhla: +${winPts} bodů!`;
  }
  saveProProfile(p);
  launchConfetti();
  playProTone("level");
  showProToast(msg);
  await updateProHud();
  await renderShopModal();
};
document.getElementById("btnBuyShieldPack").onclick = async () => {
  const p = loadProProfile();
  if (p.freezes >= 3) { alert("Zásobu Freeze už máte plnou (3/3)."); return; }
  if (p.points < 380) { alert("Potřebujete alespoň 380 bodů."); return; }
  p.points -= 380;
  p.freezes = 3;
  saveProProfile(p);
  showProToast("Zásoba Streak Freeze doplněna na 3/3!");
  await updateProHud();
  await renderShopModal();
};
document.getElementById("btnAddMilestone").onclick = async () => {
  const days = parseInt(document.getElementById("inpNewMsDays").value, 10);
  const title = document.getElementById("inpNewMsReward").value.trim() || `Milník ${days} dní`;
  const bonus = Math.max(0, parseInt(document.getElementById("inpNewMsBonus").value, 10) || 0);
  if (!days || days < 1) { alert("Zadejte platný počet dní."); return; }
  const p = loadProProfile();
  p.milestones.push({ id: "m_" + Date.now(), days, title, bonusPoints: bonus, claimed: false });
  saveProProfile(p);
  document.getElementById("inpNewMsReward").value = "";
  await renderShopModal();
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

assert '<div class="progress-pills">' in html
html = html.replace('<div class="progress-pills">', '<span class="pro-combo-badge" id="proComboBadge">Combo 3x</span>\n        <div class="progress-pills">', 1)

assert "<!-- HELP MODAL -->" in html
html = html.replace("<!-- HELP MODAL -->", PRO_MODAL_HTML + "\n<!-- HELP MODAL -->", 1)

# Include proProfile in .json progress export/import
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

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully generated pro/index.html ({len(html.encode('utf-8'))} bytes)")
