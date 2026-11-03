"""
CEO OF SUPERINTELLIGENCE -- Workshop Slide Deck (2nd Year Edition)
Toned down for beginners: fundamentals -> RAG intro -> no-code agent building
Run: streamlit run app_2ndyear.py
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
FEEDBACK_URL = os.environ.get("FEEDBACK_URL", "https://workshop-feedback-ismc.onrender.com")

# -- Page Config --
st.set_page_config(
    page_title="CEO of Superintelligence -- Workshop (2nd Year)",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -- Mega CSS --
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    .stApp { background-color: #0a0a0a; color: #e5e7eb; }
    .block-container { padding-top: 2.5rem !important; padding-bottom: 0 !important; max-width: 1100px; margin: 0 auto; }
    header[data-testid="stHeader"] { background: #0a0a0a; height: 0px !important; min-height: 0px !important; }
    
    .slide-frame {
        background: #111;
        border: 1px solid #2a0a0a;
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
        color: #ffffff;
        margin-top: 18px;
    }
    .slide-frame p, .slide-frame li {
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #ffffff;
    }
    .slide-subtitle {
        font-size: 1.3rem;
        color: #cccccc;
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
    
    .big-quote {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        padding: 32px 0;
        line-height: 1.6;
    }
    .big-quote em { color: #EF3837; font-style: normal; }
    
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
    .level-card .role { color: #cccccc; font-size: 0.85rem; margin: 0; }
    .level-card .phrase { color: #ffffff; font-size: 0.95rem; margin-top: 8px; }
    
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
    .code-editor-body { background: #1e1e1e; padding: 0; }
    .replicate-bar {
        background: #161616;
        border-top: 1px dashed #333;
        padding: 14px 20px;
        color: #cccccc;
        font-size: 0.88rem;
        line-height: 1.7;
    }
    .replicate-bar strong { color: #EF3837; }
    .replicate-bar code {
        background: #222;
        padding: 2px 7px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        color: #ffffff;
        font-size: 0.84rem;
    }
    
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
    
    .quiz-container {
        background: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 14px;
        padding: 24px;
        margin: 12px 0;
    }
    
    .activity-card {
        background: linear-gradient(135deg, #0d0d0d, #1a0a0a);
        border: 2px solid #EF3837;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }
    .activity-card h4 { color: #EF3837; margin-top: 0; }
    
    .demo-output {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 24px;
        margin: 14px 0;
    }
    
    .concept-card {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 24px;
        margin: 12px 0;
        text-align: left;
    }
    .concept-card h4 { color: #EF3837; margin-top: 0; }
    
    .analogy-box {
        background: linear-gradient(135deg, #111, #1a0a0a);
        border: 1px solid #EF3837;
        border-radius: 14px;
        padding: 24px;
        margin: 14px 0;
        text-align: left;
    }
    .analogy-box h4 { color: #EF3837; margin-top: 0; }
    
    section[data-testid="stSidebar"] { background-color: #0d0d0d; }
</style>
""", unsafe_allow_html=True)

# ================================================================
#  HELPERS
# ================================================================

def code_editor(code, filename="main.py", language="python", replicate_steps=None):
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
            <strong>Try it yourself:</strong><br><br>
            {steps_html}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def generate_qr(url):
    if not QR_AVAILABLE:
        return None
    qr = qrcode.QRCode(version=1, box_size=10, border=2,
                        error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="white", back_color="#111111")


def load_feedback_stats():
    try:
        resp = requests.get(f"{FEEDBACK_URL}/api/stats", timeout=3)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return {
        "round_1": {"count": 0, "avg_rating": 0, "entries": []},
        "round_2": {"count": 0, "avg_rating": 0, "entries": []},
        "round_3": {"count": 0, "avg_rating": 0, "entries": []},
    }


