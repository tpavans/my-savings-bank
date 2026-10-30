import os, zipfile, shutil

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>My Savings Bank</title>
<meta name="theme-color" content="#07153b">
<link rel="manifest" href="manifest.json">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="icon" type="image/png" sizes="32x32" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<style>
:root {
  box-sizing: border-box;
  padding-top: env(safe-area-inset-top, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
  --bg: #07122b;
  --card: #0c1b3f;
  --tx: #f0f4fc;
  --mu: #8ca2c9;
  --ac: #2563eb;
  --ac-glow: #3b82f6;
  --ok: #10b981;
  --bd: #162b5c;
  --cell: #102450;
  --deep-blue-base: #050d24;
  --hg: linear-gradient(135deg, #07153b 0%, #0d276b 50%, #1742a8 100%);
}
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    --bg: #edf2fa;
    --card: #ffffff;
    --tx: #0a162b;
    --mu: #576785;
    --ac: #1d4ed8;
    --ac-glow: #2563eb;
    --ok: #059669;
    --bd: #cbd8ec;
    --cell: #e0e9f8;
    --deep-blue-base: #050d24;
    --hg: linear-gradient(135deg, #07153b 0%, #0d276b 50%, #1742a8 100%);
  }
}
:root[data-theme="light"] {
  --bg: #edf2fa;
  --card: #ffffff;
  --tx: #0a162b;
  --mu: #576785;
  --ac: #1d4ed8;
  --ac-glow: #2563eb;
  --ok: #059669;
  --bd: #cbd8ec;
  --cell: #e0e9f8;
  --deep-blue-base: #050d24;
  --hg: linear-gradient(135deg, #07153b 0%, #0d276b 50%, #1742a8 100%);
}
:root[data-theme="dark"] {
  --bg: #050d22;
  --card: #0a1738;
  --tx: #f0f4fc;
  --mu: #8ca2c9;
  --ac: #3b82f6;
  --ac-glow: #60a5fa;
  --ok: #10b981;
  --bd: #152959;
  --cell: #0f224f;
  --deep-blue-base: #04091a;
  --hg: linear-gradient(135deg, #061335 0%, #0a205a 50%, #12348a 100%);
}
* { box-sizing: border-box; }
html { scroll-padding-top: env(safe-area-inset-top, 0px); }
body {
  margin: 0;
  background: var(--bg);
  color: var(--tx);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  padding: 16px;
  padding-bottom: 96px; /* Space for bottom nav bar */
  max-width: 560px;
  margin-inline: auto;
  transition: background 0.3s, color 0.3s;
}
h1 { font-size: 20px; margin: 4px 0 2px; }
.sub { color: var(--mu); font-size: 13px; margin-bottom: 12px; }
.card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 18px;
  padding: 18px;
  margin-bottom: 14px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}
.big { font-size: 38px; font-weight: 800; color: var(--ok); }
.row { display: flex; gap: 10px; flex-wrap: wrap; }
.stat { flex: 1; min-width: 100px; }
.stat b { display: block; font-size: 18px; font-weight: 700; }
.stat span { font-size: 12px; color: var(--mu); }
.bar { height: 12px; background: var(--cell); border-radius: 8px; overflow: hidden; margin: 12px 0 6px; }
.bar i { display: block; height: 100%; background: linear-gradient(90deg, var(--ac), var(--ok)); width: 0; transition: width .4s ease; }
input {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
  font-size: 16px;
  outline: none;
  transition: border-color 0.2s;
}
input:focus { border-color: var(--ac); }
label { font-size: 12px; color: var(--mu); display: block; margin-bottom: 4px; font-weight: 600; }
button {
  padding: 12px 16px;
  border: 0;
  border-radius: 12px;
  background: var(--ac);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  width: 100%;
  margin-top: 10px;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}
button:active { transform: scale(0.98); }
#tabs { display: flex; gap: 8px; overflow-x: auto; margin-bottom: 14px; padding-bottom: 4px; }
.tab, .chips button {
  width: auto;
  margin: 0;
  padding: 8px 14px;
  border-radius: 20px;
  background: var(--cell);
  color: var(--tx);
  font-size: 14px;
  white-space: nowrap;
  flex: none;
  border: 1px solid var(--bd);
}
.tab.on { background: var(--ac); color: #fff; border-color: var(--ac); }
.grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 5px; margin-top: 10px; }
.c {
  aspect-ratio: 1;
  border-radius: 6px;
  background: var(--cell);
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--mu);
}
.c.s { background: var(--ok); color: #fff; font-weight: 600; }
.c.t { outline: 2px solid var(--ac); }
.e { display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 10px 0; border-bottom: 1px solid var(--bd); font-size: 14px; }
.e:last-child { border: 0; }
.e button { width: auto; margin: 0; padding: 6px 10px; font-size: 13px; background: transparent; color: var(--mu); border: 1px solid var(--bd); }
.hint { font-size: 13px; color: var(--mu); margin-top: 8px; }
.small { font-size: 12px; color: var(--mu); cursor: pointer; text-decoration: underline; margin-right: 14px; }
.amtbox { text-align: center; margin: 6px 0; }
.amtbox span { font-size: 28px; color: var(--mu); }
.amtbox b { font-size: 52px; margin-left: 4px; }
.to { text-align: center; font-size: 13px; color: var(--mu); }
.to b { color: var(--tx); }
.chips { display: flex; gap: 8px; justify-content: center; margin: 10px 0; flex-wrap: wrap; }
.keys { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 8px 0; }
.keys button {
  margin: 0;
  width: auto;
  background: var(--bg);
  color: var(--tx);
  border: 1px solid var(--bd);
  font-size: 22px;
  padding: 14px 0;
  border-radius: 12px;
}
#nf { display: none; }
#nf.on { display: block; }
#nf .chips { justify-content: flex-start; }
#ok {
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at center, #059669 0%, #065f46 100%);
  color: #fff;
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  z-index: 900;
  padding: 24px;
  overflow: hidden;
}
#ok.on { display: flex; }
#ok .tick {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: #fff;
  color: #059669;
  font-size: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pop .5s;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}
