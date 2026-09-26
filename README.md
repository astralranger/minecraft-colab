# 🎮 Minecraft Colab (Java Edition)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/astralranger/minecraft-colab/blob/main/MineColab.ipynb)
![Minecraft Version](https://img.shields.io/badge/Minecraft-26.3%20Java-brightgreen?logo=minecraft)
![Java Version](https://img.shields.io/badge/Java-25%20LTS-orange?logo=openjdk)
![Server Core](https://img.shields.io/badge/Server-Purpur-blueviolet)
![Tunnel](https://img.shields.io/badge/Tunnel-Playit.gg-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

Run a high-performance **Minecraft 26.3 Java Edition** server completely free on **Google Colab** with **zero lag**, **Java 25 support**, **automatic Google Drive backups**, and **instant tunneling (no port-forwarding needed)**.

---

## ⚡ What Makes This Version Better?

Traditional Google Colab Minecraft notebooks suffer from severe bottlenecks:
1. **Google Drive FUSE Latency**: Running directly on Google Drive causes world generation to stall for 10+ minutes and causes massive in-game chunk stutter.
2. **Java Version Incompatibility**: Minecraft 26.x requires **Java 25**. Older Colab scripts only install Java 21, crashing with `UnsupportedClassVersionError`.
3. **Playit Daemon IPC Hangs**: Recent Playit 1.0+ versions split into a daemon that halts waiting for IPC provisioning in headless environments.
4. **Cracked / TLauncher Lockout**: Fresh servers default to `online-mode=true` and `white-list=true`, preventing TLauncher players from joining.

### 🚀 Our Improvements:
* **⚡ Fast NVMe Local Caching**: Runs the server on Google Colab's native NVMe SSD. World generation finishes in **~15–20 seconds**, and TPS remains locked at **20.0 (0 lag)**.
* **💾 Automatic Google Drive Persistence**: 
  - Syncs your world from Google Drive into local storage on boot.
  - Background daemon auto-saves world progress to Google Drive every 5 minutes.
  - Full sync executes automatically when the server stops (`rsync -a --delete`).
* **☕ Automatic Java 25 (LTS) Provisioning**: Automatically installs official Eclipse Temurin Java 25 GA JDK.
* **🛡️ Purpur 26.3**: Pre-configured with Purpur (the highest-performing Paper fork with full Spigot/Paper plugin support and Aikar's tuned GC flags).
* **🌐 Battle-Tested Playit.gg (v0.15.26)**: Single-binary standalone tunnel that generates 1-click claim links directly in console and supports free permanent `.gl.joinmc.link` domains without typing port numbers.
* **🔓 TLauncher & Offline-Mode Ready**: `online-mode=false` and `white-list=false` configured out of the box.
* **👑 Automatic OP Admin**: Pre-configures operator admin permissions in `ops.json`.
* **🔄 1-Click All-in-One Standalone Launcher**: The Console cell is completely self-contained. It can be run immediately without having to run previous cells over and over.

---

## 📋 Quick Start Guide

### Step 1: Open in Google Colab
Click the badge below to open the notebook directly in your browser:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/astralranger/minecraft-colab/blob/main/MineColab.ipynb)

*(Or connect via your IDE's Google Colab / Jupyter extension).*

---

### Step 2: First-Time Setup
If this is your first time creating the server:
1. Run **Step 1 — `🛠️ Initialize Environment & Mount Google Drive`** to mount your Google Drive (`/content/drive/MyDrive/minecraft`).
2. Run **Step 2 — `🎯 Choose or Create Minecraft Server`** (pre-configured for **Purpur 26.3** and **Playit**). It downloads the server JAR and pre-accepts the EULA.

---

### Step 3: Configure Admin Privileges (OP & Gamemodes)
Run **Step 3 — `👑 Manage Server Admins & Player Permissions (OP)`**:
1. Enter your Minecraft player name (e.g. `skywalker`).
2. Choose **Permission Level 4** (Full Admin / Operator).
3. Set your target gamemode to `creative` (or `survival`).
4. Click **Run (▶)**!
   - Calculates the exact offline-mode UUID used by TLauncher / cracked clients.
   - Automatically writes permissions to `ops.json` on both Google Drive and local storage.
   - Automatically enables `allow-flight=true` in `server.properties` so creative flight never kicks you.
   - If the server is already running, it sends live `/op` and `/gamemode` commands immediately via local RCON!

---

### Step 4: Start Your Server
Run **Step 4 — `🚀 Launch Minecraft Server Console`**:

1. It initializes local NVMe storage, provisions Java 25 LTS, and launches the **Playit.gg** tunnel daemon.
2. In ~15 seconds, you will see:
   ```text
   [INFO]: Done (xx.xxxs)! For help, type "help"
   ```
3. **Your server is now live!**

## 🌐 Connecting to Your Server

### 1. Grab Your Playit Address
* **First Launch (Claim Link)**: Look at the console output for the claim banner:
  ```text
  Claim Link: https://playit.gg/claim/xxxx
  ```
  Open that link in your browser, click **Add Tunnel** $\rightarrow$ select **Minecraft (Java)**.
* **Get a Clean `.joinmc.link` Domain (No Port Needed!)**:
  In your [playit.gg dashboard](https://playit.gg/manage), click **Change domain** and select a free **`.gl.joinmc.link`** domain (e.g. `yourname.gl.joinmc.link`).
  Because of built-in SRV records, you and your friends **never have to remember or type port numbers**!
* **Using Direct Address**:
  You can also connect using:
  - `yourname.tun.ply.gg:PORT`
  - OR direct numeric IP: `147.185.221.214:PORT` *(bypasses all DNS issues)*.

### 2. Join in Minecraft
1. Open **Minecraft Java Edition 26.3** (Official launcher or TLauncher).
2. Go to **Multiplayer** $\rightarrow$ **Direct Connection** (or **Add Server**).
3. Paste your domain (e.g. `yourname.gl.joinmc.link` or `yourname.tun.ply.gg:PORT`).
4. Click **Join Server**!

---

## 👑 In-Game Admin Rights & Gamemode Commands

With Level 4 Operator status granted from **Step 3**, you can use all in-game commands in Minecraft:
* `/gamemode creative` — Switch to Creative Mode (flying, unlimited blocks).
* `/gamemode survival` — Switch back to Survival Mode.
* `/gamemode spectator` — Fly through walls and spectate the world.
* `F3 + F4` — Quickly toggle between game modes.
* `/teleport <player> <target>` — Teleport anywhere.
* `/time set day` / `/weather clear` — Control time and weather.
* `/stop` — Safely save the world and stop the server.

---

## 🛠️ Troubleshooting & FAQ

### `Connection refused: getsockopt`
* **Cause**: The Minecraft server is currently stopped or still booting up.
* **Fix**: Check the Console cell output in Colab. Wait until it prints `Done (...s)! For help, type "help"` before clicking connect in Minecraft.

### `Unknown Host`
* **Cause**: Missing the 5-digit port number, or local ISP DNS cache hasn't updated yet.
* **Fix**: 
  - Ensure you added the `:PORT` at the end of the `.tun.ply.gg` domain.
  - Or use the numeric IP: `147.185.221.214:PORT`.
  - Or create a free `.gl.joinmc.link` domain on the Playit dashboard.

### `Failed to verify username!`
* **Cause**: Player is connecting with TLauncher / cracked client while `online-mode=true`.
* **Fix**: This notebook automatically sets `online-mode=false` upon launch. If you modified it, verify `online-mode=false` in `server.properties`.

### Where is my world saved?
Your world files, region files, plugins, and configurations are permanently stored in your Google Drive under:
```text
Google Drive > MyDrive > minecraft > minecraft_26_3/
```
Even if your Colab session expires, your world is 100% safe in your Drive and will automatically sync back on next launch.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
