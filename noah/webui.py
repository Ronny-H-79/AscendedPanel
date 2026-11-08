"""Web-UI fuer noah: Dashboard mit Instanzen + Instanzseiten + JSON-API."""
from __future__ import annotations

import json
import os
import re
import hmac
import secrets
import ssl
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .instance import Instance
from . import commands as cmdreg
from . import i18n
from . import backups as bk
from . import config as cfgfile
from . import metrics
from . import notify as notify_mod
from . import mods as modlib
from . import registry
from . import runner
from . import snapshots as snap
from . import whitelist as wl
from .rcon import RconClient

TOKEN_PATH = os.path.expanduser("~/.config/noah/token")
RE_PLAYER = re.compile(r"^\s*(\d+)\.\s*(.+?),\s*([0-9]{15,17})\s*$")
INSTALLS: dict[str, dict] = {}


def token() -> str:
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH) as fh:
            t = fh.read().strip()
            if t:
                return t
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    t = secrets.token_urlsafe(24)
    with open(os.open(TOKEN_PATH, os.O_CREAT | os.O_WRONLY, 0o600), "w") as fh:
        fh.write(t)
    return t


def _render(template: str) -> str:
    """Sprachkatalog und Sprachcode einsetzen."""
    from . import __version__
    return (template
            .replace("__LANGJSON__", json.dumps(i18n.catalog(), ensure_ascii=False))
            .replace("__VERSION__", __version__)
            .replace("__LANG__", i18n.lang()))


def rcon_cmd(inst: Instance, cmd: str, timeout: float = 12.0) -> str:
    with RconClient("127.0.0.1", inst.rcon_port, inst.rcon_password, timeout=timeout) as rc:
        return rc.command(cmd, timeout=timeout + 5)


def players(inst: Instance) -> list[dict[str, str]]:
    try:
        out = rcon_cmd(inst, "ListPlayers", timeout=10)
    except Exception:  # noqa: BLE001
        return []
    found = []
    for line in out.splitlines():
        m = RE_PLAYER.match(line)
        if m:
            found.append({"id": m.group(1), "name": m.group(2).strip(), "steamid": m.group(3)})
    return found


SHARED_CSS = """
:root{--bg:#06090e;--fg:#c8f0e0;--dim:#4e6b64;--acc:#25e6a4;--warn:#ffb454;--err:#ff5f6d}
*{box-sizing:border-box}
body{margin:0;color:var(--fg);font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
min-height:100vh;
background:
 radial-gradient(1100px 620px at 12% -8%, rgba(37,230,164,.16), transparent 62%),
 radial-gradient(900px 560px at 88% 8%, rgba(56,132,255,.13), transparent 60%),
 radial-gradient(1200px 800px at 50% 120%, rgba(37,230,164,.10), transparent 65%),
 linear-gradient(160deg,#05080c 0%,#070c12 45%,#04070a 100%);
background-attachment:fixed}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;
background:radial-gradient(120% 90% at 50% 45%, transparent 45%, rgba(0,0,0,.55) 100%)}
#bg{position:fixed;inset:0;z-index:0;opacity:.85}
header,main,.cards{position:relative;z-index:2}
header{padding:16px 24px;border-bottom:1px solid #16302a;display:flex;gap:14px;align-items:center;
flex-wrap:wrap;background:rgba(6,9,14,.75)}
h1{font-size:15px;margin:0;letter-spacing:.18em;text-transform:uppercase;color:var(--acc)}
a{color:var(--acc);text-decoration:none}
.badge.warn{border-color:#e67e22;color:#e67e22}
.badge.ok{border-color:#25e6a4;color:#25e6a4}
.badge{padding:2px 8px;border:1px solid var(--dim);border-radius:3px;font-size:11px;color:var(--dim)}
.badge.on{border-color:var(--acc);color:var(--acc)}
.badge.off{border-color:var(--err);color:var(--err)}
.badge.warn{border-color:var(--warn);color:var(--warn)}
main{padding:22px 24px;display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
section{border:1px solid #16302a;border-radius:5px;padding:14px 16px;background:rgba(11,17,22,.88)}
h2{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--dim);margin:0 0 12px}
button{background:#0f1a1f;color:var(--fg);border:1px solid #22453c;border-radius:3px;padding:6px 11px;
font:inherit;font-size:11px;cursor:pointer;letter-spacing:.06em}
button:hover{border-color:var(--acc);color:var(--acc)}
button.primary{border-color:var(--acc);color:var(--acc)}
button.danger:hover{border-color:var(--err);color:var(--err)}
#log{height:48vh;min-height:280px;max-height:none;resize:vertical;border:1px solid var(--line);
border-radius:8px;padding:10px 12px;background:rgba(0,0,0,.28)}
pre{margin:0;max-height:230px;overflow:auto;font-size:11.5px;white-space:pre-wrap;word-break:break-word;
color:#9fc4b8}
textarea{width:100%;min-height:250px;background:#0f1a1f;border:1px solid #22453c;color:#9fc4b8;
font:11.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;border-radius:3px;padding:8px}
input,select{width:100%;background:#0f1a1f;border:1px solid #22453c;color:var(--fg);padding:7px 9px;
font:inherit;border-radius:3px;margin-bottom:6px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.kv{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;font-size:12px}
.kv span:nth-child(odd){color:var(--dim)}
.p{border-top:1px solid #12241f;padding:7px 0;display:flex;gap:8px;justify-content:space-between;
align-items:center;flex-wrap:wrap}
.p small{color:var(--dim)}
#out{color:var(--warn);margin-top:8px}
.tabs{display:flex;gap:6px;padding:12px 24px 0;flex-wrap:wrap;position:relative;z-index:2}
.tabs button{background:transparent;border:1px solid #16302a;border-bottom-color:transparent;
border-radius:4px 4px 0 0;padding:7px 14px;font-size:11.5px;letter-spacing:.08em;color:var(--dim)}
.tabs button.on{border-color:var(--acc);color:var(--acc);background:rgba(37,230,164,.06)}
.tab.wide{grid-column:1/-1}
.tab{display:none}
.tab.on{display:block}
.setrow{display:grid;grid-template-columns:1fr 190px;gap:8px;align-items:center;
padding:6px 0;border-top:1px solid #12241f}
.setrow label b{font-weight:500;display:block}
.setrow label small{color:var(--dim);font-size:10.5px}
.setrow input[type=text],.setrow input[type=number]{margin:0}
.setrow .bool{display:flex;justify-content:flex-end}
.setrow input[type=checkbox]{width:auto;transform:scale(1.25);margin:0}
.cards{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));padding:0 24px 24px}
.card{border:1px solid #16302a;border-radius:6px;padding:14px 16px;background:rgba(11,17,22,.92);
display:flex;flex-direction:column;gap:10px;position:relative;overflow:hidden}
.card .bgimg{position:absolute;inset:0;background-size:cover;background-position:center;
opacity:.62;filter:saturate(.9) contrast(1.05) brightness(.95);z-index:0}
.card .bgimg::after{content:"";position:absolute;inset:0;
background:linear-gradient(180deg,rgba(6,9,14,.30) 0%,rgba(6,9,14,.62) 45%,rgba(6,9,14,.88) 100%)}
.card>*{position:relative;z-index:1}
.card h3{margin:0;font-size:14px;letter-spacing:.06em}
.card .meta{color:var(--dim);font-size:11.5px}
#mods{max-height:430px;overflow-y:auto;padding-right:4px}
.thumb{width:44px;height:44px;border-radius:4px;object-fit:cover;border:1px solid #16302a;flex:0 0 44px}
.mrow{display:flex;gap:10px;align-items:center}
.mrow .txt{min-width:0}
.mrow .txt b{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px}
.modal{position:fixed;inset:0;background:rgba(2,5,7,.82);display:none;z-index:50;
align-items:center;justify-content:center;padding:24px}
.modal.on{display:flex}
.mbox{background:#0b1116;border:1px solid #1d3a32;border-radius:8px;max-width:640px;width:100%;
max-height:80vh;overflow:auto;padding:18px 20px;position:relative}
.mbox img.big{width:96px;height:96px;border-radius:6px;border:1px solid #16302a;float:left;margin:0 14px 8px 0}
.mbox h3{margin:0 0 4px;font-size:15px}
.mbox .desc{white-space:pre-wrap;font-size:12px;color:#9fc4b8;margin-top:10px;clear:both}
.mbox .close{position:absolute;top:10px;right:12px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:2px 0}
.stats div{background:#0a1418;border:1px solid #12241f;border-radius:4px;padding:6px 8px}
.stats b{display:block;font-size:15px;color:var(--fg);font-weight:500}
.stats small{display:block;color:var(--dim);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase}
.spark{width:100%;height:38px;display:block}
.hostbar{display:flex;gap:10px;align-items:center;font-size:11px;color:var(--dim)}
"""