#ok .a { font-size: 44px; font-weight: 800; margin: 16px 0 4px; }
#ok button { background: #fff; color: #065f46; width: auto; padding: 12px 40px; margin-top: 28px; position: relative; z-index: 2; border-radius: 24px; }
.pig { position: absolute; bottom: calc(20px + env(safe-area-inset-bottom, 0px)); font-size: 64px; animation: bob .6s ease-in-out infinite alternate; }
.fall { position: absolute; top: -50px; font-size: 30px; pointer-events: none; animation: fall linear forwards; }
#ai .out { white-space: pre-wrap; font-size: 14px; line-height: 1.6; margin-top: 12px; }
#jar {
  position: relative;
  width: 62px;
  height: 72px;
  border: 3px solid var(--ac);
  border-radius: 14px 14px 22px 22px;
  overflow: hidden;
  background: var(--cell);
}
#jar i { position: absolute; bottom: 0; left: 0; right: 0; height: 0; background: linear-gradient(#ffd54a, #ffb300); transition: height .6s; }
#jar span { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 32px; }
:root[data-acc="sun"] { --ac: #ff6a3d; --hg: linear-gradient(135deg, #ff6a3d, #ff9f1c); }
:root[data-acc="forest"] { --ac: #0f9d58; --hg: linear-gradient(135deg, #0b6e4f, #12b76a); }
#pile { display: flex; flex-direction: column-reverse; align-items: center; min-width: 92px; height: 84px; justify-content: flex-start; line-height: 1.05; }
#pile div { display: flex; justify-content: center; }
#pile span { font-size: 21px; display: inline-block; }
#pile .em { font-size: 12px; color: var(--mu); align-self: center; text-align: center; }
@keyframes pp { from { transform: scale(0) translateY(-20px); } to { transform: scale(1); } }
#wdo {
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at center, #dc2626 0%, #991b1b 100%);
  color: #fff;
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  z-index: 900;
  padding: 24px;
  overflow: hidden;
}
#wdo.on { display: flex; }
.wdi { width: 88px; height: 88px; border-radius: 50%; background: #fff; color: #dc2626; font-size: 44px; display: flex; align-items: center; justify-content: center; animation: pop .5s; }
#wdo button { background: #fff; color: #991b1b; width: auto; padding: 12px 40px; margin-top: 28px; position: relative; z-index: 2; border-radius: 24px; }
.fly { position: absolute; bottom: -50px; font-size: 30px; pointer-events: none; animation: fly linear forwards; }
@keyframes fly { to { transform: translateY(-115vh) rotate(-35deg); } }
textarea { font-family: inherit; font-size: 13px; }
select {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
  font-size: 15px;
  outline: none;
}
table.pb { width: 100%; border-collapse: collapse; font-size: 12px; }
table.pb td, table.pb th { padding: 8px 4px; border-bottom: 1px solid var(--bd); text-align: left; }
.cr { color: var(--ok); font-weight: 600; }
.dr { color: #f04438; font-weight: 600; }
#ga { position: relative; height: 200px; background: var(--bg); border-radius: 14px; margin: 10px 0; overflow: hidden; border: 1px solid var(--bd); }
#ga span { position: absolute; font-size: 30px; cursor: pointer; user-select: none; }
.ach { padding: 6px 12px; border-radius: 14px; background: var(--cell); font-size: 12px; border: 1px solid var(--bd); }
.ach.off { opacity: .35; filter: grayscale(1); }

/* Deep Blue Base Headers and Auth */
.hd {
  background: var(--hg, linear-gradient(135deg, #07153b 0%, #0d276b 50%, #1742a8 100%));
  color: #fff;
  border-radius: 22px;
  padding: 20px;
  margin-bottom: 14px;
  box-shadow: 0 10px 30px rgba(7, 21, 59, 0.45);
  border: 1px solid rgba(75, 135, 255, 0.22);
}
.hb { font-size: 36px; font-weight: 800; letter-spacing: -0.5px; }

#auth {
  position: fixed;
  inset: 0;
  background: radial-gradient(ellipse at 50% 25%, #102c78 0%, #07153b 50%, #030818 100%);
  color: #fff;
  z-index: 1000;
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  overflow: auto;
}
#auth.on { display: flex; }
#auth .bx { width: 100%; max-width: 380px; }
#auth input { margin-bottom: 10px; background: rgba(255, 255, 255, 0.95); color: #0a162b; font-weight: 500; }
#auth button.g {
  background: linear-gradient(135deg, #38bdf8, #2563eb);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
}
#auth .l { background: none; border: 0; color: #93c5fd; text-decoration: underline; font-size: 14px; font-weight: 400; margin-top: 6px; }
#pin { display: none; }

#lock {
  position: fixed;
  inset: 0;
  background: radial-gradient(ellipse at 50% 25%, #102c78 0%, #07153b 50%, #030818 100%);
  color: #fff;
  z-index: 950;
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#lock.on { display: flex; }
.dots { display: flex; gap: 14px; margin: 18px; }
.dots i { width: 14px; height: 14px; border-radius: 50%; border: 2px solid #fff; }
.dots i.f { background: #fff; box-shadow: 0 0 10px #fff; }
.lk { display: grid; grid-template-columns: repeat(3, 76px); gap: 12px; }
.lk button { margin: 0; width: 76px; height: 76px; border-radius: 50%; background: rgba(255, 255, 255, 0.14); font-size: 26px; padding: 0; border: 1px solid rgba(255, 255, 255, 0.2); }

@keyframes fall { to { transform: translateY(115vh) rotate(420deg); } }
@keyframes bob { to { transform: translateY(-12px) scale(1.08); } }
@keyframes pop { 0% { transform: scale(0); } 70% { transform: scale(1.15); } 100% { transform: scale(1); } }

/* ==========================================================
   APP VIEWS & BOTTOM NAVIGATION BAR
========================================================== */
.app-view {
  display: none;
  animation: viewFade 0.22s ease-in-out;
}
.app-view.on {
  display: block;
}
@keyframes viewFade {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

#bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 560px;
  margin-inline: auto;
  background: rgba(7, 21, 59, 0.94);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-top: 1px solid rgba(255, 255, 255, 0.14);
  display: flex;
  justify-content: space-around;
  padding: 6px 4px calc(6px + env(safe-area-inset-bottom, 0px));
  z-index: 500;
  box-shadow: 0 -8px 25px rgba(0, 0, 0, 0.45);
}
.nav-btn {
  background: transparent;
  border: 0;
  color: var(--mu);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 6px 10px;
  border-radius: 12px;
  cursor: pointer;
  margin: 0;
  width: auto;
  font-size: 11px;
  font-weight: 600;
  transition: all 0.2s ease;
  user-select: none;
}
.nav-btn .icon {
  font-size: 20px;
  transition: transform 0.2s ease;
}
.nav-btn.on {
  color: #60a5fa;
  background: rgba(37, 99, 235, 0.2);
}
.nav-btn.on .icon {
  transform: translateY(-2px) scale(1.15);
}

/* Voice Entry Button under Pay to Savings */
.voice-entry-btn {
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
  color: #fff !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  margin-top: 8px !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
  border: 1px solid rgba(96, 165, 250, 0.3) !important;
}
.voice-entry-btn:active {
  transform: scale(0.98);
}

/* Goal Color Palette Bar */
.color-bar-container {
  margin: 10px 0;
}
.color-palette-bar {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 8px 4px;
  scrollbar-width: none;
}
.color-palette-bar::-webkit-scrollbar { display: none; }
.color-swatch {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex: none;
  cursor: pointer;
  border: 3px solid transparent;
  box-shadow: 0 3px 8px rgba(0,0,0,0.3);
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #fff;
  font-weight: 800;
}
.color-swatch:hover {
  transform: scale(1.12);
}
.color-swatch.active {
  border-color: #ffffff;
  box-shadow: 0 0 14px rgba(255,255,255,0.7), 0 4px 10px rgba(0,0,0,0.4);
  transform: scale(1.18);
}

/* Opening Splash Animation */
#splash-screen {
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: radial-gradient(ellipse at 50% 30%, #102c78 0%, #07153b 45%, #030818 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: #fff;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  user-select: none;
  transition: opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
#splash-screen.hide {
  opacity: 0;
  transform: scale(1.08);
  pointer-events: none;
}
.splash-ambient-glow {
  position: absolute;
  width: 440px;
  height: 440px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.35) 0%, rgba(245, 197, 24, 0.16) 45%, rgba(0, 0, 0, 0) 70%);
  filter: blur(40px);
  animation: splashGlowPulse 3s ease-in-out infinite alternate;
  pointer-events: none;
}
@keyframes splashGlowPulse {
  0% { transform: scale(0.85); opacity: 0.6; }
  100% { transform: scale(1.2); opacity: 1; }
}
.splash-particles {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}
.splash-coin {
  position: absolute;
  pointer-events: none;
  animation: splashCoinFloat linear forwards;
}
@keyframes splashCoinFloat {
  0% { transform: translateY(110vh) rotate(0deg) scale(0.6); opacity: 0; }
  15% { opacity: 0.85; }
  85% { opacity: 0.85; }
  100% { transform: translateY(-10vh) rotate(360deg) scale(1.1); opacity: 0; }
}
.splash-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 90vw;
  width: 360px;
}
.splash-logo-wrapper {
  position: relative;
  width: 140px;
  height: 140px;
  margin-bottom: 22px;
  animation: splashLogoDrop 0.9s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
@keyframes splashLogoDrop {
  0% { transform: scale(0.2) translateY(-70px) rotate(-8deg); opacity: 0; }
  70% { transform: scale(1.08) translateY(6px) rotate(2deg); opacity: 1; }
  100% { transform: scale(1) translateY(0) rotate(0deg); opacity: 1; }
}
.splash-logo-ring {
  position: absolute;
  inset: -8px;
  border-radius: 36px;
  border: 2px solid rgba(255, 215, 0, 0.45);
  box-shadow: 0 0 24px rgba(255, 215, 0, 0.3), inset 0 0 15px rgba(59, 130, 246, 0.4);
  animation: splashRingSpin 14s linear infinite;
}
@keyframes splashRingSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.splash-logo-img {
  width: 100%;
  height: 100%;
  border-radius: 30px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.55), 0 0 24px rgba(37, 99, 235, 0.45);
  object-fit: cover;
  animation: splashFloatBob 3s ease-in-out infinite alternate 0.9s;
}
@keyframes splashFloatBob {
  0% { transform: translateY(0); }
  100% { transform: translateY(-7px); }
}
.splash-shine {
  position: absolute;
  top: 0;
  left: -120%;
  width: 60%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transform: skewX(-25deg);
  animation: splashShinePass 3.5s infinite 1.2s;
  pointer-events: none;
}
@keyframes splashShinePass {
  0% { left: -120%; }
  35%, 100% { left: 180%; }
}
.splash-title-box {
  animation: splashFadeInSlideUp 0.8s ease 0.35s both;
}
@keyframes splashFadeInSlideUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}
.splash-title {
  margin: 0;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #ffffff 20%, #ffe082 60%, #ffd54f 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 4px 18px rgba(255, 213, 79, 0.25);
}
.splash-badge {
  display: inline-block;
  margin-top: 6px;
  padding: 4px 14px;
  border-radius: 20px;
  background: rgba(37, 99, 235, 0.35);
  border: 1px solid rgba(96, 165, 250, 0.4);
  font-size: 12px;
  font-weight: 600;
  color: #bfdbfe;
  letter-spacing: 0.3px;
}
.splash-tagline {
  margin: 8px 0 18px;
  font-size: 13px;
  color: #93c5fd;
  opacity: 0.9;
  line-height: 1.4;
}
.splash-loader-box {
  width: 100%;
  max-width: 260px;
  margin-top: 4px;
  animation: splashFadeInSlideUp 0.8s ease 0.5s both;
}
.splash-progress-track {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.4);
}
.splash-progress-bar {
  width: 0%;
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #38bdf8, #facc15);
  border-radius: 8px;
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.8);
  transition: width 0.18s linear;
}
.splash-status {
  margin-top: 10px;
  font-size: 12px;
  color: #94a3b8;
  letter-spacing: 0.2px;
  min-height: 18px;
}
.splash-skip-btn {
  margin-top: 20px;
  padding: 9px 26px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #e2e8f0;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  width: auto;
  transition: all 0.2s;
  backdrop-filter: blur(8px);
}
.splash-skip-btn:hover {
  background: rgba(255, 255, 255, 0.22);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
}
</style>
</head>
<body>

<!-- Showstopping Opening Splash Animation Screen -->
<div id="splash-screen">
  <div class="splash-ambient-glow"></div>
  <div class="splash-particles" id="splash-particles"></div>
  
  <div class="splash-content">
    <div class="splash-logo-wrapper">
      <div class="splash-logo-ring"></div>
      <img src="icon-512.png" alt="My Savings Bank" class="splash-logo-img">
      <div class="splash-shine"></div>
    </div>
    
    <div class="splash-title-box">
      <h1 class="splash-title">My Savings Bank</h1>
      <div class="splash-badge">నమ్మకమైన పొదుపు · Smart Savings</div>
      <p class="splash-tagline">Save smart, dream big & reach your financial goals!</p>
    </div>
    
    <div class="splash-loader-box">
      <div class="splash-progress-track">
        <div class="splash-progress-bar" id="splash-progress-bar"></div>
      </div>
      <div class="splash-status" id="splash-status">Opening your vault...</div>
    </div>
    
    <button class="splash-skip-btn" id="splash-skip-btn">Start Saving ➔</button>
  </div>
</div>

<!-- Header (Always Visible) -->
<div class="hd">
  <div style="display:flex;justify-content:space-between;align-items:center;font-size:14px;opacity:.95">
    <span style="display:inline-flex;align-items:center;gap:8px;font-weight:700">
      <img src="icon-192.png" alt="App Icon" style="width:30px;height:30px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.35);vertical-align:middle;object-fit:cover;border:1px solid rgba(255,255,255,0.25)">
      <span>My Savings Bank</span>
    </span>
    <span style="display:flex;align-items:center;gap:4px">
      <span id="clk"></span>
      <button id="btn-replay-splash" title="Replay Opening Animation" style="width:auto;margin:0;padding:3px 9px;background:rgba(255,255,255,.2);border-radius:8px;font-size:13px;border:1px solid rgba(255,255,255,0.25)">✨ Splash</button>
      <button id="eye" title="Hide/Show Balance" style="width:auto;margin:0;padding:3px 8px;background:rgba(255,255,255,.2);border-radius:8px;font-size:13px;border:1px solid rgba(255,255,255,0.25)">👁️</button>
    </span>
  </div>
  <div style="font-size:12px;opacity:.8;margin-top:14px;letter-spacing:0.3px">Total savings (అన్ని గోల్స్ కలిపి)</div>
  <div class="hb" id="all">₹0</div>
  <div style="font-size:12px;opacity:.85;margin-top:6px" id="who"></div>
</div>

<!-- ==========================================================
     VIEW 1: HOME (Goals, Balance, Pay to Savings & Voice Entry)
========================================================== -->
<div id="view-home" class="app-view on">
  <div id="tabs"></div>

  <div class="card" id="nf">
    <b>Kotha savings goal</b>
    <div class="chips" id="pre"></div>
    <div class="row">
      <div style="flex:3"><label>Name</label><input id="nn" placeholder="e.g. Goa Trip"></div>
      <div style="flex:1;min-width:70px"><label>Emoji</label><input id="ne" value="🎯"></div>
    </div>
    <div class="row" style="margin-top:8px">
      <div style="flex:1"><label>Target ₹</label><input id="nt" type="number" inputmode="decimal"></div>
      <div style="flex:1"><label>Days (0 = no deadline)</label><input id="nd" type="number" inputmode="numeric" value="0"></div>
    </div>
    <button id="mk">Create goal</button>
  </div>

  <div class="card">
    <div style="font-size:13px;color:var(--mu)" id="gname"></div>
    <div style="display:flex;justify-content:space-between;align-items:center"><div class="big" id="total">₹0</div><div id="pile"></div></div>
    <div class="bar"><i id="pb"></i></div>
    <div class="hint" id="pct"></div><a id="rch" href="https://www.jio.com/selfcare/recharge/mobility/" target="_blank" rel="noopener" style="display:none;margin-top:10px;padding:12px;border-radius:10px;background:var(--ok);color:#fff;text-align:center;font-weight:600;text-decoration:none">🔄 Recharge now (Jio)</a>
    <div class="row" style="margin-top:14px">
      <div class="stat"><b id="rem">₹0</b><span>Inka kavali</span></div>
      <div class="stat"><b id="day">-</b><span>Plan day</span></div>
      <div class="stat"><b id="today">₹0</b><span>Ee roju saved</span></div>
    </div>
    <div class="hint" id="need"></div>
  </div>

  <div class="card">
    <div class="to">Paying to <b id="payto"></b></div>
    <div class="amtbox"><span>₹</span><b id="disp">0</b></div>
    <input id="amt" type="hidden">
    <div class="chips" id="q"><button data-q="5">+5</button><button data-q="10">+10</button><button data-q="20">+20</button><button data-q="50">+50</button><button data-q="100">+100</button></div>
    <div class="keys"><button data-k="1">1</button><button data-k="2">2</button><button data-k="3">3</button><button data-k="4">4</button><button data-k="5">5</button><button data-k="6">6</button><button data-k="7">7</button><button data-k="8">8</button><button data-k="9">9</button><button data-k=".">.</button><button data-k="0">0</button><button data-k="del">⌫</button></div>
    <div class="row">
      <div style="flex:2"><label>Note</label><input id="note" placeholder="e.g. chai money save"></div>
      <div style="flex:1.3"><label>Date</label><input id="dt" type="date"></div>
      <div style="flex:1.3"><label>Time</label><input id="tm" type="time"></div>
    </div>
    <div class="row" style="margin-top:8px"><select id="src" style="flex:1"><option>💵 Cash</option><option>📲 UPI</option><option>🏦 Bank</option></select><select id="md" style="flex:1"><option>😀</option><option>😐</option><option>😞</option></select></div>
    
    <!-- Primary Pay to Savings Button -->
    <button id="add">Pay to Savings ✅</button>
    
    <!-- Voice Entry Button directly under Pay to Savings -->
    <button id="vb_quick" type="button" class="voice-entry-btn">
      <span style="font-size:18px">🎤</span>
      <span>Voice Entry (నోటితో చెప్పి Add చేయండి)</span>
    </button>
  </div>

  <div class="card">
    <div class="row"><div class="stat"><b id="stk">0</b><span>Streak</span></div><div class="stat"><b id="lvl">-</b><span>Level</span></div><div class="stat"><b id="bst">₹0</b><span>Best day</span></div></div>
    <div class="bar"><i id="dpb"></i></div><div class="hint" id="dtx"></div><div class="hint" id="qt" style="font-style:italic"></div>
    <div class="row"><button id="qs" style="flex:1">⚡ Quick save</button><button id="ns" style="flex:1;background:var(--cell);color:var(--tx)">🎲 No-spend day</button></div>
  </div>
</div>

<!-- ==========================================================
     VIEW 2: HISTORY (Charts, Calendar, Passbook, Day List)
========================================================== -->
<div id="view-history" class="app-view">
  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <b>📊 Savings chart</b>
      <span><button id="c7" class="tab" style="padding:4px 12px">7d</button> <button id="c30" class="tab" style="padding:4px 12px">30d</button></span>
    </div>
    <div id="chart" style="display:flex;gap:2px;align-items:flex-end;height:140px;margin-top:12px"></div>
  </div>

  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <button id="cp" class="tab">‹</button><b id="cmt"></b><button id="cn" class="tab">›</button>
    </div>
    <div class="grid" style="grid-template-columns:repeat(7,1fr);margin-top:8px;text-align:center;font-size:10px;color:var(--mu)"><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
    <div class="grid" id="cal" style="grid-template-columns:repeat(7,1fr);margin-top:4px"></div>
    <div class="hint">🟩 saved · 🟦 no-spend · 🟥 missed</div>
  </div>

  <div class="card">
    <b>🧾 Passbook</b>
    <div class="row" style="margin:8px 0">
      <input id="pq" placeholder="Search date / note / amount" style="flex:2">
      <button id="ud" style="flex:1;margin:0;background:var(--cell);color:var(--tx)">↩️ Undo</button>
    </div>
    <div style="overflow-x:auto"><table class="pb" id="pbt"></table></div>
  </div>

  <div class="card" id="gc"><b>Days tracker</b><div class="grid" id="grid"></div></div>
  <div class="card"><b>Day-wise History</b><div id="list"></div></div>

  <div class="card">
    <b>📈 Report &amp; Backup</b>
    <div class="row"><button id="rpb" style="flex:1">This month report</button><button id="bkb" style="flex:1;background:var(--cell);color:var(--tx)">Backup</button></div>
    <div class="hint" id="rp" style="white-space:pre-wrap;color:var(--tx)"></div>
    <textarea id="bk" rows="3" placeholder="Backup data ikkada vasthundi. Restore ki paste chesi Restore nokku" style="width:100%;margin-top:8px;border-radius:10px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);padding:8px"></textarea>
    <button id="rsb" style="background:var(--cell);color:var(--tx)">Restore</button>
  </div>
</div>

<!-- ==========================================================
     VIEW 3: TOOLS (Round-up, Withdraw, Calculators, Split, Notes)
========================================================== -->
<div id="view-tools" class="app-view">
  <div class="card">
    <b>🧰 Savings Tools</b>
    <label style="margin-top:10px">🪙 Round-up: kharchu chesina amount ₹</label>
    <div class="row"><input id="rs" type="number" inputmode="decimal" placeholder="e.g. 47" style="flex:1"><button id="rb" style="flex:1;margin:0;width:auto">Round-up save</button></div>
    <label style="margin-top:12px">💸 Withdraw / Spend ₹ (goal nundi teesukunte)</label>
    <div class="row"><input id="wa" type="number" inputmode="decimal" placeholder="Amount" style="flex:1"><input id="wn" placeholder="Reason" style="flex:2"></div><button id="wb" style="background:#f04438">Withdraw</button>
    <label style="margin-top:12px">🧮 What-if: roju ₹ / entha rojulu</label>
    <div class="row"><input id="wp" type="number" inputmode="decimal" placeholder="₹ per day" style="flex:1"><input id="wdn" type="number" inputmode="numeric" value="56" style="flex:1"></div><div class="hint" id="wr"></div>
  </div>

  <div class="card">
    <b>💱 Savings split</b>
    <div class="row" style="margin-top:8px"><input id="spa" type="number" inputmode="decimal" placeholder="Total ₹ amount"></div>
    <div id="spl"></div>
    <button id="spb">Split & save</button>
    <div class="hint" id="spm"></div>
  </div>

  <div class="card">
    <b>📒 Money notes</b>
    <div class="row" style="margin-top:8px"><select id="nt" style="flex:1.2"><option value="lend">🤝 Lend (ichanu)</option><option value="borrow">🙏 Borrow (teesukunna)</option><option value="earn">💼 Earning</option><option value="cpn">🎁 Coupon / offer</option></select><input id="ntx" placeholder="Name / source" style="flex:1.5"></div>
    <div class="row" style="margin-top:8px"><input id="nam" type="number" inputmode="decimal" placeholder="₹" style="flex:1"><input id="ndt" type="date" style="flex:1.3"></div>
    <button id="nad">Add</button>
    <div id="nl"></div>
  </div>

  <div class="card">
    <b>🧮 Financial Calculators</b>
    <label style="margin-top:10px">💰 Budget 50/30/20: monthly income ₹</label><input id="bi" type="number" inputmode="decimal"><div class="hint" id="br"></div>
    <label style="margin-top:10px">📈 Interest (RD): ₹/month · rate % · months</label><div class="row"><input id="ia" type="number" placeholder="₹/month" style="flex:1"><input id="ir" type="number" value="6.5" style="flex:1"><input id="im" type="number" value="12" style="flex:1"></div><div class="hint" id="ires"></div>
    <label style="margin-top:10px">🔄 Plan compare: price ₹ for 28 / 56 / 84 days</label><div class="row"><input id="p28" type="number" placeholder="28d ₹" style="flex:1"><input id="p56" type="number" placeholder="56d ₹" style="flex:1"><input id="p84" type="number" placeholder="84d ₹" style="flex:1"></div><div class="hint" id="pcr"></div>
  </div>
</div>

<!-- ==========================================================
     VIEW 4: AI & FUN (AI Coach, Games, Spin, Challenges, Insights)
========================================================== -->
<div id="view-fun" class="app-view">
  <div class="card" id="ai">
    <b>🤖 AI Money Coach</b>
    <div class="hint">Roju entha save/earn cheyyalo, ela cheyyalo AI cheptundi.</div>
    <label style="margin-top:10px">Nee situation (optional)</label>
    <input id="aic" placeholder="e.g. student, evenings free, laptop undi">
    <button id="aib">💡 Ideas generate chey</button>
    <button id="aik" style="background:var(--cell);color:var(--tx)">🔍 Spending leak finder</button>
    <button id="aiw" style="background:var(--cell);color:var(--tx)">📝 AI weekly review</button>
    <button id="aip" style="background:var(--cell);color:var(--tx)">📶 AI plan advisor</button>
    <div class="out" id="aio"></div>
  </div>

  <div class="card">
    <b>🕹️ Coin catch game</b>
    <div class="hint" id="gt">15 sec lo coins tap chey!</div>
    <div id="ga"></div>
    <button id="gs">▶ Start</button>
  </div>

  <div class="card">
    <b>🎰 Daily spin & challenges</b>
    <div class="row" style="margin-top:10px"><button id="sp" style="flex:1;margin:0">🎰 Spin</button><select id="ch" style="flex:2"><option value="">Challenge select chey</option><option value="ten">₹10 daily × 30 days</option><option value="inc">₹1 → ₹2 → ₹3 increasing</option><option value="w52">52-week challenge</option><option value="coin">Coin jar (₹1/₹2/₹5 matrame)</option></select></div>
    <div class="hint" id="spr" style="color:var(--tx)"></div>
    <button id="chb" style="display:none">Do today challenge</button>
  </div>

  <div class="card">
    <b>🧠 Smart insights</b>
    <div class="hint" id="sm" style="white-space:pre-wrap;color:var(--tx);line-height:1.7"></div>
    <div class="row"><button id="fz" style="flex:1;background:var(--cell);color:var(--tx)">🧊 Streak freeze</button><button id="yr" style="flex:1;background:var(--cell);color:var(--tx)">📅 Year review</button></div>
    <div class="hint" id="yrt" style="white-space:pre-wrap;color:var(--tx)"></div>
  </div>

  <div class="card">
    <b>🏅 Achievements</b>
    <div id="ach" class="chips" style="justify-content:flex-start;margin-bottom:0"></div>
  </div>
</div>

<!-- ==========================================================
     VIEW 5: SETTINGS (Goal Color Bar, Rules, Theme, PIN, Profile)
========================================================== -->
<div id="view-settings" class="app-view">
  <!-- Goal Colors Palette Bar with More Vibrant Colors -->
  <div class="card">
    <b>🎨 Goal Colors (రంగుల ఎంపిక)</b>
    <div class="hint">మీ ప్రస్తుత Goal కి నచ్చిన Color Palette ని ఎంచుకోండి:</div>
    <div class="color-bar-container">
      <div id="color-bar" class="color-palette-bar"></div>
    </div>
    <div class="row" style="margin-top:8px;align-items:center">
      <div style="flex:1.2">
        <label>Custom Color</label>
        <input id="gcol" type="color" style="padding:2px;height:44px;border-radius:10px;cursor:pointer">
      </div>
      <div style="flex:1.2">
        <label>Daily limit ₹</label>
        <input id="lm" type="number" inputmode="decimal">
      </div>
      <div style="flex:1.2">
        <label>Lock withdraw</label>
        <input id="lk" type="date">
      </div>
    </div>
  </div>

  <div class="card">
    <b>🎯 Goal Settings</b>
    <div class="row">
      <div style="flex:1"><label>Start date</label><input id="st" type="date"></div>
      <div style="flex:1"><label>Target ₹</label><input id="tg" type="number" inputmode="decimal"></div>
      <div style="flex:1"><label>Days (0 = none)</label><input id="sd" type="number" inputmode="numeric"></div>
    </div>
    <div class="hint" style="margin-top:14px">
      <span class="small" id="reset">Clear this goal entries</span>
      <span class="small" id="del">Delete this goal</span>
      <span class="small" id="pin">Set app PIN</span>
      <span class="small" id="lo">Logout</span>
    </div>
  </div>

  <div class="card">
    <b>🌓 Appearance & Accent</b>
    <div class="chips" style="justify-content:flex-start;margin-top:8px"><button id="thm" class="tab">🌗 Auto</button></div>
    <div class="chips" id="acc" style="justify-content:flex-start;margin-top:0"><button data-a="def">🔵 Deep Blue</button><button data-a="sun">🌅 Sunset ₹100🔒</button><button data-a="forest">🌲 Forest ₹500🔒</button></div>
  </div>

  <div class="card">
    <b>⚙️ Quick Controls</b>
    <div class="row" style="margin-top:8px">
      <button id="snd" style="flex:1;margin:0;background:var(--cell);color:var(--tx)">🔊 Sound on</button>
      <button id="bt" style="flex:1;margin:0;background:var(--cell);color:var(--tx)">🔠 Big text</button>
      <button id="vb" style="flex:1;margin:0;background:var(--cell);color:var(--tx)">🎤 Voice test</button>
    </div>
    <button id="chk-update" style="margin-top:10px;background:linear-gradient(135deg,#059669,#10b981);display:flex;align-items:center;justify-content:center;gap:8px">
      <span>🔄</span> Check & Install Update (యాప్ అప్‌డేట్ చేయండి)
    </button>
  </div>
</div>

<!-- ==========================================================
     BOTTOM NAVIGATION BAR (Stops Lengthy Scrolling)
========================================================== -->
<nav id="bottom-nav">
  <button class="nav-btn on" data-target="view-home">
    <span class="icon">🏠</span>
    <span>Home</span>
  </button>
  <button class="nav-btn" data-target="view-history">
    <span class="icon">📊</span>
    <span>History</span>
  </button>
  <button class="nav-btn" data-target="view-tools">
    <span class="icon">🧰</span>
    <span>Tools</span>
  </button>
  <button class="nav-btn" data-target="view-fun">
    <span class="icon">🤖</span>
    <span>AI & Fun</span>
  </button>
  <button class="nav-btn" data-target="view-settings">
    <span class="icon">⚙️</span>
    <span>Settings</span>
  </button>
</nav>

<!-- Overlays: Withdraw & Auth & Lock & Success -->
<div id="wdo"><div class="wdi">💸</div><div style="font-size:20px;font-weight:600;margin-top:14px">Money Withdrawn</div><div style="font-size:44px;font-weight:700;margin:12px 0 4px" id="wdamt"></div><div id="wdbal"></div><button id="wdd">Done</button></div>

<div id="auth"><div class="bx">
  <div style="text-align:center;margin-bottom:12px">
    <img src="icon-512.png" alt="My Savings Bank Logo" style="width:84px;height:84px;border-radius:22px;box-shadow:0 10px 24px rgba(0,0,0,0.5),0 0 20px rgba(37,99,235,0.4);border:2px solid rgba(255,215,0,0.4)">
  </div>
  <h1 style="text-align:center;margin:6px 0 4px;font-size:24px;font-weight:800;background:linear-gradient(135deg,#ffffff 20%,#ffe082 60%,#ffd54f 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent">My Savings Bank</h1>
  <div style="text-align:center;font-size:12px;color:#93c5fd;margin-bottom:18px">మీ వ్యక్తిగత పొదుపు సహాయకుడు · Secure Vault</div>
  <input id="anm" placeholder="Nee peru (name)" style="display:none">
  <div style="display:flex;gap:8px"><input value="+91" disabled style="width:70px;text-align:center"><input id="amob" type="tel" inputmode="numeric" maxlength="10" placeholder="Mobile number"></div>
  <input id="apin" type="password" inputmode="numeric" maxlength="4" placeholder="4-digit PIN">
  <div id="amsg" style="min-height:20px;font-size:13px;margin-bottom:6px"></div>
  <button id="ago" class="g">Login</button>
  <div style="text-align:center"><button class="l" id="asw">Kotha account? Register</button><br><button class="l" id="afg">PIN marchipoyava?</button></div>
</div></div>

<div id="lock">
  <div style="text-align:center;margin-bottom:12px">
    <img src="icon-192.png" alt="Lock Logo" style="width:68px;height:68px;border-radius:18px;box-shadow:0 8px 20px rgba(0,0,0,0.45);border:1.5px solid rgba(255,215,0,0.4)">
  </div>
  <div style="font-size:16px;font-weight:600;letter-spacing:0.3px">App Locked · Enter PIN</div>
  <div class="dots" id="dots"></div>
  <div id="lmsg" class="hint" style="color:#fca5a5;margin:0 0 14px"></div>
  <div class="lk" id="lk"><button data-k="1">1</button><button data-k="2">2</button><button data-k="3">3</button><button data-k="4">4</button><button data-k="5">5</button><button data-k="6">6</button><button data-k="7">7</button><button data-k="8">8</button><button data-k="9">9</button><span></span><button data-k="0">0</button><button data-k="x">⌫</button></div>
</div>

<div id="ok"><div class="tick">✓</div><div class="ttl">Payment Successful</div><div class="a" id="okamt"></div><div id="okmsg"></div><div class="hint" id="oktx" style="color:#fff;opacity:.85"></div><button id="okd">Done</button><div class="pig">🐷</div></div>

<script>
const $=id=>document.getElementById(id);
const iso=d=>{const z=new Date(d.getTime()-d.getTimezoneOffset()*6e4);return z.toISOString().slice(0,10)};
let TD=iso(new Date());
const f=n=>window._hide?"₹•••":"₹"+(Math.round(n*100)/100);
const mkG=(emoji,name,target,days,start,entries)=>({id:"g"+Date.now()+Math.floor(Math.random()*999),emoji,name,target,days,start:start||TD,entries:entries||[]});
let S=null,U="";
try{U=localStorage.getItem("rsbuser")||""}catch(e){}
const users=()=>{try{return JSON.parse(localStorage.getItem("rsbusers")||"{}")}catch(e){return{}}};
const SK=()=>"rsb2_"+U;
function loadS(){S=null;try{const r=localStorage.getItem(SK());if(r)S=JSON.parse(r)}catch(e){}
  if(!S){const g=mkG("📱","Mobile Recharge",630,56,TD,[]);S={goals:[g],cur:g.id}}}
loadS();
if(!S){let o=null;try{o=JSON.parse(localStorage.getItem("rsb1"))}catch(e){}
  const g=mkG("📱","Mobile Recharge",o?o.target:630,56,o?o.start:TD,o?o.entries:[]);S={goals:[g],cur:g.id}}
const save=()=>{if(!U)return;try{localStorage.setItem(SK(),JSON.stringify(S))}catch(e){}};
const G=()=>S.goals.find(x=>x.id===S.cur)||S.goals[0];
const tot=g=>g.entries.reduce((a,e)=>a+e.amt,0);
const PRE=[["📱","Mobile Recharge",630,56],["✈️","Trip",5000,0],["🛡️","Emergency Fund",10000,0],["🎁","Gift",1000,30],["💻","Gadget",20000,0],["🏍️","Bike",50000,0]];
$("pre").innerHTML=PRE.map((p,i)=>`<button data-p="${i}">${p[0]} ${p[1]}</button>`).join("");

// ==========================================================
// GOAL COLOR PALETTE BAR (Vibrant Colors Selection)
// ==========================================================
const VIBRANT_GOAL_COLORS = [
  { c: "#2563eb", name: "Royal Blue" },
  { c: "#10b981", name: "Emerald Green" },
  { c: "#8b5cf6", name: "Electric Purple" },
  { c: "#f97316", name: "Sunset Orange" },
  { c: "#ef4444", name: "Ruby Crimson" },
  { c: "#eab308", name: "Golden Amber" },
  { c: "#06b6d4", name: "Neon Cyan" },
  { c: "#ec4899", name: "Hot Pink" },
  { c: "#14b8a6", name: "Teal Mint" },
  { c: "#6366f1", name: "Indigo Night" },
  { c: "#d97706", name: "Metallic Bronze" },
  { c: "#64748b", name: "Slate Grey" }
];

function renderColorBar() {
  const cBar = $("color-bar");
  if (!cBar) return;
  const curCol = (G().color || "#2563eb").toLowerCase();
  cBar.innerHTML = VIBRANT_GOAL_COLORS.map(item => {
    const isAct = item.c.toLowerCase() === curCol;
    return `<div class="color-swatch ${isAct ? 'active' : ''}" data-col="${item.c}" style="background:${item.c}" title="${item.name}">${isAct ? '✓' : ''}</div>`;
  }).join("");
}

$("color-bar").onclick = e => {
  const swatch = e.target.closest("[data-col]");
  if (!swatch) return;
  const col = swatch.dataset.col;
  const g = G();
  g.color = col;
  $("gcol").value = col;
  save();
  renderColorBar();
  render();
};

// ==========================================================
// BOTTOM NAVIGATION BAR (Menu Bar switching)
// ==========================================================
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.onclick = () => {
    const targetId = btn.dataset.target;
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("on"));
    document.querySelectorAll(".app-view").forEach(v => v.classList.remove("on"));
    btn.classList.add("on");
    const vEl = $(targetId);
    if (vEl) {
      vEl.classList.add("on");
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };
});

