from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS XII</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #050505;
            --panel: #0a0f0a;
            --primary: #00ff41; /* Hacker Green */
            --secondary: #008F11;
            --alert: #ff003c;
            --glass: rgba(0, 20, 0, 0.8);
            --font-head: 'Rajdhani', sans-serif;
            --font-mono: 'Share Tech Mono', monospace;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }
        
        body {
            background: var(--bg); color: var(--primary);
            font-family: var(--font-head);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* --- BOOT SCREEN (FIXED) --- */
        #boot-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 9999;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            font-family: var(--font-mono);
        }
        .loading-bar {
            width: 200px; height: 4px; background: #333; margin-top: 20px;
            position: relative; overflow: hidden;
        }
        .loading-bar::after {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--primary); transform: translateX(-100%);
            animation: load 2s ease-in-out forwards;
        }
        @keyframes load { to { transform: translateX(0); } }

        /* Fail Safe Button */
        #force-btn {
            margin-top: 30px; padding: 10px 20px; border: 1px solid var(--primary);
            color: var(--primary); background: transparent; font-family: var(--font-mono);
            display: none; cursor: pointer;
        }

        /* --- MAIN UI --- */
        .page { display: none; height: 100%; padding: 15px; overflow-y: auto; padding-bottom: 90px; }
        .page.active { display: block; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from{opacity:0; transform:translateY(10px);} to{opacity:1; transform:translateY(0);} }

        .card {
            background: var(--panel); border: 1px solid #1a2f1a;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
            border-radius: 6px; padding: 15px; margin-bottom: 15px;
            position: relative;
        }
        .card-head {
            font-family: var(--font-mono); font-size: 16px; 
            border-bottom: 1px solid #1a2f1a; padding-bottom: 8px; margin-bottom: 10px;
            display: flex; justify-content: space-between;
        }

        /* --- 3D CUBE (LOGIN) --- */
        .scene { width: 100px; height: 100px; margin: 20px auto; perspective: 600px; }
        .cube {
            width: 100%; height: 100%; position: relative; transform-style: preserve-3d;
            animation: rot 8s infinite linear;
        }
        .face {
            position: absolute; width: 100px; height: 100px;
            border: 2px solid var(--primary); background: rgba(0, 255, 65, 0.1);
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; color: #fff; background-size: cover; background-position: center;
        }
        .f-f { transform: rotateY(0deg) translateZ(50px); }
        .f-b { transform: rotateY(180deg) translateZ(50px); }
        .f-r { transform: rotateY(90deg) translateZ(50px); }
        .f-l { transform: rotateY(-90deg) translateZ(50px); }
        .f-t { transform: rotateX(90deg) translateZ(50px); }
        .f-d { transform: rotateX(-90deg) translateZ(50px); }
        @keyframes rot { from{transform: rotateX(0) rotateY(0);} to{transform: rotateX(360deg) rotateY(360deg);} }

        /* --- INPUTS --- */
        input, textarea {
            width: 100%; background: #000; border: 1px solid #333; color: var(--primary);
            padding: 12px; font-family: var(--font-mono); margin-bottom: 10px;
        }
        button.btn-main {
            width: 100%; padding: 15px; background: #001a00; border: 1px solid var(--primary);
            color: var(--primary); font-weight: bold; cursor: pointer; text-transform: uppercase;
        }
        button.btn-main:active { background: var(--primary); color: #000; }

        /* --- RADAR (SHIPS) --- */
        .radar-box {
            width: 280px; height: 280px; margin: 0 auto;
            background: radial-gradient(circle, #001a00 0%, #000 80%);
            border: 2px solid var(--secondary); border-radius: 50%;
            position: relative; overflow: hidden;
        }
        .scan-line {
            width: 100%; height: 100%; border-radius: 50%; position: absolute;
            background: conic-gradient(transparent 270deg, rgba(0, 255, 65, 0.5));
            animation: scan 3s infinite linear;
        }
        @keyframes scan { to{transform: rotate(360deg);} }
        
        .ship {
            position: absolute; width: 20px; height: 20px;
            transform: translate(-50%, -50%); transition: all 1s;
        }
        .ship-tri {
            width: 0; height: 0; border-left: 6px solid transparent;
            border-right: 6px solid transparent; border-bottom: 15px solid var(--primary);
        }
        .ship-img {
            position: absolute; top: -15px; left: -5px; width: 22px; height: 22px;
            border-radius: 50%; border: 1px solid #fff;
        }
        .ship-name {
            position: absolute; top: 20px; left: -20px; width: 60px; text-align: center;
            font-size: 9px; color: #fff; text-shadow: 0 0 2px #000;
        }

        /* --- CHAT --- */
        .msg-box { height: 400px; overflow-y: scroll; border: 1px solid #222; padding: 10px; background: #020202; }
        .msg { display: flex; gap: 10px; margin-bottom: 12px; border-bottom: 1px solid #111; padding-bottom: 8px; }
        .msg img { width: 35px; height: 35px; border-radius: 50%; border: 1px solid #333; }
        .msg-body { flex: 1; }
        .msg-top { display: flex; justify-content: space-between; font-size: 11px; color: #666; }
        .msg-u { color: var(--primary); font-weight: bold; }
        .msg-text { font-size: 13px; color: #ccc; margin-top: 2px; }

        /* --- VAULT --- */
        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .v-item { background: #000; border: 1px solid #222; text-align: center; overflow: hidden; }
        .v-item img { width: 100%; height: 100px; object-fit: cover; display: block; }
        .v-item audio { width: 100%; filter: invert(1); height: 30px; }
        .v-tag { font-size: 10px; padding: 4px; color: #777; }

        /* --- NAV --- */
        .nav {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
            background: #080808; border-top: 1px solid #222;
            display: flex; justify-content: space-around; align-items: center;
            z-index: 100;
        }
        .n-btn { text-align: center; color: #444; font-size: 20px; padding: 10px; }
        .n-btn span { display: block; font-size: 10px; font-family: var(--font-mono); }
        .n-btn.active { color: var(--primary); text-shadow: 0 0 10px var(--primary); }

        /* --- BOT LIST --- */
        .bot-row { display: flex; justify-content: space-between; padding: 10px; background: #111; margin-bottom: 5px; border-left: 3px solid #333; }
        .bot-row.on { border-left-color: var(--primary); background: rgba(0,255,65,0.05); }
        .bot-row.off { border-left-color: var(--alert); }
        
    </style>
</head>
<body>

    <!-- BOOT SCREEN -->
    <div id="boot-screen">
        <div style="font-size: 20px;">TITAN OS <span style="color:#fff">XII</span></div>
        <div style="font-size: 12px; color:#666; margin-top:5px;">INITIALIZING KERNEL...</div>
        <div class="loading-bar"></div>
        <button id="force-btn" onclick="sys.startUI()">[ FORCE ENTRY ]</button>
    </div>

    <!-- 1. LOGIN -->
    <div id="p-login" class="page active">
        <div style="text-align:center; padding-top:20px;">
            <div class="scene">
                <div class="cube" id="loginCube">
                    <div class="face f-f">SYS</div><div class="face f-b">NET</div>
                    <div class="face f-r">SEC</div><div class="face f-l">DAT</div>
                    <div class="face f-t"></div><div class="face f-d"></div>
                </div>
            </div>
            <h2>ACCESS CONTROL</h2>
        </div>

        <div class="card">
            <label>TARGET FREQUENCY (Room)</label>
            <input type="text" id="room" value="ملتقى🥂العرب">
            <label>AGENTS (User#Pass)</label>
            <textarea id="creds" rows="3" placeholder="Spy1#123@Spy2#123"></textarea>
            <button class="btn-main" onclick="sys.connect()">ESTABLISH LINK</button>
        </div>
    </div>

    <!-- 2. STATUS -->
    <div id="p-status" class="page">
        <div class="card" style="text-align:center;">
            <h1 style="margin:0; color:#fff">WELCOME</h1>
            <div style="font-size:12px; color:var(--primary)">SECURE CONNECTION ESTABLISHED</div>
        </div>
        <div class="card">
            <div class="card-head">ACTIVE BOTS</div>
            <div id="bot-list"></div>
        </div>
    </div>

    <!-- 3. RADAR -->
    <div id="p-radar" class="page">
        <div class="card">
            <div class="card-head">SHIP RADAR <span id="u-count" style="color:#fff">0</span></div>
            <div class="radar-box" id="radar">
                <div class="scan-line"></div>
                <!-- SHIPS GO HERE -->
            </div>
        </div>
    </div>

    <!-- 4. CHAT -->
    <div id="p-chat" class="page">
        <div class="card">
            <div class="card-head">
                INTERCEPT LOG
                <button onclick="sys.export()" style="background:none; border:1px solid #444; color:#fff; font-size:10px;">EXPORT</button>
            </div>
            <div class="msg-box" id="chatbox"></div>
        </div>
    </div>

    <!-- 5. VAULT -->
    <div id="p-vault" class="page">
        <div class="card">
            <div class="card-head">MEDIA VAULT</div>
            <div class="vault-grid" id="vault"></div>
        </div>
    </div>

    <!-- NAV -->
    <div class="nav" id="navbar" style="display:none">
        <div class="n-btn" onclick="sys.page('p-status', this)">⚙️<span>SYS</span></div>
        <div class="n-btn" onclick="sys.page('p-radar', this)">📡<span>RADAR</span></div>
        <div class="n-btn" onclick="sys.page('p-chat', this)">💬<span>CHAT</span></div>
        <div class="n-btn" onclick="sys.page('p-vault', this)">📂<span>VAULT</span></div>
    </div>

<script>
class Titan {
    constructor() {
        this.ws = "wss://chatp.net:5333/server";
        this.bots = [];
        this.users = new Map();
        this.msgs = [];
        this.activeImgs = [];
    }

    startUI() {
        document.getElementById('boot-screen').style.display = 'none';
    }

    page(id, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.n-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(el) el.classList.add('active');
    }

    connect() {
        let raw = document.getElementById('creds').value;
        let room = document.getElementById('room').value;
        if(!raw.includes("#")) return alert("Invalid Credentials!");

        let list = raw.split("@");
        document.getElementById('bot-list').innerHTML = "";
        
        list.forEach((c, i) => {
            if(c.includes("#")) {
                let [u, p] = c.split("#");
                this.spawn(u.trim(), p.trim(), room, i);
            }
        });

        this.page('p-status');
        document.getElementById('navbar').style.display = "flex";
        
        // Anti-Disconnect (WakeLock)
        if('wakeLock' in navigator) navigator.wakeLock.request('screen').catch(e=>{});
        setInterval(() => this.cubeRot(), 2000);
    }

    spawn(u, p, r, i) {
        // UI
        let div = document.createElement('div');
        div.className = 'bot-row off'; div.id = `b-${i}`;
        div.innerHTML = `<b>${u}</b> <span>CONNECTING...</span>`;
        document.getElementById('bot-list').appendChild(div);

        let ws = new WebSocket(this.ws);
        
        ws.onopen = () => {
            ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p}));
            setInterval(() => { if(ws.readyState==1) ws.send(JSON.stringify({handler:"ping"})); }, 5000);
        };

        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler==="login_event" && d.type==="success") ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            if(d.handler==="room_event" && d.type==="room_joined") {
                let el = document.getElementById(`b-${i}`);
                el.className = 'bot-row on';
                el.querySelector('span').innerText = "ONLINE";
            }
            this.handle(d);
        };
        
        ws.onclose = () => {
            let el = document.getElementById(`b-${i}`);
            el.className = 'bot-row off';
            el.querySelector('span').innerText = "RETRYING...";
            setTimeout(() => this.spawn(u, p, r, i), 3000);
        };
    }

    handle(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;

        // Fix Icon
        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        if(icon && !this.activeImgs.includes(icon)) this.activeImgs.push(icon);

        // 1. RADAR / USER DB
        if(!this.users.has(u)) {
            let usr = { 
                name: u, 
                pic: icon || `https://ui-avatars.com/api/?name=${u}`,
                x: Math.random()*200 + 40, 
                y: Math.random()*200 + 40 
            };
            this.users.set(u, usr);
            this.drawShip(usr);
        }

        // 2. CHAT & VAULT
        if(d.type === "text" || d.type === "image") {
            let body = d.body;
            if(d.type === "image") body = "[IMAGE]";
            
            // Add to Chat
            this.addChat(u, this.users.get(u).pic, body);
            
            // Add to Vault (Image/Audio)
            if(d.type === "image" || (body && body.match(/http.*\.(jpg|png|mp3|wav|ogg)/i))) {
                let url = d.type === "image" ? d.url : body.match(/http.*\.(jpg|png|mp3|wav|ogg)/i)[0];
                if(!url.startsWith("http")) url = "https://chatp.net" + url;
                this.addVault(u, url);
            }
        }
    }

    drawShip(u) {
        let box = document.getElementById('radar');
        let div = document.createElement('div');
        div.className = 'ship';
        div.style.left = u.x + "px"; div.style.top = u.y + "px";
        div.innerHTML = `<img src="${u.pic}" class="ship-img"><div class="ship-tri"></div><div class="ship-name">${u.name}</div>`;
        box.appendChild(div);
        document.getElementById('u-count').innerText = this.users.size;
    }

    addChat(u, pic, txt) {
        let box = document.getElementById('chatbox');
        let html = `
            <div class="msg">
                <img src="${pic}">
                <div class="msg-body">
                    <div class="msg-top"><span class="msg-u">${u}</span> <span>${new Date().toLocaleTimeString()}</span></div>
                    <div class="msg-text">${txt}</div>
                </div>
            </div>`;
        box.insertAdjacentHTML('afterbegin', html);
        this.msgs.push(`[${new Date().toLocaleTimeString()}] ${u}: ${txt}`);
    }

    addVault(u, url) {
        let box = document.getElementById('vault');
        let isAud = url.match(/\.(mp3|wav|ogg)/i);
        let content = isAud ? `<audio controls src="${url}"></audio>` : `<img src="${url}" onclick="window.open('${url}')">`;
        let html = `<div class="v-item">${content}<div class="v-tag">${u}</div></div>`;
        box.insertAdjacentHTML('afterbegin', html);
    }

    cubeRot() {
        if(this.activeImgs.length < 1) return;
        let faces = document.querySelectorAll('.face');
        let f = faces[Math.floor(Math.random()*faces.length)];
        let img = this.activeImgs[Math.floor(Math.random()*this.activeImgs.length)];
        f.style.backgroundImage = `url(${img})`;
        f.innerText = "";
    }

    export() {
        let blob = new Blob([this.msgs.join("\n")], {type: "text/plain"});
        let a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "TITAN_CHAT.txt";
        a.click();
    }
}

const sys = new Titan();

// AUTO BOOT AFTER 3 SECONDS (FAIL SAFE)
setTimeout(() => {
    document.getElementById('force-btn').style.display = 'block';
    sys.startUI();
}, 3500);

</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)