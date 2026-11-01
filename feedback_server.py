"""
Live Feedback Server for Workshop
Run: python feedback_server.py
Opens on port 5111
Students scan QR → land on a simple form → submit name + feedback
All feedback stored in feedback_data.json
"""

from flask import Flask, request, jsonify, render_template_string
import json, os, datetime, socket

app = Flask(__name__)
DATA_FILE = "feedback_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"round_1": [], "round_2": [], "round_3": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Initialize file
if not os.path.exists(DATA_FILE):
    save_data({"round_1": [], "round_2": [], "round_3": []})

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
  .success {
    text-align: center; padding: 40px 20px;
  }
  .success .check { font-size: 4rem; margin-bottom: 12px; }
  .success h2 { color: #22c55e; font-size: 1.4rem; margin-bottom: 8px; }
  .success p { color: #9ca3af; }
  .hidden { display: none; }
</style>
</head>
<body>

<div class="card">
  <!-- FORM -->
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

  <!-- SUCCESS -->
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

ROUND_NAMES = {1: "round_1", 2: "round_2", 3: "round_3"}

@app.route("/")
def index():
    """Default → round 1"""
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
    feedback = data.get("feedback", "").strip()
    round_num = data.get("round", 1)
    round_key = ROUND_NAMES.get(round_num, "round_1")

    if not name or not rating:
        return jsonify({"error": "Name and rating required"}), 400

    entry = {
        "name": name,
        "rating": rating,
        "feedback": feedback,
        "timestamp": datetime.datetime.now().isoformat()
    }

    all_data = load_data()
    all_data[round_key].append(entry)
    save_data(all_data)

    return jsonify({"status": "ok", "count": len(all_data[round_key])})

@app.route("/api/stats")
def stats():
    """Returns counts and data for all rounds — used by Streamlit polling."""
    all_data = load_data()
    result = {}
    for key in ["round_1", "round_2", "round_3"]:
        entries = all_data.get(key, [])
        ratings = [e["rating"] for e in entries]
        result[key] = {
            "count": len(entries),
            "avg_rating": round(sum(ratings)/len(ratings), 1) if ratings else 0,
            "entries": entries
        }
    return jsonify(result)

@app.route("/api/reset", methods=["POST"])
def reset():
    """Reset all feedback data (use before a new workshop)."""
    save_data({"round_1": [], "round_2": [], "round_3": []})
    return jsonify({"status": "reset"})

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

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"\n{'='*50}")
    print(f"  📡 Feedback Server Running!")
    print(f"  Local:   http://localhost:5111")
    print(f"  Network: http://{ip}:5111")
    print(f"  Share this with students (same WiFi)")
    print(f"{'='*50}\n")
    app.run(host="0.0.0.0", port=5111, debug=False)
