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
/* --- KARTY PRO GAMIFICATION --- */
body.theme-midnight {
  --bg-main: #0b1120;
  --bg-card: #111a2e;
  --bg-card-hover: #17233d;
  --bg-surface: #1b2947;
  --border-color: #263a63;
  --border-highlight: #3b5998;
  --accent: #38bdf8;
  --accent-hover: #0ea5e9;
}
body.theme-amber {
  --bg-main: #14100a;
  --bg-card: #1f1810;
  --bg-card-hover: #292016;
  --bg-surface: #33271a;
  --border-color: #473623;
  --border-highlight: #785936;
  --accent: #f59e0b;
  --accent-hover: #d97706;
}
body.theme-mono {
  --bg-main: #09090b;
  --bg-card: #18181b;
  --bg-card-hover: #27272a;
  --bg-surface: #27272a;
  --border-color: #3f3f46;
  --border-highlight: #71717a;
  --accent: #e4e4e7;
  --accent-hover: #ffffff;
}
.pro-hud {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.pro-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-main);
  white-space: nowrap;
}
.pro-pill.streak { border-color: rgba(245, 158, 11, 0.5); color: #fbbf24; }
.pro-pill.points { border-color: rgba(34, 197, 94, 0.5); color: #4ade80; }
.pro-pill.freeze { border-color: rgba(56, 189, 248, 0.5); color: #38bdf8; }
.pro-pill.boost { border-color: rgba(168, 85, 247, 0.6); color: #c084fc; }
.hm-cell.frozen {
  background: #38bdf8 !important;
  box-shadow: 0 0 4px rgba(56, 189, 248, 0.6);
}
.pro-toast {
  position: fixed;
  bottom: 84px;
  left: 50%;
  transform: translateX(-50%) translateY(16px);
  background: #18251d;
  border: 1px solid var(--accent);
  color: #edf5f0;
  padding: 9px 16px;
  border-radius: 999px;
  font-size: 0.86rem;
  font-weight: 700;
  z-index: 300;
  opacity: 0;
  pointer-events: none;
  transition: all 0.25s ease;
  box-shadow: 0 8px 24px rgba(0,0,0,0.55);
  white-space: nowrap;
}
.pro-toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
.shop-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.shop-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  background: rgba(12, 18, 14, 0.55);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 10px 12px;
}
.shop-item-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.shop-item-title {
  font-weight: 700;
  font-size: 0.92rem;
  color: var(--text-main);
}
.shop-item-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
}
.milestone-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 7px 10px;
  border-radius: 8px;
  background: rgba(12, 18, 14, 0.45);
  border: 1px solid var(--border-color);
  font-size: 0.84rem;
}
.milestone-row.claimed {
  border-color: rgba(34, 197, 94, 0.5);
  background: rgba(34, 197, 94, 0.08);
}
@media (max-width: 768px) {
  header {
    flex-wrap: wrap;
    gap: 8px;
  }
  .pro-pill {
    padding: 3px 8px;
    font-size: 0.74rem;
  }
}
"""

PRO_HEADER_HUD = r"""  <div class="pro-hud" id="proHud">
    <span class="pro-pill streak" id="proStreakPill" title="Aktuální denní série">Série: 0 d</span>
    <span class="pro-pill points" id="proPointsPill" title="Nasbírané body">Body: 0</span>
    <span class="pro-pill freeze" id="proFreezePill" title="Zásoba Streak Freeze">Freeze: 0/3</span>
    <span class="pro-pill" id="proGoalPill" title="Dnešní denní cíl">Cíl: 0/20</span>
    <span class="pro-pill boost" id="proBoostPill" style="display:none;">2x Boost</span>
    <button class="btn btn-sm btn-primary" id="btnOpenShop">Obchod a milníky</button>
  </div>"""

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
  { id: "default", name: "Hluboký les (výchozí)", cost: 0 },
  { id: "midnight", name: "Půlnoční modř", cost: 200 },
  { id: "amber", name: "Jantarová pracovna", cost: 250 },
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
  for (const [dStr, cnt] of countsByDate.entries()) {
    if (cnt >= 1) activeSet.add(dStr);
  }
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
      msAwarded = true;
      showProToast(`Milník ${ms.days} dní splněn: ${ms.title} (+${ms.bonusPoints || 0} b.)`);
    }
  }
  if (msAwarded) saveProProfile(prof);

  const todayCount = countsByDate.get(todayStr) || 0;
  return { prof, streak, todayCount, frozenSet };
}

async function updateProHud() {
  const { prof, streak, todayCount } = await computeProStreakAndFreeze();
  applyProTheme(prof.activeTheme);
  const elStreak = document.getElementById("proStreakPill");
  const elPoints = document.getElementById("proPointsPill");
  const elFreeze = document.getElementById("proFreezePill");
  const elGoal = document.getElementById("proGoalPill");
  const elBoost = document.getElementById("proBoostPill");
  if (elStreak) elStreak.innerText = `Série: ${streak} d`;
  if (elPoints) elPoints.innerText = `Body: ${prof.points}`;
  if (elFreeze) elFreeze.innerText = `Freeze: ${prof.freezes}/3`;
  if (elGoal) elGoal.innerText = `Cíl: ${todayCount}/${prof.dailyGoal}`;
  if (elBoost) elBoost.style.display = (prof.boostUntil > Date.now()) ? "inline-flex" : "none";
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

// Wrap rateCard for XP/points and daily goal bonus
const _origRateCardPro = rateCard;
rateCard = async function(ratingKey) {
  await _origRateCardPro(ratingKey);
  const prof = loadProProfile();
  const isBoost = prof.boostUntil > Date.now();
  const basePts = (ratingKey === "good" || ratingKey === "easy") ? 10 : 5;
  const gained = basePts * (isBoost ? 2 : 1);
  prof.points += gained;

  const todayStr = getLocalDateString();
  const reviews = await dbGetAllReviews();
  const todayCount = reviews.filter(r => r && r.dateStr === todayStr).length;
  if (todayCount >= prof.dailyGoal && !prof.dailyBonusDates.includes(todayStr)) {
    prof.dailyBonusDates.push(todayStr);
    prof.points += 30;
    showProToast(`Denní cíl splněn! +${gained + 30} bodů`);
  } else {
    showProToast(`+${gained} b.${isBoost ? " (2x Boost)" : ""}`);
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