// ==========================================================
// MAHESH BABU STYLE VOICE COMMENTARY ENGINE
// ==========================================================
function sayMaheshStyle(text) {
  if (!window._snd || !window.speechSynthesis) return;
  try {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices();
    // Prioritize Indian English / Telugu voices
    const inVoice = voices.find(v => v.lang === "te-IN") ||
                    voices.find(v => v.lang.includes("IN") && (v.name.toLowerCase().includes("male") || v.name.toLowerCase().includes("ravi") || v.name.toLowerCase().includes("mohan") || v.name.toLowerCase().includes("prabhat"))) ||
                    voices.find(v => v.lang.includes("IN")) ||
                    voices.find(v => v.name.toLowerCase().includes("male")) ||
                    null;
    if (inVoice) u.voice = inVoice;
    
    // Mahesh Babu dialogue modulation: Confident, crisp baritone punch
    u.pitch = 0.92;
    u.rate = 1.04;
    u.volume = 1.0;
    
    window.speechSynthesis.speak(u);
  } catch (e) {
    console.log("Speech error:", e);
  }
}

// Fallback say function
function say(t) {
  sayMaheshStyle(t);
}

// ==========================================================
// VOICE ENTRY (Under Pay to Savings)
// ==========================================================
function startVoiceEntry() {
  const R = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!R) return alert("Ee browser lo voice recognition support ledu. Google Chrome vaadandi.");
  
  const r = new R();
  r.lang = "en-IN";
  
  const vb = $("vb_quick");
  const oldText = vb ? vb.innerHTML : "";
  if (vb) {
    vb.innerHTML = "🔴 వింటున్నాను... Amount చెప్పండి (e.g. 50)";
    vb.style.background = "#dc2626";
  }
  
  r.onresult = e => {
    if (vb) { vb.innerHTML = oldText; vb.style.background = ""; }
    const transcript = (e.results[0][0].transcript || "").trim();
    console.log("Spoken:", transcript);
    
    let m = transcript.match(/\\d+(\\.\\d+)?/);
    if (!m) {
      const words = { "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "ten": 10, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "hundred": 100, "five hundred": 500, "thousand": 1000, "padi": 10, "iravai": 20, "muppai": 30, "yaabhai": 50, "vandha": 100, "veyyi": 1000 };
      const low = transcript.toLowerCase();
      for (const [k, v] of Object.entries(words)) {
        if (low.includes(k)) { m = [String(v)]; break; }
      }
    }
    
    if (m) {
      cur = m[0];
      upd();
      $("note").value = "Voice: " + transcript;
      beep();
      $("add").focus();
    } else {
      alert("Amount అర్థం కాలేదు. '50 rupees' లేదా '100' అని స్పష్టంగా చెప్పండి.");
    }
  };
  
  r.onerror = () => {
    if (vb) { vb.innerHTML = oldText; vb.style.background = ""; }
    alert("Voice microphone error వచ్చింది. Permission check చేసి మళ్లీ ప్రయత్నించండి.");
  };
  
  r.onend = () => {
    if (vb) { vb.innerHTML = oldText; vb.style.background = ""; }
  };
  
  r.start();
}

