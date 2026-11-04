"""
Live Feedback Server for Workshop
Run locally:  python feedback_server.py
Deploy:       Render (uses PostgreSQL if DATABASE_URL set, else local JSON fallback)
"""

from flask import Flask, request, jsonify, render_template_string, Response
import json, os, datetime, socket, csv, io

app = Flask(__name__)

# ---- DATABASE SETUP ----
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL:
    # Production: PostgreSQL on Render
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    # Render uses postgres:// but psycopg2 needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    def get_db():
        return psycopg2.connect(DATABASE_URL)
    
    def init_db():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                round_num INTEGER NOT NULL,
                name VARCHAR(200) NOT NULL,
                rating INTEGER NOT NULL,
                feedback TEXT DEFAULT '',
                submitted_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback_3rdyear (
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
    print("✅ Using PostgreSQL database")
else:
    # Local dev: JSON file
    USE_POSTGRES = False
    DATA_FILE = "feedback_data.json"
    DATA_FILE_3RD = "feedback_3rdyear.json"
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"round_1": [], "round_2": [], "round_3": []}, f)
    if not os.path.exists(DATA_FILE_3RD):
        with open(DATA_FILE_3RD, "w") as f:
            json.dump({"responses": []}, f)
    DATA_FILE_2ND = "feedback_2ndyear.json"
    if not os.path.exists(DATA_FILE_2ND):
        with open(DATA_FILE_2ND, "w") as f:
            json.dump({"responses": []}, f)
    print("📁 Using local JSON file (no DATABASE_URL set)")


# ---- DATA HELPERS ----

def save_feedback(round_num, name, rating, feedback_text):
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO feedback (round_num, name, rating, feedback) VALUES (%s, %s, %s, %s)",
            (round_num, name, rating, feedback_text)
        )
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM feedback WHERE round_num = %s", (round_num,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    else:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        key = f"round_{round_num}"
        data[key].append({
            "name": name, "rating": rating, "feedback": feedback_text,
            "timestamp": datetime.datetime.now().isoformat()
        })
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return len(data[key])


def get_all_stats():
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        result = {}
        for r in [1, 2, 3]:
            cur.execute(
                "SELECT name, rating, feedback, submitted_at FROM feedback WHERE round_num = %s ORDER BY id",
                (r,)
            )
            entries = cur.fetchall()
            # Convert datetime to string
            for e in entries:
                if e.get("submitted_at"):
                    e["submitted_at"] = e["submitted_at"].isoformat()
            ratings = [e["rating"] for e in entries]
            result[f"round_{r}"] = {
                "count": len(entries),
                "avg_rating": round(sum(ratings)/len(ratings), 1) if ratings else 0,
                "entries": entries
            }
        conn.close()
        return result
    else:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        result = {}
        for key in ["round_1", "round_2", "round_3"]:
            entries = data.get(key, [])
            ratings = [e["rating"] for e in entries]
            result[key] = {
                "count": len(entries),
                "avg_rating": round(sum(ratings)/len(ratings), 1) if ratings else 0,
                "entries": entries
            }
        return result


def reset_all():
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM feedback")
        conn.commit()
        conn.close()
    else:
        with open(DATA_FILE, "w") as f:
            json.dump({"round_1": [], "round_2": [], "round_3": []}, f)


# ---- 3RD YEAR FEEDBACK HELPERS ----

def save_3rdyear_feedback(data):
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO feedback_3rdyear
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
        cur.execute("SELECT COUNT(*) FROM feedback_3rdyear")
        count = cur.fetchone()[0]
        conn.close()
        return count
    else:
        with open(DATA_FILE_3RD, "r") as f:
            store = json.load(f)
        data["timestamp"] = datetime.datetime.now().isoformat()
        store["responses"].append(data)
        with open(DATA_FILE_3RD, "w") as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
        return len(store["responses"])


