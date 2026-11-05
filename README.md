# 🤖 Building AI Agents Workshop — SRM AP x Kalvium

Interactive Streamlit slide decks for the **"Building AI Agents"** workshop at SRM University AP, November 2026. Two versions tailored to different audiences.

---

## 🚀 Deployed Links

| Service | URL | Description |
|---------|-----|-------------|
| **2nd Year Slides** | [workshop-slides-2ndyear.onrender.com](https://workshop-slides-2ndyear.onrender.com) | Streamlit slide deck (`app_2ndyear.py`) |
| **3rd Year Slides** | [workshop-slides.onrender.com](https://workshop-slides.onrender.com) | Streamlit slide deck (`app.py`) |
| **Feedback API** | [workshop-feedback-ismc.onrender.com](https://workshop-feedback-ismc.onrender.com) | Flask backend for live feedback & stats |
| **2nd Year Feedback Form** | [workshop-feedback-2ndyear.onrender.com](https://workshop-feedback-2ndyear.onrender.com) | Standalone Streamlit feedback form (QR scan) |

---

## 📁 Project Structure

```
├── app_2ndyear.py          # 2nd Year slide deck (Streamlit)
├── app.py                  # 3rd Year slide deck (Streamlit)
├── feedback_server.py      # Flask API — feedback collection + stats
├── feedback_form.py        # 2nd Year standalone feedback form (Streamlit)
├── generate_briefing_doc.py# Script to generate WORKSHOP_BRIEFING.docx
├── render.yaml             # Render deployment config (all 4 services)
├── requirements.txt        # Python dependencies
├── .streamlit/             # Streamlit theme config
├── SPEAKER_SCRIPT.md       # 3rd Year speaker notes
├── SPEAKER_SCRIPT_2NDYEAR.md # 2nd Year speaker notes
├── WORKSHOP_BRIEFING.md    # Full workshop briefing document
├── Demo7_Gradio_Agent.ipynb# Colab notebook for Gradio agent demo (3rd year)
├── Worksheet_*.pdf/.md     # Printable student worksheets
└── feedback_*.json         # Local feedback data snapshots
```

---

## 🎓 2nd Year Workshop — `app_2ndyear.py`

**Theme:** AI Fundamentals → RAG → No-Code Agents  
**Target:** 2nd year students, beginner-friendly, no prior AI experience assumed

### Slide Flow

1. Title
2. How LLMs Work
3. Setup (Groq API key)
4. **Demo 1: Roast My Insta Bio** — 4 roast styles
5. Prompt Engineering 101
6. **Activity 1: Prompt Battle** — write system prompts to review a resume
7. Quiz 1: AI Fundamentals
8. What is RAG?
9. **Demo 2: RAG Pipeline** — chat with campus notes
10. Quiz 2: RAG Basics
11. What are AI Agents?
12. Demo 3: No-Code Agent (n8n)
13. Systems Thinking
14. Activity 2: Build Your Agent
15. Final Quiz
16. Workshop Feedback
17. What to Learn Next
18. Quick Links / Timer

### 🔥 Demo 1 — Roast My Insta Bio (4 System Prompts)

| Style | System Prompt |
|-------|---------------|
| **Savage (Funny)** | *"You are a savage social media roast comedian. Roast Instagram bios like a stand-up special. Be brutally funny but reference specific things from the bio. Keep it fun, not mean-spirited."* |
| **Brutally Honest (Helpful)** | *"You are a personal branding expert who reviews social media bios. Give honest, direct feedback on what works, what's cringe, and how to actually stand out."* |
| **Gen-Z Slang** | *"You are a gen-z social media guru who speaks in memes, slang, and internet culture. Use 'bruh', 'no cap', 'lowkey', 'giving', 'slay', etc. Still give real advice though."* |
| **Indian Aunty** | *"You are a nosy Indian aunty who saw your Instagram bio. React the way an aunty would — comparing to Sharma ji ka beta, asking about studies, questioning life choices. Be dramatic and hilarious but sneak in real advice."* |

**Response structure prompt appended to all styles:**
```
Structure your response as:
THE ROAST (savage but specific — quote actual lines from the bio)
CRINGE-O-METER (rate the cringe level 1-10 with explanation)
THE GLOW-UP (rewrite the bio so it actually slaps)
```
**Model:** `qwen/qwen3.8-27b` · **Temperature:** 0.9 · **Max tokens:** 700

### ⚔️ Activity 1 — Prompt Battle

**Default resume/text to test against:**
```
Skills: HTML, CSS. Projects: Calculator app. Experience: None. GPA: 6.8
```

**Suggested persona starters:**
- *"You are a strict Indian parent who just found out their child's career choices..."*
- *"You are a dramatic Bollywood narrator reviewing a resume like it's a movie script..."*
- *"You are Virat Kohli giving a dressing room pep talk about this resume..."*

Students write their own system prompt, test it, and iterate. Best result shared with the group.

### 📚 Demo 2 — RAG Pipeline (Sample Notes & Prompts)

**Default knowledge base (10 campus facts, one per line):**
```
SRM AP campus is located in Amaravati, Andhra Pradesh.
The library is open from 8 AM to 10 PM on weekdays.
The cafeteria serves breakfast from 7:30 AM to 9:30 AM.
Wi-Fi password for students can be obtained from the IT helpdesk in Block A.
The coding club meets every Wednesday at 5 PM in Room 301.
Semester exams usually start in the last week of November.
The placement cell is located on the 2nd floor of the admin building.
Students need a minimum of 75% attendance to sit for exams.
The sports complex has a gym, basketball court, and swimming pool.
The campus bus service runs every 30 minutes from the main gate.
```

**RAG system prompt:**
```
Answer ONLY from the notes provided. If the answer is not in the notes, say 'That's not in your notes!' Be helpful and concise.
```

**User message format:**
```
NOTES:
{retrieved context chunks}

QUESTION: {user question}
```

**Default test questions:**
- In-notes: *"What time does the library close?"*
- Trick (not in notes): *"What's the Instagram password for the college page?"*

**Model:** `qwen/qwen3.8-27b` · **Temperature:** 0.3 · **Max tokens:** 300 · **Vector DB:** ChromaDB (in-memory)

### ✅ Quiz Answers — 2nd Year

**Quiz 1: AI Fundamentals (4 questions)**
1. **B)** Predicts the most likely next word based on patterns
2. **B)** A message that sets the AI's personality and behavior
3. **B)** How creative vs predictable the output is
4. **B)** Trained on past data — no live internet access