$("vb_quick").onclick = startVoiceEntry;
$("vb").onclick = startVoiceEntry;

function render(){
  const g=G();S.cur=g.id;
  $("tabs").innerHTML=S.goals.map(x=>`<button class="tab ${x.id===g.id?"on":""}" data-g="${x.id}">${x.emoji} ${x.name}</button>`).join("")+'<button class="tab" id="newg">＋ New</button>';
  const t=tot(g),T=g.target,rem=Math.max(0,T-t);
  $("all").textContent=f(S.goals.reduce((a,x)=>a+tot(x),0));const uu=users()[U]||{};$("who").textContent=U?"👤 "+(uu.name||"User")+" · +91 "+U:"";$("gname").textContent=g.emoji+" "+g.name;$("payto").textContent=g.emoji+" "+g.name;
  $("total").textContent=f(t);$("rem").textContent=f(rem);
  $("today").textContent=f(g.entries.filter(e=>e.date===TD).reduce((a,e)=>a+e.amt,0));
  const p=Math.min(100,T?t/T*100:0);$("pb").style.width=p+"%";
  $("pct").textContent=p.toFixed(1)+"% of "+f(T)+" target"+(t>=T?" — Target complete! 🎉":"");
  const D=g.days||0;
  if(D>0){const dn=Math.round((new Date(TD+"T00:00:00")-new Date(g.start+"T00:00:00"))/864e5)+1;
    const d=Math.min(Math.max(dn,1),D),left=Math.max(D-d+1,1);
    $("day").textContent=d+" / "+D;
    $("need").textContent=rem>0?"Migilina "+left+" rojulu: roju "+f(rem/left)+" save cheste target reach avthav (average "+f(T/D)+"/day)":"";
    const by={};g.entries.forEach(e=>by[e.date]=(by[e.date]||0)+e.amt);
    let h="";for(let i=1;i<=D;i++){const dd=new Date(g.start+"T00:00:00");dd.setDate(dd.getDate()+i-1);const k=iso(dd);
      h+=`<div class="c ${by[k]?"s":""} ${k===TD?"t":""}" title="${k}">${i}</div>`}
    $("grid").innerHTML=h;$("gc").style.display="";
  }else{$("day").textContent="No deadline";$("need").textContent=rem>0?"Deadline ledu — free ga save chey, "+f(rem)+" inka kavali":"";$("gc").style.display="none"}
  const L=[...g.entries].sort((a,b)=>b.date.localeCompare(a.date)||b.id-a.id);
  $("list").innerHTML=dayList(g);
  $("st").value=g.start;$("tg").value=g.target;$("sd").value=D;extras(g,t,rem,D);
  $("del").style.display=S.goals.length>1?"":"none";
  renderColorBar();
}
var cur="";
function upd(){$("disp").textContent=cur||"0";$("amt").value=cur}
function count(el,v){let n=0;const t=setInterval(()=>{n++;el.textContent=f(n>=20?v:v*n/20);if(n>=20)clearInterval(t)},30)}
function rain(E,N){const o=$("ok");for(let i=0;i<N;i++){const s=document.createElement("span");s.className="fall";s.textContent=E[i%E.length];s.style.left=Math.random()*94+"%";s.style.animationDuration=(1.8+Math.random()*1.8)+"s";s.style.animationDelay=(Math.random()*1.2)+"s";o.appendChild(s);setTimeout(()=>s.remove(),4800)}}
function beep(){try{const c=new(window.AudioContext||window.webkitAudioContext)();[880,1320,1760].forEach((fq,i)=>{const o=c.createOscillator(),g=c.createGain();o.frequency.value=fq;g.gain.value=.15;o.connect(g);g.connect(c.destination);o.start(c.currentTime+i*.11);o.stop(c.currentTime+i*.11+.14)})}catch(e){}}