def get_3rdyear_stats():
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM feedback_3rdyear ORDER BY id")
        rows = cur.fetchall()
        for r in rows:
            if r.get("submitted_at"):
                r["submitted_at"] = r["submitted_at"].isoformat()
        conn.close()
    else:
        with open(DATA_FILE_3RD, "r") as f:
            store = json.load(f)
        rows = store.get("responses", [])

    count = len(rows)
    if count == 0:
        return {"count": 0, "avg_overall": 0, "avg_relevance": 0,
                "avg_explanation": 0, "avg_practical": 0,
                "met_expectations_pct": 0, "gained_skills_pct": 0, "github_count": 0}

    avg_o = round(sum(r["overall_rating"] for r in rows) / count, 2)
    avg_r = round(sum(r["content_relevance"] for r in rows) / count, 2)
    avg_e = round(sum(r["explanation_quality"] for r in rows) / count, 2)
    avg_p = round(sum(r["practical_rating"] for r in rows) / count, 2)
    met = round(sum(1 for r in rows if str(r.get("met_expectations","")).lower() == "yes") / count * 100)
    gained = round(sum(1 for r in rows if str(r.get("gained_skills","")).lower() == "yes") / count * 100)
    gh = sum(1 for r in rows if r.get("github_link", "").strip())

    return {"count": count, "avg_overall": avg_o, "avg_relevance": avg_r,
            "avg_explanation": avg_e, "avg_practical": avg_p,
            "met_expectations_pct": met, "gained_skills_pct": gained, "github_count": gh}


# ---- 2ND YEAR FEEDBACK HELPERS ----

def save_2ndyear_feedback(data):
    if USE_POSTGRES:
        conn = get_db()
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
        with open(DATA_FILE_2ND, "r") as f:
            store = json.load(f)
        data["timestamp"] = datetime.datetime.now().isoformat()
        store["responses"].append(data)
        with open(DATA_FILE_2ND, "w") as f:
            json.dump(store, f, indent=2, ensure_ascii=False)
        return len(store["responses"])


def get_2ndyear_stats():
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM feedback_2ndyear ORDER BY id")
        rows = cur.fetchall()
        for r in rows:
            if r.get("submitted_at"):
                r["submitted_at"] = r["submitted_at"].isoformat()
        conn.close()
    else:
        with open(DATA_FILE_2ND, "r") as f:
            store = json.load(f)
        rows = store.get("responses", [])

    count = len(rows)
    if count == 0:
        return {"count": 0, "avg_overall": 0, "avg_relevance": 0,
                "avg_explanation": 0, "avg_practical": 0,
                "met_expectations_pct": 0, "gained_skills_pct": 0, "github_count": 0}

    avg_o = round(sum(r["overall_rating"] for r in rows) / count, 2)
    avg_r = round(sum(r["content_relevance"] for r in rows) / count, 2)
    avg_e = round(sum(r["explanation_quality"] for r in rows) / count, 2)
    avg_p = round(sum(r["practical_rating"] for r in rows) / count, 2)
    met = round(sum(1 for r in rows if str(r.get("met_expectations","")).lower() == "yes") / count * 100)
    gained = round(sum(1 for r in rows if str(r.get("gained_skills","")).lower() == "yes") / count * 100)
    gh = sum(1 for r in rows if r.get("github_link", "").strip())

    return {"count": count, "avg_overall": avg_o, "avg_relevance": avg_r,
            "avg_explanation": avg_e, "avg_practical": avg_p,
            "met_expectations_pct": met, "gained_skills_pct": gained, "github_count": gh}


# ---- STRUCTURED FORM HTML (shared template for 2nd & 3rd year) ----

