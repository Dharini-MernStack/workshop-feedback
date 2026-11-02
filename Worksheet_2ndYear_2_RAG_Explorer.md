# 📝 WORKSHEET 2: RAG EXPLORER
### CEO of Superintelligence Workshop — 2nd Year Edition
**Time: 20 minutes | Individual / Pair Activity**

---

## Part A: Concept Check (5 min)

### 1. RAG stands for: R_____________ A_____________ G_____________

### 2. Match the analogy:

| RAG Concept | Real-Life Analogy |
|-------------|-------------------|
| Storing documents in vector DB | a) Reading the relevant chapter before writing your answer |
| Searching for relevant docs | b) Putting sticky-note bookmarks on important pages |
| Generating answer from context | c) Flipping to the right section of your textbook |

Storing = ___  |  Searching = ___  |  Generating = ___

### 3. Fill in the flow:

```
User asks a question
        ↓
Question is converted to _____________ (numbers that capture meaning)
        ↓
Vector database finds the most _____________ documents
        ↓
Relevant documents + question are sent to the _____________
        ↓
AI answers using ONLY the _____________ provided
```

### 4. What should a good RAG system do when asked about something NOT in its documents?

a) Make up a plausible answer  
b) Search Google instead  
c) Say "I don't have that information"  
d) Crash with an error  

Answer: ___

---

## Part B: Design Your Knowledge Base (7 min)

Pick ONE of these topics (or choose your own):

- [ ] Your college/department FAQ
- [ ] A subject you're studying (DSA, DBMS, OS, etc.)
- [ ] A club or event you're part of
- [ ] Your favorite hobby/sport rules
- [ ] A topic you'd want to quiz yourself on

**Your chosen topic:** _____________________________________________

Now write **10 knowledge chunks** — one clear fact per line. Be specific!

| # | Your Knowledge Chunk |
|---|---------------------|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
| 5 | |
| 6 | |
| 7 | |
| 8 | |
| 9 | |
| 10 | |

**Pro tip:** More specific facts = better retrieval. "Library closes at 10 PM on weekdays and 6 PM on weekends" is better than "Library has hours."

---

## Part C: Test Your RAG (8 min)

Go to the **Demo 2: RAG Pipeline** slide. Paste your knowledge chunks. Load them. Then test:

### 3 Questions it SHOULD answer correctly:

| Question | Did it answer correctly? | What note did it find? |
|----------|------------------------|----------------------|
| 1. | ✅ / ❌ | |
| 2. | ✅ / ❌ | |
| 3. | ✅ / ❌ | |

### 2 Questions it should NOT be able to answer:

| Question | Did it refuse gracefully? | What did it say? |
|----------|--------------------------|-----------------|
| 1. | ✅ / ❌ | |
| 2. | ✅ / ❌ | |

### Tricky Question — Can you make it hallucinate?

> Your tricky question: _____________________________________________

> What happened? _____________________________________________

---

## Part D: Reflection

### Why is RAG better than just copy-pasting everything into ChatGPT?

_____________________________________________________________

_____________________________________________________________

### Name ONE real-world use case where RAG would be useful:

_____________________________________________________________

### What happens if your knowledge chunks are vague or poorly written?

_____________________________________________________________

---

## ✅ Self-Check

Before you move on, can you:
- [ ] Explain RAG in one sentence to a friend?
- [ ] Explain what embeddings do (in simple terms)?
- [ ] Design a knowledge base for any topic?
- [ ] Predict when RAG will fail vs succeed?

**You're ready to build agents! 🚀**
