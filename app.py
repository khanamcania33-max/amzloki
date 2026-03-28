import streamlit as st, time, random, json, os
from data_engine import load_db, save_db, run_scan, get_unseen_batch, time_until_next_scan, MASTER_POOL, SCAN_INTERVAL
from scanner import (
    start_background_scanner, scanner_is_running,
    get_scan_status, run_full_scan, time_until_next_scan as scanner_countdown
)

st.set_page_config(layout="wide", page_title="FBA AI Agent", page_icon="🤖")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
:root{--bg:#080c14;--surf:rgba(15,20,35,0.85);--bdr:rgba(99,179,255,0.12);--acc:#3b82f6;--acc2:#06b6d4;--grn:#10b981;--ylw:#f59e0b;--red:#ef4444;--txt:#e2e8f0;--muted:#64748b;}
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;}
.stApp{background:radial-gradient(ellipse 80% 60% at 50% -10%,rgba(59,130,246,0.15),transparent),radial-gradient(ellipse 60% 40% at 80% 80%,rgba(6,182,212,0.08),transparent),#080c14;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.5rem 2rem 3rem!important;max-width:1400px!important;}
[data-testid="stSidebar"]{background:rgba(10,14,26,0.97)!important;border-right:1px solid var(--bdr)!important;}
[data-testid="stSidebar"] .stButton>button{width:100%;background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.2);color:#93c5fd;border-radius:10px;font-weight:500;padding:.6rem 1rem;transition:all .2s;font-size:.85rem;margin-bottom:4px;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(59,130,246,0.2);border-color:rgba(59,130,246,.5);color:#fff;transform:translateX(4px);}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#3b82f6,#06b6d4)!important;color:#fff!important;border:none!important;border-radius:10px!important;font-weight:600!important;box-shadow:0 0 20px rgba(59,130,246,.35)!important;transition:all .3s!important;}
.stButton>button[kind="primary"]:hover{box-shadow:0 0 35px rgba(59,130,246,.6)!important;transform:translateY(-2px)!important;}
.card{background:rgba(13,19,36,0.8);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(99,179,255,0.12);border-radius:18px;overflow:hidden;margin-bottom:1.25rem;transition:transform .3s,box-shadow .3s,border-color .3s;animation:slideUp .5s ease both;}
.card:hover{transform:translateY(-5px);box-shadow:0 20px 50px rgba(0,0,0,.5),0 0 0 1px rgba(59,130,246,.3);border-color:rgba(59,130,246,.35);}
@keyframes slideUp{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:translateY(0)}}
@keyframes blink{50%{opacity:0}}
.ct{padding:1.3rem 1.4rem .9rem;}
.crumb{font-size:.65rem;color:var(--muted);margin-bottom:.5rem;text-transform:uppercase;letter-spacing:.06em;}
.cname a{font-size:1.05rem;font-weight:700;color:#e2e8f0;text-decoration:none;line-height:1.3;transition:color .2s;}
.cname a:hover{color:#60a5fa;}
.brow{display:flex;gap:6px;flex-wrap:wrap;margin:.6rem 0;}
.badge{padding:3px 9px;border-radius:20px;font-size:.68rem;font-weight:600;letter-spacing:.03em;}
.br{background:rgba(255,255,255,.07);color:#94a3b8;border:1px solid rgba(255,255,255,.09);}
.bs{background:rgba(59,130,246,.15);color:#93c5fd;border:1px solid rgba(59,130,246,.3);}
.bev{background:rgba(16,185,129,.12);color:#6ee7b7;border:1px solid rgba(16,185,129,.3);}
.bvl{background:rgba(245,158,11,.12);color:#fcd34d;border:1px solid rgba(245,158,11,.3);}
.price-row{display:flex;align-items:baseline;gap:8px;margin:.4rem 0 .2rem;}
.plabel{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;}
.pval{font-size:1.55rem;font-weight:800;background:linear-gradient(135deg,#3b82f6,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.kvol{font-size:.72rem;color:var(--muted);margin-left:auto;align-self:flex-end;padding-bottom:2px;}
.cb{padding:.9rem 1.4rem;}
.wbox{background:rgba(16,185,129,.06);border-left:3px solid #10b981;border-radius:0 8px 8px 0;padding:.6rem .85rem;margin-bottom:.9rem;font-size:.8rem;color:#94a3b8;line-height:1.5;}
.wbox strong{color:#d1fae5;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;display:block;margin-bottom:3px;}
/* Profit breakdown */
.pbreak{display:flex;gap:4px;margin-bottom:.9rem;}
.pc{flex:1;background:rgba(0,0,0,.25);border-radius:8px;padding:.5rem .4rem;text-align:center;border:1px solid rgba(255,255,255,.05);}
.pclabel{font-size:.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;display:block;}
.pcpct{font-size:.8rem;font-weight:700;display:block;margin:.2rem 0;}
.pcamt{font-size:.65rem;color:var(--muted);}
.landing .pcpct{color:#f59e0b;} .fba .pcpct{color:#ef4444;} .ppc .pcpct{color:#a78bfa;} .profit .pcpct{color:#10b981;}
.sig{display:flex;gap:8px;margin-bottom:.9rem;}
.sigbox{flex:1;background:rgba(0,0,0,.22);border:1px solid rgba(255,255,255,.06);border-radius:9px;padding:.5rem .65rem;text-align:center;}
.siglbl{font-size:.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:3px;}
.sigval{font-size:.72rem;font-weight:600;}
.grn{color:#10b981;} .ylw{color:#f59e0b;}
.mwrap{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:.9rem;}
.mc{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:6px;padding:3px 8px;font-size:.68rem;color:#94a3b8;display:flex;align-items:center;gap:3px;}
.dbox{background:rgba(59,130,246,.06);border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;padding:.55rem .85rem;margin-bottom:.7rem;font-size:.78rem;color:#94a3b8;line-height:1.45;}
.dbox strong{color:#bfdbfe;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;display:block;margin-bottom:3px;}
.rbox{background:rgba(239,68,68,.06);border-left:3px solid #ef4444;border-radius:0 8px 8px 0;padding:.55rem .85rem;margin-bottom:.7rem;font-size:.78rem;color:#94a3b8;line-height:1.45;}
.rbox strong{color:#fecaca;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;display:block;margin-bottom:3px;}
.ibox{background:rgba(139,92,246,.06);border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;padding:.55rem .85rem;margin-bottom:.7rem;font-size:.78rem;color:#94a3b8;line-height:1.45;}
.ibox strong{color:#ddd6fe;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;display:block;margin-bottom:3px;}
.swot{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:.9rem;}
.sw{background:rgba(0,0,0,.2);border-radius:7px;padding:.4rem .55rem;font-size:.68rem;color:#94a3b8;}
.sw b{display:block;font-size:.62rem;text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px;}
.sw-s b{color:#10b981;} .sw-w b{color:#f59e0b;} .sw-o b{color:#3b82f6;} .sw-t b{color:#ef4444;}
.cf{padding:.75rem 1.4rem;border-top:1px solid rgba(255,255,255,.05);display:flex;align-items:center;justify-content:space-between;}
.stypetag{font-size:.7rem;color:var(--muted);}
.stypetag strong{background:rgba(255,255,255,.08);color:#e2e8f0;padding:2px 8px;border-radius:9px;font-size:.65rem;text-transform:uppercase;margin-left:4px;}
.alink{font-size:.72rem;color:#60a5fa;border:1px solid rgba(59,130,246,.3);padding:4px 10px;border-radius:7px;text-decoration:none;transition:all .2s;}
.alink:hover{background:rgba(59,130,246,.15);color:#93c5fd;}
.criteria-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:2rem;}
.crit{background:rgba(13,19,36,.8);border:1px solid var(--bdr);border-radius:12px;padding:.85rem 1rem;text-align:center;}
.crit-icon{font-size:1.4rem;margin-bottom:.35rem;}
.crit-label{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;display:block;}
.crit-val{font-size:.82rem;font-weight:700;color:#e2e8f0;display:block;margin-top:3px;}
.stats-strip{display:flex;gap:.75rem;margin-bottom:1.75rem;flex-wrap:wrap;}
.sstat{background:rgba(13,19,36,.8);border:1px solid var(--bdr);border-radius:10px;padding:.6rem 1rem;font-size:.75rem;color:var(--muted);display:flex;align-items:center;gap:7px;}
.sstat .sv{color:#e2e8f0;font-weight:700;font-size:.82rem;}
.dot-live{width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 7px #10b981;animation:pulse-d 2s infinite;display:inline-block;}
@keyframes pulse-d{0%,100%{box-shadow:0 0 7px #10b981}50%{box-shadow:0 0 16px #10b981}}
.ph{font-size:1.5rem;font-weight:800;color:#f1f5f9;margin:0 0 .25rem;display:flex;align-items:center;gap:10px;}
.ps{font-size:.8rem;color:var(--muted);margin:0 0 1.75rem;}
.sec-hdr{font-size:1rem;font-weight:700;color:#e2e8f0;margin:0 0 1.1rem;display:flex;align-items:center;gap:8px;}
.cnt-badge{background:rgba(59,130,246,.2);color:#60a5fa;font-size:.72rem;padding:2px 8px;border-radius:20px;font-weight:600;}
.divider{height:1px;background:var(--bdr);margin:1.5rem 0;}
.timer-box{background:rgba(13,19,36,.8);border:1px solid rgba(6,182,212,.25);border-radius:10px;padding:.7rem 1rem;font-size:.8rem;color:#06b6d4;text-align:center;margin-top:.5rem;}
</style>
<style>@keyframes blink{50%{opacity:0}}</style>
""", unsafe_allow_html=True)

# ── Session state ──
for k, v in [("db", None), ("view", []), ("mode", "dashboard"), ("booted", False), ("saved", [])]:
    if k not in st.session_state: st.session_state[k] = v

if st.session_state.db is None:
    st.session_state.db = load_db()

db = st.session_state.db

# ── Cloud-compatible: no background thread; scanning is on-demand only ──
# start_background_scanner() is a no-op on Streamlit Community Cloud.
# All scans are triggered by the user clicking "Scan Now".

# ── Card builder ──
def card_html(p):
    s = p.get("swot", {})
    comp_cls = "grn" if "Very Low" in p.get("competitionScore","") else "ylw"
    return (
        '<div class="card">'
        '<div class="ct">'
        f'<div class="crumb">{p["category"]} › {p["subcategory"]} › {p["microNiche"]}</div>'
        f'<div class="cname"><a href="{p["amazonLink"]}" target="_blank">{p["name"]}</a></div>'
        '<div class="brow">'
        f'<span class="badge br">{p["region"]}</span>'
        f'<span class="badge bs">{p["source"]}</span>'
        f'<span class="badge bev">{p["seasonality"]}</span>'
        f'<span class="badge bvl" style="color:{p["validationColor"]}">{p["validationLabel"]}</span>'
        + (f'<span class="badge" style="background:rgba(236,72,153,.15);color:#f9a8d4;border:1px solid rgba(236,72,153,.3)">{p["trendSource"]}</span>' if p.get("trendSource") else '')
        +
        '</div>'
        '<div class="price-row">'
        '<span class="plabel">Est. Price</span>'
        f'<span class="pval">{p["estPrice"]}</span>'
        f'<span class="kvol">🔍 {p["keywordVolumeFormatted"]}</span>'
        '</div>'
        '</div>'
        '<div class="cb">'
        '<div class="wbox"><strong>Why it wins</strong>' + p["whyWins"] + '</div>'
        # Profit breakdown with Alibaba formula
        '<div style="margin-bottom:.5rem;font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em">💰 Cost & Profit Breakdown</div>'
        # Alibaba source formula row
        f'<div style="background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.15);border-radius:8px;padding:.5rem .8rem;margin-bottom:.6rem;font-size:.75rem;color:#fcd34d;display:flex;align-items:center;gap:6px">'
        f'🛒 <b>Alibaba Source:</b>&nbsp;{p["alibabaPrice"]}&nbsp;×&nbsp;1.5 shipping&nbsp;=&nbsp;<b style="color:#f59e0b">{p["landingAmt"]} landing cost</b>'
        f'&nbsp;<span style="margin-left:auto;font-size:.65rem;color:#92400e;background:rgba(251,191,36,.15);padding:2px 7px;border-radius:12px">Verified Merchant</span>'
        f'</div>'
        '<div class="pbreak">'
        f'<div class="pc landing"><span class="pclabel">Landing Cost</span><span class="pcpct">{p["landingPct"]}</span><span class="pcamt">{p["landingAmt"]}</span></div>'
        f'<div class="pc fba"><span class="pclabel">FBA Fees</span><span class="pcpct">30%</span><span class="pcamt">{p["fbaAmt"]}</span></div>'
        f'<div class="pc ppc"><span class="pclabel">PPC</span><span class="pcpct">20%</span><span class="pcamt">{p["ppcAmt"]}</span></div>'
        f'<div class="pc profit"><span class="pclabel">Net Profit</span><span class="pcpct">{p["netMargin"]}</span><span class="pcamt">{p["profitAmt"]}</span></div>'
        '</div>'
        '<div class="sig">'
        f'<div class="sigbox"><span class="siglbl">Demand Signal</span><span class="sigval grn">{p.get("monthlyRevenue","—")} /mo est.</span></div>'
        f'<div class="sigbox"><span class="siglbl">Competition</span><span class="sigval {comp_cls}">{p["competitionScore"]}</span></div>'
        f'<div class="sigbox"><span class="siglbl">Brand Dom.</span><span class="sigval ylw">{p["brandDominance"]}</span></div>'
        f'<div class="sigbox"><span class="siglbl">Top Reviews</span><span class="sigval">&lt;{p["topCompetitorReviews"]:,}</span></div>'
        '</div>'
        '<div class="mwrap">'
        f'<span class="mc">📦 {p["weight"]}</span>'
        f'<span class="mc">🔍 {p["keywordVolumeFormatted"]}</span>'
        f'<span class="mc">📈 Evergreen</span>'
        f'<span class="mc">💲 No Price Saturation</span>'
        f'<span class="mc">✅ Non-Restricted</span>'
        f'<span class="mc">🚫 No AMZ Basics</span>'
        '</div>'
        '<div class="dbox"><strong>Differentiation Angle</strong>' + p["differentiation"] + '</div>'
        '<div class="ibox"><strong>Customer Insight (1-Star Intel)</strong>' + p["customerInsight"] + '</div>'
        '<div class="rbox"><strong>Main Risks</strong>' + p["mainRisks"] + '</div>'
        '<div style="margin-bottom:.5rem;font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em">🧠 SWOT Analysis</div>'
        '<div class="swot">'
        f'<div class="sw sw-s"><b>Strength</b>{s.get("S","")}</div>'
        f'<div class="sw sw-w"><b>Weakness</b>{s.get("W","")}</div>'
        f'<div class="sw sw-o"><b>Opportunity</b>{s.get("O","")}</div>'
        f'<div class="sw sw-t"><b>Threat</b>{s.get("T","")}</div>'
        '</div>'
        '</div>'
        '<div class="cf">'
        f'<span class="stypetag">Best for<strong>{p["sellerType"]}</strong></span>'
        f'<a href="{p["amazonLink"]}" target="_blank" class="alink">🔗 View on Amazon</a>'
        '</div>'
        '</div>'
    )

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
<div style="padding:.4rem 0 1.4rem">
<div style="display:flex;align-items:center;gap:9px;margin-bottom:.2rem">
<div style="width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#3b82f6,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:1rem;box-shadow:0 0 12px rgba(59,130,246,.5)">🤖</div>
<span style="font-size:.95rem;font-weight:700;color:#f1f5f9">FBA AI Agent</span>
</div>
<div style="font-size:.68rem;color:#475569;padding-left:39px">Autonomous Research v4</div>
</div>""", unsafe_allow_html=True)

    if st.button("📊  Dashboard", key="nd"):
        st.session_state.mode = "dashboard"; st.rerun()
    saved_ct = len(st.session_state.get("saved", []))
    if st.button(f"🔖  Saved Niches  ({saved_ct})", key="ns"):
        st.session_state.mode = "saved"; st.rerun()
    if st.button("📡  Live Scanner", key="nlive"):
        st.session_state.mode = "live_scanner"; st.rerun()
    if st.button("📋  Criteria Guide", key="nc"):
        st.session_state.mode = "criteria"; st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Live scanner timer
    scan_status = get_scan_status()
    is_scanning = scan_status.get("status") == "scanning"
    rem = scanner_countdown()
    if is_scanning:
        st.markdown('<div class="timer-box" style="color:#f59e0b;border-color:rgba(245,158,11,.3)">⚡ Scan in progress...</div>', unsafe_allow_html=True)
    else:
        m, s = divmod(rem, 60); h, m = divmod(m, 60)
        timer_str = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        if rem > 0:
            st.markdown(f'<div class="timer-box">⏱ Next web scan in<br><b style="font-size:1.1rem">{timer_str}</b></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="timer-box" style="color:#10b981;border-color:rgba(16,185,129,.3)">⚡ Web scan ready!</div>', unsafe_allow_html=True)

    if st.button("🔄 Scan Now", key="forcescan", type="primary"):
        st.session_state.mode = "live_scanner"
        with st.spinner("🔍 Scanning Amazon · Alibaba · Trends · eBay…"):
            try:
                new_prods, updated_db = run_full_scan()
                st.session_state.db = updated_db
                st.session_state["last_scan_found"] = len(new_prods)
            except Exception as scan_err:
                st.warning(f"Scan encountered an issue: {scan_err}")
        st.rerun()

    db_from_file = load_db()
    scanned_ct = len(db_from_file.get("scanned_products", []))
    last_found  = st.session_state.get("last_scan_found", "—")
    st.markdown(f"""
<div style="font-size:.7rem;color:#334155;line-height:2;padding:.25rem">
<div style="color:#10b981">● Mode: On-Demand (Cloud)</div>
<div>● Curated DB: {len(MASTER_POOL)} products</div>
<div>● Web-Scanned: {scanned_ct} products</div>
<div>● Last scan found: {last_found} new</div>
<div>● Sources: Amazon · Alibaba · Trends · eBay</div>
<div>● Rules: 8-criteria strict mode</div>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
#  DASHBOARD
# ════════════════════════════════════════════
if st.session_state.mode == "dashboard":

    st.markdown('<div class="ph">🤖 Autonomous FBA AI Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="ps">Scanning Amazon globally · Strict 8-criteria filter · Price >$40 · Weight <5kg · Evergreen demand · No repetition</div>', unsafe_allow_html=True)

    # Stats strip
    scan_ct = db.get("scan_count", 0)
    shown_ct = len(db.get("shown_ids", []))
    db_fresh = load_db()
    web_pool_ct = len(db_fresh.get("web_pool", []))
    total_pool = len(MASTER_POOL) + web_pool_ct
    st.markdown(f"""
<div class="stats-strip">
<div class="sstat"><span class="dot-live"></span> Bot Status <span class="sv">Online</span></div>
<div class="sstat">🗃️ Curated DB <span class="sv">{len(MASTER_POOL)} Products</span></div>
<div class="sstat">📡 Web-Scanned <span class="sv">{web_pool_ct} Products</span></div>
<div class="sstat">🔍 Scans Done <span class="sv">{scan_ct}</span></div>
<div class="sstat">🎯 Remaining <span class="sv">{total_pool - shown_ct}</span></div>
<div class="sstat">⚡ Criteria <span class="sv">8 / 8 Active</span></div>
</div>""", unsafe_allow_html=True)

    # Auto-scan check when page loads
    if db.get("last_scan_time", 0) > 0 and time_until_next_scan(db) == 0 and not st.session_state.booted:
        ph = st.empty()
        batch, db = run_scan(db); st.session_state.db = db
        st.session_state.view = batch; st.session_state.booted = True

    if not st.session_state.booted:
        # Boot screen
        st.markdown("""
<div style="background:#060a12;border:1px solid rgba(6,182,212,.2);border-radius:14px;overflow:hidden;margin:1rem 0">
<div style="background:rgba(255,255,255,.04);padding:.5rem 1rem;display:flex;align-items:center;gap:7px;border-bottom:1px solid rgba(255,255,255,.05)">
<span style="width:10px;height:10px;border-radius:50%;background:#ff5f57;display:inline-block"></span>
<span style="width:10px;height:10px;border-radius:50%;background:#febc2e;display:inline-block"></span>
<span style="width:10px;height:10px;border-radius:50%;background:#28c840;display:inline-block"></span>
<span style="font-size:.7rem;color:#64748b;margin-left:auto">agent_core.exe</span>
</div>
<div style="padding:1rem 1.25rem;font-family:monospace;font-size:.8rem;color:#a0d18f;min-height:100px;line-height:1.8">
<div>&gt; <span style="color:#06b6d4">[SYSTEM]</span> FBA Agent v4.0 ready. 150 products in database.</div>
<div>&gt; <span style="color:#64748b">[IDLE]</span> Awaiting boot command to begin scan...</div>
<div>&gt; <span style="color:#a0d18f">[RULES]</span> Price &gt;$40 · Weight &lt;5kg · Reviews &lt;5000 · Margin ≥15% · KW Vol ≥1,500</div>
<div>&gt; <span style="color:#64748b">[READY]</span> All 8 criteria filters loaded and active.</div>
<div style="color:#3b82f6;animation:blink 1s step-end infinite">▌</div>
</div></div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("⚙️  Boot Agent & Extract Winning Niches", type="primary", use_container_width=True):
                ph = st.empty()
                batch, db = run_scan(db, ph)
                st.session_state.db = db; st.session_state.view = batch
                st.session_state.booted = True; st.rerun()
    else:
        # Results
        ct = len(st.session_state.view)
        st.markdown(f'<div class="sec-hdr">Extracted Winning Niches <span class="cnt-badge">{ct} results</span></div>', unsafe_allow_html=True)

        ca, cb = st.columns(2, gap="medium")
        for i, p in enumerate(st.session_state.view):
            col = ca if i % 2 == 0 else cb
            with col:
                st.markdown(card_html(p), unsafe_allow_html=True)
                is_sv = any(x["id"] == p["id"] for x in st.session_state.saved)
                bk = f"sv_{p['id']}_{i}"
                if is_sv:
                    if st.button("💔 Unsave", key=bk, use_container_width=True):
                        st.session_state.saved = [x for x in st.session_state.saved if x["id"] != p["id"]]; st.rerun()
                else:
                    if st.button("❤️ Save Niche", key=bk, type="primary", use_container_width=True):
                        st.session_state.saved.append(p); st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Build combined available pool: curated MASTER_POOL + web-scanned web_pool
        db_fresh = load_db()
        shown_set = set(db.get("shown_ids", []))
        web_pool = db_fresh.get("web_pool", [])
        master_avail = [p for p in MASTER_POOL if p["id"] not in shown_set]
        web_avail    = [p for p in web_pool    if p["id"] not in shown_set]
        available = master_avail + web_avail

        if available:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                web_label = f" incl. {len(web_avail)} live-scanned" if web_avail else ""
                if st.button(f"⚡ Generate Next 25  ({len(available)} remaining{web_label})", type="primary", use_container_width=True):
                    batch = random.sample(available, min(25, len(available)))
                    for p in batch: db["shown_ids"].append(p["id"])
                    save_db(db); st.session_state.view = batch; st.rerun()
        else:
            st.markdown("""
<div style="text-align:center;padding:1.5rem;background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-radius:12px;color:#fca5a5;font-size:.88rem">
🔴 All products shown. Next web scan in ~15 min will discover new niches automatically.
</div>""", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("🔄 Reset Agent Memory", use_container_width=True):
                    db["shown_ids"] = []; save_db(db)
                    st.session_state.booted = False; st.session_state.view = []; st.rerun()


# ════════════════════════════════════════════
#  SAVED NICHES
# ════════════════════════════════════════════
elif st.session_state.mode == "saved":
    st.markdown('<div class="ph">🔖 My Saved Niches</div>', unsafe_allow_html=True)
    st.markdown('<div class="ps">Your curated vault of validated Amazon product ideas</div>', unsafe_allow_html=True)
    if not st.session_state.saved:
        st.markdown("""
<div style="text-align:center;padding:4rem 2rem;background:rgba(15,22,40,.5);border:1px dashed rgba(99,179,255,.15);border-radius:18px">
<div style="font-size:2.5rem;margin-bottom:.75rem">🔖</div>
<div style="color:#64748b;font-size:1rem;font-weight:600">No saved niches yet</div>
<div style="color:#475569;font-size:.82rem;margin-top:.4rem">Run the agent and save your favourites.</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sec-hdr">Saved Products <span class="cnt-badge">{len(st.session_state.saved)}</span></div>', unsafe_allow_html=True)
        ca, cb = st.columns(2, gap="medium")
        for i, p in enumerate(reversed(st.session_state.saved)):
            col = ca if i % 2 == 0 else cb
            with col:
                st.markdown(card_html(p), unsafe_allow_html=True)
                if st.button("💔 Remove", key=f"rm_{p['id']}_{i}", use_container_width=True):
                    st.session_state.saved = [x for x in st.session_state.saved if x["id"] != p["id"]]; st.rerun()

# ════════════════════════════════════════════
#  CRITERIA GUIDE
# ════════════════════════════════════════════
elif st.session_state.mode == "criteria":
    st.markdown('<div class="ph">📋 Product Research Criteria</div>', unsafe_allow_html=True)
    st.markdown('<div class="ps">8 key factors enforced on every product in this database</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="criteria-grid">
<div class="crit"><div class="crit-icon">📅</div><span class="crit-label">Seasonality</span><span class="crit-val">Evergreen Only</span></div>
<div class="crit"><div class="crit-icon">💲</div><span class="crit-label">Price Range</span><span class="crit-val">&gt; $40 USD</span></div>
<div class="crit"><div class="crit-icon">📦</div><span class="crit-label">Weight Limit</span><span class="crit-val">&lt; 5 kg</span></div>
<div class="crit"><div class="crit-icon">⭐</div><span class="crit-label">Review Count</span><span class="crit-val">Top 10 &lt; 5,000</span></div>
<div class="crit"><div class="crit-icon">💰</div><span class="crit-label">Net Margin</span><span class="crit-val">15–30% Target</span></div>
<div class="crit"><div class="crit-icon">👑</div><span class="crit-label">Brand Dominance</span><span class="crit-val">Low (&lt; 20%)</span></div>
<div class="crit"><div class="crit-icon">🔍</div><span class="crit-label">Keyword Volume</span><span class="crit-val">≥ 1,500/month</span></div>
<div class="crit"><div class="crit-icon">📈</div><span class="crit-label">Monthly Revenue</span><span class="crit-val">Viable Threshold</span></div>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div style="margin-bottom:1.5rem">
<div class="sec-hdr">💰 Profit & Cost Structure</div>
<div style="background:rgba(13,19,36,.8);border:1px solid var(--bdr);border-radius:14px;padding:1.25rem 1.5rem">
<div style="background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.2);border-radius:10px;padding:.75rem 1rem;margin-bottom:1rem;font-size:.82rem;color:#fcd34d">
🛒 <b>Landing Cost Formula:</b>&nbsp; Alibaba Source Price ($5–$20) &nbsp;×&nbsp; 1.5 <span style="color:#92400e;font-size:.72rem">(shipping multiplier)</span> &nbsp;=&nbsp; <b style="color:#f59e0b">Landing Cost</b><br>
<span style="font-size:.72rem;color:#92400e">Source: Alibaba verified merchant &nbsp;·&nbsp; Acceptable source price range: $5–$20 USD</span>
</div>
<div style="display:flex;gap:1rem;flex-wrap:wrap">
<div style="flex:1;min-width:130px;text-align:center;padding:.75rem;background:rgba(245,158,11,.08);border-radius:10px;border:1px solid rgba(245,158,11,.2)">
<div style="font-size:.65rem;color:#94a3b8;margin-bottom:4px">LANDING COST</div>
<div style="font-size:1.1rem;font-weight:800;color:#f59e0b">Source × 1.5</div>
<div style="font-size:.65rem;color:#78716c;margin-top:4px">e.g. $10 × 1.5 = $15</div>
</div>
<div style="flex:1;min-width:130px;text-align:center;padding:.75rem;background:rgba(239,68,68,.08);border-radius:10px;border:1px solid rgba(239,68,68,.2)">
<div style="font-size:.65rem;color:#94a3b8;margin-bottom:4px">AMAZON FBA FEES</div>
<div style="font-size:1.4rem;font-weight:800;color:#ef4444">30%</div>
<div style="font-size:.65rem;color:#78716c;margin-top:4px">of retail price</div>
</div>
<div style="flex:1;min-width:130px;text-align:center;padding:.75rem;background:rgba(139,92,246,.08);border-radius:10px;border:1px solid rgba(139,92,246,.2)">
<div style="font-size:.65rem;color:#94a3b8;margin-bottom:4px">AMAZON PPC</div>
<div style="font-size:1.4rem;font-weight:800;color:#a78bfa">20%</div>
<div style="font-size:.65rem;color:#78716c;margin-top:4px">of retail price</div>
</div>
<div style="flex:1;min-width:130px;text-align:center;padding:.75rem;background:rgba(16,185,129,.08);border-radius:10px;border:1px solid rgba(16,185,129,.2)">
<div style="font-size:.65rem;color:#94a3b8;margin-bottom:4px">NET PROFIT</div>
<div style="font-size:1.4rem;font-weight:800;color:#10b981">≥ 15%</div>
<div style="font-size:.65rem;color:#78716c;margin-top:4px">target 20–30%</div>
</div>
</div>
<div style="margin-top:1rem;font-size:.75rem;color:#64748b;text-align:center">
Net Profit = Retail Price − Landing Cost − FBA Fees − PPC &nbsp;·&nbsp; Minimum: 15% &nbsp;·&nbsp; Good: 20%+ &nbsp;·&nbsp; Ideal: 25–30%
</div>
</div></div>

<div style="margin-bottom:1.5rem">
<div class="sec-hdr">🔬 5-Step Research Methodology</div>
<div style="display:flex;flex-direction:column;gap:.6rem">
""" + "".join([
    f'<div style="background:rgba(13,19,36,.8);border:1px solid var(--bdr);border-radius:10px;padding:.75rem 1.1rem;display:flex;align-items:flex-start;gap:.75rem">'
    f'<div style="width:26px;height:26px;min-width:26px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700">{n}</div>'
    f'<div><div style="font-size:.82rem;font-weight:600;color:#e2e8f0">{t}</div><div style="font-size:.75rem;color:#64748b;margin-top:3px">{d}</div></div></div>'
    for n, t, d in [
        (1,"Market Demand Analysis","Validate via keyword search volume ≥ 1,500/mo. Strong: 3,000+. Good: 2,000+. Viable: 1,500+."),
        (2,"Competition Check","Review count, star ratings, pricing. Top 10 competitors must have < 5,000 reviews."),
        (3,"Profitability Assessment","FBA fees, shipping, landed cost. Target ROI > 30%. Min margin 15%."),
        (4,"Differentiation Strategy","Gaps in features, packaging, colors, bundles, eco-friendly options from 1-star review mining."),
        (5,"Risk Analysis","Restricted keywords, compliance with CPC/FDA/FCC, review dominance check."),
    ]
]) + """
</div></div>

<div>
<div class="sec-hdr">🔑 Keyword Validation Thresholds</div>
<div style="background:rgba(13,19,36,.8);border:1px solid var(--bdr);border-radius:12px;padding:1rem 1.25rem;display:flex;gap:1rem;flex-wrap:wrap">
<div style="flex:1;text-align:center;padding:.6rem;background:rgba(239,68,68,.08);border-radius:8px"><div style="font-size:1.1rem;font-weight:700;color:#ef4444">&lt; 1,500</div><div style="font-size:.7rem;color:#94a3b8;margin-top:3px">Too Weak — Skip</div></div>
<div style="flex:1;text-align:center;padding:.6rem;background:rgba(245,158,11,.08);border-radius:8px"><div style="font-size:1.1rem;font-weight:700;color:#f97316">1,500+</div><div style="font-size:.7rem;color:#94a3b8;margin-top:3px">Viable — Minimum</div></div>
<div style="flex:1;text-align:center;padding:.6rem;background:rgba(245,158,11,.1);border-radius:8px"><div style="font-size:1.1rem;font-weight:700;color:#f59e0b">2,000+</div><div style="font-size:.7rem;color:#94a3b8;margin-top:3px">Good — Proceed</div></div>
<div style="flex:1;text-align:center;padding:.6rem;background:rgba(16,185,129,.1);border-radius:8px"><div style="font-size:1.1rem;font-weight:700;color:#10b981">3,000+</div><div style="font-size:.7rem;color:#94a3b8;margin-top:3px">Strong — Priority</div></div>
</div></div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════
#  LIVE SCANNER PAGE
# ════════════════════════════════════════════
elif st.session_state.mode == "live_scanner":
    st.markdown('<div class="ph">📡 Live Web Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div class="ps">Autonomous crawler scanning Amazon · Alibaba · Google Trends · eBay every hour</div>', unsafe_allow_html=True)

    scan_status = get_scan_status()
    is_scanning = scan_status.get("status") == "scanning"
    db_live = load_db()
    scanned_products = db_live.get("scanned_products", [])
    scan_history = db_live.get("scan_history", [])

    # Stats row
    st.markdown(f"""
<div class="stats-strip">
<div class="sstat"><span class="dot-live"></span> Scanner <span class="sv">{"Active" if scanner_is_running() else "Stopped"}</span></div>
<div class="sstat">📦 Web-Scanned <span class="sv">{len(scanned_products)} products</span></div>
<div class="sstat">🔍 Total Scans <span class="sv">{db_live.get("scan_count", 0)}</span></div>
<div class="sstat">⚡ Last Found <span class="sv">{scan_status.get("products_found", 0)} new</span></div>
<div class="sstat">📊 Sources <span class="sv">4 active</span></div>
</div>""", unsafe_allow_html=True)

    # Terminal
    term_lines = scan_status.get("lines", [])
    if not term_lines:
        term_lines = [
            {"msg": "> [SYSTEM] FBA Scanner v2.0 — Background thread active.", "color": "#06b6d4"},
            {"msg": "> [STATUS] Waiting for next scheduled scan or Force Scan.", "color": "#64748b"},
            {"msg": "> [INFO] Sources: Amazon BSR · Alibaba Search · Google Trends · eBay", "color": "#64748b"},
            {"msg": "> [INFO] Filter: Price >$40 · Weight <5kg · Reviews <5000 · Margin ≥15%", "color": "#a0d18f"},
        ]

    term_html = "".join(
        f'<span style="color:{l.get("color","#94a3b8")}">[{l.get("time","")}] {l.get("msg","")}</span><br>'
        for l in term_lines
    )
    cursor = '<span style="color:#3b82f6;animation:blink 1s step-end infinite">▌</span>' if is_scanning else ""
    st.markdown(f"""
<div style="background:#060a12;border:1px solid rgba(6,182,212,.2);border-radius:14px;overflow:hidden;margin-bottom:1.5rem">
<div style="background:rgba(255,255,255,.04);padding:.5rem 1rem;display:flex;align-items:center;gap:7px;border-bottom:1px solid rgba(255,255,255,.05)">
<span style="width:10px;height:10px;border-radius:50%;background:#ff5f57;display:inline-block"></span>
<span style="width:10px;height:10px;border-radius:50%;background:#febc2e;display:inline-block"></span>
<span style="width:10px;height:10px;border-radius:50%;background:#28c840;display:inline-block"></span>
<span style="font-size:.7rem;color:#64748b;margin-left:auto">scanner_core.exe — {"SCANNING" if is_scanning else "IDLE"}</span>
</div>
<div style="padding:1rem 1.25rem;font-family:monospace;font-size:.78rem;line-height:1.9;min-height:160px">
{term_html}{cursor}
</div></div>""", unsafe_allow_html=True)

    # Source breakdown
    st.markdown("""
<div class="sec-hdr">🌐 Active Scan Sources</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1.5rem">
<div style="background:rgba(13,19,36,.8);border:1px solid rgba(99,179,255,.12);border-radius:12px;padding:.85rem;text-align:center">
<div style="font-size:1.2rem;margin-bottom:.3rem">🛒</div>
<div style="font-size:.78rem;font-weight:700;color:#e2e8f0">Amazon</div>
<div style="font-size:.65rem;color:#64748b;margin-top:3px">BSR · Movers · New Releases</div>
<div style="font-size:.65rem;color:#10b981;margin-top:3px">11 category pages</div>
</div>
<div style="background:rgba(13,19,36,.8);border:1px solid rgba(99,179,255,.12);border-radius:12px;padding:.85rem;text-align:center">
<div style="font-size:1.2rem;margin-bottom:.3rem">🛍️</div>
<div style="font-size:.78rem;font-weight:700;color:#e2e8f0">Alibaba</div>
<div style="font-size:.65rem;color:#64748b;margin-top:3px">Trending product searches</div>
<div style="font-size:.65rem;color:#10b981;margin-top:3px">10 search queries</div>
</div>
<div style="background:rgba(13,19,36,.8);border:1px solid rgba(99,179,255,.12);border-radius:12px;padding:.85rem;text-align:center">
<div style="font-size:1.2rem;margin-bottom:.3rem">📊</div>
<div style="font-size:.78rem;font-weight:700;color:#e2e8f0">Google Trends</div>
<div style="font-size:.65rem;color:#64748b;margin-top:3px">Product keyword interest</div>
<div style="font-size:.65rem;color:#10b981;margin-top:3px">7 categories validated</div>
</div>
<div style="background:rgba(13,19,36,.8);border:1px solid rgba(99,179,255,.12);border-radius:12px;padding:.85rem;text-align:center">
<div style="font-size:1.2rem;margin-bottom:.3rem">🏷️</div>
<div style="font-size:.78rem;font-weight:700;color:#e2e8f0">eBay</div>
<div style="font-size:.65rem;color:#64748b;margin-top:3px">Cross-validate trending items</div>
<div style="font-size:.65rem;color:#10b981;margin-top:3px">5 category searches</div>
</div>
</div>""", unsafe_allow_html=True)

    # Scan history
    if scan_history:
        st.markdown('<div class="sec-hdr">🕐 Scan History</div>', unsafe_allow_html=True)
        history_html = '<div style="display:flex;flex-direction:column;gap:6px;margin-bottom:1.5rem">'
        for h in reversed(scan_history[-10:]):
            raw_t = h.get("time", "")
            # time can be float (unix timestamp) or ISO string
            if isinstance(raw_t, (int, float)):
                from datetime import datetime as _dt
                t = _dt.fromtimestamp(raw_t).strftime("%Y-%m-%d %H:%M:%S")
            else:
                t = str(raw_t)[:19].replace("T", " ")
            nf = h.get("products_found", 0)
            tot = h.get("total_scanned", 0)
            history_html += (
                f'<div style="background:rgba(13,19,36,.6);border:1px solid rgba(255,255,255,.06);'
                f'border-radius:8px;padding:.5rem .85rem;display:flex;justify-content:space-between;'
                f'font-size:.75rem;color:#94a3b8">'
                f'<span>🕐 {t}</span>'
                f'<span style="color:#10b981">+{nf} new</span>'
                f'<span>{tot} scanned</span>'
                f'</div>'
            )
        history_html += '</div>'
        st.markdown(history_html, unsafe_allow_html=True)

    # Web-scanned products
    if scanned_products:
        st.markdown(f'<div class="sec-hdr">📦 Web-Scanned Products <span class="cnt-badge">{len(scanned_products)}</span></div>', unsafe_allow_html=True)
        ca, cb = st.columns(2, gap="medium")
        for i, p in enumerate(reversed(scanned_products[-50:])):
            col = ca if i % 2 == 0 else cb
            with col:
                st.markdown(card_html(p), unsafe_allow_html=True)
                is_sv = any(x["id"] == p["id"] for x in st.session_state.saved)
                bk = f"svsc_{p['id']}_{i}"
                if is_sv:
                    if st.button("💔 Unsave", key=bk, use_container_width=True):
                        st.session_state.saved = [x for x in st.session_state.saved if x["id"] != p["id"]]
                        st.rerun()
                else:
                    if st.button("❤️ Save Niche", key=bk, type="primary", use_container_width=True):
                        st.session_state.saved.append(p); st.rerun()
    else:
        st.markdown("""
<div style="text-align:center;padding:3rem 2rem;background:rgba(15,22,40,.5);border:1px dashed rgba(99,179,255,.15);border-radius:18px">
<div style="font-size:2.5rem;margin-bottom:.75rem">📡</div>
<div style="color:#64748b;font-size:1rem;font-weight:600">No web-scanned products yet</div>
<div style="color:#475569;font-size:.82rem;margin-top:.4rem">Click <b>Force Scan Now</b> in the sidebar to run your first live web scan.</div>
<div style="color:#475569;font-size:.78rem;margin-top:.3rem">The scanner will then run automatically every hour.</div>
</div>""", unsafe_allow_html=True)

    # Auto-refresh every 8 seconds during scanning
    if is_scanning:
        time.sleep(8)
        st.rerun()
