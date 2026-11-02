 when trying to create a agent # SPEAKER SCRIPT — CEO of Superintelligence Workshop

Use this alongside the slide deck. Each section maps to a slide.
Show the slide first, then talk using this script.

---

## SLIDE 1: Title

Welcome everyone. Before I even introduce myself, I want to show you something.

But first -- a question. How many of you have used ChatGPT? Raise your hands.
Good. Now -- how many of you have BUILT something with AI? Not used. BUILT.

That's what today is about. By 3 PM, every single one of you will have built and deployed your own AI agent. Not used one. Built one. Let's go.

---

## SLIDE 2: The 5 Levels

Here's how I think about AI skills. There are 5 levels.

- **Level 1** -- you type "Hey ChatGPT, write me an essay." That's consumption.
- **Level 2** -- you learn prompting. "Think step by step. Act as a senior engineer."
- **Level 3** -- you feed it YOUR data. Your notes, your documents.
- **Level 4** -- you give it TOOLS. Web search, calculators, APIs. It decides when to use what. That's an agent.
- **Level 5** -- you orchestrate multiple agents. You're the CEO.

Most people in this room are at Level 1 or 2. By the end of today, you'll be at Level 4. Ready?

---

## SLIDE 3: Setup

Before we do anything, everyone needs an API key. This is your access pass to the AI.

Go to console.groq.com. Sign up with Google. Click API Keys. Create one. Paste it here.

This is free. Groq gives you 30 requests per minute on the free tier. That's more than enough for today.

Raise your hand when you see "Connected!" -- I'll wait for everyone.

---

## SLIDE 4: Demo 1 — Roast My Resume

Before I introduce myself -- watch this.

I have a resume here. A pretty typical 2nd year resume. 17 skills listed, 3 beginner projects, no experience. Sound familiar?

Let me run it through an AI with a single prompt. Watch.

**[Click ROAST IT]**

**[Wait for output, read the highlights aloud, let the room react]**

That was 10 lines of code. A good prompt plus one API call. Level 2 stuff.

But here's the thing -- it can't search the internet. It can't check what companies actually want right now. For that, you need an AGENT. That's Level 4. That's what we're building today.

---

## SLIDE 5: Demo 1 — Code Behind

Here's the actual code. Let's walk through it.

- Line 1 -- import the library.
- Line 3 -- connect to Groq with your API key.
- The magic is in the messages. There are two roles: **system** and **user**.
- System is the personality -- "you are a brutally honest recruiter."
- User is the input -- the resume.
- Temperature 0.85 means it's creative. Set it to 0.1 for factual answers.

That's it. That's the entire program. Want to try it yourself? Follow the steps at the bottom.

---

## SLIDE 6: Demo 2 — Level 1 vs Level 4

Same question. Same AI model. Watch the difference.

**[Click "Run Level 1"]**

Look. Generic advice. Could be from 2 years ago. "Both are great, it depends." Thanks for nothing.

Now watch Level 4.

**[Click "Run Level 4"]**

See the steps? It's SEARCHING the actual job market right now. Finding real salary data. Then it analyzes everything together.

The answer is specific, data-backed, with a 3-month plan.

Same question. Same model. The difference? ORCHESTRATION. Searching, retrieving, reasoning. That's what a CEO does -- they don't do the work, they coordinate the team.

---

## SLIDE 7: Demo 2 — Code Behind

Two steps. That's it.

- Step 1 -- search the web with DuckDuckGo. Free, no API key needed.
- Step 2 -- take that real data and feed it into the LLM as context.

The LLM doesn't know today's job market. But we GAVE it today's job market. This pattern -- search then reason -- is the foundation of every AI agent.

---

## SLIDE 8: Demo 3 — Embeddings

Every sentence becomes 384 numbers. Like GPS coordinates, but for MEANING. Similar meanings get nearby coordinates. Watch.

**[Click the button]**

Look at the scores.

- "I love Python" and "Python coding is my passion" -- 0.92. Almost identical!
- "Python" and "my cat is sleeping" -- 0.08. The computer KNOWS these have nothing in common.