BG_JS = """
const cv=document.getElementById('bg');
if(cv){
  const ctx=cv.getContext('2d');
  let W=0,H=0,dpr=Math.min(devicePixelRatio||1,2),pts=[],mx=.5,my=.5,t0=performance.now();
  // Glow-Sprite einmal vorrendern (schneller als Schatten pro Punkt)
  const glow=document.createElement('canvas'); glow.width=glow.height=64;
  const gc=glow.getContext('2d'); const grd=gc.createRadialGradient(32,32,0,32,32,32);
  grd.addColorStop(0,'rgba(120,255,214,.85)');
  grd.addColorStop(.35,'rgba(37,230,164,.35)');
  grd.addColorStop(1,'rgba(37,230,164,0)');
  gc.fillStyle=grd; gc.fillRect(0,0,64,64);

  function build(){
    W=cv.width=innerWidth*dpr; H=cv.height=innerHeight*dpr;
    cv.style.width=innerWidth+'px'; cv.style.height=innerHeight+'px';
    const n=Math.min(90,Math.max(28,Math.floor(innerWidth*innerHeight/22000)));
    pts=Array.from({length:n},()=>({
      x:Math.random()*W, y:Math.random()*H,
      z:.35+Math.random()*.65,
      vx:(Math.random()-.5)*.10, vy:(Math.random()-.5)*.10,
      ph:Math.random()*Math.PI*2
    }));
  }
  addEventListener('resize',build); addEventListener('mousemove',e=>{mx=e.clientX/innerWidth;my=e.clientY/innerHeight;});
  build();

  function frame(now){
    const t=(now-t0)/1000, dt=Math.min(.05,(now-t0)/1000);
    ctx.clearRect(0,0,W,H);
    const ox=(mx-.5)*40*dpr, oy=(my-.5)*40*dpr;
    for(const p of pts){
      p.x+=p.vx*dpr*6*(1+p.z); p.y+=p.vy*dpr*6*(1+p.z);
      if(p.x<-80)p.x=W+80; if(p.x>W+80)p.x=-80;
      if(p.y<-80)p.y=H+80; if(p.y>H+80)p.y=-80;
    }
    // Verbindungen
    const R=170*dpr;
    for(let i=0;i<pts.length;i++){
      const a=pts[i];
      for(let j=i+1;j<pts.length;j++){
        const b=pts[j];
        const dx=a.x-b.x, dy=a.y-b.y, d=Math.hypot(dx,dy);
        if(d<R){
          const al=(1-d/R)*.28*Math.min(a.z,b.z);
          ctx.strokeStyle='rgba(37,230,164,'+al.toFixed(3)+')';
          ctx.lineWidth=(.6+a.z*.7)*dpr;
          ctx.beginPath();
          ctx.moveTo(a.x+ox*a.z, a.y+oy*a.z);
          ctx.lineTo(b.x+ox*b.z, b.y+oy*b.z);
          ctx.stroke();
        }
      }
    }
    // Knoten mit Glow und langsamem Puls
    for(const p of pts){
      const pulse=.55+.45*Math.sin(t*1.2+p.ph);
      const s=(10+p.z*22)*dpr*pulse;
      ctx.globalAlpha=(.35+p.z*.5)*pulse;
      ctx.drawImage(glow, p.x-s/2+ox*p.z, p.y-s/2+oy*p.z, s, s);
      ctx.globalAlpha=1;
      ctx.fillStyle='rgba(200,255,235,'+(.25+p.z*.45)+')';
      const c=(1.1+p.z*1.6)*dpr;
      ctx.fillRect(p.x+ox*p.z, p.y+oy*p.z, c, c);
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
"""

DASH = """<!doctype html><html lang="__LANG__"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>noah</title>
<style>""" + SHARED_CSS + """</style></head><body>
<canvas id="bg"></canvas>
<header><h1>noah</h1><span class="badge" id="cnt">…</span>
<span class="badge" data-t="dash.dashboard">Dashboard</span>
<span class="hostbar"><span id="hostcpu">CPU –</span><span id="hostram">RAM –</span>
  <button onclick="noahUpdate()" id="verbtn" style="padding:2px 8px">noah</button>
  <button onclick="openChangelog()" id="clogbtn" style="padding:2px 8px"
    data-t="self.changelog" title="Changelog">Changelog</button>
  <button onclick="toggleLang()" id="langbtn" style="padding:2px 8px">EN</button></span></header>
<div class="modal" id="modal" onclick="if(event.target.id==='modal')closeModal()">
  <div class="mbox"><button class="close" onclick="closeModal()">×</button>
    <div id="mbody">…</div></div>
</div>
<div class="cards" id="cards"></div>
<main>
  <section><h2 data-t="dash.new_instance">Neue Instanz</h2>
    <input id="nname" data-tp="dash.name_ph" placeholder="Name">
    <select id="nmap">__MAPS__</select>
    <input id="nport" data-tp="dash.port_ph" placeholder="Port">
    <input id="nsession" data-tp="dash.session_ph" placeholder="Session">
    <div class="row"><button class="primary" onclick="createInst()" data-t="dash.create">Anlegen</button></div>
    <pre id="out">–</pre>
  </section>
  <section><h2 data-t="dash.note">Hinweis</h2>
    <div class="kv">
      <span data-t="dash.install_label">Installation</span><span data-t="dash.install_size">SteamCMD</span>
      <span data-t="dash.ports_label">Ports</span><span data-t="dash.ports">Ports</span>
      <span data-t="dash.memory_label">Speicher</span><span data-t="dash.memory">RAM</span>
    </div>
  </section>
</main>
<script>""" + BG_JS + """
const L=__LANGJSON__;
async function toggleLang(){
  const next = (L.lang === 'de') ? 'en' : 'de';
  try{ await fetch('/api/lang?set=' + next + '&token=' + encodeURIComponent(T), {method:'POST'}); }
  catch(e){ alert('Sprache/Sprache konnte nicht gespeichert werden: ' + e); return; }
  location.reload();
}
function applyLang(){
  document.querySelectorAll('[data-t]').forEach(e=>{const k=e.dataset.t;if(L[k])e.textContent=L[k];});
  document.querySelectorAll('[data-tp]').forEach(e=>{const k=e.dataset.tp;if(L[k])e.placeholder=L[k];});
  const lb=document.getElementById('langbtn'); if(lb) lb.textContent=(L.lang==='de')?'EN':'DE';
}
const T=new URLSearchParams(location.search).get('token')||'';
const api=(p,o)=>fetch(p+(p.includes('?')?'&':'?')+'token='+encodeURIComponent(T),o).then(r=>r.text());
let DATA=[];
function fmtUp(s){ if(!s) return '–'; const h=Math.floor(s/3600), m=Math.floor(s%3600/60);
  return h? h+'h '+m+'m' : m+'m'; }
function spark(cv, a, b, amax, bmax){
  const ctx=cv.getContext('2d'), W=cv.width, H=cv.height, P=2;
  const line=(arr,max,color)=>{ if(!arr||arr.length<2)return;
    ctx.beginPath(); ctx.strokeStyle=color; ctx.lineWidth=1.4;
    arr.forEach((v,idx)=>{ const x=P+idx/(arr.length-1)*(W-2*P);
      const y=H-P-Math.min(1,v/(max||1))*(H-2*P);
      idx?ctx.lineTo(x,y):ctx.moveTo(x,y); });
    ctx.stroke(); };
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(37,230,164,.10)'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(0,H-P); ctx.lineTo(W,H-P); ctx.stroke();
  line(b, bmax, 'rgba(120,170,255,.55)');
  line(a, amax, 'rgba(37,230,164,.95)');
}
async function load(){
  const list=JSON.parse(await api('/api/instances'));
  DATA=list;
  document.getElementById('cnt').textContent=list.length+' '+L['dash.instances'];
  document.getElementById('cards').innerHTML=list.map(i=>`
    <div class="card">
      ${i.map_image?`<div class="bgimg" style="background-image:url('${i.map_image}?token=${encodeURIComponent(T)}')"></div>`:''}
      <div class="row" style="justify-content:space-between">
        <h3>${i.name}</h3>
        <span class="badge ${i.running?(i.ready?'on':'warn'):'off'}">${i.running?(i.ready?L['status.running']:L['status.starting']):L['status.off']}</span>
      </div>
      <div class="meta">${i.map} · Port ${i.port} · RCON ${i.rcon_port}</div>
      <div class="meta">${i.installed?('Build '+i.build+' · '+i.size_gb+' GB'):L['dash.not_installed']}</div>
      ${i.running?`<div class="stats">
        <div><b>${i.cpu.toFixed(1)}%</b><small>${L['dash.cpu']}</small></div>
        <div title="Spitze: ${i.ram_peak_gb||0} GB"><b>${i.ram_gb.toFixed(1)}G</b><small>${L['dash.ram']}</small></div>
        <div><b>${i.players}</b><small>${L['dash.players']}</small></div>
        <div><b>${fmtUp(i.uptime)}</b><small>${L['dash.uptime']}</small></div>
      </div><canvas class="spark" width="300" height="38"></canvas>`:''}
      <div class="row">
        <a href="/i/${i.name}?token=${encodeURIComponent(T)}"><button>${L['common.open']}</button></a>
        ${i.installed
          ? `<button onclick="act('${i.name}','start')">${L['common.start']}</button>
             <button onclick="act('${i.name}','restart')">${L['common.restart']}</button>
             <button onclick="updInst('${i.name}')">${L['common.update']}</button>
             <button class="danger" onclick="act('${i.name}','stop')">${L['common.stop']}</button>
             <button class="danger" onclick="delInst('${i.name}',${i.size_gb||0})">${L['common.delete']}</button>`
          : `<button class="primary" onclick="install('${i.name}')">${L['dash.install']}</button>`}
      </div>
    </div>`).join('');
  const canvases=[...document.querySelectorAll('.spark')];
  canvases.forEach(cv=>{
    const name=cv.closest('.card').querySelector('h3').textContent.trim();
    const d=DATA.find(x=>x.name===name); if(!d)return;
    const rmax=Math.max(1,...(d.ram_hist||[0]));
    spark(cv, d.cpu_hist||[], d.ram_hist||[], 100, rmax*1.15);
  });
}
async function loadHost(){
  try{ const h=JSON.parse(await api('/api/host'));
    document.getElementById('hostcpu').textContent='CPU '+h.cpu.toFixed(1)+'%';
    document.getElementById('hostram').textContent='RAM '+h.ram_used_gb+'/'+h.ram_total_gb+' GB ('+h.ram_pct+'%)';
  }catch(e){}
}
async function act(name,what){ await api('/api/'+what+'?name='+name,{method:'POST'}); setTimeout(load,1500); }


async function updInst(name){
  if(!confirm(L['msg.confirm_update'])) return;
  try{
    await api('/api/update?name='+encodeURIComponent(name), {method:'POST'});
    alert(L['msg.update_started']);
    setTimeout(load, 1500);
  }catch(e){ alert(String(e)); }
}
async function delInst(name, sizeGb){
  if(!confirm(L['msg.confirm_instance_delete'].replace('{n}', name))) return;
  let files = 0;
  if(confirm(L['msg.confirm_instance_files'].replace('{n}', name).replace('{size}', sizeGb))){
    files = 1;
  }
  const msg = document.getElementById('instmsg');
  if(msg) msg.textContent='…';
  try{
    const r = await api('/api/instance/delete?name='+encodeURIComponent(name)+'&files='+files, {method:'POST'});
    if(r.ok){ load(); } else { alert(r.error || 'Fehler'); }
  }catch(e){ alert(String(e)); }
}
async function createInst(){
  const name=document.getElementById('nname').value.trim();
  if(!name){alert('Name fehlt');return;}
  const q=new URLSearchParams({name:name,map:document.getElementById('nmap').value,
    port:document.getElementById('nport').value,session:document.getElementById('nsession').value}).toString();
  document.getElementById('out').textContent=await api('/api/instances?'+q,{method:'POST'});
  setTimeout(load,800);
}
async function install(name){
  document.getElementById('out').textContent=await api('/api/install?name='+name,{method:'POST'});
  const t=setInterval(async()=>{
    const l=await api('/api/install/log?name='+name);
    document.getElementById('out').textContent=l;
    if(l.startsWith('[fertig]')) clearInterval(t);
  },4000);
}

let _noahInfo=null;
async function checkNoah(){
  try{ _noahInfo=JSON.parse(await api('/api/selfupdate')); }catch(e){ return; }
  const b=document.getElementById('verbtn');
  if(!b||!_noahInfo||!_noahInfo.ok) return;
  if(!_noahInfo.update){
    b.textContent='noah '+_noahInfo.installed+' · '+L['self.current_build']; b.className='';
    b.disabled=true; b.style.cursor='default'; b.style.opacity='.7';
    b.title=L['self.up_to_date'];
    return;
  }
  else if(_noahInfo.available && _noahInfo.available!==_noahInfo.installed){
    b.textContent='noah update: '+_noahInfo.installed+' → '+_noahInfo.available;
    b.className='badge on';
  } else {
    // gleiche Version, nur neuer Commit: nur ein Hinweis, nicht klickbar
    b.textContent='noah '+_noahInfo.installed+' · '+L['self.new_build'];
    b.className='badge';
    b.disabled=true; b.style.cursor='default'; b.style.opacity='.7';
    b.title=L['self.build_only'];
    return;
  }
  b.disabled=false; b.style.cursor=''; b.style.opacity='';

  b.title = _noahInfo.update ? L['self.click_update'] : L['self.up_to_date'];
}

function closeModal(){ const m=document.getElementById('modal'); if(m) m.classList.remove('on'); }
function _links(html){
  let out='', i=0;
  while(true){
    const a=html.indexOf('[', i), b=html.indexOf('](', a+1), c=html.indexOf(')', b+2);
    if(a<0||b<0||c<0){ out+=html.slice(i); break; }
    const label=html.slice(a+1,b);
    if(b-a>80 || label.indexOf('<')>=0){ out+=html.slice(i,a+1); i=a+1; continue; }
    out+=html.slice(i,a);
    out+='<a href="'+html.slice(b+2,c)+'" target="_blank">'+html.slice(a+1,b)+'</a>';
    i=c+1;
  }
  return out;
}
function _mdToHtml(text){
  const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
  const out=[];
  for(const raw of text.split(String.fromCharCode(10))){
    const line=raw.split(String.fromCharCode(13)).join('');
    if(line.startsWith('### ')) out.push('<h4 style="margin:10px 0 4px">'+esc(line.slice(4))+'</h4>');
    else if(line.startsWith('## ')) out.push('<h3 style="margin:14px 0 6px;color:var(--acc)">'+esc(line.slice(3))+'</h3>');
    else if(line.startsWith('# ')) out.push('<h3 style="margin:0 0 8px">'+esc(line.slice(2))+'</h3>');
    else if(line.startsWith('  - ')||line.startsWith('    - ')) out.push('<div class="meta" style="padding-left:26px">• '+esc(line.trim().slice(2))+'</div>');
    else if(line.startsWith('- ')) out.push('<div style="margin:3px 0 3px 12px">• '+esc(line.slice(2))+'</div>');
    else if(line.trim()==='') out.push('<div style="height:4px"></div>');
    else out.push('<div class="meta">'+esc(line)+'</div>');
  }
  let html=out.join('');
  const bold=html.split('**');
  html=bold.map((part,i)=> (i%2) ? '<b>'+part+'</b>' : part).join('');
  const code=html.split('`');
  html=code.map((part,i)=> (i%2) ? '<code>'+part+'</code>' : part).join('');
  html=_links(html);
  return html;
}
async function openChangelog(){
  const box=document.getElementById('mbody');
  box.innerHTML='<div class="meta">'+L['common.loading']+'</div>';
  document.getElementById('modal').classList.add('on');
  let d;
  try{ d=JSON.parse(await api('/api/changelog?lang='+encodeURIComponent(L.lang||'de'))); }
  catch(e){ box.innerHTML='<div class="meta">'+L['mods.search_failed']+'</div>'; return; }
  if(!d.ok){ box.innerHTML='<div class="meta">'+(d.error||'')+'</div>'; return; }
  box.innerHTML='<div style="max-height:64vh;overflow:auto;padding-right:6px">'+_mdToHtml(d.text)+'</div>'+
    (d.url?('<div style="margin-top:10px"><a href="'+d.url+'" target="_blank">'+L['self.on_github']+'</a></div>'):'');
}
async function noahUpdate(){
  if(!_noahInfo){ await checkNoah(); }
  if(!_noahInfo || !_noahInfo.ok) return;
  if(!_noahInfo.update){ alert(L['self.up_to_date']); return; }
  let notes='';
  try{ const n=JSON.parse(await api('/api/selfupdate/notes?v='+encodeURIComponent(_noahInfo.available)));
       if(n.ok && n.text) notes=String.fromCharCode(10,10)+n.text.slice(0,900); }catch(e){}
  if(!confirm(L['self.confirm'].replace('{v}', _noahInfo.available)+notes)) return;
  const b=document.getElementById('verbtn');
  b.textContent='…';
  try{ await api('/api/selfupdate',{method:'POST'}); }catch(e){}
  alert(L['self.done']);
  setTimeout(()=>location.reload(), 4000);
}
applyLang(); load(); loadHost(); checkNoah(); setInterval(load,3000); setInterval(loadHost,3000);
</script><footer style="text-align:center;padding:16px 0 10px;font-size:11.5px;color:var(--dim);
letter-spacing:.04em">noah __VERSION__ · © 2026 Ronny H.</footer>
</body></html>"""

