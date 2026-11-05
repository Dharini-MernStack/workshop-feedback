"""
Structured Workshop Feedback Form (Streamlit)
Students scan QR → this form opens → submits to shared PostgreSQL
"""

import streamlit as st
import os, json, datetime

st.set_page_config(page_title="Workshop Feedback", page_icon="🧠", layout="centered")

# ---- DATABASE SETUP ----
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL:
    import psycopg2
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    def init_db():
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback_2ndyear (
                id SERIAL PRIMARY KEY,
                email VARCHAR(300) NOT NULL,
                overall_rating INTEGER NOT NULL,
                content_relevance INTEGER NOT NULL,
                explanation_quality INTEGER NOT NULL,
                practical_rating INTEGER NOT NULL,
                met_expectations VARCHAR(20) NOT NULL,
                gained_skills VARCHAR(10) NOT NULL,
                most_useful TEXT DEFAULT '',
                github_link TEXT DEFAULT '',
                additional_comments TEXT DEFAULT '',
                submitted_at TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
        conn.close()

    init_db()
    USE_POSTGRES = True
else:
    USE_POSTGRES = False
    DATA_FILE = "feedback_2ndyear.json"
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"responses": []}, f)


def save_feedback(data):
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO feedback_2ndyear
               (email, overall_rating, content_relevance, explanation_quality,
                practical_rating, met_expectations, gained_skills,
                most_useful, github_link, additional_comments)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (data["email"], data["overall_rating"], data["content_relevance"],
             data["explanation_quality"], data["practical_rating"],
             data["met_expectations"], data["gained_skills"],
             data.get("most_useful", ""), data.get("github_link", ""),
             data.get("additional_comments", ""))
        )
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM feedback_2ndyear")
        count = cur.fetchone()[0]
        conn.close()
        return count
    else:
        with open(DATA_FILE, "r") as f:
            store = json.load(f)
        data["timestamp"] = datetime.datetime.now().isoformat()
        store["responses"].append(data)
        with open(DATA_FILE, "w") as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
        return len(store["responses"])


def get_count():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM feedback_2ndyear")
        count = cur.fetchone()[0]
        conn.close()
        return count
    else:
        with open(DATA_FILE, "r") as f:
            store = json.load(f)
        return len(store.get("responses", []))


# ---- STYLING ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    .stApp { background-color: #0a0a0a; }
    .block-container { max-width: 520px; padding-top: 2rem !important; }
    header[data-testid="stHeader"] { background: #0a0a0a; height: 0px !important; min-height: 0px !important; }
    h1 { font-family: 'Inter', sans-serif; text-align: center; }
    .stButton > button {
        background: linear-gradient(135deg, #EF3837, #cc2a29);
        color: white; border: none; border-radius: 12px;
        padding: 14px 32px; font-weight: 700; font-size: 1.1rem;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(239,56,55,0.5);
    }
    div[data-testid="stForm"] {
        background: #111; border: 1px solid #222; border-radius: 20px;
        padding: 28px 24px;
    }
    .stSelectbox label, .stTextArea label, .stTextInput label, .stRadio label {
        color: #ccc !important; font-weight: 600 !important;
    }
    .stSelectbox div[data-baseweb], .stTextArea textarea, .stTextInput input {
        background: #1a1a1a !important; border-color: #333 !important;
        color: #e5e7eb !important;
    }
    .success-box {
        text-align: center; padding: 40px 20px;
        background: #111; border: 1px solid #222; border-radius: 20px;
    }
    .success-box h2 { color: #22c55e; }
    .success-box p { color: #9ca3af; }
</style>
""", unsafe_allow_html=True)

# ---- FORM ----

if st.session_state.get("submitted"):
    st.markdown("""
    <div class="success-box">
        <p style="font-size:4rem;">✅</p>
        <h2>Thank you!</h2>
        <p>Your feedback has been recorded.<br>Great work today! 🎉</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style="text-align:center; font-size:2.2rem; margin-bottom:0;">🧠</p>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='background: linear-gradient(135deg, #EF3837, #ff6b6b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size:1.6rem; margin-bottom:2px;'>CEO of Superintelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#9ca3af; margin-bottom:20px;'>2nd Year Workshop Feedback</p>", unsafe_allow_html=True)

    with st.form("feedback_form"):
        rating_options = ["Select...", "1 - Poor", "2 - Fair", "3 - Good", "4 - Excellent"]

        overall = st.selectbox("How would you rate the overall day? *", rating_options)
        relevance = st.selectbox("How relevant was the workshop content to your learning needs? *", rating_options)
        explanation = st.selectbox("How effectively were the concepts explained? *", rating_options)
        practical = st.selectbox("How would you rate the practical sessions / hands-on activities? *", rating_options)

        st.markdown("---")

        expectations = st.radio("Did the workshop meet your expectations? *", ["Yes", "Partially", "No"], horizontal=True)
        skills = st.radio("Did you gain new knowledge or practical skills from this workshop? *", ["Yes", "No"], horizontal=True)

        st.markdown("---")

        most_useful = st.text_area("What was the most useful aspect of the workshop?", placeholder="e.g. The hands-on coding activity...")
        github_link = st.text_input("Submit your GitHub Repository Link / Google Colab", placeholder="https://github.com/... or https://colab.research.google.com/...")
        comments = st.text_area("Any additional comments or suggestions?", placeholder="Optional...")
        email = st.text_input("Email address *", placeholder="your.name@kalvium.community")

        submitted = st.form_submit_button("Submit Feedback 🚀")

        if submitted:
            # Validate
            errors = []
            if overall == "Select...": errors.append("Overall rating")
            if relevance == "Select...": errors.append("Content relevance")
            if explanation == "Select...": errors.append("Explanation quality")
            if practical == "Select...": errors.append("Practical sessions")
            if not email.strip(): errors.append("Email address")

            if errors:
                st.error(f"Please fill in: {', '.join(errors)}")
            else:
                data = {
                    "email": email.strip(),
                    "overall_rating": int(overall[0]),
                    "content_relevance": int(relevance[0]),
                    "explanation_quality": int(explanation[0]),
                    "practical_rating": int(practical[0]),
                    "met_expectations": expectations,
                    "gained_skills": skills,
                    "most_useful": most_useful.strip(),
                    "github_link": github_link.strip(),
                    "additional_comments": comments.strip(),
                }
                try:
                    count = save_feedback(data)
                    st.session_state.submitted = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving: {e}. Please try again.")