def render_feedback_slide(round_num, slide_num_html, sn, TOTAL):
    round_key = f"round_{round_num}"
    round_labels = {1: "First Impressions", 2: "Midway Check", 3: "Final Pulse"}
    
    n = slide_start(f"Live Feedback — Round {round_num}", round_labels.get(round_num, ""), sn, TOTAL)
    
    url = f"{FEEDBACK_URL}/round/{round_num}"
    
    col_qr, col_stats = st.columns([1, 1])
    
    with col_qr:
        st.markdown(f"""
        <div style="text-align:center; padding: 10px 0;">
            <p style="font-size:1.3rem; color:#cccccc; margin-bottom:8px;">Scan with your phone</p>
            <p style="font-size:0.85rem; color:#555; margin-bottom:12px;">Works on <strong style='color:#EF3837;'>any network</strong> — mobile data is fine.</p>
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
        
        rating_label = {1: "Low", 2: "Fair", 3: "Good", 4: "Great", 5: "Excellent"}
        avg_label = rating_label.get(round(avg) if avg else 3, "Good")
        
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0;">
            <p style="font-size:5rem; font-weight:900; color:#22c55e; margin:0; font-family:'JetBrains Mono',monospace;">{count}</p>
            <p style="font-size:1.2rem; color:#cccccc;">responses received</p>
        </div>
        """, unsafe_allow_html=True)
        
        if avg > 0:
            st.markdown(f"""
            <div style="text-align:center; padding:10px 0;">
                <p style="font-size:2rem; margin:0; color:#ffffff; font-weight:700;">{avg_label}</p>
                <p style="font-size:1.1rem; color:#cccccc;">Average: <strong style="color:#EF3837;">{avg}/5</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        if rd["entries"]:
            recent = rd["entries"][-8:]
            names = " | ".join([f"{e['name']} ({e['rating']}/5)" for e in reversed(recent)])
            st.markdown(f"""
            <div style="text-align:center; padding:12px 0;">
                <p style="color:#555; font-size:0.8rem; margin-bottom:4px;">RECENT</p>
                <p style="color:#cccccc; font-size:0.95rem;">{names}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("Refresh Count", use_container_width=True, key=f"refresh_fb_{round_num}"):
        st.rerun()
    
    if rd["entries"]:
        with st.expander(f"View All {count} Responses"):
            for e in reversed(rd["entries"]):
                fb_text = f' — "{e["feedback"]}"' if e.get("feedback") else ""
                st.markdown(f"**{e['name']}** ({e['rating']}/5){fb_text}")
    
    slide_end(n)


def slide_start(title, subtitle=None, slide_num=None, total=None):
    sub = f'<p class="slide-subtitle">{subtitle}</p>' if subtitle else ""
    num = f'<div class="slide-number">{slide_num} / {total}</div>' if slide_num else ""
    st.markdown(f"""<div class="slide-frame">
        <h1>{title}</h1>{sub}""", unsafe_allow_html=True)
    return num


def slide_end(num_html=""):
    st.markdown(f"""{num_html}</div>""", unsafe_allow_html=True)


# ================================================================
#  SLIDE DEFINITIONS (2nd Year -- Beginner Friendly)
# ================================================================
SLIDES = [
    "Title",
    "The 5 Levels",
    "What is AI Really?",
    "How LLMs Work",
    "Setup",
    "Demo 1: Roast My Insta Bio",
    "Prompt Engineering 101",
    "Activity 1: Prompt Battle",
    "Feedback 1",
    "Quiz 1: AI Fundamentals",
    "What is RAG?",
    "Demo 2: RAG Pipeline",
    "Feedback 2",
    "Quiz 2: RAG Basics",
    "What are AI Agents?",
    "Demo 3: No-Code Agent (n8n)",
    "Activity 2: Build Your Agent",
    "Feedback 3",
    "Final Quiz",
    "What to Learn Next",
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
#  NAVIGATION BAR
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
                     "AI Agents Workshop — SRM AP x Kalvium — Nov 2026 (2nd Year Edition)", sn, TOTAL)
    st.markdown("""
    <div class="big-quote">
        Person at Level 1: "AI will take my job"<br><br>
        Person at Level 5: <em>"I just automated my job and started a side business"</em><br><br>
        Same AI. Different user. Different outcome.<br><br>
        <span style="font-size: 1rem; color: #cccccc;">Today's goal: Go from Level 1 to Level 3 (and peek at Level 4)</span>
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: THE 5 LEVELS
# ================================================================
elif current == "The 5 Levels":
    n = slide_start("The 5 Levels of AI Users", "Where are you today?", sn, TOTAL)
    st.markdown("""
    <div class="level-grid">
        <div class="level-card active">
            <h4>Level 1</h4>
            <p class="role">Consumer</p>
            <p class="phrase">"Hey ChatGPT"</p>
        </div>
        <div class="level-card active">
            <h4>Level 2</h4>
            <p class="role">Prompter</p>
            <p class="phrase">"Think step by step"</p>
        </div>
        <div class="level-card active">
            <h4>Level 3</h4>
            <p class="role">Integrator</p>
            <p class="phrase">"Here's MY data"</p>
        </div>
        <div class="level-card">
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
    
    st.markdown("""
    <div class="analogy-box">
        <h4>Today's Journey</h4>
        <p><strong>Level 1 to 2:</strong> Learn how to talk to AI properly (prompt engineering)</p>
        <p><strong>Level 2 to 3:</strong> Feed AI YOUR data so it actually knows your stuff (RAG)</p>
        <p><strong>Peek at Level 4:</strong> Build a simple AI agent with no code</p>
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: WHAT IS AI REALLY?
# ================================================================
elif current == "What is AI Really?":
    n = slide_start("What is AI, Really?", "Busting the myths first", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>The Pizza Analogy</h4>
        <p><strong>AI</strong> = An entire restaurant (the broad field)</p>
        <p><strong>Machine Learning</strong> = The kitchen (learns from data)</p>
        <p><strong>Deep Learning</strong> = The oven (neural networks)</p>
        <p><strong>LLM (Large Language Model)</strong> = The pizza chef (specializes in language)</p>
        <p><strong>ChatGPT, Gemini, Claude</strong> = Different pizza brands (different LLMs packaged for you)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="concept-card">
            <h4>What AI is NOT</h4>
            <p>Not sentient or conscious</p>
            <p>Not "thinking" like humans</p>
            <p>Not always correct</p>
            <p>Not magic — it's math + data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-card">
            <h4>What AI actually IS</h4>
            <p>A very advanced pattern matcher</p>
            <p>Trained on billions of text examples</p>
            <p>Predicts "what word comes next"</p>
            <p>Like autocomplete on steroids</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="big-quote" style="font-size: 1.3rem;">
        ChatGPT doesn't "know" anything.<br>
        It predicts <em>the most likely next word</em> based on patterns in its training data.
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: HOW LLMS WORK
# ================================================================
elif current == "How LLMs Work":
    n = slide_start("How LLMs Actually Work", "The 60-second version", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>The WhatsApp Analogy</h4>
        <p>You know how your phone keyboard suggests the next word?</p>
        <p style="font-size: 1.3rem; color: #EF3837; text-align: center; padding: 12px 0;">
            "I am going to the" → <strong>store</strong> / <strong>gym</strong> / <strong>mall</strong>
        </p>
        <p>An LLM does the exact same thing... but it's read the ENTIRE internet, so its predictions are insanely good.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### The 3 Key Ingredients")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Training Data</h4>
            <p>Books, websites, Wikipedia, code, forums — trillions of words</p>
            <p style="color:#cccccc; font-size:0.9rem;">This is why it "knows" so much</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>The Model</h4>
            <p>Billions of "parameters" (numbers) that capture patterns in language</p>
            <p style="color:#cccccc; font-size:0.9rem;">This is the "brain"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Your Prompt</h4>
            <p>Your input that steers the output. Better prompt = better response</p>
            <p style="color:#cccccc; font-size:0.9rem;">This is YOUR superpower</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="big-quote" style="font-size: 1.2rem;">
        <strong>Key insight:</strong> The AI was trained in the past. It doesn't know <em>your</em> notes, <em>your</em> college, or <em>today's</em> news.<br>
        That's the problem we'll solve with <em>RAG</em> later today.
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: SETUP
# ================================================================
elif current == "Setup":
    n = slide_start("API Key Setup", "Let's connect to an AI model", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>What's an API Key?</h4>
        <p>Think of it like a <strong>password to use an AI model</strong>. Just like you need a login for Instagram, 
        you need an API key to use AI models in your own code/tools.</p>
        <p><strong>Groq</strong> = A company that lets you use powerful AI models for FREE (with limits).</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Follow these steps:")
    st.markdown("""
    1. Go to [console.groq.com](https://console.groq.com)
    2. Sign up with your Google account
    3. Click **"API Keys"** in the left sidebar
    4. Click **"Create API Key"**
    5. Copy it and paste below
    """)
    
    key = st.text_input("Paste your Groq API Key here:", value=st.session_state.groq_key, type="password")
    if key:
        st.session_state.groq_key = key
        os.environ['GROQ_API_KEY'] = key
    
    if st.button("Test My Connection", use_container_width=True):
        if not key:
            st.error("Please paste an API key first!")
        else:
            try:
                from groq import Groq
                client = Groq(api_key=key)
                resp = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[{"role": "user", "content": "Say 'Hello, future CEO!' in exactly those words."}],
                    max_tokens=20
                )
                st.success(f"Connected! AI says: {resp.choices[0].message.content}")
                st.balloons()
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.info("Double-check your API key and try again!")
    slide_end(n)

# ================================================================
#  SLIDE: DEMO 1 - ROAST MY INSTA BIO
# ================================================================
elif current == "Demo 1: Roast My Insta Bio":
    n = slide_start("Demo 1: Roast My Insta Bio", "Let AI judge your online personality", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>What's happening here?</h4>
        <p>We're giving the AI a <strong>personality</strong> (system prompt) and a <strong>task</strong> (roast your bio).</p>
        <p>This is your first taste of <strong>prompt engineering</strong> — controlling HOW the AI behaves.</p>
    </div>
    """, unsafe_allow_html=True)
    
    default_bio = """Instagram Bio:
Name: Rahul Kumar
SRM AP | CSE '27
Coder | Dreamer | Hustler
"Work hard in silence, let success make the noise"
DM for collabs
Founder @ nothing yet
Future Software Engineer at Google (manifesting)"""
    
    bio = st.text_area("Paste your Insta Bio (or use the example):", value=default_bio, height=180)
    mode = st.selectbox("Roast Style:", ["Savage (Funny)", "Brutally Honest (Helpful)", "Gen-Z Slang", "Indian Aunty"])
    
    if st.button("ROAST IT", use_container_width=True):
        if not st.session_state.groq_key:
            st.error("Go back to Setup and enter your API key first!")
        else:
            styles = {
                "Savage (Funny)": "You are a savage social media roast comedian. Roast Instagram bios like a stand-up special. Be brutally funny but reference specific things from the bio. Keep it fun, not mean-spirited.",
                "Brutally Honest (Helpful)": "You are a personal branding expert who reviews social media bios. Give honest, direct feedback on what works, what's cringe, and how to actually stand out.",
                "Gen-Z Slang": "You are a gen-z social media guru who speaks in memes, slang, and internet culture. Use 'bruh', 'no cap', 'lowkey', 'giving', 'slay', etc. Still give real advice though.",
                "Indian Aunty": "You are a nosy Indian aunty who saw your Instagram bio. React the way an aunty would — comparing to Sharma ji ka beta, asking about studies, questioning life choices. Be dramatic and hilarious but sneak in real advice."
            }
            from groq import Groq
            client = Groq(api_key=st.session_state.groq_key)
            with st.spinner("AI is analyzing your bio..."):
                response = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": f"""{styles[mode]}
Structure your response as:
THE ROAST (savage but specific — quote actual lines from the bio)
CRINGE-O-METER (rate the cringe level 1-10 with explanation)
THE GLOW-UP (rewrite the bio so it actually slaps)"""},
                        {"role": "user", "content": f"Roast this Instagram bio:\n{bio}"}
                    ],
                    temperature=0.9, max_tokens=700
                )
            st.markdown(f'<div class="demo-output">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    with st.expander("How does this work? (Click to see)"):
        st.markdown("""
        **Just 2 messages make this work:**
        
        1. **System message** = The AI's personality & instructions  
           "You are a savage social media roast comedian..."
        
        2. **User message** = What you're asking  
           "Roast this Instagram bio: ..."
        
        **That's it.** The AI follows the system prompt's personality and applies it to your input.
        
        **The magic variable:** `temperature` (0-1)  
        - 0 = Robotic, predictable  
        - 0.5 = Balanced  
        - 0.9 = Creative, funny (what we're using)
        
        **Try changing the roast style** — same bio, completely different output. That's the power of system prompts!
        """)
    slide_end(n)

# ================================================================
#  SLIDE: PROMPT ENGINEERING 101
# ================================================================
elif current == "Prompt Engineering 101":
    n = slide_start("Prompt Engineering 101", "The single most valuable AI skill", sn, TOTAL)
    
    st.markdown("""
    <div class="big-quote" style="font-size: 1.3rem;">
        A bad prompt is like telling a taxi driver "take me somewhere nice."<br>
        A good prompt is like giving them <em>the exact address + preferred route</em>.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### The 5 Rules of Great Prompts")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="concept-card">
            <h4>1. Give it a Role</h4>
            <p><strong>Bad:</strong> "Explain Python"</p>
            <p><strong>Good:</strong> "You are a patient CS professor teaching a beginner. Explain Python."</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-card">
            <h4>2. Be Specific</h4>
            <p><strong>Bad:</strong> "Write code"</p>
            <p><strong>Good:</strong> "Write a Python function that takes a list of numbers and returns the top 3 largest. Include comments."</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-card">
            <h4>3. Give Structure</h4>
            <p><strong>Bad:</strong> "Tell me about arrays"</p>
            <p><strong>Good:</strong> "Explain arrays in this format: Definition (2 lines), Real-world analogy, When to use, When NOT to use."</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-card">
            <h4>4. Give Examples</h4>
            <p><strong>Bad:</strong> "Summarize this"</p>
            <p><strong>Good:</strong> "Summarize this in the style of: 'React is like LEGO blocks for websites — snap pieces together to build anything.'"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-card">
            <h4>5. Iterate</h4>
            <p><strong>First attempt:</strong> "Explain ML"</p>
            <p><strong>After reading output:</strong> "That was too technical. Explain ML using only food analogies. No jargon."</p>
            <p style="color: #EF3837;">The best prompt is rarely your first one!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-card">
            <h4>Bonus: Chain of Thought</h4>
            <p>Add <strong>"Think step by step"</strong> to any prompt and watch the quality jump.</p>
            <p style="color: #cccccc;">This forces the AI to reason through problems instead of jumping to answers.</p>
        </div>
        """, unsafe_allow_html=True)
    
    slide_end(n)

# ================================================================
#  SLIDE: ACTIVITY 1 - PROMPT BATTLE
# ================================================================
elif current == "Activity 1: Prompt Battle":
    n = slide_start("Activity 1: Prompt Battle", "15 minutes — Best prompt wins", sn, TOTAL)
    
    st.markdown("""
    <div class="activity-card">
        <h4>CHALLENGE: Write the best system prompt</h4>
        <ol>
            <li>Pick a persona: <strong>Strict Indian Parent</strong>, <strong>Silicon Valley Bro</strong>, <strong>Bollywood Narrator</strong>, or <strong>your own idea</strong></li>
            <li>Write a system prompt that makes the AI review a resume in that style</li>
            <li>Test it below — iterate until it's amazing</li>
            <li>Best result gets shared with the group</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Example starters:")
    st.markdown("""
    - *"You are a strict Indian parent who just found out their child's career choices..."*
    - *"You are a dramatic Bollywood narrator reviewing a resume like it's a movie script..."*
    - *"You are Virat Kohli giving a dressing room pep talk about this resume..."*
    """)
    
    custom_prompt = st.text_area("Your system prompt:", height=120,
        placeholder="You are a strict Indian parent who...")
    custom_input = st.text_area("Resume or text to test:", height=120, key="a1r",
        value="Skills: HTML, CSS. Projects: Calculator app. Experience: None. GPA: 6.8")
    
    if st.button("Test My Prompt", use_container_width=True):
        if not st.session_state.groq_key:
            st.error("Set your API key in Setup first!")
        elif not custom_prompt:
            st.error("Write a system prompt first!")
        else:
            from groq import Groq
            client = Groq(api_key=st.session_state.groq_key)
            with st.spinner("Running your prompt..."):
                resp = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": custom_prompt},
                        {"role": "user", "content": f"Review this:\n{custom_input}"}
                    ],
                    temperature=0.85, max_tokens=500
                )
            st.markdown(f'<div class="demo-output">{resp.choices[0].message.content}</div>', unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: FEEDBACK 1
# ================================================================
elif current == "Feedback 1":
    render_feedback_slide(1, None, sn, TOTAL)

# ================================================================
#  SLIDE: QUIZ 1 - AI FUNDAMENTALS
# ================================================================
elif current == "Quiz 1: AI Fundamentals":
    n = slide_start("Quiz 1: AI Fundamentals", "Let's see what stuck", sn, TOTAL)
    
    q1 = st.radio("**1. What does an LLM actually do?**", [
        "A) Thinks like a human brain",
        "B) Predicts the most likely next word based on patterns",
        "C) Searches Google for answers",
        "D) Copies text from Wikipedia"
    ], key="q1_1")
    
    q2 = st.radio("**2. What is a 'system prompt'?**", [
        "A) The AI's operating system",
        "B) A message that sets the AI's personality and behavior",
        "C) The first thing the user types",
        "D) A way to hack the AI"
    ], key="q1_2")
    
    q3 = st.radio("**3. What does 'temperature' control?**", [
        "A) How fast the AI responds",
        "B) How creative vs predictable the output is",
        "C) The length of the response",
        "D) How accurate the response is"
    ], key="q1_3")
    
    q4 = st.radio("**4. Why can't ChatGPT tell you what happened yesterday?**", [
        "A) It's too lazy",
        "B) It was trained on past data and doesn't have live internet access",
        "C) You need to pay for that feature",
        "D) It can, you just need to ask nicely"
    ], key="q1_4")
    
    if st.button("Check Answers", key="c1"):
        score = sum([
            1 if st.session_state.get("q1_1","").startswith("B") else 0,
            1 if st.session_state.get("q1_2","").startswith("B") else 0,
            1 if st.session_state.get("q1_3","").startswith("B") else 0,
            1 if st.session_state.get("q1_4","").startswith("B") else 0,
        ])
        if score == 4:
            st.balloons()
            st.success(f"Score: {score}/4 — Perfect! You get how AI works!")
        elif score >= 3:
            st.info(f"Score: {score}/4 — Almost there!")
        else:
            st.warning(f"Score: {score}/4 — Review the 'What is AI' and 'How LLMs Work' slides.")
        with st.expander("Correct answers"):
            st.markdown("""
            1. **B)** Predicts the most likely next word based on patterns
            2. **B)** A message that sets the AI's personality and behavior  
            3. **B)** How creative vs predictable the output is (0=robotic, 1=creative)
            4. **B)** It was trained on past data — it doesn't browse the internet in real-time
            """)
    slide_end(n)

# ================================================================
#  SLIDE: WHAT IS RAG?
# ================================================================
elif current == "What is RAG?":
    n = slide_start("What is RAG?", "Retrieval Augmented Generation — the superpower", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>The Open-Book Exam Analogy</h4>
        <p><strong>Without RAG</strong> = Closed-book exam. The AI can only use what it memorized during training. 
        If it didn't read your college notes... it can't answer questions about them. It might even make stuff up!</p>
        <p><strong>With RAG</strong> = Open-book exam. Before answering, the AI <strong>looks up relevant pages</strong> from YOUR documents, 
        then answers based on what it found. Much more accurate!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### How RAG Works (3 Simple Steps)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Step 1: Store</h4>
            <p>Convert your documents into numbers (embeddings) and store them in a special database</p>
            <p style="color:#cccccc; font-size:0.9rem;">Like creating an index for a textbook</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Step 2: Search</h4>
            <p>When you ask a question, find the most <strong>relevant</strong> documents by meaning (not just keywords!)</p>
            <p style="color:#cccccc; font-size:0.9rem;">Like flipping to the right chapter</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Step 3: Answer</h4>
            <p>Give the AI the relevant docs + your question. It answers using ONLY your data!</p>
            <p style="color:#cccccc; font-size:0.9rem;">Like reading the chapter, then answering</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="big-quote" style="font-size: 1.2rem;">
        <strong>Why this matters:</strong><br>
        Without RAG: "What time does the SRM AP library close?" — AI guesses (probably wrong)<br>
        With RAG: <em>AI checks your college FAQ document</em> — "The library closes at 10 PM on weekdays"
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="concept-card">
        <h4>What are Embeddings?</h4>
        <p><strong>Simple version:</strong> Embeddings are a way to convert text into numbers that capture <strong>meaning</strong>.</p>
        <p>"I love coding" and "Programming is my passion" would have <strong>similar numbers</strong> because they mean similar things.</p>
        <p>"I love coding" and "My cat is sleeping" would have <strong>very different numbers</strong>.</p>
        <p style="color:#cccccc;">This is how the database can search by meaning instead of exact keyword matches!</p>
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: DEMO 2 - RAG PIPELINE
# ================================================================
elif current == "Demo 2: RAG Pipeline":
    n = slide_start("Demo 2: RAG in Action", "Chat with your own notes", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>What we're doing</h4>
        <p>1. Load some study notes into a smart database</p>
        <p>2. Ask it questions — it finds the right notes and answers from them</p>
        <p>3. Ask something NOT in the notes — watch it say "I don't know" (that's good!)</p>
    </div>
    """, unsafe_allow_html=True)
    
    default_notes = """SRM AP campus is located in Amaravati, Andhra Pradesh.
The library is open from 8 AM to 10 PM on weekdays.
The cafeteria serves breakfast from 7:30 AM to 9:30 AM.
Wi-Fi password for students can be obtained from the IT helpdesk in Block A.
The coding club meets every Wednesday at 5 PM in Room 301.
Semester exams usually start in the last week of November.
The placement cell is located on the 2nd floor of the admin building.
Students need a minimum of 75% attendance to sit for exams.
The sports complex has a gym, basketball court, and swimming pool.
The campus bus service runs every 30 minutes from the main gate."""
    
    notes = st.text_area("Knowledge Base (your notes — one fact per line):", value=default_notes, height=200)
    
    if st.button("Load Notes into Smart Database", use_container_width=True):
        try:
            import chromadb
            docs = [n.strip() for n in notes.strip().split("\n") if n.strip()]
            if 'chroma_client' not in st.session_state:
                st.session_state.chroma_client = chromadb.Client()
            client = st.session_state.chroma_client
            try: client.delete_collection("demo_rag")
            except: pass
            collection = client.create_collection("demo_rag")
            collection.add(documents=docs, ids=[f"d_{i}" for i in range(len(docs))])
            st.session_state.rag_collection = collection
            st.session_state.rag_ready = True
            st.success(f"Loaded {len(docs)} notes. Now ask a question below.")
        except Exception as e:
            st.error(f"Error: {e}. Try refreshing the page.")
    
    if st.session_state.get('rag_ready'):
        st.markdown("---")
        
        col_good, col_trick = st.columns(2)
        
        with col_good:
            st.markdown("### Ask something IN the notes")
            query = st.text_input("Your question:", value="What time does the library close?", key="rag_q1")
            if st.button("Ask (RAG)", use_container_width=True, key="rag_btn1"):
                if not st.session_state.groq_key:
                    st.error("Set API key in Setup first!")
                else:
                    collection = st.session_state.rag_collection
                    with st.status("RAG Pipeline running...", expanded=True) as status:
                        st.write("Step 1: Searching notes for relevant info...")
                        results = collection.query(query_texts=[query], n_results=2)
                        for i, doc in enumerate(results['documents'][0]):
                            st.write(f"Found: *{doc[:80]}...*")
                        context = "\n---\n".join(results['documents'][0])
                        st.write("Step 2: Sending to AI with the relevant notes...")
                        from groq import Groq
                        client = Groq(api_key=st.session_state.groq_key)
                        resp = client.chat.completions.create(
                            model="qwen/qwen3.8-27b",
                            messages=[
                                {"role": "system", "content": "Answer ONLY from the notes provided. If the answer is not in the notes, say 'That's not in your notes!' Be helpful and concise."},
                                {"role": "user", "content": f"NOTES:\n{context}\n\nQUESTION: {query}"}
                            ],
                            max_tokens=300, temperature=0.3
                        )
                        status.update(label="Done!", state="complete")
                    st.markdown(f'<div class="demo-output">{resp.choices[0].message.content}</div>', unsafe_allow_html=True)
        
        with col_trick:
            st.markdown("### Ask something NOT in the notes")
            trick_q = st.text_input("Try to trick it:", value="What's the Instagram password for the college page?", key="rag_q2")
            if st.button("Ask (should say 'I don't know')", use_container_width=True, key="rag_btn2"):
                if not st.session_state.groq_key:
                    st.error("Set API key in Setup first!")
                else:
                    collection = st.session_state.rag_collection
                    results = collection.query(query_texts=[trick_q], n_results=2)
                    context = "\n---\n".join(results['documents'][0])
                    from groq import Groq
                    client = Groq(api_key=st.session_state.groq_key)
                    resp = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {"role": "system", "content": "Answer ONLY from the notes provided. If the answer is not in the notes, say 'That's not in your notes! Here's what I DO know about...' and mention the closest topic."},
                            {"role": "user", "content": f"NOTES:\n{context}\n\nQUESTION: {trick_q}"}
                        ],
                        max_tokens=200, temperature=0.3
                    )
                    st.info(resp.choices[0].message.content)
    
    with st.expander("What just happened? (Simple explanation)"):
        st.markdown("""
        1. **We loaded your notes** into a vector database (ChromaDB). Each note was converted into numbers (embeddings).
        2. **When you asked a question**, the database found the notes most similar *in meaning* to your question.
        3. **The AI read those notes** and answered based on them — not from its general knowledge!
        4. **When the answer wasn't in the notes**, the AI honestly said so instead of making stuff up.
        
        **This is RAG!** The AI is "augmented" with your specific data. This is how companies build chatbots for their own documents.
        """)
    slide_end(n)

# ================================================================
#  SLIDE: FEEDBACK 2
# ================================================================
elif current == "Feedback 2":
    render_feedback_slide(2, None, sn, TOTAL)

# ================================================================
#  SLIDE: QUIZ 2 - RAG BASICS
# ================================================================
elif current == "Quiz 2: RAG Basics":
    n = slide_start("Quiz 2: RAG Basics", None, sn, TOTAL)
    
    q1 = st.radio("**1. What does RAG stand for?**", [
        "A) Really Awesome Generator",
        "B) Retrieval Augmented Generation",
        "C) Random Answer Generator",
        "D) Rapid AI Growth"
    ], key="q2_1")
    
    q2 = st.radio("**2. In the open-book exam analogy, what is 'retrieval'?**", [
        "A) Writing the answer",
        "B) Studying the night before",
        "C) Looking up the relevant pages before answering",
        "D) Memorizing everything"
    ], key="q2_2")
    
    q3 = st.radio("**3. What are embeddings?**", [
        "A) Images inside documents",
        "B) Numbers that capture the meaning of text",
        "C) Links to websites",
        "D) AI model names"
    ], key="q2_3")
    
    q4 = st.radio("**4. What should a good RAG system do when asked something NOT in its documents?**", [
        "A) Make up an answer anyway",
        "B) Crash and show an error",
        "C) Honestly say it doesn't have that information",
        "D) Search Google instead"
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
            st.success(f"Score: {score}/4 — RAG master!")
        elif score >= 3:
            st.info(f"Score: {score}/4 — Solid understanding!")
        else:
            st.warning(f"Score: {score}/4 — Review the RAG slides and demo.")
        with st.expander("Correct answers"):
            st.markdown("""
            1. **B)** Retrieval Augmented Generation
            2. **C)** Looking up the relevant pages before answering (retrieval = finding the right context)
            3. **B)** Numbers that capture the meaning of text
            4. **C)** Honestly say it doesn't have that information (no hallucination!)
            """)
    slide_end(n)

# ================================================================
#  SLIDE: WHAT ARE AI AGENTS?
# ================================================================
elif current == "What are AI Agents?":
    n = slide_start("What are AI Agents?", "From chatbot to autonomous worker", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>The Intern vs Employee Analogy</h4>
        <p><strong>ChatGPT (Chatbot)</strong> = An intern. You ask a question, they answer. You ask another, they answer. 
        They only do exactly what you say, one thing at a time.</p>
        <p><strong>AI Agent</strong> = A smart employee. You say "Research this topic and email me a summary." 
        They <strong>decide</strong> to search Google, read 5 articles, summarize them, and send the email — all on their own!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### What Makes an Agent Different?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="concept-card">
            <h4>Regular Chatbot</h4>
            <p>You ask, it answers</p>
            <p>Can't use tools</p>
            <p>Can't search the internet</p>
            <p>Can't take actions</p>
            <p>One-shot response</p>
            <p style="color: #EF3837;">Like texting a friend</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-card">
            <h4>AI Agent</h4>
            <p>You give a goal, it figures out the steps</p>
            <p>Can use tools (search, calculator, APIs)</p>
            <p>Can browse the internet</p>
            <p>Can take actions (send email, write files)</p>
            <p>Multi-step reasoning</p>
            <p style="color: #22c55e;">Like hiring an assistant</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### The 4 Parts of an AI Agent")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Brain</h4>
            <p>The LLM that thinks and decides</p>
            <p style="color:#cccccc; font-size:0.85rem;">(GPT, Gemini, Llama, etc.)</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Memory</h4>
            <p>RAG — your documents and context</p>
            <p style="color:#cccccc; font-size:0.85rem;">(What we just learned!)</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Tools</h4>
            <p>Search, calculator, APIs, databases</p>
            <p style="color:#cccccc; font-size:0.85rem;">(The agent's hands)</p>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Orchestrator</h4>
            <p>The logic: what to do when</p>
            <p style="color:#cccccc; font-size:0.85rem;">(The agent's brain plan)</p>
        </div>
        """, unsafe_allow_html=True)
    
    slide_end(n)

# ================================================================
#  SLIDE: DEMO 3 - NO-CODE AGENT (N8N)
# ================================================================
elif current == "Demo 3: No-Code Agent (n8n)":
    n = slide_start("Demo 3: Build an Agent — No Code", "Using n8n — drag-and-drop AI agent builder", sn, TOTAL)
    
    st.markdown("""
    <div class="analogy-box">
        <h4>What is n8n?</h4>
        <p><strong>n8n</strong> (pronounced "n-eight-n") is a free visual workflow tool where you build AI agents by <strong>connecting blocks</strong> — no coding needed!</p>
        <p>Think of it like <strong>LEGO for AI</strong>. Each block does one thing (chat, search, read a document). You snap them together to build an agent.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.link_button("Open n8n Cloud", "https://app.n8n.cloud/register", use_container_width=True)
    with col2: st.link_button("n8n AI Docs", "https://docs.n8n.io/advanced-ai/", use_container_width=True)
    with col3: st.link_button("Get Groq Key", "https://console.groq.com", use_container_width=True)
    
    st.markdown("### Follow Along — Step by Step")
    
    steps = [
        ("Sign up on n8n Cloud", "Free tier available — use your Google account!"),
        ("Create a new workflow, click '+' to add nodes", "A workflow is like a flowchart for your agent"),
        ("Add a 'Chat Trigger' node", "This is the starting point — where user messages come in"),
        ("Add an 'AI Agent' node, connect it to the trigger", "This is the brain — it decides what to do!"),
        ("Configure the AI model: Add Groq credential, select a model", "Paste your Groq API key when asked"),
        ("Add a 'System Message' in the agent, paste the prompt below", "This is the agent's personality and rules"),
        ("Add Tools: Click '+' under Tools, add 'Wikipedia' and 'HTTP Request'", "These let your agent search for info!"),
        ("Test it! Click 'Chat' in the bottom panel", "Ask: 'What are the top programming languages in 2026?'"),
        ("Watch the execution path light up", "You can see which tools the agent chose to use"),
        ("Click 'Share' to get a webhook URL or embed it", "Your agent is now accessible"),
    ]
    
    for i, (step, hint) in enumerate(steps, 1):
        st.checkbox(f"**Step {i}:** {step}", key=f"n8n_{i}", help=hint)
    
    st.markdown("### System Prompt to Copy:")
    code_editor(
        code="""You are Campus Buddy AI, a friendly and helpful assistant for 
college students at SRM AP.

Your personality: Friendly, encouraging, uses simple language.
When you don't know something, say so honestly.

When asked about current events, job market, or trends:
-> Use your tools to SEARCH first, then answer with real data.

When asked about general knowledge or topics:
-> Use Wikipedia to get accurate information.

Always end with a helpful tip or next step the student can take.""",
        filename="system_prompt.txt",
        language=None,
        replicate_steps=[
            "Copy this entire prompt",
            "Paste it into the 'System Message' field in n8n's AI Agent node",
            "Feel free to customize the personality!",
            "The key line is 'Use your tools to SEARCH first' — this tells the agent WHEN to use tools",
        ]
    )
    
    st.markdown("""
    <div class="analogy-box">
        <h4>Why n8n is great for beginners</h4>
        <p>You can <strong>see</strong> the agent thinking — the workflow lights up as each step runs</p>
        <p>Drag and drop — no syntax errors, no debugging code</p>
        <p>400+ integrations — connect to Google Sheets, Slack, Email, Notion, and more</p>
        <p>The same tool professionals use in production. This isn't a toy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="big-quote" style="font-size: 1.2rem;">
        You just built an AI agent with:<br>
        Brain (LLM) + Tools (Wikipedia, Search) + Logic (System Prompt)<br><br>
        <em>Zero lines of code. Just drag, drop, and connect.</em>
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: ACTIVITY 2 - BUILD YOUR AGENT
# ================================================================
elif current == "Activity 2: Build Your Agent":
    n = slide_start("Activity 2: Build YOUR Agent", "30 minutes — Teams of 2-3", sn, TOTAL)
    
    st.markdown("""
    <div class="activity-card">
        <h4>CHALLENGE: Build a useful AI agent on n8n</h4>
        <ol>
            <li>Form teams of 2-3 people</li>
            <li>Pick a problem from the ideas below (or come up with your own!)</li>
            <li>Build it on n8n — add an AI Agent node, connect tools, write a great system prompt</li>
            <li>Test it with at least 5 different questions</li>
            <li>Watch the workflow execute — see which tools the agent uses</li>
            <li>Each team: 2-minute demo to the group</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Project Ideas (Pick one)")
    
    ideas = {
        "PlacePrep Coach": "Helps students prepare for placements. Upload interview questions as knowledge base. Uses web search for latest company patterns.",
        "Study Buddy": "Upload your course notes as knowledge base. Ask it questions about your syllabus. Great for exam prep!",
        "Campus Navigator": "Knowledge base with campus info (locations, timings, contacts). Answers any campus question.",
        "Career Advisor": "Uses web search to find current job trends, salary data, and skill requirements. Gives personalized advice.",
        "Food Recommender": "Knowledge base with local restaurant info. Recommends based on budget, cuisine, and mood.",
        "Entertainment Buddy": "Uses web search to find latest movies, shows, and events. Gives personalized recommendations.",
    }
    
    col1, col2 = st.columns(2)
    for i, (name, desc) in enumerate(ideas.items()):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="concept-card">
                <h4>{name}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### Judging Criteria")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Usefulness (40%)</h4>
            <p>Does it solve a real problem a student would have?</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Creativity (30%)</h4>
            <p>Is the system prompt clever? Good personality?</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="concept-card" style="text-align:center;">
            <h4>Demo Quality (30%)</h4>
            <p>Does it work live? Clear presentation?</p>
        </div>
        """, unsafe_allow_html=True)
    
    slide_end(n)

# ================================================================
#  SLIDE: FEEDBACK 3
# ================================================================
elif current == "Feedback 3":
    render_feedback_slide(3, None, sn, TOTAL)

# ================================================================
#  SLIDE: FINAL QUIZ
# ================================================================
elif current == "Final Quiz":
    n = slide_start("Final Quiz: What Did You Learn?", None, sn, TOTAL)
    
    q1 = st.radio("**1. You want AI to answer questions about YOUR college notes. You need:**", [
        "A) A bigger AI model",
        "B) RAG — store notes in a database, retrieve relevant ones, then answer",
        "C) Copy-paste all notes into ChatGPT every time",
        "D) Fine-tune GPT-4 on your notes"
    ], key="qf_1")
    
    q2 = st.radio("**2. What makes an AI agent different from a chatbot?**", [
        "A) Agents are more expensive",
        "B) Agents can use tools and make decisions autonomously",
        "C) Agents are always more accurate",
        "D) There's no real difference"
    ], key="qf_2")
    
    q3 = st.radio("**3. The BEST way to improve an AI's output is to:**", [
        "A) Use a more expensive model",
        "B) Write a better prompt with clear role, structure, and examples",
        "C) Ask the same question 10 times",
        "D) Use all caps"
    ], key="qf_3")
    
    q4 = st.radio("**4. What does the 'system prompt' control?**", [
        "A) The AI model's speed",
        "B) The AI's personality, behavior, and rules",
        "C) How much the API costs",
        "D) The language of the response"
    ], key="qf_4")
    
    q5 = st.radio("**5. In the 5 Levels framework, which skill matters MOST in the AI era?**", [
        "A) Memorizing code syntax",
        "B) Typing faster",
        "C) Knowing how to orchestrate AI — connecting tools, data, and models",
        "D) Using ChatGPT for homework"
    ], key="qf_5")
    
    if st.button("Check My Score", key="cf"):
        score = sum([
            1 if st.session_state.get("qf_1","").startswith("B") else 0,
            1 if st.session_state.get("qf_2","").startswith("B") else 0,
            1 if st.session_state.get("qf_3","").startswith("B") else 0,
            1 if st.session_state.get("qf_4","").startswith("B") else 0,
            1 if st.session_state.get("qf_5","").startswith("C") else 0,
        ])
        if score == 5:
            st.balloons()
            st.success(f"5/5 — You're ready to be a CEO of Superintelligence! Amazing!")
        elif score >= 4:
            st.success(f"{score}/5 — Excellent! You've got the fundamentals down!")
        elif score >= 3:
            st.info(f"{score}/5 — Good start! Review the slides you missed.")
        else:
            st.warning(f"{score}/5 — No worries! Check the 'What to Learn Next' slide for resources.")
        with st.expander("Correct answers"):
            st.markdown("""
            1. **B)** RAG — store, retrieve, then answer
            2. **B)** Agents can use tools and make decisions autonomously
            3. **B)** Write a better prompt with clear role, structure, and examples
            4. **B)** The AI's personality, behavior, and rules
            5. **C)** Knowing how to orchestrate AI — the CEO mindset!
            """)
    slide_end(n)

# ================================================================
#  SLIDE: WHAT TO LEARN NEXT
# ================================================================
elif current == "What to Learn Next":
    n = slide_start("What to Learn Next", "Your roadmap after today", sn, TOTAL)
    
    st.markdown("### Your Learning Path")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="concept-card">
            <h4>This Week</h4>
            <p>Practice prompt engineering daily — try different system prompts on ChatGPT/Gemini</p>
            <p>Build 2 more agents on n8n with different use cases</p>
            <p>Share your agent link with friends and get feedback</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-card">
            <h4>This Month</h4>
            <p>Learn Python basics if you haven't (freeCodeCamp, W3Schools)</p>
            <p>Try the Groq API in Python — just 10 lines of code!</p>
            <p>Take the free DeepLearning.AI "ChatGPT Prompt Engineering" course</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-card">
            <h4>Next 3 Months</h4>
            <p>Learn LangChain or CrewAI for building agents with code</p>
            <p>Build a RAG system with your own documents</p>
            <p>Deploy something on Hugging Face Spaces (free hosting)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="concept-card">
            <h4>By Next Year</h4>
            <p>Build a portfolio of 3-5 AI projects</p>
            <p>Contribute to open-source AI projects</p>
            <p>Apply for AI/ML internships with your projects as proof</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="big-quote" style="font-size: 1.3rem;">
        The people who will thrive in the AI era aren't the ones who <em>fear</em> AI.<br>
        They're the ones who <em>learn to orchestrate it</em>.<br><br>
        You started that journey today. <em>Don't stop.</em>
    </div>
    """, unsafe_allow_html=True)
    slide_end(n)

# ================================================================
#  SLIDE: QUICK LINKS
# ================================================================
elif current == "Quick Links":
    n = slide_start("Quick Links", "Everything you need in one place", sn, TOTAL)
    
    st.markdown("### Tools We Used Today")
    c1, c2, c3 = st.columns(3)
    with c1: st.link_button("n8n Cloud (Agent Builder)", "https://app.n8n.cloud", use_container_width=True)
    with c2: st.link_button("Groq Console (API Key)", "https://console.groq.com", use_container_width=True)
    with c3: st.link_button("Google Colab", "https://colab.research.google.com", use_container_width=True)
    
    st.markdown("### Free Learning Resources")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.link_button("DeepLearning.AI (Free)", "https://deeplearning.ai/courses", use_container_width=True)
    with c2: st.link_button("Prompt Engineering Guide", "https://www.promptingguide.ai/", use_container_width=True)
    with c3: st.link_button("HuggingFace (Free hosting)", "https://huggingface.co/spaces", use_container_width=True)
    with c4: st.link_button("LangChain (Agents)", "https://python.langchain.com", use_container_width=True)
    
    st.markdown("### Workshop Materials")
    st.text_input("Feedback Form:", key="fbl", placeholder="https://forms.google.com/...")
    st.text_input("Slide Deck / Resources:", key="rl", placeholder="https://...")
    st.text_input("WhatsApp / Discord Group:", key="wl", placeholder="https://chat.whatsapp.com/...")
    
    slide_end(n)

# ================================================================
#  SLIDE: TIMER
# ================================================================
elif current == "Timer":
    n = slide_start("Activity Timer", None, sn, TOTAL)
    c1, c2 = st.columns(2)
    with c1: mins = st.number_input("Minutes:", min_value=1, max_value=60, value=15)
    with c2: label = st.text_input("Activity:", value="Build Your Agent")
    
    if st.button("START TIMER", use_container_width=True):
        placeholder = st.empty()
        total_seconds = mins * 60
        for remaining in range(total_seconds, -1, -1):
            m, s = divmod(remaining, 60)
            color = "#22c55e" if remaining > 60 else "#f59e0b" if remaining > 15 else "#EF3837"
            msg = "TIME'S UP!" if remaining == 0 else "Go!" if remaining > 60 else "Wrapping up..." if remaining > 15 else "Almost done!"
            placeholder.markdown(f"""
            <div style="text-align:center; padding:60px 0;">
                <p style="font-size:1.5rem; color:#cccccc;">{label}</p>
                <p style="font-size:10rem; font-weight:900; color:{color}; margin:0; font-family:'JetBrains Mono',monospace;">{m:02d}:{s:02d}</p>
                <p style="font-size:1.3rem; color:#cccccc;">{msg}</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        st.balloons()
        st.success(f"Time's up! {label} complete!")
    slide_end(n)

# ================================================================
#  BOTTOM NAV
# ================================================================
st.markdown("---")
bl, bc, br = st.columns([1, 3, 1])
with bl:
    if st.button("< Previous ", use_container_width=True, disabled=(st.session_state.slide == 0), key="bp"):
        st.session_state.slide -= 1
        st.rerun()
with bc:
    st.markdown(f"<p style='text-align:center; color:#555; font-family:JetBrains Mono,monospace; padding-top:8px;'>{sn} / {TOTAL} — {current}</p>", unsafe_allow_html=True)
with br:
    if st.button("Next > ", use_container_width=True, disabled=(st.session_state.slide == TOTAL - 1), key="bn"):
        st.session_state.slide += 1
        st.rerun()
