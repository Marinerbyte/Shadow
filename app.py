from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS: GOD MODE</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Orbitron:wght@500;900&display=swap" rel="stylesheet">
    <style>
        /* =========================================
           1. MODERN GLASS UI THEME
           ========================================= */
        :root {
            --bg-deep: #050510;
            --glass: rgba(20, 30, 40, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --primary: #00f3ff;
            --accent: #bc13fe;
            --success: #00ff9d;
            --danger: #ff0055;
            --font-main: 'Rajdhani', sans-serif;
            --font-head: 'Orbitron', sans-serif;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }

        body {
            background: var(--bg-deep); color: #fff;
            font-family: var(--font-main);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* DYNAMIC BACKGROUND */
        #bg-canvas {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -2; opacity: 0.6;
            background: radial-gradient(circle at center, #1a0b2e 0%, #000 100%);
        }

        /* RED FLASH ALERT */
        #alert-overlay {
            position: fixed; top:0; left:0; width:100%; height:100%;
            background: rgba(255, 0, 85, 0.2); pointer-events: none;
            z-index: 9999; opacity: 0; transition: opacity 0.2s;
            box-shadow: inset 0 0 100px var(--danger);
        }
        .flash-active { animation: flashAnim 0.5s infinite alternate; }
        @keyframes flashAnim { from{opacity:0;} to{opacity:1;} }

        /* =========================================
           2. LAYOUT & NAVIGATION
           ========================================= */
        .header {
            height: 70px; background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px); border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 20px; z-index: 100;
        }
        .logo { font-family: var(--font-head); font-size: 20px; background: linear-gradient(90deg, var(--primary), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        /* MINI CUBE IN HEADER */
        .mini-cube-box { width: 40px; height: 40px; perspective: 400px; }
        .mini-cube { width: 100%; height: 100%; transform-style: preserve-3d; animation: spin 5s infinite linear; }
        .mc-face { 
            position: absolute; width: 40px; height: 40px; border: 1px solid var(--primary);
            background: rgba(0,0,0,0.5); background-size: cover;
        }
        .m1 { transform: translateZ(20px); }
        .m2 { transform: rotateY(180deg) translateZ(20px); }
        .m3 { transform: rotateY(90deg) translateZ(20px); }
        .m4 { transform: rotateY(-90deg) translateZ(20px); }
        .m5 { transform: rotateX(90deg) translateZ(20px); }
        .m6 { transform: rotateX(-90deg) translateZ(20px); }

        .viewport { flex: 1; overflow-y: auto; padding: 20px; position: relative; padding-bottom: 100px; }
        .page { display: none; animation: slideUp 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); }
        .page.active { display: block; }
        @keyframes slideUp { from{opacity:0; transform:translateY(20px);} to{opacity:1; transform:translateY(0);} }

        /* NAV DOCK */
        .dock {
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
            background: rgba(20, 20, 20, 0.9); backdrop-filter: blur(20px);
            border: 1px solid var(--border); border-radius: 20px;
            padding: 10px 20px; display: flex; gap: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5); z-index: 200;
        }
        .dock-item {
            display: flex; flex-direction: column; align-items: center;
            color: #888; transition: 0.3s; cursor: pointer; width: 50px;
        }
        .dock-icon { font-size: 24px; margin-bottom: 4px; transition: 0.3s; }
        .dock-label { font-size: 10px; font-weight: bold; }
        .dock-item.active { color: var(--primary); }
        .dock-item.active .dock-icon { transform: translateY(-5px); text-shadow: 0 0 15px var(--primary); }
        .dock-item.active.alert-mode { color: var(--danger); }

        /* =========================================
           3. COMPONENT STYLING
           ========================================= */
        .glass-card {
            background: var(--glass); border: 1px solid var(--border);
            border-radius: 12px; padding: 20px; margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            position: relative; overflow: hidden;
        }
        .glass-card::before {
            content:''; position: absolute; top:0; left:0; width:100%; height:2px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
        }
        .c-title { font-family: var(--font-head); font-size: 14px; color: #aaa; margin-bottom: 15px; display: flex; justify-content: space-between; }

        /* INPUTS & BUTTONS */
        .modern-input {
            width: 100%; background: rgba(0,0,0,0.3); border: 1px solid #444;
            color: #fff; padding: 12px 15px; border-radius: 8px; font-family: var(--font-main);
            margin-bottom: 15px; transition: 0.3s;
        }
        .modern-input:focus { border-color: var(--primary); box-shadow: 0 0 15px rgba(0, 243, 255, 0.2); }
        
        .modern-btn {
            width: 100%; padding: 14px; border-radius: 8px; border: none;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: #fff; font-weight: bold; font-size: 16px; cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 243, 255, 0.3); transition: 0.3s;
        }
        .modern-btn:active { transform: scale(0.98); }
        .btn-danger { background: linear-gradient(135deg, #ff0055, #ff0000); box-shadow: 0 4px 15px rgba(255, 0, 85, 0.3); }

        /* =========================================
           4. TARGET SYSTEM
           ========================================= */
        .target-header { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; }
        .tgt-pic { width: 70px; height: 70px; border-radius: 50%; border: 2px solid var(--danger); box-shadow: 0 0 20px var(--danger); object-fit: cover; }
        .tgt-info h2 { margin: 0; color: var(--danger); font-family: var(--font-head); }
        .tgt-badge { background: rgba(255, 0, 85, 0.2); color: var(--danger); padding: 4px 8px; border-radius: 4px; font-size: 10px; border: 1px solid var(--danger); }

        .timeline { border-left: 2px solid #333; margin-left: 10px; padding-left: 20px; }
        .tl-item { position: relative; margin-bottom: 15px; }
        .tl-item::before { content:''; position: absolute; left: -26px; top: 5px; width: 10px; height: 10px; background: var(--danger); border-radius: 50%; box-shadow: 0 0 10px var(--danger); }
        .tl-time { font-size: 12px; color: #888; }
        .tl-msg { background: rgba(255, 0, 85, 0.1); padding: 10px; border-radius: 6px; border: 1px solid rgba(255, 0, 85, 0.2); color: #ffcccc; margin-top: 5px; }

        /* =========================================
           5. MOVING RADAR
           ========================================= */
        .radar-box {
            width: 300px; height: 300px; border-radius: 50%; border: 1px solid #333;
            background: radial-gradient(circle, #101015 0%, #000 80%);
            margin: 0 auto; position: relative; overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.1);
        }
        .radar-grid {
            position: absolute; inset: 0; border-radius: 50%;
            background-image: radial-gradient(transparent 60%, rgba(0, 243, 255, 0.1) 60%),
            linear-gradient(0deg, transparent 49%, rgba(0,243,255,0.1) 50%, transparent 51%),
            linear-gradient(90deg, transparent 49%, rgba(0,243,255,0.1) 50%, transparent 51%);
        }
        .radar-sweep {
            position: absolute; inset: 0; border-radius: 50%;
            background: conic-gradient(transparent 270deg, rgba(0, 243, 255, 0.3));
            animation: radarSpin 4s infinite linear;
        }
        @keyframes radarSpin { to { transform: rotate(360deg); } }
        
        .ship {
            position: absolute; width: 40px; height: 40px; transform: translate(-50%, -50%);
            display: flex; flex-direction: column; align-items: center; z-index: 10;
        }
        .ship img { width: 20px; height: 20px; border-radius: 50%; border: 1px solid #fff; }
        .ship-tri {
            width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 8px solid var(--primary);
            filter: drop-shadow(0 0 5px var(--primary)); margin-top: -2px;
        }
        .ship-name { font-size: 9px; color: var(--primary); text-shadow: 0 0 2px #000; margin-top: 2px; }

        /* =========================================
           6. CHAT & VAULT
           ========================================= */
        .chat-row { display: flex; gap: 15px; margin-bottom: 15px; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from{opacity:0; transform:translateY(10px);} to{opacity:1; transform:translateY(0);} }
        .c-av { width: 40px; height: 40px; border-radius: 10px; object-fit: cover; border: 1px solid #444; }
        .c-bub { flex: 1; background: #16161e; padding: 12px; border-radius: 0 12px 12px 12px; border: 1px solid #333; }
        .c-meta { display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 5px; }
        .c-usr { color: var(--primary); font-weight: 600; }
        .c-txt { color: #ddd; font-size: 14px; line-height: 1.4; }

        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .v-item { background: #000; border-radius: 8px; overflow: hidden; border: 1px solid #333; position: relative; height: 120px; }
        .v-item img { width: 100%; height: 100%; object-fit: cover; }
        .v-ov { position: absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:#fff; font-size:10px; padding:5px; }

        /* LOGIN CUBE (BIG) */
        .big-cube-box { width: 120px; height: 120px; margin: 40px auto; perspective: 800px; }
        .big-cube { width: 100%; height: 100%; transform-style: preserve-3d; animation: spin 8s infinite linear; }
        .bf { position: absolute; width: 120px; height: 120px; border: 2px solid var(--primary); background: rgba(0,243,255,0.1); display:flex; align-items:center; justify-content:center; font-size:20px; color:#fff; }
        @keyframes spin { from{transform: rotateX(0) rotateY(0);} to{transform: rotateX(360deg) rotateY(360deg);} }

    </style>
</head>
<body>

{% raw %}
    <canvas id="bg-canvas"></canvas>
    <div id="alert-overlay"></div>

    <!-- HEADER (Visible after Login) -->
    <div class="header" id="sys-header" style="display:none;">
        <div class="logo">TITAN <span style="color:#fff">OS</span></div>
        <div class="mini-cube-box">
            <div class="mini-cube" id="miniCube">
                <div class="mc-face m1"></div><div class="mc-face m2"></div>
                <div class="mc-face m3"></div><div class="mc-face m4"></div>
                <div class="mc-face m5"></div><div class="mc-face m6"></div>
            </div>
        </div>
    </div>

    <div class="viewport">
        
        <!-- 1. LOGIN -->
        <div id="p-login" class="page active">
            <div style="text-align:center;">
                <div class="big-cube-box">
                    <div class="big-cube">
                        <div class="bf m1">TITAN</div><div class="bf m2">XV</div>
                        <div class="bf m3">SEC</div><div class="bf m4">NET</div>
                        <div class="bf m5"></div><div class="bf m6"></div>
                    </div>
                </div>
                <h1>SYSTEM ENTRY</h1>
            </div>
            <div class="glass-card">
                <div class="c-title">CREDENTIALS</div>
                <input type="text" id="room" class="modern-input" value="ملتقى🥂العرب" placeholder="ROOM NAME">
                <textarea id="creds" class="modern-input" rows="3" placeholder="Spy1#pass@Spy2#pass"></textarea>
                <button class="modern-btn" onclick="sys.login()">INITIALIZE UPLINK</button>
            </div>
        </div>

        <!-- 2. DASHBOARD -->
        <div id="p-dash" class="page">
            <div class="glass-card" style="text-align:center; border-color:var(--success)">
                <h2 style="color:var(--success); margin:0;">SYSTEM ONLINE</h2>
                <div style="font-size:12px; opacity:0.7;">MONITORING NETWORK TRAFFIC</div>
            </div>
            
            <div class="glass-card">
                <div class="c-title">BOTNET STATUS</div>
                <div id="bot-list"></div>
            </div>
        </div>

        <!-- 3. TARGET OPS (DEEP FEATURE) -->
        <div id="p-target" class="page">
            <div class="glass-card" style="border-color: var(--danger);">
                <div class="c-title" style="color:var(--danger)">TARGET DESIGNATION</div>
                
                <!-- Target Input -->
                <div style="display:flex; gap:10px; margin-bottom:15px;">
                    <input type="text" id="tgt-name" class="modern-input" placeholder="Enter Target Username" style="margin:0;">
                    <button class="modern-btn btn-danger" onclick="sys.lockTarget()" style="width:auto;">LOCK</button>
                </div>

                <!-- Active Target View -->
                <div id="tgt-view" style="display:none;">
                    <div class="target-header">
                        <img id="t-img" src="" class="tgt-pic">
                        <div class="tgt-info">
                            <h2 id="t-display">UNKNOWN</h2>
                            <span class="tgt-badge">SURVEILLANCE ACTIVE</span>
                            <div style="margin-top:5px; font-size:10px; color:#aaa;">STATUS: <span style="color:#fff">ONLINE</span></div>
                        </div>
                    </div>

                    <div style="display:flex; gap:10px; margin-bottom:20px;">
                        <button class="modern-btn" onclick="sys.clearTgt()">CLEAR LOGS</button>
                        <button class="modern-btn" onclick="sys.exportTgt()">EXPORT</button>
                    </div>

                    <div class="c-title">ACTIVITY TIMELINE</div>
                    <div class="timeline" id="t-feed"></div>
                </div>
            </div>
        </div>

        <!-- 4. LIVE RADAR -->
        <div id="p-radar" class="page">
            <div class="glass-card">
                <div class="c-title">LIVE SONAR <span id="r-count" style="color:#fff">0</span></div>
                <div class="radar-box" id="radar-ui">
                    <div class="radar-grid"></div>
                    <div class="radar-sweep"></div>
                </div>
            </div>
        </div>

        <!-- 5. CHAT FEED -->
        <div id="p-chat" class="page">
            <div class="glass-card">
                <div class="c-title">
                    GLOBAL INTERCEPT
                    <button onclick="sys.exportAll()" style="background:none; border:1px solid #555; color:#fff; padding:2px 8px; border-radius:4px; font-size:10px;">SAVE ALL</button>
                </div>
                <div id="chat-feed" style="min-height:300px;"></div>
            </div>
        </div>

        <!-- 6. VAULT -->
        <div id="p-vault" class="page">
            <div class="glass-card">
                <div class="c-title">MEDIA EXTRACTION</div>
                <div class="vault-grid" id="vault-feed"></div>
            </div>
        </div>

    </div>

    <!-- NAVIGATION DOCK -->
    <div class="dock" id="nav-dock" style="display:none;">
        <div class="dock-item active" onclick="sys.nav('p-dash', this)">
            <div class="dock-icon">⚙️</div><div class="dock-label">SYS</div>
        </div>
        <div class="dock-item alert-mode" onclick="sys.nav('p-target', this)">
            <div class="dock-icon">🎯</div><div class="dock-label">OPS</div>
        </div>
        <div class="dock-item" onclick="sys.nav('p-radar', this)">
            <div class="dock-icon">📡</div><div class="dock-label">RADAR</div>
        </div>
        <div class="dock-item" onclick="sys.nav('p-chat', this)">
            <div class="dock-icon">💬</div><div class="dock-label">FEED</div>
        </div>
        <div class="dock-item" onclick="sys.nav('p-vault', this)">
            <div class="dock-icon">📂</div><div class="dock-label">VAULT</div>
        </div>
    </div>

<script>
class AudioSys {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    tone(f, t, type='sine') {
        if(this.ctx.state === 'suspended') this.ctx.resume();
        let o = this.ctx.createOscillator();
        let g = this.ctx.createGain();
        o.connect(g); g.connect(this.ctx.destination);
        o.frequency.value = f; o.type = type;
        g.gain.value = 0.1;
        o.start(); o.stop(this.ctx.currentTime + t);
    }
    alert() { this.tone(800, 0.1, 'square'); setTimeout(()=>this.tone(600, 0.3, 'sawtooth'), 100); }
    lock() { this.tone(1200, 0.1, 'sine'); }
}

class Titan {
    constructor() {
        this.ws = "wss://chatp.net:5333/server";
        this.users = new Map(); // Stores {x, y, vx, vy, pic, name}
        this.target = null;
        this.tgtLogs = [];
        this.globalLogs = [];
        this.imgs = [];
        this.audio = new AudioSys();
        this.loopId = null;
    }

    nav(pid, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
        document.getElementById(pid).classList.add('active');
        el.classList.add('active');
    }

    login() {
        let r = document.getElementById('room').value;
        let c = document.getElementById('creds').value;
        if(!c.includes("#")) return alert("Invalid Format");

        document.getElementById('p-login').classList.remove('active');
        document.getElementById('p-dash').classList.add('active');
        document.getElementById('sys-header').style.display = 'flex';
        document.getElementById('nav-dock').style.display = 'flex';

        let list = c.split("@");
        document.getElementById('bot-list').innerHTML = "";
        
        list.forEach((cr, i) => {
            if(cr.includes("#")) {
                let [u, p] = cr.split("#");
                this.spawnBot(u.trim(), p.trim(), r, i);
            }
        });

        // Start Systems
        this.loopId = requestAnimationFrame(() => this.radarLoop());
        setInterval(() => this.rotateMiniCube(), 2000);
        if('wakeLock' in navigator) navigator.wakeLock.request('screen').catch(e=>{});
    }

    spawnBot(u, p, r, i) {
        let d = document.createElement('div');
        d.id = `b-${i}`; d.style = "padding:10px; border-bottom:1px solid #333; display:flex; justify-content:space-between;";
        d.innerHTML = `<b>${u}</b> <span style="color:#aaa">CONN...</span>`;
        document.getElementById('bot-list').appendChild(d);

        let ws = new WebSocket(this.ws);
        ws.onopen = () => { ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p})); setInterval(()=>ws.send(JSON.stringify({handler:"ping"})),5000); };
        ws.onmessage = (e) => {
            let msg = JSON.parse(e.data);
            if(msg.handler=="login_event" && msg.type=="success") ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            if(msg.handler=="room_event" && msg.type=="room_joined") document.querySelector(`#b-${i} span`).innerHTML = `<span style="color:var(--success)">ONLINE</span>`;
            this.process(msg);
        };
        ws.onclose = () => setTimeout(()=>this.spawnBot(u,p,r,i), 3000);
    }

    process(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;
        
        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        if(icon && !this.imgs.includes(icon)) this.imgs.push(icon);

        // 1. User Management (Radar Physics)
        if(!this.users.has(u)) {
            this.users.set(u, {
                name: u,
                pic: icon || `https://ui-avatars.com/api/?name=${u}`,
                x: 140, y: 140, // Center
                vx: (Math.random()-0.5)*1.5, vy: (Math.random()-0.5)*1.5 // Velocity
            });
            this.addRadarElement(u);
        }

        // 2. Chat & Target Logic
        if(d.type === "text" || d.type === "image") {
            let body = d.type==="image" ? "[IMAGE]" : d.body;
            this.addChat(u, this.users.get(u).pic, body);
            
            // Vault
            if(d.type==="image") this.addVault(u, d.url);

            // Target Alert
            if(this.target && u === this.target) {
                this.audio.alert();
                this.flashScreen();
                this.addTgtLog(body);
            }
        }
    }

    // --- TARGET OPS ---
    lockTarget() {
        let n = document.getElementById('tgt-name').value;
        if(!n) return;
        this.target = n;
        this.audio.lock();
        document.getElementById('tgt-view').style.display = 'block';
        document.getElementById('t-display').innerText = n;
        // Try to find pic
        if(this.users.has(n)) document.getElementById('t-img').src = this.users.get(n).pic;
        else document.getElementById('t-img').src = `https://ui-avatars.com/api/?name=${n}`;
    }

    clearTgt() { document.getElementById('t-feed').innerHTML = ""; this.tgtLogs = []; }
    
    addTgtLog(txt) {
        let t = new Date().toLocaleTimeString();
        let h = `<div class="tl-item"><div class="tl-time">${t}</div><div class="tl-msg">${txt}</div></div>`;
        document.getElementById('t-feed').insertAdjacentHTML('afterbegin', h);
        this.tgtLogs.push(`[${t}] ${txt}`);
    }

    flashScreen() {
        let f = document.getElementById('alert-overlay');
        f.classList.add('flash-active');
        setTimeout(() => f.classList.remove('flash-active'), 2000);
    }

    // --- RADAR PHYSICS ---
    addRadarElement(u) {
        let box = document.getElementById('radar-ui');
        let el = document.createElement('div');
        el.className = 'ship'; id = `ship-${u}`;
        el.innerHTML = `<img src="${this.users.get(u).pic}"> <div class="ship-tri"></div> <div class="ship-name">${u}</div>`;
        box.appendChild(el);
        this.users.get(u).el = el;
        document.getElementById('r-count').innerText = this.users.size;
    }

    radarLoop() {
        this.users.forEach(usr => {
            // Update Position
            usr.x += usr.vx;
            usr.y += usr.vy;

            // Bounce off walls (Radius 140)
            let dx = usr.x - 140;
            let dy = usr.y - 140;
            let dist = Math.sqrt(dx*dx + dy*dy);
            
            if(dist > 130) {
                usr.vx *= -1; usr.vy *= -1;
            }

            // Render
            if(usr.el) {
                usr.el.style.left = usr.x + "px";
                usr.el.style.top = usr.y + "px";
            }
        });
        requestAnimationFrame(() => this.radarLoop());
    }

    // --- UTILS ---
    addChat(u, pic, txt) {
        let h = `
        <div class="msg-row">
            <img src="${pic}" class="msg-av">
            <div class="msg-bubble">
                <div class="msg-header"><span class="msg-user">${u}</span><span>${new Date().toLocaleTimeString()}</span></div>
                <div class="msg-text">${txt}</div>
            </div>
        </div>`;
        document.getElementById('chat-feed').insertAdjacentHTML('afterbegin', h);
        this.globalLogs.push(`${u}: ${txt}`);
    }

    addVault(u, url) {
        if(!url.startsWith("http")) url = "https://chatp.net"+url;
        let h = `<div class="v-item" onclick="window.open('${url}')"><img src="${url}"><div class="v-tag">${u}</div></div>`;
        document.getElementById('vault-feed').insertAdjacentHTML('afterbegin', h);
    }

    rotateMiniCube() {
        if(this.imgs.length === 0) return;
        let faces = document.querySelectorAll('.mc-face');
        let f = faces[Math.floor(Math.random()*faces.length)];
        let i = this.imgs[Math.floor(Math.random()*this.imgs.length)];
        f.style.backgroundImage = `url(${i})`;
    }

    exportTgt() { this.dl(this.tgtLogs.join("\\n"), "TARGET_LOG.txt"); }
    exportAll() { this.dl(this.globalLogs.join("\\n"), "FULL_LOG.txt"); }
    
    dl(c, n) {
        let b = new Blob([c], {type:"text/plain"});
        let a = document.createElement('a');
        a.href = URL.createObjectURL(b);
        a.download = n;
        a.click();
    }
}

const sys = new Titan();
// Canvas Effect
const c = document.getElementById('bg-canvas'); const x = c.getContext('2d');
c.width=window.innerWidth; c.height=window.innerHeight;
let stars=[]; for(let i=0;i<100;i++) stars.push({x:Math.random()*c.width, y:Math.random()*c.height, r:Math.random()*2});
function anim() {
    x.clearRect(0,0,c.width,c.height); x.fillStyle='#fff';
    stars.forEach(s=>{ s.y+=0.5; if(s.y>c.height)s.y=0; x.beginPath(); x.arc(s.x,s.y,s.r,0,Math.PI*2); x.fill(); });
    requestAnimationFrame(anim);
}
anim();
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