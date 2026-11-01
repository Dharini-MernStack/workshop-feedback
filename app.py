"""
CEO OF SUPERINTELLIGENCE -- Workshop Slide Deck
Run: streamlit run app.py
"""

import streamlit as st
import time
import os
import json
import socket
import io
import requests
try:
    import qrcode
    from PIL import Image
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# ---- FEEDBACK SERVER URL ----
# Change this to your Render URL after deploying, e.g.:
# FEEDBACK_URL = "https://workshop-feedback-xxxx.onrender.com"
# For local testing:
FEEDBACK_URL = os.environ.get("FEEDBACK_URL", "https://workshop-feedback-ismc.onrender.com")

# -- Page Config --
st.set_page_config(
    page_title="CEO of Superintelligence -- Workshop",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -- Mega CSS: fullscreen slides, code editor, nav buttons --
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* ---- Base ---- */
    .stApp { background-color: #0a0a0a; color: #e5e7eb; }
    .block-container { padding-top: 2.5rem !important; padding-bottom: 0 !important; max-width: 1100px; margin: 0 auto; }
    header[data-testid="stHeader"] { background: #0a0a0a; height: 0px !important; min-height: 0px !important; }
    
    /* ---- Slide Frame ---- */
    .slide-frame {
        background: #111;
        border: 1px solid #222;
        border-radius: 20px;
        padding: 48px 56px;
        min-height: 70vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        position: relative;
    }
    .slide-frame > * { width: 100%; }
    .slide-frame h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #EF3837, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        line-height: 1.15;
        text-align: center;
    }
    .slide-frame h2 {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .slide-frame h3 {
        font-family: 'Inter', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #d1d5db;
        margin-top: 18px;
    }
    .slide-frame p, .slide-frame li {
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #d1d5db;
    }
    .slide-subtitle {
        font-size: 1.3rem;
        color: #9ca3af;
        margin-top: 0;
        text-align: center;
    }
    .slide-number {
        position: absolute;
        bottom: 18px;
        right: 28px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #555;
    }
    
    /* ---- Big quote ---- */
    .big-quote {
        font-size: 1.6rem;
        font-weight: 700;
        color: #e5e7eb;
        text-align: center;
        padding: 32px 0;
        line-height: 1.6;
    }
    .big-quote em { color: #EF3837; font-style: normal; }
    
    /* ---- Level cards ---- */
    .level-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 14px;
        margin: 24px 0;
    }
    .level-card {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 20px 16px;
        text-align: center;
    }
    .level-card.active { border-color: #EF3837; background: #1a0a0a; }
    .level-card h4 { color: #EF3837; margin: 0 0 4px 0; font-size: 1.1rem; }
    .level-card .role { color: #9ca3af; font-size: 0.85rem; margin: 0; }
    .level-card .phrase { color: #e5e7eb; font-size: 0.95rem; margin-top: 8px; }
    
    /* ---- Code editor ---- */
    .code-editor {
        border: 1px solid #333;
        border-radius: 14px;
        overflow: hidden;
        margin: 16px 0;
    }
    .code-editor-bar {
        background: #1e1e1e;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #333;
    }
    .dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
    .dot-r { background: #ff5f57; }
    .dot-y { background: #ffbd2e; }
    .dot-g { background: #28c840; }
    .code-editor-bar span.fname {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #888;
        margin-left: 10px;
    }
    .code-editor-body {
        background: #1e1e1e;
        padding: 0;
    }
    .replicate-bar {
        background: #161616;
        border-top: 1px dashed #333;
        padding: 14px 20px;
        color: #9ca3af;
        font-size: 0.88rem;
        line-height: 1.7;
    }
    .replicate-bar strong { color: #EF3837; }
    .replicate-bar code {
        background: #222;
        padding: 2px 7px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        color: #e5e7eb;
        font-size: 0.84rem;
    }
    

    
    /* ---- Streamlit overrides ---- */
    .stButton > button {
        background: linear-gradient(135deg, #EF3837, #cc2a29);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-weight: 700;
        font-size: 1.05rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(239,56,55,0.5);
    }
    .stCodeBlock { border-radius: 0 !important; margin: 0 !important; }
    [data-testid="stMetricValue"] { font-size: 2.5rem; color: #EF3837; }
    .stLinkButton > a {
        background: linear-gradient(135deg, #EF3837, #cc2a29) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #EF3837 !important;
        border-bottom-color: #EF3837 !important;
    }
    
    /* Quiz styling */
    .quiz-container {
        background: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 14px;
        padding: 24px;
        margin: 12px 0;
    }
    
    /* Activity card */
    .activity-card {
        background: linear-gradient(135deg, #0d1117, #111a2e);
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }
    .activity-card h4 { color: #3b82f6; margin-top: 0; }
    
    /* Demo output */
    .demo-output {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 24px;
        margin: 14px 0;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #0d0d0d; }
</style>
""", unsafe_allow_html=True)

# ================================================================
#  HELPERS
# ================================================================

def code_editor(code, filename="main.py", language="python", replicate_steps=None):
    """Render code in a VS Code-style editor block."""
    st.markdown(f"""
    <div class="code-editor">
        <div class="code-editor-bar">
            <span class="dot dot-r"></span>
            <span class="dot dot-y"></span>
            <span class="dot dot-g"></span>
            <span class="fname">{filename}</span>
        </div>
        <div class="code-editor-body">
    """, unsafe_allow_html=True)
    st.code(code, language=language)
    if replicate_steps:
        steps_html = "<br>".join([f"{i+1}. {s}" for i, s in enumerate(replicate_steps)])
        st.markdown(f"""
        <div class="replicate-bar">
            <strong>How to run this yourself:</strong><br><br>
            {steps_html}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# Speaker script is in SPEAKER_SCRIPT.md (separate file)


def get_local_ip():
    """Get LAN IP for QR code."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def generate_qr(url):
    """Generate QR code image for a URL."""
    if not QR_AVAILABLE:
        return None
    qr = qrcode.QRCode(version=1, box_size=10, border=2,
                        error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="#111111")
    return img


def load_feedback_stats():
    """Load feedback stats from the feedback server API."""
    try:
        resp = requests.get(f"{FEEDBACK_URL}/api/stats", timeout=3)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    # Fallback: empty
    return {
        "round_1": {"count": 0, "avg_rating": 0, "entries": []},
        "round_2": {"count": 0, "avg_rating": 0, "entries": []},
        "round_3": {"count": 0, "avg_rating": 0, "entries": []},
    }


def render_feedback_slide(round_num, slide_num_html, sn, TOTAL):
    """Render a live feedback collection slide."""
    round_key = f"round_{round_num}"
    round_labels = {1: "11:00 AM — First Impressions", 2: "1:00 PM — Before Lunch Break", 3: "3:30 PM — Final Pulse"}
    
    n = slide_start(f"⚡ Live Feedback — Round {round_num}", round_labels.get(round_num, ""), sn, TOTAL)
    
    url = f"{FEEDBACK_URL}/round/{round_num}"
    
    col_qr, col_stats = st.columns([1, 1])
    
    with col_qr:
        st.markdown(f"""
        <div style="text-align:center; padding: 10px 0;">
            <p style="font-size:1.3rem; color:#9ca3af; margin-bottom:8px;">📱 Scan with your phone</p>
            <p style="font-size:0.85rem; color:#555; margin-bottom:12px;">Works on <strong style='color:#EF3837;'>any network</strong> — mobile data is fine!</p>
        </div>
        """, unsafe_allow_html=True)
        
        qr_img = generate_qr(url)
        if qr_img:
            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf, width=280, use_container_width=False)
        else:
            st.warning("Install qrcode & Pillow: pip install qrcode[pil]")
        
        st.markdown(f"""
        <div style="text-align:center;">
            <code style="background:#1a1a1a; padding:8px 16px; border-radius:8px; color:#ff6b6b; font-size:0.9rem;">{url}</code>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats:
        stats = load_feedback_stats()
        rd = stats.get(round_key, {"count": 0, "avg_rating": 0, "entries": []})
        count = rd["count"]
        avg = rd["avg_rating"]
        
        rating_emoji = {1: "😴", 2: "😐", 3: "🙂", 4: "😃", 5: "🤯"}
        avg_emoji = rating_emoji.get(round(avg) if avg else 3, "🙂")
        
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0;">
            <p style="font-size:5rem; font-weight:900; color:#22c55e; margin:0; font-family:'JetBrains Mono',monospace;">{count}</p>
            <p style="font-size:1.2rem; color:#9ca3af;">responses received</p>
        </div>
        """, unsafe_allow_html=True)
        
        if avg > 0:
            st.markdown(f"""
            <div style="text-align:center; padding:10px 0;">
                <p style="font-size:3rem; margin:0;">{avg_emoji}</p>
                <p style="font-size:1.1rem; color:#9ca3af;">Average: <strong style="color:#EF3837;">{avg}/5</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show recent names
        if rd["entries"]:
            recent = rd["entries"][-8:]  # last 8
            names = " • ".join([f"{rating_emoji.get(e['rating'],'🙂')} {e['name']}" for e in reversed(recent)])
            st.markdown(f"""
            <div style="text-align:center; padding:12px 0;">
                <p style="color:#555; font-size:0.8rem; margin-bottom:4px;">RECENT</p>
                <p style="color:#9ca3af; font-size:0.95rem;">{names}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Auto-refresh button
    if st.button("🔄 Refresh Count", use_container_width=True, key=f"refresh_fb_{round_num}"):
        st.rerun()
    
    # Show all feedback in expander
    if rd["entries"]:
        with st.expander(f"📋 View All {count} Responses"):
            for e in reversed(rd["entries"]):
                emoji = rating_emoji.get(e["rating"], "🙂")
                fb_text = f' — "{e["feedback"]}"' if e.get("feedback") else ""
                st.markdown(f"{emoji} **{e['name']}** {fb_text}")
    
    slide_end(n)


def slide_start(title, subtitle=None, slide_num=None, total=None):
    """Open a slide frame."""
    sub = f'<p class="slide-subtitle">{subtitle}</p>' if subtitle else ""
    num = f'<div class="slide-number">{slide_num} / {total}</div>' if slide_num else ""
    st.markdown(f"""<div class="slide-frame">
        <h1>{title}</h1>{sub}""", unsafe_allow_html=True)
    return num


def slide_end(num_html=""):
    st.markdown(f"""{num_html}</div>""", unsafe_allow_html=True)


# ================================================================
#  SLIDE DEFINITIONS
# ================================================================
SLIDES = [
    "Title",
    "The 5 Levels",
    "Setup",
    "Demo 1: Roast My Resume",
    "Demo 1: Code Behind",
    "Demo 2: Level 1 vs Level 4",
    "Demo 2: Code Behind",
    "Demo 3: Embeddings",
    "Demo 3: Code Behind",
    "⚡ Feedback 1",
    "Quiz 1: Agents Basics",
    "Demo 4: RAG Pipeline",
    "Demo 4: Code Behind",
    "Demo 5: No-Code Agent",
    "⚡ Feedback 2",
    "Quiz 2: RAG and Embeddings",
    "Activity 1: Prompt Engineering",
    "Demo 6: Code Agent",
    "Demo 6: Code Behind",
    "Demo 7: Gradio Deploy",
    "Demo 7: Colab Instructions",
    "⚡ Feedback 3",
    "Quiz 3: Building Agents",
    "Activity 2: Build a RAG",
    "Activity 3: Build an Agent",
    "Activity 4: Hackathon",
    "Final Quiz",
    "Quick Links",
    "Timer",
]
TOTAL = len(SLIDES)

# ================================================================
#  SESSION STATE
# ================================================================
if 'slide' not in st.session_state:
    st.session_state.slide = 0
if 'groq_key' not in st.session_state:
    st.session_state.groq_key = os.environ.get('GROQ_API_KEY', '')

# ================================================================
#  NAVIGATION BAR (top)
# ================================================================
nav_left, nav_center, nav_right = st.columns([1, 3, 1])

with nav_left:
    if st.button("< Previous", use_container_width=True, disabled=(st.session_state.slide == 0)):
        st.session_state.slide -= 1
        st.rerun()

with nav_center:
    selected = st.selectbox(
        "Jump to slide:",
        range(TOTAL),
        index=st.session_state.slide,
        format_func=lambda i: f"{i+1}. {SLIDES[i]}",
        label_visibility="collapsed"
    )
    if selected != st.session_state.slide:
        st.session_state.slide = selected
        st.rerun()

with nav_right:
    if st.button("Next >", use_container_width=True, disabled=(st.session_state.slide == TOTAL - 1)):
        st.session_state.slide += 1
        st.rerun()

current = SLIDES[st.session_state.slide]
sn = st.session_state.slide + 1

# ================================================================
#  SLIDE: TITLE
# ================================================================
if current == "Title":
    n = slide_start("BECOME THE CEO OF SUPERINTELLIGENCE",
                     "Building AI Agents Workshop -- SRM AP x Kalvium -- Nov 2026", sn, TOTAL)
    st.markdown("""
    <div class="big-quote">
        Person at Level 1: "AI will take my job"<br><br>
        Person at Level 5: <em>"I just automated my job and started a side business"</em><br><br>
        Same AI. Different user. Different outcome.
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)
    

# ================================================================
#  SLIDE: THE 5 LEVELS
# ================================================================
elif current == "The 5 Levels":
    n = slide_start("The 5 Levels of AI Users", None, sn, TOTAL)
    st.markdown("""
    <div class="level-grid">
        <div class="level-card">
            <h4>Level 1</h4>
            <p class="role">Consumer</p>
            <p class="phrase">"Hey ChatGPT"</p>
        </div>
        <div class="level-card">
            <h4>Level 2</h4>
            <p class="role">Prompter</p>
            <p class="phrase">"Think step by step"</p>
        </div>
        <div class="level-card">
            <h4>Level 3</h4>
            <p class="role">Integrator</p>
            <p class="phrase">"Here's MY data"</p>
        </div>
        <div class="level-card active">
            <h4>Level 4</h4>
            <p class="role">Agent Builder</p>
            <p class="phrase">"Use tools, decide"</p>
        </div>
        <div class="level-card">
            <h4>Level 5</h4>
            <p class="role">CEO</p>
            <p class="phrase">"Orchestrate a team"</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)
    

# ================================================================
#  SLIDE: SETUP
# ================================================================
elif current == "Setup":
    n = slide_start("API Key Setup", None, sn, TOTAL)
    st.markdown("Enter your Groq API key. Get one free at [console.groq.com](https://console.groq.com)")
    
    key = st.text_input("Groq API Key:", value=st.session_state.groq_key, type="password")
    if key:
        st.session_state.groq_key = key
        os.environ['GROQ_API_KEY'] = key
    
    if st.button("Test Connection", use_container_width=True):
        if not key:
            st.error("Please enter an API key first!")
        else:
            try:
                from groq import Groq
                client = Groq(api_key=key)
                resp = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[{"role": "user", "content": "Say 'CEO mode activated' in exactly those words"}],
                    max_tokens=20
                )
                st.success(f"Connected! Response: {resp.choices[0].message.content}")
            except Exception as e:
                st.error(f"Failed: {e}")
    
    code_editor(
        code="""# 1. Go to https://console.groq.com
# 2. Sign up / Log in with Google
# 3. Click "API Keys" in the left sidebar
# 4. Click "Create API Key"
# 5. Copy the key and paste it above

from groq import Groq
client = Groq(api_key='your-key-here')""",
        filename="setup.py",
        replicate_steps=[
            "Go to <code>console.groq.com</code> and create a free account",
            "Generate an API key (free tier: 30 requests/min)",
            "Install: <code>pip install groq</code>",
        ]
    )
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 1 - ROAST MY RESUME
# ================================================================
elif current == "Demo 1: Roast My Resume":
    n = slide_start("Demo 1: Roast My Resume", "The opening jaw-drop", sn, TOTAL)
    
    default_resume = """RESUME
Name: Rahul Kumar
B.Tech CSE, 2nd Year, GPA: 7.2

Skills: C, C++, Python, Java, HTML, CSS, JavaScript, React, 
Node.js, MongoDB, SQL, Machine Learning, Deep Learning, 
Blockchain, Cloud Computing, DevOps, Kubernetes, Docker

Projects:
1. To-Do App (HTML, CSS, JS)
2. Calculator App (Python)
3. Weather App (React) -- used an API

Experience: None
Achievements: Participated in college hackathon (didn't win)
Hobbies: Coding, Reading, Cricket"""
    
    resume = st.text_area("Resume to Roast:", value=default_resume, height=250)
    mode = st.selectbox("Roast Style:", ["Savage (Funny)", "Professional (Helpful)", "Gen-Z Slang"])
    
    if st.button("ROAST IT", use_container_width=True):
        if not st.session_state.groq_key:
            st.error("Set your API key in Setup first!")
        else:
            styles = {
                "Savage (Funny)": "You are a brutally honest recruiter who roasts resumes like a stand-up comedy special. Be savage but educational.",
                "Professional (Helpful)": "You are a senior tech recruiter. Give honest, direct, constructive feedback.",
                "Gen-Z Slang": "You are a gen-z career coach who speaks in memes, slang, and internet culture. Still give real advice."
            }
            from groq import Groq
            client = Groq(api_key=st.session_state.groq_key)
            with st.spinner("Generating roast..."):
                response = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": f"""{styles[mode]}
Structure your response as:
THE ROAST (savage, reference specific resume lines)
THE HARD TRUTH (what a recruiter actually thinks)
THE FIX (3 specific actions for TODAY)"""},
                        {"role": "user", "content": f"Roast this resume:\n{resume}"}
                    ],
                    temperature=0.85, max_tokens=700
                )
            st.markdown(f'<div class="demo-output">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 1 CODE
# ================================================================
elif current == "Demo 1: Code Behind":
    n = slide_start("Demo 1: The Code", "10 lines that roast a resume", sn, TOTAL)
    code_editor(
        code="""from groq import Groq

client = Groq(api_key="YOUR_KEY")

resume = \"\"\"Paste any resume here\"\"\"

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {
            "role": "system",
            "content": "You are a brutally honest recruiter who roasts resumes. "
                       "Structure: THE ROAST, THE HARD TRUTH, THE FIX."
        },
        {
            "role": "user",
            "content": f"Roast this resume:\\n{resume}"
        }
    ],
    temperature=0.85,
    max_tokens=700
)

print(response.choices[0].message.content)""",
        filename="roast_resume.py",
        replicate_steps=[
            "Install: <code>pip install groq</code>",
            "Replace <code>YOUR_KEY</code> with your Groq API key from console.groq.com",
            "Paste any resume text into the resume variable",
            "Run: <code>python roast_resume.py</code>",
            "<strong>Key concept:</strong> The <code>system</code> message controls the AI personality. The <code>user</code> message is your input. <code>temperature</code> (0-1) controls how creative the response is.",
        ]
    )
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 2 - LEVEL 1 VS LEVEL 4
# ================================================================
elif current == "Demo 2: Level 1 vs Level 4":
    n = slide_start("Demo 2: Level 1 vs Level 4", "Same question. Different universe.", sn, TOTAL)
    
    question = st.text_input("The Question:",
        value="I'm a 2nd year CSE student at SRM AP. Should I learn React or Next.js for getting an internship?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Level 1: Just Ask")
        if st.button("Run Level 1", key="l1"):
            if not st.session_state.groq_key:
                st.error("Set API key first!")
            else:
                from groq import Groq
                client = Groq(api_key=st.session_state.groq_key)
                with st.spinner("Thinking..."):
                    resp = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[{"role": "user", "content": question}],
                        max_tokens=300
                    )
                st.warning("Generic answer -- could be outdated:")
                st.markdown(resp.choices[0].message.content)
    
    with col2:
        st.markdown("### Level 4: Agent Mode")
        if st.button("Run Level 4", key="l4"):
            if not st.session_state.groq_key:
                st.error("Set API key first!")
            else:
                from groq import Groq
                from duckduckgo_search import DDGS
                client = Groq(api_key=st.session_state.groq_key)
                
                with st.status("Agent working...", expanded=True) as status:
                    st.write("Step 1: Searching current job market...")
                    try:
                        with DDGS() as ddgs:
                            jobs = "\n".join([f"- {r['title']}: {r['body']}" for r in ddgs.text("React Next.js jobs India 2026 fresher", max_results=3)])
                        st.code(jobs[:300] + "...", language=None)
                    except:
                        jobs = "Search unavailable -- using cached knowledge"
                        st.write(jobs)
                    
                    st.write("Step 2: Searching salary data...")
                    try:
                        with DDGS() as ddgs:
                            salary = "\n".join([f"- {r['title']}: {r['body']}" for r in ddgs.text("React Next.js developer salary India 2026", max_results=3)])
                        st.code(salary[:300] + "...", language=None)
                    except:
                        salary = "Salary data search unavailable"
                        st.write(salary)
                    
                    st.write("Step 3: Analyzing with your profile...")
                    resp = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {"role": "system", "content": "You are a career advisor. Give specific, data-backed advice with a 3-month action plan. Pick a side."},
                            {"role": "user", "content": f"Student: 2nd year CSE, knows basic JS.\nQuestion: {question}\n\nJOB DATA:\n{jobs}\n\nSALARY DATA:\n{salary}"}
                        ],
                        max_tokens=500
                    )
                    status.update(label="Agent done!", state="complete")
                st.success("Level 4 -- Data-backed, personalized:")
                st.markdown(resp.choices[0].message.content)
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 2 CODE
# ================================================================
elif current == "Demo 2: Code Behind":
    n = slide_start("Demo 2: The Code", "Search the web, then reason", sn, TOTAL)
    code_editor(
        code="""from groq import Groq
from duckduckgo_search import DDGS

client = Groq(api_key="YOUR_KEY")
question = "Should I learn React or Next.js for internships?"

# STEP 1: Search the web for real-time data
with DDGS() as ddgs:
    job_results = list(ddgs.text("React Next.js jobs India 2026", max_results=3))
    salary_results = list(ddgs.text("React Next.js salary India 2026", max_results=3))

jobs = "\\n".join([f"- {r['title']}: {r['body']}" for r in job_results])
salary = "\\n".join([f"- {r['title']}: {r['body']}" for r in salary_results])

# STEP 2: Feed real data to the LLM for reasoning
response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {"role": "system", "content": "You are a career advisor. Use the data provided."},
        {"role": "user", "content": f"Question: {question}\\n\\nJOB DATA:\\n{jobs}\\n\\nSALARY DATA:\\n{salary}"}
    ],
    max_tokens=500
)
print(response.choices[0].message.content)""",
        filename="level4_agent.py",
        replicate_steps=[
            "Install: <code>pip install groq duckduckgo-search</code>",
            "Replace <code>YOUR_KEY</code> with your Groq API key",
            "Run: <code>python level4_agent.py</code>",
            "<strong>Key concept:</strong> Search the web FIRST, then feed real data into the LLM. The model reasons over fresh data instead of stale training data.",
            "Change the search queries to match any question you want to research",
        ]
    )
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 3 - EMBEDDINGS
# ================================================================
elif current == "Demo 3: Embeddings":
    n = slide_start("Demo 3: Embeddings", "GPS for meaning", sn, TOTAL)
    
    default_sentences = [
        "I love programming in Python",
        "Python coding is my passion",
        "I enjoy writing Python code",
        "The weather today is sunny and warm",
        "It's a beautiful day outside",
        "My cat is sleeping on the couch",
    ]
    sentences_input = st.text_area("Sentences (one per line):", value="\n".join(default_sentences), height=160)
    sentences = [s.strip() for s in sentences_input.strip().split("\n") if s.strip()]
    
    if st.button("Compute Embeddings and Similarity", use_container_width=True):
        with st.spinner("Computing..."):
            from sentence_transformers import SentenceTransformer
            import numpy as np
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(sentences)
            
            st.markdown(f"**Each sentence becomes {embeddings.shape[1]} numbers**")
            st.code(f"'{sentences[0]}' => {embeddings[0][:8].round(4).tolist()} ...", language=None)
        
        st.markdown("### Similarity Scores")
        import numpy as np
        for i in range(len(sentences)):
            for j in range(i+1, min(len(sentences), i+3)):
                score = float(np.dot(embeddings[i], embeddings[j]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])))
                bar_len = int(score * 30)
                color = "#22c55e" if score > 0.6 else "#EF3837" if score < 0.3 else "#f59e0b"
                bar = f'<span style="color:{color};font-family:monospace;">{"#" * bar_len}{"." * (30 - bar_len)}</span>'
                st.markdown(f'`{score:.3f}` {bar} **{sentences[i][:35]}** vs **{sentences[j][:35]}**', unsafe_allow_html=True)
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 3 CODE
# ================================================================
elif current == "Demo 3: Code Behind":
    n = slide_start("Demo 3: The Code", "Text to numbers to meaning", sn, TOTAL)
    code_editor(
        code="""from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # downloads ~80MB first time

sentences = [
    "I love programming in Python",
    "Python coding is my passion",
    "My cat is sleeping on the couch",
]

embeddings = model.encode(sentences)  # Each sentence -> 384 numbers

print(f"Shape: {embeddings.shape}")   # (3, 384)

# Cosine similarity: how close are two meaning-vectors?
def similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"Python vs Python passion: {similarity(embeddings[0], embeddings[1]):.3f}")  # ~0.92
print(f"Python vs cat sleeping:   {similarity(embeddings[0], embeddings[2]):.3f}")  # ~0.08""",
        filename="embeddings_demo.py",
        replicate_steps=[
            "Install: <code>pip install sentence-transformers numpy</code>",
            "Run: <code>python embeddings_demo.py</code> (first run downloads the model ~80MB)",
            "<strong>Key concept:</strong> Embeddings convert text into vectors that capture meaning. Similar text = similar vectors.",
            "Cosine similarity ranges from -1 (opposite) to 1 (identical meaning)",
            "Try your own sentences -- song lyrics, code comments, anything",
        ]
    )
    slide_end(n)

# ================================================================
#  SLIDE: FEEDBACK 1 (11:00 AM)
# ================================================================
elif current == "⚡ Feedback 1":
    render_feedback_slide(1, None, sn, TOTAL)

# ================================================================
#  SLIDE: QUIZ 1
# ================================================================
elif current == "Quiz 1: Agents Basics":
    n = slide_start("Quiz 1: AI Agents Basics", "Let's check what you've learned so far", sn, TOTAL)
    
    q1 = st.radio("**1. What are the 4 parts of an AI Agent?**", [
        "A) Input, Output, Model, Database",
        "B) Brain (LLM), Memory (RAG), Tools, Orchestrator",
        "C) Frontend, Backend, API, Database",
        "D) Prompt, Response, Context, History"
    ], key="q1_1")
    
    q2 = st.radio("**2. What's the difference between ChatGPT and an AI Agent?**", [
        "A) Nothing, they're the same",
        "B) ChatGPT is smarter",
        "C) An agent can use tools and act autonomously",
        "D) An agent is always better"
    ], key="q1_2")
    
    q3 = st.radio("**3. In the CEO analogy, what is the 'orchestrator'?**", [
        "A) The AI model itself",
        "B) The database",
        "C) The logic that decides WHAT to do WHEN",
        "D) The user interface"
    ], key="q1_3")
    
    if st.button("Check Answers", key="c1"):
        score = sum([
            1 if st.session_state.get("q1_1","").startswith("B") else 0,
            1 if st.session_state.get("q1_2","").startswith("C") else 0,
            1 if st.session_state.get("q1_3","").startswith("C") else 0,
        ])
        if score == 3:
            st.balloons()
            st.success(f"Score: {score}/3 -- Perfect!")
        elif score >= 2:
            st.info(f"Score: {score}/3 -- Almost there!")
        else:
            st.warning(f"Score: {score}/3 -- Review the demos.")
        with st.expander("Correct answers"):
            st.markdown("""
            1. **B)** Brain (LLM), Memory (RAG), Tools, Orchestrator
            2. **C)** An agent can use tools and act autonomously
            3. **C)** The logic that decides WHAT to do WHEN
            """)
    slide_end(n)

# ================================================================
#  SLIDE: DEMO 4 - RAG
# ================================================================
elif current == "Demo 4: RAG Pipeline":
    n = slide_start("Demo 4: RAG Pipeline", "Chat with your own notes", sn, TOTAL)
    
    default_notes = """Arrays store elements in contiguous memory. O(1) access by index.
Stacks follow LIFO. Push/Pop are O(1). Used in function calls, undo operations.
Queues follow FIFO. Enqueue/Dequeue are O(1). Used in BFS, print spooling.
Binary Search Trees: O(log n) average search/insert/delete.
BFS uses a queue -- shortest path in unweighted graphs. DFS uses stack/recursion -- cycle detection.
Dynamic Programming: overlapping subproblems + optimal substructure. Memoization vs tabulation.
Hash tables: O(1) average lookup. Collisions handled by chaining or open addressing.
REST APIs: GET (read), POST (create), PUT (update), DELETE (remove). JSON format."""
    
    notes = st.text_area("Your Knowledge Base (one topic per line):", value=default_notes, height=180)
    
    if st.button("Load into Vector DB", use_container_width=True):
        import chromadb
        docs = [n.strip() for n in notes.strip().split("\n") if n.strip()]
        client = chromadb.Client()
        try: client.delete_collection("demo_rag")
        except: pass
        collection = client.create_collection("demo_rag")
        collection.add(documents=docs, ids=[f"d_{i}" for i in range(len(docs))])
        st.session_state.rag_collection = collection
        st.session_state.rag_ready = True
        st.success(f"Loaded {len(docs)} documents into vector DB!")
    
    if st.session_state.get('rag_ready'):
        st.markdown("---")
        query = st.text_input("Ask your notes:", value="When should I use a stack vs a queue?")
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("Ask (RAG)", use_container_width=True):
                if not st.session_state.groq_key:
                    st.error("Set API key first!")
                else:
                    collection = st.session_state.rag_collection
                    with st.status("RAG Pipeline...", expanded=True) as status:
                        st.write("1. Embedding question...")
                        st.write("2. Searching vector DB...")
                        results = collection.query(query_texts=[query], n_results=2)
                        for i, (doc, dist) in enumerate(zip(results['documents'][0], results['distances'][0])):
                            st.write(f"Match {i+1} (relevance: {1-dist:.2f}): {doc[:80]}...")
                        context = "\n---\n".join(results['documents'][0])
                        st.write("3. Sending to LLM...")
                        from groq import Groq
                        client = Groq(api_key=st.session_state.groq_key)
                        resp = client.chat.completions.create(
                            model="qwen/qwen3.8-27b",
                            messages=[
                                {"role": "system", "content": "Answer ONLY from the provided notes. If not covered, say 'Not in your notes yet!'"},
                                {"role": "user", "content": f"NOTES:\n{context}\n\nQUESTION: {query}"}
                            ],
                            max_tokens=300, temperature=0.3
                        )
                        status.update(label="Done!", state="complete")
                    st.markdown(f'<div class="demo-output">{resp.choices[0].message.content}</div>', unsafe_allow_html=True)
        
        with col_b:
            trick_q = st.text_input("Try to break it:", value="What's Instagram's algorithm?")
            if st.button("Ask (should fail gracefully)", key="trick"):
                collection = st.session_state.rag_collection
                results = collection.query(query_texts=[trick_q], n_results=2)
                context = "\n---\n".join(results['documents'][0])
                from groq import Groq
                client = Groq(api_key=st.session_state.groq_key)
                resp = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": "Answer ONLY from the provided notes. If not covered, say 'That's not in your notes yet! Here's what IS related...'"},
                        {"role": "user", "content": f"NOTES:\n{context}\n\nQUESTION: {trick_q}"}
                    ],
                    max_tokens=200, temperature=0.3
                )
                st.info(resp.choices[0].message.content)
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 4 CODE
# ================================================================
elif current == "Demo 4: Code Behind":
    n = slide_start("Demo 4: The Code", "Complete RAG in 30 lines", sn, TOTAL)
    code_editor(
        code="""import chromadb
from groq import Groq

# STEP 1: Create vector database
chroma = chromadb.Client()
collection = chroma.create_collection("my_notes")

# STEP 2: Add documents (embeddings created automatically)
notes = [
    "Arrays: O(1) access by index. Contiguous memory.",
    "Stacks: LIFO. Push/Pop O(1). Used in function calls.",
    "Queues: FIFO. Used in BFS and request handling.",
    "Hash tables: O(1) average lookup via hash functions.",
]
collection.add(documents=notes, ids=[f"doc_{i}" for i in range(len(notes))])

# STEP 3: Search by meaning
results = collection.query(query_texts=["When to use a stack?"], n_results=2)
context = "\\n".join(results['documents'][0])

# STEP 4: Generate answer from retrieved context
client = Groq(api_key="YOUR_KEY")
response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {"role": "system", "content": "Answer ONLY from the notes provided."},
        {"role": "user", "content": f"NOTES:\\n{context}\\n\\nQ: When to use a stack?"}
    ],
    max_tokens=300, temperature=0.3
)
print(response.choices[0].message.content)""",
        filename="rag_pipeline.py",
        replicate_steps=[
            "Install: <code>pip install chromadb groq</code>",
            "Replace <code>YOUR_KEY</code> with your Groq API key",
            "Run: <code>python rag_pipeline.py</code>",
            "<strong>RAG = Retrieval Augmented Generation:</strong> Store docs in vector DB, search by meaning, feed relevant context to LLM",
            "ChromaDB handles embeddings internally -- no manual vector math needed",
            "Try replacing the notes with YOUR study material",
        ]
    )
    slide_end(n)

# ================================================================
#  SLIDE: DEMO 5 - NO CODE
# ================================================================
elif current == "Demo 5: No-Code Agent":
    n = slide_start("Demo 5: No-Code Agent", "Dify.ai -- full agent, zero code", sn, TOTAL)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.link_button("Open Dify.ai", "https://cloud.dify.ai", use_container_width=True)
    with col2: st.link_button("Dify Docs", "https://docs.dify.ai", use_container_width=True)
    with col3: st.link_button("Get Groq Key", "https://console.groq.com", use_container_width=True)
    
    st.markdown("### Live Demo Steps")
    for i, step in enumerate([
        "Create from Blank > Select **Agent** (not Chatbot)",
        "Name it **PlacePrep AI**",
        "Paste the system prompt below",
        "Add Tools: **DuckDuckGo + Wikipedia + Calculator**",
        "Create Knowledge Base > Upload a DSA PDF",
        "Connect Knowledge Base to Agent",
        "Test: *'I have a Google interview in 2 weeks'*",
        "Publish > Get shareable URL",
    ], 1):
        st.checkbox(f"**Step {i}:** {step}", key=f"dify_{i}")
    
    st.markdown("### System Prompt:")
    code_editor(
        code="""You are PlacePrep AI, a brutally honest but encouraging placement 
preparation coach for Computer Science students in India.

Be direct. Use analogies. If code is wrong, say so -- explain the fix. 
Always end with a motivational one-liner.

When asked about a specific company, SEARCH THE WEB first for 
their latest interview process before answering.""",
        filename="system_prompt.txt",
        language=None,
        replicate_steps=[
            "Copy this into Dify.ai's Instructions field",
            "The prompt defines personality AND when to use tools",
            "Customize for any use case: tutor, coach, recruiter bot",
        ]
    )
    slide_end(n)
    

# ================================================================
#  SLIDE: FEEDBACK 2 (1:00 PM — Before Lunch)
# ================================================================
elif current == "⚡ Feedback 2":
    render_feedback_slide(2, None, sn, TOTAL)

# ================================================================
#  SLIDE: QUIZ 2
# ================================================================
elif current == "Quiz 2: RAG and Embeddings":
    n = slide_start("Quiz 2: RAG and Embeddings", None, sn, TOTAL)
    
    q1 = st.radio("**1. What does RAG stand for?**", [
        "A) Really Awesome Generator",
        "B) Retrieval Augmented Generation",
        "C) Random Answer Generator",
        "D) Recursive Algorithm Graph"
    ], key="q2_1")
    q2 = st.radio("**2. What are embeddings?**", [
        "A) Images in documents",
        "B) Code in HTML",
        "C) Numbers that capture the MEANING of text",
        "D) Links in websites"
    ], key="q2_2")
    q3 = st.radio("**3. Why use a Vector Database?**", [
        "A) Regular DBs can't store text",
        "B) To search by MEANING instead of keywords",
        "C) It's faster than everything",
        "D) It's required by law"
    ], key="q2_3")
    q4 = st.radio("**4. RAG question NOT in documents?**", [
        "A) AI crashes",
        "B) AI hallucinates",
        "C) Good RAG says 'I don't have that info'",
        "D) Searches Google instead"
    ], key="q2_4")
    
    if st.button("Check Answers", key="c2"):
        score = sum([
            1 if st.session_state.get("q2_1","").startswith("B") else 0,
            1 if st.session_state.get("q2_2","").startswith("C") else 0,
            1 if st.session_state.get("q2_3","").startswith("B") else 0,
            1 if st.session_state.get("q2_4","").startswith("C") else 0,
        ])
        if score == 4:
            st.balloons()
            st.success(f"Score: {score}/4 -- RAG Master!")
        elif score >= 3: st.info(f"Score: {score}/4 -- Solid!")
        else: st.warning(f"Score: {score}/4 -- Review the RAG demo.")
        with st.expander("Correct answers"):
            st.markdown("1. **B** Retrieval Augmented Generation\n2. **C** Numbers capturing meaning\n3. **B** Search by meaning\n4. **C** Says 'I don't have that info'")
    slide_end(n)

# ================================================================
#  SLIDE: ACTIVITY 1
# ================================================================
elif current == "Activity 1: Prompt Engineering":
    n = slide_start("Activity 1: Prompt Engineering Challenge", "15 minutes", sn, TOTAL)
    
    st.markdown("""
    <div class="activity-card">
        <h4>CHALLENGE: Write the best system prompt</h4>
        <ol>
            <li>Make sure your API key works (Setup slide)</li>
            <li>Write a custom system prompt below</li>
            <li>Make the AI act as: a strict Indian parent, a Silicon Valley VC, OR a drill sergeant reviewing a resume</li>
            <li>Test it. Iterate. Make it funnier / more useful.</li>
            <li>Best result wins -- share with the group.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    custom_prompt = st.text_area("Your system prompt:", height=120,
        placeholder="You are a strict Indian parent looking at your child's resume...")
    custom_resume = st.text_area("Resume to test:", height=120, key="a1r",
        placeholder="Paste a resume here...")
    
    if st.button("Test Your Prompt", use_container_width=True):
        if not st.session_state.groq_key:
            st.error("Set API key first!")
        elif not custom_prompt or not custom_resume:
            st.error("Fill in both fields!")
        else:
            from groq import Groq
            client = Groq(api_key=st.session_state.groq_key)
            with st.spinner("Running..."):
                resp = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": custom_prompt},
                        {"role": "user", "content": f"Review this resume:\n{custom_resume}"}
                    ],
                    temperature=0.85, max_tokens=500
                )
            st.markdown(f'<div class="demo-output">{resp.choices[0].message.content}</div>', unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: DEMO 6 - CODE AGENT
# ================================================================
elif current == "Demo 6: Code Agent":
    n = slide_start("Demo 6: Code Agent with Tools", "Watch it DECIDE", sn, TOTAL)
    
    query = st.text_input("Ask the agent:", value="What is 847 * 293 and what are the latest trends in AI agents?")
    
    if st.button("Run Agent", use_container_width=True):
        if not st.session_state.groq_key:
            st.error("Set API key first!")
        else:
            from groq import Groq
            from duckduckgo_search import DDGS
            client = Groq(api_key=st.session_state.groq_key)
            
            def calculator(expr):
                try:
                    allowed = set('0123456789+-*/.() ')
                    return str(eval(expr)) if all(c in allowed for c in expr) else "Invalid"
                except Exception as e: return str(e)
            
            def web_search(q):
                try:
                    with DDGS() as ddgs:
                        return "\n".join([f"- {r['title']}: {r['body']}" for r in ddgs.text(q, max_results=3)])
                except: return "Search unavailable"
            
            TOOLS = {
                "calculator": {"fn": calculator, "desc": "Math. Input: '25*4'"},
                "web_search": {"fn": web_search, "desc": "Search internet. Input: query"},
            }
            tools_text = "\n".join([f"- {k}: {v['desc']}" for k, v in TOOLS.items()])
            messages = [
                {"role": "system", "content": f"You are an AI agent with tools:\n{tools_text}\n\nTo use a tool: ACTION: tool_name | input\nAfter results, give final answer. If no tool needed, answer directly."},
                {"role": "user", "content": query}
            ]
            
            with st.status("Agent working...", expanded=True) as status:
                for step in range(4):
                    resp = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=500, temperature=0.2)
                    reply = resp.choices[0].message.content
                    if "ACTION:" in reply:
                        action_line = [l for l in reply.split('\n') if 'ACTION:' in l][0]
                        parts = action_line.split("ACTION:")[1].strip().split("|", 1)
                        tool_name = parts[0].strip()
                        tool_input = parts[1].strip() if len(parts) > 1 else ""
                        st.write(f"**Step {step+1}:** Using `{tool_name}` with `{tool_input}`")
                        result = TOOLS[tool_name]["fn"](tool_input) if tool_name in TOOLS else "Unknown tool"
                        st.code(result[:300], language=None)
                        messages.append({"role": "assistant", "content": reply})
                        messages.append({"role": "user", "content": f"Tool result: {result}\nContinue or give final answer."})
                    else:
                        status.update(label="Agent done!", state="complete")
                        st.markdown(f'<div class="demo-output"><strong>Final Answer:</strong><br><br>{reply}</div>', unsafe_allow_html=True)
                        break
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 6 CODE
# ================================================================
elif current == "Demo 6: Code Behind":
    n = slide_start("Demo 6: The Code", "The agent loop pattern", sn, TOTAL)
    code_editor(
        code="""from groq import Groq
from duckduckgo_search import DDGS

client = Groq(api_key="YOUR_KEY")

# --- Tools ---
def calculator(expr):
    allowed = set('0123456789+-*/.() ')
    return str(eval(expr)) if all(c in allowed for c in expr) else "Invalid"

def web_search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        return "\\n".join([f"- {r['title']}: {r['body']}" for r in results])

TOOLS = {"calculator": calculator, "web_search": web_search}

# --- Agent loop ---
messages = [
    {"role": "system", "content": \"\"\"You are an AI agent with tools:
- calculator: Math like '25*4'
- web_search: Search the internet
To use: ACTION: tool_name | input
After results, give final answer.\"\"\"},
    {"role": "user", "content": "What is 847*293 and latest AI trends?"}
]

for step in range(5):
    resp = client.chat.completions.create(
        model="qwen/qwen3.8-27b", messages=messages,
        max_tokens=500, temperature=0.2
    )
    reply = resp.choices[0].message.content
    print(f"Step {step+1}: {reply[:100]}...")

    if "ACTION:" in reply:
        line = [l for l in reply.split('\\n') if 'ACTION:' in l][0]
        parts = line.split("ACTION:")[1].strip().split("|", 1)
        name, inp = parts[0].strip(), parts[1].strip() if len(parts)>1 else ""
        result = TOOLS[name](inp)
        print(f"  Tool result: {result[:100]}")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"Tool result: {result}"})
    else:
        print(f"\\nFINAL: {reply}")
        break""",
        filename="code_agent.py",
        replicate_steps=[
            "Install: <code>pip install groq duckduckgo-search</code>",
            "Run: <code>python code_agent.py</code>",
            "<strong>The Agent Loop:</strong> Ask LLM > if it wants a tool > run tool > feed result back > repeat until final answer",
            "The LLM DECIDES which tool. You don't hard-code the logic.",
            "Add your own tools: weather API, GPA calculator, file reader, anything",
            "Production agents use JSON function calling instead of text parsing",
        ]
    )
    slide_end(n)

# ================================================================
#  SLIDE: DEMO 7 - GRADIO
# ================================================================
elif current == "Demo 7: Gradio Deploy":
    n = slide_start("Demo 7: Deploy with Gradio", "Code + beautiful UI + public URL", sn, TOTAL)
    
    code_editor(
        code="""import gradio as gr
from groq import Groq
from duckduckgo_search import DDGS

client = Groq(api_key="YOUR_KEY")

def calculator(expr):
    allowed = set('0123456789+-*/.() ')
    return str(eval(expr)) if all(c in allowed for c in expr) else "Invalid"

def web_search(query):
    with DDGS() as ddgs:
        return "\\n".join([f"- {r['title']}: {r['body']}" for r in ddgs.text(query, max_results=3)])

TOOLS = {"calculator": calculator, "web_search": web_search}

def agent(message, history):
    messages = [
        {"role": "system", "content": "You are a helpful AI agent. Tools: calculator (math), web_search (internet). Use ACTION: tool | input"},
        {"role": "user", "content": message}
    ]
    for _ in range(3):
        resp = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=messages, max_tokens=500)
        reply = resp.choices[0].message.content
        if "ACTION:" not in reply:
            return reply
        line = [l for l in reply.split('\\n') if 'ACTION:' in l][0]
        parts = line.split("ACTION:")[1].strip().split("|", 1)
        name, inp = parts[0].strip(), parts[1].strip() if len(parts)>1 else ""
        result = TOOLS.get(name, lambda x: "Unknown tool")(inp)
        messages += [{"role": "assistant", "content": reply}, {"role": "user", "content": f"Result: {result}"}]
    return reply

demo = gr.ChatInterface(fn=agent, title="My AI Agent -- Built at SRM AP")
demo.launch(share=True)  # Gives a PUBLIC URL anyone can access!""",
        filename="gradio_agent.py",
        replicate_steps=[
            "Install: <code>pip install gradio groq duckduckgo-search</code>",
            "Replace <code>YOUR_KEY</code> with your Groq API key",
            "Run: <code>python gradio_agent.py</code>",
            "It prints a public URL like <code>https://xxxxx.gradio.live</code>",
            "Open that URL on your phone. Share with friends. It just works.",
            "<strong>Key concept:</strong> <code>gr.ChatInterface</code> wraps ANY function into a chat UI. <code>share=True</code> creates a public tunnel.",
        ]
    )
    
    st.markdown("""
    <div class="big-quote" style="font-size:1.2rem;">
        <strong>"How it looks":</strong> Pretty chat interface<br><br>
        <strong>"How it works":</strong> LLM + vector database + web search + tool orchestration<br>
        + 40 lines of Python
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)
    

# ================================================================
#  SLIDE: DEMO 7 - COLAB INSTRUCTIONS
# ================================================================
elif current == "Demo 7: Colab Instructions":
    n = slide_start("Running on Google Colab", "Step-by-step: from zero to public URL", sn, TOTAL)
    
    st.markdown("### Follow these steps exactly:")
    
    st.markdown("""
    **Step 1:** Open [colab.research.google.com](https://colab.research.google.com) and create a new notebook.
    
    **Step 2:** In the first cell, install dependencies:
    """)
    code_editor("!pip install gradio groq duckduckgo-search", filename="Cell 1 -- Install", replicate_steps=None)
    
    st.markdown("**Step 3:** In the second cell, paste the full agent code:")
    code_editor(
        code="""import gradio as gr
from groq import Groq
from duckduckgo_search import DDGS

# PUT YOUR KEY HERE
client = Groq(api_key="YOUR_GROQ_API_KEY")

def calculator(expr):
    allowed = set('0123456789+-*/.() ')
    return str(eval(expr)) if all(c in allowed for c in expr) else "Invalid"

def web_search(query):
    try:
        with DDGS() as ddgs:
            return "\\n".join([f"- {r['title']}: {r['body']}" for r in ddgs.text(query, max_results=3)])
    except:
        return "Search unavailable"

TOOLS = {"calculator": calculator, "web_search": web_search}

def agent(message, history):
    messages = [
        {"role": "system", "content": \"\"\"You are a helpful AI agent built at SRM AP.
Tools available:
- calculator: Math expressions like '25*4'
- web_search: Search the internet for current info
To use a tool: ACTION: tool_name | input
After getting results, give your final answer.\"\"\"},
        {"role": "user", "content": message}
    ]
    for _ in range(3):
        resp = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
            max_tokens=500,
            temperature=0.3
        )
        reply = resp.choices[0].message.content
        if "ACTION:" not in reply:
            return reply
        line = [l for l in reply.split('\\n') if 'ACTION:' in l][0]
        parts = line.split("ACTION:")[1].strip().split("|", 1)
        name = parts[0].strip()
        inp = parts[1].strip() if len(parts) > 1 else ""
        result = TOOLS.get(name, lambda x: "Unknown tool")(inp)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"Tool result: {result}"})
    return reply

demo = gr.ChatInterface(
    fn=agent,
    title="AI Agent -- Built at SRM AP Workshop",
    description="I can search the web, do math, and answer questions!",
    examples=[
        "What is 1847 * 293?",
        "What are the top AI trends right now?",
        "Compare React vs Next.js for freshers in India"
    ]
)

demo.launch(share=True, debug=True)""",
        filename="Cell 2 -- Agent + Gradio",
        replicate_steps=None
    )
    
    st.markdown("""
    **Step 4:** Replace `YOUR_GROQ_API_KEY` with your actual key from console.groq.com
    
    **Step 5:** Run both cells (Shift+Enter)
    
    **Step 6:** Wait for the output. You'll see:
    """)
    st.code("""Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://abc123def.gradio.live""", language=None)
    
    st.markdown("""
    **Step 7:** Click the **public URL**. Open it on your phone. Share it with the person next to you.
    
    **That's it.** Your AI agent is live on the internet.
    
    ---
    
    **Troubleshooting:**
    - If `share=True` doesn't work on Colab, the local URL still works within the notebook
    - If you get rate limited, wait 60 seconds (free tier: 30 req/min)
    - If search fails, the agent still works -- it just can't search the web
    """)
    slide_end(n)
    

# ================================================================
#  SLIDE: FEEDBACK 3 (3:30 PM — Final)
# ================================================================
elif current == "⚡ Feedback 3":
    render_feedback_slide(3, None, sn, TOTAL)

# ================================================================
#  SLIDE: QUIZ 3
# ================================================================
elif current == "Quiz 3: Building Agents":
    n = slide_start("Quiz 3: Building Agents", None, sn, TOTAL)
    
    q1 = st.radio("**1. When to use no-code (Dify.ai)?**", [
        "A) Always",
        "B) Quick prototyping and simple agents",
        "C) Only for frontend",
        "D) Never"
    ], key="q3_1")
    q2 = st.radio("**2. Agent vs chatbot?**", [
        "A) Agents cost more",
        "B) Agents use tools and decide autonomously",
        "C) Agents are always smarter",
        "D) No difference"
    ], key="q3_2")
    q3 = st.radio("**3. 'Hybrid' approach means?**", [
        "A) Two AI models",
        "B) No-code prototyping + code for full control",
        "C) Cloud + local",
        "D) Python + JavaScript"
    ], key="q3_3")
    
    if st.button("Check Answers", key="c3"):
        score = sum([
            1 if st.session_state.get("q3_1","").startswith("B") else 0,
            1 if st.session_state.get("q3_2","").startswith("B") else 0,
            1 if st.session_state.get("q3_3","").startswith("B") else 0,
        ])
        if score == 3:
            st.balloons()
            st.success(f"Score: {score}/3 -- Ready to build!")
        else: st.info(f"Score: {score}/3")
        with st.expander("Correct answers"):
            st.markdown("1. **B** Quick prototyping\n2. **B** Tools + autonomous decisions\n3. **B** No-code prototype, then code for production")
    slide_end(n)

# ================================================================
#  SLIDE: ACTIVITY 2
# ================================================================
elif current == "Activity 2: Build a RAG":
    n = slide_start("Activity 2: Build Your Own RAG", "25 minutes", sn, TOTAL)
    st.markdown("""
    <div class="activity-card">
        <h4>CHALLENGE: RAG over YOUR content</h4>
        <ol>
            <li>Choose a domain: your course notes, club FAQ, a topic you're studying</li>
            <li>Write 8-10 knowledge chunks (one fact per line)</li>
            <li>Go to the RAG Pipeline slide and paste your content</li>
            <li>Load it into the vector DB</li>
            <li>Test with 3 answerable questions + 2 unanswerable ones</li>
            <li>Does it answer correctly? Does it refuse gracefully?</li>
            <li>Bonus: Can you trick it into hallucinating?</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Template:")
    code_editor(
        code="""# Replace with YOUR content -- one fact per line

Our coding club meets every Wednesday at 5 PM in Room 301.
Membership fee is Rs 200 per semester.
We host a monthly hackathon called CodeSprint.
The club president is Arun Kumar, 3rd year CSE.
To join, fill the form at srmap.club/coding.
We teach Python, JavaScript, and competitive programming.
Last year we won 3 inter-college hackathons.
No prior coding experience required to join.""",
        filename="my_knowledge.txt", language=None,
        replicate_steps=[
            "Write one clear fact per line",
            "More specific = better retrieval",
            "Aim for 8-15 chunks",
            "Paste into the RAG Pipeline demo slide",
        ]
    )
    slide_end(n)

# ================================================================
#  SLIDE: ACTIVITY 3
# ================================================================
elif current == "Activity 3: Build an Agent":
    n = slide_start("Activity 3: Custom Agent Tool", "30 minutes", sn, TOTAL)
    st.markdown("""
    <div class="activity-card">
        <h4>CHALLENGE: Add a custom tool to the agent</h4>
        <ol>
            <li>Start with the agent code from Demo 6</li>
            <li>Write a new tool function (ideas below)</li>
            <li>Add it to the TOOLS dictionary</li>
            <li>Update the system prompt</li>
            <li>Test with questions that need your tool</li>
            <li>Bonus: Chain two tools in one query</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    code_editor(
        code="""# Example custom tool: GPA Calculator

def gpa_calculator(grades_str):
    \"\"\"Input: 'A,B+,A-,B,A'\"\"\"
    points = {'A+':10,'A':9,'A-':8.5,'B+':8,'B':7,'B-':6.5,'C':5,'D':4,'F':0}
    grades = [g.strip() for g in grades_str.split(',')]
    vals = [points.get(g, 0) for g in grades]
    return f"GPA: {sum(vals)/len(vals):.2f} from {len(grades)} courses"

# Add to TOOLS dict:
TOOLS["gpa_calculator"] = gpa_calculator

# Update system prompt to include:
# - gpa_calculator: Calculate GPA. Input: comma-separated grades like 'A,B+,A-'""",
        filename="custom_tool.py",
        replicate_steps=[
            "Copy the agent code from Demo 6",
            "Add your tool function",
            "Register in TOOLS dictionary",
            "Update system prompt",
            "Tool ideas: unit converter, todo manager, quiz generator, dictionary lookup",
        ]
    )
    slide_end(n)

# ================================================================
#  SLIDE: ACTIVITY 4 - HACKATHON
# ================================================================
elif current == "Activity 4: Hackathon":
    n = slide_start("Mini Hackathon", "45 minutes -- Ship something real", sn, TOTAL)
    st.markdown("""
    <div class="activity-card">
        <h4>BUILD and DEPLOY a complete AI agent</h4>
        <ol>
            <li>Teams of 2-3</li>
            <li>Pick a problem (ideas below)</li>
            <li>No-code (Dify) for speed OR Python for control</li>
            <li>Build it. 45 minutes.</li>
            <li>Deploy: Dify URL or Gradio public link</li>
            <li>2-minute demo to the group</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Usefulness (40%)**\n\nDoes it solve a real problem?")
    with col2:
        st.markdown("**Technical depth (30%)**\n\nTools? RAG? Smart logic?")
    with col3:
        st.markdown("**Demo quality (30%)**\n\nClear? Live demo works?")
    
    st.markdown("---")
    st.markdown("### Project Ideas")
    for name, desc in {
        "PlacePrep Coach": "RAG over interview questions + web search for latest patterns",
        "Study Buddy": "RAG over course notes + quiz generation",
        "Campus Navigator": "Knowledge base of locations, events, contacts",
        "Code Reviewer": "Reviews code for bugs, style, best practices",
        "Research Summarizer": "RAG over papers + Q&A",
        "Event Planner": "Web search for venues + budget calculator",
    }.items():
        st.markdown(f"**{name}:** {desc}")
    slide_end(n)

# ================================================================
#  SLIDE: FINAL QUIZ
# ================================================================
elif current == "Final Quiz":
    n = slide_start("Final Quiz: Are You a CEO?", None, sn, TOTAL)
    
    q1 = st.radio("**1. AI that answers from YOUR college notes. You need:**", [
        "A) A bigger LLM",
        "B) RAG -- embed notes in vector DB, retrieve chunks",
        "C) Fine-tune GPT-4 on your notes",
        "D) Copy-paste into ChatGPT every time"
    ], key="qf_1")
    q2 = st.radio("**2. Agent needs today's weather. It needs:**", [
        "A) A newer model",
        "B) A TOOL -- a weather API it can call",
        "C) More training data",
        "D) Bigger context window"
    ], key="qf_2")
    q3 = st.radio("**3. Most important skill in the AI era:**", [
        "A) Memorizing algorithms",
        "B) Writing perfect prompts",
        "C) Orchestrating AI -- knowing what to build and how to connect tools",
        "D) Using ChatGPT faster"
    ], key="qf_3")
    
    if st.button("Am I a CEO?", key="cf"):
        score = sum([
            1 if st.session_state.get("qf_1","").startswith("B") else 0,
            1 if st.session_state.get("qf_2","").startswith("B") else 0,
            1 if st.session_state.get("qf_3","").startswith("C") else 0,
        ])
        if score == 3:
            st.balloons()
            st.success("3/3 -- You ARE a CEO of Superintelligence!")
        elif score >= 2:
            st.info(f"{score}/3 -- Almost!")
        else:
            st.warning(f"{score}/3 -- Review the modules.")
        with st.expander("Correct answers"):
            st.markdown("1. **B** RAG\n2. **B** A tool (API)\n3. **C** Orchestrating AI")
    slide_end(n)

# ================================================================
#  SLIDE: QUICK LINKS
# ================================================================
elif current == "Quick Links":
    n = slide_start("Quick Links", None, sn, TOTAL)
    
    st.markdown("### Tools")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.link_button("Dify.ai", "https://cloud.dify.ai", use_container_width=True)
    with c2: st.link_button("Groq Console", "https://console.groq.com", use_container_width=True)
    with c3: st.link_button("Google Colab", "https://colab.research.google.com", use_container_width=True)
    with c4: st.link_button("Gradio", "https://gradio.app", use_container_width=True)
    
    st.markdown("### Learning")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.link_button("DeepLearning.AI", "https://deeplearning.ai/courses", use_container_width=True)
    with c2: st.link_button("LangChain", "https://python.langchain.com", use_container_width=True)
    with c3: st.link_button("ChromaDB", "https://docs.trychroma.com", use_container_width=True)
    with c4: st.link_button("HuggingFace", "https://huggingface.co/spaces", use_container_width=True)
    
    st.markdown("### Workshop Materials")
    st.text_input("Lab 1 Colab:", key="l1l", placeholder="https://colab.research.google.com/...")
    st.text_input("Lab 2 Colab:", key="l2l", placeholder="https://colab.research.google.com/...")
    st.text_input("Feedback Form:", key="fbl", placeholder="https://forms.google.com/...")
    slide_end(n)

# ================================================================
#  SLIDE: TIMER
# ================================================================
elif current == "Timer":
    n = slide_start("Activity Timer", None, sn, TOTAL)
    c1, c2 = st.columns(2)
    with c1: mins = st.number_input("Minutes:", min_value=1, max_value=60, value=8)
    with c2: label = st.text_input("Activity:", value="Group Activity")
    
    if st.button("START TIMER", use_container_width=True):
        placeholder = st.empty()
        total_seconds = mins * 60
        for remaining in range(total_seconds, -1, -1):
            m, s = divmod(remaining, 60)
            color = "#22c55e" if remaining > 60 else "#f59e0b" if remaining > 15 else "#EF3837"
            msg = "TIME'S UP!" if remaining == 0 else "Go!" if remaining > 60 else "Wrapping up..." if remaining > 15 else "Almost done!"
            placeholder.markdown(f"""
            <div style="text-align:center; padding:60px 0;">
                <p style="font-size:1.5rem; color:#9ca3af;">{label}</p>
                <p style="font-size:10rem; font-weight:900; color:{color}; margin:0; font-family:'JetBrains Mono',monospace;">{m:02d}:{s:02d}</p>
                <p style="font-size:1.3rem; color:#9ca3af;">{msg}</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        st.balloons()
        st.success(f"Time's up! {label} complete!")
    slide_end(n)

# ================================================================
#  BOTTOM NAV (duplicate for easy access)
# ================================================================
st.markdown("---")
bl, bc, br = st.columns([1, 3, 1])
with bl:
    if st.button("< Previous ", use_container_width=True, disabled=(st.session_state.slide == 0), key="bp"):
        st.session_state.slide -= 1
        st.rerun()
with bc:
    st.markdown(f"<p style='text-align:center; color:#555; font-family:JetBrains Mono,monospace; padding-top:8px;'>{sn} / {TOTAL} -- {current}</p>", unsafe_allow_html=True)
with br:
    if st.button("Next > ", use_container_width=True, disabled=(st.session_state.slide == TOTAL - 1), key="bn"):
        st.session_state.slide += 1
        st.rerun()
