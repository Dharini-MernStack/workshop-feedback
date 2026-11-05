# CEO OF SUPERINTELLIGENCE — Workshop Briefing Document

**Prepared by:** Dharini Srinivasan
**Event:** AI Agents Workshop — SRM AP × Kalvium
**Date:** November 2026
**Duration:** Full-day workshop (per batch)
**Batches:** 2nd Year CSE + 3rd Year CSE (separate sessions, tailored content)

---

## 1. LIVE WORKSHOP LINKS

| Resource | Link |
|----------|------|
| **2nd Year Slide Deck** | [workshop-slides-2ndyear.onrender.com](https://workshop-slides-2ndyear.onrender.com) |
| **3rd Year Slide Deck** | [workshop-slides.onrender.com](https://workshop-slides.onrender.com) |
| **2nd Year Feedback Form** | [workshop-feedback-2ndyear.onrender.com](https://workshop-feedback-2ndyear.onrender.com) |
| **Feedback Server (API + Data)** | [workshop-feedback-ismc.onrender.com](https://workshop-feedback-ismc.onrender.com) |

---

## 2. WORKSHOP OVERVIEW

### Theme
**"Become the CEO of Superintelligence"** — a hands-on, zero-to-builder workshop where students go from passively using AI (ChatGPT) to understanding, controlling, and building AI agents.

### Core Message
> *Person at Level 1: "AI will take my job"*
> *Person at Level 5: "I just automated my job and started a side business"*
> **Same AI. Different user. Different outcome.**

### The 5 Levels Framework (used across both batches)

| Level | Role | Skill | What They Say |
|-------|------|-------|---------------|
| 1 | Consumer | Uses ChatGPT | "Hey ChatGPT" |
| 2 | Prompter | Prompt engineering | "Think step by step" |
| 3 | Integrator | Feeds own data (RAG) | "Here's MY data" |
| 4 | Agent Builder | Builds tools + agents | "Use tools, decide" |
| 5 | CEO | Orchestrates agent teams | "Run the company" |

---

## 3. WHAT'S DIFFERENT BETWEEN THE TWO BATCHES

### 3rd Year — Advanced Track (Levels 2 → 4+)
**Assumption:** Students have programming experience, know Python, familiar with APIs.
**Goal:** Build and deploy a fully functional AI agent with code.

### 2nd Year — Beginner Track (Levels 1 → 3, peek at 4)
**Assumption:** Most have only used ChatGPT. Limited coding experience.
**Goal:** Understand how AI works, learn prompt engineering, build a no-code agent.

| Aspect | 3rd Year | 2nd Year |
|--------|----------|----------|
| **Starting Level** | Level 2 | Level 1 |
| **Target Level** | Level 4–5 | Level 3 (peek at 4) |
| **Coding Required** | Yes (Python) | No (n8n no-code) |
| **API Used** | Groq API (code) | Groq API (via n8n) |
| **Agent Building** | Python + LangChain patterns | n8n drag-and-drop |
| **Deployment** | Google Colab + Gradio (public URL) | n8n shareable workflow |
| **Tone** | Fast-paced, technical | Friendly, analogy-heavy, beginner-safe |

---

## 4. SESSION FLOW — 3RD YEAR

**21 slides | ~6 hours | Mix of demos, coding, quizzes, and activities**

### Morning Block (Concepts + Demos)
| # | Slide | What Happens | Time |
|---|-------|-------------|------|
| 1 | **Title** | Opening hook — "How many have BUILT something with AI?" | 3 min |
| 2 | **The 5 Levels** | Framework introduction — where are you today? | 5 min |
| 3 | **API Key Setup** | Everyone gets a Groq API key (free) | 8 min |
| 4 | **Demo 1: Roast My Resume** | Live demo — AI roasts a resume in different styles | 8 min |
| 5 | **Demo 1: Code Behind** | Walk through the 10 lines of code that made it work | 5 min |
| 6 | **Demo 2: Level 1 vs Level 4** | Side-by-side — generic ChatGPT vs agent with web search | 10 min |
| 7 | **Demo 2: Code Behind** | Search → retrieve → reason pattern explained | 5 min |
| 8 | **Demo 3: Embeddings** | Text → numbers → meaning. Similarity scores visualized | 8 min |
| 9 | **Demo 3: Code Behind** | sentence-transformers + cosine similarity | 5 min |
| 10 | **⚡ Feedback Round 1** | QR code scan, quick pulse check | 3 min |
| 11 | **Quiz 1: Agent Basics** | 3 multiple-choice questions | 5 min |

### Midday Block (RAG + No-Code)
| # | Slide | What Happens | Time |
|---|-------|-------------|------|
| 12 | **Demo 4: RAG Pipeline** | Build a working RAG — load notes, ask questions, test failure cases | 12 min |
| 13 | **Demo 4: Code Behind** | ChromaDB + Groq in 30 lines | 5 min |
| 14 | **Demo 5: No-Code Agent (Dify.ai)** | Full agent built live in 4 minutes with zero code | 10 min |
| 15 | **⚡ Feedback Round 2** | Midway pulse check | 3 min |
| 16 | **Quiz 2: RAG & Embeddings** | 4 multiple-choice questions | 5 min |

### Afternoon Block (Hands-on Building)
| # | Slide | What Happens | Time |
|---|-------|-------------|------|
| 17 | **Activity 1: Prompt Engineering** | 15-min challenge — write the best/funniest system prompt | 15 min |
| 18 | **Demo 6: Code Agent** | Agent with calculator + web search — watch it DECIDE which tool | 10 min |
| 19 | **Demo 6: Code Behind** | The agent loop pattern: ask → tool → result → repeat | 5 min |
| 20 | **Demo 7: Gradio Deploy** | Turn the agent into a shareable web app with public URL | 8 min |
| 21 | **Demo 7: Colab Instructions** | Step-by-step Google Colab setup for everyone | 10 min |
| 22 | **⚡ Feedback Round 3** | Final pulse check | 3 min |
| 23 | **Quiz 3: Building Agents** | 3 multiple-choice questions | 5 min |
| 24 | **Activity 2: Build a RAG** | 25 min — RAG over their own study content | 25 min |
| 25 | **Activity 3: Custom Agent Tool** | 30 min — add a custom tool to the agent | 30 min |
| 26 | **Activity 4: Mini Hackathon** | 45 min — teams of 2-3, build + deploy a complete agent | 45 min |
| 27 | **Final Quiz** | 3 comprehensive questions — "Are you a CEO?" | 5 min |
| 28 | **📊 Workshop Feedback** | Structured feedback form via QR — live count on screen | 5 min |
| 29 | **Quick Links** | All resources, tools, and learning paths | 2 min |

### What Students Build (3rd Year)
1. Resume roaster (prompt engineering)
2. Research agent with live web search
3. Embedding similarity system
4. RAG pipeline over custom notes
5. No-code agent on Dify.ai
6. Code agent with custom tools
7. **Deployed Gradio app with public URL** (final deliverable)

---

## 5. SESSION FLOW — 2ND YEAR

**21 slides | ~5 hours | Beginner-friendly, analogy-driven, no-code focus**

### Morning Block (Understanding AI)
| # | Slide | What Happens | Time |
|---|-------|-------------|------|
| 1 | **Title** | Opening — "How many have used ChatGPT? Now, how many understand HOW it works?" | 3 min |
| 2 | **The 5 Levels** | Framework — "You're at Level 1, we're going to Level 3 today" | 5 min |
| 3 | **What is AI Really?** | Pizza analogy — AI vs ML vs DL vs LLM vs ChatGPT. Myth-busting. | 8 min |
| 4 | **How LLMs Work** | WhatsApp keyboard analogy — "It's autocomplete on steroids" | 8 min |
| 5 | **API Key Setup** | Guided setup with "What's an API key?" explanation | 8 min |
| 6 | **Demo 1: Roast My Insta Bio** | Live demo — AI roasts Instagram bios in 4 styles (incl. Indian Aunty mode) | 10 min |
| 7 | **Prompt Engineering 101** | 5 rules: Role, Specificity, Structure, Examples, Iterate | 10 min |
| 8 | **Activity 1: Prompt Battle** | 15-min creative challenge — best/funniest system prompt wins | 15 min |

### Mid-Morning Block (Quizzes + RAG)
| # | Slide | What Happens | Time |
|---|-------|-------------|------|
| 9 | **Quiz 1: AI Fundamentals** | 4 questions on LLMs, prompting, temperature | 5 min |
| 10 | **What is RAG?** | Open-book exam analogy. Embeddings explained simply. | 10 min |
| 11 | **Demo 2: RAG Pipeline** | Campus FAQ as knowledge base — ask questions, try to break it | 12 min |

### Afternoon Block (Agents + Building)
| # | Slide | What Happens | Time |
|---|-------|-------------|------|
| 12 | **Quiz 2: RAG Basics** | 4 questions on RAG, embeddings, vector DBs | 5 min |
| 13 | **What are AI Agents?** | Intern vs Employee analogy. 4 parts of an agent. | 8 min |
| 14 | **Demo 3: No-Code Agent (n8n)** | Live build — drag-and-drop agent with Wikipedia + search | 15 min |
| 15 | **Systems Thinking** | Input → Process → Output framework. Map RAG and agent systems. | 10 min |
| 16 | **Activity 2: Build Your Agent** | 30 min — teams build agents on n8n. 2-min demos at end. | 35 min |
| 17 | **Final Quiz** | 5 comprehensive questions — "Am I a CEO?" | 5 min |
| 18 | **📊 Workshop Feedback** | Structured feedback form via QR — live count on screen | 5 min |
| 19 | **What to Learn Next** | Weekly/monthly/quarterly roadmap for continued learning | 5 min |
| 20 | **Quick Links** | All tools, resources, learning paths | 2 min |

### What Students Build (2nd Year)
1. Creative AI persona via prompt engineering
2. RAG system over campus FAQ / study notes
3. **No-code AI agent on n8n** (final deliverable — drag and drop, with tools)

---

## 6. WORKSHEET MATERIALS

### 3rd Year Worksheets
| Worksheet | Focus | Format |
|-----------|-------|--------|
| **Worksheet 1: The Prompt Lab** | Prompt engineering challenges, system prompt design | PDF |
| **Worksheet 2: Build and Break** | RAG pipeline building, testing edge cases | PDF |
| **Worksheet 3: Agent Architect** | Custom tool design, agent planning, deployment | PDF |

### 2nd Year Worksheets
| Worksheet | Focus | Format |
|-----------|-------|--------|
| **Worksheet 1: The Prompt Lab** | Fill-in-the-blank AI concepts, prompt makeover challenge, system prompt design | PDF + MD |
| **Worksheet 2: RAG Explorer** | RAG concept check, design a knowledge base (10 chunks), test & break the RAG | PDF + MD |
| **Worksheet 3: Agent Builder** | Agent concepts quiz, agent blueprint planning, n8n build checklist, demo prep | PDF + MD |

### Worksheet Design Principles
- **Self-paced** — students can work through even if they fall behind the live session
- **Scaffolded** — Part A = concepts, Part B = guided practice, Part C = free building
- **Self-check** — every worksheet ends with a checklist so students know if they're ready to move on
- **Practical** — every exercise produces something real (a prompt, a knowledge base, an agent)

---

## 7. FEEDBACK COLLECTION

### Structure
Feedback is collected via a **structured digital form** that students access by scanning a QR code displayed on the presentation slide.

### Feedback Form Questions
| # | Question | Type |
|---|----------|------|
| 1 | How would you rate the overall day? | Rating: 1 (Poor) → 4 (Excellent) |
| 2 | How relevant was the workshop content to your learning needs? | Rating: 1 → 4 |
| 3 | How effectively were the concepts explained? | Rating: 1 → 4 |
| 4 | How would you rate the practical sessions / hands-on activities? | Rating: 1 → 4 |
| 5 | Did the workshop meet your expectations? | Yes / Partially / No |
| 6 | Did you gain new knowledge or practical skills from this workshop? | Yes / No |
| 7 | What was the most useful aspect of the workshop? | Open text |
| 8 | Submit your GitHub Repository Link / Google Colab | URL |
| 9 | Any additional comments or suggestions? | Open text |
| 10 | Email address | Email (required) |

### How It Works
1. Presenter shows the **📊 Workshop Feedback** slide (with QR code)
2. Students scan QR → opens a mobile-friendly form on their phones
3. Students fill the structured form and submit
4. Responses are saved to a **shared PostgreSQL database** on Render
5. The slide shows a **live count** of responses + average ratings, refreshable in real-time
6. All data is downloadable as CSV after the workshop

### Data Displayed on Presenter Screen (Count Only)
- Total response count (big green number)
- Average ratings (Overall, Relevance, Clarity, Hands-on) out of 4
- % who said "Yes" to meeting expectations
- % who said "Yes" to gaining new skills
- Number of GitHub/Colab links submitted

### Separate Data Per Batch
- **3rd Year** responses stored in `feedback_3rdyear` table → accessed via `/3rdyear` form
- **2nd Year** responses stored in `feedback_2ndyear` table → accessed via `/2ndyear` form (Streamlit app)
- No cross-contamination between batches

---

## 8. LEARNING OUTCOMES

### By end of workshop, students can:

**2nd Year (Beginner)**
- [ ] Explain what AI/LLMs actually are (not magic — pattern matching on training data)
- [ ] Write effective prompts using the 5 rules (Role, Specificity, Structure, Examples, Iterate)
- [ ] Explain what RAG is and why it matters (open-book exam analogy)
- [ ] Build a RAG knowledge base and test it with questions
- [ ] Explain the difference between a chatbot and an AI agent
- [ ] Build a working AI agent on n8n (no code) with tools and a system prompt
- [ ] Apply systems thinking (Input → Process → Output) to AI problems

**3rd Year (Advanced)**
- [ ] Use the Groq API to build AI-powered applications in Python
- [ ] Implement prompt engineering patterns (system prompts, temperature, structured output)
- [ ] Build a complete RAG pipeline with ChromaDB (embed → store → retrieve → generate)
- [ ] Understand embeddings and semantic similarity
- [ ] Build an AI agent with custom tools (calculator, web search, custom functions)
- [ ] Understand the agent loop pattern (ask → tool → result → repeat)
- [ ] Deploy an AI agent as a web app with a public URL (Gradio + Google Colab)
- [ ] Build no-code agents on Dify.ai for rapid prototyping

---

## 9. TOOLS & PLATFORMS USED

| Tool | Purpose | Cost |
|------|---------|------|
| **Groq** (console.groq.com) | LLM API provider — fast inference | Free tier (30 req/min) |
| **Google Colab** | Cloud Python notebooks for coding exercises | Free |
| **ChromaDB** | Vector database for RAG | Free (open source) |
| **n8n** (app.n8n.cloud) | No-code agent builder (2nd year) | Free tier |
| **Dify.ai** (cloud.dify.ai) | No-code agent builder (3rd year) | Free tier |
| **Gradio** | AI app deployment with public URL | Free |
| **DuckDuckGo Search** | Free web search API (no key needed) | Free |
| **Streamlit** | Workshop slide deck + feedback dashboard | Free |
| **Render** | Cloud hosting for all workshop services | Free tier |
| **PostgreSQL** | Feedback data storage | Free (Render) |

---

## 10. TECHNICAL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    RENDER (Cloud)                         │
│                                                           │
│  ┌──────────────────┐   ┌──────────────────────────┐     │
│  │ workshop-slides   │   │ workshop-slides-2ndyear   │     │
│  │ (Streamlit)       │   │ (Streamlit)               │     │
│  │ 3rd Year Deck     │   │ 2nd Year Deck             │     │
│  └──────────────────┘   └──────────────────────────┘     │
│                                                           │
│  ┌──────────────────────────┐   ┌──────────────────┐     │
│  │ workshop-feedback-2ndyear │   │ workshop-feedback │     │
│  │ (Streamlit Form)          │   │ (Flask API)       │     │
│  │ QR → Students fill here   │   │ Round-based API   │     │
│  └────────────┬─────────────┘   └────────┬─────────┘     │
│               │                           │               │
│               ▼                           ▼               │
│         ┌──────────────────────────────────┐              │
│         │      PostgreSQL Database          │              │
│         │  feedback_2ndyear (table)         │              │
│         │  feedback_3rdyear (table)         │              │
│         │  feedback (rounds table)          │              │
│         └──────────────────────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

**QR Flow:**
Student scans QR → Opens feedback form (Streamlit app) → Submits → Saved to PostgreSQL → Presenter refreshes slide → Count updates live

---

*Document generated for internal review. All links are live and deployed.*