**Quiz 2: RAG Basics (4 questions)**
1. **B)** Retrieval Augmented Generation
2. **C)** Looking up the relevant pages before answering
3. **B)** Numbers that capture the meaning of text
4. **C)** Honestly say it doesn't have that info

**Final Quiz (5 questions)**
1. **B)** RAG — store, retrieve, then answer
2. **B)** Agents use tools and decide autonomously
3. **B)** Better prompt with role, structure, examples
4. **B)** AI's personality, behavior, and rules
5. **C)** Orchestrating AI — the CEO mindset!

---

## 🎓 3rd Year Workshop — `app.py`

**Theme:** AI Agents deep-dive → Embeddings → RAG → Code Agents → Gradio Deploy  
**Target:** 3rd year students with some coding experience

### Slide Flow

1. Title
2. The 5 Levels of AI Users
3. Setup (Groq API key)
4. **Demo 1: Roast My Resume** — 3 roast styles
5. Demo 1: Code Behind
6. Demo 2: Level 1 vs Level 4 (web search + reasoning)
7. Demo 2: Code Behind
8. Demo 3: Embeddings (GPS for meaning)
9. Demo 3: Code Behind
10. ⚡ Feedback Round 1
11. Quiz 1: Agents Basics
12. **Demo 4: RAG Pipeline** — chat with CS notes
13. Demo 4: Code Behind
14. Demo 5: No-Code Agent (Dify.ai)
15. ⚡ Feedback Round 2
16. Quiz 2: RAG and Embeddings
17. Activity 1: Prompt Engineering
18. Demo 6: Code Agent
19. Demo 6: Code Behind
20. Demo 7: Gradio Deploy
21. Demo 7: Colab Instructions
22. ⚡ Feedback Round 3
23. Quiz 3: Building Agents
24. Activity 2: Build a RAG
25. Activity 3: Build an Agent
26. Activity 4: Hackathon
27. Final Quiz
28. 3rd Year Feedback
29. Quick Links / Timer

