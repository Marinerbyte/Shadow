from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS v8.0 ELITE</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        /* --- 1. CORE VISUALS --- */
        :root {
            --bg: #000000;
            --panel: #0a0a0a;
            --border: #1f1f1f;
            --neon-cyan: #00f3ff;
            --neon-green: #0aff0a;
            --neon-red: #ff003c;
            --glass: rgba(10, 20, 30, 0.85);
            --font-main: 'Rajdhani', sans-serif;
            --font-tech: 'Share Tech Mono', monospace;
        }

        * { box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; user-select: none; }
        
        body {
            background: var(--bg); color: #ccc;
            font-family: var(--font-main); margin: 0; padding: 0;
            height: 100vh; display: flex; flex-direction: column; overflow: hidden;
        }

        /* --- 2. 3D CUBE ANIMATION (Login Screen) --- */
        .cube-container {
            width: 80px; height: 80px; perspective: 400px; margin: 20px auto;
        }
        .cube {
            width: 100%; height: 100%; position: relative; transform-style: preserve-3d;
            animation: spin 6s infinite linear;
        }
        .face {
            position: absolute; width: 80px; height: 80px; border: 2px solid var(--neon-cyan);
            background: rgba(0, 243, 255, 0.1); display: flex; align-items: center; justify-content: center;
            font-size: 20px; color: var(--neon-cyan); box-shadow: 0 0 10px var(--neon-cyan);
        }
        .front  { transform: rotateY(0deg) translateZ(40px); }
        .back   { transform: rotateY(180deg) translateZ(40px); }
        .right  { transform: rotateY(90deg) translateZ(40px); }
        .left   { transform: rotateY(-90deg) translateZ(40px); }
        .top    { transform: rotateX(90deg) translateZ(40px); }
        .bottom { transform: rotateX(-90deg) translateZ(40px); }
        
        @keyframes spin { from{transform: rotateX(0) rotateY(0);} to{transform: rotateX(360deg) rotateY(360deg);} }

        /* --- 3. SHIP RADAR (Sonar) --- */
        .radar-scope {
            width: 260px; height: 260px; background: radial-gradient(circle, #002200 0%, #000 100%);
            border: 2px solid var(--neon-green); border-radius: 50%;
            position: relative; margin: 10px auto; overflow: hidden;
            box-shadow: 0 0 20px rgba(10, 255, 10, 0.2);
        }
        /* Grid Lines */
        .radar-scope::after {
            content: ''; position: absolute; inset: 0;
            background: 
                repeating-radial-gradient(transparent 0, transparent 39px, var(--neon-green) 40px),
                linear-gradient(90deg, transparent 129px, var(--neon-green) 130px, transparent 131px),
                linear-gradient(0deg, transparent 129px, var(--neon-green) 130px, transparent 131px);
            opacity: 0.3;
        }
        /* Scanner Line */
        .scanner {
            width: 50%; height: 50%; position: absolute; top: 0; left: 0;
            background: linear-gradient(45deg, rgba(0,255,10,0) 50%, rgba(0,255,10,0.5) 100%);
            transform-origin: 100% 100%;
            animation: scan 4s infinite linear; pointer-events: none; z-index: 5;
        }
        @keyframes scan { from{transform: rotate(0deg);} to{transform: rotate(360deg);} }
        
        /* User Blips */
        .blip {
            position: absolute; width: 6px; height: 6px; background: #fff;
            border-radius: 50%; box-shadow: 0 0 4px #fff;
            animation: blipAnim 2s infinite ease-in-out;
            z-index: 2; transition: all 0.5s;
        }
        .blip.target { background: var(--neon-red); box-shadow: 0 0 8px var(--neon-red); width: 8px; height: 8px; }
        @keyframes blipAnim { 0%, 100% {opacity:1; transform: scale(1);} 50% {opacity:0.4; transform: scale(0.8);} }
        
        /* Floating names on Radar */
        .blip-label {
            position: absolute; color: var(--neon-green); font-size: 8px;
            top: -12px; left: -10px; font-family: var(--font-tech);
            white-space: nowrap; text-shadow: 0 0 2px #000;
        }

        /* --- 4. LAYOUT & UI --- */
        .viewport { flex: 1; overflow-y: auto; padding: 10px; padding-bottom: 80px; }
        .page { display: none; }
        .page.active { display: block; animation: slideUp 0.3s ease; }
        @keyframes slideUp { from{opacity:0; transform:translateY(10px);} to{opacity:1; transform:translateY(0);} }

        .card {
            background: linear-gradient(180deg, #0f0f13, #050505);
            border: 1px solid #333; border-radius: 4px; padding: 12px; margin-bottom: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }
        .card-head {
            font-family: var(--font-main); font-size: 18px; color: var(--neon-cyan);
            border-bottom: 1px solid #222; padding-bottom: 5px; margin-bottom: 10px;
            display: flex; justify-content: space-between; text-transform: uppercase; letter-spacing: 1px;
        }

        input, textarea {
            width: 100%; background: #000; border: 1px solid #444; color: var(--neon-cyan);
            padding: 12px; margin-bottom: 10px; font-family: var(--font-tech); font-size: 14px;
        }
        .btn {
            width: 100%; padding: 14px; background: #111; border: 1px solid var(--neon-green);
            color: var(--neon-green); font-weight: bold; font-family: var(--font-main);
            font-size: 16px; cursor: pointer; text-transform: uppercase;
        }
        .btn:active { background: #0f2f0f; }

        /* --- 5. VAULT (IMAGES) --- */
        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        .v-item { position: relative; border: 1px solid #333; height: 120px; overflow: hidden; }
        .v-item img { width: 100%; height: 100%; object-fit: cover; }
        .v-meta {
            position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.8);
            color: #fff; font-size: 10px; padding: 4px; display: flex; justify-content: space-between;
        }

        /* --- 6. TARGET UI --- */
        .t-stat-row { display: flex; justify-content: space-between; border-bottom: 1px solid #222; padding: 8px 0; font-size: 14px; }
        .t-msg { background: #111; padding: 8px; margin-bottom: 5px; border-left: 2px solid var(--neon-red); font-size: 13px; }
        .export-btn { background: #330000; color: var(--neon-red); border-color: var(--neon-red); margin-top: 10px; }

        /* --- 7. NAV BAR --- */
        .nav {
            position: fixed; bottom: 0; width: 100%; height: 60px; background: #0a0a0a;
            border-top: 1px solid #333; display: flex; justify-content: space-around; align-items: center; z-index: 999;
        }
        .nav-item { text-align: center; color: #555; transition: 0.3s; }
        .nav-item div { font-size: 20px; margin-bottom: 2px; }
        .nav-item span { font-size: 10px; font-family: var(--font-tech); }
        .nav-item.active { color: var(--neon-cyan); text-shadow: 0 0 10px var(--neon-cyan); }
        .nav-item.active.alert { color: var(--neon-red); text-shadow: 0 0 10px var(--neon-red); }

        /* Feed Bubble */
        .msg-row { font-size: 13px; margin-bottom: 8px; border-bottom: 1px solid #111; padding-bottom: 4px; }
        .msg-u { color: var(--neon-cyan); font-weight: bold; font-family: var(--font-tech); }
        .msg-t { color: #555; font-size: 10px; float: right; }
    </style>
</head>
<body>

<!-- 1. DEPLOYMENT (LOGIN) -->
<div id="p-home" class="page active">
    <div style="text-align:center; padding-top:40px;">
        <div class="cube-container">
            <div class="cube">
                <div class="face front">TITAN</div>
                <div class="face back">OS</div>
                <div class="face right">v8</div>
                <div class="face left">SEC</div>
                <div class="face top"></div>
                <div class="face bottom"></div>
            </div>
        </div>
        <h2 style="color:var(--neon-cyan); font-family:var(--font-tech); letter-spacing:4px;">TITAN OS v8.0</h2>
    </div>

    <div class="viewport">
        <div class="card">
            <div class="card-head">SYSTEM ACCESS</div>
            <label style="font-size:12px; color:#666">TARGET ROOM NAME</label>
            <input type="text" id="room" value="ملتقى🥂العرب">
            <label style="font-size:12px; color:#666">AGENTS (User#Pass)</label>
            <textarea id="accs" rows="3" placeholder="Spy1#123@Spy2#123"></textarea>
            <button class="btn" onclick="engageSystem()">CONNECT SYSTEM</button>
        </div>
        <div class="card">
            <div class="card-head">UPLINK STATUS</div>
            <div id="status-log" style="font-family:var(--font-tech); font-size:12px; color:var(--neon-green)">STANDBY</div>
        </div>
    </div>
</div>

<!-- 2. SHIP RADAR -->
<div id="p-radar" class="page">
    <div class="viewport">
        <div class="radar-scope" id="sonarScope">
            <div class="scanner"></div>
            <!-- Blips injected here -->
        </div>
        
        <div class="card">
            <div class="card-head">DETECTED SIGNALS <span id="radar-count" style="color:#fff">0</span></div>
            <div id="radar-list" style="max-height:300px; overflow-y:auto;"></div>
        </div>
    </div>
</div>

<!-- 3. TARGET OPS -->
<div id="p-target" class="page">
    <div class="viewport">
        <div class="card" style="border-color:var(--neon-red)">
            <div class="card-head" style="color:var(--neon-red)">TARGET DOSSIER</div>
            <select id="tgt-select" onchange="loadTarget(this.value)" style="width:100%; background:#111; color:#fff; padding:10px; border:1px solid #444; margin-bottom:10px;">
                <option value="">-- SELECT TARGET --</option>
            </select>
            
            <div id="tgt-data" style="display:none">
                <div class="t-stat-row"><span>STATUS</span><span style="color:var(--neon-green)">ONLINE</span></div>
                <div class="t-stat-row"><span>LAST SEEN</span><span id="t-seen">--</span></div>
                <div class="t-stat-row"><span>MESSAGES</span><span id="t-cnt">0</span></div>
                
                <div class="card-head" style="margin-top:20px; font-size:14px;">INTERCEPTED LOGS</div>
                <div id="t-logs" style="max-height:200px; overflow-y:auto; background:#000; padding:5px; border:1px solid #333;"></div>
                
                <button class="btn export-btn" onclick="exportChat()">DOWNLOAD LOGS (.TXT)</button>
            </div>
        </div>
    </div>
</div>

<!-- 4. GLOBAL FEED -->
<div id="p-feed" class="page">
    <div class="viewport">
        <div class="card">
            <div class="card-head">GLOBAL INTERCEPT</div>
            <div id="feed-box" style="font-family:'Roboto', sans-serif;"></div>
        </div>
    </div>
</div>

<!-- 5. SECURE VAULT -->
<div id="p-vault" class="page">
    <div class="viewport">
        <div class="card">
            <div class="card-head">MEDIA VAULT</div>
            <div id="vault-grid" class="vault-grid"></div>
        </div>
    </div>
</div>

<!-- NAVIGATION -->
<div class="nav">
    <div class="nav-item" onclick="nav('p-home', this)"><div>⚙️</div><span>SYS</span></div>
    <div class="nav-item active" onclick="nav('p-radar', this)"><div>📡</div><span>RADAR</span></div>
    <div class="nav-item" onclick="nav('p-target', this)"><div>🎯</div><span>TARGET</span></div>
    <div class="nav-item" onclick="nav('p-feed', this)"><div>💬</div><span>FEED</span></div>
    <div class="nav-item" onclick="nav('p-vault', this)"><div>📂</div><span>VAULT</span></div>
</div>

<script>
    // --- TITAN CORE V8.0 ---
    const WS_URL = "wss://chatp.net:5333/server";
    let bots = [];
    let users = new Map(); // Stores {name, last, icon, msgs:[]}
    let vault = [];
    let currentTgt = null;
    let wakeLock = null;

    // --- UTILITIES ---
    const getID = () => Math.random().toString(36).substr(2, 8);
    const getTime = () => new Date().toLocaleTimeString('en-US', {hour12:false, hour:'2-digit', minute:'2-digit'});
    
    // --- ANTI DISCONNECT & WAKELOCK ---
    async function activateGodMode() {
        try { if('wakeLock' in navigator) wakeLock = await navigator.wakeLock.request('screen'); } 
        catch(e) { console.log("WakeLock Err", e); }
    }
    // Reconnect on tab focus
    document.addEventListener("visibilitychange", () => {
        if(document.visibilityState === 'visible') {
            bots.forEach(b => { if(b.ws.readyState !== 1) b.reconnect(); });
            activateGodMode();
        }
    });

    // --- NAVIGATION ---
    function nav(id, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        el.classList.add('active');
    }

    // --- SYSTEM START ---
    function engageSystem() {
        activateGodMode();
        let raw = document.getElementById("accs").value;
        let room = document.getElementById("room").value;
        if(!raw.includes("#")) { alert("Enter Credentials!"); return; }

        document.getElementById("status-log").innerText = "INITIALIZING BOTNET...";
        
        // Kill old
        bots.forEach(b => b.ws.close());
        bots = [];

        let creds = raw.split("@").filter(s => s.includes("#"));
        creds.forEach((c, i) => {
            let [u, p] = c.split("#");
            spawnBot(u.trim(), p.trim(), room, i);
        });
        
        setTimeout(() => nav('p-radar', document.querySelectorAll('.nav-item')[1]), 1000);
    }

    function spawnBot(user, pass, room, idx) {
        let bot = {
            ws: null,
            reconnect: function() {
                this.ws = new WebSocket(WS_URL);
                this.ws.onopen = () => {
                    this.ws.send(JSON.stringify({handler:"login", id:getID(), username:user, password:pass}));
                };
                this.ws.onmessage = (e) => handlePacket(JSON.parse(e.data), this.ws, room);
                this.ws.onclose = () => {
                    document.getElementById("status-log").innerText = `LOST ${user}. RETRYING...`;
                    setTimeout(() => this.reconnect(), 2000); // Auto Retry 2s
                };
            }
        };
        bot.reconnect();
        bots.push(bot);
    }

    function handlePacket(d, ws, room) {
        // Auth Logic
        if(d.handler === "login_event" && d.type === "success") {
            ws.send(JSON.stringify({handler:"room_join", id:getID(), name:room}));
        }
        if(d.handler === "room_event" && d.type === "room_joined") {
            document.getElementById("status-log").innerText = "SYSTEM ONLINE - INTERCEPTING";
            document.getElementById("status-log").style.color = "var(--neon-cyan)";
        }

        // --- CORE DATA PROCESSING ---
        let u = d.username || d.from;
        if(!u) return;

        // 1. UPDATE USER DATABASE (For Radar & Target)
        if(!users.has(u)) {
            // New User: Assign random radar coordinates
            let angle = Math.random() * 360;
            let dist = Math.random() * 40 + 10; // 10% to 50% from center
            users.set(u, {
                name: u, icon: d.icon || d.avatar_url, 
                last: Date.now(), msgs: [], 
                radX: dist * Math.cos(angle * Math.PI/180),
                radY: dist * Math.sin(angle * Math.PI/180)
            });
            updateRadar(u);
            updateTargetList(u);
        } else {
            // Update Activity
            let usr = users.get(u);
            usr.last = Date.now();
            if(d.icon) usr.icon = d.icon;
            users.set(u, usr);
        }

        // 2. PROCESS MESSAGE
        if(d.type === "text" || d.type === "image") {
            let msgObj = { time: getTime(), txt: d.body, type: d.type };
            users.get(u).msgs.push(msgObj);
            
            // Global Feed
            addToFeed(u, d.body, d.type);
            
            // Vault (Image Sniffer)
            if(d.type === "image" || (d.body && d.body.match(/http.*(jpg|png|jpeg)/i))) {
                let url = d.type==="image" ? "https://chatp.net"+d.url : d.body.match(/http.*(jpg|png|jpeg)/i)[0];
                addToVault(u, url);
            }

            // If watching this target, update UI
            if(currentTgt === u) loadTarget(u);
        }
    }

    // --- UI MODULES ---

    // 1. RADAR (SHIP BLIPS)
    function updateRadar(name) {
        let usr = users.get(name);
        let scope = document.getElementById("sonarScope");
        let list = document.getElementById("radar-list");
        
        // Avoid duplicate blips
        let existBlip = document.getElementById(`blip-${name}`);
        if(!existBlip) {
            // Create Blip on Sonar
            let blip = document.createElement("div");
            blip.id = `blip-${name}`;
            blip.className = "blip";
            // Position from center (50% 50%)
            blip.style.top = `calc(50% + ${usr.radY}%)`;
            blip.style.left = `calc(50% + ${usr.radX}%)`;
            blip.innerHTML = `<span class="blip-label">${name}</span>`;
            scope.appendChild(blip);
            
            // Add to List
            list.insertAdjacentHTML('afterbegin', `
                <div style="display:flex; justify-content:space-between; padding:8px; border-bottom:1px solid #222; font-size:12px;">
                    <span style="color:#fff">${name}</span>
                    <span style="color:var(--neon-green)">DETECTED</span>
                </div>
            `);
            document.getElementById("radar-count").innerText = users.size;
        }
        
        // Jitter Effect (Hilna)
        existBlip = document.getElementById(`blip-${name}`);
        if(existBlip) {
            existBlip.style.transform = `translate(${Math.random()*4-2}px, ${Math.random()*4-2}px)`;
        }
    }

    // 2. TARGET OPS
    function updateTargetList(name) {
        let sel = document.getElementById("tgt-select");
        let opt = document.createElement("option");
        opt.value = name; opt.innerText = name;
        sel.appendChild(opt);
    }

    function loadTarget(name) {
        if(!name) { document.getElementById("tgt-data").style.display="none"; currentTgt=null; return; }
        currentTgt = name;
        document.getElementById("tgt-data").style.display="block";
        let u = users.get(name);
        
        document.getElementById("t-seen").innerText = new Date(u.last).toLocaleTimeString();
        document.getElementById("t-cnt").innerText = u.msgs.length;
        
        // Logs
        let box = document.getElementById("t-logs");
        box.innerHTML = "";
        u.msgs.slice().reverse().forEach(m => {
            box.insertAdjacentHTML('beforeend', `
                <div class="t-msg">
                    <div style="color:#666; font-size:10px;">${m.time}</div>
                    <div style="color:#ddd;">${m.txt}</div>
                </div>
            `);
        });
        
        // Mark as Target on Radar
        let blip = document.getElementById(`blip-${name}`);
        if(blip) blip.classList.add("target");
    }

    function exportChat() {
        if(!currentTgt) return;
        let u = users.get(currentTgt);
        let txt = `TARGET: ${u.name}\nEXPORT TIME: ${new Date().toLocaleString()}\n\n`;
        u.msgs.forEach(m => { txt += `[${m.time}] ${m.txt}\n`; });
        
        let blob = new Blob([txt], {type:"text/plain"});
        let a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = `${u.name}_LOGS.txt`;
        a.click();
    }

    // 3. GLOBAL FEED
    function addToFeed(u, txt, type) {
        let box = document.getElementById("feed-box");
        let content = type==="image" ? "[SENT PHOTO]" : txt.replace(/</g,'&lt;');
        let html = `
            <div class="msg-row">
                <span class="msg-u">${u}</span> <span class="msg-t">${getTime()}</span>
                <div style="color:#bbb; margin-top:2px;">${content}</div>
            </div>
        `;
        box.insertAdjacentHTML('afterbegin', html);
        if(box.childElementCount > 60) box.lastElementChild.remove();
    }

    // 4. VAULT
    function addToVault(u, url) {
        let grid = document.getElementById("vault-grid");
        let html = `
            <div class="v-item">
                <img src="${url}" onclick="window.open(this.src)">
                <div class="v-meta">
                    <span>${u}</span>
                    <span>${getTime()}</span>
                </div>
            </div>
        `;
        grid.insertAdjacentHTML('afterbegin', html);
    }

</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)