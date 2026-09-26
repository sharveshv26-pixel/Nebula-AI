# 🤖 Nebula-AI (AI/ML Track)

An intelligent, conversational AI platform designed to make early-stage hiring objective, adaptive, and trustworthy. Built explicitly for the Hackathon AI/ML Track (Problem Statement #2).

## 🚀 Key Features Built

- **🧠 Profile-Aware Questioning & Evaluation:** Dynamically initializes interview sessions to test core developer skills and provides a complete markdown Recruiter Evaluation Dashboard with Hiring Metrics at the end of the session.
- **🔄 Conversational & Adaptive Interviewing:** Replicates a real senior interviewer. Instead of static forms, it asks sharp individual questions, probing deeper where candidates exhibit high competence or adjusting dynamically when they encounter issues.
- **🛡️ Interview Integrity Monitoring:** Features an active frontend event guard that monitors tab visibility changes and focus shifts to catch potential cheating or external aid usage, logging data cleanly for recruiter visibility.

## 🛠️ Tech Stack
- **Frontend & Dashboard:** Streamlit (Python)
- **AI Orchestration Engine:** OpenAI GPT-4o-mini API
- **Integrity Guard:** JavaScript Visibility API Integration

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sharveshv26-pixel/Nebula-AI.git
   cd Nebula-AI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variable:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
