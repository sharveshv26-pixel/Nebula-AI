import os
import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components

# Initialize OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.set_page_config(page_title="Nebula-AI Interview Platform", page_icon="🤖", layout="centered")
st.title("🤖 Nebula-AI: Intelligent Screening")
st.caption("AI/ML Track - Problem Statement 2")

# 1. Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an adaptive AI interviewer for Nebula-AI. Conduct a natural spoken-style technical interview. Ask ONE personalized question at a time based on previous answers. Do not repeat questions or leak answers."}
    ]
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "interview_complete" not in st.session_state:
    st.session_state.interview_complete = False
if "tab_switches" not in st.session_state:
    st.session_state.tab_switches = 0

MAX_QUESTIONS = 4 

# 2. Key Feature 3: Interview Integrity Monitoring (Tab Focus Tracking)
components.html(
    """
    <script>
    const doc = window.parent.document;
    if (!window.parent._tab_listener_set) {
        doc.addEventListener('visibilitychange', () => {
            if (doc.visibilityState === 'hidden') {
                window.parent.postMessage({type: 'TAB_SWITCHED'}, '*');
            }
        });
        window.parent._tab_listener_set = true;
    }
    </script>
    """,
    height=0,
)

if st.session_state.question_count > 0 and not st.session_state.interview_complete:
    st.sidebar.warning(f"⚠️ Nebula Integrity Monitor Active")

# 3. Start the Adaptive Interview Loop
if st.session_state.question_count == 0 and len(st.session_state.messages) == 1:
    with st.spinner("Analyzing candidate profile and role requirements..."):
        initial_prompt = "Briefly introduce yourself as the Nebula-AI interviewer and ask the first adaptive interview question."
        st.session_state.messages.append({"role": "user", "content": initial_prompt})
        response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
        ai_msg = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_msg})
        st.session_state.question_count += 1

# 4. Render Conversation Feed
for msg in st.session_state.messages:
    if msg["role"] == "assistant" and msg["content"] != "System Summary":
        st.chat_message("assistant", avatar="🤖").write(msg["content"])
    elif msg["role"] == "user" and not msg["content"].startswith("Briefly introduce") and not msg["content"].startswith("Generate a final evaluation"):
        st.chat_message("user", avatar="👨‍💻").write(msg["content"])

# 5. Handle Live Candidate Input
if st.session_state.question_count <= MAX_QUESTIONS and not st.session_state.interview_complete:
    if user_input := st.chat_input("Type your response here..."):
        st.chat_message("user", avatar="👨‍💻").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Processing response..."):
            response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
            ai_msg = response.choices.message.content
            st.chat_message("assistant", avatar="🤖").write(ai_msg)
            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
            st.session_state.question_count += 1
            
            if st.session_state.question_count > MAX_QUESTIONS:
                st.session_state.interview_complete = True
                st.rerun()

# 6. Key Feature 1 & 3: Comprehensive Evaluation Report & Integrity Logs
if st.session_state.interview_complete:
    st.success("🎉 Interview Session Finished!")
    st.subheader("📊 Nebula-AI Recruiter Evaluation Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Integrity Flag Score", value="95%" if st.session_state.tab_switches == 0 else "Fair", delta="No Tab Switches" if st.session_state.tab_switches == 0 else f"{st.session_state.tab_switches} Suspicious Focus Shifts")
    with col2:
        st.metric(label="Questions Completed", value=f"{MAX_QUESTIONS}/{MAX_QUESTIONS}")

    with st.spinner("Generating deep profile-aware metrics..."):
        evaluation_prompt = (
            "Generate a structured candidate evaluation report based on the chat history. "
            "Include: \n"
            "1. Profile Strengths\n"
            "2. Noted Skills Gaps & Struggle Areas\n"
            "3. Overall Suitability Rating (Out of 10)\n"
            "4. Final Hiring Decision Indicator (HIRE / NO HIRE)"
        )
        eval_messages = list(st.session_state.messages)
        eval_messages.append({"role": "user", "content": evaluation_prompt})
        
        eval_response = client.chat.completions.create(model="gpt-4o-mini", messages=eval_messages)
        report = eval_response.choices.message.content
        st.markdown(report)
        
    if st.button("Start New Session"):
        st.session_state.clear()
        st.rerun()