document.querySelector(".keys").onclick=e=>{const k=e.target.dataset.k;if(k==null)return;if(k==="del")cur=cur.slice(0,-1);else if(k==="."){if(!cur.includes("."))cur=(cur||"0")+"."}else if(cur.length<7)cur=(cur==="0"?"":cur)+k;upd()};
$("q").onclick=e=>{const q=e.target.dataset.q;if(q){cur=String((parseFloat(cur)||0)+parseFloat(q));upd()}};

$("add").onclick=()=>{const a=parseFloat($("amt").value),d=$("dt").value||TD;if(!(a>0))return;
  const g=G(),before=tot(g),t="SB"+Date.now().toString().slice(-8)+Math.floor(Math.random()*90+10);
  const tmv=$("tm").value||nowT();g.entries.push({id:Date.now(),date:d,time:tmv,amt:a,note:$("note").value.trim(),txn:t,src:$("src").value,md:$("md").value});$("tm").value=nowT();save();cur="";upd();$("note").value="";render();
  const done=before<g.target&&tot(g)>=g.target;
  count($("okamt"),a);$("oktx").textContent="Txn ID: "+t+" · "+d+" · "+h12(tmv);
  $("okmsg").textContent=done?"🎉 Target complete! "+g.name+" ready":"Savings Bank ki add ayindi → "+g.emoji+" "+g.name;
  $("ok").classList.add("on");chime();
  const ms=[100,250,500,1000,2500,5000].find(m=>before<m&&tot(g)>=m);
  if(ms)$("okmsg").textContent="🏆 Milestone ₹"+ms+" reached! "+g.name;
  if(done||ms)rain(["🎉","🎊","⭐","🪙","💰"],60);else rain(["💸","🪙","💰","💵"],32);
  
  // Dynamic Mahesh Babu style dialogue with real logged-in user name
  const uObj = users()[U] || {};
  const currentUserName = uObj.name || (U ? "Pavan Sai" : "Pavan Sai");
  const maheshDialogue = `${a} rupees mee savings bank ki add ayindi, mee goal ${g.name} kosam... Super ${currentUserName}!`;
  sayMaheshStyle(maheshDialogue);
};

$("okd").onclick=()=>$("ok").classList.remove("on");
$("list").onclick=e=>{const i=e.target.dataset.i;if(i){const g=G();g.entries=g.entries.filter(x=>String(x.id)!==i);save();render()}};
$("tabs").onclick=e=>{const id=e.target.dataset.g;if(id){S.cur=id;save();render()}else if(e.target.id==="newg"){$("nf").classList.toggle("on");$("nf").scrollIntoView({behavior:"smooth"})}};
$("pre").onclick=e=>{const p=PRE[e.target.dataset.p];if(p){$("ne").value=p[0];$("nn").value=p[1];$("nt").value=p[2];$("nd").value=p[3]}};
$("mk").onclick=()=>{const n=$("nn").value.trim(),t=parseFloat($("nt").value);if(!n||!(t>0))return;
  const g=mkG($("ne").value.trim()||"🎯",n,t,parseInt($("nd").value)||0);S.goals.push(g);S.cur=g.id;save();$("nf").classList.remove("on");$("nn").value="";$("nt").value="";render();window.scrollTo({top:0,behavior:"smooth"})};
$("st").onchange=e=>{if(e.target.value){G().start=e.target.value;save();render()}};
$("tg").onchange=e=>{const v=parseFloat(e.target.value);if(v>0){G().target=v;save();render()}};
$("sd").onchange=e=>{G().days=Math.max(0,parseInt(e.target.value)||0);save();render()};
$("reset").onclick=()=>{if(confirm("Ee goal entries anni clear cheyyala?")){G().entries=[];save();render()}};
$("del").onclick=()=>{if(S.goals.length>1&&confirm("Ee goal ni delete cheyyala?")){S.goals=S.goals.filter(x=>x.id!==S.cur);S.cur=S.goals[0].id;save();render()}};
(async()=>{let sm=null;try{sm=await window.claude.use("sample")}catch(e){}
  if(!sm)return;window._sm=sm;$("ai").style.display="";
  $("aib").onclick=async()=>{const g=G(),t=tot(g),rem=Math.max(0,g.target-t),D=g.days||0;
    let left=0;if(D>0){const dn=Math.round((new Date(TD+"T00:00:00")-new Date(g.start+"T00:00:00"))/864e5)+1;left=Math.max(D-Math.min(Math.max(dn,1),D)+1,1)}
    const p="I am a student in India using a savings tracker. Goal: "+g.name+", target Rs "+g.target+", saved Rs "+t+", remaining Rs "+rem+", "+(left?left+" days left":"no deadline")+". My situation: "+($("aic").value.trim()||"not given")+".\\nReply in Telugu-English mix (Telugu words written in English letters), short and mobile friendly, plain text, no markdown symbols like ** or #. Give: 1) Daily amount needed for this goal. 2) 5 realistic daily money-saving habits with approx Rs saved per day. 3) 5 realistic ways to earn extra money per day (tutoring, freelancing, reselling, small services, etc.) with first steps to start and approx earning. 4) A simple 7-day action plan. No gambling, trading tips, or get-rich-quick schemes. Under 300 words.";
    $("aib").disabled=true;$("aio").textContent="Thinking...";
    try{await sm(p,{cache:false,onText:({text})=>{$("aio").textContent=text}})}
    catch(e){$("aio").textContent=e&&e.code==="rate_limited"?"Konchem sepu aagi malli try chey.":"AI ippudu available ledu, malli try chey."}
    $("aib").disabled=false}})();
function chime(){try{navigator.vibrate&&navigator.vibrate([60,40,120])}catch(e){}
  try{const c=new(window.AudioContext||window.webkitAudioContext)();[523.25,659.25,783.99,1046.5,1318.5].forEach((fq,i)=>{const t=c.currentTime+i*.13,o=c.createOscillator(),o2=c.createOscillator(),g=c.createGain();o.type="triangle";o2.type="sine";o.frequency.value=fq;o2.frequency.value=fq*2;g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.22,t+.02);g.gain.exponentialRampToValueAtTime(.001,t+(i===4?.9:.35));o.connect(g);o2.connect(g);g.connect(c.destination);o.start(t);o2.start(t);o.stop(t+1);o2.stop(t+1)})}catch(e){}}
let pin="",ent="";
function ld(){$("dots").innerHTML=[0,1,2,3].map(i=>`<i class="${i<ent.length?"f":""}"></i>`).join("")}
$("lk").onclick=e=>{const k=e.target.dataset.k;if(k==null)return;$("lmsg").textContent="";if(k==="x")ent=ent.slice(0,-1);else if(ent.length<4)ent+=k;ld();if(ent.length===4){if(ent===pin)$("lock").classList.remove("on");else{$("lmsg").textContent="Wrong PIN, malli try chey";ent="";setTimeout(ld,250)}}};
$("pin").onclick=()=>{if(pin){if(confirm("PIN remove cheyyala?")){pin="";try{localStorage.removeItem("rsbpin")}catch(e){}}}else{const p=prompt("Kotha 4-digit PIN enter chey");if(p&&/^\\d{4}$/.test(p)){pin=p;try{localStorage.setItem("rsbpin",p)}catch(e){}}else if(p)alert("4 digits matrame undali")}$("pin").textContent=pin?"Remove PIN":"Set app PIN"};
$("pin").textContent=pin?"Remove PIN":"Set app PIN";if(pin){ld();$("lock").classList.add("on")}
const nowT=()=>{const n=new Date();return String(n.getHours()).padStart(2,"0")+":"+String(n.getMinutes()).padStart(2,"0")};
const h12=t=>{const[h,m]=t.split(":").map(Number);return (h%12||12)+":"+String(m).padStart(2,"0")+(h<12?" AM":" PM")};

const tick=()=>{const n=iso(new Date());if(n!==TD){const old=TD;TD=n;if($("dt").value===old)$("dt").value=n;$("tm").value=nowT();render()}
  $("clk").textContent=new Date().toLocaleString([],{day:"2-digit",month:"short",hour:"numeric",minute:"2-digit"})};
