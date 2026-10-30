# 💰 My Savings Bank (నా సేవింగ్స్ బ్యాంక్)

> **Smart Personal Savings & Goals Vault** with Deep Blue Base Theme, Rupee Coins & Notes Logo, and Cinematic App Opening Animation with Audio Chime.

🌐 **Live Web & Mobile App**: [https://tpavans.github.io/my-savings-bank/](https://tpavans.github.io/my-savings-bank/)

![My Savings Bank App Icon](savings-app-1/icon-512.png)

---

## ✨ Features

- 🌟 **Deep Blue Base Theme**: Modern royal navy & midnight sapphire aesthetics (`#050d24` / `#07153b` / `#102a71`) with glowing gradients and executive glass cards.
- 🎬 **Cinematic Opening Animation**:
  - Dramatic 3D drop-in of the custom Rupee money logo with rotating gold halo and shine sweep.
  - Floating golden currency notes and coins (`₹`, `🪙`, `💵`, `✨`).
  - Web Audio API harmonic fintech chime sequence with coin clink.
  - Interactive loading progress bar with Telugu & English status updates.
  - "Start Saving ➔" instant skip or tap-anywhere dismissal.
  - Replay button (`✨ Splash`) in header to replay the animation anytime!
- 🪙 **Custom Indian Rupee App Icon**: High-resolution icons in 512x512, 192x192, maskable PWA, Apple touch, and multi-resolution Windows `icon.ico` formats.
- 📱 **Cross-Platform PWA**: Installable on Android, iPhone/iPad, Windows PC, and Mac directly from browser. Works 100% offline via Service Worker.
- 🖥️ **Windows Desktop App**: Runs natively via Electron with custom window frame, icon, and desktop launcher.
- 🎯 **Goals & Daily Tracker**: Create custom goals (e.g., Mobile Recharge, Emergency Fund, Gadget, Bike, Trip) with daily target calculation and days streak.
- 📊 **Visual Charts & Calendar**: 7-day/30-day savings charts and monthly calendar tracker.
- 🤖 **AI Money Coach**: Personalized money-saving and side-income advice tailored for students and young earners.
- 🎮 **Mini-Games & Challenges**: Coin catch game, daily spin, 52-week challenge, and streak freeze.
- 🔒 **Security & Multi-Account**: 4-digit PIN locker, account creation, passbook search, and local backup/restore.

---

## 🚀 Quick Start

### 1. Run as Desktop App (Electron)

```bash
# Clone the repository
git clone https://github.com/tpavans/my-savings-bank.git
cd my-savings-bank

# Install dependencies
npm install

# Launch desktop app
npm start
```

Or simply double-click `run-app.bat` on Windows!

### 2. Run in Web Browser / PWA

Open `savings-app-1/index.html` directly in any modern browser (Chrome, Edge, Safari, Firefox), or start a local server:

```bash
npm run web
```
Then visit `http://localhost:8080`.

---

## 📁 Project Structure

```text
my-savings-bank/
├── main.js                  # Electron desktop application main process
├── package.json             # NPM package scripts & configuration
├── run-app.bat              # 1-click Windows desktop runner
├── run-web.bat              # 1-click local web server runner
├── icon.ico                 # Multi-resolution Windows executable icon
├── icon-512.png             # Master 512x512 deep blue app icon
├── savings-app-1/           # Full Web / PWA App directory
│   ├── index.html           # Main application code with opening splash animation
│   ├── manifest.json        # PWA Web App manifest (Deep blue theme)
│   ├── sw.js                # Offline Service Worker cache
│   ├── app-logo.png         # Transparent cutout of money illustration
│   ├── icon-192.png         # 192x192 PWA icon
│   ├── icon-512.png         # 512x512 PWA icon
│   ├── icon-maskable-512.png# Adaptive Android icon
│   ├── apple-touch-icon.png # iOS Safari home screen icon
│   ├── favicon.png          # 32x32 favicon
│   ├── favicon.ico          # Browser favicon
│   └── icon.ico             # Windows shortcut icon
└── savings-app-1.zip        # Pre-packaged ready-to-deploy zip
```

---

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML5, CSS3 (Modern Flexbox/Grid, Animations), JavaScript ES6+
- **Audio**: Web Audio API (Synthesized fintech chords, 100% offline)
- **Desktop**: Electron 34 / Node.js
- **Assets**: Python Pillow (High-precision Lanczos anti-aliased icon rendering)

---

## 📜 License

ISC License - Made with ❤️ for smart savers.
