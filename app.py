from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN OS: OMEGA GOD</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        /* =============================================================================
           1. CORE KERNEL STYLES (THEME CONFIGURATION)
           ============================================================================= */
        :root {
            --hex-bg: #020202;
            --hex-panel: #0a0b10;
            --hex-cyan: #00f3ff;
            --hex-green: #0aff0a;
            --hex-red: #ff003c;
            --hex-gold: #ffd700;
            --hex-glass: rgba(10, 20, 30, 0.95);
            --font-ui: 'Orbitron', sans-serif;
            --font-code: 'Share Tech Mono', monospace;
            --scanline-color: rgba(0, 255, 255, 0.02);
        }

        * { box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; outline: none; }

        body {
            background-color: var(--hex-bg);
            color: #fff;
            font-family: var(--font-ui);
            margin: 0; padding: 0;
            height: 100vh; overflow: hidden;
            display: flex; flex-direction: column;
        }

        /* CRT SCANLINE OVERLAY */
        body::after {
            content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 9999; background-size: 100% 2px, 3px 100%; pointer-events: none;
        }

        /* DYNAMIC STARDUST BACKGROUND */
        #bg-canvas {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -2; opacity: 0.5;
        }

        /* =============================================================================
           2. LAYOUT & NAVIGATION SYSTEMS
           ============================================================================= */
        
        /* HEADER (Appears after login) */
        .sys-header {
            height: 60px; background: rgba(5,5,5,0.95); border-bottom: 1px solid #333;
            display: none; justify-content: space-between; align-items: center; padding: 0 15px;
            z-index: 500;
        }
        .sys-logo { font-size: 18px; color: var(--hex-cyan); letter-spacing: 2px; }
        .header-cube-box { width: 30px; height: 30px; perspective: 200px; }
        
        /* MAIN VIEWPORT */
        .viewport {
            flex: 1; overflow-y: auto; padding: 15px; padding-bottom: 100px;
            position: relative;
        }
        
        .page { display: none; animation: slideUp 0.4s ease-out; }
        .page.active { display: block; }
        @keyframes slideUp { from{opacity:0; transform:translateY(20px);} to{opacity:1; transform:translateY(0);} }

        /* CARDS & PANELS */
        .titan-card {
            background: var(--hex-panel); border: 1px solid #222;
            border-left: 3px solid var(--hex-cyan); border-radius: 6px;
            padding: 15px; margin-bottom: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative; overflow: hidden;
        }
        .card-head {
            font-size: 14px; color: var(--hex-cyan); border-bottom: 1px solid #333;
            padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between;
        }

        /* =============================================================================
           3. ADVANCED 3D CUBE (DUAL MODE)
           ============================================================================= */
        /* Login Mode (Big) */
        .cube-big-box { width: 140px; height: 140px; margin: 30px auto; perspective: 800px; }
        /* Header Mode (Small) */
        .cube-small-box { width: 100%; height: 100%; transform-style: preserve-3d; animation: spin 5s infinite linear; }
        
        .cube-core {
            width: 100%; height: 100%; position: relative; transform-style: preserve-3d;
            animation: spin 12s infinite linear;
        }
        .c-face {
            position: absolute; width: 100%; height: 100%;
            border: 2px solid var(--hex-cyan); background: rgba(0, 243, 255, 0.1);
            display: flex; align-items: center; justify-content: center;
            font-size: 14px; color: #fff; background-size: cover; background-position: center;
            box-shadow: inset 0 0 20px rgba(0, 243, 255, 0.2);
        }
        .cf1 { transform: translateZ(70px); }
        .cf2 { transform: rotateY(180deg) translateZ(70px); }
        .cf3 { transform: rotateY(90deg) translateZ(70px); }
        .cf4 { transform: rotateY(-90deg) translateZ(70px); }
        .cf5 { transform: rotateX(90deg) translateZ(70px); }
        .cf6 { transform: rotateX(-90deg) translateZ(70px); }
        
        /* Small cube face adjustments */
        .header-cube-box .cf1 { transform: translateZ(15px); }
        .header-cube-box .cf2 { transform: rotateY(180deg) translateZ(15px); }
        .header-cube-box .cf3 { transform: rotateY(90deg) translateZ(15px); }
        .header-cube-box .cf4 { transform: rotateY(-90deg) translateZ(15px); }
        .header-cube-box .cf5 { transform: rotateX(90deg) translateZ(15px); }
        .header-cube-box .cf6 { transform: rotateX(-90deg) translateZ(15px); }

        @keyframes spin { 100% { transform: rotateX(360deg) rotateY(360deg); } }

        /* =============================================================================
           4. BOT STATUS BAR (COMPACT DOCK)
           ============================================================================= */
        .bot-bar {
            position: fixed; bottom: 80px; left: 0; width: 100%; height: 40px;
            background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
            display: none; align-items: center; padding: 0 10px; gap: 10px;
            overflow-x: auto; z-index: 200;
        }
        .bot-pill {
            background: #111; border: 1px solid #333; padding: 4px 10px;
            border-radius: 20px; font-size: 10px; color: #aaa; font-family: var(--font-code);
            display: flex; align-items: center; gap: 6px; white-space: nowrap;
            box-shadow: 0 2px 5px #000;
        }
        .bot-pill.online { border-color: var(--hex-green); color: #fff; background: rgba(0, 255, 10, 0.1); }
        .status-dot { width: 6px; height: 6px; border-radius: 50%; background: #444; }
        .online .status-dot { background: var(--hex-green); box-shadow: 0 0 5px var(--hex-green); }

        /* =============================================================================
           5. NAVIGATION DOCK (BOTTOM)
           ============================================================================= */
        .nav-dock {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 80px;
            background: #050505; border-top: 1px solid #333;
            display: none; justify-content: space-around; align-items: center;
            z-index: 300; box-shadow: 0 -5px 20px rgba(0,0,0,0.8);
        }
        .nav-item {
            text-align: center; color: #555; transition: 0.3s; cursor: pointer;
            width: 60px;
        }
        .nav-icon { width: 24px; height: 24px; margin: 0 auto 5px; fill: currentColor; }
        .nav-lbl { font-size: 10px; font-weight: bold; letter-spacing: 1px; }
        .nav-item.active { color: var(--hex-cyan); transform: translateY(-5px); }
        .nav-item.active .nav-icon { filter: drop-shadow(0 0 5px var(--hex-cyan)); }

        /* =============================================================================
           6. PHYSICS RADAR (REAL MOVEMENT)
           ============================================================================= */
        .radar-frame {
            width: 280px; height: 280px; margin: 0 auto; border-radius: 50%;
            border: 2px solid #333; background: radial-gradient(circle, #001 0%, #000 90%);
            position: relative; overflow: hidden; box-shadow: 0 0 30px rgba(0,243,255,0.15);
        }
        .radar-sweep {
            position: absolute; inset: 0; border-radius: 50%;
            background: conic-gradient(transparent 270deg, rgba(0,255,10,0.3));
            animation: scan 3s infinite linear; pointer-events: none;
        }
        @keyframes scan { to { transform: rotate(360deg); } }

        .radar-blip {
            position: absolute; width: 44px; height: 44px;
            transform: translate(-50%, -50%); cursor: grab; z-index: 10;
            display: flex; flex-direction: column; align-items: center;
        }
        .blip-img {
            width: 30px; height: 30px; border-radius: 50%; border: 1px solid #fff;
            box-shadow: 0 0 8px var(--hex-cyan); pointer-events: none;
        }
        .blip-name {
            font-size: 8px; color: var(--hex-green); background: rgba(0,0,0,0.8);
            padding: 2px 4px; border-radius: 4px; margin-top: 2px;
            white-space: nowrap; pointer-events: none;
        }

        /* =============================================================================
           7. TARGET SYSTEM (GRID & DOSSIER)
           ============================================================================= */
        .user-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .user-cell {
            background: #111; border: 1px solid #333; border-radius: 6px; padding: 10px;
            text-align: center; cursor: pointer; transition: 0.2s;
        }
        .user-cell:hover { border-color: var(--hex-red); background: rgba(255,0,60,0.1); }
        .u-pic { width: 40px; height: 40px; border-radius: 50%; margin-bottom: 5px; border: 1px solid #555; }
        .u-name { font-size: 10px; color: #ccc; overflow: hidden; text-overflow: ellipsis; }

        /* DOSSIER MODAL (Full Screen Overlay within Tab) */
        .dossier-view {
            display: none; background: #080808; border: 1px solid var(--hex-red);
            padding: 15px; border-radius: 8px; animation: fadeIn 0.3s;
        }
        .dos-header { display: flex; gap: 15px; align-items: center; border-bottom: 1px solid #333; padding-bottom: 15px; margin-bottom: 15px; }
        .dos-pic { width: 70px; height: 70px; border-radius: 50%; border: 2px solid var(--hex-red); box-shadow: 0 0 15px var(--hex-red); }
        .dos-info h2 { margin: 0; color: var(--hex-red); font-size: 18px; }
        .dos-stat { font-size: 10px; color: #888; font-family: var(--font-code); margin-top: 5px; }
        
        .dos-logs { height: 150px; overflow-y: auto; background: #000; border: 1px solid #333; padding: 10px; margin-bottom: 10px; font-family: var(--font-code); font-size: 11px; color: #bbb; }
        .dos-log-row { margin-bottom: 5px; border-bottom: 1px solid #111; padding-bottom: 2px; }
        
        /* =============================================================================
           8. CHAT & VAULT
           ============================================================================= */
        .chat-feed { height: 400px; overflow-y: auto; }
        .msg-entry { display: flex; gap: 12px; margin-bottom: 15px; }
        .msg-pic { width: 40px; height: 40px; border-radius: 6px; border: 1px solid #444; }
        .msg-bub { flex: 1; background: #111; padding: 10px; border-radius: 0 12px 12px 12px; border: 1px solid #222; }
        .msg-meta { display: flex; justify-content: space-between; font-size: 10px; color: #666; margin-bottom: 4px; }
        .msg-usr { color: var(--hex-cyan); font-weight: bold; }
        .msg-body { font-size: 13px; color: #eee; line-height: 1.4; word-break: break-all; }

        .vault-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .v-item { background: #000; border: 1px solid #333; height: 120px; position: relative; cursor: pointer; }
        .v-item img { width: 100%; height: 100%; object-fit: cover; }
        .v-lbl { position: absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:#fff; font-size:9px; padding:3px; text-align: center;}

        /* UTILS */
        .input-cyber { width: 100%; background: #000; border: 1px solid #444; color: var(--hex-cyan); padding: 12px; font-family: var(--font-code); margin-bottom: 10px; }
        .btn-cyber { width: 100%; padding: 15px; background: rgba(0,243,255,0.1); border: 1px solid var(--hex-cyan); color: var(--hex-cyan); font-weight: bold; cursor: pointer; text-transform: uppercase; font-family: var(--font-ui); }
        
        #boot-screen {
            position: fixed; top:0; left:0; width:100%; height:100%; background:#000;
            z-index: 9999; display: flex; flex-direction: column; align-items: center; justify-content: center;
            font-family: var(--font-code); color: var(--hex-green);
        }
    </style>
</head>
<body>

{% raw %}
    <!-- DYNAMIC BACKGROUND -->
    <canvas id="bg-canvas"></canvas>

    <!-- BOOT SEQUENCE -->
    <div id="boot-screen">
        <div style="font-size:24px; margin-bottom:10px;">TITAN OS <span style="color:#fff">v18</span></div>
        <div id="boot-log">INITIALIZING KERNEL...</div>
        <div style="width:200px; height:4px; background:#333; margin-top:20px;">
            <div id="boot-prog" style="width:0%; height:100%; background:var(--hex-green); transition: width 3s;"></div>
        </div>
        <button onclick="document.getElementById('boot-screen').style.display='none'" style="margin-top:20px; background:none; border:1px solid #444; color:#666;">[ SKIP BOOT ]</button>
    </div>

    <!-- HEADER (Hidden until Login) -->
    <div class="sys-header" id="header">
        <div class="sys-logo">TITAN</div>
        <div class="header-cube-box">
            <div class="cube-core" id="headerCube">
                <div class="c-face cf1"></div><div class="c-face cf2"></div>
                <div class="c-face cf3"></div><div class="c-face cf4"></div>
                <div class="c-face cf5"></div><div class="c-face cf6"></div>
            </div>
        </div>
    </div>

    <div class="viewport">
        
        <!-- 1. LOGIN PAGE -->
        <div id="p-login" class="page active">
            <div style="text-align:center;">
                <div class="cube-big-box">
                    <div class="cube-core" id="loginCube">
                        <div class="c-face cf1">SYS</div><div class="c-face cf2">NET</div>
                        <div class="c-face cf3">SEC</div><div class="c-face cf4">DATA</div>
                        <div class="c-face cf5"></div><div class="c-face cf6"></div>
                    </div>
                </div>
                <h1 style="color:var(--hex-cyan); letter-spacing:5px;">TITAN OS</h1>
            </div>

            <div class="titan-card">
                <div class="card-head">SECURE ACCESS</div>
                <label style="font-size:10px; color:#888;">TARGET ROOM</label>
                <input type="text" id="room" class="input-cyber" value="ملتقى🥂العرب">
                <label style="font-size:10px; color:#888;">AGENTS (User#Pass)</label>
                <textarea id="creds" class="input-cyber" rows="3" placeholder="Spy1#pass@Spy2#pass"></textarea>
                <button class="btn-cyber" onclick="sys.login()">ESTABLISH UPLINK</button>
                <button class="btn-cyber" style="margin-top:10px; border-color:var(--hex-green); color:var(--hex-green)" onclick="sys.demo()">DEMO MODE</button>
            </div>
        </div>

        <!-- 2. RADAR PAGE -->
        <div id="p-radar" class="page">
            <div class="titan-card">
                <div class="card-head">PHYSICS RADAR <span id="r-cnt" style="color:#fff">0</span></div>
                <div class="radar-frame" id="radar-ui">
                    <div class="radar-sweep"></div>
                    <!-- Blips go here -->
                </div>
                <div style="text-align:center; font-size:10px; color:#666; margin-top:10px;">
                    OBJECTS ARE MOVING • DRAG TO INTERACT
                </div>
            </div>
        </div>

        <!-- 3. TARGET SYSTEM (GRID + DOSSIER) -->
        <div id="p-target" class="page">
            <!-- Grid View -->
            <div id="target-grid-view">
                <div class="titan-card">
                    <div class="card-head">DETECTED ENTITIES</div>
                    <div class="user-grid" id="user-list">
                        <div style="grid-column:span 3; text-align:center; padding:20px; color:#555;">SCANNING NETWORK...</div>
                    </div>
                </div>
            </div>

            <!-- Dossier View (Hidden) -->
            <div id="target-dossier-view" class="dossier-view">
                <button onclick="sys.closeDossier()" style="background:none; border:1px solid #444; color:#fff; padding:5px 10px; margin-bottom:10px;">&laquo; BACK TO LIST</button>
                
                <div class="dos-header">
                    <img id="dos-pic" src="" class="dos-pic">
                    <div class="dos-info">
                        <h2 id="dos-name">UNKNOWN</h2>
                        <div class="dos-stat">STATUS: <span style="color:var(--hex-green)">ACTIVE</span></div>
                        <div class="dos-stat">MESSAGES: <span id="dos-msg-cnt" style="color:#fff">0</span></div>
                        <button onclick="sys.exportTarget()" style="margin-top:5px; background:var(--hex-red); color:#fff; border:none; padding:5px; border-radius:3px; cursor:pointer;">DOWNLOAD DOSSIER</button>
                    </div>
                </div>

                <div style="font-size:12px; color:#aaa; margin-bottom:5px;">COMMUNICATION LOGS</div>
                <div class="dos-logs" id="dos-logs"></div>

                <div style="font-size:12px; color:#aaa; margin:10px 0 5px 0;">CAPTURED MEDIA</div>
                <div class="vault-grid" id="dos-media"></div>
            </div>
        </div>

        <!-- 4. CHAT FEED -->
        <div id="p-chat" class="page">
            <div class="titan-card">
                <div class="card-head">
                    GLOBAL FEED
                    <button onclick="sys.exportAll()" style="background:none; border:1px solid #444; color:#fff; font-size:10px; cursor:pointer;">SAVE ALL</button>
                </div>
                <div class="chat-feed" id="chat-feed"></div>
            </div>
        </div>

        <!-- 5. VAULT -->
        <div id="p-vault" class="page">
            <div class="titan-card">
                <div class="card-head">EVIDENCE VAULT</div>
                <div class="vault-grid" id="vault-feed"></div>
            </div>
        </div>

    </div>

    <!-- BOT STATUS BAR -->
    <div class="bot-bar" id="bot-dock" style="display:none;"></div>

    <!-- NAVIGATION DOCK -->
    <div class="nav-dock" id="navbar" style="display:none;">
        <div class="nav-item active" onclick="sys.nav('p-radar', this)">
            <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5.5-2.5l7.51-3.49L17.5 6.5 9.99 9.99 6.5 17.5zm5.5-6.6c.61 0 1.1.49 1.1 1.1s-.49 1.1-1.1 1.1-1.1-.49-1.1-1.1.49-1.1 1.1-1.1z"/></svg>
            <div class="nav-lbl">RADAR</div>
        </div>
        <div class="nav-item" onclick="sys.nav('p-target', this)">
            <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <div class="nav-lbl">TARGET</div>
        </div>
        <div class="nav-item" onclick="sys.nav('p-chat', this)">
            <svg class="nav-icon" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>
            <div class="nav-lbl">CHAT</div>
        </div>
        <div class="nav-item" onclick="sys.nav('p-vault', this)">
            <svg class="nav-icon" viewBox="0 0 24 24"><path d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-5 3c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm4 8h-8v-1c0-1.33 2.67-2 4-2s4 .67 4 2v1z"/></svg>
            <div class="nav-lbl">VAULT</div>
        </div>
    </div>

<script>
class TitanCore {
    constructor() {
        this.wsUrl = "wss://chatp.net:5333/server";
        this.users = new Map(); // Key: username, Val: {pic, logs[], media[], x, y, vx, vy}
        this.allLogs = [];
        this.avatars = [];
        this.activeTarget = null;
        this.audio = new (window.AudioContext || window.webkitAudioContext)();
    }

    init() {
        this.animateBg();
        setTimeout(() => { document.getElementById('boot-prog').style.width="100%"; }, 100);
        setTimeout(() => { document.getElementById('boot-screen').style.display="none"; this.beep(800); }, 3000);
    }

    nav(pid, el) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        document.getElementById(pid).classList.add('active');
        el.classList.add('active');
        this.beep(1200);
    }

    // --- LOGIN ---
    login() {
        let r = document.getElementById('room').value;
        let c = document.getElementById('creds').value;
        if(!c.includes("#")) return alert("Format: User#Pass");

        document.getElementById('p-login').classList.remove('active');
        document.getElementById('p-radar').classList.add('active');
        document.getElementById('header').style.display = 'flex';
        document.getElementById('bot-dock').style.display = 'flex';
        document.getElementById('navbar').style.display = 'flex';

        let list = c.split("@");
        document.getElementById('bot-dock').innerHTML = "";
        
        list.forEach((str, i) => {
            if(str.includes("#")) {
                let [u, p] = str.split("#");
                this.connectBot(u.trim(), p.trim(), r, i);
            }
        });

        // Start Physics
        this.radarLoop();
        setInterval(() => this.updateCubes(), 2000);
        if('wakeLock' in navigator) navigator.wakeLock.request('screen').catch(e=>{});
    }

    demo() {
        document.getElementById('creds').value = "DemoBot#123";
        this.login();
        setTimeout(() => {
            this.handleData({username: "Target_X", icon: "", type: "text", body: "System check operational."});
        }, 2000);
    }

    // --- BOTNET ---
    connectBot(u, p, r, i) {
        // Create Pill
        let pill = document.createElement('div');
        pill.className = 'bot-pill'; pill.id = `pill-${i}`;
        pill.innerHTML = `<div class="status-dot"></div> ${u}`;
        document.getElementById('bot-dock').appendChild(pill);

        let ws = new WebSocket(this.wsUrl);
        ws.onopen = () => { ws.send(JSON.stringify({handler:"login", id:Math.random(), username:u, password:p})); setInterval(()=>ws.send(JSON.stringify({handler:"ping"})),5000); };
        ws.onmessage = (e) => {
            let d = JSON.parse(e.data);
            if(d.handler=="login_event" && d.type=="success") ws.send(JSON.stringify({handler:"room_join", id:Math.random(), name:r}));
            if(d.handler=="room_event" && d.type=="room_joined") document.getElementById(`pill-${i}`).classList.add('online');
            this.handleData(d);
        };
        ws.onclose = () => {
            document.getElementById(`pill-${i}`).classList.remove('online');
            setTimeout(()=>this.connectBot(u,p,r,i), 3000);
        }
    }

    // --- DATA HANDLING ---
    handleData(d) {
        let u = d.username || d.from;
        let icon = d.icon || d.avatar_url;
        if(!u) return;

        if(icon && !icon.startsWith("http")) icon = "https://chatp.net" + icon;
        if(icon && !this.avatars.includes(icon)) this.avatars.push(icon);

        // 1. User Management
        if(!this.users.has(u)) {
            let usr = {
                name: u,
                pic: icon || `https://ui-avatars.com/api/?name=${u}`,
                logs: [], media: [],
                x: 140, y: 140, vx: (Math.random()-0.5)*2, vy: (Math.random()-0.5)*2
            };
            this.users.set(u, usr);
            this.spawnBlip(usr);
            this.refreshGrid();
        }
        let userObj = this.users.get(u);

        // 2. Chat Processing
        if(d.type === "text" || d.type === "image") {
            let body = d.type === "image" ? "[IMAGE]" : d.body;
            let time = new Date().toLocaleTimeString();
            
            userObj.logs.push({time, body});
            this.allLogs.push(`${u}: ${body}`);
            
            this.addChatUI(u, userObj.pic, body, time);
            
            if(d.type === "image") {
                userObj.media.push(d.url);
                this.addVaultUI(u, d.url);
            }

            // Live Update Dossier if open
            if(this.activeTarget === u) {
                this.addLogToDossier(time, body);
                if(d.type==="image") this.addMediaToDossier(d.url);
                this.beep(600);
            }
        }
    }

    // --- RADAR PHYSICS ---
    spawnBlip(usr) {
        let box = document.getElementById('radar-ui');
        let el = document.createElement('div');
        el.className = 'radar-blip';
        el.innerHTML = `<img src="${usr.pic}" class="blip-img"><div class="blip-name">${usr.name}</div>`;
        
        // Touch Drag Logic (Basic)
        el.onclick = () => { usr.vx = (Math.random()-0.5)*5; usr.vy = (Math.random()-0.5)*5; };
        
        box.appendChild(el);
        usr.el = el;
        document.getElementById('r-cnt').innerText = this.users.size;
    }

    radarLoop() {
        this.users.forEach(u => {
            if(!u.el) return;
            u.x += u.vx; u.y += u.vy;
            
            // Wall Bounce (Radius 140)
            let dx = u.x - 140, dy = u.y - 140;
            if(Math.sqrt(dx*dx + dy*dy) > 120) {
                u.vx *= -1; u.vy *= -1;
            }
            u.el.style.left = u.x + "px";
            u.el.style.top = u.y + "px";
        });
        requestAnimationFrame(() => this.radarLoop());
    }

    // --- TARGET SYSTEM ---
    refreshGrid() {
        let grid = document.getElementById('user-list');
        grid.innerHTML = "";
        this.users.forEach(u => {
            let cell = document.createElement('div');
            cell.className = 'user-cell';
            cell.innerHTML = `<img src="${u.pic}" class="u-pic"><div class="u-name">${u.name}</div>`;
            cell.onclick = () => this.openDossier(u.name);
            grid.appendChild(cell);
        });
    }

    openDossier(name) {
        this.activeTarget = name;
        let u = this.users.get(name);
        document.getElementById('target-grid-view').style.display = 'none';
        document.getElementById('target-dossier-view').style.display = 'block';
        
        document.getElementById('dos-name').innerText = u.name;
        document.getElementById('dos-pic').src = u.pic;
        document.getElementById('dos-msg-cnt').innerText = u.logs.length;
        
        // Populate Logs
        let lb = document.getElementById('dos-logs'); lb.innerHTML = "";
        u.logs.forEach(l => { lb.innerHTML += `<div class="dos-log-row">[${l.time}] ${l.body}</div>`; });
        
        // Populate Media
        let mb = document.getElementById('dos-media'); mb.innerHTML = "";
        u.media.forEach(m => {
             if(!m.startsWith("http")) m = "https://chatp.net"+m;
             mb.innerHTML += `<div class="v-item" onclick="window.open('${m}')"><img src="${m}"></div>`;
        });
    }

    closeDossier() {
        this.activeTarget = null;
        document.getElementById('target-dossier-view').style.display = 'none';
        document.getElementById('target-grid-view').style.display = 'block';
    }

    addLogToDossier(time, body) {
        let d = document.createElement('div'); d.className="dos-log-row";
        d.innerText = `[${time}] ${body}`;
        document.getElementById('dos-logs').prepend(d);
    }
    
    addMediaToDossier(url) {
        if(!url.startsWith("http")) url = "https://chatp.net"+url;
        let d = document.createElement('div'); d.className="v-item";
        d.innerHTML = `<img src="${url}">`; d.onclick = ()=>window.open(url);
        document.getElementById('dos-media').prepend(d);
    }

    // --- UI UTILS ---
    addChatUI(u, pic, txt, time) {
        let box = document.getElementById('chat-feed');
        let h = `
        <div class="msg-entry">
            <img src="${pic}" class="msg-pic">
            <div class="msg-bub">
                <div class="msg-meta"><span class="msg-usr">${u}</span><span>${time}</span></div>
                <div class="msg-body">${txt}</div>
            </div>
        </div>`;
        box.insertAdjacentHTML('afterbegin', h);
    }

    addVaultUI(u, url) {
        if(!url.startsWith("http")) url = "https://chatp.net"+url;
        let box = document.getElementById('vault-feed');
        box.insertAdjacentHTML('afterbegin', `<div class="v-item" onclick="window.open('${url}')"><img src="${url}"><div class="v-lbl">${u}</div></div>`);
    }

    updateCubes() {
        if(this.avatars.length === 0) return;
        let faces = document.querySelectorAll('.c-face');
        let f = faces[Math.floor(Math.random()*faces.length)];
        let img = this.avatars[Math.floor(Math.random()*this.avatars.length)];
        f.style.backgroundImage = `url(${img})`;
        f.innerText = "";
    }

    beep(f) {
        if(this.audio.state === 'suspended') this.audio.resume();
        let o = this.audio.createOscillator();
        let g = this.audio.createGain();
        o.connect(g); g.connect(this.audio.destination);
        o.frequency.value = f; g.gain.value = 0.1;
        o.start(); o.stop(this.audio.currentTime + 0.1);
    }

    exportTarget() {
        if(!this.activeTarget) return;
        let u = this.users.get(this.activeTarget);
        let txt = u.logs.map(l => `[${l.time}] ${l.body}`).join("\n");
        this.dl(txt, `${this.activeTarget}_LOGS.txt`);
    }
    
    exportAll() { this.dl(this.allLogs.join("\n"), "FULL_LOGS.txt"); }
    
    dl(c, n) {
        let a = document.createElement('a');
        a.href = URL.createObjectURL(new Blob([c], {type:'text/plain'}));
        a.download = n;
        a.click();
    }

    animateBg() {
        const c = document.getElementById('bg-canvas'); const x = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        let p = []; for(let i=0;i<50;i++) p.push({x:Math.random()*c.width, y:Math.random()*c.height, r:Math.random()*2});
        function draw() {
            x.clearRect(0,0,c.width,c.height); x.fillStyle = "white";
            p.forEach(d => { d.y -= 0.5; if(d.y < 0) d.y = c.height; x.beginPath(); x.arc(d.x, d.y, d.r, 0, 6.28); x.fill(); });
            requestAnimationFrame(draw);
        }
        draw();
    }
}

const sys = new TitanCore();
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