tick();setInterval(tick,5000);document.addEventListener("visibilitychange",tick);$("tm").value=nowT();
let cr=7,cm=0;
function extras(g,t,rem,D){
  const T=g.target,by={},ns=g.ns||[];g.entries.forEach(e=>by[e.date]=(by[e.date]||0)+e.amt);
  const ok=d=>(by[d]||0)>0||ns.includes(d)||(g.fr||[]).includes(d);
  const dd=new Date(TD+"T00:00:00");if(!ok(iso(dd)))dd.setDate(dd.getDate()-1);
  let st=0;while(ok(iso(dd))){st++;dd.setDate(dd.getDate()-1)}
  $("stk").textContent=st+" 🔥";
  const all=S.goals.reduce((a,x)=>a+tot(x),0);
  $("lvl").textContent=all>=2000?"💎 Diamond":all>=500?"🥇 Gold":all>=100?"🥈 Silver":"🥉 Bronze";
  $("bst").textContent=f(Math.max(0,...Object.values(by)));
  let left=1;if(D>0){const dn=Math.round((new Date(TD+"T00:00:00")-new Date(g.start+"T00:00:00"))/864e5)+1;left=Math.max(D-Math.min(Math.max(dn,1),D)+1,1)}
  const tg=Math.max(1,Math.ceil(D>0?rem/left:10)),td=Math.max(0,by[TD]||0);
  window._tg=rem>0?tg:10;
  $("dpb").style.width=Math.min(100,td/tg*100)+"%";
  $("dtx").textContent="Daily target: "+f(td)+" / "+f(tg)+(td>=tg?" ✅ Done!":"");
  $("qs").textContent="⚡ Quick save "+f(window._tg);
  $("ns").textContent=ns.includes(TD)?"✅ No-spend marked":"🎲 No-spend day";
  const Q=["Chinna chinna savings, pedda dreams! 💪","Roju ₹10 kuda oka month lo ₹300 avthundi 🪙","Kharchu mundu kaadu, save mundu! 🎯","Discipline unte dabbulu nee venake vasthayi 🐷","Ee roju save chesav ante, repu nee future happy 😊","Chai money kuda savings ki start 🍵","Streak break cheyyaku, oka rupee aina save chey 🔥"];
  $("qt").textContent=Q[Math.floor(Date.now()/864e5)%Q.length];
  {const p=Math.min(100,Math.max(0,T?t/T*100:0)),n=t>0?Math.max(1,Math.round(p/10)):0,an=n!==window._pn;window._pn=n;
    const rows=[4,3,2,1],ic=["💵","💵","🪙","💰"];let h="",k=0;
    rows.forEach((c,r)=>{let s="";for(let i=0;i<c;i++){if(k<n)s+=`<span style="${an?`animation:pp .45s ${k*50}ms both`:""}">${ic[r]}</span>`;k++}if(s)h+=`<div>${s}</div>`});
    if(p>=100)h+='<div><span style="animation:pp .5s both">👑</span></div>';
    $("pile").innerHTML=h||'<div class="em">Money gutta<br>ikkada pedutundi 💵</div>'}
  $("rch").style.display=(t>=T&&/recharge/i.test(g.name))?"block":"none";
  chart();cal();more(g,by,t,rem,D,tg,st,all)}
function chart(){const g=G(),by={};g.entries.forEach(e=>by[e.date]=(by[e.date]||0)+e.amt);
  const a=[];for(let i=cr-1;i>=0;i--){const d=new Date(TD+"T00:00:00");d.setDate(d.getDate()-i);const k=iso(d);a.push([k,Math.max(0,by[k]||0)])}
  const mx=Math.max(1,...a.map(x=>x[1]));
  $("chart").innerHTML=a.map(x=>`<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;min-width:0"><div style="font-size:9px;color:var(--mu)">${x[1]?Math.round(x[1]):""}</div><div style="width:70%;background:linear-gradient(var(--ok),var(--ac));border-radius:4px 4px 0 0;height:${x[1]/mx*90}px;min-height:${x[1]?3:1}px"></div><div style="font-size:9px;color:var(--mu)">${x[0].slice(cr>7?8:5)}</div></div>`).join("");
  $("c7").style.opacity=cr===7?1:.5;$("c30").style.opacity=cr===30?1:.5}
function cal(){const g=G(),by={},ns=g.ns||[];g.entries.forEach(e=>by[e.date]=(by[e.date]||0)+e.amt);
  const b=new Date(TD+"T00:00:00");b.setDate(1);b.setMonth(b.getMonth()+cm);const y=b.getFullYear(),m=b.getMonth(),n=new Date(y,m+1,0).getDate();
  $("cmt").textContent=b.toLocaleDateString([],{month:"long",year:"numeric"});
  let h="";for(let i=0;i<b.getDay();i++)h+="<div></div>";
  for(let d=1;d<=n;d++){const k=iso(new Date(y,m,d)),s=(by[k]||0)>0,z=ns.includes(k),p=k<TD&&k>=g.start;
    const bg=s?"var(--ok)":z?"var(--ac)":p?"#f04438":"var(--cell)",c=(s||z||p)?"#fff":"var(--mu)";
    h+=`<div class="c" style="background:${bg};color:${c};${k===TD?"outline:2px solid var(--ac)":""}">${d}</div>`}
  $("cal").innerHTML=h}
$("c7").onclick=()=>{cr=7;chart()};$("c30").onclick=()=>{cr=30;chart()};$("cp").onclick=()=>{cm--;cal()};$("cn").onclick=()=>{cm++;cal()};
$("qs").onclick=()=>{cur=String(window._tg||10);upd();$("note").value="Quick save";$("add").click()};
$("ns").onclick=()=>{const g=G();g.ns=g.ns||[];const i=g.ns.indexOf(TD);if(i>=0)g.ns.splice(i,1);else g.ns.push(TD);save();render()};
$("rb").onclick=()=>{const x=parseFloat($("rs").value);if(!(x>0))return;const r=Math.round((Math.ceil(x/10)*10-x)*100)/100;if(!(r>0)){$("rs").value="";return alert("Already round number, round-up em ledu 😄")}cur=String(r);upd();$("note").value="Round-up on ₹"+x;$("rs").value="";$("add").click()};
$("wb").onclick=()=>{const a=parseFloat($("wa").value),g=G();if(!(a>0))return;if(g.lock&&TD<g.lock)return alert("🔒 Ee goal "+g.lock+" varaku locked");
  if(g.lim){const sp=g.entries.filter(e=>e.date===TD&&e.amt<0).reduce((x,e)=>x-e.amt,0);if(sp+a>g.lim&&!confirm("⚠️ Daily limit ₹"+g.lim+" cross avthundi. Continue?"))return}
  if(a>tot(g)&&!confirm("Saved kante ekkuva withdraw chestunnav. Continue?"))return;
  g.entries.push({id:Date.now(),date:TD,time:nowT(),amt:-a,note:"Withdraw: "+($("wn").value.trim()||"spend"),txn:"WD"+Date.now().toString().slice(-8)});$("wa").value="";$("wn").value="";save();render();wdAnim(a,g)};
const wf=()=>{const p=parseFloat($("wp").value),d=parseInt($("wdn").value)||0,g=G(),rem=Math.max(0,g.target-tot(g));if(!(p>0)){$("wr").textContent="";return}const x=p*d;$("wr").textContent="₹"+p+" × "+d+" days = "+f(x)+(x>=rem?" ✅ Target reach avthav!":" — inka "+f(rem-x)+" kavali")};
$("wp").oninput=wf;$("wdn").oninput=wf;
$("rpb").onclick=()=>{const g=G(),ym=TD.slice(0,7),by={};let sp=0;g.entries.filter(e=>e.date.startsWith(ym)).forEach(e=>{if(e.amt>0)by[e.date]=(by[e.date]||0)+e.amt;else sp-=e.amt});
  const v=Object.entries(by),sv=v.reduce((a,x)=>a+x[1],0),b=[...v].sort((x,y)=>y[1]-x[1])[0];
  $("rp").textContent=g.emoji+" "+g.name+" · "+ym+"\\nSaved: "+f(sv)+"\\nWithdrawn: "+f(sp)+"\\nSaving days: "+v.length+(v.length?"\\nAverage per saving day: "+f(sv/v.length):"")+(b?"\\nBest day: "+b[0]+" ("+f(b[1])+")":"")+"\\nStreak: "+$("stk").textContent+"\\nTotal balance: "+f(tot(g))};
$("bkb").onclick=()=>{const t=JSON.stringify(S);$("bk").value=t;$("bk").select();try{navigator.clipboard.writeText(t)}catch(e){}};
$("rsb").onclick=()=>{try{const o=JSON.parse($("bk").value);if(!o.goals||!o.goals.length)throw 0;if(!confirm("Ee data tho current data replace cheyyala?"))return;S=o;S.cur=S.goals[0].id;save();render()}catch(e){alert("Valid backup data kaadu")}};
let TH={mode:"auto",acc:"def"};try{TH=Object.assign(TH,JSON.parse(localStorage.getItem("rsbtheme")))}catch(e){}
function applyTh(){const r=document.documentElement;if(TH.mode==="auto")r.removeAttribute("data-theme");else r.dataset.theme=TH.mode;if(TH.acc==="def")r.removeAttribute("data-acc");else r.dataset.acc=TH.acc;$("thm").textContent=TH.mode==="auto"?"🌗 Auto":TH.mode==="dark"?"🌙 Dark":"☀️ Light";try{localStorage.setItem("rsbtheme",JSON.stringify(TH))}catch(e){}}
$("thm").onclick=()=>{TH.mode={auto:"light",light:"dark",dark:"auto"}[TH.mode];applyTh()};
$("acc").onclick=e=>{const a=e.target.dataset.a;if(!a)return;const all=S.goals.reduce((x,y)=>x+tot(y),0);if(a==="sun"&&all<100)return alert("₹100 save chesthe unlock avthundi 🔒");if(a==="forest"&&all<500)return alert("₹500 save chesthe unlock avthundi 🔒");TH.acc=a;applyTh()};
$("aik").onclick=async()=>{const sm=window._sm;if(!sm)return;const g=G(),notes=g.entries.slice(-40).map(e=>(e.amt<0?"spent ":"saved ")+Math.abs(e.amt)+" "+(e.note||"")).join("; ");
  if(!notes){$("aio").textContent="Mundu konni entries / withdrawals add chey.";return}
  $("aik").disabled=true;$("aio").textContent="Analyzing...";
  try{await sm("Student in India. Savings tracker entries: "+notes+". In Telugu-English mix (Telugu written in English letters), plain text, under 200 words: find where money probably leaks (chai, snacks, recharge etc.), give 4 specific small fixes with approx Rs saved per day, and one motivating line. No markdown symbols.",{cache:false,onText:({text})=>{$("aio").textContent=text}})}catch(e){$("aio").textContent="AI ippudu available ledu, malli try chey."}
  $("aik").disabled=false};
applyTh();
function wdAnim(a,g){
  $("wdamt").textContent="−"+f(a);$("wdbal").textContent="Balance left: "+f(tot(g));$("wdo").classList.add("on");
  const o=$("wdo"),E=["💸","💸","💵","🪙"];
  for(let i=0;i<28;i++){const s=document.createElement("span");s.className="fly";s.textContent=E[i%4];s.style.left=Math.random()*94+"%";s.style.animationDuration=(1.6+Math.random()*1.6)+"s";s.style.animationDelay=(Math.random()*1)+"s";o.appendChild(s);setTimeout(()=>s.remove(),4400)}
  try{navigator.vibrate&&navigator.vibrate([200,80,200])}catch(e){}
  try{const c=new(window.AudioContext||window.webkitAudioContext)();[660,523,392,262].forEach((fq,i)=>{const t=c.currentTime+i*.14,os=c.createOscillator(),gn=c.createGain();os.type="triangle";os.frequency.value=fq;gn.gain.setValueAtTime(.2,t);gn.gain.exponentialRampToValueAtTime(.001,t+.4);os.connect(gn);gn.connect(c.destination);os.start(t);os.stop(t+.5)})}catch(e){}}
$("wdd").onclick=()=>$("wdo").classList.remove("on");
const ls=k=>{try{return localStorage.getItem(k)}catch(e){return null}};
window._snd=true;window._AC=window.AudioContext;window._WAC=window.webkitAudioContext;

let big=false;
function chAmt(g){const v=$("ch").value,dn=Math.max(1,Math.round((new Date(TD+'T00:00:00')-new Date(g.start+'T00:00:00'))/864e5)+1),wk=Math.min(52,Math.floor((dn-1)/7)+1);
  return v==='ten'?10:v==='inc'?Math.min(dn,30):v==='w52'?wk:v==='coin'?[1,2,5][dn%3]:0}
