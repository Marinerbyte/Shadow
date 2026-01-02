from flask import Flask, render_template_string

app = Flask(__name__)

# FLASK TEMPLATE HANDLING
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS XIV | UNLOCKED</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        /* --- 1. THEME: DARK MATTER --- */
        :root {
            --bg: #000000;
            --panel: #0a0a0c;
            --cyan: #00f3ff;
            --green: #0aff0a;
            --red: #ff003c;
            --font-head: 'Orbitron', sans-serif;
            --font-mono: 'Share Tech Mono', monospace;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }
        
        body {
            background: var(--bg); color: #fff;
            font-family: var(--font-head);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* --- 2. ANIMATED BACKGROUND --- */
        .cyber-grid {
            position: fixed; top: 0; left: 0; width: 200vw; height: 200vh;
            background: 
                linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px), 
                linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
            animation: moveGrid 10s linear infinite;
            z-index: -1; pointer-events: none;
        }
        @keyframes moveGrid { from {transform: perspective(500px) rotateX(60deg) translateY(0);} to {transform: perspective(500px) rotateX(60deg) translateY(40px);} }

        /* --- 3. PAGE SYSTEM --- */
        .viewport {
            flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 90px;
            position: relative;
        }
        .page { display: none; animation: fadeIn 0.5s ease-out; }
        .page.active { display: block; }
        @keyframes fadeIn { from{opacity:0; transform:translateY(20px);} to{opacity:1; transform:translateY(0);} }

        /* CARDS */
        .card {
            background: rgba(10, 15, 20, 0.9);
            border: 1px solid #333; border-left: 3px solid var(--cyan);
            border-radius: 6px; padding: 15px; margin-bottom: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }
        .card-h {
            color: var(--cyan); font-size: 14px; border-bottom: 1px solid #333;
            padding-bottom: 8px; margin-bottom: 10px; display: flex; justify-content: space-between;
        }

        /* --- 4. 3D CUBE (LOGIN) --- */
        .cube-container { width: 100px; height: 100px; margin: 30px auto; perspective: 800px; }
        .cube {
            width: 100%; height: 100%; position: relative; transform-style: preserve-3d;
            animation: spin 6s infinite linear;
        }
        .face {
            position: absolute; width: 100px; height: 100px;
            background: rgba(0, 243, 255, 0.1); border: 2px solid var(--cyan);
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; color: #fff; box-shadow: 0 0 15px rgba(0,243,255,0.2);
            background-size: cover; background-position: center;
        }
        .f1 { transform: translateZ(50px); }
        .f2 { transform: rotateY(180deg) translateZ(50px); }
        .f3 { transform: rotateY(90deg) translateZ(50px); }
        .f4 { transform: rotateY(-90deg) translateZ(50px); }
        .f5 { transform: rotateX(90deg) translateZ(50px); }
        .f6 { transform: rotateX(-90deg) translateZ(50px); }
        @keyframes spin { 100% { transform: rotateX(360deg) rotateY(360deg); } }

        /* --- 5. CONTROLS --- */
        input, textarea {
            width: 100%; background: #000; border: 1px solid #444; color: var(--cyan);
            padding: 12px; font-family: var(--font-mono); margin-bottom: 10px;
        }
        .btn {
            width: 100%; padding: 15px; background: rgba(0,243,255,0.1);
            border: 1px solid var(--cyan); color: var(--cyan);
            font-family: var(--font-head); font-weight: bold; cursor: pointer;
            text-transform: uppercase; margin-bottom: 10px;
        }
        .btn-demo { border-color: var(--green); color: var(--green); background: rgba(0,255,10,0.1); }

        /* --- 6. RADAR UI --- */
        .radar-box {
            width: 280px; height: 280px; margin: 0 auto; border-radius: 50%;
            border: 2px solid #333; background: radial-gradient(#002 0%, #000 80%);
            position: relative; overflow: hidden;
            box-shadow: 0 0 20px rgba(0,243,255,0.1);
        }
        .scanner {
            position: absolute; inset: 0; border-radius: 50%;
            background: conic-gradient(transparent 270deg, rgba(0,255,10,0.4));
            animation: scan 4s infinite linear;
        }
        @keyframes scan { to { transform: rotate(360deg); } }
        
        .ship {
            position: absolute; width: 30px; height: 30px; transform: translate(-50%, -50%);
            display: flex; flex-direction: column; align-items: center;
            transition: all 1s; animation: hover 2s infinite alternate; z-index: 10;
        }
        @keyframes hover { from{margin-top:0;} to{margin-top:-5px;} }
        
        .ship-img { width: 24px; height: 24px; border-radius: 50%; border: 1px solid #fff; }
        .ship-body { 
            width: 0; height: 0; border-left: 5px solid transparent; 
            border-right: 5px solid transparent; border-bottom: 10px solid var(--green); 
        }

        /* --- 7. CHAT --- */
        .chat-container { height: 350px; overflow-y: auto; }
        .msg { display: flex; gap: 10px; margin-bottom: 10px; border-bottom: 1px solid #222; padding-bottom: 5px; }
        .msg img { width: 35px; height: 35px; border-radius: 6px; border: 1px solid #444; }
        .msg-c { flex: 1; font-family: var(--font-mono); font-size: 12px; color: #ccc; }
        .msg-n { color: var(--cyan); font-weight: bold; font-size: 11px; margin-bottom: 2px; }

        /* --- 8. VAULT --- */
        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .v-card { background: #000; border: 1px solid #333; text-align: center; }
        .v-card img { width: 100%; height: 100px; object-fit: cover; }
        
        /* --- 9. NAV BAR --- */
        .nav {
            position: fixed; bottom: 0; width: 100%; height: 70px;
            background: rgba(5,5,5,0.95); border-top: 1px solid #333;
            display: none; justify-content: space-around; align-items: center;
            z-index: 999;
        }
        .nav-icon { text-align: center; color: #555; transition: 0.3s; font-size: 20px; }
        .nav-icon span { display: block; font-size: 9px; font-family: var(--font-mono); }
        .nav-icon.active { color: var(--cyan); transform: translateY(-5px); text-shadow: 0 0 10px var(--cyan); }

        /* --- 10. BOT LIST --- */
        .bot-row { padding: 10px; background: #111; margin-bottom: 5px; border-left: 3px solid #555; display: flex; justify-content: space-between; }
        .bot-row.on { border-color: var(--green); background: rgba(0,255,10,0.1); }
        .bot-row.off { border-color: var(--red); }

    </style>
</head>
<body>

{% raw %}
    <div class="cyber-grid"></div>

    <!-- 1. LOGIN PAGE -->
    <div id="p-login" class="page active">
        <div style="text-align:center; margin-top:20px;">
            <div class="cube-container">
                <div class="cube" id="cube">
                    <div class="face f1">TITAN</div><div class="face f2">OS</div>
                    <div class="face f3">XIV</div><div class="face f4">SEC</div>
                    <div class="face f5"></div><div class="face f6"></div>
                </div>
            </div>
            <h1 style="color:var(--cyan); margin-bottom:5px;">TITAN OS XIV</h1>
            <div style="font-size:10px; color:#666;">ADVANCED SURVEILLANCE SUITE</div>
        </div>

        <div class="card" style="margin-top:20px;">
            <div class="card-h">SECURE LOGIN</div>
            <label style="font-size:10px; color:#aaa;">TARGET ROOM</label>
            <input type="text" id="room" value="ملتقى🥂العرب">
            <label style="font-size:10px; color:#aaa;">AGENTS (User#Pass)</label>
            <textarea id="creds" rows="2" placeholder="Spy1#pass@Spy2#pass"></textarea>
            
            <button class="btn" onclick="sys.login()">CONNECT SYSTEM</button>
            <button class="btn btn-demo" onclick="sys.demoMode()">ENTER DEMO MODE</button>
        </div>
    </div>

    <!-- 2. DASHBOARD PAGE -->
    <div id="p-dash" class="page">
        <div class="card" style="border-color:var(--green); text-align:center;">
            <h2 style="color:var(--green); margin:0;">SYSTEM ACTIVE</h2>
            <div style="font-size:10px;">MONITORING TARGET FREQUENCIES</div>
        </div>
        
        <div class="card">
            <div class="card-h">ACTIVE AGENTS</div>
            <div id="bot-list">
                <div style="padding:10px; text-align:center; color:#555;">NO AGENTS CONNECTED</div>
            </div>
        </div>
    </div>

    <!-- 3. RADAR PAGE -->
    <div id="p-radar" class="page">
        <div class="card">
            <div class="card-h">SONAR TRACKING <span id="cnt" style="color:#fff">0</span></div>
            <div class="radar-box" id="radar-scope">
                <div class="scanner"></div>
                <!-- Ships appear here -->
            </div>
        </div>
    </div>

    <!-- 4. CHAT PAGE -->
    <div id="p-chat" class="page">
        <div class="card">
            <div class="card-h">
                LIVE INTERCEPT
                <button onclick="sys.export()" style="background:none; border:1px solid #444; color:#fff; font-size:10px;">EXPORT</button>
            </div>
            <div class="chat-container" id="chat-feed"></div>
        </div>
    </div>

    <!-- 5. VAULT PAGE -->
    <div id="p-vault" class="page">
        <div class="card">
            <div class="card-h">MEDIA VAULT</div>
            <div class="vault-grid" id="vault-feed"></div>
        </div>
    </div>

    <!-- NAVIGATION BAR -->
    <div class="nav" id="navbar">
        <div class="nav-icon active" onclick="sys.go('p-dash', this)">⚙️<span>SYS</span></div>
        <div class="nav-icon" onclick="sys.go('p-radar', this)">📡<span>RADAR</span></div>
        <div class="nav-icon" onclick="sys.go('p-chat', this)">💬<span>CHAT</span></div>
        <div class="nav-icon" onclick="sys.go('p-vault', this)">📂<span>VAULT</span></div>
    </div>

<script>
class TitanCore {
    constructor() {
        this.wsUrl = "wss://chatp.net:5333/server";
        this.bots = [];
        this.users = new Map();
        this.logs = [];
        this.images = [];
    }

    // --- NAVIGATION ---
    go(pageId, el) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(pageId).classList.add('active');
        
        // Update Nav
        if(el) {
            document.querySelectorAll('.nav-icon').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
        }
    }

    // --- DEMO MODE (THE FAILSAFE) ---
    demoMode() {
        alert("DEMO MODE ACTIVATED: UI Unlocked for testing.");
        this.unlockUI();
        // Add fake data for visual check
        this.addUser("Target_X", "https://ui-avatars.com/api/?name=X&background=random");
        this.addChat("Target_X", "https://ui-avatars.com/api/?name=X", "System check... UI is functional.");
        this.spawnBotUI("Demo_Bot", 0);
        document.getElementById("b-0").classList.remove("off");
        document.getElementById("b-0").classList.add("on");
        document.querySelector("#b-0 span:last-child").innerText = "DEMO ONLINE";
    }

    unlockUI() {
        document.getElementById('p-login').classList.remove('active');
        document.getElementById('p-dash').classList.add('active');
        document.getElementById('navbar').style.display = 'flex';
        // Anti-Sleep
        if('wakeLock' in navigator) navigator.wakeLock.request('screen').catch(e=>{});
    }

    // --- REAL LOGIN ---
    login() {
        let raw = document.getElementById('creds').value;
        let room = document.getElementById('room').value;
        if(!raw.includes("#")) return alert("Use format: User#Pass");

        this.unlockUI();
        document.getElementById('bot-list').innerHTML = "";
        
        let list = raw.split("@");
        list.forEach((c, i) => {
            if(c.includes("#")) {
                let [u, p] = c.split("#");
                this.connectBot(u.trim(), p.trim(), room, i);
            }
        });

        // 3D Cube Rotation
        setInterval(() => this.rotateCube(), 2000);
    }

    spawnBotUI(name, id) {
        let div = document.createElement('div');
        div.className = 'bot-row off'; div.id = `b-${id}`;
        div.innerHTML = `<b>${name}</b> <span>CONNECTING...</span>`;
        document.getElementById('bot-list').appendChild(div);
    }

    connectBot(u, p, r, i) {
        this.spawnBotUI(u, i);
        let ws = new WebSocket(this.wsUrl);
        
        ws.onopen = () => {
            ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p}));
            // Heartbeat
            setInterval(() => { if(ws.readyState===1) ws.send(JSON.stringify({handler:"ping"})); }, 5000);
        };

        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler==="login_event" && d.type==="success") {
                ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            }
            if(d.handler==="room_event" && d.type==="room_joined") {
                let b = document.getElementById(`b-${i}`);
                b.className = "bot-row on";
                b.querySelector("span:last-child").innerText = "ONLINE";
            }
            this.handleData(d);
        };

        ws.onclose = () => {
            let b = document.getElementById(`b-${i}`);
            b.className = "bot-row off";
            b.querySelector("span:last-child").innerText = "RETRYING...";
            setTimeout(() => this.connectBot(u, p, r, i), 3000);
        };
    }

    handleData(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;

        // Fix Icon
        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        if(icon && !this.images.includes(icon)) this.images.push(icon);

        // 1. Radar Logic
        if(!this.users.has(u)) {
            this.addUser(u, icon);
        }

        // 2. Chat Logic
        if(d.type === "text" || d.type === "image") {
            let txt = d.type==="image" ? "[IMAGE]" : d.body;
            this.addChat(u, this.users.get(u).pic, txt);
            
            if(d.type==="image") this.addVault(u, d.url);
            if(d.body && d.body.match(/http.*(jpg|png)/i)) this.addVault(u, d.body.match(/http.*(jpg|png)/i)[0]);
        }
    }

    addUser(name, icon) {
        let usr = {
            name: name,
            pic: icon || `https://ui-avatars.com/api/?name=${name}`,
            x: Math.random() * 200 + 40,
            y: Math.random() * 200 + 40
        };
        this.users.set(name, usr);
        
        let box = document.getElementById('radar-scope');
        let ship = document.createElement('div');
        ship.className = 'ship';
        ship.style.left = usr.x + 'px';
        ship.style.top = usr.y + 'px';
        ship.innerHTML = `<img src="${usr.pic}" class="ship-img"><div class="ship-body"></div>`;
        box.appendChild(ship);
        document.getElementById('cnt').innerText = this.users.size;
    }

    addChat(u, pic, txt) {
        let box = document.getElementById('chat-feed');
        let html = `
            <div class="msg">
                <img src="${pic}">
                <div class="msg-c">
                    <div class="msg-n">${u} • ${new Date().toLocaleTimeString()}</div>
                    <div>${txt}</div>
                </div>
            </div>`;
        box.insertAdjacentHTML('afterbegin', html);
        this.logs.push(`${u}: ${txt}`);
    }

    addVault(u, url) {
        if(!url.startsWith("http")) url = "https://chatp.net"+url;
        let box = document.getElementById('vault-feed');
        box.insertAdjacentHTML('afterbegin', `<div class="v-card" onclick="window.open('${url}')"><img src="${url}"></div>`);
    }

    rotateCube() {
        if(this.images.length === 0) return;
        let faces = document.querySelectorAll('.face');
        let f = faces[Math.floor(Math.random()*faces.length)];
        let img = this.images[Math.floor(Math.random()*this.images.length)];
        f.style.backgroundImage = `url(${img})`;
        f.innerText = "";
    }

    export() {
        let blob = new Blob([this.logs.join("\n")], {type:"text/plain"});
        let a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = "LOGS.txt";
        a.click();
    }
}

const sys = new TitanCore();
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