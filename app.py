from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS: OMEGA</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        /* ==========================================================================
           1. CORE SYSTEM STYLES (HEAVY UI)
           ========================================================================== */
        :root {
            --hex-bg: #030303;
            --hex-panel: #0a0b0e;
            --hex-cyan: #00f0ff;
            --hex-green: #0aff0a;
            --hex-red: #ff003c;
            --hex-dim: #444;
            --glass: rgba(10, 20, 30, 0.9);
            --font-ui: 'Orbitron', sans-serif;
            --font-code: 'Share Tech Mono', monospace;
            --scanline: rgba(0, 255, 255, 0.02);
        }

        * { box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; outline: none; }

        body {
            background-color: var(--hex-bg);
            color: var(--hex-cyan);
            font-family: var(--font-ui);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* CRT SCANLINE & FLICKER EFFECT */
        body::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 2px, 3px 100%;
            pointer-events: none; z-index: 9999;
        }

        /* CANVAS BACKGROUND */
        #bg-canvas {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1; opacity: 0.4;
        }

        /* SCROLLBARS */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #000; }
        ::-webkit-scrollbar-thumb { background: var(--hex-cyan); }

        /* ==========================================================================
           2. COMPONENT LIBRARY
           ========================================================================== */
        
        /* PAGES SYSTEM */
        .screen {
            display: none; height: 100%; padding: 15px; overflow-y: auto; padding-bottom: 90px;
            opacity: 0; transition: opacity 0.4s ease-in-out;
        }
        .screen.active { display: block; opacity: 1; }

        /* CARDS (GLASSMORPHISM) */
        .titan-panel {
            background: var(--hex-panel);
            border: 1px solid #1f1f1f;
            border-left: 4px solid var(--hex-cyan);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 4px; padding: 20px; margin-bottom: 20px;
            position: relative; overflow: hidden;
        }
        .titan-panel::before {
            content: ''; position: absolute; top: 0; right: 0; 
            width: 20px; height: 20px; 
            border-top: 2px solid var(--hex-cyan); border-right: 2px solid var(--hex-cyan);
        }

        .panel-header {
            font-size: 14px; letter-spacing: 2px; color: var(--hex-cyan);
            border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 15px;
            display: flex; justify-content: space-between; align-items: center;
        }

        /* INPUTS */
        .cyber-input {
            width: 100%; background: #050505; border: 1px solid #333;
            color: #fff; padding: 15px; font-family: var(--font-code);
            margin-bottom: 15px; font-size: 14px; letter-spacing: 1px;
            transition: 0.3s;
        }
        .cyber-input:focus { border-color: var(--hex-cyan); box-shadow: 0 0 15px rgba(0, 243, 255, 0.1); }

        /* BUTTONS */
        .cyber-btn {
            width: 100%; padding: 16px; 
            background: linear-gradient(90deg, rgba(0,243,255,0.1) 0%, rgba(0,0,0,0) 100%);
            border: 1px solid var(--hex-cyan); color: var(--hex-cyan);
            font-family: var(--font-ui); font-weight: bold; cursor: pointer;
            text-transform: uppercase; letter-spacing: 3px;
            position: relative; overflow: hidden; transition: 0.3s;
        }
        .cyber-btn:hover { background: var(--hex-cyan); color: #000; box-shadow: 0 0 20px var(--hex-cyan); }
        .cyber-btn:active { transform: scale(0.98); }

        .btn-demo { border-color: var(--hex-green); color: var(--hex-green); margin-top: 10px; }

        /* ==========================================================================
           3. ADVANCED 3D CUBE (LOGIN)
           ========================================================================== */
        .cube-viewport { width: 120px; height: 120px; margin: 30px auto; perspective: 1000px; }
        .cube-core {
            width: 100%; height: 100%; position: relative; transform-style: preserve-3d;
            animation: rotateCore 12s infinite linear;
        }
        .cube-face {
            position: absolute; width: 120px; height: 120px;
            border: 2px solid var(--hex-cyan); background: rgba(0, 243, 255, 0.1);
            box-shadow: inset 0 0 30px rgba(0, 243, 255, 0.2);
            display: flex; align-items: center; justify-content: center;
            font-size: 14px; color: #fff; text-shadow: 0 0 10px var(--hex-cyan);
            background-size: cover; background-position: center;
        }
        .cf-1 { transform: rotateY(0deg) translateZ(60px); }
        .cf-2 { transform: rotateY(180deg) translateZ(60px); }
        .cf-3 { transform: rotateY(90deg) translateZ(60px); }
        .cf-4 { transform: rotateY(-90deg) translateZ(60px); }
        .cf-5 { transform: rotateX(90deg) translateZ(60px); }
        .cf-6 { transform: rotateX(-90deg) translateZ(60px); }
        
        @keyframes rotateCore { 0% {transform: rotateX(0) rotateY(0);} 100% {transform: rotateX(360deg) rotateY(360deg);} }

        /* ==========================================================================
           4. WARSHIP RADAR (HEAVY SVG)
           ========================================================================== */
        .radar-system {
            width: 280px; height: 280px; margin: 0 auto; border-radius: 50%;
            border: 4px solid #1a1a1a; background: radial-gradient(#001100 0%, #000000 80%);
            position: relative; overflow: hidden;
            box-shadow: 0 0 40px rgba(0, 243, 255, 0.1);
        }
        .radar-grid {
            position: absolute; inset: 0; 
            background-image: 
                radial-gradient(transparent 65%, rgba(0,255,0,0.2) 70%, transparent 71%),
                linear-gradient(0deg, transparent 49%, rgba(0,255,0,0.1) 50%, transparent 51%),
                linear-gradient(90deg, transparent 49%, rgba(0,255,0,0.1) 50%, transparent 51%);
            border-radius: 50%;
        }
        .radar-sweep {
            position: absolute; inset: 0; border-radius: 50%;
            background: conic-gradient(transparent 270deg, rgba(0, 255, 0, 0.5));
            animation: radarSpin 4s infinite linear;
        }
        @keyframes radarSpin { to { transform: rotate(360deg); } }
        
        .warship {
            position: absolute; width: 40px; height: 40px;
            transform: translate(-50%, -50%);
            display: flex; flex-direction: column; align-items: center;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 10;
        }
        .warship-icon {
            width: 26px; height: 26px; border-radius: 50%; border: 1px solid #fff;
            box-shadow: 0 0 10px #fff; background: #000; object-fit: cover;
        }
        .warship-marker {
            width: 0; height: 0; border-left: 5px solid transparent; 
            border-right: 5px solid transparent; border-bottom: 10px solid var(--hex-green);
            margin-top: -3px; filter: drop-shadow(0 0 5px var(--hex-green));
        }
        .warship-tag { font-size: 9px; color: var(--hex-green); background: rgba(0,0,0,0.8); padding: 2px 4px; border-radius: 4px; margin-top: 2px; }

        /* ==========================================================================
           5. PRO CHAT INTERFACE
           ========================================================================== */
        .terminal-feed { height: 450px; overflow-y: auto; padding-right: 5px; }
        .chat-entry { display: flex; gap: 12px; margin-bottom: 15px; animation: slideEntry 0.3s ease-out; }
        @keyframes slideEntry { from{opacity:0; transform:translateX(-20px);} to{opacity:1; transform:translateX(0);} }
        
        .entry-avatar { width: 45px; height: 45px; border-radius: 4px; border: 1px solid #444; }
        .entry-body {
            flex: 1; background: rgba(255,255,255,0.03); border: 1px solid #222;
            padding: 12px; border-radius: 0 12px 12px 12px; position: relative;
        }
        .entry-meta { display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 6px; }
        .entry-user { color: var(--hex-cyan); font-weight: bold; letter-spacing: 1px; }
        .entry-content { font-family: var(--font-code); font-size: 13px; color: #ddd; line-height: 1.5; word-break: break-all; }

        /* ==========================================================================
           6. VAULT & NAVIGATION
           ========================================================================== */
        .vault-matrix { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .vault-file {
            background: #000; border: 1px solid #333; height: 140px; position: relative;
            cursor: pointer; transition: 0.3s;
        }
        .vault-file:hover { border-color: var(--hex-cyan); transform: scale(1.02); }
        .vault-file img { width: 100%; height: 100%; object-fit: cover; opacity: 0.8; }
        .vault-label {
            position: absolute; bottom: 0; left: 0; width: 100%;
            background: rgba(0,0,0,0.9); color: #fff; font-size: 10px; padding: 5px;
            font-family: var(--font-code);
        }

        /* NAVIGATION DOCK */
        .omega-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 80px;
            background: rgba(5, 5, 5, 0.98); border-top: 1px solid #333;
            display: none; justify-content: space-around; align-items: center;
            z-index: 100; box-shadow: 0 -10px 30px rgba(0,0,0,0.9);
        }
        .nav-link {
            display: flex; flex-direction: column; align-items: center; gap: 5px;
            color: #555; width: 60px; padding: 5px; transition: 0.3s;
        }
        /* INLINE SVG ICONS FOR HEAVY LOOK */
        .nav-svg { width: 24px; height: 24px; fill: currentColor; }
        .nav-txt { font-size: 10px; font-weight: bold; letter-spacing: 1px; }
        
        .nav-link.active { color: var(--hex-cyan); transform: translateY(-8px); }
        .nav-link.active .nav-svg { filter: drop-shadow(0 0 8px var(--hex-cyan)); }

        /* BOT STATUS ROW */
        .agent-status {
            display: flex; justify-content: space-between; align-items: center;
            background: #0e0e0e; padding: 12px; margin-bottom: 8px; border-left: 3px solid #333;
        }
        .agent-status.online { border-color: var(--hex-green); background: rgba(0,255,10,0.05); }
        .agent-status.offline { border-color: var(--hex-red); }

        /* BOOT OVERLAY */
        #boot-seq {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 2000; display: flex; flex-direction: column;
            justify-content: center; align-items: center; font-family: var(--font-code);
            color: var(--hex-green); font-size: 12px; padding: 20px;
        }
    </style>
</head>
<body>

{% raw %}
    <!-- DYNAMIC BACKGROUND -->
    <canvas id="bg-canvas"></canvas>

    <!-- BOOT SEQUENCE -->
    <div id="boot-seq">
        <div id="boot-txt">INITIALIZING OMEGA KERNEL...</div>
        <div style="margin-top:10px; width:200px; height:2px; background:#333;">
            <div id="boot-bar" style="width:0%; height:100%; background:var(--hex-green); transition: width 3s;"></div>
        </div>
        <button id="skip-boot" onclick="sys.skipBoot()" style="margin-top:20px; background:none; border:1px solid #444; color:#666; display:none;">[ SYSTEM OVERRIDE ]</button>
    </div>

    <!-- 1. LOGIN SCREEN -->
    <div id="pg-login" class="screen active">
        <div style="text-align:center; padding-top:40px;">
            <div class="cube-viewport">
                <div class="cube-core" id="loginCube">
                    <div class="cube-face cf-1">TITAN</div>
                    <div class="cube-face cf-2">OMEGA</div>
                    <div class="cube-face cf-3">SYS</div>
                    <div class="cube-face cf-4">SEC</div>
                    <div class="cube-face cf-5"></div>
                    <div class="cube-face cf-6"></div>
                </div>
            </div>
            <h1 style="color:var(--hex-cyan); letter-spacing:6px; text-shadow:0 0 15px var(--hex-cyan);">TITAN OMEGA</h1>
            <p style="font-size:12px; color:#666; font-family:var(--font-code);">ENCRYPTED UPLINK PROTOCOL v9.0</p>
        </div>

        <div class="titan-panel" style="margin-top:30px;">
            <div class="panel-header">IDENTITY VERIFICATION</div>
            <label style="font-size:10px; color:#666;">TARGET FREQUENCY</label>
            <input type="text" id="ipt-room" class="cyber-input" value="ملتقى🥂العرب">
            <label style="font-size:10px; color:#666;">OPERATIVES (User#Pass)</label>
            <textarea id="ipt-creds" class="cyber-input" rows="3" placeholder="Spy1#pass@Spy2#pass"></textarea>
            
            <button class="cyber-btn" onclick="sys.login()">ESTABLISH UPLINK</button>
            <button class="cyber-btn btn-demo" onclick="sys.demo()">ENTER DEMO MODE</button>
        </div>
    </div>

    <!-- 2. STATUS DASHBOARD -->
    <div id="pg-dash" class="screen">
        <div class="titan-panel" style="text-align:center; border-color:var(--hex-green);">
            <h2 style="color:var(--hex-green); margin:0;">CONNECTION SECURE</h2>
            <div style="font-size:11px; color:#888; margin-top:5px;">ALL SYSTEMS OPERATIONAL</div>
        </div>

        <div class="titan-panel">
            <div class="panel-header">BOTNET STATUS</div>
            <div id="bot-list">
                <div style="text-align:center; color:#555; padding:20px;">NO AGENTS DEPLOYED</div>
            </div>
        </div>
    </div>

    <!-- 3. RADAR -->
    <div id="pg-radar" class="screen">
        <div class="titan-panel">
            <div class="panel-header">WARSHIP RADAR <span id="rad-count" style="color:#fff">0</span></div>
            <div class="radar-system" id="radar-scope">
                <div class="radar-grid"></div>
                <div class="radar-sweep"></div>
                <!-- SHIPS -->
            </div>
        </div>
    </div>

    <!-- 4. CHAT -->
    <div id="pg-chat" class="screen">
        <div class="titan-panel">
            <div class="panel-header">
                TERMINAL FEED
                <button onclick="sys.exportLog()" style="background:transparent; border:1px solid #444; color:#fff; font-size:10px; cursor:pointer;">SAVE LOGS</button>
            </div>
            <div class="terminal-feed" id="chat-feed"></div>
        </div>
    </div>

    <!-- 5. VAULT -->
    <div id="pg-vault" class="screen">
        <div class="titan-panel">
            <div class="panel-header">EVIDENCE VAULT</div>
            <div class="vault-matrix" id="vault-feed"></div>
        </div>
    </div>

    <!-- NAVIGATION DOCK -->
    <div class="omega-nav" id="nav-dock">
        <div class="nav-link active" onclick="sys.nav('pg-dash', this)">
            <svg class="nav-svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
            <span class="nav-txt">SYS</span>
        </div>
        <div class="nav-link" onclick="sys.nav('pg-radar', this)">
            <svg class="nav-svg" viewBox="0 0 24 24"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>
            <span class="nav-txt">RADAR</span>
        </div>
        <div class="nav-link" onclick="sys.nav('pg-chat', this)">
            <svg class="nav-svg" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>
            <span class="nav-txt">FEED</span>
        </div>
        <div class="nav-link" onclick="sys.nav('pg-vault', this)">
            <svg class="nav-svg" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
            <span class="nav-txt">VAULT</span>
        </div>
    </div>

<script>
/* ==========================================================================
   TITAN OMEGA KERNEL (HEAVY JS)
   ========================================================================== */

class AudioController {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    beep(freq = 1000, type = 'sine') {
        if(this.ctx.state === 'suspended') this.ctx.resume();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.frequency.value = freq;
        osc.type = type;
        gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.1);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.1);
    }
    alert() { this.beep(600, 'square'); }
    click() { this.beep(1500, 'triangle'); }
}

class OmegaSystem {
    constructor() {
        this.wsUrl = "wss://chatp.net:5333/server";
        this.audio = new AudioController();
        this.users = new Map();
        this.chats = [];
        this.avatars = [];
    }

    // --- BOOT & NAV ---
    init() {
        this.drawBackground();
        setTimeout(() => { document.getElementById('boot-bar').style.width = "100%"; }, 100);
        setTimeout(() => { 
            document.getElementById('boot-seq').style.display = 'none'; 
            this.audio.beep(800, 'square');
        }, 3200);
        // Fail-safe
        setTimeout(() => { document.getElementById('skip-boot').style.display = 'block'; }, 4000);
    }

    skipBoot() { document.getElementById('boot-seq').style.display = 'none'; }

    nav(id, el) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        el.classList.add('active');
        this.audio.click();
    }

    unlockUI() {
        document.getElementById('pg-login').classList.remove('active');
        document.getElementById('pg-dash').classList.add('active');
        document.getElementById('nav-dock').style.display = 'flex';
        // Anti-Disconnect
        if(navigator.wakeLock) navigator.wakeLock.request('screen').catch(e=>{});
        setInterval(() => this.rotateCube(), 2000);
    }

    // --- LOGIN LOGIC ---
    login() {
        let room = document.getElementById('ipt-room').value;
        let creds = document.getElementById('ipt-creds').value;
        if(!creds.includes("#")) return alert("Format: User#Pass");
        
        // Save Config
        localStorage.setItem("titan_room", room);
        
        this.unlockUI();
        document.getElementById('bot-list').innerHTML = "";
        
        let list = creds.split("@");
        list.forEach((c, i) => {
            if(c.includes("#")) {
                let [u, p] = c.split("#");
                this.spawnBot(u.trim(), p.trim(), room, i);
            }
        });
    }

    demo() {
        this.unlockUI();
        alert("DEMO MODE ACTIVE");
        this.updateBotUI(0, "Demo_Operative", "ONLINE");
        this.handleData({
            username: "Target_Zero", 
            icon: "https://ui-avatars.com/api/?name=TZ&background=random",
            type: "text", body: "Communication channels open."
        });
    }

    // --- BOT LOGIC ---
    spawnBot(u, p, r, i) {
        this.createBotUI(i, u);
        let ws = new WebSocket(this.wsUrl);
        
        ws.onopen = () => {
            ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p}));
            setInterval(() => { if(ws.readyState===1) ws.send(JSON.stringify({handler:"ping"})); }, 5000);
        };
        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler === "login_event" && d.type === "success") {
                ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            }
            if(d.handler === "room_event" && d.type === "room_joined") {
                this.updateBotUI(i, u, "ONLINE");
                this.audio.beep(2000, 'sine');
            }
            this.handleData(d);
        };
        ws.onclose = () => {
            this.updateBotUI(i, u, "OFFLINE");
            setTimeout(() => this.spawnBot(u, p, r, i), 3000);
        };
    }

    createBotUI(id, name) {
        let div = document.createElement('div');
        div.className = 'agent-status offline'; div.id = `b-${id}`;
        div.innerHTML = `<b>${name}</b> <span>CONNECTING...</span>`;
        document.getElementById('bot-list').appendChild(div);
    }

    updateBotUI(id, name, status) {
        let el = document.getElementById(`b-${id}`);
        if(el) {
            el.className = `agent-status ${status.toLowerCase()}`;
            el.innerHTML = `<b>${name}</b> <span>${status}</span>`;
        }
    }

    // --- DATA HANDLING ---
    handleData(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;
        
        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        if(icon && !this.avatars.includes(icon)) this.avatars.push(icon);

        // Radar
        if(!this.users.has(u)) {
            let usr = { 
                name: u, 
                pic: icon || `https://ui-avatars.com/api/?name=${u}`,
                x: Math.random()*200+40, y: Math.random()*200+40 
            };
            this.users.set(u, usr);
            this.drawShip(usr);
        }

        // Chat & Vault
        if(d.type === "text" || d.type === "image") {
            let body = d.type === "image" ? "[IMAGE]" : d.body;
            this.addChat(u, this.users.get(u).pic, body);
            
            if(d.type === "image") this.addVault(u, d.url);
            if(d.body && d.body.match(/http.*(jpg|png)/i)) this.addVault(u, d.body.match(/http.*(jpg|png)/i)[0]);
        }
    }

    // --- UI RENDERERS ---
    drawShip(u) {
        let box = document.getElementById('radar-scope');
        let h = `
            <div class="warship" style="left:${u.x}px; top:${u.y}px">
                <img src="${u.pic}" class="warship-icon">
                <div class="warship-marker"></div>
                <div class="warship-tag">${u.name}</div>
            </div>`;
        box.insertAdjacentHTML('beforeend', h);
        document.getElementById('rad-count').innerText = this.users.size;
    }

    addChat(u, pic, txt) {
        let box = document.getElementById('chat-feed');
        let h = `
            <div class="chat-entry">
                <img src="${pic}" class="entry-avatar">
                <div class="entry-body">
                    <div class="entry-meta"><span class="entry-user">${u}</span><span>${new Date().toLocaleTimeString()}</span></div>
                    <div class="entry-content">${txt}</div>
                </div>
            </div>`;
        box.insertAdjacentHTML('afterbegin', h);
        this.chats.push(`${u}: ${txt}`);
    }

    addVault(u, url) {
        if(!url.startsWith("http")) url = "https://chatp.net"+url;
        let box = document.getElementById('vault-feed');
        let h = `<div class="vault-file" onclick="window.open('${url}')"><img src="${url}"><div class="vault-label">${u}</div></div>`;
        box.insertAdjacentHTML('afterbegin', h);
    }

    rotateCube() {
        if(this.avatars.length === 0) return;
        let faces = document.querySelectorAll('.cube-face');
        let f = faces[Math.floor(Math.random()*faces.length)];
        let img = this.avatars[Math.floor(Math.random()*this.avatars.length)];
        f.style.backgroundImage = `url(${img})`;
        f.innerText = "";
    }

    exportLog() {
        let b = new Blob([this.chats.join("\\n")], {type:"text/plain"});
        let a = document.createElement('a');
        a.href = URL.createObjectURL(b);
        a.download = "TITAN_LOGS.txt";
        a.click();
    }

    // --- CANVAS BACKGROUND ---
    drawBackground() {
        const c = document.getElementById('bg-canvas');
        const ctx = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        const drops = Array(Math.floor(c.width/20)).fill(1);
        
        setInterval(() => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, c.width, c.height);
            ctx.fillStyle = '#0f0';
            ctx.font = '12px monospace';
            drops.forEach((y, i) => {
                const text = String.fromCharCode(Math.random() * 128);
                ctx.fillText(text, i*20, y*20);
                if(y*20 > c.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }, 50);
    }
}

const sys = new OmegaSystem();
window.onload = () => sys.init();

</script>
{% endraw %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)