INST = """<!doctype html><html lang="__LANG__"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>noah · __NAME__</title>
<style>""" + SHARED_CSS + """</style></head><body>
<canvas id="bg"></canvas>
<div class="modal" id="modal" onclick="if(event.target.id==='modal')closeModal()">
  <div class="mbox">
    <button class="close" onclick="closeModal()">×</button>
    <div id="mbody">…</div>
  </div>
</div>
<header>
  <a href="/?token=__TOK__" style="font-size:15px;letter-spacing:.18em;color:var(--acc)">noah</a>
  <a href="/?token=__TOK__" style="margin-left:6px"><button data-t="common.back_dashboard">← Dashboard</button></a>
  <span class="badge" id="st">…</span><span class="badge" id="rd">…</span>
  <span class="badge">__NAME__</span><span class="badge" id="upd" role="button" tabindex="0">UPDATE ?</span>
  <button onclick="toggleLang()" id="langbtn" style="padding:2px 8px">EN</button>
</header>
<div class="tabs">
  <button class="on" data-tab="overview" onclick="showTab('overview',this)" data-t="tabs.overview">Übersicht</button>
  <button data-tab="settings" onclick="showTab('settings',this)" data-t="tabs.settings">Einstellungen</button>
  <button data-tab="mods" onclick="showTab('mods',this)" data-t="tabs.mods">Mods</button>
  <button data-tab="server" onclick="showTab('server',this)" data-t="tabs.manage">Verwaltung</button>
</div>
<main>
  <section class="tab tab-overview on wide" id="logsec"><h2 data-t="inst.log">Server-Log</h2><pre id="log">…</pre></section>

  <section class="tab tab-overview on"><h2 data-t="inst.commands">Befehle</h2>
    <div id="cmds"></div>
    <input id="cmd" data-tp="inst.rcon_free" placeholder="RCON"
      onkeydown="if(event.key==='Enter')rcon()" style="margin-top:10px">
    <div class="row"><button onclick="rcon()" data-t="common.send">Senden</button></div>
    <pre id="out">–</pre>
  </section>

  <section class="tab tab-overview on"><h2 data-t="inst.players">Spieler</h2><div id="players">…</div></section>

  <section class="tab tab-server"><h2 data-t="wl.title">Whitelist &amp; Bans</h2>
    <div class="row" style="margin-bottom:8px">
      <button id="wlbtn" onclick="toggleWl()">Whitelist …</button>
      <span class="meta" id="wlcount"></span>
    </div>
    <input id="pid" data-tp="wl.id_ph" placeholder="ID" onkeydown="if(event.key==='Enter')addWl()">
    <div class="row">
      <button onclick="addWl()" data-t="wl.add">Auf Whitelist</button>
      <button class="danger" onclick="banId()" data-t="wl.ban">Bannen</button>
    </div>
    <div class="meta" style="margin:10px 0 2px">Whitelist</div>
    <div id="wllist">…</div>
    <div class="meta" style="margin:10px 0 2px" data-t="wl.banned_list">Gebannt (über noah)</div>
    <div id="banlist">…</div>
    <pre id="wlmsg">–</pre>
  </section>

  <section class="tab tab-mods"><h2 data-t="tabs.mods">Mods</h2>
    <div id="mods">…</div>
    <div class="row" style="margin-top:8px">
      <input id="modid" data-tp="mods.search_ph" placeholder="Mod suchen oder ID eingeben"
        oninput="suggestMods()" onkeydown="if(event.key==='Enter')searchMods()"
        autocomplete="off" style="flex:1">
      <button onclick="searchMods()" data-t="mods.search">Suchen</button>
      <button onclick="addMod()" data-t="common.add">Hinzufügen</button>
    </div>
    <div class="row"><span class="meta" id="keystate"></span></div>
    <div id="modhits"></div>
    <div class="row"><span class="meta" id="modsize"></span></div>
    <div class="setrow" style="margin-top:10px">
      <label><b data-t="mods.key">CurseForge-API-Key</b>
        <small data-t="mods.key_hint">optional - ohne Key ist die Suche unzuverlaessig; Key gibt es kostenlos auf console.curseforge.com</small></label>
      <input id="cfkey" type="password" placeholder="…">
    </div>
    <div class="row"><button onclick="saveKey()" data-t="common.save">Speichern</button>
      <span class="meta" id="cfkeymsg"></span></div>
    <pre id="modout" style="margin-top:8px">–</pre>
  </section>

  <section class="tab tab-settings"><h2 data-t="set.gui">Einstellungen (GUI)</h2>
    <div id="settings">lädt …</div>
    <div class="row" style="margin-top:10px">
      <button class="primary" onclick="saveSettings()" data-t="set.save_changes">Änderungen speichern</button>
      <span class="meta" id="setmsg"></span>
    </div>
  </section>

  <section class="tab tab-settings"><h2 data-t="set.raw">INI direkt bearbeiten</h2>
    <select id="cfgfile" onchange="loadCfg()">
      <option value="gus">GameUserSettings.ini</option>
      <option value="game">Game.ini</option>
    </select>
    <textarea id="cfgtext"></textarea>
    <div class="row" style="margin-top:6px"><button onclick="saveCfg()" data-t="common.save">Speichern</button>
      <span class="meta" id="cfgmsg"></span></div>
  </section>

  <section class="tab tab-server"><h2 data-t="snap.title">Instanz-Snapshot (Rollback)</h2>
    <div class="meta" data-t="snap.hint_text">Komplette Kopie der Serverdateien inklusive Mods – für den Fall, dass ein ARK-Update
      die Installation zerschießt. Ein Welt-Backup hilft dort nicht, weil SteamCMD immer die neue
      Programmversion liefert. Platzbedarf: ca. 12 GB pro Snapshot.</div>
    <div id="snaps" style="margin-top:10px">…</div>
    <div class="row" style="margin-top:8px">
      <button class="primary" onclick="makeSnap()" data-t="snap.create">Snapshot erstellen</button>
      <span class="meta" id="snapmsg"></span>
    </div>
  </section>

  <section class="tab tab-server"><h2 data-t="notify.title">Benachrichtigungen (Discord)</h2>
    <div class="meta" data-t="notify.hint">Webhook-Adresse aus Discord (Servereinstellungen → Integrationen → Webhooks).
      Meldungen: Absturz, Hänger-Neustart, neues Server-Update, Backup-Fehler.</div>
    <div class="setrow" style="margin-top:8px">
      <label><b data-t="notify.url">Webhook-URL</b><small data-t="notify.url_hint">leer = keine Meldungen</small></label>
      <input id="hookurl" data-tp="notify.url_ph" placeholder="https://discord.com/api/webhooks/…">
    </div>
    <div class="row" style="margin-top:8px">
      <button class="primary" onclick="saveHook()" data-t="common.save">Speichern</button>
      <button onclick="testHook()" data-t="notify.test">Test senden</button>
      <span class="meta" id="hookmsg"></span>
    </div>
  </section>

  <section class="tab tab-server"><h2 data-t="bk.title">Backups</h2>
    <div id="backups">…</div>
    <div class="setrow"><label><b data-t="bk.times">Backup-Uhrzeiten</b>
      <small data-t="bk.times_hint">hint</small></label>
      <input id="schedBackup" type="text" placeholder="03:00"></div>
    <div class="row" style="margin-top:8px">
      <button class="primary" onclick="makeBackup()" data-t="bk.now">Jetzt sichern</button>
      <span class="meta" id="bkmsg"></span>
    </div>
  </section>

  <section class="tab tab-server"><h2 data-t="sched.title">Zeitplan (Neustart)</h2>
    <div class="setrow"><label><b data-t="sched.restart_times">Neustart-Uhrzeiten</b>
      <small data-t="sched.restart_hint">hint</small></label>
      <input id="schedRestart" type="text" placeholder="05:00,17:00"></div>
    <div class="setrow"><label><b data-t="sched.warn">Vorwarnung vor Neustart</b>
      <small data-t="sched.warn_hint">hint</small></label>
      <input id="schedWarn" type="number" placeholder="5"></div>
    <div class="setrow"><label><b data-t="sched.keep">Backups behalten</b>
      <small data-t="sched.keep_hint">hint</small></label>
      <input id="schedKeep" type="number" placeholder="10"></div>
    <div class="row" style="margin-top:10px"><button onclick="saveSchedule()" data-t="common.save">Speichern</button></div>
    <pre id="schedmsg">–</pre>
  </section>

</main>
<script>""" + BG_JS + """
const NAME='__NAME__';
const L=__LANGJSON__;
async function toggleLang(){
  const next = (L.lang === 'de') ? 'en' : 'de';
  try{ await fetch('/api/lang?set=' + next + '&token=' + encodeURIComponent(T), {method:'POST'}); }
  catch(e){ alert('Sprache/Sprache konnte nicht gespeichert werden: ' + e); return; }
  location.reload();
}
function applyLang(){
  document.querySelectorAll('[data-t]').forEach(e=>{const k=e.dataset.t;if(L[k])e.textContent=L[k];});
  document.querySelectorAll('[data-tp]').forEach(e=>{const k=e.dataset.tp;if(L[k])e.placeholder=L[k];});
  const lb=document.getElementById('langbtn'); if(lb) lb.textContent=(L.lang==='de')?'EN':'DE';
}
const T=new URLSearchParams(location.search).get('token')||'';
const api=(p,o)=>fetch(p+(p.includes('?')?'&':'?')+'token='+encodeURIComponent(T)+'&name='+NAME,o).then(r=>r.text());
async function refresh(){
  try{
    const s=JSON.parse(await api('/api/status'));
    const st=document.getElementById('st'); st.textContent=s.running?L['status.running']:L['status.off'];
    st.className='badge '+(s.running?'on':'off');
    const rd=document.getElementById('rd'); rd.textContent=s.ready?L['status.ready']:L['status.starting'];
    rd.className='badge '+(s.ready?'on':'');
    const infoEl=document.getElementById('info');
    if(infoEl){ const rows=[['PID',s.pid??'–'],['RCON',s.rcon??'–']];
      infoEl.innerHTML=rows.map(([k,v])=>`<span>${k}</span><span>${v}</span>`).join(''); }
  }catch(e){}
  try{ const _l=document.getElementById('log'); _l.textContent=await api('/api/logs?n=150');
       const _end=()=>{_l.scrollTop=_l.scrollHeight;};
       _end(); requestAnimationFrame(()=>{_end(); setTimeout(_end,60);}); }catch(e){}
  try{
    const pl=JSON.parse(await api('/api/players'));
    document.getElementById('players').innerHTML=pl.length?pl.map(p=>
      `<div class="p"><span><b>${p.name}</b><br><small>${p.steamid}</small></span>
       <span class="row">
         <button onclick="pa('${p.steamid}','kick')">${L['inst.kick']}</button>
         <button class="danger" onclick="pa('${p.steamid}','ban')">${L['inst.ban']}</button>
         <button onclick="pa('${p.steamid}','whitelist')">${L['inst.whitelist']}</button>
         <button onclick="give('${p.steamid}')">${L['inst.item']}</button>
       </span></div>`).join('')
      :'<span style="color:var(--dim)">– '+L['inst.no_players']+' –</span>';
  }catch(e){}
}
async function act(a){ await api('/api/'+a,{method:'POST'}); setTimeout(refresh,1200); }
async function updCheck(){
  try{ const u=JSON.parse(await api('/api/update')); const b=document.getElementById('upd');
    if(u.up_to_date===null || u.installed==null){b.style.display='none';return;}
    b.style.display='';
    if(u.up_to_date){
      // Build ist aktuell: Klick prüft erneut
      b.textContent=L['status.current']+' '+u.installed; b.className='badge on';
      b.title=L['status.hint_current']; b.style.cursor='pointer';
      b.onclick=updCheck; b.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();updCheck();}};
    } else {
      // Update verfuegbar: Klick startet es (mit Rueckfrage) - auch hier auf der Instanzseite
      b.textContent=L['status.update_available']+' '+u.installed+'→'+u.available; b.className='badge off';
      b.title=L['status.hint_update']; b.style.cursor='pointer';
      b.onclick=doUpdate; b.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();doUpdate();}};
    }
  }catch(e){}
}
async function doUpdate(){
  if(!confirm(L['msg.confirm_update']))return;
  document.getElementById('out').textContent=await api('/api/update',{method:'POST'});
  setTimeout(refresh,5000);
}
async function rcon(){ const c=document.getElementById('cmd').value.trim(); if(!c)return;
  document.getElementById('out').textContent=await api('/api/rcon?cmd='+encodeURIComponent(c),{method:'POST'}); }
let CMDS=null;
async function loadCmds(){ if(CMDS)return CMDS; CMDS=JSON.parse(await api('/api/commands')); return CMDS; }
async function renderCmds(){
  const list=await loadCmds(); const groups={};
  list.forEach(c=>{(groups[c.group]=groups[c.group]||[]).push(c);});
  document.getElementById('cmds').innerHTML=Object.entries(groups).map(([g,items])=>
    `<div style="margin-bottom:8px"><div style="color:var(--dim);font-size:10px;letter-spacing:.14em;
      text-transform:uppercase;margin:6px 0 4px">${g}</div>
     <div class="row">${items.map(c=>
       `<button class="${c.danger?'danger':''}" title="${c.note||''}"
          onclick="runCmd('${c.id}')">${c.label}</button>`).join('')}</div></div>`).join('');
}
async function runCmd(id){
  const c=(await loadCmds()).find(x=>x.id===id); if(!c)return;
  const params=new URLSearchParams({id:id});
  for(const [name,question,def] of c.args){
    const v=prompt(question,def); if(v===null)return; params.set(name,v);
  }
  if(c.confirm&&!confirm((c.note||c.label)+String.fromCharCode(10,10)+'Wirklich ausfuehren?'))return;
  document.getElementById('out').textContent='…';
  document.getElementById('out').textContent=await api('/api/command?'+params.toString(),{method:'POST'});
  setTimeout(refresh,1500);
}
function modRow(m, active){
  const label = m.state==='valid' ? L['mods.loaded'] : (m.state==='cooked' ? L['mods.old_engine'] : L['mods.unknown']);
  const sub = `${m.id}${active?' · '+label+(m.issue?' · '+m.issue:''):' · '+L['mods.on_disk']}`;
  const thumb = m.thumbnail
    ? `<img class="thumb" src="${m.thumbnail}" alt="" loading="lazy">`
    : '<div class="thumb"></div>';
  const actions = active
    ? `<button onclick="modInfo('${m.id}')">${L['common.info']}</button>
       <button onclick="delModFiles('${m.id}')">${L['common.delete']}</button>
       <button class="danger" onclick="delMod('${m.id}')">${L['common.disable']}</button>`
    : `<button onclick="modInfo('${m.id}')">Info</button>
       <button class="primary" onclick="enableMod('${m.id}')">${L['common.enable']}</button>
       <button class="danger" onclick="delModFiles('${m.id}')">${L['common.delete']}</button>`;
  return `<div class="p"><span class="mrow">${thumb}
      <span class="txt"><b>${m.title||m.name||('Mod '+m.id)}</b>${m.outdated?' <span class="badge warn">'+L['mods.outdated']+'</span>':''}
      <small>${sub}${m.outdated&&m.age_days!=null?(' · '+L['mods.updated_ago']+' '+m.age_days+' '+L['mods.days']):''}${m.summary?(' · '+m.summary):''}</small></span></span>
    <span class="row">${actions}</span></div>`;
}
async function modInfo(id){
  document.getElementById('mbody').innerHTML='lädt …';
  document.getElementById('modal').classList.add('on');
  const m=JSON.parse(await api('/api/mod/meta?id='+id));
  const img=m.thumbnail?`<img class="big" src="${m.thumbnail}" alt="">`:'';
  const cats=(m.categories||[]).join(', ');
  document.getElementById('mbody').innerHTML=`${img}
    <h3>${m.title||('Mod '+id)}</h3>
    <div class="meta">${id}${m.downloads?(' · '+m.downloads.toLocaleString('de-DE')+' Downloads'):''}${cats?(' · '+cats):''}</div>
    <div class="desc">${(m.description||m.summary||L['mods.no_desc']).replace(/</g,'&lt;')}</div>
    ${m.url?`<div style="margin-top:12px"><a href="${m.url}" target="_blank">Auf CurseForge öffnen</a></div>`:''}`;
}
function closeModal(){ document.getElementById('modal').classList.remove('on'); }
function showTab(name, btn){
  document.querySelectorAll('.tab').forEach(el=>el.classList.toggle('on', el.classList.contains('tab-'+name)));
  document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('on'));
  if(btn) btn.classList.add('on');
  try{ localStorage.setItem('noah.tab', name); if(history.replaceState) history.replaceState(null,'','#'+name); }catch(e){}
  if(name==='overview'){ const l=document.getElementById('log');
    if(l){ requestAnimationFrame(()=>{ l.scrollTop=l.scrollHeight; }); } }
}
function restoreTab(){
  let t='';
  try{ t = (location.hash||'').replace('#','') || localStorage.getItem('noah.tab') || ''; }catch(e){}
  const known=['overview','settings','mods','server'];
  if(!known.includes(t)) t='overview';
  const b=document.querySelector('.tabs button[data-tab="'+t+'"]');
  if(b) showTab(t, b); else showTab('overview', document.querySelector('.tabs button'));
}
window.addEventListener('hashchange', ()=>{
  const t=(location.hash||'').replace('#','');
  if(['overview','settings','mods','server'].includes(t)){
    const b=document.querySelector('.tabs button[data-tab="'+t+'"]');
    if(b) showTab(t, b);
  }
});
let SETTINGS=[];
async function loadSettings(){
  SETTINGS=JSON.parse(await api('/api/settings'));
  const groups={};
  SETTINGS.forEach(v=>{ const g=v.file==='gus'?'GameUserSettings.ini':'Game.ini';
    (groups[g]=groups[g]||[]).push(v); });
  document.getElementById('settings').innerHTML=Object.entries(groups).map(([file,items])=>
    `<div class="meta" style="margin:12px 0 4px">${file}</div>`+items.map((v,idx)=>{
      const i=SETTINGS.indexOf(v);
      let field;
      if(v.type==='bool'){
        const on=(v.value||'').toLowerCase()==='true';
        field=`<div class="bool"><input type="checkbox" data-i="${i}" ${on?'checked':''}></div>`;
      } else if(v.type==='longtext'){
        field=`<textarea data-i="${i}" rows="4" style="width:100%;resize:vertical"
                 >${(v.value||'').replace(/\\n/g,String.fromCharCode(10)).replace(/</g,'&lt;')}</textarea>`;
      } else {
        const t=(v.type==='int'||v.type==='float')?'number':'text';
        field=`<input type="${t}" data-i="${i}" value="${(v.value||'').replace(/"/g,'&quot;')}"
                 placeholder="${v.type==='bool'?'True/False':''}">`;
      }
      return `<div class="setrow"><label><b>${v.label}</b><small>${v.key}${v.hint?(' · '+v.hint):''}</small></label>${field}</div>`;
    }).join('')).join('');
}
async function saveSettings(){
  const payload=[];
  document.querySelectorAll('#settings input, #settings textarea').forEach(el=>{
    const v=SETTINGS[Number(el.dataset.i)];
    let value;
    if(el.type==='checkbox') value=el.checked?'True':'False';
    else if(el.tagName==='TEXTAREA') value=el.value.split(String.fromCharCode(13)).join('').split(String.fromCharCode(10)).join(String.fromCharCode(92)+'n').trim();
    else value=el.value.trim();
    if(value!=='' && value!==v.value){
      payload.push({file:v.file,section:v.section,key:v.key,value:value});
    }
  });
  if(!payload.length){document.getElementById('setmsg').textContent=L['set.no_changes'];return;}
  const r=await fetch('/api/settings?name='+NAME+'&token='+encodeURIComponent(T),
    {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  document.getElementById('setmsg').textContent=await r.text();
  loadSettings(); loadCfg();
}
async function loadWl(){
  const w=JSON.parse(await api('/api/whitelist'));
  const b=JSON.parse(await api('/api/bans'));
  const btn=document.getElementById('wlbtn');
  btn.textContent='Whitelist '+(w.enabled?L['wl.on']:L['wl.off']);
  btn.className=w.enabled?'primary':'';
  document.getElementById('wlcount').textContent=w.players.length+' '+L['wl.entries']+' · '+(w.exists?L['wl.file_present']:L['wl.file_missing']);
  document.getElementById('wllist').innerHTML=w.players.length?w.players.map(p=>
    `<div class="p"><span><b>${p}</b></span>
      <span class="row"><button onclick="delWl('${p}')">${L['common.remove']}</button></span></div>`).join('')
    :'<span style="color:var(--dim)">– leer –</span>';
  document.getElementById('banlist').innerHTML=(b.bans||[]).length?b.bans.map(p=>
    `<div class="p"><span><b>${p}</b></span>
      <span class="row"><button onclick="unbanId('${p}')">Entbannen</button></span></div>`).join('')
    :'<span style="color:var(--dim)">– '+L['bk.none_dash']+' –</span>';
}
async function toggleWl(){
  const w=JSON.parse(await api('/api/whitelist'));
  document.getElementById('wlmsg').textContent=await api('/api/whitelist/enable?on='+(w.enabled?0:1),{method:'POST'});
  loadWl();
}
async function addWl(){
  const id=document.getElementById('pid').value.trim(); if(!id)return;
  document.getElementById('wlmsg').textContent=await api('/api/whitelist/add?id='+encodeURIComponent(id),{method:'POST'});
  document.getElementById('pid').value=''; loadWl();
}
async function delWl(id){
  document.getElementById('wlmsg').textContent=await api('/api/whitelist/remove?id='+encodeURIComponent(id),{method:'POST'});
  loadWl();
}
async function banId(){
  const id=document.getElementById('pid').value.trim(); if(!id)return;
  if(!confirm('Spieler '+id+' bannen?'))return;
  document.getElementById('wlmsg').textContent=await api('/api/ban?id='+encodeURIComponent(id),{method:'POST'});
  document.getElementById('pid').value=''; loadWl();
}
async function unbanId(id){
  document.getElementById('wlmsg').textContent=await api('/api/unban?id='+encodeURIComponent(id),{method:'POST'});
  loadWl();
}
async function loadMods(){
  try{
    const d=JSON.parse(await api('/api/mods'));
    document.getElementById('modsize').textContent=d.size_mb?(d.size_mb>=1024?(d.size_mb/1024).toFixed(1)+' GB':d.size_mb+' MB')+' '+L['mods.size_on_disk']:'';
    const active=(d.active||[]), inactive=(d.inactive||[]);
    document.getElementById('mods').innerHTML =
      `<div class="meta" style="margin:6px 0 2px">${L['mods.active']} (${active.length})</div>` +
      (active.length?active.map(m=>modRow(m,true)).join(''):'<span style="color:var(--dim)">– '+L['mods.none_active']+' –</span>') +
      `<div class="meta" style="margin:14px 0 2px">${L['mods.inactive']} (${inactive.length})</div>` +
      (inactive.length?inactive.map(m=>modRow(m,false)).join(''):'<span style="color:var(--dim)">– '+L['mods.none_inactive']+' –</span>');
    if((d.missing_meta||[]).length && !META_BUSY){
      META_BUSY=true;
      api('/api/mods/refresh',{method:'POST'}).then(()=>{META_BUSY=false; loadMods();}).catch(()=>{META_BUSY=false;});
    }
  }catch(e){}
}
let META_BUSY=false;
async function enableMod(id){
  document.getElementById('modout').textContent=await api('/api/mods/add?id='+id,{method:'POST'});
  loadMods();
}


let _suggTimer=null;
function suggestMods(){
  clearTimeout(_suggTimer);
  const q=document.getElementById('modid').value.trim();
  const box=document.getElementById('modhits');
  if(q.length<2){ box.innerHTML=''; return; }
  _suggTimer=setTimeout(async()=>{
    let data;
    try{ data=JSON.parse(await api('/api/mods/suggest?q='+encodeURIComponent(q))); }
    catch(e){ return; }
    const hits=(data.results||[]).slice(0,8);
    if(!hits.length){
      box.innerHTML='<div class="meta">'+L['mods.search_empty']+
        (data.needs_key?(' · <a href="https://console.curseforge.com" target="_blank">'+L['mods.key']+'</a>'):'')+'</div>';
      return;
    }
    box.innerHTML=hits.map(m=>`<div class="p" style="cursor:pointer" onclick="addModId('${m.id}')">
        <span class="mrow">
          ${m.thumbnail?`<img class="thumb" src="${m.thumbnail}" alt="" loading="lazy">`:'<div class="thumb"></div>'}
          <span class="txt"><b>${m.title||('Mod '+m.id)}</b>
          <small>${m.id}${m.downloads?(' · '+m.downloads.toLocaleString('de-DE')):''}${m.summary?(' · '+m.summary.slice(0,80)):''}</small></span>
        </span>
        <span class="row"><span class="badge">+</span></span></div>`).join('');
  }, 350);
}
async function searchMods(){
  const q=document.getElementById('modid').value.trim();
  const box=document.getElementById('modhits');
  if(!q){ box.innerHTML=''; return; }
  box.innerHTML='<div class="meta">'+L['common.loading']+'</div>';
  let data;
  try{ data=JSON.parse(await api('/api/mods/search?q='+encodeURIComponent(q))); }
  catch(e){ box.innerHTML='<div class="meta">'+L['mods.search_failed']+'</div>'; return; }
  const hits=(data.results||[]);
  if(!hits.length){
    box.innerHTML='<div class="meta">'+L['mods.search_empty']+
      (data.needs_key?(' · <a href="https://console.curseforge.com" target="_blank">'+L['mods.key']+'</a>'):'')+'</div>';
    return;
  }
  box.innerHTML=hits.map(m=>`<div class="p"><span class="mrow">
      ${m.thumbnail?`<img class="thumb" src="${m.thumbnail}" alt="" loading="lazy">`:'<div class="thumb"></div>'}
      <span class="txt"><b>${m.title||('Mod '+m.id)}</b>
      <small>${m.id}${m.downloads?(' · '+m.downloads.toLocaleString('de-DE')+' Downloads'):''}${m.summary?(' · '+m.summary.slice(0,90)):''}</small></span></span>
      <span class="row"><button class="primary" onclick="addModId('${m.id}')">${L['mods.add_hit']}</button></span></div>`).join('');
}
async function addModId(id){
  const out=document.getElementById('modout');
  out.textContent=await api('/api/mods/add?id='+encodeURIComponent(id),{method:'POST'});
  loadMods();
}
async function loadKeyState(){
  const el=document.getElementById('keystate'); if(!el) return;
  try{
    const d=JSON.parse(await api('/api/mods/key'));
    el.textContent = d.has_key ? (L['mods.key_on']+(d.masked?(' · '+d.masked):'')) : L['mods.key_off'];
    el.style.color = d.has_key ? 'var(--ok,#3ecf8e)' : '';
  }catch(e){ el.textContent=''; }
}
async function saveKey(){
  const v=document.getElementById('cfkey').value.trim();
  try{ await api('/api/mods/key?key='+encodeURIComponent(v),{method:'POST'});
       document.getElementById('cfkeymsg').textContent=L['notify.saved'];
       document.getElementById('cfkey').value=''; loadKeyState(); }
  catch(e){ document.getElementById('cfkeymsg').textContent=L['notify.failed']; }
}
async function addMod(){
  const id=document.getElementById('modid').value.trim(); if(!/^[0-9]+$/.test(id)){alert('nur Zahlen');return;}
  document.getElementById('modout').textContent=await api('/api/mods/add?id='+id,{method:'POST'});
  document.getElementById('modid').value=''; loadMods();
}
async function delMod(id){
  if(!confirm('Mod '+id+' aus der Liste entfernen?'))return;
  document.getElementById('modout').textContent=await api('/api/mods/remove?id='+id,{method:'POST'});
  loadMods();
}
async function delModFiles(id){
  if(!confirm('Heruntergeladene Dateien von Mod '+id+' loeschen?'))return;
  document.getElementById('modout').textContent=await api('/api/mods/delete-files?id='+id,{method:'POST'});
  loadMods();
}
async function loadCfg(){
  const f=document.getElementById('cfgfile').value;
  document.getElementById('cfgtext').value=await api('/api/config?file='+f);
  document.getElementById('cfgmsg').textContent='';
}
async function saveCfg(){
  const f=document.getElementById('cfgfile').value;
  const t=document.getElementById('cfgtext').value;
  const r=await fetch('/api/config?file='+f+'&name='+NAME+'&token='+encodeURIComponent(T),
    {method:'POST',body:t});
  document.getElementById('cfgmsg').textContent=await r.text();
}
async function loadSnaps(){
  try{
    const list=JSON.parse(await api('/api/snapshots'));
    document.getElementById('snaps').innerHTML=list.length?list.map(x=>
      `<div class="p"><span><b>${x.mtime}</b><br><small>${x.name} · ${x.size_gb} GB</small></span>
       <span class="row">
         <button onclick="restoreSnap('${x.name}')">${L['snap.restore']}</button>
         <button class="danger" onclick="delSnap('${x.name}')">${L['common.delete']}</button>
       </span></div>`).join(''):'<span style="color:var(--dim)">– kein Snapshot vorhanden –</span>';
  }catch(e){}
}
async function makeSnap(){
  document.getElementById('snapmsg').textContent='kopiert … (kann 1–2 Minuten dauern)';
  document.getElementById('snapmsg').textContent=await api('/api/snapshot',{method:'POST'});
  loadSnaps();
}
async function restoreSnap(name){
  if(!confirm(L['msg.confirm_snapshot']))return;
  document.getElementById('snapmsg').textContent='spielt zurück …';
  document.getElementById('snapmsg').textContent=await api('/api/snapshot/restore?file='+encodeURIComponent(name),{method:'POST'});
  setTimeout(refresh,3000);
}
async function delSnap(name){
  if(!confirm('Snapshot '+name+' löschen?'))return;
  document.getElementById('snapmsg').textContent=await api('/api/snapshot/delete?file='+encodeURIComponent(name),{method:'POST'});
  loadSnaps();
}
async function loadBackups(){
  try{
    const list=JSON.parse(await api('/api/backups'));
    document.getElementById('backups').innerHTML=list.length?list.slice(0,8).map(b=>
      `<div class="p"><span><b>${b.mtime} · ${L['bk.kind_'+({manuell:'manual',geplant:'auto','vor Restore':'pre_restore','älter':'old'}[b.kind]||'old')]}</b><br><small>${b.file} · ${b.size_mb} MB</small></span>
       <span class="row">
         <button onclick="restoreBk('${b.file}')">${L['bk.restore']}</button>
         <button class="danger" onclick="delBk('${b.file}')">${L['common.delete']}</button>
       </span></div>`).join(''):'<span style="color:var(--dim)">– '+L['bk.none']+' –</span>';
  }catch(e){}
}
async function makeBackup(){
  document.getElementById('bkmsg').textContent='sichert …';
  document.getElementById('bkmsg').textContent=await api('/api/backup',{method:'POST'});
  loadBackups();
}
async function restoreBk(f){
  if(!confirm(L['msg.confirm_restore']))return;
  document.getElementById('bkmsg').textContent='spielt ein …';
  document.getElementById('bkmsg').textContent=await api('/api/backup/restore?file='+encodeURIComponent(f),{method:'POST'});
  setTimeout(refresh,3000);
}
async function delBk(f){
  if(!confirm('Backup '+f+' löschen?'))return;
  document.getElementById('bkmsg').textContent=await api('/api/backup/delete?file='+encodeURIComponent(f),{method:'POST'});
  loadBackups();
}

async function loadHooks(){
  try{ const d=JSON.parse(await api('/api/webhook')); document.getElementById('hookurl').value=d.url||''; }catch(e){}
}
async function saveHook(){
  const url=document.getElementById('hookurl').value.trim();
  try{ await api('/api/webhook?url='+encodeURIComponent(url),{method:'POST'});
       document.getElementById('hookmsg').textContent=L['notify.saved']; }
  catch(e){ document.getElementById('hookmsg').textContent=L['notify.failed']; }
}
async function testHook(){
  const url=document.getElementById('hookurl').value.trim();
  const msg=document.getElementById('hookmsg');
  msg.textContent='…';
  try{ const r=JSON.parse(await api('/api/notify/test?url='+encodeURIComponent(url),{method:'POST'}));
       msg.textContent = r.ok ? L['notify.test_ok'] : (L['notify.test_fail']+': '+r.error); }
  catch(e){ msg.textContent=L['notify.test_fail']; }
}
async function loadSchedule(){
  const s=JSON.parse(await api('/api/schedule'));
  document.getElementById('schedRestart').value=(s.restart_times||[]).join(',');
  document.getElementById('schedBackup').value=(s.backup_times||[]).join(',');
  document.getElementById('schedWarn').value=s.warn_minutes;
  document.getElementById('schedKeep').value=s.backups_keep;
}
async function saveSchedule(){
  const p=new URLSearchParams({restart:document.getElementById('schedRestart').value,
    backup:document.getElementById('schedBackup').value,
    warn:document.getElementById('schedWarn').value,
    keep:document.getElementById('schedKeep').value});
  document.getElementById('schedmsg').textContent=await api('/api/schedule?'+p.toString(),{method:'POST'});
}
async function pa(sid,action){ if(!confirm(action+' für '+sid+'?'))return;
  document.getElementById('out').textContent=await api('/api/player/action?steamid='+sid+'&action='+action,{method:'POST'});
  setTimeout(refresh,1500); }
async function give(sid){ const bp=prompt('Blueprint','PrimalItemResource_Stone_C'); if(!bp)return;
  const q=prompt('Menge','10')||'10';
  document.getElementById('out').textContent=await api('/api/player/give?steamid='+sid+'&bp='+encodeURIComponent(bp)+'&qty='+q,{method:'POST'}); }
applyLang(); restoreTab(); setTimeout(restoreTab, 250); refresh(); updCheck(); renderCmds(); loadMods(); loadKeyState(); loadCfg(); loadWl(); loadSettings(); loadSnaps(); loadBackups(); loadSchedule(); loadHooks();
setInterval(refresh,5000); setInterval(updCheck,60000);
</script><footer style="text-align:center;padding:16px 0 10px;font-size:11.5px;color:var(--dim);
letter-spacing:.04em">noah __VERSION__ · © 2026 Ronny H.</footer>
</body></html>"""

