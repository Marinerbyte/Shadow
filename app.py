from flask import Flask, render_template_string

app = Flask(__name__)

# JINJA2 RAW BLOCK USE KIYA HAI TAAKI FLASK CODE KO CHANGE NA KARE
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS XIII</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        /* --- CORE THEME (CYBERPUNK) --- */
        :root {
            --bg: #020202;
            --panel: #0b0c10;
            --cyan: #00f3ff;
            --green: #0aff0a;
            --red: #ff003c;
            --gold: #ffd700;
            --font-head: 'Orbitron', sans-serif;
            --font-mono: 'Roboto Mono', monospace;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }

        body {
            background: var(--bg); color: #fff;
            font-family: var(--font-head); margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* BACKGROUND GRID */
        .grid-bg {
            position: fixed; top: 0; left: 0; width: 200vw; height: 200vh;
            background: linear-gradient(rgba(0, 243, 255, 0.05) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(0, 243, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
            animation: gridMove 20s linear infinite;
            z-index: -1; pointer-events: none;
        }
        @keyframes gridMove { 0% {transform: perspective(500px) rotateX(60deg) translateY(0);} 100% {transform: perspective(500px) rotateX(60deg) translateY(40px);} }

        /* --- UI CARDS --- */
        .page { display: none; height: 100%; padding: 10px; overflow-y: auto; padding-bottom: 80px; }
        .page.active { display: block; }

        .card {
            background: rgba(11, 12, 16, 0.9); border: 1px solid #333;
            border-left: 3px solid var(--cyan); border-radius: 6px;
            padding: 15px; margin-bottom: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.5);
        }
        .card-head {
            font-size: 16px; color: var(--cyan); border-bottom: 1px solid #333;
            padding-bottom: 8px; margin-bottom: 10px; display: flex; justify-content: space-between;
        }

        /* INPUTS */
        .inp {
            width: 100%; background: #000; border: 1px solid #444; color: var(--cyan);
            padding: 12px; font-family: var(--font-mono); margin-bottom: 10px; font-size: 14px;
        }
        .btn {
            width: 100%; padding: 15px; background: #002222; border: 1px solid var(--cyan);
            color: var(--cyan); font-weight: bold; cursor: pointer; font-family: var(--font-head);
            text-transform: uppercase; letter-spacing: 2px; transition: 0.3s;
        }
        .btn:active { background: var(--cyan); color: #000; }

        /* --- 3D CUBE (CSS ONLY - NO CRASH) --- */
        .cube-box { width: 100px; height: 100px; margin: 40px auto; perspective: 800px; }
        .cube {
            width: 100%; height: 100%; position: relative; transform-style: preserve-3d;
            animation: spin 8s infinite linear;
        }
        .face {
            position: absolute; width: 100px; height: 100px;
            border: 2px solid var(--cyan); background: rgba(0, 243, 255, 0.1);
            display: flex; align-items: center; justify-content: center;
            font-size: 14px; color: #fff; box-shadow: inset 0 0 15px rgba(0, 243, 255, 0.3);
            background-size: cover; background-position: center;
        }
        .f1 { transform: rotateY(0deg) translateZ(50px); }
        .f2 { transform: rotateY(180deg) translateZ(50px); }
        .f3 { transform: rotateY(90deg) translateZ(50px); }
        .f4 { transform: rotateY(-90deg) translateZ(50px); }
        .f5 { transform: rotateX(90deg) translateZ(50px); }
        .f6 { transform: rotateX(-90deg) translateZ(50px); }
        @keyframes spin { 0% {transform: rotateX(0) rotateY(0);} 100% {transform: rotateX(360deg) rotateY(360deg);} }

        /* --- SHIP RADAR --- */
        .radar-ui {
            width: 280px; height: 280px; margin: 0 auto; border-radius: 50%;
            border: 4px solid #333; background: radial-gradient(circle, #001 0%, #000 90%);
            position: relative; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
        .scan-beam {
            position: absolute; inset: 0; border-radius: 50%;
            background: conic-gradient(transparent 270deg, rgba(0, 255, 10, 0.4));
            animation: scan 4s infinite linear;
        }
        @keyframes scan { to { transform: rotate(360deg); } }
        
        .ship {
            position: absolute; width: 30px; height: 30px;
            display: flex; flex-direction: column; align-items: center;
            transform: translate(-50%, -50%); transition: all 1s ease;
            animation: hover 2s infinite ease-in-out alternate;
            z-index: 10;
        }
        @keyframes hover { from{margin-top:0;} to{margin-top:-5px;} }
        
        .ship-img { width: 24px; height: 24px; border-radius: 50%; border: 1px solid #fff; }
        .ship-tri {
            width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent;
            border-bottom: 10px solid var(--green); margin-top: -5px;
        }
        .ship-tag { font-size: 8px; color: var(--green); text-shadow: 0 0 2px #000; margin-top: 2px; }

        /* --- CHAT --- */
        .chat-box { height: 400px; overflow-y: auto; padding-right: 5px; }
        .msg { display: flex; gap: 10px; margin-bottom: 12px; }
        .msg img { width: 35px; height: 35px; border-radius: 8px; border: 1px solid #444; }
        .msg-b { flex: 1; background: #111; padding: 10px; border-radius: 0 10px 10px 10px; border: 1px solid #333; }
        .msg-h { display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 5px; }
        .msg-u { color: var(--cyan); font-weight: bold; }
        .msg-c { font-size: 13px; color: #ddd; word-break: break-all; }

        /* --- VAULT --- */
        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .v-item { background: #000; border: 1px solid #333; height: 120px; position: relative; }
        .v-item img { width: 100%; height: 100%; object-fit: cover; }
        .v-meta { position: absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:#fff; font-size:9px; padding:3px; }

        /* --- BOT STATUS --- */
        .bot-row { display: flex; justify-content: space-between; padding: 12px; background: #111; margin-bottom: 8px; border-left: 3px solid #444; }
        .bot-row.online { border-left-color: var(--green); background: rgba(0, 255, 10, 0.05); }
        .bot-row.offline { border-left-color: var(--red); }

        /* --- NAV --- */
        .nav-bar {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
            background: rgba(5, 5, 5, 0.95); border-top: 1px solid #333;
            display: flex; justify-content: space-around; align-items: center; z-index: 999;
        }
        .nav-btn { text-align: center; color: #555; font-size: 20px; transition: 0.3s; }
        .nav-btn span { display: block; font-size: 9px; font-family: var(--font-mono); margin-top: 2px; }
        .nav-btn.active { color: var(--cyan); transform: translateY(-5px); text-shadow: 0 0 10px var(--cyan); }
    </style>
</head>
<body>

{% raw %}
    <div class="grid-bg"></div>

    <!-- 1. LOGIN -->
    <div id="p-login" class="page active">
        <div style="text-align:center;">
            <div class="cube-box">
                <div class="cube" id="loginCube">
                    <div class="face f1">TITAN</div><div class="face f2">OS</div>
                    <div class="face f3">XII</div><div class="face f4">SEC</div>
                    <div class="face f5"></div><div class="face f6"></div>
                </div>
            </div>
            <h2 style="color:var(--cyan); letter-spacing:4px; margin-bottom:5px;">TITAN OS XIII</h2>
            <div style="font-size:10px; color:#666; margin-bottom:30px;">ADVANCED SURVEILLANCE SYSTEM</div>
        </div>

        <div class="card">
            <div class="card-head">SYSTEM ENTRY</div>
            <label style="font-size:10px; color:#888;">TARGET ROOM</label>
            <input type="text" id="room" class="inp" value="ملتقى🥂العرب">
            <label style="font-size:10px; color:#888;">BOTS (User#Pass)</label>
            <textarea id="creds" class="inp" rows="3" placeholder="Spy1#pass@Spy2#pass"></textarea>
            <button class="btn" onclick="sys.login()">ACCESS SYSTEM</button>
        </div>
    </div>

    <!-- 2. STATUS -->
    <div id="p-status" class="page">
        <div class="card" style="text-align:center; border-color:var(--green)">
            <h1 style="color:var(--green); margin:0;">CONNECTED</h1>
            <div style="font-size:11px; color:#aaa;">SYSTEM ACTIVE • MONITORING</div>
        </div>
        <div class="card">
            <div class="card-head">BOTNET STATUS</div>
            <div id="bot-list"></div>
        </div>
    </div>

    <!-- 3. RADAR -->
    <div id="p-radar" class="page">
        <div class="card">
            <div class="card-head">SHIP RADAR <span id="r-count" style="color:#fff">0</span></div>
            <div class="radar-ui" id="radar">
                <div class="scan-beam"></div>
                <!-- SHIPS -->
            </div>
        </div>
    </div>

    <!-- 4. CHAT -->
    <div id="p-chat" class="page">
        <div class="card">
            <div class="card-head">
                LIVE INTERCEPT
                <button onclick="sys.exportChat()" style="background:none; border:1px solid #555; color:#fff; font-size:10px; cursor:pointer;">EXPORT .TXT</button>
            </div>
            <div class="chat-box" id="chat-box"></div>
        </div>
    </div>

    <!-- 5. VAULT -->
    <div id="p-vault" class="page">
        <div class="card">
            <div class="card-head">MEDIA VAULT</div>
            <div class="vault-grid" id="vault-box"></div>
        </div>
    </div>

    <!-- NAV -->
    <div class="nav-bar" id="navbar" style="display:none">
        <div class="nav-btn active" onclick="sys.nav('p-status', this)">⚙️<span>SYS</span></div>
        <div class="nav-btn" onclick="sys.nav('p-radar', this)">📡<span>RADAR</span></div>
        <div class="nav-btn" onclick="sys.nav('p-chat', this)">💬<span>FEED</span></div>
        <div class="nav-btn" onclick="sys.nav('p-vault', this)">📂<span>VAULT</span></div>
    </div>

<script>
class System {
    constructor() {
        this.ws = "wss://chatp.net:5333/server";
        this.users = new Map();
        this.logs = [];
        this.imgs = [];
        this.bots = [];
    }

    nav(id, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(el) el.classList.add('active');
    }

    login() {
        let room = document.getElementById('room').value;
        let creds = document.getElementById('creds').value;
        if(!creds.includes("#")) return alert("Check Format: User#Pass");

        document.getElementById('p-login').classList.remove('active');
        document.getElementById('p-status').classList.add('active');
        document.getElementById('navbar').style.display = "flex";

        let list = creds.split("@");
        document.getElementById('bot-list').innerHTML = "";

        list.forEach((c, i) => {
            if(c.includes("#")) {
                let [u, p] = c.split("#");
                this.connectBot(u.trim(), p.trim(), room, i);
            }
        });

        // Anti-Disconnect Features
        setInterval(() => this.heartbeat(), 5000);
        setInterval(() => this.updateCube(), 2000);
        if(navigator.wakeLock) navigator.wakeLock.request('screen').catch(e=>{});
    }

    connectBot(u, p, r, i) {
        let div = document.createElement('div');
        div.className = 'bot-row offline'; div.id = `bot-${i}`;
        div.innerHTML = `<b>${u}</b> <span id="st-${i}">CONNECTING...</span>`;
        document.getElementById('bot-list').appendChild(div);

        let ws = new WebSocket(this.ws);
        let bot = { ws: ws, u: u, p: p, r: r, id: i };
        this.bots.push(bot);

        ws.onopen = () => ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p}));
        
        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler === "login_event" && d.type === "success") {
                ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            }
            if(d.handler === "room_event" && d.type === "room_joined") {
                let row = document.getElementById(`bot-${i}`);
                row.className = 'bot-row online';
                document.getElementById(`st-${i}`).innerText = "ONLINE";
            }
            this.parse(d);
        };

        ws.onclose = () => {
            let row = document.getElementById(`bot-${i}`);
            row.className = 'bot-row offline';
            document.getElementById(`st-${i}`).innerText = "RECONNECTING...";
            setTimeout(() => this.connectBot(u, p, r, i), 3000);
        };
    }

    heartbeat() {
        this.bots.forEach(b => {
            if(b.ws && b.ws.readyState === 1) b.ws.send(JSON.stringify({handler:"ping"}));
        });
    }

    parse(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;

        // Clean Icon
        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        if(icon && !this.imgs.includes(icon)) this.imgs.push(icon);

        // Radar Logic
        if(!this.users.has(u)) {
            let usr = { 
                name: u, 
                pic: icon || `https://ui-avatars.com/api/?name=${u}`,
                x: Math.random() * 200 + 40,
                y: Math.random() * 200 + 40
            };
            this.users.set(u, usr);
            this.spawnShip(usr);
        }

        // Chat & Vault Logic
        if(d.type === "text" || d.type === "image") {
            let txt = d.type === "image" ? "[SENT IMAGE]" : d.body;
            this.addChat(u, this.users.get(u).pic, txt);
            
            // Image Vault
            if(d.type === "image") this.addVault(u, d.url);
            // Link Sniffer
            if(d.body && d.body.match(/http.*(jpg|png|jpeg)/i)) {
                this.addVault(u, d.body.match(/http.*(jpg|png|jpeg)/i)[0]);
            }
        }
    }

    spawnShip(u) {
        let box = document.getElementById('radar');
        let html = `
            <div class="ship" style="left:${u.x}px; top:${u.y}px">
                <img src="${u.pic}" class="ship-img">
                <div class="ship-tri"></div>
                <div class="ship-tag">${u.name}</div>
            </div>
        `;
        box.insertAdjacentHTML('beforeend', html);
        document.getElementById('r-count').innerText = this.users.size;
    }

    addChat(u, pic, txt) {
        let box = document.getElementById('chat-box');
        let html = `
            <div class="msg">
                <img src="${pic}">
                <div class="msg-b">
                    <div class="msg-h"><span class="msg-u">${u}</span> <span>${new Date().toLocaleTimeString()}</span></div>
                    <div class="msg-c">${txt}</div>
                </div>
            </div>`;
        box.insertAdjacentHTML('afterbegin', html);
        this.logs.push(`[${new Date().toLocaleTimeString()}] ${u}: ${txt}`);
    }

    addVault(u, url) {
        if(!url.startsWith("http")) url = "https://chatp.net" + url;
        let box = document.getElementById('vault-box');
        let html = `
            <div class="v-item" onclick="window.open('${url}')">
                <img src="${url}">
                <div class="v-meta">${u}</div>
            </div>`;
        box.insertAdjacentHTML('afterbegin', html);
    }

    updateCube() {
        if(this.imgs.length < 1) return;
        let faces = document.querySelectorAll('.face');
        let f = faces[Math.floor(Math.random() * faces.length)];
        let img = this.imgs[Math.floor(Math.random() * this.imgs.length)];
        f.style.backgroundImage = `url(${img})`;
        f.innerText = "";
    }

    exportChat() {
        let blob = new Blob([this.logs.join("\n")], {type: "text/plain"});
        let a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "TITAN_LOGS.txt";
        a.click();
    }
}

const sys = new System();
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