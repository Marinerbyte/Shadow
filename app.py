from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS XI | GENESIS</title>
    <link href="https://fonts.googleapis.com/css2?family=Oxanium:wght@400;600;800&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* =========================================
           1. CORE UNIVERSE (THEME)
           ========================================= */
        :root {
            --bg-void: #030305;
            --bg-panel: rgba(15, 20, 25, 0.85);
            --neon-cyan: #00f3ff;
            --neon-green: #0aff0a;
            --neon-red: #ff0055;
            --neon-gold: #ffd700;
            --glass: blur(12px);
            --font-main: 'Oxanium', display;
            --font-code: 'Roboto Mono', monospace;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; user-select: none; }
        
        body {
            background-color: var(--bg-void);
            color: #e0e0e0;
            font-family: var(--font-main);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* DIGITAL WORLD BACKGROUND (MOVING GRID) */
        .digital-grid {
            position: fixed; top: -50%; left: -50%; width: 200vw; height: 200vh;
            background: 
                linear-gradient(transparent 0%, rgba(0, 243, 255, 0.05) 50%, transparent 100%),
                linear-gradient(90deg, transparent 0%, rgba(0, 243, 255, 0.03) 50%, transparent 100%);
            background-size: 50px 50px;
            transform: perspective(500px) rotateX(60deg);
            animation: gridMove 15s linear infinite;
            z-index: -2; pointer-events: none;
        }
        @keyframes gridMove { 0% {transform: perspective(500px) rotateX(60deg) translateY(0);} 100% {transform: perspective(500px) rotateX(60deg) translateY(50px);} }

        /* PARTICLE DUST */
        .particles {
            position: fixed; top:0; left:0; width:100%; height:100%;
            background-image: radial-gradient(var(--neon-cyan) 1px, transparent 1px);
            background-size: 60px 60px; opacity: 0.1; z-index: -1;
        }

        /* =========================================
           2. ANIMATIONS & TRANSITIONS
           ========================================= */
        .page { 
            display: none; height: 100%; padding: 15px; overflow-y: auto; padding-bottom: 90px;
            animation: zoomIn 0.4s ease-out;
        }
        .page.active { display: block; }
        @keyframes zoomIn { from{opacity:0; transform: scale(0.95);} to{opacity:1; transform: scale(1);} }
        
        .hidden { display: none !important; }

        /* =========================================
           3. UI COMPONENTS (PROFESSIONAL)
           ========================================= */
        .titan-card {
            background: var(--bg-panel);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 3px solid var(--neon-cyan);
            backdrop-filter: var(--glass);
            border-radius: 8px; padding: 15px; margin-bottom: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .card-head {
            font-size: 16px; color: var(--neon-cyan); text-transform: uppercase;
            letter-spacing: 2px; border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between;
        }

        /* INPUTS */
        .cyber-input {
            width: 100%; background: rgba(0,0,0,0.6); border: 1px solid #333;
            color: #fff; padding: 15px; font-family: var(--font-code);
            margin-bottom: 15px; font-size: 14px; border-radius: 4px;
            transition: 0.3s;
        }
        .cyber-input:focus { border-color: var(--neon-cyan); box-shadow: 0 0 15px rgba(0, 243, 255, 0.2); }

        /* BUTTONS */
        .cyber-btn {
            width: 100%; padding: 15px; font-weight: 800; font-size: 16px;
            text-transform: uppercase; letter-spacing: 2px; cursor: pointer;
            background: linear-gradient(90deg, rgba(0, 243, 255, 0.1), rgba(0,0,0,0));
            border: 1px solid var(--neon-cyan); color: var(--neon-cyan);
            transition: 0.3s; clip-path: polygon(0 0, 100% 0, 100% 70%, 95% 100%, 0 100%);
        }
        .cyber-btn:active { background: var(--neon-cyan); color: #000; }

        /* =========================================
           4. 3D CUBE ENGINE (LOGIN SCREEN)
           ========================================= */
        .scene-3d {
            width: 120px; height: 120px; margin: 40px auto; perspective: 1000px;
        }
        .cube {
            width: 100%; height: 100%; position: relative; transform-style: preserve-3d;
            animation: spin 10s infinite linear;
        }
        .face {
            position: absolute; width: 120px; height: 120px;
            background: rgba(0, 243, 255, 0.1); border: 2px solid var(--neon-cyan);
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; color: #fff; box-shadow: inset 0 0 20px rgba(0, 243, 255, 0.2);
            background-size: cover; background-position: center; transition: background 0.5s;
        }
        .f-fr { transform: rotateY(0deg) translateZ(60px); }
        .f-bk { transform: rotateY(180deg) translateZ(60px); }
        .f-rt { transform: rotateY(90deg) translateZ(60px); }
        .f-lt { transform: rotateY(-90deg) translateZ(60px); }
        .f-tp { transform: rotateX(90deg) translateZ(60px); }
        .f-bm { transform: rotateX(-90deg) translateZ(60px); }
        
        @keyframes spin { 0%{transform: rotateX(0) rotateY(0);} 100%{transform: rotateX(360deg) rotateY(360deg);} }

        /* =========================================
           5. RADAR SYSTEM (SHIP STYLE)
           ========================================= */
        .radar-frame {
            width: 280px; height: 280px; margin: 0 auto; border-radius: 50%;
            border: 4px solid #1a1a1a; position: relative;
            background: radial-gradient(circle, #001 0%, #000 90%);
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.1); overflow: hidden;
        }
        .radar-scan {
            position: absolute; inset: 0; border-radius: 50%;
            background: conic-gradient(transparent 270deg, rgba(0,255,10,0.4));
            animation: radarSpin 4s infinite linear; z-index: 1;
        }
        @keyframes radarSpin { to { transform: rotate(360deg); } }
        
        .ship-blip {
            position: absolute; width: 30px; height: 30px; z-index: 10;
            display: flex; flex-direction: column; align-items: center;
            transition: all 1s ease-in-out;
            animation: hoverShip 2s infinite ease-in-out alternate;
        }
        .ship-body {
            width: 0; height: 0; 
            border-left: 6px solid transparent; border-right: 6px solid transparent;
            border-bottom: 14px solid var(--neon-green);
            filter: drop-shadow(0 0 5px var(--neon-green));
        }
        .ship-avatar {
            width: 20px; height: 20px; border-radius: 50%; border: 1px solid #fff;
            margin-bottom: 2px; background-size: cover;
        }
        .ship-name {
            font-size: 8px; color: var(--neon-green); margin-top: 2px; 
            text-shadow: 0 0 2px #000; white-space: nowrap;
        }
        @keyframes hoverShip { from{transform: translateY(0);} to{transform: translateY(-3px);} }

        /* =========================================
           6. CHAT FEED & VAULT
           ========================================= */
        .msg-row {
            display: flex; gap: 10px; margin-bottom: 15px; animation: slideUp 0.3s;
        }
        @keyframes slideUp { from{transform:translateY(10px); opacity:0;} to{transform:translateY(0); opacity:1;} }
        
        .msg-pic { width: 40px; height: 40px; border-radius: 8px; border: 1px solid var(--neon-cyan); }
        .msg-bubble {
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            padding: 10px; border-radius: 0 10px 10px 10px; flex: 1;
        }
        .msg-u { color: var(--neon-cyan); font-size: 12px; font-weight: bold; margin-bottom: 4px; }
        .msg-t { color: #666; font-size: 10px; float: right; }
        .msg-txt { font-size: 13px; color: #ddd; word-break: break-all; }

        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .media-card { background: #000; border: 1px solid #333; position: relative; height: 140px; }
        .media-card img { width: 100%; height: 100%; object-fit: cover; }
        .media-tag { position: absolute; bottom:0; width:100%; background:rgba(0,0,0,0.8); color:#fff; font-size:10px; padding:3px; }

        /* =========================================
           7. BOT STATUS PAGE
           ========================================= */
        .bot-row {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(0,0,0,0.4); border-left: 3px solid #333;
            padding: 10px; margin-bottom: 8px;
        }
        .bot-row.online { border-left-color: var(--neon-green); background: rgba(0,255,10,0.05); }
        .bot-row.offline { border-left-color: var(--neon-red); }

        /* =========================================
           8. NAVIGATION DOCK
           ========================================= */
        .dock {
            position: fixed; bottom: 0; width: 100%; height: 80px;
            background: #050508; border-top: 1px solid #333;
            display: flex; justify-content: space-around; align-items: center;
            z-index: 100; box-shadow: 0 -10px 20px rgba(0,0,0,0.5);
        }
        .dock-item {
            text-align: center; color: #555; transition: 0.3s;
            display: flex; flex-direction: column; align-items: center;
        }
        .dock-item svg { width: 24px; height: 24px; fill: currentColor; margin-bottom: 5px; }
        .dock-item span { font-size: 10px; font-weight: bold; }
        .dock-item.active { color: var(--neon-cyan); transform: translateY(-5px); text-shadow: 0 0 10px var(--neon-cyan); }

        /* BOOT OVERLAY */
        #boot-layer {
            position: fixed; top:0; left:0; width:100%; height:100%; background:#000;
            z-index: 9999; display: flex; align-items: center; justify-content: center;
            font-family: var(--font-code); color: var(--neon-green); font-size: 12px;
        }
    </style>
</head>
<body>

    <div class="digital-grid"></div>
    <div class="particles"></div>

    <!-- BOOT SEQUENCE -->
    <div id="boot-layer">
        <div>
            <div>INITIALIZING TITAN KERNEL...</div>
            <div id="boot-txt"></div>
        </div>
    </div>

    <!-- 1. LOGIN PAGE -->
    <div id="p-login" class="page active" style="display:flex; flex-direction:column; justify-content:center;">
        <div class="scene-3d">
            <div class="cube" id="loginCube">
                <div class="face f-fr">TITAN</div>
                <div class="face f-bk">SEC</div>
                <div class="face f-rt">NET</div>
                <div class="face f-lt">SYS</div>
                <div class="face f-tp"></div>
                <div class="face f-bm"></div>
            </div>
        </div>
        <h2 style="text-align:center; color:var(--neon-cyan); margin-bottom:30px;">TITAN OS XI</h2>
        
        <div class="titan-card">
            <div class="card-head">SECURE LOGIN</div>
            <input type="text" id="ipt-room" class="cyber-input" value="ملتقى🥂العرب" placeholder="ROOM NAME">
            <textarea id="ipt-creds" class="cyber-input" rows="3" placeholder="User#Pass@User#Pass"></textarea>
            <button class="cyber-btn" onclick="sys.login()">INITIATE UPLINK</button>
        </div>
    </div>

    <!-- 2. DASHBOARD (BOT STATUS) -->
    <div id="p-dash" class="page">
        <div class="titan-card" style="text-align:center; border-color:var(--neon-green)">
            <h1 style="color:var(--neon-green); margin:0;">ACCESS GRANTED</h1>
            <p style="color:#888; font-size:12px;">WELCOME TO THE GRID</p>
        </div>

        <div class="titan-card">
            <div class="card-head">BOTNET STATUS</div>
            <div id="bot-list"></div>
        </div>
    </div>

    <!-- 3. RADAR -->
    <div id="p-radar" class="page">
        <div class="titan-card">
            <div class="card-head">SONAR TRACKING <span id="r-count" style="color:#fff">0</span></div>
            <div class="radar-frame" id="radar-scope">
                <div class="radar-scan"></div>
                <!-- SHIPS INJECTED HERE -->
            </div>
        </div>
        <div class="titan-card">
            <div class="card-head">DETECTED ENTITIES</div>
            <div id="radar-logs" style="font-size:12px; color:#aaa; max-height:200px; overflow:auto;"></div>
        </div>
    </div>

    <!-- 4. CHAT -->
    <div id="p-chat" class="page">
        <div class="titan-card">
            <div class="card-head">
                <span>GLOBAL FEED</span>
                <button style="background:none; border:1px solid var(--neon-cyan); color:var(--neon-cyan); font-size:10px; cursor:pointer;" onclick="sys.exportChat()">EXPORT</button>
            </div>
            <div id="chat-box" style="padding-bottom:20px;"></div>
        </div>
    </div>

    <!-- 5. VAULT -->
    <div id="p-vault" class="page">
        <div class="titan-card">
            <div class="card-head">SECURE VAULT</div>
            <div id="vault-grid" class="vault-grid"></div>
        </div>
    </div>

    <!-- NAVIGATION -->
    <div id="nav-dock" class="dock hidden">
        <div class="dock-item" onclick="sys.nav('p-dash', this)">
            <svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
            <span>STATUS</span>
        </div>
        <div class="dock-item" onclick="sys.nav('p-radar', this)">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5.5-2.5l7.51-3.49L17.5 6.5 9.99 9.99 6.5 17.5zm5.5-6.6c.61 0 1.1.49 1.1 1.1s-.49 1.1-1.1 1.1-1.1-.49-1.1-1.1.49-1.1 1.1-1.1z"/></svg>
            <span>RADAR</span>
        </div>
        <div class="dock-item" onclick="sys.nav('p-chat', this)">
            <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>
            <span>FEED</span>
        </div>
        <div class="dock-item" onclick="sys.nav('p-vault', this)">
            <svg viewBox="0 0 24 24"><path d="M22 16V4c0-1.1-.9-2-2-2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2zm-11-4l2.03 2.71L16 11l4 5H8l3-4zM2 6v14c0 1.1.9 2 2 2h14v-2H4V6H2z"/></svg>
            <span>VAULT</span>
        </div>
    </div>

<script>
class TitanSystem {
    constructor() {
        this.wsUrl = "wss://chatp.net:5333/server";
        this.users = new Map();
        this.chats = [];
        this.activeAvatars = [];
        this.bots = [];
    }

    // --- SYSTEM BOOT ---
    boot() {
        let txt = document.getElementById('boot-txt');
        let steps = ["LOADING CORE...", "CONNECTING TO SATELLITE...", "DECRYPTING PROTOCOLS...", "SYSTEM READY"];
        let i = 0;
        let t = setInterval(() => {
            if(i >= steps.length) {
                clearInterval(t);
                document.getElementById('boot-layer').style.display = 'none';
            }
            txt.innerText = steps[i];
            i++;
        }, 800);

        // Anti-Disconnect Heartbeat
        setInterval(() => this.heartbeat(), 5000);
        
        // Cube Rotation with Faces
        setInterval(() => this.rotateCubeFaces(), 2000);
    }

    heartbeat() {
        this.bots.forEach(b => {
            if(b.ws && b.ws.readyState === 1) b.ws.send(JSON.stringify({handler:"ping"}));
        });
    }

    // --- LOGIN ---
    login() {
        let room = document.getElementById('ipt-room').value;
        let creds = document.getElementById('ipt-creds').value;
        if(!creds.includes("#")) return alert("INVALID CREDENTIALS");

        document.getElementById('p-login').classList.remove('active');
        document.getElementById('p-dash').classList.add('active');
        document.getElementById('nav-dock').classList.remove('hidden');

        let list = creds.split("@");
        document.getElementById('bot-list').innerHTML = "";

        list.forEach((c, i) => {
            if(c.includes("#")) {
                let [u, p] = c.split("#");
                this.spawnBot(u.trim(), p.trim(), room, i);
            }
        });
    }

    spawnBot(u, p, r, i) {
        // UI Entry
        let div = document.createElement("div");
        div.className = "bot-row offline";
        div.id = `bot-${i}`;
        div.innerHTML = `<span>${u}</span> <span style="font-size:10px;">CONNECTING...</span>`;
        document.getElementById('bot-list').appendChild(div);

        let ws = new WebSocket(this.wsUrl);
        let botObj = { ws: ws, user: u, id: i };

        ws.onopen = () => ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p}));
        
        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler === "login_event" && d.type === "success") {
                ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            }
            if(d.handler === "room_event" && d.type === "room_joined") {
                let row = document.getElementById(`bot-${i}`);
                row.classList.remove('offline');
                row.classList.add('online');
                row.querySelector('span:last-child').innerText = "ONLINE";
            }
            this.processPacket(d);
        };

        ws.onclose = () => {
            let row = document.getElementById(`bot-${i}`);
            if(row) {
                row.classList.remove('online');
                row.classList.add('offline');
                row.querySelector('span:last-child').innerText = "RECONNECTING...";
            }
            setTimeout(() => this.spawnBot(u, p, r, i), 3000);
        };

        this.bots.push(botObj);
    }

    // --- CORE PROCESSING ---
    processPacket(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;

        // Fix Icon
        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        
        // Update User & Radar
        if(!this.users.has(u)) {
            let usr = {
                name: u, icon: icon || `https://ui-avatars.com/api/?name=${u}`,
                x: Math.random() * 200 + 20, // Random Pos
                y: Math.random() * 200 + 20
            };
            this.users.set(u, usr);
            this.addRadarShip(usr);
            if(icon) this.activeAvatars.push(icon);
            
            // Log to Radar Text
            let log = document.getElementById('radar-logs');
            log.innerHTML = `<div>[${new Date().toLocaleTimeString()}] DETECTED: ${u}</div>` + log.innerHTML;
        }

        // Chat & Vault
        if(d.type === "text" || d.type === "image") {
            this.addChat(u, this.users.get(u).icon, d.body, d.type);
            
            if(d.type === "image") {
                 this.addVault(u, d.url);
            } else if (d.body.match(/http.*(jpg|png|jpeg)/i)) {
                this.addVault(u, d.body.match(/http.*(jpg|png|jpeg)/i)[0]);
            }
        }
    }

    // --- UI MODULES ---
    addRadarShip(u) {
        let scope = document.getElementById('radar-scope');
        let ship = document.createElement('div');
        ship.className = 'ship-blip';
        ship.style.left = u.x + "px";
        ship.style.top = u.y + "px";
        ship.innerHTML = `
            <div class="ship-avatar" style="background-image:url(${u.icon})"></div>
            <div class="ship-body"></div>
            <div class="ship-name">${u.name}</div>
        `;
        scope.appendChild(ship);
        document.getElementById('r-count').innerText = this.users.size;
    }

    addChat(u, icon, body, type) {
        let box = document.getElementById('chat-box');
        let content = type === "image" ? "[SENT AN IMAGE]" : body;
        let html = `
            <div class="msg-row">
                <img src="${icon}" class="msg-pic">
                <div class="msg-bubble">
                    <div class="msg-u">${u} <span class="msg-t">${new Date().toLocaleTimeString()}</span></div>
                    <div class="msg-txt">${content}</div>
                </div>
            </div>
        `;
        box.insertAdjacentHTML('afterbegin', html);
        this.chats.push(`[${new Date().toLocaleTimeString()}] ${u}: ${content}`);
    }

    addVault(u, url) {
        if(!url.startsWith("http")) url = "https://chatp.net" + url;
        let grid = document.getElementById('vault-grid');
        let html = `
            <div class="media-card" onclick="window.open('${url}')">
                <img src="${url}">
                <div class="media-tag">${u}</div>
            </div>
        `;
        grid.insertAdjacentHTML('afterbegin', html);
    }

    rotateCubeFaces() {
        if(this.activeAvatars.length === 0) return;
        let faces = document.querySelectorAll('.face');
        let rFace = faces[Math.floor(Math.random()*faces.length)];
        let rImg = this.activeAvatars[Math.floor(Math.random()*this.activeAvatars.length)];
        rFace.style.backgroundImage = `url(${rImg})`;
        rFace.innerText = "";
    }

    exportChat() {
        let blob = new Blob([this.chats.join("\n")], {type: "text/plain"});
        let a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "TITAN_LOGS.txt";
        a.click();
    }

    nav(id, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        el.classList.add('active');
    }
}

const sys = new TitanSystem();
window.onload = () => sys.boot();

</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)