PLAYER_ACTIONS = {
    "kick": "KickPlayer %s",
    "ban": "BanPlayer %s",
    "unban": "UnbanPlayer %s",
    "whitelist": "AllowPlayerToJoinNoCheck %s",
    "unwhitelist": "DisallowPlayerToJoinNoCheck %s",
}


def _start_install(inst: Instance) -> None:
    """Installation im Hintergrund ueber den gemeinsamen Installer."""
    from . import installer
    INSTALLS[inst.name] = {"log": os.path.join(inst.directory, ".install.log"),
                           "started": time.time()}

    def run() -> None:
        try:
            result = installer.install_server(inst)
            # Dienst gleich mit anlegen: Ueberwachung und Autostart ohne Handarbeit
            if result.get("ok"):
                from . import units
                u = units.install(inst)
                try:
                    with open(os.path.join(inst.directory, ".install.log"), "a") as fh:
                        if u.get("ok"):
                            fh.write("Dienst eingerichtet: %s (%s)\n"
                                     % (u["path"], "System" if u["system"] else "Benutzer"))
                        else:
                            fh.write("Dienst konnte nicht eingerichtet werden: %s\n"
                                     % (u.get("error") or u.get("message")))
                except OSError:
                    pass
        except Exception as exc:  # noqa: BLE001
            try:
                with open(os.path.join(inst.directory, ".install.log"), "a") as fh:
                    fh.write("Fehler: %s\n" % exc)
            except OSError:
                pass
        finally:
            INSTALLS.pop(inst.name, None)

    threading.Thread(target=run, daemon=True).start()


