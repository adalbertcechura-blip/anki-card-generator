# -*- coding: utf-8 -*-
"""
Script to construct the standalone Karty.html offline flashcard application.
Inlines jszip.min.js and packages complete offline learning engine with IndexedDB,
Anki-style review heatmap, deck statistics modal, daily new card limits, and type-in card mode.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSZIP_PATH = os.path.join(BASE_DIR, "jszip.min.js")

with open(JSZIP_PATH, "r", encoding="utf-8") as f:
    jszip_code = f.read()

html_template = r"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#0c120e">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>Karty – Chytrý přehrávač kartiček</title>
<style>
:root {
  --bg-main: #0c120e;
  --bg-card: #141e17;
  --bg-card-hover: #19271e;
  --bg-surface: #1b2b21;
  --border-color: #24392b;
  --border-highlight: #3b6348;
  --accent: #22c55e;
  --accent-hover: #16a34a;
  --text-main: #edf5f0;
  --text-muted: #95ab9e;
  --btn-again: #ef4444;
  --btn-hard: #f59e0b;
  --btn-good: #3b82f6;
  --btn-easy: #10b981;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  --radius: 12px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-tap-highlight-color: transparent;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

header {
  background: rgba(12, 18, 14, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border-color);
  padding: 12px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 50;
}

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-main);
  cursor: pointer;
  user-select: none;
}
.logo-badge {
  background: var(--accent);
  color: #051a0c;
  font-size: 0.72rem;
  padding: 2px 7px;
  border-radius: 999px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--bg-surface);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
}
.btn:hover {
  background: var(--border-highlight);
  border-color: var(--accent);
}
.btn-primary {
  background: var(--accent);
  color: #041f0f;
  border-color: var(--accent);
}
.btn-primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}
.btn-sm {
  padding: 5px 10px;
  font-size: 0.8rem;
  border-radius: 6px;
}
.btn-danger {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.4);
  color: #fca5a5;
}
.btn-danger:hover {
  background: #ef4444;
  color: #fff;
}
.btn-icon {
  width: 28px;
  height: 28px;
  padding: 0;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

main {
  flex: 1;
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

/* SCREEN: DECKS LIBRARY */
#decksView {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.drop-zone {
  border: 2px dashed var(--border-highlight);
  background: rgba(27, 43, 33, 0.4);
  border-radius: var(--radius);
  padding: 24px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}
.drop-zone:hover, .drop-zone.dragover {
  border-color: var(--accent);
  background: rgba(34, 197, 94, 0.12);
  transform: translateY(-2px);
}
.drop-icon {
  font-size: 2.2rem;
  margin-bottom: 6px;
}
.drop-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 2px;
}
.drop-subtitle {
  font-size: 0.82rem;
  color: var(--text-muted);
}

/* REVIEW HEATMAP (ANKI STYLE) */
.heatmap-container {
  background: #141a16;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 14px 18px;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.heatmap-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.heatmap-nav-group {
  display: flex;
  align-items: center;
  gap: 6px;
}
.heatmap-year-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
  min-width: 50px;
  text-align: center;
}
.heatmap-filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}
.select-sm {
  background: var(--bg-surface);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.82rem;
  outline: none;
}
.heatmap-scroll-area {
  overflow-x: auto;
  padding: 4px 0;
  -webkit-overflow-scrolling: touch;
}
.heatmap-body {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  min-width: 660px;
}
.heatmap-days-col {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 84px;
  font-size: 9px;
  color: var(--text-muted);
  user-select: none;
  padding-top: 1px;
}
.heatmap-grid {
  display: grid;
  grid-template-rows: repeat(7, 10px);
  grid-auto-flow: column;
  grid-auto-columns: 10px;
  gap: 2.5px;
}
.hm-day {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  background: #232b25;
  transition: transform 0.1s ease;
  cursor: pointer;
}
.hm-day:hover {
  transform: scale(1.4);
  z-index: 10;
  box-shadow: 0 0 5px rgba(74, 222, 128, 0.8);
}
.hm-day.is-future {
  opacity: 0.22;
  cursor: default;
}
.hm-day.is-today {
  outline: 1.5px solid #ffffff;
  outline-offset: 1px;
}
.hm-lvl-0 { background: #232b25; }
.hm-lvl-1 { background: #166534; } /* 1-9 */
.hm-lvl-2 { background: #15803d; } /* 10-24 */
.hm-lvl-3 { background: #22c55e; } /* 25-59 */
.hm-lvl-4 { background: #86efac; } /* 60+ */

.heatmap-stats-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.85rem;
  color: #d1d5db;
}
.hm-stat {
  display: flex;
  gap: 5px;
  align-items: baseline;
}
.hm-stat-val {
  color: #4ade80;
  font-weight: 700;
}
.hm-stat-val.zero {
  color: #ffffff;
}

/* Tooltip for Heatmap */
.hm-tooltip {
  position: fixed;
  background: #18221b;
  border: 1px solid var(--border-highlight);
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 0.78rem;
  color: #fff;
  pointer-events: none;
  z-index: 999;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  display: none;
  white-space: nowrap;
}

/* DECK LIST */
.deck-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.deck-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 16px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  transition: all 0.15s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.deck-card:hover {
  border-color: var(--border-highlight);
  background: var(--bg-card-hover);
}
.deck-info {
  flex: 1;
  min-width: 220px;
}
.deck-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 4px;
}
.deck-meta {
  display: flex;
  gap: 8px;
  font-size: 0.82rem;
  color: var(--text-muted);
  flex-wrap: wrap;
  align-items: center;
}
.badge-count {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--bg-surface);
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
}
.badge-new {
  color: #60a5fa;
  border-color: rgba(96, 165, 250, 0.4);
}
.badge-due {
  color: #f87171;
  border-color: rgba(248, 113, 113, 0.4);
}
.deck-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

/* SCREEN: STUDY / REVIEW */
#studyView {
  display: none;
  flex-direction: column;
  height: 100%;
}

.study-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 10px;
}
.study-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
}
.progress-pills {
  display: flex;
  gap: 6px;
}
.pill {
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
  min-width: 28px;
  text-align: center;
}
.pill-new { background: rgba(59, 130, 246, 0.2); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.4); }
.pill-due { background: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }
.pill-done { background: rgba(34, 197, 94, 0.2); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); }

.study-options-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.85rem;
  color: var(--text-muted);
  flex-wrap: wrap;
  gap: 10px;
}
.mode-toggle-group {
  display: inline-flex;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 2px;
}
.btn-mode-tgl {
  background: transparent;
  color: var(--text-muted);
  border: none;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-mode-tgl.active {
  background: var(--border-highlight);
  color: #fff;
}
.switch-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.flashcard-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.flashcard {
  flex: 1;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 24px;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow);
  overflow-y: auto;
  max-height: calc(100vh - 250px);
}

.card-face {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.card-question {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.card-answer {
  display: none;
  flex-direction: column;
  gap: 14px;
  padding-top: 18px;
  border-top: 2px dashed var(--border-color);
  margin-top: 18px;
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Card images */
.card-img-thumb {
  display: block;
  margin: 8px auto;
  max-width: 100%;
  width: auto;
  border-radius: 10px;
  object-fit: contain;
  cursor: zoom-in;
  border: 1px solid var(--border-color);
  background: #000;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.45);
  transition: transform 0.15s ease, border-color 0.15s ease;
}
.card-img-thumb:hover {
  transform: scale(1.02);
  border-color: var(--accent);
}

/* DESKTOP PC (velké a zřetelné fotografie na monitoru) */
@media (min-width: 769px) {
  main {
    max-width: 1100px;
  }
  .flashcard {
    max-height: calc(100vh - 210px);
    padding: 28px 36px;
  }
  .card-img-thumb {
    max-height: 540px;
    min-height: 260px;
  }
}

/* MOBILNÍ TELEFON (přizpůsobení rozměrům displeje mobilu) */
@media (max-width: 768px) {
  main {
    padding: 8px 6px;
    max-width: 100%;
  }
  header {
    padding: 10px 14px;
  }
  .logo {
    font-size: 1.1rem;
  }
  #studyView {
    height: 100%;
    max-height: calc(100dvh - 54px);
  }
  .flashcard {
    padding: 14px 10px;
    max-height: calc(100dvh - 190px);
    border-radius: 10px;
  }
  .card-face {
    gap: 10px;
  }
  .card-question, .card-answer {
    gap: 8px;
  }
  .card-img-thumb {
    width: 100%;
    max-width: 100%;
    max-height: 38vh;
    min-height: 170px;
    margin: 4px auto;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }
  .card-text {
    font-size: 0.98rem;
    line-height: 1.5;
  }
  .study-controls {
    margin-top: 8px;
    gap: 6px;
  }
  .btn-flip {
    padding: 12px;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .flashcard {
    padding: 12px 8px;
    max-height: calc(100dvh - 180px);
  }
  .card-img-thumb {
    max-height: 36vh;
    min-height: 150px;
  }
  .rating-grid {
    gap: 5px;
  }
  .btn-rate {
    padding: 8px 3px;
    font-size: 0.86rem;
  }
}

.card-text {
  font-size: 1.05rem;
  line-height: 1.6;
}
.card-text strong { color: #fff; }
.card-text h1, .card-text h2, .card-text h3 {
  color: var(--text-main);
  margin-bottom: 6px;
}
.card-text p { margin-bottom: 10px; }
.card-text ul { padding-left: 20px; margin-bottom: 10px; }
.card-text a {
  color: var(--accent);
  text-decoration: underline;
  word-break: break-all;
}

/* TYPE-IN MODE AREA */
.type-input-area {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.type-input-box {
  display: flex;
  gap: 8px;
}
.type-text-input {
  flex: 1;
  background: var(--bg-surface);
  border: 1.5px solid var(--border-highlight);
  color: #fff;
  padding: 12px 14px;
  font-size: 1.05rem;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.15s ease;
}
.type-text-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
}
.type-diff-display {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px 14px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.05rem;
  line-height: 1.6;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.diff-char {
  display: inline-block;
  padding: 1px 2px;
  border-radius: 3px;
}
.diff-ok {
  background: rgba(34, 197, 94, 0.25);
  color: #86efac;
  font-weight: 700;
}
.diff-err {
  background: rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  text-decoration: underline;
  font-weight: 700;
}
.diff-miss {
  background: rgba(245, 158, 11, 0.2);
  color: #fcd34d;
  opacity: 0.85;
}

/* Study Control Bars */
.study-controls {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.btn-flip {
  width: 100%;
  padding: 14px;
  font-size: 1.05rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-highlight);
  color: var(--text-main);
  font-weight: 700;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-flip:hover {
  background: var(--border-highlight);
  border-color: var(--accent);
}

.rating-grid {
  display: none;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
@media (max-width: 580px) {
  .rating-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
.btn-rate {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 8px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.95rem;
  border: 1px solid transparent;
  transition: transform 0.1s ease, filter 0.15s ease;
  user-select: none;
}
.btn-rate:active { transform: scale(0.96); }
.btn-rate span.interval {
  font-size: 0.72rem;
  font-weight: 500;
  opacity: 0.85;
  margin-top: 2px;
}
.btn-rate-again { background: rgba(239, 68, 68, 0.18); border-color: var(--btn-again); color: #fca5a5; }
.btn-rate-again:hover { background: var(--btn-again); color: #fff; }
.btn-rate-hard { background: rgba(245, 158, 11, 0.18); border-color: var(--btn-hard); color: #fcd34d; }
.btn-rate-hard:hover { background: var(--btn-hard); color: #000; }
.btn-rate-good { background: rgba(59, 130, 246, 0.18); border-color: var(--btn-good); color: #93c5fd; }
.btn-rate-good:hover { background: var(--btn-good); color: #fff; }
.btn-rate-easy { background: rgba(16, 185, 129, 0.18); border-color: var(--btn-easy); color: #6ee7b7; }
.btn-rate-easy:hover { background: var(--btn-easy); color: #042415; }

/* SCREEN: FINISHED */
#finishedView {
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
  gap: 20px;
}
.finished-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 36px 28px;
  max-width: 500px;
  width: 100%;
  box-shadow: var(--shadow);
}
.finished-icon {
  font-size: 3.5rem;
  margin-bottom: 12px;
}

/* LIGHTBOX ZOOM */
.lightbox {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.93);
  z-index: 100;
  align-items: center;
  justify-content: center;
  padding: 16px;
  cursor: zoom-out;
}
.lightbox.active { display: flex; }
.lightbox-img {
  max-width: 96vw;
  max-height: 94vh;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.8);
}
.lightbox-close {
  position: absolute;
  top: 16px;
  right: 20px;
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  cursor: pointer;
  background: rgba(0,0,0,0.5);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* MODALS */
.modal-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(4px);
  z-index: 80;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.modal-overlay.active { display: flex; }
.modal-box {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 24px;
  max-width: 480px;
  width: 100%;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 90vh;
  overflow-y: auto;
}

/* ANKI DECK STATS MODAL SPECIFICS */
.stats-modal-box {
  background: #121c15;
  border-color: var(--border-color);
  color: #d4d4d8;
  max-width: 470px;
}
.stats-table {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 0.95rem;
  margin: 10px 0;
}
.stats-row {
  display: grid;
  grid-template-columns: 175px 65px 55px 55px;
  align-items: center;
  line-height: 1.6;
}
.stats-lbl {
  color: #e4e4e7;
  font-weight: 500;
}
.stats-num {
  text-align: right;
  font-weight: 700;
  padding-right: 14px;
}
.num-blue { color: #3b82f6; }
.num-red { color: #ef4444; }
.num-green { color: #22c55e; }
.stats-pct {
  text-align: right;
  color: #71717a;
  font-size: 0.86rem;
}
.stats-divider {
  height: 1px;
  background: #27272a;
  margin: 6px 0;
}
.stats-done-row {
  display: flex;
  justify-content: space-between;
  font-size: 1.02rem;
  margin: 10px 0 14px 0;
  color: #e4e4e7;
}
.stats-done-row strong {
  color: #ffffff;
  font-size: 1.12rem;
}
.daily-limit-control {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid #27272a;
  border-radius: 8px;
  font-size: 0.88rem;
  margin-bottom: 6px;
}
.btn-study-now-blue {
  background: #2563eb;
  color: #ffffff;
  border: none;
  border-radius: 999px;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  width: 100%;
  text-align: center;
  transition: all 0.15s ease;
  margin-top: 4px;
}
.btn-study-now-blue:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}
</style>
</head>
<body>

<header>
  <div class="logo" id="btnHome">
    🌱 <span>Karty</span>
    
  </div>
  <div class="nav-actions">
    <button class="btn btn-sm" id="btnHelp" title="Nápověda k ovládání">
      ❓ Nápověda
    </button>
  </div>
</header>

<main>
  <!-- 1. KNIHOVNA BALÍČKŮ -->
  <section id="decksView">


    <!-- REVIEW HEATMAP (ANKI STYLE) -->
    <div class="heatmap-container" id="heatmapContainer">
      <div class="heatmap-topbar">
        <div class="heatmap-nav-group">
          <button class="btn btn-sm btn-icon" id="hmBtnPrevYear" title="Předchozí rok">◀</button>
          <button class="btn btn-sm btn-icon" id="hmBtnToday" title="Aktuální rok">●</button>
          <button class="btn btn-sm btn-icon" id="hmBtnNextYear" title="Následující rok">▶</button>
          <span class="heatmap-year-title" id="hmYearTitle">2026</span>
        </div>
        <div class="heatmap-filter-group">
          <select id="hmDeckSelect" class="select-sm">
            <option value="all">Všechny balíčky</option>
          </select>
        </div>
      </div>

      <div class="heatmap-scroll-area">
        <div class="heatmap-body">
          <div class="heatmap-days-col">
            <span>Po</span>
            <span>St</span>
            <span>Pá</span>
            <span>Ne</span>
          </div>
          <div class="heatmap-grid" id="heatmapGrid">
            <!-- Dynamically generated days -->
          </div>
        </div>
      </div>

      <div class="heatmap-stats-bar">
        <div class="hm-stat">Denní průměr: <span class="hm-stat-val" id="hmDailyAvg">0 karet</span></div>
        <div class="hm-stat">Dny s učením: <span class="hm-stat-val" id="hmDaysLearned">0%</span></div>
        <div class="hm-stat">Nejdelší série: <span class="hm-stat-val" id="hmLongestStreak">0 dní</span></div>
        <div class="hm-stat">Aktuální série: <span class="hm-stat-val zero" id="hmCurrentStreak">0 dní</span></div>
      </div>
    </div>

    <div class="drop-zone" id="dropZone">
      <div class="drop-icon">📦</div>
      <div class="drop-title">Přetáhněte sem balíček .zip nebo klikněte</div>
      <div class="drop-subtitle">Otevřete balíček s kartičkami vygenerovaný generátorem (nebo vyberte soubory kartiček)</div>
      <input type="file" id="fileZipInput" accept=".zip,application/zip,application/x-zip-compressed,application/octet-stream,.md,text/markdown,*/*" multiple style="display:none">
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h2 style="font-size:1.15rem; font-weight:700;">Moje balíčky</h2>
      <span id="deckCountInfo" style="font-size:0.85rem; color:var(--text-muted);">0 balíčků</span>
    </div>

    <div class="deck-list" id="deckList">
      <!-- Generováno dynamicky -->
    </div>
  </section>

  <!-- 2. PROHLÍŽEČ KARTIČEK / ZKOUŠENÍ -->
  <section id="studyView">
    <div class="study-header">
      <div style="display:flex; align-items:center; gap:10px;">
        <button class="btn btn-sm" id="btnBackToDecks">← Balíčky</button>
        <span class="study-title" id="activeDeckTitle">Název balíčku</span>
      </div>
      <div class="study-progress">
        <div class="progress-pills">
          <span class="pill pill-new" id="pillNew" title="Nové karty dnes">0</span>
          <span class="pill pill-due" id="pillDue" title="K opakování dnes">0</span>
          <span class="pill pill-done" id="pillDone" title="Hotovo v této relaci">0</span>
        </div>
      </div>
    </div>

    <div class="study-options-bar">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <div class="mode-toggle-group">
          <button class="btn-mode-tgl active" id="btnModeFlip" title="Režim otáčení karty">🔄 Otáčecí</button>
          <button class="btn-mode-tgl" id="btnModeType" title="Režim vepisování z klávesnice">⌨️ Vepisovací</button>
        </div>
        <label class="switch-label">
          <input type="checkbox" id="chkReverseStudy">
          <span>Otočit směr</span>
        </label>
        <label class="switch-label">
          <input type="checkbox" id="chkQuickReview">
          <span>Rychlé procvičení</span>
        </label>
      </div>
    </div>

    <div class="flashcard-wrapper">
      <div class="flashcard" id="flashcardBox">
        <div class="card-face">
          <div class="card-question" id="cardQuestion">
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
          </div>

          <div class="card-answer" id="cardAnswer">
            <!-- Odpověď po otočení -->
          </div>
        </div>
      </div>

      <div class="study-controls">
        <button class="btn-flip" id="btnFlip">Zobrazit odpověď (Mezerník / Klepnutí)</button>
        <div class="rating-grid" id="ratingGrid">
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
        </div>
        <div id="quickNavGrid" style="display:none; justify-content:space-between; gap:10px;">
          <button class="btn" id="btnPrevCard" style="flex:1;">← Předchozí</button>
          <button class="btn btn-primary" id="btnNextCard" style="flex:1;">Další →</button>
        </div>
      </div>
    </div>
  </section>

  <!-- 3. OBRAZOVKA: HOTOVO -->
  <section id="finishedView">
    <div class="finished-card">
      <div class="finished-icon">🎉</div>
      <h2 style="margin-bottom:8px;">Všechny kartičky jsou zopakované!</h2>
      <p style="color:var(--text-muted); margin-bottom:20px;" id="finishedMsg">
        Skvělá práce. Na dnešek máte splněné všechny naplánované kartičky v tomto balíčku.
      </p>
      <div style="display:flex; flex-direction:column; gap:10px;" id="finishedActions">
        <button class="btn btn-primary" id="btnStudyMoreNew" style="display:none;">Procvičit dalších 10 nových karet dnes</button>
        <button class="btn" id="btnStudyAllAgain">Procvičit celý balíček znova (rychlý režim)</button>
        <button class="btn" id="btnFinishBackDecks">Zpět na přehled balíčků</button>
      </div>
    </div>
  </section>
</main>

<!-- FLOATING TOOLTIP FOR HEATMAP -->
<div class="hm-tooltip" id="hmTooltip"></div>

<!-- LIGHTBOX ZOOM -->
<div class="lightbox" id="lightbox">
  <div class="lightbox-close" id="lightboxClose">&times;</div>
  <img class="lightbox-img" id="lightboxImg" src="" alt="Detail">
</div>

<!-- HELP MODAL -->
<div class="modal-overlay" id="helpModal">
  <div class="modal-box">
    <h3 style="font-size:1.2rem;">Klávesové zkratky a ovládání</h3>
    <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 8px 12px; font-size: 0.82rem; color: #86efac;">
      💡 Tento přehrávač funguje plně offline přímo ve vašem webovém prohlížeči (na počítači, telefonu i tabletu).
    </div>
    <ul style="padding-left:20px; line-height:1.8; color:var(--text-muted); font-size:0.92rem;">
      <li><strong style="color:#fff;">Mezerník / Enter / Klepnutí na kartu</strong>: Zobrazit odpověď</li>
      <li><strong style="color:#fff;">Vepisovací režim (⌨️)</strong>: Napište název a stiskněte Enter pro okamžité porovnání</li>
      <li><strong style="color:#fff;">1</strong>: Znovu (nepamatuji si, ukázat za chvíli)</li>
      <li><strong style="color:#fff;">2</strong>: Těžké (správně, ale s obtížemi)</li>
      <li><strong style="color:#fff;">3</strong>: Dobré (správně, standardní interval)</li>
      <li><strong style="color:#fff;">4</strong>: Snadné (velmi jednoduché, dlouhý interval)</li>
      <li><strong style="color:#fff;">Klepnutí na fotografii</strong>: Zvětšení na celou obrazovku</li>
      <li><strong style="color:#fff;">Esc</strong>: Zavřít zvětšeninu / Zpět na balíčky</li>
    </ul>
    <button class="btn btn-primary" id="btnHelpClose" style="align-self:flex-end;">Rozumím</button>
  </div>
</div>

<!-- ANKI-STYLE DECK STATS MODAL (SCREENSHOT 2) -->
<div class="modal-overlay" id="deckStatsModal">
  <div class="modal-box stats-modal-box">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:12px;">
      <h3 style="font-size:1.15rem; font-weight:700; color:#fff;" id="stDeckTitle">Statistiky balíčku</h3>
      <button class="btn btn-sm" id="btnStatsClose" style="padding:4px 8px;">✕</button>
    </div>

    <div class="stats-table">
      <div class="stats-row"><span class="stats-lbl">Nové karty:</span><span class="stats-num num-blue" id="stNewNum">0</span><span class="stats-pct" id="stNewPct1">0%</span><span class="stats-pct" id="stNewPct2">0%</span></div>
      <div class="stats-row"><span class="stats-lbl">V procesu učení:</span><span class="stats-num num-red" id="stLearnNum">0</span><span class="stats-pct" id="stLearnPct1">0%</span><span class="stats-pct" id="stLearnPct2">0%</span></div>
      <div class="stats-row"><span class="stats-lbl">K opakování:</span><span class="stats-num num-green" id="stRevNum">0</span><span class="stats-pct" id="stRevPct1">0%</span><span class="stats-pct" id="stRevPct2">0%</span></div>
      <div class="stats-divider"></div>
      <div class="stats-row"><span class="stats-lbl">Zvládnuté (≥ 21 dní):</span><span class="stats-num num-blue" id="stMatNum">0</span><span class="stats-pct" id="stMatPct1">0%</span><span class="stats-pct" id="stMatPct2">0%</span></div>
      <div class="stats-row"><span class="stats-lbl">Mladé (< 21 dní):</span><span class="stats-num num-blue" id="stYngNum">0</span><span class="stats-pct" id="stYngPct1">0%</span><span class="stats-pct" id="stYngPct2">0%</span></div>
      <div class="stats-divider"></div>
      <div class="stats-row"><span class="stats-lbl">Naučené celkem:</span><span class="stats-num num-green" id="stLrnNum">0</span><span class="stats-pct" id="stLrnPct1">0%</span><span class="stats-pct" id="stLrnPct2">0%</span></div>
      <div class="stats-row"><span class="stats-lbl">Dosud neviděné:</span><span class="stats-num num-red" id="stUnsNum">0</span><span class="stats-pct" id="stUnsPct1">0%</span><span class="stats-pct" id="stUnsPct2">0%</span></div>
      <div class="stats-row"><span class="stats-lbl">Odložené:</span><span class="stats-num" id="stBurNum">0</span><span class="stats-pct">0%</span><span class="stats-pct">0%</span></div>
      <div class="stats-row"><span class="stats-lbl">Pozastavené:</span><span class="stats-num" id="stSusNum">0</span><span class="stats-pct">0%</span><span class="stats-pct" style="color:#71717a;">přeskočeno</span></div>
      <div class="stats-divider"></div>
      <div class="stats-row" style="font-weight:700;"><span class="stats-lbl" style="color:#fff;">Celkem kartiček:</span><span class="stats-num" style="color:#fff;" id="stTotNum">0</span><span class="stats-pct">100%</span><span class="stats-pct">100%</span></div>
      <div class="stats-divider"></div>
      <div class="stats-done-row">
        <span>Dokončení za: <strong id="stDoneDays">0 dní</strong></span>
        <span>dne: <strong id="stDoneDate">--</strong></span>
      </div>
    </div>

    <!-- Nastavení denního limitu pro tento balíček -->
    <div class="daily-limit-control">
      <span style="color:#a1a1aa; font-weight:500;">Denní limit nových karet:</span>
      <div style="display:flex; align-items:center; gap:6px;">
        <input type="number" id="inpStatsNewLimit" min="0" max="500" value="20" style="width:68px; background:#09090b; border:1px solid #3f3f46; color:#fff; padding:4px 8px; border-radius:6px; text-align:center; font-weight:700; font-size:0.92rem;">
        <span style="font-size:0.8rem; color:#71717a;">/ den</span>
      </div>
    </div>

    <button class="btn-study-now-blue" id="btnStatsStudyNow">Začít studovat tento balíček</button>
  </div>
</div>

<!-- INLINED JSZIP LIBRARY -->
<script>
__JSZIP_SOURCE__
</script>

<!-- PRELOADED DECK (BUILT-IN DATA FROM GENERATOR) -->
<script id="inlinedPreloadedDeck">
/* __INLINED_DECK_DATA__ */
</script>
<script src="deck_data.js" onerror="/* Standalone mode without external deck_data.js */"></script>

<!-- APP LOGIC -->
<script>
// --- INDEXEDDB STORAGE MANAGER ---
const DB_NAME = "KartyFlashcardsDB";
const DB_VERSION = 2;
let db = null;

function initDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const d = e.target.result;
      if (!d.objectStoreNames.contains("decks")) {
        d.createObjectStore("decks", { keyPath: "id" });
      }
      if (!d.objectStoreNames.contains("media")) {
        d.createObjectStore("media");
      }
      if (!d.objectStoreNames.contains("reviews")) {
        const revStore = d.createObjectStore("reviews", { keyPath: "id", autoIncrement: true });
        revStore.createIndex("deckId", "deckId", { unique: false });
        revStore.createIndex("dateStr", "dateStr", { unique: false });
      }
    };
    req.onsuccess = (e) => {
      db = e.target.result;
      resolve(db);
    };
    req.onerror = (e) => reject(e);
  });
}

function dbSaveDeck(deck) {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["decks"], "readwrite");
    tx.objectStore("decks").put(deck);
    tx.oncomplete = () => resolve();
    tx.onerror = (e) => reject(e);
  });
}

function dbGetAllDecks() {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["decks"], "readonly");
    const req = tx.objectStore("decks").getAll();
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = (e) => reject(e);
  });
}

function dbGetDeck(id) {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["decks"], "readonly");
    const req = tx.objectStore("decks").get(id);
    req.onsuccess = () => resolve(req.result);
    req.onerror = (e) => reject(e);
  });
}

function dbDeleteDeck(id) {
  return new Promise(async (resolve, reject) => {
    try {
      const stores = ["decks", "media"];
      if (db.objectStoreNames.contains("reviews")) stores.push("reviews");
      const tx = db.transaction(stores, "readwrite");
      tx.objectStore("decks").delete(id);
      
      const mediaStore = tx.objectStore("media");
      const cursorReq = mediaStore.openCursor();
      cursorReq.onsuccess = (e) => {
        const cursor = e.target.result;
        if (cursor) {
          if (String(cursor.key).startsWith(id + ":")) {
            cursor.delete();
          }
          cursor.continue();
        }
      };

      if (db.objectStoreNames.contains("reviews")) {
        const revStore = tx.objectStore("reviews");
        const revReq = revStore.openCursor();
        revReq.onsuccess = (e) => {
          const c = e.target.result;
          if (c) {
            if (c.value && c.value.deckId === id) c.delete();
            c.continue();
          }
        };
      }

      tx.oncomplete = () => resolve();
      tx.onerror = (e) => reject(e);
    } catch(err) {
      reject(err);
    }
  });
}

function dbSaveMedia(deckId, filename, blob) {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["media"], "readwrite");
    tx.objectStore("media").put(blob, deckId + ":" + filename);
    tx.oncomplete = () => resolve();
    tx.onerror = (e) => reject(e);
  });
}

function dbGetMedia(deckId, filename) {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["media"], "readonly");
    const req = tx.objectStore("media").get(deckId + ":" + filename);
    req.onsuccess = () => resolve(req.result);
    req.onerror = (e) => reject(e);
  });
}

function dbAddReview(entry) {
  return new Promise((resolve) => {
    try {
      if (!db.objectStoreNames.contains("reviews")) {
        resolve();
        return;
      }
      const tx = db.transaction(["reviews"], "readwrite");
      tx.objectStore("reviews").add(entry);
      tx.oncomplete = () => resolve();
      tx.onerror = () => resolve();
    } catch(err) {
      resolve();
    }
  });
}

function dbGetAllReviews() {
  return new Promise((resolve) => {
    try {
      if (!db.objectStoreNames.contains("reviews")) {
        dbGetAllDecks().then(decks => {
          let list = [];
          decks.forEach(d => { if (d.history) list = list.concat(d.history); });
          resolve(list);
        });
        return;
      }
      const tx = db.transaction(["reviews"], "readonly");
      const req = tx.objectStore("reviews").getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => resolve([]);
    } catch(err) {
      resolve([]);
    }
  });
}

// Media Blob URL Cache
const mediaUrlCache = new Map();

async function getMediaUrl(deckId, filename) {
  const cacheKey = deckId + ":" + filename;
  if (mediaUrlCache.has(cacheKey)) {
    return mediaUrlCache.get(cacheKey);
  }
  const blob = await dbGetMedia(deckId, filename);
  if (blob) {
    const url = URL.createObjectURL(blob);
    mediaUrlCache.set(cacheKey, url);
    return url;
  }
  return null;
}

// Helper: Formát místního data YYYY-MM-DD
function getLocalDateString(d = new Date()) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

// --- STATE ---
let currentDeck = null;
let studyQueue = [];
let currentIndex = 0;
let isCardFlipped = false;
let sessionStats = { newCount: 0, dueCount: 0, doneCount: 0 };
let currentCard = null;
let cardStudyMode = "flip"; // "flip" or "type"
let heatmapYear = new Date().getFullYear();
let statsModalDeck = null;
let extraNewCardsGranted = 0;

// --- SPACED REPETITION (SM-2) CALCULATION ---
function calcNextIntervals(card) {
  const reps = card.reps || 0;
  const ease = card.ease || 2.5;
  const interval = card.interval || 0;

  // 1. Znovu (Again)
  const againMinutes = 10;
  
  // 2. Těžké (Hard)
  let hardDays;
  if (reps === 0) {
    hardDays = 1;
  } else {
    hardDays = Math.max(1, Math.round(interval * 1.2));
  }

  // 3. Dobré (Good)
  let goodDays;
  if (reps === 0) {
    goodDays = 1;
  } else if (reps === 1) {
    goodDays = 4;
  } else {
    goodDays = Math.max(2, Math.round(interval * ease));
  }

  // 4. Snadné (Easy)
  let easyDays;
  if (reps === 0) {
    easyDays = 4;
  } else {
    easyDays = Math.max(goodDays + 1, Math.round(interval * ease * 1.3));
  }

  return {
    again: { text: "< 10 min", ms: againMinutes * 60 * 1000, newInterval: 0.007, newEase: Math.max(1.3, ease - 0.2), newReps: 0 },
    hard: { text: formatDays(hardDays), ms: hardDays * 86400000, newInterval: hardDays, newEase: Math.max(1.3, ease - 0.15), newReps: reps + 1 },
    good: { text: formatDays(goodDays), ms: goodDays * 86400000, newInterval: goodDays, newEase: ease, newReps: reps + 1 },
    easy: { text: formatDays(easyDays), ms: easyDays * 86400000, newInterval: easyDays, newEase: ease + 0.15, newReps: reps + 1 }
  };
}

function formatDays(days) {
  if (days <= 1) return "1 den";
  if (days < 5) return days + " dny";
  if (days < 30) return days + " dní";
  const months = Math.round(days / 30);
  if (months <= 1) return "1 měsíc";
  if (months < 5) return months + " měsíce";
  return months + " měsíců";
}

// --- RENDER MARKDOWN & IMAGES ---
async function renderContentToHtml(content, deckId) {
  if (!content) return "";
  
  const htmlTags = [];
  const protectTag = (tag) => {
    const idx = htmlTags.length;
    htmlTags.push(tag);
    return `@@HTMLTAG_${idx}@@`;
  };

  // 1. Nahrazení Obsidian obrázků ![[nazev.jpg]]
  let text = content.replace(/!\[\[(.*?)\]\]/g, (match, fn) => {
    const cleanFn = fn.trim().split('/').pop().split('\\').pop();
    return protectTag(`<img src="" data-src="${cleanFn}" class="card-img-thumb pending-media" alt="${cleanFn}">`);
  });

  // 2. Nahrazení standardních markdown obrázků ![alt](nazev.jpg)
  text = text.replace(/!\[(.*?)\]\((.*?)\)/g, (match, alt, src) => {
    const cleanSrc = src.trim().split('/').pop().split('\\').pop();
    return protectTag(`<img src="" data-src="${cleanSrc}" class="card-img-thumb pending-media" alt="${alt}">`);
  });

  // 3. HTML img tagy: <img src="...">
  text = text.replace(/<img[^>]+src=["'](.*?)["'][^>]*>/gi, (match, src) => {
    const cleanSrc = src.trim().split('/').pop().split('\\').pop();
    return protectTag(`<img src="" data-src="${cleanSrc}" class="card-img-thumb pending-media" alt="${cleanSrc}">`);
  });

  // 4. Odkazy [text](url)
  text = text.replace(/\[(.*?)\]\((https?:\/\/.*?)\)/g, (match, label, url) => {
    return protectTag(`<a href="${url}" target="_blank" rel="noopener">${label}</a>`);
  });

  // 5. Tučné písmo **text**
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // 6. Kurzíva *text*
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Obnovení chráněných HTML tagů (aby se neporušily názvy souborů s podtržítky/hvězdičkami)
  text = text.replace(/@@HTMLTAG_(\d+)@@/g, (match, idx) => htmlTags[Number(idx)] || '');

  // 7. Odstavce a řádky
  const lines = text.split('\n');
  let html = "";
  let inList = false;

  for (let l of lines) {
    l = l.trim();
    if (!l) {
      if (inList) { html += "</ul>"; inList = false; }
      continue;
    }
    if (l.startsWith('# ')) {
      if (inList) { html += "</ul>"; inList = false; }
      html += `<h2 style="font-size:1.4rem; color:#fff; margin-bottom:8px;">${l.substring(2)}</h2>`;
    } else if (l.startsWith('## ')) {
      if (inList) { html += "</ul>"; inList = false; }
      html += `<h3 style="font-size:1.2rem; color:#4ade80; margin-bottom:6px;">${l.substring(3)}</h3>`;
    } else if (l.startsWith('- ')) {
      if (!inList) { html += '<ul style="padding-left:20px; margin-bottom:10px;">'; inList = true; }
      html += `<li>${l.substring(2)}</li>`;
    } else {
      if (inList) { html += "</ul>"; inList = false; }
      html += `<p style="margin-bottom:8px;">${l}</p>`;
    }
  }
  if (inList) html += "</ul>";

  return html;
}

async function resolvePendingImages(container, deckId) {
  const imgs = container.querySelectorAll("img.pending-media");
  for (const img of imgs) {
    const filename = img.getAttribute("data-src");
    if (filename) {
      const url = await getMediaUrl(deckId, filename);
      if (url) {
        img.src = url;
        img.classList.remove("pending-media");
        img.addEventListener("click", (e) => {
          e.stopPropagation();
          openLightbox(url);
        });
      } else {
        // Fallback: přímé cesty při spuštění ze složky
        img.src = filename;
        img.onerror = () => {
          img.onerror = () => { img.style.display = "none"; };
          img.src = "media/" + filename;
        };
        img.addEventListener("click", (e) => {
          e.stopPropagation();
          openLightbox(img.src);
        });
      }
    }
  }
}

// --- LIGHTBOX ---
function openLightbox(src) {
  const lb = document.getElementById("lightbox");
  const img = document.getElementById("lightboxImg");
  img.src = src;
  lb.classList.add("active");
}
document.getElementById("lightboxClose").onclick = () => document.getElementById("lightbox").classList.remove("active");
document.getElementById("lightbox").onclick = () => document.getElementById("lightbox").classList.remove("active");

// --- ZIP PARSER ---
async function importZipFile(file) {
  try {
    const zip = await JSZip.loadAsync(file);
    let deckName = file.name.replace(/\.zip$/i, "").replace(/_/g, " ");
    
    const files = Object.keys(zip.files);
    const mediaBlobs = {};
    const mdCards = [];

    for (const filename of files) {
      const entry = zip.files[filename];
      if (entry.dir) continue;

      const lower = filename.toLowerCase();
      const baseFn = filename.split('/').pop().split('\\').pop();

      if (lower.endsWith('.jpg') || lower.endsWith('.jpeg') || lower.endsWith('.png') || lower.endsWith('.webp') || lower.endsWith('.svg') || lower.endsWith('.gif')) {
        const blob = await entry.async("blob");
        mediaBlobs[baseFn] = blob;
      } else if (lower.endsWith('.md')) {
        if (baseFn.startsWith("00_")) continue;
        const text = await entry.async("text");
        mdCards.push({ filename: baseFn, text: text });
      }
    }

    if (mdCards.length === 0) {
      alert("V archivu nebyl nalezen žádný soubor s kartičkami (.md).");
      return;
    }

    const deckId = "deck_" + Date.now();
    const cards = [];

    for (let i = 0; i < mdCards.length; i++) {
      const { filename, text } = mdCards[i];
      let front = "";
      let back = "";
      let title = filename.replace(/\.md$/i, "");

      const matchQ = text.match(/\n(\?{1,2})\n/);
      if (matchQ) {
        const qIndex = matchQ.index;
        const qLen = matchQ[0].length;
        front = text.substring(0, qIndex).trim();
        back = text.substring(qIndex + qLen).trim();
      } else {
        const parts = text.split(/^---$/m);
        if (parts.length >= 3) {
          const body = parts.slice(2).join("---").trim();
          const subQ = body.indexOf("\n?\n");
          if (subQ !== -1) {
            front = body.substring(0, subQ).trim();
            back = body.substring(subQ + 3).trim();
          } else {
            front = title;
            back = body;
          }
        } else {
          front = title;
          back = text;
        }
      }

      front = front.replace(/^---[\s\S]*?---\s*/, "");
      front = front.replace(/#flashcards[^\s]*/gi, "").trim();

      cards.push({
        id: "c_" + i + "_" + Date.now(),
        title: title,
        front: front,
        back: back,
        interval: 0,
        reps: 0,
        ease: 2.5,
        due: 0,
        state: 0
      });
    }

    for (const [fn, blob] of Object.entries(mediaBlobs)) {
      await dbSaveMedia(deckId, fn, blob);
    }

    const newDeck = {
      id: deckId,
      name: deckName,
      createdAt: Date.now(),
      cards: cards,
      settings: {
        newCardsPerDay: 20
      },
      history: []
    };

    await dbSaveDeck(newDeck);
    alert(`Úspěšně importován balíček "${deckName}" (${cards.length} kartiček, ${Object.keys(mediaBlobs).length} fotografií)!`);
    await loadDeckList();
  } catch (err) {
    console.error(err);
    alert("Chyba při čtení archivu .zip: " + err.message);
  }
}

async function importLooseFiles(files) {
  try {
    const mediaBlobs = {};
    const mdCards = [];
    let sampleDeckName = "Importovaný balíček";

    for (const f of files) {
      const lower = f.name.toLowerCase();
      const baseFn = f.name.split('/').pop().split('\\').pop();

      if (lower.endsWith('.jpg') || lower.endsWith('.jpeg') || lower.endsWith('.png') || lower.endsWith('.webp') || lower.endsWith('.svg') || lower.endsWith('.gif')) {
        mediaBlobs[baseFn] = f;
      } else if (lower.endsWith('.md')) {
        if (baseFn.startsWith("00_")) continue;
        const text = await f.text();
        mdCards.push({ filename: baseFn, text: text });
      }
    }

    if (mdCards.length === 0) {
      alert("Nebyly nalezeny žádné soubory s kartičkami (.md).");
      return;
    }

    const deckId = "deck_" + Date.now();
    const cards = [];

    for (let i = 0; i < mdCards.length; i++) {
      const { filename, text } = mdCards[i];
      let front = "";
      let back = "";
      let title = filename.replace(/\.md$/i, "");

      const matchQ = text.match(/\n(\?{1,2})\n/);
      if (matchQ) {
        const qIndex = matchQ.index;
        const qLen = matchQ[0].length;
        front = text.substring(0, qIndex).trim();
        back = text.substring(qIndex + qLen).trim();
      } else {
        const parts = text.split(/^---$/m);
        if (parts.length >= 3) {
          const body = parts.slice(2).join("---").trim();
          const subQ = body.indexOf("\n?\n");
          if (subQ !== -1) {
            front = body.substring(0, subQ).trim();
            back = body.substring(subQ + 3).trim();
          } else {
            front = title;
            back = body;
          }
        } else {
          front = title;
          back = text;
        }
      }

      front = front.replace(/^---[\s\S]*?---\s*/, "");
      front = front.replace(/#flashcards[^\s]*/gi, "").trim();

      cards.push({
        id: "c_" + i + "_" + Date.now(),
        title: title,
        front: front,
        back: back,
        interval: 0,
        reps: 0,
        ease: 2.5,
        due: 0,
        state: 0
      });
    }

    for (const [fn, blob] of Object.entries(mediaBlobs)) {
      await dbSaveMedia(deckId, fn, blob);
    }

    const newDeck = {
      id: deckId,
      name: sampleDeckName,
      createdAt: Date.now(),
      cards: cards,
      settings: {
        newCardsPerDay: 20
      },
      history: []
    };

    await dbSaveDeck(newDeck);
    alert(`Úspěšně importováno ${cards.length} kartiček (${Object.keys(mediaBlobs).length} fotografií)!`);
    await loadDeckList();
  } catch (err) {
    console.error(err);
    alert("Chyba při importu souborů: " + err.message);
  }
}

// --- REVIEW HEATMAP ENGINE (SCREENSHOT 1) ---
async function renderHeatmap() {
  const allDecks = await dbGetAllDecks();
  const allReviews = await dbGetAllReviews();
  const selectEl = document.getElementById("hmDeckSelect");

  // Synchronizace výběru balíčků ve filtru
  const currentVal = selectEl.value;
  selectEl.innerHTML = '<option value="all">Všechny balíčky</option>';
  allDecks.forEach(d => {
    const opt = document.createElement("option");
    opt.value = d.id;
    opt.textContent = d.name;
    selectEl.appendChild(opt);
  });
  if (Array.from(selectEl.options).some(o => o.value === currentVal)) {
    selectEl.value = currentVal;
  }

  const selectedDeckId = selectEl.value;
  document.getElementById("hmYearTitle").innerText = heatmapYear;

  // Filtrovat recenze podle balíčku
  const filtered = selectedDeckId === "all" ? allReviews : allReviews.filter(r => r.deckId === selectedDeckId);

  // Spočítat počty podle data (YYYY-MM-DD)
  const dateCounts = {};
  filtered.forEach(r => {
    const dStr = r.dateStr || (r.timestamp ? getLocalDateString(new Date(r.timestamp)) : null);
    if (dStr) {
      dateCounts[dStr] = (dateCounts[dStr] || 0) + 1;
    }
  });

  // Příprava kalendářní mřížky pro vybraný rok
  const gridEl = document.getElementById("heatmapGrid");
  gridEl.innerHTML = "";

  const jan1 = new Date(heatmapYear, 0, 1);
  const dec31 = new Date(heatmapYear, 11, 31);
  const now = new Date();
  const todayStr = getLocalDateString(now);

  // Vytvoříme dny od prvního pondělí
  // Den v týdnu 0 = Ne, 1 = Po, ... 6 = So
  let startOffset = jan1.getDay() - 1; // 0 pro Po, 6 pro Ne
  if (startOffset === -1) startOffset = 6;

  // Prázdné buňky před 1. lednem pro zarovnání na pondělí
  for (let pad = 0; pad < startOffset; pad++) {
    const empty = document.createElement("div");
    empty.style.width = "10px";
    empty.style.height = "10px";
    empty.style.visibility = "hidden";
    gridEl.appendChild(empty);
  }

  let totalReviews = 0;
  let activeDaysCount = 0;
  let totalDaysUpToToday = 0;
  let dayList = [];

  const cur = new Date(jan1);
  while (cur <= dec31) {
    const dStr = getLocalDateString(cur);
    const count = dateCounts[dStr] || 0;
    const isFuture = cur > now && dStr !== todayStr;
    const isToday = dStr === todayStr;

    if (!isFuture) {
      totalDaysUpToToday++;
      if (count > 0) {
        totalReviews += count;
        activeDaysCount++;
      }
    }

    dayList.push({ dStr, count, isFuture, isToday, dateObj: new Date(cur) });

    const cell = document.createElement("div");
    cell.className = "hm-day";
    if (isFuture) cell.classList.add("is-future");
    if (isToday) cell.classList.add("is-today");

    if (count === 0) cell.classList.add("hm-lvl-0");
    else if (count < 10) cell.classList.add("hm-lvl-1");
    else if (count < 25) cell.classList.add("hm-lvl-2");
    else if (count < 60) cell.classList.add("hm-lvl-3");
    else cell.classList.add("hm-lvl-4");

    // Tooltip
    cell.onmouseenter = (e) => showHeatmapTooltip(e, dStr, count);
    cell.onmouseleave = hideHeatmapTooltip;

    gridEl.appendChild(cell);
    cur.setDate(cur.getDate() + 1);
  }

  // Statistiky heatmapy (Screenshot 1)
  const avg = activeDaysCount > 0 ? Math.round(totalReviews / activeDaysCount) : 0;
  const daysPct = totalDaysUpToToday > 0 ? Math.round((activeDaysCount / totalDaysUpToToday) * 100) : 0;

  // Streaks
  let longestStreak = 0;
  let currentStreak = 0;
  let tempStreak = 0;

  for (let i = 0; i < dayList.length; i++) {
    if (dayList[i].isFuture) break;
    if (dayList[i].count > 0) {
      tempStreak++;
      if (tempStreak > longestStreak) longestStreak = tempStreak;
    } else {
      tempStreak = 0;
    }
  }

  // Current streak (od dneška zpět)
  const todayIdx = dayList.findIndex(d => d.dStr === todayStr);
  if (todayIdx !== -1) {
    let checkIdx = todayIdx;
    // Pokud dnes ještě neopakoval, podíváme se na včerejšek
    if (dayList[todayIdx].count === 0 && todayIdx > 0 && dayList[todayIdx - 1].count > 0) {
      checkIdx = todayIdx - 1;
    }
    while (checkIdx >= 0 && dayList[checkIdx].count > 0) {
      currentStreak++;
      checkIdx--;
    }
  }

  document.getElementById("hmDailyAvg").innerText = `${avg} karet`;
  document.getElementById("hmDaysLearned").innerText = `${daysPct}%`;
  document.getElementById("hmLongestStreak").innerText = `${longestStreak} dní`;

  const curStreakEl = document.getElementById("hmCurrentStreak");
  curStreakEl.innerText = currentStreak + (currentStreak === 1 ? " den" : (currentStreak < 5 && currentStreak > 0 ? " dny" : " dní"));
  if (currentStreak > 0) {
    curStreakEl.className = "hm-stat-val";
  } else {
    curStreakEl.className = "hm-stat-val zero";
  }
}

const tooltipEl = document.getElementById("hmTooltip");
function showHeatmapTooltip(e, dStr, count) {
  const parts = dStr.split("-");
  const dObj = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
  const dayNames = ["Neděle", "Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota"];
  const monthNames = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"];
  const dayName = dayNames[dObj.getDay()];
  const formatted = `${dayName} ${parseInt(parts[2])}. ${monthNames[dObj.getMonth()]} ${parts[0]}`;
  let countText = `${count} zopakovaných karet`;
  if (count === 0) countText = "Žádná aktivita v tento den";
  else if (count === 1) countText = "1 zopakovaná karta";
  else if (count >= 2 && count <= 4) countText = `${count} zopakované karty`;

  tooltipEl.innerHTML = `<strong>${formatted}</strong><br>${countText}`;
  tooltipEl.style.display = "block";
  tooltipEl.style.left = (e.clientX + 10) + "px";
  tooltipEl.style.top = (e.clientY - 35) + "px";
}
function hideHeatmapTooltip() {
  tooltipEl.style.display = "none";
}

document.getElementById("hmBtnPrevYear").onclick = () => { heatmapYear--; renderHeatmap(); };
document.getElementById("hmBtnNextYear").onclick = () => { heatmapYear++; renderHeatmap(); };
document.getElementById("hmBtnToday").onclick = () => { heatmapYear = new Date().getFullYear(); renderHeatmap(); };
document.getElementById("hmDeckSelect").onchange = renderHeatmap;

// --- ANKI DECK STATS MODAL ENGINE (SCREENSHOT 2) ---
function openDeckStats(deck) {
  statsModalDeck = deck;
  document.getElementById("stDeckTitle").innerText = `Statistiky: ${deck.name}`;

  const cards = deck.cards || [];
  const total = cards.length;
  const now = Date.now();

  let countNew = 0;
  let countLearn = 0;
  let countReview = 0;
  let countMature = 0;
  let countYoung = 0;

  cards.forEach(c => {
    const isNew = !c.due || c.due === 0;
    const interval = c.interval || 0;
    const reps = c.reps || 0;

    if (isNew) {
      countNew++;
    } else {
      if (reps === 1 || interval < 1) {
        countLearn++;
      } else {
        countReview++;
      }

      if (interval >= 21) {
        countMature++;
      } else if (interval > 0) {
        countYoung++;
      }
    }
  });

  const countLearned = countMature + countYoung;
  const countUnseen = countNew;

  const pct = (val) => total > 0 ? Math.round((val / total) * 100) + "%" : "0%";

  document.getElementById("stNewNum").innerText = countNew;
  document.getElementById("stNewPct1").innerText = pct(countNew);
  document.getElementById("stNewPct2").innerText = pct(countNew);

  document.getElementById("stLearnNum").innerText = countLearn;
  document.getElementById("stLearnPct1").innerText = pct(countLearn);
  document.getElementById("stLearnPct2").innerText = pct(countLearn);

  document.getElementById("stRevNum").innerText = countReview;
  document.getElementById("stRevPct1").innerText = pct(countReview);
  document.getElementById("stRevPct2").innerText = pct(countReview);

  document.getElementById("stMatNum").innerText = countMature;
  document.getElementById("stMatPct1").innerText = pct(countMature);
  document.getElementById("stMatPct2").innerText = pct(countMature);

  document.getElementById("stYngNum").innerText = countYoung;
  document.getElementById("stYngPct1").innerText = pct(countYoung);
  document.getElementById("stYngPct2").innerText = pct(countYoung);

  document.getElementById("stLrnNum").innerText = countLearned;
  document.getElementById("stLrnPct1").innerText = pct(countLearned);
  document.getElementById("stLrnPct2").innerText = pct(countLearned);

  document.getElementById("stUnsNum").innerText = countUnseen;
  document.getElementById("stUnsPct1").innerText = pct(countUnseen);
  document.getElementById("stUnsPct2").innerText = pct(countUnseen);

  document.getElementById("stTotNum").innerText = total;

  // Nastavení denního limitu
  const currentLimit = (deck.settings && typeof deck.settings.newCardsPerDay === "number") ? deck.settings.newCardsPerDay : 20;
  const inpLimit = document.getElementById("inpStatsNewLimit");
  inpLimit.value = currentLimit;

  function updateDoneInCalculation(limit) {
    if (limit <= 0) {
      document.getElementById("stDoneDays").innerText = "1 den";
      document.getElementById("stDoneDate").innerText = "ihned (bez limitu)";
      return;
    }
    const daysNeeded = Math.ceil(countUnseen / limit);
    document.getElementById("stDoneDays").innerText = `${daysNeeded} ${daysNeeded === 1 ? 'den' : (daysNeeded < 5 ? 'dny' : 'dní')}`;
    const targetDate = new Date(Date.now() + daysNeeded * 86400000);
    const dStr = `${targetDate.getDate()}.${targetDate.getMonth() + 1}.${targetDate.getFullYear()}`;
    document.getElementById("stDoneDate").innerText = dStr;
  }

  updateDoneInCalculation(currentLimit);

  inpLimit.oninput = async () => {
    const val = parseInt(inpLimit.value) || 0;
    deck.settings = deck.settings || {};
    deck.settings.newCardsPerDay = val;
    updateDoneInCalculation(val);
    await dbSaveDeck(deck);
  };

  document.getElementById("btnStatsStudyNow").onclick = () => {
    document.getElementById("deckStatsModal").classList.remove("active");
    startStudy(deck.id, false);
  };

  document.getElementById("deckStatsModal").classList.add("active");
}

document.getElementById("btnStatsClose").onclick = () => {
  document.getElementById("deckStatsModal").classList.remove("active");
};
document.getElementById("deckStatsModal").onclick = (e) => {
  if (e.target.id === "deckStatsModal") document.getElementById("deckStatsModal").classList.remove("active");
};

// --- DECK LIST VIEW ---
async function loadDeckList() {
  const decks = await dbGetAllDecks();
  const listEl = document.getElementById("deckList");
  const countEl = document.getElementById("deckCountInfo");
  listEl.innerHTML = "";
  countEl.innerText = `${decks.length} ${decks.length === 1 ? 'balíček' : (decks.length < 5 ? 'balíčky' : 'balíčků')}`;

  if (decks.length === 0) {
    listEl.innerHTML = `
      <div style="text-align:center; padding:30px; color:var(--text-muted); background:var(--bg-card); border-radius:var(--radius); border:1px solid var(--border-color);">
        Zatím nemáte nahrané žádné balíčky. Přetáhněte sem soubor <strong>.zip</strong> vygenerovaný generátorem nebo klikněte na pole výše.
      </div>`;
    await renderHeatmap();
    return;
  }

  const now = Date.now();
  const todayStr = getLocalDateString();
  const allReviews = await dbGetAllReviews();

  decks.forEach(deck => {
    let newCardsTotal = 0;
    let dueCards = 0;
    deck.cards.forEach(c => {
      if (!c.due || c.due === 0) newCardsTotal++;
      else if (c.due <= now) dueCards++;
    });

    const dailyLimit = (deck.settings && typeof deck.settings.newCardsPerDay === "number") ? deck.settings.newCardsPerDay : 20;

    // Kolik nových karet uživatel dnes již prošel
    const newStudiedToday = allReviews.filter(r => r.deckId === deck.id && r.dateStr === todayStr && r.isNew).length;
    const newRemainingToday = dailyLimit > 0 ? Math.max(0, dailyLimit - newStudiedToday) : newCardsTotal;
    const newCardsToStudyToday = Math.min(newCardsTotal, newRemainingToday);

    const studyCount = dueCards + newCardsToStudyToday;

    const cardEl = document.createElement("div");
    cardEl.className = "deck-card";
    cardEl.innerHTML = `
      <div class="deck-info">
        <div class="deck-title">${escapeHtml(deck.name)}</div>
        <div class="deck-meta">
          <span class="badge-count">Celkem: ${deck.cards.length}</span>
          <span class="badge-count badge-due" title="Karty vyžadující zopakování">K opakování: ${dueCards}</span>
          <span class="badge-count badge-new" title="Zbývá nových na dnešek z limitu ${dailyLimit}/den">Nové dnes: ${newCardsToStudyToday} / ${dailyLimit > 0 ? dailyLimit : '∞'}</span>
        </div>
      </div>
      <div class="deck-actions">
        <button class="btn btn-primary btn-study" data-id="${deck.id}">Učit se (${studyCount})</button>
        <button class="btn btn-sm btn-stats" data-id="${deck.id}" title="Podrobné Anki statistiky balíčku">📊 Statistiky</button>
        <button class="btn btn-sm btn-review" data-id="${deck.id}" title="Procvičit všechny karty z balíčku">Procvičit vše</button>
        <button class="btn btn-sm btn-reset" data-id="${deck.id}" title="Vrátit všechny karty do stavu Nové">↺ Reset</button>
        <button class="btn btn-danger btn-sm btn-del" data-id="${deck.id}" title="Smazat balíček">🗑️</button>
      </div>
    `;

    cardEl.querySelector(".btn-study").onclick = () => startStudy(deck.id, false);
    cardEl.querySelector(".btn-stats").onclick = () => openDeckStats(deck);
    cardEl.querySelector(".btn-review").onclick = () => startStudy(deck.id, true);
    cardEl.querySelector(".btn-reset").onclick = async () => {
      if (confirm(`Opravdu chcete resetovat postup učení pro balíček "${deck.name}"? Všechny kartičky budou označeny jako nové.`)) {
        deck.cards.forEach(c => {
          c.due = 0;
          c.interval = 0;
          c.reps = 0;
          c.ease = 2.5;
          c.state = 0;
        });
        await dbSaveDeck(deck);
        await loadDeckList();
      }
    };
    cardEl.querySelector(".btn-del").onclick = async () => {
      if (confirm(`Opravdu chcete smazat balíček "${deck.name}"? Všechny kartičky a statistiky budou odstraněny.`)) {
        await dbDeleteDeck(deck.id);
        await loadDeckList();
      }
    };

    listEl.appendChild(cardEl);
  });

  await renderHeatmap();
}

function escapeHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// --- STUDY ENGINE ---
async function startStudy(deckId, quickMode = false) {
  currentDeck = await dbGetDeck(deckId);
  if (!currentDeck || currentDeck.cards.length === 0) {
    alert("Balíček je prázdný.");
    return;
  }

  const now = Date.now();
  const todayStr = getLocalDateString();
  const allReviews = await dbGetAllReviews();

  document.getElementById("chkQuickReview").checked = quickMode;

  if (quickMode) {
    studyQueue = [...currentDeck.cards].sort(() => Math.random() - 0.5);
  } else {
    const due = currentDeck.cards.filter(c => c.due && c.due > 0 && c.due <= now);
    const newCardsAll = currentDeck.cards.filter(c => !c.due || c.due === 0);

    // Vymáhání denního limitu nových karet
    const dailyLimit = (currentDeck.settings && typeof currentDeck.settings.newCardsPerDay === "number") ? currentDeck.settings.newCardsPerDay : 20;
    const studiedNewToday = allReviews.filter(r => r.deckId === currentDeck.id && r.dateStr === todayStr && r.isNew).length;
    
    let allowedNew = dailyLimit > 0 ? Math.max(0, dailyLimit + extraNewCardsGranted - studiedNewToday) : newCardsAll.length;
    const selectedNew = newCardsAll.slice(0, allowedNew);

    studyQueue = [...due, ...selectedNew];
  }

  if (studyQueue.length === 0) {
    showFinishedView();
    return;
  }

  currentIndex = 0;
  sessionStats = {
    newCount: studyQueue.filter(c => !c.due || c.due === 0).length,
    dueCount: studyQueue.filter(c => c.due && c.due > 0 && c.due <= now).length,
    doneCount: 0
  };

  document.getElementById("activeDeckTitle").innerText = currentDeck.name;
  showView("study");
  loadCard(currentIndex);
}

// Extrakce očekávaného textu pro vepisovací režim
function extractTargetAnswer(card, isReverse) {
  if (!card) return "";
  const cleanFirstField = (raw) => {
    const cleanText = (raw || "")
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]+>/g, '')
      .replace(/!\[.*?\]\(.*?\)/g, '')
      .replace(/!\[\[.*?\]\]/g, '')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g, '$1')
      .trim();
    if (!cleanText) return "";
    const lines = cleanText
      .split('\n')
      .map(l => l
        .replace(/^\s*(?:[-*+]|\d+\.)\s+/, '')
        .replace(/^\s*\*{1,2}[^*\n]+?:\*{1,2}\s*/, '')
        .replace(/^\s*\*{1,2}[^*\n]+?\*{1,2}:\s*/, '')
        .replace(/\*\*(.*?)\*\*/g, '$1')
        .replace(/\*(.*?)\*/g, '$1')
        .replace(/\*/g, '')
        .trim()
      )
      .filter(l => l.length > 0);
    return lines[0] || "";
  };
  if (isReverse) {
    if (card.answerReverse && card.answerReverse.trim()) {
      return card.answerReverse.trim();
    }
    const firstFront = cleanFirstField(card.front);
    if (firstFront) return firstFront;
    return (card.title || "").trim();
  } else {
    if (card.answer && card.answer.trim()) {
      return card.answer.trim();
    }
    const firstBack = cleanFirstField(card.back);
    if (firstBack) return firstBack;
    if (card.title && card.title.trim()) {
      return card.title.trim();
    }
    return "Odpověď";
  }
}

// Porovnání odpovědi znak po znaku (Anki diff)
function compareAnswers(typed, target) {
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
}

async function loadCard(idx) {
  if (idx >= studyQueue.length) {
    showFinishedView();
    return;
  }

  currentCard = studyQueue[idx];
  isCardFlipped = false;

  const isReverse = document.getElementById("chkReverseStudy").checked;
  const isQuick = document.getElementById("chkQuickReview").checked;

  const qContent = isReverse ? currentCard.back : currentCard.front;
  const aContent = isReverse ? currentCard.front : currentCard.back;

  const qBox = document.getElementById("cardQuestion");
  const aBox = document.getElementById("cardAnswer");

  qBox.innerHTML = await renderContentToHtml(qContent, currentDeck.id);
  aBox.innerHTML = await renderContentToHtml(aContent, currentDeck.id);

  await resolvePendingImages(qBox, currentDeck.id);
  await resolvePendingImages(aBox, currentDeck.id);

  aBox.style.display = "none";
  document.getElementById("ratingGrid").style.display = "none";
  document.getElementById("quickNavGrid").style.display = isQuick ? "flex" : "none";

  // Obsluha Vepisovacího vs. Otáčecího režimu
  const typeArea = document.getElementById("typeInputArea");
  const typeInput = document.getElementById("typeTextInput");
  const typeDiff = document.getElementById("typeDiffDisplay");
  const btnFlip = document.getElementById("btnFlip");

  if (cardStudyMode === "type") {
    typeArea.style.display = "flex";
    typeInput.value = "";
    typeDiff.style.display = "none";
    typeDiff.innerHTML = "";
    btnFlip.style.display = "none";
    setTimeout(() => typeInput.focus(), 50);
  } else {
    typeArea.style.display = "none";
    btnFlip.style.display = "block";
  }

  const intervals = calcNextIntervals(currentCard);
  document.getElementById("intAgain").innerText = intervals.again.text;
  document.getElementById("intHard").innerText = intervals.hard.text;
  document.getElementById("intGood").innerText = intervals.good.text;
  document.getElementById("intEasy").innerText = intervals.easy.text;

  document.getElementById("pillNew").innerText = sessionStats.newCount;
  document.getElementById("pillDue").innerText = sessionStats.dueCount;
  document.getElementById("pillDone").innerText = sessionStats.doneCount;

  document.getElementById("flashcardBox").scrollTop = 0;
}

function submitTypeAnswer() {
  if (isCardFlipped) return;
  const typeInput = document.getElementById("typeTextInput");
  const typeDiff = document.getElementById("typeDiffDisplay");
  const isReverse = document.getElementById("chkReverseStudy").checked;

  const target = extractTargetAnswer(currentCard, isReverse);
  const result = compareAnswers(typeInput.value, target);

  typeDiff.style.display = "flex";
  typeDiff.innerHTML = `
    <div><strong>Zadáno:</strong> ${result.diffHtml || '<em style="color:#f87171;">(prázdné)</em>'}</div>
    <div><strong>Správně:</strong> <span style="color:#86efac; font-weight:700;">${escapeHtml(result.target)}</span></div>
  `;

  revealAnswer();
}

function flipCard() {
  if (isCardFlipped) return;
  revealAnswer();
}

function revealAnswer() {
  isCardFlipped = true;
  document.getElementById("cardAnswer").style.display = "flex";
  document.getElementById("btnFlip").style.display = "none";

  const isQuick = document.getElementById("chkQuickReview").checked;
  if (isQuick) {
    document.getElementById("quickNavGrid").style.display = "flex";
  } else {
    document.getElementById("ratingGrid").style.display = "grid";
  }
}

async function rateCard(ratingKey) {
  if (!currentCard || !currentDeck) return;
  const intervals = calcNextIntervals(currentCard);
  const choice = intervals[ratingKey];

  const cardInDeck = currentDeck.cards.find(c => c.id === currentCard.id);
  if (cardInDeck) {
    const wasNew = !cardInDeck.due || cardInDeck.due === 0;
    cardInDeck.interval = choice.newInterval;
    cardInDeck.ease = choice.newEase;
    cardInDeck.reps = choice.newReps;
    cardInDeck.due = Date.now() + choice.ms;
    cardInDeck.state = ratingKey === "again" ? 1 : 2;

    if (wasNew && sessionStats.newCount > 0) sessionStats.newCount--;
    else if (!wasNew && sessionStats.dueCount > 0) sessionStats.dueCount--;
    sessionStats.doneCount++;

    const reviewEntry = {
      deckId: currentDeck.id,
      cardId: currentCard.id,
      timestamp: Date.now(),
      dateStr: getLocalDateString(),
      rating: ratingKey,
      interval: choice.newInterval,
      isNew: wasNew
    };

    currentDeck.history = currentDeck.history || [];
    currentDeck.history.push(reviewEntry);

    await dbAddReview(reviewEntry);
    await dbSaveDeck(currentDeck);
  }

  if (ratingKey === "again") {
    studyQueue.push(currentCard);
  }

  currentIndex++;
  loadCard(currentIndex);
}

function nextQuickCard() {
  currentIndex++;
  sessionStats.doneCount++;
  loadCard(currentIndex);
}
function prevQuickCard() {
  if (currentIndex > 0) {
    currentIndex--;
    loadCard(currentIndex);
  }
}

function showFinishedView() {
  const btnMoreNew = document.getElementById("btnStudyMoreNew");
  const msgEl = document.getElementById("finishedMsg");

  if (currentDeck) {
    const remainingUnseen = currentDeck.cards.filter(c => !c.due || c.due === 0).length;
    if (remainingUnseen > 0) {
      msgEl.innerText = `Skvělá práce! Na dnešek máte splněný denní limit nových karet i všechna opakování. V balíčku zbývá ještě ${remainingUnseen} nových kartiček pro další dny.`;
      btnMoreNew.style.display = "block";
    } else {
      msgEl.innerText = "Skvělá práce. Na dnešek máte splněné všechny naplánované kartičky v tomto balíčku.";
      btnMoreNew.style.display = "none";
    }
  }

  showView("finished");
}

function showView(view) {
  document.getElementById("decksView").style.display = view === "decks" ? "flex" : "none";
  document.getElementById("studyView").style.display = view === "study" ? "flex" : "none";
  document.getElementById("finishedView").style.display = view === "finished" ? "flex" : "none";
}

// --- MODE TOGGLES (OTÁČECÍ VS VEPISOVACÍ) ---
const btnModeFlip = document.getElementById("btnModeFlip");
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
};

// Vepisovací tlačítko a Enter
document.getElementById("btnCheckType").onclick = submitTypeAnswer;
document.getElementById("typeTextInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    if (!isCardFlipped) {
      submitTypeAnswer();
    }
  }
});

// --- EVENT HANDLERS ---
document.getElementById("btnHome").onclick = () => { showView("decks"); loadDeckList(); };
document.getElementById("btnBackToDecks").onclick = () => { showView("decks"); loadDeckList(); };
document.getElementById("btnFinishBackDecks").onclick = () => { showView("decks"); loadDeckList(); };

document.getElementById("btnFlip").onclick = flipCard;
document.getElementById("flashcardBox").onclick = (e) => {
  if (e.target.tagName === 'A' || e.target.tagName === 'IMG' || e.target.tagName === 'INPUT' || e.target.tagName === 'BUTTON') return;
  if (!isCardFlipped && cardStudyMode === "flip") flipCard();
};

document.getElementById("btnAgain").onclick = () => rateCard("again");
document.getElementById("btnHard").onclick = () => rateCard("hard");
document.getElementById("btnGood").onclick = () => rateCard("good");
document.getElementById("btnEasy").onclick = () => rateCard("easy");

document.getElementById("btnNextCard").onclick = nextQuickCard;
document.getElementById("btnPrevCard").onclick = prevQuickCard;

document.getElementById("btnStudyAllAgain").onclick = () => {
  if (currentDeck) startStudy(currentDeck.id, true);
};

document.getElementById("btnStudyMoreNew").onclick = () => {
  extraNewCardsGranted += 10;
  if (currentDeck) startStudy(currentDeck.id, false);
};

document.getElementById("chkReverseStudy").onchange = () => {
  loadCard(currentIndex);
};
document.getElementById("chkQuickReview").onchange = (e) => {
  if (currentDeck) startStudy(currentDeck.id, e.target.checked);
};

// Help Modal
document.getElementById("btnHelp").onclick = () => document.getElementById("helpModal").classList.add("active");
document.getElementById("btnHelpClose").onclick = () => document.getElementById("helpModal").classList.remove("active");
document.getElementById("helpModal").onclick = (e) => {
  if (e.target.id === "helpModal") document.getElementById("helpModal").classList.remove("active");
};

// File upload / drag & drop (podpora .zip i jednotlivých .md kartiček a obrázků)
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileZipInput");

dropZone.addEventListener("click", () => {
  fileInput.click();
});

async function handleIncomingFiles(fileList) {
  if (!fileList || fileList.length === 0) return;
  const files = Array.from(fileList);

  // 1. Zda je mezi vybranými soubory archiv .zip
  const zipFile = files.find(f => f.name.toLowerCase().endsWith('.zip') || f.type.includes('zip') || f.type === 'application/x-zip-compressed');
  if (zipFile) {
    return await importZipFile(zipFile);
  }

  // 2. Pokud uživatel vybral soubory kartiček .md a obrázky (např. z rozbalené složky na mobilu)
  const mdFiles = files.filter(f => f.name.toLowerCase().endsWith('.md') && !f.name.startsWith('00_'));
  if (mdFiles.length > 0) {
    return await importLooseFiles(files);
  }

  alert("Vyberte prosím archiv .zip s kartičkami, nebo soubory kartiček (.md) a případné obrázky.");
}

fileInput.addEventListener("change", (e) => {
  if (e.target.files && e.target.files.length > 0) {
    handleIncomingFiles(e.target.files);
    fileInput.value = "";
  }
});

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    handleIncomingFiles(e.dataTransfer.files);
  }
});

// Keyboard Shortcuts
window.addEventListener("keydown", (e) => {
  if (document.getElementById("lightbox").classList.contains("active")) {
    if (e.key === "Escape") document.getElementById("lightbox").classList.remove("active");
    return;
  }
  if (document.getElementById("helpModal").classList.contains("active")) {
    if (e.key === "Escape") document.getElementById("helpModal").classList.remove("active");
    return;
  }
  if (document.getElementById("deckStatsModal").classList.contains("active")) {
    if (e.key === "Escape") document.getElementById("deckStatsModal").classList.remove("active");
    return;
  }

  const isStudy = document.getElementById("studyView").style.display === "flex";
  if (!isStudy) return;

  // Pokud je aktivní textové pole pro vepisování a karta ještě není otočená, nezachytáváme mezerník
  if (cardStudyMode === "type" && !isCardFlipped && document.activeElement === document.getElementById("typeTextInput")) {
    return;
  }

  if (e.key === " " || e.key === "Enter") {
    e.preventDefault();
    if (!isCardFlipped) {
      if (cardStudyMode === "type") submitTypeAnswer();
      else flipCard();
    }
  } else if (e.key === "1") {
    if (isCardFlipped) rateCard("again");
  } else if (e.key === "2") {
    if (isCardFlipped) rateCard("hard");
  } else if (e.key === "3") {
    if (isCardFlipped) rateCard("good");
  } else if (e.key === "4") {
    if (isCardFlipped) rateCard("easy");
  } else if (e.key === "Escape") {
    showView("decks");
    loadDeckList();
  }
});

// Auto-check for preloaded deck data if provided via script tag
async function checkPreloadedDeck() {
  if (window.PRELOADED_DECK && window.PRELOADED_DECK.name && Array.isArray(window.PRELOADED_DECK.cards) && window.PRELOADED_DECK.cards.length > 0) {
    try {
      const existing = await dbGetDeck(window.PRELOADED_DECK.id);
      if (!existing) {
        await dbSaveDeck(window.PRELOADED_DECK);
        console.log("Preloaded deck auto-imported:", window.PRELOADED_DECK.name, "Karet:", window.PRELOADED_DECK.cards.length);
      } else {
        // Balíček již existuje: zachováme statistiky učení (interval, reps, ease, due), ale zaktualizujeme obsah
        const statMap = new Map();
        (existing.cards || []).forEach(c => {
          if (c.id) statMap.set(c.id, c);
          if (c.title) statMap.set(c.title, c);
        });
        window.PRELOADED_DECK.cards.forEach(c => {
          const s = statMap.get(c.id) || statMap.get(c.title);
          if (s) {
            if (s.interval !== undefined) c.interval = s.interval;
            if (s.reps !== undefined) c.reps = s.reps;
            if (s.ease !== undefined) c.ease = s.ease;
            if (s.due !== undefined) c.due = s.due;
            if (s.state !== undefined) c.state = s.state;
            if (s.lastReview !== undefined) c.lastReview = s.lastReview;
          }
        });
        if (existing.settings) {
          window.PRELOADED_DECK.settings = existing.settings;
        }
        await dbSaveDeck(window.PRELOADED_DECK);
        console.log("Preloaded deck updated, stats preserved:", window.PRELOADED_DECK.name);
      }
    } catch(err) {
      console.warn("Could not auto-import preloaded deck:", err);
    }
  }
}

// Initial boot
window.addEventListener("DOMContentLoaded", async () => {
  await initDB();
  await checkPreloadedDeck();
  await loadDeckList();
});
</script>

</body>
</html>
"""

final_html = html_template.replace("__JSZIP_SOURCE__", jszip_code)

output_html_path = os.path.join(BASE_DIR, "Karty.html")
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Successfully generated Karty.html at: {output_html_path} ({len(final_html.encode('utf-8'))} bytes)")