def build_structured_form(year_label, api_endpoint):
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>""" + year_label + """ Workshop Feedback</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0a; color: #e5e7eb; min-height: 100vh;
    display: flex; justify-content: center;
    padding: 20px;
  }
  .card {
    background: #111; border: 1px solid #222; border-radius: 20px;
    padding: 32px 24px; max-width: 480px; width: 100%;
    box-shadow: 0 20px 60px rgba(0,0,0,.5);
  }
  .logo { text-align: center; font-size: 2.2rem; margin-bottom: 6px; }
  h1 {
    text-align: center; font-size: 1.4rem; font-weight: 800;
    background: linear-gradient(135deg, #EF3837, #ff6b6b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
  }
  .subtitle { text-align: center; color: #9ca3af; font-size: 0.85rem; margin-bottom: 24px; }
  label { display: block; color: #ccc; font-size: 0.88rem; margin-bottom: 8px; font-weight: 600; }
  .required::after { content: ' *'; color: #EF3837; }
  input, select, textarea {
    width: 100%; padding: 12px 14px; border-radius: 12px;
    border: 1px solid #333; background: #1a1a1a; color: #e5e7eb;
    font-size: 1rem; margin-bottom: 18px; outline: none;
    transition: border-color .2s;
  }
  input:focus, select:focus, textarea:focus { border-color: #EF3837; }
  textarea { resize: vertical; min-height: 70px; }
  .rating-group { margin-bottom: 18px; }
  .rating-options { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
  .rating-opt {
    flex: 1; min-width: 70px; text-align: center; padding: 10px 6px;
    background: #1a1a1a; border: 2px solid #333; border-radius: 12px;
    cursor: pointer; transition: all .2s; font-size: 0.82rem; color: #ccc;
  }
  .rating-opt:hover { border-color: #555; }
  .rating-opt.selected { border-color: #EF3837; background: #2a1515; color: #fff; }
  .rating-opt .num { font-size: 1.3rem; font-weight: 800; display: block; color: #EF3837; }
  .yesno-group { margin-bottom: 18px; }
  .yesno-options { display: flex; gap: 10px; margin-top: 6px; }
  .yesno-opt {
    flex: 1; text-align: center; padding: 12px 8px;
    background: #1a1a1a; border: 2px solid #333; border-radius: 12px;
    cursor: pointer; transition: all .2s; font-size: 0.95rem; color: #ccc; font-weight: 600;
  }
  .yesno-opt:hover { border-color: #555; }
  .yesno-opt.selected { border-color: #EF3837; background: #2a1515; color: #fff; }
  .submit-btn {
    width: 100%; padding: 15px; border: none; border-radius: 14px;
    background: linear-gradient(135deg, #EF3837, #ff6b6b);
    color: white; font-size: 1.1rem; font-weight: 700;
    cursor: pointer; transition: transform .2s, box-shadow .2s;
    margin-top: 8px;
  }
  .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(239,56,55,.4); }
  .submit-btn:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }
  .divider { border: none; border-top: 1px solid #222; margin: 20px 0; }
  .success { text-align: center; padding: 40px 20px; }
  .success .check { font-size: 4rem; margin-bottom: 12px; }
  .success h2 { color: #22c55e; font-size: 1.4rem; margin-bottom: 8px; }
  .success p { color: #9ca3af; }
  .hidden { display: none; }
</style>
</head>
<body>
<div class="card">
  <div id="formSection">
    <div class="logo">\U0001f9e0</div>
    <h1>CEO of Superintelligence</h1>
    <p class="subtitle">""" + year_label + """ Workshop Feedback</p>

    <div class="rating-group">
      <label class="required">How would you rate the overall day?</label>
      <div class="rating-options">
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <div class="rating-group">
      <label class="required">How relevant was the workshop content to your learning needs?</label>
      <div class="rating-options">
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <div class="rating-group">
      <label class="required">How effectively were the concepts explained?</label>
      <div class="rating-options">
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <div class="rating-group">
      <label class="required">How would you rate the practical sessions / hands-on activities?</label>
      <div class="rating-options">
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <hr class="divider">

    <div class="yesno-group">
      <label class="required">Did the workshop meet your expectations?</label>
      <div class="yesno-options">
        <div class="yesno-opt" onclick="pickYesNo(this, 'met_expectations', 'Yes')">Yes</div>
        <div class="yesno-opt" onclick="pickYesNo(this, 'met_expectations', 'Partially')">Partially</div>
        <div class="yesno-opt" onclick="pickYesNo(this, 'met_expectations', 'No')">No</div>
      </div>
    </div>

    <div class="yesno-group">
      <label class="required">Did you gain new knowledge or practical skills from this workshop?</label>
      <div class="yesno-options">
        <div class="yesno-opt" onclick="pickYesNo(this, 'gained_skills', 'Yes')">Yes</div>
        <div class="yesno-opt" onclick="pickYesNo(this, 'gained_skills', 'No')">No</div>
      </div>
    </div>

    <hr class="divider">

    <label>What was the most useful aspect of the workshop?</label>
    <textarea id="most_useful" placeholder="e.g. The hands-on coding activity..."></textarea>

    <label>Submit your GitHub Repository Link / Google Colab</label>
    <input type="url" id="github_link" placeholder="https://github.com/... or https://colab.research.google.com/...">

    <label>Any additional comments or suggestions?</label>
    <textarea id="additional_comments" placeholder="Optional..."></textarea>

    <label class="required">Email address</label>
    <input type="email" id="email" placeholder="your.name@kalvium.community">

    <button class="submit-btn" id="submitBtn" onclick="submitForm()">Submit Feedback \U0001f680</button>
  </div>

  <div id="successSection" class="success hidden">
    <div class="check">\u2705</div>
    <h2>Thank you!</h2>
    <p>Your feedback has been recorded.<br>Great work today! \U0001f389</p>
  </div>
</div>

<script>
const formData = {
  overall_rating: 0, content_relevance: 0,
  explanation_quality: 0, practical_rating: 0,
  met_expectations: '', gained_skills: ''
};
const API_ENDPOINT = '""" + api_endpoint + """';

function pickRating(el, field, value) {
  el.parentElement.querySelectorAll('.rating-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  formData[field] = value;
}
function pickYesNo(el, field, value) {
  el.parentElement.querySelectorAll('.yesno-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  formData[field] = value;
}
async function submitForm() {
  const email = document.getElementById('email').value.trim();
  if (!email) { alert('Please enter your email address!'); return; }
  if (!formData.overall_rating) { alert('Please rate the overall day!'); return; }
  if (!formData.content_relevance) { alert('Please rate content relevance!'); return; }
  if (!formData.explanation_quality) { alert('Please rate explanation quality!'); return; }
  if (!formData.practical_rating) { alert('Please rate the practical sessions!'); return; }
  if (!formData.met_expectations) { alert('Please select if workshop met expectations!'); return; }
  if (!formData.gained_skills) { alert('Please select if you gained new skills!'); return; }
  const payload = {
    ...formData, email: email,
    most_useful: document.getElementById('most_useful').value.trim(),
    github_link: document.getElementById('github_link').value.trim(),
    additional_comments: document.getElementById('additional_comments').value.trim()
  };
  document.getElementById('submitBtn').disabled = true;
  document.getElementById('submitBtn').textContent = 'Submitting...';
  try {
    const res = await fetch(API_ENDPOINT, {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      document.getElementById('formSection').classList.add('hidden');
      document.getElementById('successSection').classList.remove('hidden');
    } else {
      const err = await res.json();
      alert(err.error || 'Something went wrong. Try again!');
      document.getElementById('submitBtn').disabled = false;
      document.getElementById('submitBtn').textContent = 'Submit Feedback \U0001f680';
    }
  } catch(e) {
    alert('Network error. Try again!');
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('submitBtn').textContent = 'Submit Feedback \U0001f680';
  }
}
</script>
</body>
</html>
"""


# ---- 3RD YEAR FORM HTML (kept for backward compat) ----

FORM_3RDYEAR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>3rd Year Workshop Feedback</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0a; color: #e5e7eb; min-height: 100vh;
    display: flex; justify-content: center;
    padding: 20px;
  }
  .card {
    background: #111; border: 1px solid #222; border-radius: 20px;
    padding: 32px 24px; max-width: 480px; width: 100%;
    box-shadow: 0 20px 60px rgba(0,0,0,.5);
  }
  .logo { text-align: center; font-size: 2.2rem; margin-bottom: 6px; }
  h1 {
    text-align: center; font-size: 1.4rem; font-weight: 800;
    background: linear-gradient(135deg, #EF3837, #ff6b6b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
  }
  .subtitle { text-align: center; color: #9ca3af; font-size: 0.85rem; margin-bottom: 24px; }
  label { display: block; color: #ccc; font-size: 0.88rem; margin-bottom: 8px; font-weight: 600; }
  .required::after { content: ' *'; color: #EF3837; }
  input, select, textarea {
    width: 100%; padding: 12px 14px; border-radius: 12px;
    border: 1px solid #333; background: #1a1a1a; color: #e5e7eb;
    font-size: 1rem; margin-bottom: 18px; outline: none;
    transition: border-color .2s;
  }
  input:focus, select:focus, textarea:focus { border-color: #EF3837; }
  select { appearance: none; cursor: pointer; }
  textarea { resize: vertical; min-height: 70px; }
  .rating-group { margin-bottom: 18px; }
  .rating-options { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
  .rating-opt {
    flex: 1; min-width: 70px; text-align: center; padding: 10px 6px;
    background: #1a1a1a; border: 2px solid #333; border-radius: 12px;
    cursor: pointer; transition: all .2s; font-size: 0.82rem; color: #ccc;
  }
  .rating-opt:hover { border-color: #555; }
  .rating-opt.selected { border-color: #EF3837; background: #2a1515; color: #fff; }
  .rating-opt .num { font-size: 1.3rem; font-weight: 800; display: block; color: #EF3837; }
  .yesno-group { margin-bottom: 18px; }
  .yesno-options { display: flex; gap: 10px; margin-top: 6px; }
  .yesno-opt {
    flex: 1; text-align: center; padding: 12px 8px;
    background: #1a1a1a; border: 2px solid #333; border-radius: 12px;
    cursor: pointer; transition: all .2s; font-size: 0.95rem; color: #ccc; font-weight: 600;
  }
  .yesno-opt:hover { border-color: #555; }
  .yesno-opt.selected { border-color: #EF3837; background: #2a1515; color: #fff; }
  .submit-btn {
    width: 100%; padding: 15px; border: none; border-radius: 14px;
    background: linear-gradient(135deg, #EF3837, #ff6b6b);
    color: white; font-size: 1.1rem; font-weight: 700;
    cursor: pointer; transition: transform .2s, box-shadow .2s;
    margin-top: 8px;
  }
  .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(239,56,55,.4); }
  .submit-btn:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }
  .divider { border: none; border-top: 1px solid #222; margin: 20px 0; }
  .success { text-align: center; padding: 40px 20px; }
  .success .check { font-size: 4rem; margin-bottom: 12px; }
  .success h2 { color: #22c55e; font-size: 1.4rem; margin-bottom: 8px; }
  .success p { color: #9ca3af; }
  .hidden { display: none; }
</style>
</head>
<body>
<div class="card">
  <div id="formSection">
    <div class="logo">🧠</div>
    <h1>CEO of Superintelligence</h1>
    <p class="subtitle">3rd Year Workshop Feedback</p>

    <!-- Q1: Overall Day -->
    <div class="rating-group">
      <label class="required">How would you rate the overall day?</label>
      <div class="rating-options" data-field="overall_rating">
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'overall_rating', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <!-- Q2: Content Relevance -->
    <div class="rating-group">
      <label class="required">How relevant was the workshop content to your learning needs?</label>
      <div class="rating-options" data-field="content_relevance">
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'content_relevance', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <!-- Q3: Explanation Quality -->
    <div class="rating-group">
      <label class="required">How effectively were the concepts explained?</label>
      <div class="rating-options" data-field="explanation_quality">
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'explanation_quality', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <!-- Q4: Practical Sessions -->
    <div class="rating-group">
      <label class="required">How would you rate the practical sessions / hands-on activities?</label>
      <div class="rating-options" data-field="practical_rating">
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 1)"><span class="num">1</span>Poor</div>
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 2)"><span class="num">2</span>Fair</div>
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 3)"><span class="num">3</span>Good</div>
        <div class="rating-opt" onclick="pickRating(this, 'practical_rating', 4)"><span class="num">4</span>Excellent</div>
      </div>
    </div>

    <hr class="divider">

    <!-- Q5: Met Expectations -->
    <div class="yesno-group">
      <label class="required">Did the workshop meet your expectations?</label>
      <div class="yesno-options" data-field="met_expectations">
        <div class="yesno-opt" onclick="pickYesNo(this, 'met_expectations', 'Yes')">Yes</div>
        <div class="yesno-opt" onclick="pickYesNo(this, 'met_expectations', 'Partially')">Partially</div>
        <div class="yesno-opt" onclick="pickYesNo(this, 'met_expectations', 'No')">No</div>
      </div>
    </div>

    <!-- Q6: Gained Skills -->
    <div class="yesno-group">
      <label class="required">Did you gain new knowledge or practical skills from this workshop?</label>
      <div class="yesno-options" data-field="gained_skills">
        <div class="yesno-opt" onclick="pickYesNo(this, 'gained_skills', 'Yes')">Yes</div>
        <div class="yesno-opt" onclick="pickYesNo(this, 'gained_skills', 'No')">No</div>
      </div>
    </div>

    <hr class="divider">

    <!-- Q7: Most Useful -->
    <label>What was the most useful aspect of the workshop?</label>
    <textarea id="most_useful" placeholder="e.g. The hands-on coding activity..."></textarea>

    <!-- Q8: GitHub Link -->
    <label>Submit your GitHub Repository Link / Google Colab</label>
    <input type="url" id="github_link" placeholder="https://github.com/... or https://colab.research.google.com/...">

    <!-- Q9: Additional Comments -->
    <label>Any additional comments or suggestions?</label>
    <textarea id="additional_comments" placeholder="Optional..."></textarea>

    <!-- Q10: Email -->
    <label class="required">Email address</label>
    <input type="email" id="email" placeholder="your.name@kalvium.community">

    <button class="submit-btn" id="submitBtn" onclick="submitForm()">Submit Feedback 🚀</button>
  </div>

  <div id="successSection" class="success hidden">
    <div class="check">✅</div>
    <h2>Thank you!</h2>
    <p>Your feedback has been recorded.<br>Great work today! 🎉</p>
  </div>
</div>

<script>
const formData = {
  overall_rating: 0,
  content_relevance: 0,
  explanation_quality: 0,
  practical_rating: 0,
  met_expectations: '',
  gained_skills: ''
};

function pickRating(el, field, value) {
  el.parentElement.querySelectorAll('.rating-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  formData[field] = value;
}

function pickYesNo(el, field, value) {
  el.parentElement.querySelectorAll('.yesno-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  formData[field] = value;
}

async function submitForm() {
  const email = document.getElementById('email').value.trim();
  if (!email) { alert('Please enter your email address!'); return; }
  if (!formData.overall_rating) { alert('Please rate the overall day!'); return; }
  if (!formData.content_relevance) { alert('Please rate content relevance!'); return; }
  if (!formData.explanation_quality) { alert('Please rate explanation quality!'); return; }
  if (!formData.practical_rating) { alert('Please rate the practical sessions!'); return; }
  if (!formData.met_expectations) { alert('Please select if workshop met expectations!'); return; }
  if (!formData.gained_skills) { alert('Please select if you gained new skills!'); return; }

  const payload = {
    ...formData,
    email: email,
    most_useful: document.getElementById('most_useful').value.trim(),
    github_link: document.getElementById('github_link').value.trim(),
    additional_comments: document.getElementById('additional_comments').value.trim()
  };

  document.getElementById('submitBtn').disabled = true;
  document.getElementById('submitBtn').textContent = 'Submitting...';

  try {
    const res = await fetch('/api/3rdyear/submit', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      document.getElementById('formSection').classList.add('hidden');
      document.getElementById('successSection').classList.remove('hidden');
    } else {
      const err = await res.json();
      alert(err.error || 'Something went wrong. Try again!');
      document.getElementById('submitBtn').disabled = false;
      document.getElementById('submitBtn').textContent = 'Submit Feedback 🚀';
    }
  } catch(e) {
    alert('Network error. Try again!');
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('submitBtn').textContent = 'Submit Feedback 🚀';
  }
}
</script>
</body>
</html>
"""


# ---- MOBILE FORM HTML (Round-based, 2nd year) ----

FORM_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Workshop Feedback</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0a; color: #e5e7eb; min-height: 100vh;
    display: flex; justify-content: center; align-items: center;
    padding: 20px;
  }
  .card {
    background: #111; border: 1px solid #222; border-radius: 20px;
    padding: 32px 28px; max-width: 420px; width: 100%;
    box-shadow: 0 20px 60px rgba(0,0,0,.5);
  }
  .logo { text-align: center; font-size: 2.5rem; margin-bottom: 8px; }
  h1 {
    text-align: center; font-size: 1.5rem; font-weight: 800;
    background: linear-gradient(135deg, #EF3837, #ff6b6b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
  }
  .round-label {
    text-align: center; color: #9ca3af; font-size: 0.9rem; margin-bottom: 24px;
  }
  label { display: block; color: #9ca3af; font-size: 0.85rem; margin-bottom: 6px; font-weight: 600; }
  input, select, textarea {
    width: 100%; padding: 12px 14px; border-radius: 12px;
    border: 1px solid #333; background: #1a1a1a; color: #e5e7eb;
    font-size: 1rem; margin-bottom: 16px; outline: none;
    transition: border-color .2s;
  }
  input:focus, select:focus, textarea:focus { border-color: #EF3837; }
  textarea { resize: vertical; min-height: 80px; }
  .emoji-row { display: flex; justify-content: center; gap: 12px; margin-bottom: 20px; }
  .emoji-btn {
    font-size: 2rem; background: #1a1a1a; border: 2px solid #333;
    border-radius: 14px; width: 56px; height: 56px;
    cursor: pointer; transition: all .2s; display: flex;
    align-items: center; justify-content: center;
  }
  .emoji-btn:hover { transform: scale(1.15); }
  .emoji-btn.selected { border-color: #EF3837; background: #2a1515; transform: scale(1.15); }
  .submit-btn {
    width: 100%; padding: 14px; border: none; border-radius: 14px;
    background: linear-gradient(135deg, #EF3837, #ff6b6b);
    color: white; font-size: 1.1rem; font-weight: 700;
    cursor: pointer; transition: transform .2s, box-shadow .2s;
  }
  .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(239,56,55,.4); }
  .submit-btn:disabled { opacity: .5; cursor: not-allowed; transform: none; box-shadow: none; }
  .success { text-align: center; padding: 40px 20px; }
  .success .check { font-size: 4rem; margin-bottom: 12px; }
  .success h2 { color: #22c55e; font-size: 1.4rem; margin-bottom: 8px; }
  .success p { color: #9ca3af; }
  .hidden { display: none; }
</style>
</head>
<body>

<div class="card">
  <div id="formSection">
    <div class="logo">🧠</div>
    <h1>Quick Feedback</h1>
    <div class="round-label" id="roundLabel">Round {{ round_num }} of 3</div>

    <label>Your Name</label>
    <input type="text" id="name" placeholder="e.g. Dharini" autocomplete="off">

    <label>How's the session so far?</label>
    <div class="emoji-row">
      <button class="emoji-btn" data-rating="1" onclick="pickRating(this)">😴</button>
      <button class="emoji-btn" data-rating="2" onclick="pickRating(this)">😐</button>
      <button class="emoji-btn" data-rating="3" onclick="pickRating(this)">🙂</button>
      <button class="emoji-btn" data-rating="4" onclick="pickRating(this)">😃</button>
      <button class="emoji-btn" data-rating="5" onclick="pickRating(this)">🤯</button>
    </div>

    <label>One thing you learned / want more of</label>
    <textarea id="feedback" placeholder="Type here..."></textarea>

    <button class="submit-btn" id="submitBtn" onclick="submitFeedback()">Submit Feedback 🚀</button>
  </div>

  <div id="successSection" class="success hidden">
    <div class="check">✅</div>
    <h2>Thanks!</h2>
    <p>Your feedback has been recorded.<br>Enjoy the rest of the session! 🎉</p>
  </div>
</div>

<script>
let selectedRating = 0;
const roundNum = {{ round_num }};

function pickRating(btn) {
  document.querySelectorAll('.emoji-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  selectedRating = parseInt(btn.dataset.rating);
}

async function submitFeedback() {
  const name = document.getElementById('name').value.trim();
  const feedback = document.getElementById('feedback').value.trim();
  if (!name) { alert('Please enter your name!'); return; }
  if (!selectedRating) { alert('Please pick an emoji rating!'); return; }

  document.getElementById('submitBtn').disabled = true;
  document.getElementById('submitBtn').textContent = 'Submitting...';

  try {
    const res = await fetch('/api/submit', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ name, rating: selectedRating, feedback, round: roundNum })
    });
    if (res.ok) {
      document.getElementById('formSection').classList.add('hidden');
      document.getElementById('successSection').classList.remove('hidden');
    } else {
      alert('Something went wrong. Try again!');
      document.getElementById('submitBtn').disabled = false;
      document.getElementById('submitBtn').textContent = 'Submit Feedback 🚀';
    }
  } catch(e) {
    alert('Network error. Try again!');
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('submitBtn').textContent = 'Submit Feedback 🚀';
  }
}
</script>
</body>
</html>
"""


# ---- ROUTES ----

@app.route("/")
def index():
    return render_template_string(FORM_HTML, round_num=1)

@app.route("/round/<int:num>")
def feedback_round(num):
    num = max(1, min(3, num))
    return render_template_string(FORM_HTML, round_num=num)

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name", "").strip()
    rating = data.get("rating", 0)
    feedback_text = data.get("feedback", "").strip()
    round_num = data.get("round", 1)

    if not name or not rating:
        return jsonify({"error": "Name and rating required"}), 400

    count = save_feedback(round_num, name, rating, feedback_text)
    return jsonify({"status": "ok", "count": count})

@app.route("/api/stats")
def stats():
    return jsonify(get_all_stats())

@app.route("/api/reset", methods=["POST"])
def reset():
    reset_all()
    return jsonify({"status": "reset"})

@app.route("/3rdyear")
def form_3rdyear():
    """3rd year workshop feedback form."""
    return build_structured_form("3rd Year", "/api/3rdyear/submit")

@app.route("/2ndyear")
def form_2ndyear():
    """2nd year workshop feedback form."""
    return build_structured_form("2nd Year", "/api/2ndyear/submit")

@app.route("/api/3rdyear/submit", methods=["POST"])
def submit_3rdyear():
    data = request.get_json()
    required = ["email", "overall_rating", "content_relevance",
                "explanation_quality", "practical_rating",
                "met_expectations", "gained_skills"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    count = save_3rdyear_feedback(data)
    return jsonify({"status": "ok", "count": count})

@app.route("/api/2ndyear/submit", methods=["POST"])
def submit_2ndyear():
    data = request.get_json()
    required = ["email", "overall_rating", "content_relevance",
                "explanation_quality", "practical_rating",
                "met_expectations", "gained_skills"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    count = save_2ndyear_feedback(data)
    return jsonify({"status": "ok", "count": count})

@app.route("/api/3rdyear/stats")
def stats_3rdyear():
    return jsonify(get_3rdyear_stats())

@app.route("/api/2ndyear/stats")
def stats_2ndyear():
    return jsonify(get_2ndyear_stats())

@app.route("/api/download")
def download():
    """Download ALL feedback as CSV — use after workshop."""
    all_stats = get_all_stats()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Round", "Name", "Rating", "Feedback", "Timestamp"])
    for r in [1, 2, 3]:
        for e in all_stats[f"round_{r}"]["entries"]:
            writer.writerow([
                f"Round {r}",
                e.get("name", ""),
                e.get("rating", ""),
                e.get("feedback", ""),
                e.get("timestamp", e.get("submitted_at", ""))
            ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=workshop_feedback.csv"}
    )

@app.route("/api/3rdyear/download")
def download_3rdyear():
    """Download 3rd year feedback as CSV."""
    stats = get_3rdyear_stats()
    # Re-fetch raw rows for CSV
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM feedback_3rdyear ORDER BY id")
        rows = cur.fetchall()
        conn.close()
    else:
        with open(DATA_FILE_3RD, "r") as f:
            rows = json.load(f).get("responses", [])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Overall Rating", "Content Relevance",
                     "Explanation Quality", "Practical Rating",
                     "Met Expectations", "Gained Skills",
                     "Most Useful", "GitHub Link", "Additional Comments", "Email"])
    for r in rows:
        writer.writerow([
            r.get("submitted_at", r.get("timestamp", "")),
            r.get("overall_rating", ""), r.get("content_relevance", ""),
            r.get("explanation_quality", ""), r.get("practical_rating", ""),
            r.get("met_expectations", ""), r.get("gained_skills", ""),
            r.get("most_useful", ""), r.get("github_link", ""),
            r.get("additional_comments", ""), r.get("email", ""),
        ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=3rdyear_feedback.csv"}
    )

@app.route("/api/2ndyear/download")
def download_2ndyear():
    """Download 2nd year feedback as CSV."""
    if USE_POSTGRES:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM feedback_2ndyear ORDER BY id")
        rows = cur.fetchall()
        conn.close()
    else:
        with open(DATA_FILE_2ND, "r") as f:
            rows = json.load(f).get("responses", [])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Overall Rating", "Content Relevance",
                     "Explanation Quality", "Practical Rating",
                     "Met Expectations", "Gained Skills",
                     "Most Useful", "GitHub Link", "Additional Comments", "Email"])
    for r in rows:
        writer.writerow([
            r.get("submitted_at", r.get("timestamp", "")),
            r.get("overall_rating", ""), r.get("content_relevance", ""),
            r.get("explanation_quality", ""), r.get("practical_rating", ""),
            r.get("met_expectations", ""), r.get("gained_skills", ""),
            r.get("most_useful", ""), r.get("github_link", ""),
            r.get("additional_comments", ""), r.get("email", ""),
        ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=2ndyear_feedback.csv"}
    )


# ---- LOCAL DEV ----

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"\n{'='*50}")
    print(f"  📡 Feedback Server Running!")
    print(f"  Local:   http://localhost:5111")
    print(f"  Network: http://{ip}:5111")
    print(f"{'='*50}\n")
    app.run(host="0.0.0.0", port=5111, debug=False)
