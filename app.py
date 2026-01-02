from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#000000">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>TITAN OS X | EXTREME</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        /* =========================================
           1. SYSTEM CORE VISUALS (HEAVY CSS)
           ========================================= */
        :root {
            --bg-deep: #020202;
            --bg-panel: #0a0b10;
            --hex-blue: #00f3ff;
            --hex-green: #0aff0a;
            --hex-red: #ff003c;
            --hex-gold: #ffd700;
            --scanline: rgba(0, 255, 255, 0.03);
            --glass: rgba(10, 20, 30, 0.6);
            --font-head: 'Orbitron', sans-serif;
            --font-code: 'Share Tech Mono', monospace;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }

        body {
            background-color: var(--bg-deep);
            color: var(--hex-blue);
            font-family: var(--font-code);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* CRT SCANLINE EFFECT */
        body::after {
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 999;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        /* BACKGROUND GRID ANIMATION */
        .cyber-grid {
            position: fixed; width: 200vw; height: 200vh;
            top: -50%; left: -50%;
            background-image: 
                linear-gradient(var(--scanline) 1px, transparent 1px),
                linear-gradient(90deg, var(--scanline) 1px, transparent 1px);
            background-size: 40px 40px;
            transform: perspective(500px) rotateX(60deg);
            animation: grid-fly 20s linear infinite;
            z-index: -1;
        }
        @keyframes grid-fly { 0% {transform: perspective(500px) rotateX(60deg) translateY(0);} 100% {transform: perspective(500px) rotateX(60deg) translateY(40px);} }

        /* =========================================
           2. BOOT SEQUENCE UI
           ========================================= */
        #boot-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 2000;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            font-family: var(--font-code); color: var(--hex-green);
        }
        .boot-log { width: 90%; max-width: 400px; font-size: 12px; line-height: 1.4; white-space: pre-wrap; }
        .cursor-blink { animation: blink 0.8s infinite; }
        @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0;} }

        /* =========================================
           3. ADVANCED 3D CUBE (THREE.JS STYLE CSS)
           ========================================= */
        .scene-container {
            width: 140px; height: 140px; margin: 40px auto;
            perspective: 800px;
        }
        .cube-3d {
            width: 100%; height: 100%; position: relative;
            transform-style: preserve-3d;
            animation: rotate-cube 12s infinite linear;
        }
        .cube-face {
            position: absolute; width: 140px; height: 140px;
            border: 2px solid var(--hex-blue);
            background: rgba(0, 243, 255, 0.15);
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.2) inset;
            display: flex; align-items: center; justify-content: center;
            font-size: 14px; color: #fff; font-weight: bold;
            backface-visibility: visible;
            background-size: cover; background-position: center;
            transition: border-color 0.3s, background-image 0.5s;
        }
        /* Cube Transforms */
        .face-f { transform: rotateY(0deg) translateZ(70px); }
        .face-b { transform: rotateY(180deg) translateZ(70px); }
        .face-r { transform: rotateY(90deg) translateZ(70px); }
        .face-l { transform: rotateY(-90deg) translateZ(70px); }
        .face-t { transform: rotateX(90deg) translateZ(70px); }
        .face-bt { transform: rotateX(-90deg) translateZ(70px); }

        @keyframes rotate-cube { 
            0% {transform: rotateX(0deg) rotateY(0deg);} 
            100% {transform: rotateX(360deg) rotateY(360deg);} 
        }

        /* =========================================
           4. MAIN LAYOUT & COMPONENTS
           ========================================= */
        .main-viewport {
            flex: 1; overflow-y: auto; padding: 20px; padding-bottom: 90px;
            opacity: 0; transition: opacity 1s;
        }
        .main-viewport.visible { opacity: 1; }

        .titan-card {
            background: var(--bg-panel);
            border: 1px solid #333;
            border-left: 4px solid var(--hex-blue);
            padding: 20px; margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative; overflow: hidden;
        }
        .titan-card::before {
            content: ''; position: absolute; top:0; right:0; width: 20px; height: 20px;
            border-top: 2px solid var(--hex-blue); border-right: 2px solid var(--hex-blue);
        }
        
        .card-header {
            display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 10px; margin-bottom: 15px;
        }
        .card-title {
            font-family: var(--font-head); font-size: 18px; letter-spacing: 2px;
            color: #fff; text-shadow: 0 0 10px var(--hex-blue);
            display: flex; align-items: center; gap: 10px;
        }

        /* Inputs */
        .cyber-input {
            width: 100%; background: #050505; border: 1px solid #333;
            color: var(--hex-green); padding: 15px; font-family: var(--font-code);
            margin-bottom: 15px; font-size: 14px; letter-spacing: 1px;
            transition: 0.3s;
        }
        .cyber-input:focus { border-color: var(--hex-green); box-shadow: 0 0 15px rgba(10, 255, 10, 0.2); }

        /* Buttons */
        .cyber-btn {
            width: 100%; padding: 18px; background: rgba(0, 243, 255, 0.1);
            border: 1px solid var(--hex-blue); color: var(--hex-blue);
            font-family: var(--font-head); font-weight: 700; font-size: 16px;
            cursor: pointer; text-transform: uppercase; letter-spacing: 3px;
            position: relative; overflow: hidden; transition: 0.3s;
        }
        .cyber-btn:hover { background: var(--hex-blue); color: #000; box-shadow: 0 0 25px var(--hex-blue); }
        .cyber-btn:active { transform: scale(0.98); }

        /* =========================================
           5. ADVANCED RADAR (SVG)
           ========================================= */
        .radar-container {
            width: 280px; height: 280px; margin: 0 auto; position: relative;
            background: radial-gradient(circle, #001100 0%, #000000 70%);
            border-radius: 50%; border: 4px solid #333;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.1);
            overflow: hidden;
        }
        .radar-grid-svg {
            position: absolute; top:0; left:0; width: 100%; height: 100%;
            opacity: 0.4;
        }
        .radar-sweep {
            position: absolute; top:0; left:0; width: 100%; height: 100%;
            background: conic-gradient(transparent 270deg, rgba(0,255,0,0.6) 360deg);
            border-radius: 50%; animation: radar-spin 3s infinite linear;
        }
        @keyframes radar-spin { from{transform: rotate(0deg);} to{transform: rotate(360deg);} }
        
        .radar-blip {
            position: absolute; width: 32px; height: 32px; border-radius: 50%;
            border: 2px solid #fff; background-size: cover; background-position: center;
            box-shadow: 0 0 10px #fff; z-index: 10;
            display: flex; align-items: center; justify-content: center;
            transition: all 0.5s ease-out;
        }
        .blip-tag {
            position: absolute; top: -15px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.8); color: var(--hex-green);
            padding: 2px 5px; font-size: 9px; white-space: nowrap; border: 1px solid var(--hex-green);
        }

        /* =========================================
           6. ENHANCED VAULT (GRID)
           ========================================= */
        .vault-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;
        }
        .vault-item {
            background: #000; border: 1px solid #333; position: relative;
            height: 150px; overflow: hidden; transition: 0.3s;
            cursor: pointer;
        }
        .vault-item:hover { border-color: var(--hex-gold); }
        .vault-item img { width: 100%; height: 100%; object-fit: cover; opacity: 0.7; transition: 0.3s; }
        .vault-item:hover img { opacity: 1; transform: scale(1.1); }
        .vault-meta {
            position: absolute; bottom: 0; left: 0; right: 0;
            background: linear-gradient(0deg, #000, transparent);
            padding: 5px; font-size: 10px; color: #fff;
            display: flex; justify-content: space-between;
        }

        /* =========================================
           7. TARGET OPS
           ========================================= */
        .target-timeline {
            border-left: 2px solid var(--hex-red); padding-left: 20px; margin-left: 10px;
        }
        .timeline-event {
            position: relative; margin-bottom: 20px;
        }
        .timeline-event::before {
            content:''; position: absolute; left: -26px; top: 0; width: 10px; height: 10px;
            background: #000; border: 2px solid var(--hex-red); border-radius: 50%;
        }
        .event-time { color: #666; font-size: 11px; margin-bottom: 4px; }
        .event-body { color: #ddd; font-size: 13px; background: rgba(255,0,0,0.05); padding: 10px; border: 1px solid rgba(255,0,0,0.2); }

        /* =========================================
           8. NAVIGATION BAR
           ========================================= */
        .nav-dock {
            position: fixed; bottom: 0; left: 0; right: 0; height: 80px;
            background: rgba(2, 2, 2, 0.95); backdrop-filter: blur(10px);
            border-top: 1px solid #333; display: flex; justify-content: space-around;
            align-items: center; z-index: 1000;
        }
        .nav-item {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            color: #444; width: 60px; height: 60px; border-radius: 10px;
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .nav-icon-svg { width: 24px; height: 24px; fill: currentColor; margin-bottom: 5px; }
        .nav-text { font-size: 9px; font-family: var(--font-head); letter-spacing: 1px; }
        
        .nav-item.active {
            color: var(--hex-blue); background: rgba(0, 243, 255, 0.05);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.1); transform: translateY(-10px);
        }
        .nav-item.active .nav-icon-svg { filter: drop-shadow(0 0 5px var(--hex-blue)); }

        /* UTILS */
        .page { display: none; }
        .page.active { display: block; animation: slide-up 0.4s ease-out; }
        @keyframes slide-up { from {opacity:0; transform: translateY(30px);} to {opacity:1; transform:translateY(0);} }
        .hidden { display: none !important; }
        .text-neon { color: var(--hex-blue); }
        .text-alert { color: var(--hex-red); }

    </style>
</head>
<body>

<!-- BOOT SCREEN -->
<div id="boot-screen">
    <div class="boot-log" id="bootLog"></div>
</div>

<!-- BACKGROUND -->
<div class="cyber-grid"></div>

<!-- NAV DOCK (Moved to top for visibility in code structure, fixed at bottom in CSS) -->
<div class="nav-dock hidden" id="navBar">
    <div class="nav-item active" onclick="app.nav('p-home', this)">
        <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M12 2L2 12h3v8h6v-6h2v6h6v-8h3L12 2zm0 2.8L19.2 12H17v8h-4v-6H9v6H7v-8H4.8L12 4.8z"/></svg>
        <span class="nav-text">CORE</span>
    </div>
    <div class="nav-item" onclick="app.nav('p-radar', this)">
        <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5.5-2.5l7.51-3.49L17.5 6.5 9.99 9.99 6.5 17.5zm5.5-6.6c.61 0 1.1.49 1.1 1.1s-.49 1.1-1.1 1.1-1.1-.49-1.1-1.1.49-1.1 1.1-1.1z"/></svg>
        <span class="nav-text">RADAR</span>
    </div>
    <div class="nav-item" onclick="app.nav('p-target', this)">
        <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
        <span class="nav-text">OPS</span>
    </div>
    <div class="nav-item" onclick="app.nav('p-vault', this)">
        <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>
        <span class="nav-text">VAULT</span>
    </div>
</div>

<div class="main-viewport" id="viewport">
    
    <!-- 1. HOME / LOGIN / DASHBOARD -->
    <div id="p-home" class="page active">
        <!-- 3D CUBE CONTAINER -->
        <div class="scene-container">
            <div class="cube-3d" id="titanCube">
                <div class="cube-face face-f">TITAN</div>
                <div class="cube-face face-b">SEC</div>
                <div class="cube-face face-l">NET</div>
                <div class="cube-face face-r">DATA</div>
                <div class="cube-face face-t">SYS</div>
                <div class="cube-face face-bt">X</div>
            </div>
        </div>

        <!-- LOGIN FORM -->
        <div id="login-panel" class="titan-card">
            <div class="card-header">
                <span class="card-title">
                    <svg style="width:20px;height:20px;fill:var(--hex-blue)" viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
                    SECURE UPLINK
                </span>
            </div>
            <input type="text" id="ipt-room" class="cyber-input" value="ملتقى🥂العرب" placeholder="TARGET FREQUENCY (ROOM)">
            <textarea id="ipt-creds" class="cyber-input" rows="3" placeholder="AGENT LIST (Format: User#Pass@User#Pass)"></textarea>
            <button class="cyber-btn" onclick="app.initiate()">INITIALIZE SEQUENCE</button>
        </div>

        <!-- CONNECTED DASHBOARD (Replaces Login) -->
        <div id="dash-panel" class="titan-card hidden">
            <div class="card-header">
                <span class="card-title" style="color:var(--hex-green)">
                    <svg style="width:20px;height:20px;fill:var(--hex-green)" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                    SYSTEM ENGAGED
                </span>
            </div>
            <div style="font-size:12px; color:#888; margin-bottom:15px;">UPLINK ESTABLISHED. MONITORING ACTIVE.</div>
            <div id="bot-status-log" style="font-family:var(--font-code); font-size:11px; color:var(--hex-blue);"></div>
            <div style="margin-top:20px; border-top:1px solid #333; padding-top:10px;">
                <button class="cyber-btn" style="border-color:var(--hex-red); color:var(--hex-red)" onclick="location.reload()">TERMINATE LINK</button>
            </div>
        </div>
    </div>

    <!-- 2. RADAR -->
    <div id="p-radar" class="page">
        <div class="titan-card">
            <div class="card-header">
                <span class="card-title">SONAR TRACKING</span>
                <span id="radar-counter" style="color:var(--hex-green); font-size:14px;">0 HOSTILES</span>
            </div>
            <div class="radar-container" id="radar-scope">
                <!-- SVG Grid -->
                <svg class="radar-grid-svg">
                    <circle cx="140" cy="140" r="35" stroke="#0f0" stroke-width="1" fill="none"/>
                    <circle cx="140" cy="140" r="70" stroke="#0f0" stroke-width="1" fill="none"/>
                    <circle cx="140" cy="140" r="105" stroke="#0f0" stroke-width="1" fill="none"/>
                    <line x1="140" y1="0" x2="140" y2="280" stroke="#0f0" stroke-width="1"/>
                    <line x1="0" y1="140" x2="280" y2="140" stroke="#0f0" stroke-width="1"/>
                </svg>
                <div class="radar-sweep"></div>
                <!-- BLIPS GO HERE -->
            </div>
        </div>
    </div>

    <!-- 3. TARGET OPS -->
    <div id="p-target" class="page">
        <div class="titan-card" style="border-left-color: var(--hex-red);">
            <div class="card-header">
                <span class="card-title" style="color:var(--hex-red)">TARGET DOSSIER</span>
            </div>
            <select id="tgt-select" class="cyber-input" onchange="app.loadTarget(this.value)">
                <option value="">SELECT TARGET...</option>
            </select>
            
            <div id="tgt-data" class="hidden">
                <div style="display:flex; gap:15px; margin-bottom:15px;">
                    <img id="t-avatar" src="" style="width:60px; height:60px; border:1px solid var(--hex-red);">
                    <div>
                        <div id="t-name" style="font-size:16px; font-weight:bold; color:var(--hex-red)">UNKNOWN</div>
                        <div id="t-seen" style="font-size:11px; color:#888;">LAST SEEN: NOW</div>
                    </div>
                </div>
                <div class="target-timeline" id="t-timeline"></div>
                <button class="cyber-btn" onclick="app.exportLogs()">EXPORT LOGS (.TXT)</button>
            </div>
        </div>
    </div>

    <!-- 4. VAULT -->
    <div id="p-vault" class="page">
        <div class="titan-card">
            <div class="card-header"><span class="card-title">EVIDENCE VAULT</span></div>
            <div class="vault-grid" id="vault-box"></div>
        </div>
    </div>

</div>

<script>
    /* =========================================
       TITAN CORE ENGINE (JS)
       ========================================= */
    
    class AudioEngine {
        constructor() {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }
        playTone(freq, type, duration) {
            if(this.ctx.state === 'suspended') this.ctx.resume();
            let osc = this.ctx.createOscillator();
            let gain = this.ctx.createGain();
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
            gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        }
        beep() { this.playTone(1200, 'sine', 0.1); }
        alert() { this.playTone(600, 'sawtooth', 0.3); }
        boot() { this.playTone(100, 'square', 0.5); }
    }

    class TitanSystem {
        constructor() {
            this.wsUrl = "wss://chatp.net:5333/server";
            this.bots = [];
            this.users = new Map(); // Stores all user data
            this.targets = new Map(); // Stores target specific logs
            this.audio = new AudioEngine();
            this.activeImages = []; // For Cube
            this.wakeLock = null;
        }

        // --- 1. BOOT SEQUENCE ---
        boot() {
            let log = document.getElementById('bootLog');
            let lines = [
                "TITAN KERNEL v10.0.4 LOADING...",
                "MOUNTING FILE SYSTEM... [OK]",
                "INITIALIZING NETWORK DRIVERS... [OK]",
                "LOADING GRAPHICS ENGINE (THREE.JS CSS)... [OK]",
                "BYPASSING SECURITY PROTOCOLS...",
                "SYSTEM READY."
            ];
            let i = 0;
            let interval = setInterval(() => {
                if(i >= lines.length) {
                    clearInterval(interval);
                    setTimeout(() => {
                        document.getElementById('boot-screen').style.display = 'none';
                        document.getElementById('viewport').classList.add('visible');
                        this.audio.boot();
                    }, 500);
                    return;
                }
                log.innerText += lines[i] + "\n";
                this.audio.playTone(800 + (i*100), 'square', 0.05);
                i++;
            }, 600);
        }

        // --- 2. NETWORK HANDLER (ROBUST) ---
        initiate() {
            this.requestWakeLock();
            let room = document.getElementById('ipt-room').value;
            let creds = document.getElementById('ipt-creds').value;
            
            if(!creds.includes("#")) { alert("INVALID CREDENTIALS"); return; }
            
            // UI Switch
            document.getElementById('login-panel').classList.add('hidden');
            document.getElementById('dash-panel').classList.remove('hidden');
            document.getElementById('navBar').classList.remove('hidden');

            let list = creds.split("@");
            list.forEach((c, idx) => {
                if(c.includes("#")) {
                    let [u, p] = c.split("#");
                    this.spawnBot(u.trim(), p.trim(), room);
                }
            });
        }

        spawnBot(user, pass, room) {
            let ws = new WebSocket(this.wsUrl);
            let botLog = document.getElementById('bot-status-log');
            
            ws.onopen = () => {
                ws.send(JSON.stringify({handler:"login", id:this.genId(), username:user, password:pass}));
            };

            ws.onmessage = (e) => {
                let d = JSON.parse(e.data);
                
                // Auth & Join Logic
                if(d.handler === "login_event" && d.type === "success") {
                    ws.send(JSON.stringify({handler:"room_join", id:this.genId(), name:room}));
                }
                if(d.handler === "room_event" && d.type === "room_joined") {
                    botLog.innerHTML += `<div style="color:var(--hex-green)">> AGENT [${user}] UPLINKED TO ${room}</div>`;
                    this.audio.beep();
                }

                // Global Packet Processing
                this.processPacket(d);
            };

            ws.onclose = () => {
                botLog.innerHTML += `<div style="color:var(--hex-red)">> CONNECTION LOST [${user}]. RETRYING...</div>`;
                setTimeout(() => this.spawnBot(user, pass, room), 3000); // Auto Retry
            };

            this.bots.push(ws);
        }

        // --- 3. DATA PROCESSOR ---
        processPacket(d) {
            let u = d.username || d.from;
            let icon = d.icon || d.avatar_url;
            
            if(!u) return;

            // Fix Avatar URL
            if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;

            // Update User DB
            if(!this.users.has(u)) {
                // New User Found
                this.users.set(u, {
                    name: u, icon: icon || `https://ui-avatars.com/api/?name=${u}`,
                    pos: { x: Math.random()*200, y: Math.random()*200 }, // Radar Coords
                    logs: []
                });
                this.renderRadarBlip(u);
                this.updateTargetSelect(u);
                
                // Add to Cube Rotation
                if(icon) this.activeImages.push(icon);
            }
            
            // Log Event
            let userObj = this.users.get(u);
            if(d.type === "text" || d.type === "image") {
                let msg = d.body;
                if(d.type === "image") msg = "[IMAGE SENT]";
                
                userObj.logs.push({time: new Date().toLocaleTimeString(), msg: msg});
                this.users.set(u, userObj);

                // Update UI if viewing this target
                let sel = document.getElementById('tgt-select').value;
                if(sel === u) this.renderTargetTimeline(u);
            }

            // Vault Logic
            if(d.type === "image" || (d.body && d.body.match(/http.*(jpg|png|jpeg)/i))) {
                let url = d.type==="image" ? "https://chatp.net"+d.url : d.body.match(/http.*(jpg|png|jpeg)/i)[0];
                this.renderVaultItem(u, url);
            }
        }

        // --- 4. VISUAL RENDERERS ---

        // Radar
        renderRadarBlip(name) {
            let u = this.users.get(name);
            let scope = document.getElementById('radar-scope');
            
            let blip = document.createElement('div');
            blip.className = 'radar-blip';
            blip.style.backgroundImage = `url(${u.icon})`;
            // Center is 140,140. Map random x,y to radial style
            let angle = Math.random() * 6.28;
            let dist = Math.random() * 100; // Radius
            let left = 140 + Math.cos(angle) * dist - 16;
            let top = 140 + Math.sin(angle) * dist - 16;
            
            blip.style.left = left + 'px';
            blip.style.top = top + 'px';
            
            let tag = document.createElement('div');
            tag.className = 'blip-tag';
            tag.innerText = name;
            blip.appendChild(tag);
            
            scope.appendChild(blip);
            
            document.getElementById('radar-counter').innerText = `${this.users.size} HOSTILES`;
        }

        // Cube Animation (Updates Faces)
        updateCubeFaces() {
            if(this.activeImages.length < 1) return;
            let faces = document.querySelectorAll('.cube-face');
            let randomFace = faces[Math.floor(Math.random() * faces.length)];
            let randomImg = this.activeImages[Math.floor(Math.random() * this.activeImages.length)];
            
            randomFace.style.backgroundImage = `url(${randomImg})`;
            randomFace.innerText = ""; 
            randomFace.style.borderColor = "#fff";
        }

        // Vault
        renderVaultItem(user, url) {
            let box = document.getElementById('vault-box');
            let html = `
                <div class="vault-item" onclick="window.open('${url}')">
                    <img src="${url}">
                    <div class="vault-meta">
                        <span>${user}</span>
                        <span>${new Date().toLocaleTimeString()}</span>
                    </div>
                </div>
            `;
            box.insertAdjacentHTML('afterbegin', html);
        }

        // Target Ops
        updateTargetSelect(name) {
            let sel = document.getElementById('tgt-select');
            let opt = document.createElement('option');
            opt.value = name; opt.innerText = name;
            sel.appendChild(opt);
        }

        loadTarget(name) {
            if(!name) { document.getElementById('tgt-data').classList.add('hidden'); return; }
            document.getElementById('tgt-data').classList.remove('hidden');
            
            let u = this.users.get(name);
            document.getElementById('t-name').innerText = u.name;
            document.getElementById('t-avatar').src = u.icon;
            
            this.renderTargetTimeline(name);
        }

        renderTargetTimeline(name) {
            let u = this.users.get(name);
            let tl = document.getElementById('t-timeline');
            tl.innerHTML = "";
            
            // Show last 20 logs reversed
            u.logs.slice(-20).reverse().forEach(l => {
                let html = `
                    <div class="timeline-event">
                        <div class="event-time">${l.time}</div>
                        <div class="event-body">${l.msg}</div>
                    </div>
                `;
                tl.insertAdjacentHTML('beforeend', html);
            });
        }
        
        exportLogs() {
            let name = document.getElementById('tgt-select').value;
            if(!name) return;
            let u = this.users.get(name);
            let txt = `TITAN OS SURVEILLANCE LOG\nTARGET: ${name}\nTIME: ${new Date().toLocaleString()}\n----------------------------\n`;
            u.logs.forEach(l => { txt += `[${l.time}] ${l.msg}\n`; });
            
            let blob = new Blob([txt], {type: "text/plain"});
            let a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = `TARGET_${name}.txt`;
            a.click();
        }

        // Utils
        nav(pid, el) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById(pid).classList.add('active');
            el.classList.add('active');
            this.audio.beep();
        }
        
        genId() { return Math.random().toString(36).substr(2, 9); }
        
        async requestWakeLock() {
            try { if('wakeLock' in navigator) this.wakeLock = await navigator.wakeLock.request('screen'); }
            catch(e) { console.log(e); }
        }
    }

    // --- INIT ---
    const app = new TitanSystem();
    
    // Start Cube Randomizer
    setInterval(() => app.updateCubeFaces(), 2000);
    
    // Start Boot
    window.onload = () => app.boot();

    // Anti-Disconnect Visibility Handler
    document.addEventListener("visibilitychange", () => {
        if(document.visibilityState === 'visible') {
            app.requestWakeLock();
            // Reconnection logic is handled by ws.onclose
        }
    });

</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)