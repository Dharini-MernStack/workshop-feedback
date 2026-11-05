"""Generate the CEO Briefing .docx from scratch."""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

doc = Document()

# ---- Page margins ----
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

# ---- Style helpers ----
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
style.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

def heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0xEF, 0x38, 0x37) if level == 1 else RGBColor(0x22, 0x22, 0x22)
    return h

def para(text, bold=False, italic=False, size=None, color=None, align=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    if size: run.font.size = Pt(size)
    if color: run.font.color.rgb = color
    if align: p.alignment = align
    return p

def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p

def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
    return table

def spacer():
    doc.add_paragraph()

# =====================================================================
# DOCUMENT CONTENT
# =====================================================================

# ---- COVER ----
spacer()
spacer()
para("CEO OF SUPERINTELLIGENCE", bold=True, size=28, color=RGBColor(0xEF, 0x38, 0x37), align=WD_ALIGN_PARAGRAPH.CENTER)
para("Workshop Briefing Document", bold=True, size=16, color=RGBColor(0x55, 0x55, 0x55), align=WD_ALIGN_PARAGRAPH.CENTER)
spacer()
para("AI Skills Workshop — Kalvium × SRM AP", size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
para("November 2026", size=12, color=RGBColor(0x99, 0x99, 0x99), align=WD_ALIGN_PARAGRAPH.CENTER)
spacer()
para("Prepared by: Dharini Srinivasan", size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
para("Format: Full-day workshop (per batch)", size=11, color=RGBColor(0x99, 0x99, 0x99), align=WD_ALIGN_PARAGRAPH.CENTER)
para("Batches: 2nd Year BTech CSE + 3rd Year BTech CSE", size=11, color=RGBColor(0x99, 0x99, 0x99), align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_page_break()

# ---- 1. LIVE LINKS ----
heading("1. Live Workshop Links", level=1)
para("All services are deployed and accessible via browser on any device.")
add_table(
    ["Resource", "Link"],
    [
        ["2nd Year Slide Deck", "https://workshop-slides-2ndyear.onrender.com"],
        ["3rd Year Slide Deck", "https://workshop-slides.onrender.com"],
        ["2nd Year Feedback Form (QR)", "https://workshop-feedback-2ndyear.onrender.com"],
        ["Feedback Data API", "https://workshop-feedback-ismc.onrender.com"],
    ]
)
spacer()

# ---- 2. OVERVIEW ----
heading("2. Workshop Overview", level=1)

heading("Theme", level=2)
para('"Become the CEO of Superintelligence" — a hands-on, zero-to-builder workshop where students move from passively using AI to understanding, controlling, and building AI agents.')

heading("Core Message", level=2)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Person at Level 1: "AI will take my job"\nPerson at Level 5: "I just automated my job and started a side business"\n\nSame AI. Different user. Different outcome.')
run.italic = True
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

heading("The 5 Levels Framework", level=2)
para("This framework anchors the entire workshop — students self-assess at the start and track their progress.")
add_table(
    ["Level", "Role", "Skill", "Signature Phrase"],
    [
        ["1", "Consumer", "Uses ChatGPT", '"Hey ChatGPT"'],
        ["2", "Prompter", "Prompt engineering", '"Think step by step"'],
        ["3", "Integrator", "Feeds own data (RAG)", '"Here\'s MY data"'],
        ["4", "Agent Builder", "Builds agents + tools", '"Use tools, decide"'],
        ["5", "CEO", "Orchestrates agent teams", '"Run the company"'],
    ]
)
spacer()

# ---- 3. BATCH COMPARISON ----
heading("3. What's Different Between the Two Batches", level=1)

add_table(
    ["Aspect", "3rd Year (Advanced)", "2nd Year (Beginner)"],
    [
        ["Starting Level", "Level 2", "Level 1"],
        ["Target Level", "Level 4–5", "Level 3 (peek at 4)"],
        ["Coding Required", "Yes — Python", "No — n8n (no-code)"],
        ["API Usage", "Groq API via code", "Groq API via n8n"],
        ["Agent Building", "Python + LangChain patterns", "n8n drag-and-drop"],
        ["Deployment", "Google Colab + Gradio (public URL)", "n8n shareable workflow"],
        ["Tone", "Fast-paced, technical", "Friendly, analogy-heavy"],
        ["Assumption", "Knows Python, APIs", "May have no coding experience"],
    ]
)
spacer()

# ---- 4. SESSION FLOW — 3RD YEAR ----
heading("4. Session Flow — 3rd Year", level=1)
para("29 slides  |  ~6 hours  |  Demos → Code → Quizzes → Hands-on Activities → Hackathon", bold=True)

heading("Morning Block — Concepts + Demos", level=2)
add_table(
    ["#", "Slide", "What Happens", "Min"],
    [
        ["1", "Title", "Opening hook — Level 1 vs Level 5 quote", "3"],
        ["2", "The 5 Levels", "Framework intro — self-assessment", "5"],
        ["3", "API Key Setup", "Everyone gets free Groq API key", "8"],
        ["4", "Demo 1: Roast My Resume", "Live demo — AI roasts resumes in 3 styles", "8"],
        ["5", "Demo 1: Code Behind", "10 lines of Python walkthrough", "5"],
        ["6", "Demo 2: Level 1 vs Level 4", "Side-by-side: generic answer vs agent with web search", "10"],
        ["7", "Demo 2: Code Behind", "Search → retrieve → reason pattern", "5"],
        ["8", "Demo 3: Embeddings", "Text → numbers → meaning. Similarity visualized", "8"],
        ["9", "Demo 3: Code Behind", "sentence-transformers + cosine similarity", "5"],
        ["10", "Feedback Round 1", "Quick emoji pulse check via QR", "3"],
        ["11", "Quiz 1: Agent Basics", "3 multiple-choice questions", "5"],
    ]
)
spacer()

heading("Midday Block — RAG + No-Code", level=2)
add_table(
    ["#", "Slide", "What Happens", "Min"],
    [
        ["12", "Demo 4: RAG Pipeline", "Build working RAG — load notes, query, test failure", "12"],
        ["13", "Demo 4: Code Behind", "ChromaDB + Groq in 30 lines", "5"],
        ["14", "Demo 5: No-Code Agent (Dify.ai)", "Full agent built live, zero code, 4 minutes", "10"],
        ["15", "Feedback Round 2", "Midway pulse check", "3"],
        ["16", "Quiz 2: RAG & Embeddings", "4 questions", "5"],
    ]
)
spacer()

heading("Afternoon Block — Hands-on Building", level=2)
add_table(
    ["#", "Slide", "What Happens", "Min"],
    [
        ["17", "Activity 1: Prompt Engineering", "15-min challenge — best system prompt", "15"],
        ["18", "Demo 6: Code Agent", "Agent decides which tool to use autonomously", "10"],
        ["19", "Demo 6: Code Behind", "Agent loop: ask → tool → result → repeat", "5"],
        ["20", "Demo 7: Gradio Deploy", "Agent → web app with public URL", "8"],
        ["21", "Demo 7: Colab Instructions", "Step-by-step Google Colab setup", "10"],
        ["22", "Feedback Round 3", "Final pulse check", "3"],
        ["23", "Quiz 3: Building Agents", "3 questions", "5"],
        ["24", "Activity 2: Build a RAG", "25 min — RAG over own study material", "25"],
        ["25", "Activity 3: Custom Agent Tool", "30 min — add custom tool to agent", "30"],
        ["26", "Activity 4: Mini Hackathon", "45 min — teams build + deploy agent", "45"],
        ["27", "Final Quiz", "3 comprehensive questions", "5"],
        ["28", "Workshop Feedback", "Structured form via QR, live count", "5"],
        ["29", "Quick Links", "All resources + learning paths", "2"],
    ]
)
spacer()

heading("What 3rd Years Build", level=2)
bullet("Resume roaster ", bold_prefix="(Prompt Engineering) — ")
bullet("Research agent with live web search ", bold_prefix="(Agent + Tools) — ")
bullet("Embedding similarity system ", bold_prefix="(Understanding Meaning) — ")
bullet("RAG pipeline over custom notes ", bold_prefix="(RAG) — ")
bullet("No-code agent on Dify.ai ", bold_prefix="(Rapid Prototyping) — ")
bullet("Code agent with custom tools ", bold_prefix="(Full Control) — ")
bullet("Deployed Gradio app with public URL ", bold_prefix="(Final Deliverable) — ")
spacer()

# ---- 5. SESSION FLOW — 2ND YEAR ----
heading("5. Session Flow — 2nd Year", level=1)
para("21 slides  |  ~5 hours  |  Beginner-friendly, analogy-driven, no-code focus", bold=True)

heading("Morning Block — Understanding AI", level=2)
add_table(
    ["#", "Slide", "What Happens", "Min"],
    [
        ["1", "Title", "Opening — AI Skills Workshop, Kalvium × SRM AP", "3"],
        ["2", "The 5 Levels", "Framework — 'You're at Level 1, going to Level 3 today'", "5"],
        ["3", "What is AI Really?", "Pizza analogy — AI vs ML vs LLM vs ChatGPT. Myths busted.", "8"],
        ["4", "How LLMs Work", "WhatsApp keyboard analogy — 'autocomplete on steroids'", "8"],
        ["5", "API Key Setup", "Guided setup with 'What is an API key?' explanation", "8"],
        ["6", "Demo 1: Roast My Insta Bio", "AI roasts bios in 4 styles (incl. Indian Aunty mode)", "10"],
        ["7", "Prompt Engineering 101", "5 rules: Role, Specificity, Structure, Examples, Iterate", "10"],
        ["8", "Activity 1: Prompt Battle", "15-min creative challenge — best/funniest prompt wins", "15"],
    ]
)
spacer()

heading("Mid-Morning Block — Quizzes + RAG", level=2)
add_table(
    ["#", "Slide", "What Happens", "Min"],
    [
        ["9", "Quiz 1: AI Fundamentals", "4 questions on LLMs, prompting, temperature", "5"],
        ["10", "What is RAG?", "Open-book exam analogy. Embeddings explained simply.", "10"],
        ["11", "Demo 2: RAG Pipeline", "Campus FAQ as knowledge base — test + break it", "12"],
    ]
)
spacer()

heading("Afternoon Block — Agents + Building", level=2)
add_table(
    ["#", "Slide", "What Happens", "Min"],
    [
        ["12", "Quiz 2: RAG Basics", "4 questions on RAG, embeddings, vector DBs", "5"],
        ["13", "What are AI Agents?", "Intern vs Employee analogy. 4 parts of an agent.", "8"],
        ["14", "Demo 3: No-Code Agent (n8n)", "Live build — drag-and-drop agent with tools", "15"],
        ["15", "Systems Thinking", "Input → Process → Output framework", "10"],
        ["16", "Activity 2: Build Your Agent", "30 min — teams build agents on n8n + demos", "35"],
        ["17", "Final Quiz", "5 comprehensive questions — 'Am I a CEO?'", "5"],
        ["18", "Workshop Feedback", "Structured form via QR, live count on screen", "5"],
        ["19", "What to Learn Next", "Weekly/monthly/quarterly learning roadmap", "5"],
        ["20", "Quick Links", "All tools, resources, learning paths", "2"],
    ]
)
spacer()

heading("What 2nd Years Build", level=2)
bullet("Creative AI persona via prompt engineering ", bold_prefix="(Prompt Engineering) — ")
bullet("RAG system over campus FAQ / study notes ", bold_prefix="(RAG) — ")
bullet("No-code AI agent on n8n with tools ", bold_prefix="(Final Deliverable) — ")
spacer()

# ---- 6. WORKSHEET MATERIALS ----
heading("6. Worksheet Materials", level=1)

heading("3rd Year Worksheets", level=2)
add_table(
    ["Worksheet", "Focus Area", "Format"],
    [
        ["Worksheet 1: The Prompt Lab", "Prompt engineering challenges, system prompt design", "PDF"],
        ["Worksheet 2: Build and Break", "RAG pipeline building, testing edge cases", "PDF"],
        ["Worksheet 3: Agent Architect", "Custom tool design, agent planning, deployment", "PDF"],
    ]
)
spacer()

heading("2nd Year Worksheets", level=2)
add_table(
    ["Worksheet", "Focus Area", "Format"],
    [
        ["Worksheet 1: The Prompt Lab", "AI concepts fill-in-the-blank, prompt makeover challenge, system prompt design", "PDF + MD"],
        ["Worksheet 2: RAG Explorer", "RAG concepts, design a 10-chunk knowledge base, test & break the RAG", "PDF + MD"],
        ["Worksheet 3: Agent Builder", "Agent concepts, blueprint planning, n8n build checklist, demo preparation", "PDF + MD"],
    ]
)
spacer()

heading("Design Principles", level=2)
bullet("Self-paced — ", bold_prefix="")
doc.paragraphs[-1].runs[0].text = ""
r = doc.paragraphs[-1].add_run("Self-paced")
r.bold = True
doc.paragraphs[-1].add_run(" — students can work through even if they fall behind the live session")

bullet("Scaffolded — ", bold_prefix="")
doc.paragraphs[-1].runs[0].text = ""
r = doc.paragraphs[-1].add_run("Scaffolded")
r.bold = True
doc.paragraphs[-1].add_run(" — Part A = concepts, Part B = guided practice, Part C = free building")

bullet("Self-check — ", bold_prefix="")
doc.paragraphs[-1].runs[0].text = ""
r = doc.paragraphs[-1].add_run("Self-check")
r.bold = True
doc.paragraphs[-1].add_run(" — every worksheet ends with a checklist so students know if they're ready")

bullet("Practical — ", bold_prefix="")
doc.paragraphs[-1].runs[0].text = ""
r = doc.paragraphs[-1].add_run("Practical")
r.bold = True
doc.paragraphs[-1].add_run(" — every exercise produces something real (a prompt, a knowledge base, an agent)")
spacer()

# ---- 7. FEEDBACK COLLECTION ----
heading("7. Feedback Collection", level=1)

heading("Method", level=2)
para("Feedback is collected via a structured digital form that students access by scanning a QR code displayed on the presentation slide. Responses are stored in a shared PostgreSQL database. The presenter sees a live response count and average ratings on screen.")

heading("Feedback Form Questions", level=2)
add_table(
    ["#", "Question", "Response Type"],
    [
        ["1", "How would you rate the overall day?", "Rating: 1 (Poor) → 4 (Excellent)"],
        ["2", "How relevant was the workshop content to your learning needs?", "Rating: 1 → 4"],
        ["3", "How effectively were the concepts explained?", "Rating: 1 → 4"],
        ["4", "How would you rate the practical sessions / hands-on activities?", "Rating: 1 → 4"],
        ["5", "Did the workshop meet your expectations?", "Yes / Partially / No"],
        ["6", "Did you gain new knowledge or practical skills?", "Yes / No"],
        ["7", "What was the most useful aspect of the workshop?", "Open text"],
        ["8", "Submit your GitHub Repository / Google Colab link", "URL"],
        ["9", "Any additional comments or suggestions?", "Open text"],
        ["10", "Email address", "Email (required)"],
    ]
)
spacer()

heading("What the Presenter Sees (Live Dashboard)", level=2)
bullet("Total response count (large green number)")
bullet("Average ratings for: Overall, Relevance, Clarity, Hands-on (out of 4)")
bullet("Percentage who said 'Yes' to meeting expectations")
bullet("Percentage who said 'Yes' to gaining new skills")
bullet("Number of GitHub/Colab links submitted")

heading("Data Separation", level=2)
bullet("3rd Year responses → stored in feedback_3rdyear table")
bullet("2nd Year responses → stored in feedback_2ndyear table (separate Streamlit form app)")
bullet("No cross-contamination between batches")
spacer()

# ---- 8. LEARNING OUTCOMES ----
heading("8. Learning Outcomes", level=1)

heading("2nd Year (Beginner Track)", level=2)
for outcome in [
    "Explain what AI/LLMs actually are — not magic, but pattern matching on training data",
    "Write effective prompts using the 5 rules (Role, Specificity, Structure, Examples, Iterate)",
    "Explain what RAG is and why it matters (open-book exam analogy)",
    "Build a RAG knowledge base and test it with questions",
    "Explain the difference between a chatbot and an AI agent",
    "Build a working AI agent on n8n (no code) with tools and a system prompt",
    "Apply systems thinking (Input → Process → Output) to AI problems",
]:
    bullet(outcome)

heading("3rd Year (Advanced Track)", level=2)
for outcome in [
    "Use the Groq API to build AI-powered applications in Python",
    "Implement prompt engineering patterns (system prompts, temperature, structured output)",
    "Build a complete RAG pipeline with ChromaDB (embed → store → retrieve → generate)",
    "Understand embeddings and semantic similarity",
    "Build an AI agent with custom tools (calculator, web search, custom functions)",
    "Understand the agent loop pattern (ask → tool → result → repeat)",
    "Deploy an AI agent as a web app with a public URL (Gradio + Google Colab)",
    "Build no-code agents on Dify.ai for rapid prototyping",
]:
    bullet(outcome)
spacer()

# ---- 9. TOOLS & PLATFORMS ----
heading("9. Tools & Platforms Used", level=1)
add_table(
    ["Tool", "Purpose", "Cost"],
    [
        ["Groq (console.groq.com)", "LLM API provider — fast inference", "Free (30 req/min)"],
        ["Google Colab", "Cloud Python notebooks", "Free"],
        ["ChromaDB", "Vector database for RAG", "Free (open source)"],
        ["n8n (app.n8n.cloud)", "No-code agent builder (2nd year)", "Free tier"],
        ["Dify.ai (cloud.dify.ai)", "No-code agent builder (3rd year)", "Free tier"],
        ["Gradio", "AI app deployment with public URL", "Free"],
        ["DuckDuckGo Search", "Web search API (no key needed)", "Free"],
        ["Streamlit", "Slide deck + feedback dashboard", "Free"],
        ["Render", "Cloud hosting for all services", "Free tier"],
        ["PostgreSQL", "Feedback data storage", "Free (Render)"],
    ]
)
spacer()

# ---- FOOTER ----
doc.add_page_break()
spacer()
para("— End of Document —", size=11, color=RGBColor(0x99, 0x99, 0x99), align=WD_ALIGN_PARAGRAPH.CENTER)
para("All links are live and deployed. For questions, contact Dharini Srinivasan.", size=10, color=RGBColor(0x99, 0x99, 0x99), align=WD_ALIGN_PARAGRAPH.CENTER)

# ---- SAVE ----
doc.save("WORKSHOP_BRIEFING.docx")
print("✅ Generated WORKSHOP_BRIEFING.docx")