function pbook(){const g=G(),q=$("pq").value.trim().toLowerCase();let bal=0;
  const rows=[...g.entries].sort((a,b)=>(a.date+(a.time||'')).localeCompare(b.date+(b.time||''))||a.id-b.id).map(e=>{bal+=e.amt;return{e,bal}}).reverse().filter(r=>!q||(r.e.date+' '+(r.e.note||'')+' '+r.e.amt+' '+(r.e.txn||'')).toLowerCase().includes(q)).slice(0,100);
  $("pbt").innerHTML='<tr><th>Date</th><th>Details</th><th>Dr/Cr</th><th>Bal</th></tr>'+rows.map(r=>`<tr><td>${r.e.date.slice(5)}${r.e.time?'<br>'+h12(r.e.time):''}</td><td>${r.e.note||'Saved'}</td><td class='${r.e.amt<0?'dr':'cr'}'>${r.e.amt<0?'−':'+'}${Math.abs(r.e.amt)}</td><td>${Math.round(r.bal*100)/100}</td></tr>`).join('')}

function more(g,by,t,rem,D,tg,st,all){
  window._st=st;
  const ymd=n=>{const d=new Date(TD+'T00:00:00');d.setDate(d.getDate()+n);return iso(d)},Y=ymd(-1),L=[];
  if(D>0){const dn=Math.round((new Date(TD+'T00:00:00')-new Date(g.start+'T00:00:00'))/864e5)+1;L.push('⏳ Plan end ki inka '+Math.max(D-dn,0)+' rojulu · '+f(rem)+' kavali')}
  let s14=0;for(let i=0;i<14;i++)s14+=Math.max(0,by[ymd(-i)]||0);const av=s14/14;
  if(rem>0&&av>0){const dd=Math.ceil(rem/av);L.push('🔮 Ee speed lo ('+f(av)+'/day) target '+ymd(dd)+' ki reach avthav ('+dd+' days)')}else if(rem>0)L.push('🔮 Konni rojulu save chesthe target date predict chestha');
  const wd=new Date(TD+'T00:00:00').getDay();if(wd===0||wd===6)L.push('📍 Weekend boost: ivala target x2 = '+f(tg*2));
  const miss=Y>=g.start&&!((by[Y]||0)>0)&&!(g.ns||[]).includes(Y)&&!(g.fr||[]).includes(Y);
  if(miss&&rem>0)L.push('🔄 Nenna miss ayav, ivala '+f(tg*2)+' save chesthe catch-up');
  if((by[TD]||0)<=0&&rem>0)L.push('💡 Ivala inka save cheyyaledu, '+f(tg)+' chey!');
  L.push('🎬 Total '+f(all)+' = '+Math.floor(all/10)+' chai ☕'+(g.target>0?' · target lo '+Math.round(t/g.target*100)+'%':''));
  $("sm").textContent=L.join('\\n');
  const hs=+(ls('rsbhs')||0);
  const A=[['🥇 First save',g.entries.some(e=>e.amt>0)],['💯 ₹100 club',all>=100],['🏆 ₹500 club',all>=500],['💎 ₹2000 club',all>=2000],['🔥 7-day streak',st>=7],['📆 30-day streak',st>=30],['🎯 Goal done',S.goals.some(x=>tot(x)>=x.target)],['🧊 Freeze used',(g.fr||[]).length>0],['🎲 No-spend',(g.ns||[]).length>0],['🕹️ Gamer',hs>0]];
  $("ach").innerHTML=A.map(a=>`<span class='ach ${a[1]?'':'off'}'>${a[0]}</span>`).join('');
  let o=null;try{o=JSON.parse(ls('rsbspin'))}catch(e){}
  $("spr").textContent=(o&&o.d===TD)?'🎰 Ivala spin: '+o.t:'';
  $("ch").value=g.ch||'';const ca=chAmt(g);$("chb").style.display=ca>0?'block':'none';$("chb").textContent='Do today challenge: ₹'+ca;
  $("lk").value=g.lock||'';$("lm").value=g.lim||'';$("gcol").value=g.color||'#2563eb';
  $("pb").style.background=g.color||'';document.querySelectorAll('.tab.on[data-g]').forEach(e=>e.style.background=g.color||'');
  const key=S.goals.map(x=>x.id).join();
  if($("spl").dataset.k!==key){$("spl").dataset.k=key;$("spl").innerHTML=S.goals.map(x=>`<div class='row' style='margin-top:6px;align-items:center'><span style='flex:2'>${x.emoji} ${x.name}</span><input data-sp='${x.id}' type='number' value='${Math.round(100/S.goals.length)}' style='flex:1'></div>`).join('')}
  const N=S.notes||[],tp={lend:'🤝 Lend',borrow:'🙏 Borrow',earn:'💼 Earning',cpn:'🎁 Coupon'},sm2=k=>N.filter(n=>n.t===k).reduce((a,n)=>a+(n.amt||0),0);
  $("nl").innerHTML=(N.length?`<div class='hint'>Lend ${f(sm2('lend'))} · Borrow ${f(sm2('borrow'))} · Earnings ${f(sm2('earn'))}</div>`:'')+N.map(n=>`<div class='e'><span>${tp[n.t]} · ${n.txt||''}<br><small style='color:var(--mu)'>${n.d||''}${n.d&&n.t==='cpn'&&n.d<TD?' · expired':''}</small></span><b>${n.amt?'₹'+n.amt:''}</b><button data-n='${n.id}'>✕</button></div>`).join('');
  pbook()}
$("fz").onclick=()=>{const g=G();g.fr=g.fr||[];const b=new Date(TD+'T00:00:00').getTime(),y=iso(new Date(b-864e5)),w=iso(new Date(b-6*864e5));
  if(g.fr.some(d=>d>=w))return alert('Vaaraniki 1 freeze matrame 🧊');g.fr.push(y);save();render();alert('🧊 Nenna roju streak freeze ayindi')};
$("yr").onclick=()=>{const g=G(),yy=TD.slice(0,4),by={},bm={};g.entries.filter(e=>e.date.startsWith(yy)&&e.amt>0).forEach(e=>{by[e.date]=(by[e.date]||0)+e.amt;const m=e.date.slice(0,7);bm[m]=(bm[m]||0)+e.amt});
  const tt=Object.values(by).reduce((a,x)=>a+x,0),bd=Object.entries(by).sort((a,b)=>b[1]-a[1])[0],bo=Object.entries(bm).sort((a,b)=>b[1]-a[1])[0];
  $("yrt").textContent='📅 '+yy+' Review\\n💰 Total saved: '+f(tt)+'\\n🗓️ Saving days: '+Object.keys(by).length+(bo?'\\n🏆 Best month: '+bo[0]+' ('+f(bo[1])+')':'')+(bd?'\\n⭐ Best day: '+bd[0]+' ('+f(bd[1])+')':'')+'\\n🔥 Current streak: '+(window._st||0)};
$("sp").onclick=()=>{let o=null;try{o=JSON.parse(ls('rsbspin'))}catch(e){}if(o&&o.d===TD){$("spr").textContent='🎰 Ivala spin already chesav: '+o.t;return}
  const A=['Ivala ₹15 save chey 💪','No-spend day try chey 🎲','Chai kharchu skip chesi ₹10 save chey ☕','Bonus: ₹5 extra save chey 🪙','Ivala withdraw cheyyaku! 🔒','Round-up save try chey 🪙','Friend ki savings app cheppu 😄'],t=A[Math.floor(Math.random()*A.length)];
  try{localStorage.setItem('rsbspin',JSON.stringify({d:TD,t}))}catch(e){}$("spr").textContent='🎰 '+t};
$("ch").onchange=e=>{G().ch=e.target.value;save();render()};
$("chb").onclick=()=>{const a=chAmt(G());if(a>0){cur=String(a);upd();$("note").value='Challenge';$("add").click()}};
$("gs").onclick=()=>{let sc=0,tl=15;const a=$("ga");a.innerHTML='';$("gt").textContent='Score 0 · 15s';
  const sp=setInterval(()=>{const c=document.createElement('span');c.textContent=['💰','🪙','💵'][Math.floor(Math.random()*3)];c.style.left=Math.random()*85+'%';c.style.top=Math.random()*80+'%';c.onclick=()=>{sc++;c.remove();$("gt").textContent='Score '+sc+' · '+tl+'s'};a.appendChild(c);setTimeout(()=>c.remove(),1100)},420);
  const iv=setInterval(()=>{tl--;$("gt").textContent='Score '+sc+' · '+tl+'s';if(tl<=0){clearInterval(iv);clearInterval(sp);a.innerHTML='';let hs=+(ls('rsbhs')||0);if(sc>hs){hs=sc;try{localStorage.setItem('rsbhs',hs)}catch(e){}}$("gt").textContent='🎉 Final score '+sc+' · High score '+hs;render()}},1000)};
$("lk").onchange=e=>{G().lock=e.target.value;save()};$("lm").onchange=e=>{G().lim=parseFloat(e.target.value)||0;save()};
$("gcol").onchange=e=>{G().color=e.target.value;save();renderColorBar();render()};

$("spb").onclick=()=>{const a=parseFloat($("spa").value),ins=[...document.querySelectorAll('[data-sp]')];if(!(a>0))return;
  const sum=ins.reduce((x,i)=>x+(parseFloat(i.value)||0),0);if(Math.abs(sum-100)>.5){$("spm").textContent='Total % 100 undali (ippudu '+sum+'%)';return}
  ins.forEach(i=>{const p=parseFloat(i.value)||0,g=S.goals.find(x=>x.id===i.dataset.sp);if(g&&p>0)g.entries.push({id:Date.now()+Math.floor(Math.random()*1e4),date:TD,time:nowT(),amt:Math.round(a*p)/100,note:'Split save',txn:'SP'+Date.now().toString().slice(-8)})});
  $("spa").value='';$("spm").textContent='✅ Split ayindi';save();render()};
$("nad").onclick=()=>{const a=parseFloat($("nam").value)||0,x=$("ntx").value.trim();if(!x&&!a)return;S.notes=S.notes||[];S.notes.push({id:Date.now(),t:$("nt").value,txt:x,amt:a,d:$("ndt").value});
  if($("nt").value==='earn'&&a>0)alert('💡 Earning ayindi! 20% = ₹'+Math.round(a*20)/100+' save cheyyi');$("ntx").value='';$("nam").value='';save();render()};
$("nl").onclick=e=>{const i=e.target.dataset.n;if(i){S.notes=(S.notes||[]).filter(n=>String(n.id)!==i);save();render()}};
function calc(){const b=parseFloat($("bi").value);$("br").textContent=b>0?'Needs '+f(b*.5)+' · Wants '+f(b*.3)+' · Savings '+f(b*.2):'';
  const P=parseFloat($("ia").value),rt=parseFloat($("ir").value)||0,n=parseInt($("im").value)||0;
  if(P>0&&n>0){const r=rt/1200,fv=r?P*((Math.pow(1+r,n)-1)/r)*(1+r):P*n;$("ires").textContent='Deposit '+f(P*n)+' → '+f(fv)+' (interest '+f(fv-P*n)+')'}else $("ires").textContent='';
  const pr=[[28,'p28'],[56,'p56'],[84,'p84']].map(x=>[x[0],parseFloat($(x[1]).value)]).filter(x=>x[1]>0);
  if(pr.length>1){const m=Math.min(...pr.map(x=>x[1]/x[0]));$("pcr").textContent=pr.map(x=>x[0]+'d: '+f(x[1]/x[0])+'/day'+(x[1]/x[0]===m?' ✅ cheapest':'')).join(' · ')}else $("pcr").textContent=''}