### 🔥 Demo 1 — Roast My Resume (3 System Prompts)

| Style | System Prompt |
|-------|---------------|
| **Savage (Funny)** | *"You are a brutally honest recruiter who roasts resumes like a stand-up comedy special. Be savage but educational."* |
| **Professional (Helpful)** | *"You are a senior tech recruiter. Give honest, direct, constructive feedback."* |
| **Gen-Z Slang** | *"You are a gen-z career coach who speaks in memes, slang, and internet culture. Still give real advice."* |

**Default sample resume:**
```
RESUME
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
Hobbies: Coding, Reading, Cricket
```

### 📚 Demo 4 — RAG Pipeline (Sample Notes)

**Default knowledge base (CS/DSA topics):**
```
Arrays store elements in contiguous memory. O(1) access by index.
Stacks follow LIFO. Push/Pop are O(1). Used in function calls, undo operations.
Queues follow FIFO. Enqueue/Dequeue are O(1). Used in BFS, print spooling.
Binary Search Trees: O(log n) average search/insert/delete.
BFS uses a queue -- shortest path in unweighted graphs. DFS uses stack/recursion -- cycle detection.
Dynamic Programming: overlapping subproblems + optimal substructure. Memoization vs tabulation.
Hash tables: O(1) average lookup. Collisions handled by chaining or open addressing.
REST APIs: GET (read), POST (create), PUT (update), DELETE (remove). JSON format.
```

### ✅ Quiz Answers — 3rd Year

**Quiz 1: Agents Basics (3 questions)**
1. **B)** Brain (LLM), Memory (RAG), Tools, Orchestrator
2. **C)** An agent can use tools and act autonomously
3. **C)** The logic that decides WHAT to do WHEN

**Quiz 2: RAG and Embeddings (4 questions)**
1. **B)** Retrieval Augmented Generation
2. **C)** Numbers that capture the meaning of text
3. **B)** To search by meaning instead of keywords
4. **C)** Good RAG says "I don't have that info"

**Quiz 3: Building Agents (3 questions)**
1. **B)** Quick prototyping and simple agents
2. **B)** Agents use tools and decide autonomously
3. **B)** No-code prototyping + code for full control

**Final Quiz (3 questions)**
1. **B)** RAG — embed notes in vector DB, retrieve chunks
2. **B)** A tool — a weather API it can call
3. **C)** Orchestrating AI — knowing what to build and how to connect tools

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit (slides + feedback form)
- **Backend:** Flask (feedback API)
- **AI Model:** Groq API → `qwen/qwen3.8-27b`
- **Vector DB:** ChromaDB (in-memory, for RAG demos)
- **Web Search:** DuckDuckGo Search (3rd year Level 4 demo)
- **Database:** PostgreSQL on Render (feedback storage)
- **Deployment:** Render (all services)

## 🔑 Environment Variables

| Variable | Used By | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | Slide apps | Groq API key (entered by students at runtime via Setup slide) |
| `FEEDBACK_URL` | Slide apps | URL of the feedback Flask API |
| `FEEDBACK_FORM_URL` | 2nd year app | URL of the standalone feedback form |
| `DATABASE_URL` | Feedback server + form | PostgreSQL connection string |

> **No API keys are committed in this repo.** Students enter their own Groq API key during the workshop via the Setup slide.

## 🏃 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run 2nd year slides
streamlit run app_2ndyear.py

# Run 3rd year slides
streamlit run app.py

# Run feedback API
python feedback_server.py

# Run feedback form
streamlit run feedback_form.py
```

---

**Workshop by [Dharini Srinivasan](https://github.com/Dharini-MernStack) · SRM University AP x Kalvium · November 2026**
