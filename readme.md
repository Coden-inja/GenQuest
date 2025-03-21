# AI Powered Exam Question Generator - MVP Approach

## 📌 Project Goal
Build an AI-powered system that generates practice questions from **text or PDFs**, allowing students to:
1. **Upload text/PDF** as input.
2. **Choose question types** (MCQ, fill in the blanks, short, long).
3. **Select difficulty levels** before generation.
4. **Use free APIs & tools** (zero production cost).

---

## 🛠️ Tech Stack & Free Tools

| Component | Tool/Technology | Cost |
|-----------|----------------|------|
| **Frontend** | HTML, CSS, JavaScript | Free |
| **PDF Processing** | [pdf.js](https://mozilla.github.io/pdf.js/) | Free |
| **Question Generation API** | [Hugging Face Models](https://huggingface.co/models) / OpenAI (Free Tier) | Free |
| **Hosting** | [GitHub Pages](https://pages.github.com/) / [Vercel](https://vercel.com/) | Free |
| **Backend (If needed)** | Flask (on **Replit** or **Render.com Free Tier**) | Free |

---

## 🏗️ Technical Flowchart

```plaintext
Start
 │
 ▼
User Inputs Text / Uploads PDF
 │
 ▼
Extract Text (pdf.js or Backend API)
 │
 ▼
User Selects Question Type & Difficulty
 │
 ▼
Send Data to Free AI API (Hugging Face)
 │
 ▼
Receive AI-Generated Questions
 │
 ▼
Display Questions on UI (HTML, JS)
 │
 ▼
Deploy on GitHub Pages / Vercel
 │
 ▼
End



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




curl -X POST "https://api.deepseek.com/v1/chat/completions" \
-H "Authorization: Bearer sk-f9cec80e2c227c127b30c6bf8db385ae0f539ef25d2403047d9ab446448b0fdd" \
-H "Content-Type: application/json" \
-d '{
  "model": "deepseek-chat",
  "messages": [{"role": "user", "content": "Test message"}]
}'


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