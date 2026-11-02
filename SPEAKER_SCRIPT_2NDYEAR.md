# SPEAKER SCRIPT — CEO of Superintelligence Workshop (2nd Year Edition)

Use this alongside `app_2ndyear.py`. Each section maps to a slide.
Show the slide first, then talk using this script.
Tone: Friendly, encouraging, lots of analogies. They're beginners — don't assume prior knowledge.

---

## SLIDE 1: Title

Hey everyone! Welcome. Quick question before we start — how many of you have used ChatGPT or Gemini? Raise your hands.

Cool, almost everyone. Now — how many of you actually understand HOW it works? Like, what's happening behind the scenes?

That's okay. Most people don't. And that's exactly what today is about.

By the end of today, you won't just USE AI — you'll understand it, control it, and even build your own AI assistant. Without writing much code. Let's go.

---

## SLIDE 2: The 5 Levels

So here's how I think about AI skills. There are 5 levels.

- **Level 1** — you open ChatGPT and say "write me an essay." That's just consuming. Like watching YouTube vs making YouTube.
- **Level 2** — you learn how to TALK to AI properly. "Think step by step. Act as a senior engineer." This is called prompt engineering. Same AI, way better results.
- **Level 3** — you feed AI YOUR data. Your college notes, your club FAQ. Now it can answer questions about YOUR stuff, not just generic internet stuff.
- **Level 4** — you give AI TOOLS. Web search, calculators, APIs. It decides when to use what. That's an agent.
- **Level 5** — you orchestrate multiple agents. You're the CEO.

Most of you are at Level 1. And that's totally fine! Today, we're going from Level 1 to Level 3, and we'll peek at Level 4. That's a huge jump in one day.

---

## SLIDE 3: What is AI Really?

Before we touch any tools, let's clear up some myths. Because Bollywood and Twitter have... creative interpretations of AI.

**[Show the pizza analogy on screen]**

AI is NOT Terminator. It's not conscious. It's not plotting against humanity. It's basically... really really good autocomplete.

You know how your phone keyboard predicts the next word? "I am going to the..." and it suggests "store" or "gym"? 

ChatGPT does the EXACT same thing. But it's been trained on basically the entire internet — trillions of words. So its predictions are insanely good. It LOOKS like intelligence, but it's really just very sophisticated pattern matching.

This matters because — if you understand that it's predicting words, you'll understand WHY your prompt matters so much. Garbage in, garbage out. Good prompt in, magic out.

---

## SLIDE 4: How LLMs Work

**[Point to the 3 ingredients on screen]**

Three things make an LLM work:

1. **Training data** — books, websites, Wikipedia, code, forums. This is why it "knows" things about history, Python, and cooking. It READ all of it.

2. **The model** — billions of numbers (parameters) that capture patterns. When you hear "GPT-4 has 1.8 trillion parameters" — that's 1.8 trillion numbers that represent patterns in language.

3. **Your prompt** — this is YOUR superpower. The training data and model are fixed. You can't change them. But you CAN control what you ask and HOW you ask it.

Here's the important part: **the AI was trained in the past.** It does NOT know what happened yesterday. It does NOT know your college's exam schedule. It does NOT know your personal notes.

That's the problem we'll solve later today with something called RAG. But first — let's get set up and have some fun.

---

## SLIDE 5: Setup

Alright, everyone needs an API key. Think of it like a password to use AI in your own tools.

**What's Groq?** It's a company that gives you access to powerful AI models for free. Free tier, 30 requests per minute. More than enough for today.

Follow the steps on screen. Should take about 2 minutes.

**[Walk through: console.groq.com → Sign up → API Keys → Create → Copy → Paste]**

Raise your hand when you see "Hello, future CEO!" — I'll wait for everyone.

**[Wait. Help anyone stuck. This is critical — nobody moves forward without a working key.]**

---

## SLIDE 6: Demo 1 — Roast My Insta Bio

Okay, first demo. And I promise this will make you laugh.

How many of you have an Instagram bio? Okay, keep that in mind.

I've got a very... typical... college student bio here. Let me read it. "Coder, Dreamer, Hustler." "Founder @ nothing yet." Sound familiar? We've all seen these.

Let's see what AI thinks of it.

**[Select "Indian Aunty" mode for maximum laughs]**

**[Click ROAST IT]**

**[Wait for output. Read the highlights aloud. Let the room react and laugh.]**

Now watch — I'm going to change ONE thing. Same bio. But I'll switch to "Savage" mode.

**[Switch mode, click ROAST IT again]**

Completely different response! Same bio, same AI model. The ONLY thing that changed was the **system prompt** — the personality we gave the AI.

That's prompt engineering. That's Level 2. And you just saw it in action.

**[Click the "How does this work?" expander and briefly explain system vs user message and temperature]**

---