class Handler(BaseHTTPRequestHandler):
    server_version = "noah"

    def _auth(self) -> bool:
        q = urllib.parse.urlparse(self.path).query
        tok = urllib.parse.parse_qs(q).get("token", [""])[0] or self.headers.get("X-Token", "")
        return hmac.compare_digest(tok, token())

    def end_headers(self) -> None:
        """Sicherheits-Header auf jeder Antwort."""
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; "
                         "script-src 'self' 'unsafe-inline'; connect-src 'self'")
        super().end_headers()

    def _send(self, code: int, body: bytes, ctype: str = "text/plain; charset=utf-8") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data) -> None:
        self._send(200, json.dumps(data, ensure_ascii=False).encode(), "application/json")

    def _html(self, text: str) -> None:
        self._send(200, text.encode(), "text/html; charset=utf-8")

    def _inst(self, q: dict) -> Instance | None:
        name = q.get("name", [""])[0]
        if not name:
            parts = urllib.parse.urlparse(self.path).path.strip("/").split("/")
            if len(parts) == 2 and parts[0] == "i":
                name = parts[1]
        if not name:
            known = registry.names()
            name = known[0] if known else ""
        try:
            return registry.load(name) if name else None
        except TypeError:
            return None

    def log_message(self, *_args) -> None:
        pass

    # ------------------------------------------------------------------ GET
    def do_GET(self) -> None:  # noqa: N802
        if not self._auth():
            self._send(401, b"token fehlt")
            return
        u = urllib.parse.urlparse(self.path)
        path, q = u.path, urllib.parse.parse_qs(u.query)
        tok = q.get("token", [""])[0]

        if path == "/":
            maps = "".join('<option value="%s">%s</option>' % (m, l) for m, l in registry.MAPS)
            self._html(_render(DASH.replace("__MAPS__", maps)))
            return
        if path.startswith("/i/"):
            inst = self._inst(q)
            if not inst:
                self._send(404, b"Instanz nicht gefunden")
                return
            self._html(_render(INST.replace("__NAME__", inst.name).replace("__TOK__", tok)))
            return

        if path.startswith("/static/maps/"):
            name = os.path.basename(path)
            base = os.path.expanduser("~/.config/noah/static/maps")
            full = os.path.join(base, name)
            if not name.endswith(".jpg") or not os.path.isfile(full):
                self._send(404, b"kein Bild")
                return
            with open(full, "rb") as fh:
                blob = fh.read()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Content-Length", str(len(blob)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(blob)
            return
        if path == "/api/host":
            self._json(metrics.host())
            return
        if path == "/api/selfupdate":
            from . import selfupdate
            self._json(selfupdate.check())
            return
        if path == "/api/changelog":
            from . import selfupdate
            self._json(selfupdate.changelog(i18n.lang()))
            return
        if path == "/api/selfupdate/notes":
            from . import selfupdate
            self._json(selfupdate.notes(q.get("v", [""])[0]))
            return

        if path == "/api/instances":
            out = []
            for name in registry.names():
                obj = registry.load(name)
                if obj:
                    out.append(registry.info(obj))
            self._json(out)
            return

        # Mods: Suche und Key-Status brauchen keine Instanz
        if path == "/api/mods/search":
            term = q.get("q", [""])[0]
            key = modlib._api_key()
            self._json({"results": modlib.search(term, limit=10),
                        "needs_key": not bool(key), "has_key": bool(key)})
            return
        if path == "/api/mods/suggest":
            self._json(modlib.suggest(q.get("q", [""])[0]))
            return
        if path == "/api/mods/key":
            key = modlib._api_key()
            self._json({"has_key": bool(key),
                        "masked": (key[:3] + "…" + key[-3:]) if len(key) > 8 else ""})
            return

        inst = self._inst(q)
        if path == "/api/install/log":
            if not inst:
                self._send(404, b"keine Instanz")
                return
            log_path = os.path.join(inst.directory, ".install.log")
            state = "laeuft" if inst.name in INSTALLS else "fertig"
            lines = runner.tail(log_path, 10) if os.path.exists(log_path) else []
            self._send(200, ("[%s]\n" % state + "\n".join(lines)).encode())
            return
        if not inst:
            self._send(404, b"keine Instanz")
            return

        if path == "/api/status":
            self._json(runner.status(inst))
        elif path == "/api/logs":
            self._send(200, "\n".join(runner.tail(inst.log_path, int(q.get("n", ["30"])[0]))).encode())
        elif path == "/api/console":
            self._send(200, "\n".join(runner.tail_console(inst, int(q.get("n", ["40"])[0]))).encode())
        elif path == "/api/players":
            self._json(players(inst))
        elif path == "/api/update":
            self._json(runner.check_update(inst))
        elif path == "/api/lang":
            self._json({"lang": i18n.lang(), "catalog": i18n.catalog()})

        elif path == "/api/webhook":
            self._json({"url": inst.webhook_url if inst else "", "log": notify_mod.log_path(inst) if inst else ""})
        elif path == "/api/commands":
            self._json([i18n.command(c) for c in cmdreg.COMMANDS])
        elif path == "/api/mods":
            data = modlib.list_all_enriched(inst)
            data["size_mb"] = modlib.mod_size_mb(inst)
            self._json(data)
        elif path == "/api/config":
            which = q.get("file", ["gus"])[0]
            self._send(200, cfgfile.read(inst, which).encode())
        elif path == "/api/mod/meta":
            self._json(modlib.meta(q.get("id", [""])[0], force=q.get("force", [""])[0] == "1"))
        elif path == "/api/whitelist":
            self._json(wl.info(inst))
        elif path == "/api/bans":
            self._json({"bans": wl.bans(inst)})
        elif path == "/api/snapshots":
            self._json(snap.listing(inst))
        elif path == "/api/settings":
            self._json(cfgfile.read_values(inst))
        elif path == "/api/backups":
            self._json(bk.listing(inst))
        elif path == "/api/schedule":
            self._json({
                "restart_times": inst.restart_times,
                "backup_times": inst.backup_times,
                "warn_minutes": inst.warn_minutes,
                "backups_keep": inst.backups_keep,
            })
        elif path == "/api/config/known":
            self._json(cfgfile.known_for(q.get("file", ["gus"])[0]))
        else:
            self._send(404, b"unbekannt")

    # ------------------------------------------------------------------ POST
    def do_POST(self) -> None:  # noqa: N802
        if not self._auth():
            self._send(401, b"token fehlt")
            return
        u = urllib.parse.urlparse(self.path)
        path, q = u.path, urllib.parse.parse_qs(u.query)

        if path == "/api/selfupdate":
            from . import selfupdate

            def run_update() -> None:
                result = selfupdate.apply()
                if result.get("ok"):
                    selfupdate.restart_service()

            threading.Thread(target=run_update, daemon=True).start()
            self._json({"ok": True, "started": True})
            return

        if path == "/api/instances":
            port = q.get("port", [""])[0]
            try:
                inst = registry.create(
                    q.get("name", [""])[0].strip(),
                    q.get("map", ["Ragnarok_WP"])[0],
                    int(port) if port.isdigit() else None,
                    q.get("session", [""])[0],
                )
            except (ValueError, RuntimeError) as exc:
                self._send(200, ("Fehler: %s" % exc).encode())
                return
            inst.write_ini()
            self._send(200, ("Instanz '%s' angelegt - Port %d, RCON %d\nJetzt 'Installieren' druecken."
                             % (inst.name, inst.port, inst.rcon_port)).encode())
            return

        if path == "/api/mods/key":
            i18n.put("curseforge_key", q.get("key", [""])[0].strip())
            self._send(200, b"ok")
            return

        inst = self._inst(q)
        if not inst:
            self._send(404, b"keine Instanz")
            return

        if path == "/api/install":
            if inst.name in INSTALLS:
                self._send(200, b"Installation laeuft bereits")
                return
            _start_install(inst)
            self._send(200, ("Installation gestartet: %s\nDauer je nach Leitung 10-30 Minuten."
                             % inst.directory).encode())
        elif path == "/api/start":
            if runner.is_running(inst):
                self._json({"ok": True, "info": "laeuft bereits"})
            else:
                threading.Thread(target=runner.start, args=(inst,), daemon=True).start()
                self._json({"ok": True, "info": "start ausgeloest"})
        elif path == "/api/stop":
            threading.Thread(target=runner.stop, args=(inst,), daemon=True).start()
            self._json({"ok": True, "info": "stop ausgeloest"})
        elif path == "/api/restart":
            def _r() -> None:
                runner.stop(inst, timeout=90)
                time.sleep(3)
                runner.start(inst)
            threading.Thread(target=_r, daemon=True).start()
            self._json({"ok": True, "info": "restart ausgeloest"})
        elif path == "/api/update":
            if not inst:
                self._json({"ok": False, "error": "Instanz nicht gefunden"})
                return
            threading.Thread(target=runner.update_installed, args=(inst,), daemon=True).start()
            self._json({"ok": True, "info": "Update gestartet"})
        elif path == "/api/rcon":
            cmd = q.get("cmd", [""])[0]
            try:
                self._send(200, (rcon_cmd(inst, cmd) or "(keine Antwort)").encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("RCON-Fehler: %s" % exc).encode())
        elif path == "/api/whitelist/add":
            try:
                wl.add_to_whitelist(inst, q.get("id", [""])[0])
                self._send(200, ("%s auf die Whitelist gesetzt" % q.get("id", [""])[0]).encode())
            except ValueError as exc:
                self._send(200, ("Fehler: %s" % exc).encode())
        elif path == "/api/whitelist/remove":
            try:
                wl.remove_from_whitelist(inst, q.get("id", [""])[0])
                self._send(200, ("%s von der Whitelist entfernt" % q.get("id", [""])[0]).encode())
            except ValueError as exc:
                self._send(200, ("Fehler: %s" % exc).encode())
        elif path == "/api/whitelist/enable":
            on = q.get("on", ["0"])[0] == "1"
            wl.set_enabled(inst, on)
            self._send(200, ("Whitelist %s - Neustart noetig" % ("AN" if on else "AUS")).encode())
        elif path == "/api/ban":
            pid = q.get("id", [""])[0]
            try:
                out = rcon_cmd(inst, "BanPlayer %s" % pid)
                wl.record_ban(inst, pid)
                self._send(200, ("%s: %s" % (pid, out or "gebannt")).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("RCON-Fehler: %s" % exc).encode())
        elif path == "/api/unban":
            pid = q.get("id", [""])[0]
            try:
                out = rcon_cmd(inst, "UnbanPlayer %s" % pid)
                wl.forget_ban(inst, pid)
                self._send(200, ("%s: %s" % (pid, out or "entbannt")).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("RCON-Fehler: %s" % exc).encode())
        elif path == "/api/webhook":
            url = q.get("url", [""])[0].strip()
            if url and not url.startswith("https://"):
                self._send(400, b"Webhook muss mit https:// beginnen")
                return
            inst.webhook_url = url
            registry.save(inst)
            self._send(200, ("ok").encode())
            return
        elif path == "/api/instance/delete":
            files = q.get("files", ["0"])[0] in ("1", "true", "yes")
            if runner.is_running(inst):
                runner.stop(inst, timeout=90)
            try:
                result = registry.forget(inst.name, delete_files=files)
            except Exception as exc:  # noqa: BLE001
                self._json({"ok": False, "error": str(exc)[:200]})
                return
            self._json(result)
            return
        elif path == "/api/notify/test":
            url = q.get("url", [""])[0].strip() or inst.webhook_url
            result = notify_mod.test(inst, url)
            self._json(result)
            return
        elif path == "/api/mods/refresh":
            ids = [m["id"] for m in modlib.list_all(inst)["active"] + modlib.list_all(inst)["inactive"]]
            self._json(modlib.refresh_meta(ids))
        elif path == "/api/mods/add":
            try:
                modlib.add_mod(inst, q.get("id", [""])[0])
                self._send(200, ("Mod %s eingetragen. Server neu starten, damit er sie laedt."
                                 % q.get("id", [""])[0]).encode())
            except ValueError as exc:
                self._send(200, ("Fehler: %s" % exc).encode())
        elif path == "/api/mods/remove":
            modlib.remove_mod(inst, q.get("id", [""])[0])
            self._send(200, ("Mod %s aus der Liste entfernt." % q.get("id", [""])[0]).encode())
        elif path == "/api/mods/delete-files":
            ok = modlib.remove_folder(inst, q.get("id", [""])[0])
            self._send(200, (("Dateien geloescht." if ok else "Keine Dateien gefunden.")).encode())
        elif path == "/api/snapshot":
            try:
                info = snap.create(inst)
                self._send(200, ("Snapshot erstellt: %s (%.1f GB)" % (info["name"], info["size_gb"])).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("Snapshot-Fehler: %s" % exc).encode())
        elif path == "/api/snapshot/restore":
            try:
                snapname = q.get("file", [""])[0] or q.get("snap", [""])[0]
                self._send(200, snap.restore(inst, snapname).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("Restore-Fehler: %s" % exc).encode())
        elif path == "/api/snapshot/delete":
            ok = snap.delete(inst, q.get("file", [""])[0] or q.get("snap", [""])[0])
            self._send(200, (("geloescht" if ok else "nicht gefunden")).encode())
        elif path == "/api/settings":
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length).decode("utf-8", "replace") if length else "[]"
            try:
                items = json.loads(raw)
            except ValueError:
                items = []
            changed = 0
            for item in items:
                try:
                    cfgfile.set_value(inst, item["file"], item["section"], item["key"],
                                      str(item.get("value", "")))
                    changed += 1
                except (KeyError, TypeError):
                    continue
            self._send(200, ("%d Einstellung(en) gespeichert - wirksam nach Neustart"
                             % changed).encode())
        elif path == "/api/backup":
            try:
                info = bk.create(inst)
                self._send(200, ("Backup erstellt: %s (%.1f MB)" % (info["file"], info["size_mb"])).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("Backup-Fehler: %s" % exc).encode())
        elif path == "/api/backup/restore":
            fname = q.get("file", [""])[0]
            try:
                self._send(200, bk.restore(inst, fname).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("Restore-Fehler: %s" % exc).encode())
        elif path == "/api/backup/delete":
            ok = bk.delete(inst, q.get("file", [""])[0])
            self._send(200, (("geloescht" if ok else "nicht gefunden")).encode())
        elif path == "/api/schedule":
            def _times(key: str) -> list[str]:
                raw = q.get(key, [""])[0]
                return [t.strip() for t in raw.split(",") if t.strip()]
            if "restart" in q:
                inst.restart_times = _times("restart")
            if "backup" in q:
                inst.backup_times = _times("backup")
            if "warn" in q and q["warn"][0].isdigit():
                inst.warn_minutes = int(q["warn"][0])
            if "keep" in q and q["keep"][0].isdigit():
                inst.backups_keep = int(q["keep"][0])
            registry.save(inst)
            self._send(200, ("Zeitplan gespeichert: Neustart %s | Backup %s | Vorwarnung %d min"
                             % (", ".join(inst.restart_times) or "-",
                                ", ".join(inst.backup_times) or "-", inst.warn_minutes)).encode())
        elif path == "/api/config":
            which = q.get("file", ["gus"])[0]
            length = int(self.headers.get("Content-Length") or 0)
            text = self.rfile.read(length).decode("utf-8", "replace") if length else ""
            try:
                backup = cfgfile.write(inst, which, text)
                self._send(200, ("gespeichert%s" % ((" (Sicherung: %s)" % os.path.basename(backup))
                                                   if backup else "")).encode())
            except ValueError as exc:
                self._send(200, ("Fehler: %s" % exc).encode())
        elif path == "/api/lang":
            value = q.get("set", [""])[0].lower()
            try:
                i18n.set_lang(value)
                self._send(200, ("lang=%s" % value).encode())
            except ValueError:
                self._send(400, b"unbekannte Sprache")
        elif path == "/api/command":
            entry = cmdreg.by_id(q.get("id", [""])[0])
            if not entry:
                self._send(400, b"unbekannter Befehl")
                return
            values = {name: q.get(name, [""])[0] for name, _qq, _dd in entry["args"]}
            cmd = cmdreg.build(entry["id"], values) or ""
            try:
                out = rcon_cmd(inst, cmd)
                self._send(200, ("$ %s\n%s" % (cmd, out or "(keine Antwort)")).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("$ %s\nRCON-Fehler: %s" % (cmd, exc)).encode())
        elif path == "/api/player/action":
            steamid = q.get("steamid", [""])[0]
            tpl = PLAYER_ACTIONS.get(q.get("action", [""])[0])
            if not steamid or not tpl:
                self._send(400, b"steamid/action fehlt")
                return
            try:
                self._send(200, (rcon_cmd(inst, tpl % steamid) or "ok").encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("RCON-Fehler: %s" % exc).encode())
        elif path == "/api/player/give":
            steamid = q.get("steamid", [""])[0]
            bp = q.get("bp", [""])[0]
            qty = q.get("qty", ["1"])[0]
            if not steamid or not bp:
                self._send(400, b"steamid/bp fehlt")
                return
            try:
                self._send(200, rcon_cmd(inst, "GiveItemToPlayer %s %s %s 0 0" % (steamid, bp, qty)).encode())
            except Exception as exc:  # noqa: BLE001
                self._send(200, ("RCON-Fehler: %s" % exc).encode())
        else:
            self._send(404, b"unbekannt")


def serve(host: str = "127.0.0.1", port: int = 8790,
          cert: str = "", key: str = "") -> None:
    srv = ThreadingHTTPServer((host, port), Handler)
    scheme = "http"
    if cert and key:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
        scheme = "https"
    print("noah UI: %s://%s:%d/?token=%s" % (scheme, host, port, token()), flush=True)
    srv.serve_forever()