No rules. No keywords. Pure meaning. This is how Google search actually works. And this is the foundation of RAG, which we'll build next.

---

## SLIDE 9: Demo 3 — Code Behind

*(Walk through the code on screen. Point out: model.encode() converts text to numbers. cosine_similarity measures how close two vectors are. That's the entire concept.)*

---

## SLIDE 10: Quiz 1 — Agents Basics

Alright, quick knowledge check. No pressure. Let's see what stuck.

**[Run the quiz, read questions aloud, give 30 seconds per question]**

**[After checking]** Nice! If you got 3/3, you're already thinking like an agent builder.

---

## SLIDE 11: Demo 4 — RAG Pipeline

What if your AI could read YOUR notes and answer from them? Not the internet. Not ChatGPT's generic training. YOUR data.

**[Load the notes into vector DB]**

Now ask it a question.

**[Ask "When should I use a stack vs a queue?"]**

See the pipeline? Step 1: embed the question. Step 2: search the vector DB for matching notes. Step 3: send those notes plus the question to the LLM.

Now let's try to break it. Ask about Instagram's algorithm. It's not in the notes.

**[Run the trick question]**

See? It says "not in your notes." No hallucination. It KNOWS what it doesn't know. That's RAG.

---

## SLIDE 12: Demo 4 — Code Behind

*(Walk through the 4 steps in the code: create DB, add documents, query by meaning, generate answer. Emphasize that ChromaDB handles embeddings automatically.)*

---

## SLIDE 13: Demo 5 — No-Code Agent (Dify.ai)

I'm going to build a fully functional AI agent -- with web search, a knowledge base, and a personality -- without a SINGLE line of code. Watch the clock.

**[Open Dify.ai on screen, follow the checklist steps live]**

**[After publishing and getting the URL]**

4 minutes. No code. Full AI agent with web search and custom knowledge. You could build this during lunch.

But no-code has limits. When you need custom tools, complex logic, or integration with YOUR app -- that's when you need code. Let me show you.

---

## SLIDE 14: Quiz 2 — RAG and Embeddings

Another quick check. This one's about what we just covered.

**[Run quiz]**

---

## SLIDE 15: Activity 1 — Prompt Engineering Challenge

Alright, your turn. 15 minutes. I want you to write the most creative system prompt you can.

Make the AI act as a strict Indian parent reviewing a resume. Or a Silicon Valley VC. Or a drill sergeant. Whatever makes you laugh.

Test it. Iterate. Best result gets shared with the group.

**[Start 15-min timer]**

---

## SLIDE 16: Demo 6 — Code Agent

Same thing as Dify, but now with FULL control. Watch the agent DECIDE which tool to use.

**[Click Run Agent]**

See? I didn't say "use the calculator." It REASONED that 847 times 293 needs math, so it grabbed the calculator. Then it realized it needs current data for AI trends, so it searched the web.

That's autonomy. That's an agent. And you can add ANY tool you want -- weather APIs, databases, file readers, anything.

---

## SLIDE 17: Demo 6 — Code Behind

*(Walk through the agent loop: ask LLM, if ACTION in response, parse tool name, run it, feed result back, repeat. This is the core pattern of EVERY agent framework -- LangChain, CrewAI, AutoGen -- they all do this loop.)*

---

## SLIDE 18: Demo 7 — Gradio Deploy

### What Are We Building?

Okay, so we built an agent in the last demo. It can search the web, do math, reason about problems. But right now, it only runs in a code cell. Only YOU can use it. That's not a product. That's a script.

In this demo, we're turning that agent into a **real, shareable AI product** -- a beautiful chat interface with a public URL that ANYONE can open and use. Your friends, your parents, a recruiter, someone in another country. They type a question, your agent answers. Just like ChatGPT -- except YOU built it.

We're going from "I wrote some code" to "I shipped a product." That's the difference between a student and a builder.

### Why Gradio?

Now, there are many ways to build a UI. You could use React, Flask, Streamlit, HTML/CSS. So why Gradio? Let me explain.

**1. It's built for AI apps.** Gradio was created specifically for machine learning demos. It understands chat interfaces, input/output flows, and AI model patterns natively. You don't need to build a chat UI from scratch -- it already has one.

**2. Minimal code.** Look at this. Three lines:
- `gr.ChatInterface(fn=agent)` -- wraps your agent function into a full chat UI with message history, input box, send button, everything.
- `demo.launch(share=True)` -- starts the server AND creates a public tunnel URL.

That's it. No HTML. No CSS. No JavaScript. No routing. No WebSocket setup. Three lines and you have a production-looking chat app.

**3. Instant public sharing.** This is the killer feature. When you pass `share=True`, Gradio creates a secure tunnel through their servers and gives you a URL like `https://abc123.gradio.live`. Anyone in the world can access it. No need to buy a domain, configure a server, set up HTTPS, or deploy to a cloud platform. It just works.

**4. It's the industry standard for AI demos.** Hugging Face -- the largest AI model hub in the world -- uses Gradio for ALL their model demos. Every model you see on huggingface.co/spaces runs on Gradio. When you learn Gradio, you're learning the tool the AI industry actually uses.

**5. Compare the alternatives:**
- **Streamlit** -- great for dashboards, but chat interfaces need workarounds. No built-in public URL sharing.
- **Flask/FastAPI** -- you'd need to write HTML templates, handle WebSockets, build the entire frontend. Days of work.
- **React** -- powerful but massive overkill for a demo. You'd spend more time on the UI than the AI.
- **Gradio** -- purpose-built for exactly this. Chat UI + public URL in 3 lines.

### What the Code Does (Line by Line)

Let me walk through what's actually happening:

- `import gradio as gr` -- import the library.
- `gr.ChatInterface(fn=agent)` -- this takes your `agent()` function and wraps it. Every time a user types a message and hits send, Gradio calls your function with that message. Whatever your function returns becomes the AI's response in the chat. It handles the entire conversation loop, message history display, scrolling, everything.
- `title` and `description` -- the header text on the page.
- `examples` -- clickable example prompts so users know what to ask. Great UX touch.
- `demo.launch(share=True, debug=True)` -- starts a local server on the Colab machine, creates a Gradio tunnel for public access, and prints two URLs: a local one and a public one.

The public URL is what you share. It routes through Gradio's servers to your Colab notebook. As long as your notebook is running, the URL works.

Anyone in the world can use your agent with that link. Your parents, your friends, a recruiter. THAT'S shipping. THAT'S being a CEO.

---

## SLIDE 19: Demo 7 — Colab Instructions

### Why Google Colab?

Now, why are we running this on Google Colab instead of your local machine? This is important to understand.

**Reason 1: Zero setup.** You don't need to install Python, pip, or any libraries on your laptop. Some of you might be on Windows with no Python configured. Some might have version conflicts. Some might not have admin access to install packages. None of that matters with Colab. It gives you a full Python environment in the browser. Open the link, click Run. Done.

**Reason 2: Free compute.** Colab runs on Google's cloud servers. Your laptop doesn't need to do any heavy lifting. Even if you're on a low-spec machine, a Chromebook, or slow college Wi-Fi, it works. The code runs on Google's infrastructure, not yours.

**Reason 3: Instant public URL -- this is the big one.** When you run Gradio locally on your laptop, it starts a server on `localhost:7860`. That's only accessible on YOUR machine. Nobody else can reach it because your laptop is behind a firewall, behind your college network. You'd need port forwarding, ngrok, or a cloud deployment to make it public.

But on Colab, when Gradio runs with `share=True`, it creates a secure tunnel through Gradio's servers and gives you a public URL like `https://abc123.gradio.live`. This URL works for ANYONE -- your friend sitting next to you, your parent at home, someone in another country. No networking setup, no deployment pipeline, no cloud account needed.

**Reason 4: It mirrors real-world AI development.** Most AI engineers prototype on cloud notebooks (Colab, Kaggle, SageMaker) before deploying to production. This workflow -- write code in notebook, test, get a shareable demo -- is exactly how startups and research labs work. You're learning a real workflow, not a toy exercise.

### The Limitations (Be Honest)

- The Gradio public link **expires after 72 hours**. It's for demos, not permanent hosting.
- If you **close the Colab tab** or it times out (after ~30 min idle), the URL stops working.
- For **permanent deployment**, you'd use Hugging Face Spaces (free, built for Gradio), Render, Railway, or AWS.
- But for a workshop, hackathon, quick prototype, or sharing with friends -- **Colab + Gradio is unbeatable.**

### Step-by-Step: Let's Do It Live

**[Open Colab on screen, share screen]**

**Step 1:** Go to `colab.research.google.com`. Click "New Notebook" or upload the notebook file I'll share.

**Step 2:** Run Cell 1 -- this installs three packages:
- `gradio` -- the UI framework we just discussed
- `groq` -- the Python client for the Groq API (our LLM provider)
- `duckduckgo-search` -- free web search, no API key needed

This takes about 15-20 seconds.

**Step 3:** In Cell 2, find the line that says `GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"`. Replace that with the API key you created earlier on `console.groq.com`. Keep the quotes.

**Step 4:** Run Cell 2. This starts the agent and the Gradio interface. Wait about 30 seconds.

**[Wait for the public URL to appear]**

There it is. Look at the output: `Running on public URL: https://something.gradio.live`

That's YOUR URL. Open it on your phone right now.

**[Pull out phone, open the URL, type a question, show the response to the room]**

See? Same agent we built. Beautiful chat UI. Running on Google's servers. Accessible from any device in the world. You just deployed an AI product. In 2 minutes. From a free notebook.

Now everyone -- try it. 5 minutes. Open Colab, follow these 4 steps. Raise your hand when you see a public URL. Share it with the person next to you -- let THEM use YOUR agent.

**[Start 5-min timer. Walk around. Help anyone stuck. Celebrate each working URL.]**

---

## SLIDE 20: Quiz 3 — Building Agents

Quick check before the hands-on labs.

**[Run quiz]**

---

## SLIDE 21: Activity 2 — Build a RAG (25 min)

Your turn to build. Pick a knowledge domain -- your course notes, your club's FAQ, a topic you're studying -- and build a RAG system over it.

The goal: 3 questions it CAN answer, 2 questions it CANNOT. Verify both work correctly.

**[Start 25-min timer]**

---

## SLIDE 22: Activity 3 — Build an Agent (30 min)

Now extend the agent. Add your own custom tool. A GPA calculator, a unit converter, a dictionary, whatever you want.

The magic moment: when you ask a question and the agent DECIDES to use YOUR tool without you telling it to.

**[Start 30-min timer]**

---

## SLIDE 23: Activity 4 — Hackathon (45 min)

Form teams of 2-3. Pick a real problem. Build and deploy a complete agent.

You have 45 minutes. At the end, each team gets 2 minutes to demo.

Judging: Usefulness (40%), Technical depth (30%), Demo quality (30%).

**[Start 45-min timer]**

---

## SLIDE 24: Final Quiz

Last one. This is the big one.

**[Run quiz]**

If you got 3/3, you are officially a CEO of Superintelligence. You walked in as Level 1. You're walking out as Level 4.

---

## SLIDE 25: Quick Links

All the resources you need are here. Bookmark this page.

---

## SLIDE 26: Timer

*(Use this for any activity timing during the workshop.)*

---

## CLOSING (after all slides)

Here's what you built today:
- A resume roaster (Level 2 -- prompting)
- A research agent with web search (Level 4 -- tools)
- An embedding system (Level 3 -- understanding meaning)
- A RAG pipeline (Level 3 -- your own data)
- A no-code agent (Level 4 -- Dify)
- A code agent with custom tools (Level 4 -- full control)
- A deployed app with a public URL (Level 4 -- shipped product)

You walked in as consumers. You're walking out as builders.

The AI isn't going to take your job. But someone who knows how to BUILD with AI? They might.

Be that someone.

Thank you.