## SLIDE 7: Prompt Engineering 101

Okay, so you just saw how powerful a good prompt is. Let's learn the rules.

**[Walk through the 5 rules on screen]**

The biggest mistake people make? They type "explain arrays" and get a boring, generic response. Then they say "AI is useless."

No. YOU were useless at prompting. The AI is only as good as your instructions.

**Rule 1: Give it a role.** "You are a patient CS professor teaching a beginner" — instantly better.

**Rule 2: Be specific.** Don't say "write code." Say "write a Python function that takes a list of numbers and returns the top 3 largest. Include comments."

**Rule 3: Give structure.** Tell it the FORMAT you want. "Explain in: Definition, Analogy, Example."

**Rule 4: Give examples.** Show it what good output looks like.

**Rule 5: Iterate!** Your first prompt is almost never your best. Read the output. Refine. Try again.

And the bonus trick — add "Think step by step" to ANY prompt. Forces the AI to reason instead of jumping to answers. Try it, it's like magic.

---

## SLIDE 8: Activity 1 — Prompt Battle

Okay, your turn! 15 minutes. I want you to write the most creative, funniest system prompt you can.

Ideas: Strict Indian parent reviewing your bio. Virat Kohli giving a pep talk. A dramatic Bollywood narrator. A disappointed Sharma ji ka beta. Whatever makes you laugh!

Test it. Iterate. Make it better. We'll share the best ones with the group.

**[Start 15-min timer. Walk around. Encourage creativity. Hype up good ones.]**

**[After timer: Ask 2-3 volunteers to share their prompts and outputs. Celebrate creativity.]**

The point of this exercise: you now FEEL the difference between a lazy prompt and a crafted one. That intuition is worth gold.

---

## SLIDE 9: ⚡ Feedback 1

Quick check-in! Scan the QR code and tell me how it's going. Takes 10 seconds.

**[Show QR code. Wait 60-90 seconds. Click refresh to show count going up.]**

---

## SLIDE 10: Quiz 1 — AI Fundamentals

Let's see what stuck. Quick quiz — no pressure, this isn't graded!

**[Run through questions. Give 20-30 seconds per question.]**

**[After checking answers]** 

If you got 4/4 — amazing, you actually understand how AI works now. That puts you ahead of 90% of people who use ChatGPT daily without knowing any of this.

---

## SLIDE 11: What is RAG?

Okay, here's the big concept for today. RAG. Retrieval Augmented Generation.

Sounds fancy. It's not. Let me explain with an analogy.

**Closed-book exam** — you can only use what you memorized. If you didn't study chapter 7, you can't answer questions about it. You might even make stuff up to fill the page. That's ChatGPT without RAG. It can only use what it memorized during training.

**Open-book exam** — before answering, you flip to the relevant chapter, read it, THEN answer. Way more accurate. That's RAG.

**[Point to the 3 steps on screen]**

Step 1: Store your documents in a smart database. 
Step 2: When someone asks a question, find the most relevant documents.
Step 3: Give those documents to the AI and say "answer from THIS."

The key insight: the AI now answers from YOUR data, not its general training. So it can answer "What time does the SRM AP library close?" — because you GAVE it that info.

And — this is important — if you ask something that's NOT in the documents, a good RAG system says "I don't have that information" instead of making stuff up. That's called avoiding hallucination.

**[Briefly explain embeddings using the concept card on screen — "similar text gets similar numbers"]**

---

## SLIDE 12: Demo 2 — RAG Pipeline

Let's see this in action. I've got some campus facts here as our "knowledge base."

**[Click "Load Notes into Smart Database"]**

Done. 10 facts are now in our vector database. Now watch.

**[Ask: "What time does the library close?"]**

See the pipeline? Step 1: it searched the database for notes about the library. Step 2: it found the right note. Step 3: it answered using that note. "10 PM on weekdays." Correct!

Now let's try to break it.

**[Switch to the right column. Ask: "What's the Instagram password for the college page?"]**

Look — "That's not in your notes!" Perfect. It didn't make something up. It honestly said it doesn't know. THAT'S the power of RAG.

**[Click the "What just happened?" expander for the simple explanation]**

Imagine this with YOUR actual study notes. Upload your DSA notes, your DBMS notes, your entire syllabus. Then just ASK it questions before exams. And it only answers from YOUR notes — not random internet stuff.

That's Level 3. You just saw it.

---

## SLIDE 13: ⚡ Feedback 2

Midway check! How are we doing? Scan again.

**[QR code. Wait. Refresh.]**

---

## SLIDE 14: Quiz 2 — RAG Basics

Quick quiz on RAG. Let's lock this in.

**[Run quiz. 20-30 seconds per question.]**

If you got 4/4 — you understand RAG better than most CS graduates. No joke. This is cutting-edge stuff that companies are hiring for RIGHT NOW.