['bi','ia','ir','im','p28','p56','p84'].forEach(i=>$(i).oninput=calc);
$("pq").oninput=pbook;
$("ud").onclick=()=>{const g=G();if(!g.entries.length)return;const m=Math.max(...g.entries.map(e=>e.id));if(confirm('Last entry undo cheyyala?')){g.entries=g.entries.filter(e=>e.id!==m);save();render()}};
$("snd").onclick=()=>{window._snd=!window._snd;window.AudioContext=window._snd?window._AC:null;window.webkitAudioContext=window._snd?window._WAC:null;$("snd").textContent=window._snd?'🔊 Sound on':'🔇 Sound off'};
$("bt").onclick=()=>{big=!big;document.body.style.zoom=big?1.18:1;$("bt").textContent=big?'🔠 Normal text':'🔠 Big text'};
$('eye').onclick=()=>{window._hide=!window._hide;$('eye').textContent=window._hide?'🙈':'👁️';render()};
async function ask(btn,p){const sm=window._sm;if(!sm)return;btn.disabled=true;$('aio').textContent='Thinking...';try{await sm(p,{cache:false,onText:({text})=>{$('aio').textContent=text}})}catch(e){$('aio').textContent='AI ippudu available ledu, malli try chey.'}btn.disabled=false}
$("aiw").onclick=()=>{const g=G(),by={};g.entries.forEach(e=>by[e.date]=(by[e.date]||0)+e.amt);let s='';for(let i=6;i>=0;i--){const d=new Date(TD+'T00:00:00');d.setDate(d.getDate()-i);const k=iso(d);s+=k+': '+(by[k]||0)+'; '}
  ask($("aiw"),'Weekly savings review for an Indian student. Goal '+g.name+' target Rs '+g.target+', saved Rs '+tot(g)+'. Daily net savings last 7 days: '+s+'. In Telugu-English mix (Telugu in English letters), plain text, under 180 words: what went well, which day was missed, one improvement, and a score out of 10. No markdown symbols.')};
$("aip").onclick=()=>ask($("aip"),'Indian prepaid mobile user paying Rs '+G().target+' per recharge. In Telugu-English mix (Telugu in English letters), plain text, under 200 words: how to choose the cheapest recharge plan (per-day cost across 28/56/84 day validity, daily data needed, skipping unused OTT bundles) and 4 practical tips. Do not quote exact current plan prices. No markdown symbols.');
function dayList(g){
  const y=new Date(TD+"T00:00:00");y.setDate(y.getDate()-1);const Y=iso(y),R=n=>Math.round(n*100)/100;
  const ds=[...new Set([...g.entries.map(e=>e.date),TD,Y])].sort().reverse();
  const nm=d=>d===TD?"Today":d===Y?"Yesterday":new Date(d+"T00:00:00").toLocaleDateString([],{weekday:"short",day:"numeric",month:"short"});
  return ds.map(d=>{const es=g.entries.filter(e=>e.date===d).sort((a,b)=>(b.time||"").localeCompare(a.time||"")||b.id-a.id);
    const dt=es.reduce((a,e)=>a+e.amt,0),cum=g.entries.filter(e=>e.date<=d).reduce((a,e)=>a+e.amt,0);
    return `<div style="margin-top:12px;padding:10px;border-radius:12px;background:var(--bg)"><div style="display:flex;justify-content:space-between;align-items:center"><b>${nm(d)}</b><b style="color:${dt>0?"var(--ok)":dt<0?"#f04438":"var(--mu)"}">${dt>0?"+":dt<0?"−":""}₹${R(Math.abs(dt))}</b></div><div class="hint" style="margin:2px 0 6px">${d} · Total savings up to this day: <b>₹${R(cum)}</b></div>`+(es.length?es.map(e=>`<div class="e"><span>${e.note||"Saved"}<br><small style="color:var(--mu)">${e.time?h12(e.time)+" · ":""}${e.src?e.src+" "+(e.md||"")+" · ":""}${e.txn||"-"}</small></span><b style="color:${e.amt<0?"#f04438":"var(--ok)"}">${e.amt<0?"−":"+"}₹${Math.abs(e.amt)}</b><button data-i="${e.id}">✕</button></div>`).join(""):'<div class="hint">Em save cheyaledu</div>')+"</div>"}).join("")}
let mode="login";
const sha=async s=>{try{const b=await crypto.subtle.digest("SHA-256",new TextEncoder().encode("sb:"+s));return[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,"0")).join("")}catch(e){return s}};
function amode(m){mode=m;$("anm").style.display=m==="reg"?"":"none";$("ago").textContent=m==="reg"?"Create account":"Login";$("asw").textContent=m==="reg"?"Already account undi? Login":"Kotha account? Register";$("amsg").textContent=""}
$("asw").onclick=()=>amode(mode==="reg"?"login":"reg");
$("ago").onclick=async()=>{const m=$("amob").value.trim(),p=$("apin").value.trim(),us=users();
  if(!/^[6-9]\\d{9}$/.test(m))return $("amsg").textContent="Valid 10-digit mobile number enter chey";
  if(!/^\\d{4}$/.test(p))return $("amsg").textContent="4-digit PIN enter chey";
  const h=await sha(m+":"+p);
  if(mode==="reg"){if(us[m])return $("amsg").textContent="Ee number already registered, Login chey";
    const first=!Object.keys(us).length;us[m]={name:$("anm").value.trim()||"User",h};
    try{localStorage.setItem("rsbusers",JSON.stringify(us));const old=localStorage.getItem("rsb2");if(first&&old&&!localStorage.getItem("rsb2_"+m))localStorage.setItem("rsb2_"+m,old)}catch(e){}
  }else{if(!us[m])return $("amsg").textContent="Account ledu, Register chey";if(us[m].h!==h)return $("amsg").textContent="Wrong PIN, malli try chey"}
  U=m;try{localStorage.setItem("rsbuser",m)}catch(e){}loadS();$("apin").value="";$("auth").classList.remove("on");render();window.scrollTo(0,0)};
$("lo").onclick=()=>{if(confirm("Logout cheyyala?")){U="";try{localStorage.removeItem("rsbuser")}catch(e){}$("amob").value="";amode("login");$("auth").classList.add("on")}};
$("afg").onclick=()=>{const m=$("amob").value.trim(),us=users();if(!us[m])return $("amsg").textContent="Mundu registered mobile number enter chey";if(confirm("PIN reset ante ee account data anni delete avthayi. Continue?")){delete us[m];try{localStorage.setItem("rsbusers",JSON.stringify(us));localStorage.removeItem("rsb2_"+m)}catch(e){}amode("reg");$("amsg").textContent="Account reset ayindi, kotha PIN tho register chey"}};
amode("login");
$("dt").value=TD;render();if(!U)$("auth").classList.add("on");

// ==========================================================
// OPENING SPLASH ANIMATION ENGINE
// ==========================================================
function playSplashChime() {
  if (!window._snd) return;
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    if (ctx.state === 'suspended') ctx.resume();
    const notes = [
      { f: 523.25, t: 0.00, dur: 0.6, gain: 0.16, type: 'sine' },
      { f: 659.25, t: 0.12, dur: 0.6, gain: 0.16, type: 'triangle' },
      { f: 783.99, t: 0.24, dur: 0.7, gain: 0.18, type: 'sine' },
      { f: 1046.50, t: 0.36, dur: 0.9, gain: 0.22, type: 'triangle' },
      { f: 2093.00, t: 0.48, dur: 0.4, gain: 0.07, type: 'sine' },
      { f: 3135.96, t: 0.52, dur: 0.3, gain: 0.05, type: 'sine' }
    ];
    notes.forEach(n => {
      const start = ctx.currentTime + n.t;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = n.type;
      osc.frequency.setValueAtTime(n.f, start);
      gain.gain.setValueAtTime(0.0001, start);
      gain.gain.linearRampToValueAtTime(n.gain, start + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + n.dur);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(start);
      osc.stop(start + n.dur + 0.05);
    });
  } catch (e) {}
}

function spawnSplashCoins() {
  const container = $("splash-particles");
  if (!container) return;
  container.innerHTML = "";
  const icons = ["₹", "🪙", "💵", "✨", "💰", "⭐"];
  for (let i = 0; i < 16; i++) {
    const el = document.createElement("span");
    el.className = "splash-coin";
    el.textContent = icons[i % icons.length];
    el.style.left = (Math.random() * 90 + 5) + "%";
    el.style.animationDuration = (2.2 + Math.random() * 2) + "s";
    el.style.animationDelay = (Math.random() * 1.4) + "s";
    el.style.fontSize = (18 + Math.random() * 16) + "px";
    el.style.opacity = (0.5 + Math.random() * 0.5).toFixed(2);
    container.appendChild(el);
  }
}

let splashTimer = null;
function runSplashScreen(autoSkip = true) {
  const splash = $("splash-screen");
  if (!splash) return;
  splash.classList.remove("hide");
  spawnSplashCoins();
  
  const pbar = $("splash-progress-bar");
  const pstatus = $("splash-status");
  if (pbar) pbar.style.width = "0%";
  
  const stages = [
    { pct: "35%", text: "సేవింగ్స్ వాల్ట్ ఓపెన్ అవుతోంది..." },
    { pct: "75%", text: "సెక్యూర్ లాకర్ లోడ్ అవుతోంది..." },
    { pct: "100%", text: "స్వాగతం! Welcome to My Savings Bank 🎉" }
  ];
  
  let step = 0;
  if (splashTimer) clearInterval(splashTimer);
  
  setTimeout(playSplashChime, 250);
  
  splashTimer = setInterval(() => {
    if (step < stages.length) {
      if (pbar) pbar.style.width = stages[step].pct;
      if (pstatus) pstatus.textContent = stages[step].text;
      step++;
    } else {
      clearInterval(splashTimer);
      if (autoSkip) {
        setTimeout(closeSplashScreen, 400);
      }
    }
  }, 480);
}

function closeSplashScreen() {
  const splash = $("splash-screen");
  if (!splash) return;
  splash.classList.add("hide");
  if (splashTimer) clearInterval(splashTimer);
}

$("splash-skip-btn").onclick = (e) => {
  e.stopPropagation();
  closeSplashScreen();
};
$("splash-screen").onclick = () => {
  closeSplashScreen();
};
$("btn-replay-splash").onclick = () => {
  runSplashScreen(true);
};

runSplashScreen(true);

// Auto-update and registration
if("serviceWorker" in navigator) {
  navigator.serviceWorker.register("sw.js").then(reg => {
    reg.onupdatefound = () => {
      const w = reg.installing;
      if (w) {
        w.onstatechange = () => {
          if (w.state === "installed" && navigator.serviceWorker.controller) {
            window.location.reload();
          }
        };
      }
    };
  }).catch(()=>{});
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    window.location.reload();
  });
}

$("chk-update").onclick = async () => {
  const btn = $("chk-update");
  btn.textContent = "⏳ Updating to latest version...";
  try {
    if ("serviceWorker" in navigator) {
      const regs = await navigator.serviceWorker.getRegistrations();
      for (let r of regs) await r.update();
    }
    if (window.caches) {
      const keys = await caches.keys();
      await Promise.all(keys.map(k => caches.delete(k)));
    }
  } catch(e) {}
  window.location.reload(true);
};
</script>
</body>
</html>
'''

# 1. Write to root index.html
root_index = r'D:\my saving bank\index.html'
with open(root_index, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Updated {root_index}")

# 2. Write to savings-app-1/index.html
sub_index = r'D:\my saving bank\savings-app-1\index.html'
with open(sub_index, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Updated {sub_index}")

# 3. Update zip files
for zpath in [r'D:\my saving bank\savings-app-1.zip', r'D:\my saving bank\my-savings-bank-pwa.zip']:
    src_dir = r'D:\my saving bank\savings-app-1'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for r, d, files in os.walk(src_dir):
            for file in files:
                fp = os.path.join(r, file)
                z.write(fp, os.path.relpath(fp, src_dir))
    print(f"Repackaged {zpath}")

print("All files updated successfully!")
