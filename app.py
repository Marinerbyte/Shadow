from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS v21</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        /* =============================================================================
           1. CORE SYSTEM (TITAN THEME)
           ============================================================================= */
        :root {
            --bg: #020202;
            --panel: rgba(10, 12, 16, 0.95);
            --cyan: #00f3ff;
            --green: #0aff0a;
            --red: #ff003c;
            --gold: #ffd700;
            --glass: blur(10px);
            --font-head: 'Orbitron', sans-serif;
            --font-code: 'Share Tech Mono', monospace;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }

        body {
            background-color: var(--bg);
            color: #fff;
            font-family: var(--font-head);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* MATRIX BACKGROUND */
        .bg-matrix {
            position: fixed; top: 0; left: 0; width: 200vw; height: 200vh;
            background: 
                linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px), 
                linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
            animation: gridMove 15s linear infinite;
            z-index: -2; pointer-events: none;
        }
        @keyframes gridMove { from {transform: perspective(500px) rotateX(60deg) translateY(0);} to {transform: perspective(500px) rotateX(60deg) translateY(40px);} }

        /* =============================================================================
           2. LAYOUT & NAVIGATION
           ============================================================================= */
        
        /* HEADER (LIVE CUBE) */
        .header {
            height: 60px; background: rgba(5,5,5,0.95); border-bottom: 1px solid #333;
            display: none; justify-content: space-between; align-items: center;
            padding: 0 15px; z-index: 500;
        }
        .logo { font-size: 18px; color: var(--cyan); letter-spacing: 2px; }
        .mini-cube-wrap { width: 30px; height: 30px; perspective: 400px; }
        .mini-cube { width: 100%; height: 100%; transform-style: preserve-3d; animation: spin 5s infinite linear; }
        .mc-face { 
            position: absolute; width: 30px; height: 30px; border: 1px solid var(--cyan);
            background: rgba(0,243,255,0.1); background-size: cover;
        }
        
        /* PAGES */
        .viewport {
            flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 120px;
            position: relative;
        }
        .page { display: none; animation: slideUp 0.3s ease-out; }
        .page.active { display: block; }
        @keyframes slideUp { from{opacity:0; transform:translateY(15px);} to{opacity:1; transform:translateY(0);} }

        /* CARDS */
        .card {
            background: var(--panel); border: 1px solid #222;
            border-left: 3px solid var(--cyan); border-radius: 4px;
            padding: 15px; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            backdrop-filter: var(--glass);
        }
        .c-title {
            font-size: 14px; color: var(--cyan); border-bottom: 1px solid #333;
            padding-bottom: 8px; margin-bottom: 10px; display: flex; justify-content: space-between;
        }

        /* INPUTS & BUTTONS */
        input, textarea {
            width: 100%; background: #050505; border: 1px solid #444; color: var(--cyan);
            padding: 12px; font-family: var(--font-code); margin-bottom: 10px; font-size: 14px;
        }
        .btn {
            width: 100%; padding: 15px; background: rgba(0,243,255,0.1); border: 1px solid var(--cyan);
            color: var(--cyan); font-weight: bold; cursor: pointer; text-transform: uppercase;
            font-family: var(--font-code); transition: 0.3s;
        }
        .btn:active { background: var(--cyan); color: #000; }
        .btn-red { border-color: var(--red); color: var(--red); background: rgba(255,0,60,0.1); }
        .btn-sm { width: auto; padding: 5px 10px; font-size: 10px; }

        /* =============================================================================
           3. RADAR (FLOATING USER CIRCLES)
           ============================================================================= */
        .radar-frame {
            width: 280px; height: 280px; margin: 0 auto; border-radius: 50%;
            border: 2px solid #333; background: radial-gradient(circle, #001 0%, #000 90%);
            position: relative; overflow: hidden; box-shadow: 0 0 30px rgba(0,243,255,0.1);
        }
        .scanner {
            position: absolute; inset: 0; border-radius: 50%;
            background: conic-gradient(transparent 270deg, rgba(0,255,10,0.3));
            animation: scan 3s infinite linear; pointer-events: none;
        }
        @keyframes scan { to { transform: rotate(360deg); } }

        /* Floating User Animation */
        .r-user {
            position: absolute; width: 44px; height: 44px;
            display: flex; flex-direction: column; align-items: center;
            cursor: pointer; z-index: 10;
            animation: floatAnim 4s ease-in-out infinite;
        }
        @keyframes floatAnim { 
            0% { transform: translate(0, 0); }
            50% { transform: translate(0, -5px); }
            100% { transform: translate(0, 0); }
        }
        .r-img {
            width: 32px; height: 32px; border-radius: 50%; border: 2px solid #fff;
            box-shadow: 0 0 10px var(--cyan); object-fit: cover;
        }
        .r-tag {
            font-size: 8px; color: var(--green); background: rgba(0,0,0,0.8);
            padding: 1px 4px; border-radius: 4px; margin-top: 2px; white-space: nowrap;
        }

        /* =============================================================================
           4. TARGET SYSTEM (LIST & DOSSIER)
           ============================================================================= */
        /* GRID VIEW */
        .user-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .u-cell {
            background: #111; border: 1px solid #333; padding: 10px; border-radius: 6px;
            text-align: center; cursor: pointer; transition: 0.2s;
        }
        .u-cell:hover { border-color: var(--red); background: rgba(255,0,60,0.1); }
        .u-pic { width: 40px; height: 40px; border-radius: 50%; margin-bottom: 5px; }
        .u-name { font-size: 10px; color: #ccc; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

        /* DOSSIER VIEW */
        .dossier-panel { display: none; border-color: var(--red); }
        .dos-head { display: flex; gap: 15px; align-items: center; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 10px; }
        .dos-pic { width: 70px; height: 70px; border-radius: 50%; border: 2px solid var(--red); box-shadow: 0 0 15px var(--red); }
        .dos-info h2 { margin: 0; color: var(--red); font-size: 18px; }
        .dos-meta { font-size: 10px; color: #888; font-family: var(--font-code); }
        
        .dos-actions { display: flex; gap: 10px; margin-bottom: 10px; }
        .dos-logs { height: 180px; overflow-y: auto; background: #000; border: 1px solid #333; padding: 5px; font-family: var(--font-code); font-size: 11px; color: #bbb; }
        .log-row { border-bottom: 1px solid #111; padding: 4px 0; }

        /* =============================================================================
           5. FEED & VAULT
           ============================================================================= */
        .msg-row { display: flex; gap: 10px; margin-bottom: 12px; }
        .msg-pic { width: 35px; height: 35px; border-radius: 6px; border: 1px solid #444; }
        .msg-bub { flex: 1; background: #121215; padding: 10px; border-radius: 0 10px 10px 10px; border: 1px solid #222; }
        .msg-inf { display: flex; justify-content: space-between; font-size: 10px; color: #666; margin-bottom: 4px; }
        .msg-u { color: var(--cyan); font-weight: bold; }
        .msg-t { color: #ddd; font-size: 13px; word-break: break-all; }

        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .v-item { background: #000; border: 1px solid #333; height: 120px; position: relative; }
        .v-item img { width: 100%; height: 100%; object-fit: cover; }
        .v-id { 
            position: absolute; bottom:0; left:0; width:100%; 
            background: rgba(0,0,0,0.8); color: var(--cyan); font-size: 10px; 
            padding: 3px; text-align: center; border-top: 1px solid #333;
        }

        /* =============================================================================
           6. BOTTOM NAVIGATION & DOCK
           ============================================================================= */
        .bot-dock {
            position: fixed; bottom: 70px; left: 0; width: 100%; height: 40px;
            background: linear-gradient(to top, #000, transparent);
            display: flex; align-items: center; gap: 10px; padding: 0 15px;
            overflow-x: auto; z-index: 90;
        }
        .bot-chip {
            background: #111; border: 1px solid #333; padding: 4px 10px;
            border-radius: 20px; font-size: 10px; color: #777; white-space: nowrap;
            display: flex; align-items: center; gap: 5px;
        }
        .bot-chip.on { border-color: var(--green); color: #fff; background: rgba(0,255,10,0.1); }
        .dot { width: 6px; height: 6px; border-radius: 50%; background: #444; }
        .on .dot { background: var(--green); box-shadow: 0 0 5px var(--green); }

        .nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
            background: #080808; border-top: 1px solid #333;
            display: none; justify-content: space-around; align-items: center; z-index: 100;
        }
        .nav-btn { text-align: center; color: #555; font-size: 20px; transition: 0.2s; }
        .nav-btn span { display: block; font-size: 10px; font-family: var(--font-head); margin-top: 3px; }
        .nav-btn.active { color: var(--cyan); transform: translateY(-5px); text-shadow: 0 0 10px var(--cyan); }

        /* LOGIN CUBE (BIG) */
        .cube-big-wrap { width: 120px; height: 120px; margin: 30px auto; perspective: 800px; }
        .cube-big { width: 100%; height: 100%; transform-style: preserve-3d; animation: spin 8s infinite linear; }
        .cf { position: absolute; width: 120px; height: 120px; border: 2px solid var(--cyan); background: rgba(0,243,255,0.1); display:flex; align-items:center; justify-content:center; font-size:20px; color:#fff; }
        .c1 { transform: translateZ(60px); }
        .c2 { transform: rotateY(180deg) translateZ(60px); }
        .c3 { transform: rotateY(90deg) translateZ(60px); }
        .c4 { transform: rotateY(-90deg) translateZ(60px); }
        .c5 { transform: rotateX(90deg) translateZ(60px); }
        .c6 { transform: rotateX(-90deg) translateZ(60px); }
        @keyframes spin { 100% { transform: rotateX(360deg) rotateY(360deg); } }

    </style>
</head>
<body>

{% raw %}
    <div class="bg-matrix"></div>

    <!-- HEADER (Hidden initially) -->
    <div class="header" id="sys-header">
        <div class="logo">TITAN <span style="color:#fff">OS</span></div>
        <div class="mini-cube-wrap">
            <div class="mini-cube" id="miniCube">
                <div class="mc-face c1"></div><div class="mc-face c2"></div>
                <div class="mc-face c3"></div><div class="mc-face c4"></div>
                <div class="mc-face c5"></div><div class="mc-face c6"></div>
            </div>
        </div>
    </div>

    <div class="viewport">
        
        <!-- 1. LOGIN -->
        <div id="p-login" class="page active">
            <div style="text-align:center;">
                <div class="cube-big-wrap">
                    <div class="cube-big">
                        <div class="cf c1">TITAN</div><div class="cf c2">v21</div>
                        <div class="cf c3">SYS</div><div class="cf c4">SEC</div>
                        <div class="cf c5"></div><div class="cf c6"></div>
                    </div>
                </div>
                <h1 style="color:var(--cyan); letter-spacing:4px; margin:0;">TITAN OS</h1>
                <p style="color:#666; font-size:12px;">ULTIMATE SURVEILLANCE</p>
            </div>

            <div class="card" style="margin-top:20px;">
                <div class="c-title">ACCESS CONTROL</div>
                <label style="font-size:10px; color:#888;">TARGET ROOM</label>
                <input type="text" id="room" value="ملتقى🥂العرب">
                <label style="font-size:10px; color:#888;">BOT CREDENTIALS</label>
                <textarea id="creds" rows="3" placeholder="Spy1#pass@Spy2#pass"></textarea>
                <button class="btn" onclick="sys.login()">INITIALIZE SYSTEM</button>
            </div>
        </div>

        <!-- 2. RADAR PAGE -->
        <div id="p-radar" class="page">
            <div class="card">
                <div class="c-title">LIVE SONAR <span id="r-cnt" style="color:#fff">0</span></div>
                <div class="radar-frame" id="radar-ui">
                    <div class="scanner"></div>
                    <!-- USER BLIPS -->
                </div>
                <div style="text-align:center; font-size:10px; color:#666; margin-top:5px;">ACTIVE ENTITIES DETECTED</div>
            </div>
        </div>

        <!-- 3. TARGET SYSTEM -->
        <div id="p-target" class="page">
            <!-- Grid View -->
            <div id="tgt-grid">
                <div class="card">
                    <div class="c-title">USER DATABASE</div>
                    <div class="user-grid" id="user-list">
                        <div style="grid-column:span 3; text-align:center; padding:20px; color:#555;">WAITING FOR DATA...</div>
                    </div>
                </div>
            </div>

            <!-- Dossier View -->
            <div id="tgt-dossier" class="dossier-panel card">
                <div class="c-title" style="color:var(--red)">TARGET LOCKED</div>
                <button onclick="sys.closeDossier()" class="btn btn-sm" style="margin-bottom:10px;">&laquo; BACK TO LIST</button>
                
                <div class="dos-head">
                    <img id="d-pic" class="dos-pic">
                    <div>
                        <h2 id="d-name" style="margin:0; color:var(--red); font-size:16px;">UNKNOWN</h2>
                        <div class="dos-meta">STATUS: <span style="color:var(--green)">ACTIVE</span></div>
                        <div style="margin-top:5px;">
                            <button onclick="sys.clearLog()" class="btn btn-sm btn-red">CLEAR</button>
                            <button onclick="sys.exportTgt()" class="btn btn-sm btn-red">EXPORT</button>
                        </div>
                    </div>
                </div>

                <div class="c-title" style="font-size:12px; border:none; margin-bottom:5px;">INTERCEPTED LOGS</div>
                <div class="dos-logs" id="d-logs"></div>

                <div class="c-title" style="font-size:12px; border:none; margin:10px 0 5px;">CAPTURED MEDIA</div>
                <div class="vault-grid" id="d-media"></div>
            </div>
        </div>

        <!-- 4. FEED -->
        <div id="p-chat" class="page">
            <div class="card">
                <div class="c-title">
                    GLOBAL FEED
                    <button onclick="sys.exportAll()" class="btn btn-sm" style="width:auto;">EXPORT</button>
                </div>
                <div id="chat-feed"></div>
            </div>
        </div>

        <!-- 5. VAULT -->
        <div id="p-vault" class="page">
            <div class="card">
                <div class="c-title">MEDIA VAULT</div>
                <div class="vault-grid" id="vault-feed"></div>
            </div>
        </div>

    </div>

    <!-- BOT DOCK -->
    <div class="bot-dock" id="bot-dock" style="display:none"></div>

    <!-- NAVIGATION -->
    <div class="nav" id="navbar" style="display:none">
        <div class="nav-btn active" onclick="sys.nav('p-radar', this)">📡<span>RADAR</span></div>
        <div class="nav-btn" onclick="sys.nav('p-target', this)">🎯<span>TARGET</span></div>
        <div class="nav-btn" onclick="sys.nav('p-chat', this)">💬<span>FEED</span></div>
        <div class="nav-btn" onclick="sys.nav('p-vault', this)">📂<span>VAULT</span></div>
    </div>

<script>
class TitanOS {
    constructor() {
        this.ws = "wss://chatp.net:5333/server";
        this.users = new Map(); // Stores {pic, logs[], media[]}
        this.allLogs = [];
        this.avatars = [];
        this.target = null;
        this.audio = new (window.AudioContext || window.webkitAudioContext)();
    }

    nav(pid, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(pid).classList.add('active');
        el.classList.add('active');
    }

    login() {
        let r = document.getElementById('room').value;
        let c = document.getElementById('creds').value;
        if(!c.includes("#")) return alert("Format: User#Pass");

        document.getElementById('p-login').classList.remove('active');
        document.getElementById('p-radar').classList.add('active');
        document.getElementById('sys-header').style.display = 'flex';
        document.getElementById('navbar').style.display = 'flex';
        document.getElementById('bot-dock').style.display = 'flex';

        let list = c.split("@");
        document.getElementById('bot-dock').innerHTML = "";
        
        list.forEach((str, i) => {
            if(str.includes("#")) {
                let [u, p] = str.split("#");
                this.spawnBot(u.trim(), p.trim(), r, i);
            }
        });

        // Anti-Hang Measures
        setInterval(() => this.rotateCube(), 2500); // Low freq update
        if('wakeLock' in navigator) navigator.wakeLock.request('screen').catch(e=>{});
    }

    spawnBot(u, p, r, i) {
        let pill = document.createElement('div');
        pill.className = 'bot-chip'; pill.id = `pill-${i}`;
        pill.innerHTML = `<div class="dot"></div> ${u}`;
        document.getElementById('bot-dock').appendChild(pill);

        let ws = new WebSocket(this.ws);
        ws.onopen = () => { ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p})); setInterval(()=>ws.send(JSON.stringify({handler:"ping"})),5000); };
        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler=="login_event" && d.type=="success") ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            if(d.handler=="room_event" && d.type=="room_joined") document.getElementById(`pill-${i}`).classList.add('on');
            this.handle(d);
        };
        ws.onclose = () => {
            document.getElementById(`pill-${i}`).classList.remove('on');
            setTimeout(()=>this.spawnBot(u,p,r,i), 3000);
        }
    }

    handle(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;

        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        if(icon && !this.avatars.includes(icon)) this.avatars.push(icon);

        // 1. User Management
        if(!this.users.has(u)) {
            this.users.set(u, {
                pic: icon || `https://ui-avatars.com/api/?name=${u}`,
                logs: [], media: []
            });
            this.addRadarBlip(u, this.users.get(u).pic);
            this.refreshGrid();
        }
        let obj = this.users.get(u);

        // 2. Chat & Vault
        if(d.type === "text" || d.type === "image") {
            let txt = d.type==="image" ? "[IMAGE]" : d.body;
            let time = new Date().toLocaleTimeString();
            
            obj.logs.push({time, txt});
            this.allLogs.push(`${u}: ${txt}`);
            this.addChat(u, obj.pic, txt, time);

            if(d.type==="image") {
                obj.media.push(d.url);
                this.addVault(u, d.url);
            }

            // Update Target Dossier Live
            if(this.target === u) {
                this.addDossierLog(time, txt);
                if(d.type==="image") this.addDossierMedia(d.url);
                this.beep();
            }
        }
    }

    // --- RADAR (CSS PHYSICS) ---
    addRadarBlip(u, pic) {
        let box = document.getElementById('radar-ui');
        let el = document.createElement('div');
        el.className = 'r-user';
        // Random Position 10-90%
        el.style.left = (Math.random()*80 + 10) + "%";
        el.style.top = (Math.random()*80 + 10) + "%";
        // Random Animation Delay for natural chaos
        el.style.animationDelay = (Math.random()*2) + "s";
        el.innerHTML = `<img src="${pic}" class="r-img"><div class="r-tag">${u}</div>`;
        
        // Tap to move
        el.onclick = function() {
            this.style.left = (Math.random()*80 + 10) + "%";
            this.style.top = (Math.random()*80 + 10) + "%";
        };
        
        box.appendChild(el);
        document.getElementById('r-cnt').innerText = this.users.size;
    }

    // --- TARGET SYSTEM ---
    refreshGrid() {
        let g = document.getElementById('user-list'); g.innerHTML = "";
        this.users.forEach((val, key) => {
            let d = document.createElement('div'); d.className = 'u-cell';
            d.innerHTML = `<img src="${val.pic}" class="u-pic"><div class="u-name">${key}</div>`;
            d.onclick = () => this.openDossier(key);
            g.appendChild(d);
        });
    }

    openDossier(name) {
        this.target = name;
        let u = this.users.get(name);
        document.getElementById('tgt-grid').style.display = 'none';
        document.getElementById('tgt-dossier').style.display = 'block';
        
        document.getElementById('d-name').innerText = name;
        document.getElementById('d-pic').src = u.pic;
        
        // Load Logs
        let lb = document.getElementById('d-logs'); lb.innerHTML = "";
        u.logs.forEach(l => lb.innerHTML += `<div class="log-row"><span style="color:#666">[${l.time}]</span> ${l.txt}</div>`);
        
        // Load Media
        let mb = document.getElementById('d-media'); mb.innerHTML = "";
        u.media.forEach(m => {
            if(!m.startsWith("http")) m = "https://chatp.net"+m;
            mb.innerHTML += `<div class="v-item" onclick="window.open('${m}')"><img src="${m}"><div class="v-id">${name}</div></div>`;
        });
    }

    closeDossier() {
        this.target = null;
        document.getElementById('tgt-dossier').style.display = 'none';
        document.getElementById('tgt-grid').style.display = 'block';
    }

    addDossierLog(t, m) {
        let d = document.createElement('div'); d.className="log-row"; d.innerHTML=`<span style="color:#666">[${t}]</span> ${m}`;
        document.getElementById('d-logs').prepend(d);
    }
    
    addDossierMedia(u) {
        if(!u.startsWith("http")) u="https://chatp.net"+u;
        let d=document.createElement('div'); d.className="v-item"; 
        d.innerHTML=`<img src="${u}"><div class="v-id">${this.target}</div>`;
        d.onclick=()=>window.open(u);
        document.getElementById('d-media').prepend(d);
    }

    clearLog() { 
        if(this.target) {
            this.users.get(this.target).logs = [];
            document.getElementById('d-logs').innerHTML = "";
        }
    }

    // --- UI UTILS ---
    addChat(u, pic, txt, time) {
        let h = `<div class="msg-row"><img src="${pic}" class="msg-pic"><div class="msg-bub"><div class="msg-inf"><span class="msg-u">${u}</span><span>${time}</span></div><div class="msg-t">${txt}</div></div></div>`;
        document.getElementById('chat-feed').insertAdjacentHTML('afterbegin', h);
    }

    addVault(u, url) {
        if(!url.startsWith("http")) url="https://chatp.net"+url;
        let h = `<div class="v-item" onclick="window.open('${url}')"><img src="${url}"><div class="v-id">${u}</div></div>`;
        document.getElementById('vault-feed').insertAdjacentHTML('afterbegin', h);
    }

    rotateCube() {
        if(this.avatars.length < 1) return;
        let faces = document.querySelectorAll('.mc-face');
        let f = faces[Math.floor(Math.random()*faces.length)];
        let i = this.avatars[Math.floor(Math.random()*this.avatars.length)];
        f.style.backgroundImage = `url(${i})`;
    }

    beep() {
        if(this.audio.state==='suspended') this.audio.resume();
        let o=this.audio.createOscillator(); let g=this.audio.createGain();
        o.connect(g); g.connect(this.audio.destination);
        o.frequency.value=800; g.gain.value=0.1;
        o.start(); o.stop(this.audio.currentTime+0.1);
    }

    exportTgt() { if(this.target) this.dl(this.users.get(this.target).logs.map(l=>`[${l.time}] ${l.txt}`).join("\\n"), "TARGET.txt"); }
    exportAll() { this.dl(this.allLogs.join("\\n"), "FULL.txt"); }
    dl(c, n) { let a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([c],{type:'text/plain'})); a.download=n; a.click(); }
}

const sys = new TitanOS();
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