---

## SLIDE 15: What are AI Agents?

Okay, final big concept. AI Agents.

**[Point to the intern vs employee analogy on screen]**

A chatbot is like an intern. You ask, they answer. One thing at a time. They don't take initiative.

An agent is like a smart employee. You say "find me the best laptop under 50k" and they:
1. Search online for reviews
2. Compare specs
3. Check prices on Amazon and Flipkart
4. Give you a recommendation with links

They DECIDED which steps to take. They used TOOLS (search, comparison). They completed a GOAL, not just answered a question.

**[Point to the 4 parts on screen]**

Every agent has 4 parts:
- **Brain** — the LLM (GPT, Gemini, Llama, etc.)
- **Memory** — RAG, which we just learned!
- **Tools** — web search, calculator, APIs
- **Orchestrator** — the logic that decides what to do when

And here's the exciting part — you're about to BUILD one. Without writing a single line of code.

---

## SLIDE 16: Demo 3 — No-Code Agent (n8n)

This is n8n. Think of it as LEGO blocks for AI. Each block does one thing — you snap them together to build an agent.

**[Open n8n on screen. Share screen.]**

**[Follow the checklist steps live. Go slow. Let students follow along on their own laptops.]**

Step 1: Sign up. Step 2: New workflow. Step 3: Chat Trigger — this is where messages come in.

Now the magic — Step 4: AI Agent node. This is the brain. Connect it to the trigger.

Step 5: Add your Groq API key. Step 6: Paste the system prompt. Step 7: Add Wikipedia and a search tool.

**[Test it live. Ask a question. Show the workflow lighting up as each step executes.]**

See that? You can WATCH the agent think. The trigger fires, the agent decides to use Wikipedia, it gets the result, then it formulates an answer. You can SEE the entire thought process.

**[Show the final working chat]**

That's a full AI agent. Brain, tools, logic. It decides when to search. It decides what to answer from its own knowledge vs what to look up.

And you built it by dragging and dropping blocks. Zero code.

n8n has 400+ integrations by the way. Google Sheets, Slack, Email, Notion, WhatsApp. You can connect your agent to literally anything.

---

## SLIDE 17: Activity 2 — Build Your Agent

Your turn! Teams of 2-3. 30 minutes. Build an agent on n8n.

Pick one of the ideas on screen — PlacePrep Coach, Study Buddy, Campus Navigator, whatever excites you.

The key: write a GREAT system prompt (use everything you learned in Prompt Engineering 101), add at least one tool, and test with 5 different questions.

Each team gets 2 minutes to demo at the end.

**[Start 30-min timer. Walk around. Help teams. Encourage creativity.]**

**[After timer: Each team demos. Celebrate everyone. Pick a winner based on usefulness, creativity, demo quality.]**

---

## SLIDE 18: ⚡ Feedback 3

Final feedback round! Scan the QR one last time.

**[QR code. Wait. Refresh. Read out any fun comments.]**

---

## SLIDE 19: Final Quiz

Last quiz of the day. This is the comprehensive one.

**[Run quiz. Give a bit more time — 30 seconds per question.]**

**[After checking]**

5/5? You walked in as Level 1 and you're walking out understanding concepts that companies PAY people to know. Be proud of that.

---

## SLIDE 20: What to Learn Next

I don't want today to be a one-time thing. Here's your roadmap.

**[Walk through the timeline on screen]**

**This week:** Practice prompting on ChatGPT/Gemini daily. Build 2 more agents on n8n.

**This month:** Start Python if you haven't. Try the Groq API — it's just 10 lines. Take the free DeepLearning.AI course.

**3 months:** Learn LangChain. Build a RAG system with your own docs. Deploy something on Hugging Face.

**By next year:** You'll have a portfolio of AI projects. You'll be applying for internships with PROOF that you can build.

---

## SLIDE 21: Quick Links

All resources are here. Bookmark this page. Everything you need to keep going.

---

## SLIDE 22: Timer

*(Use for any activity timing during the workshop.)*

---

## CLOSING (after all slides)

Let's recap what you learned today:

- **What AI actually is** — not magic, not Terminator. Pattern matching on steroids.
- **Prompt engineering** — the skill that makes the same AI 10x more useful.
- **RAG** — making AI answer from YOUR data, not random internet stuff.
- **AI Agents** — AI that uses tools and makes decisions on its own.
- **You BUILT one** — on n8n, no code, with web search and a knowledge base.

Here's what I want you to remember:

The people who will succeed in the next 10 years aren't the ones who are scared of AI. And they're not the ones who just USE AI. They're the ones who learn to BUILD with it. To orchestrate it. To be the CEO.

You took your first step today. Don't let it be your last.

Go build something. Go break something. Go show someone what you made.

Thank you. 🚀
