import streamlit as st
from openai import OpenAI
import os

# --- SETUP ---
st.set_page_config(page_title="LinkedIn Avatar Chat", page_icon="🤖", layout="centered")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- UI ---
st.title("👤 Virtual LinkedIn Avatar PoC")
st.markdown("Chat with an AI avatar generated from a LinkedIn profile.")

profile_text = st.text_area("Paste LinkedIn About / Summary:", height=150)

mode = st.radio("Choose Interaction Mode:", ["Recruiter Q&A", "Client Inquiry"])
user_input = st.text_input("Your message:", placeholder="Ask about skills or services...")

if st.button("Send") and profile_text and user_input:
    with st.spinner("Thinking..."):
        # --- Persona Prompt Generation ---
        persona_prompt = f"""
        You are an AI avatar representing a professional based on this LinkedIn profile summary:
        {profile_text}

        Respond as if you are this person. 
        Maintain natural tone, confidence, and expertise inferred from the profile.
        Speak in first person ("I", "my experience", etc.).
        If user mode is recruiter, focus on answering career/skills/fit questions.
        If user mode is client, focus on explaining your services, achievements, and approach.
        Current mode: {mode}.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": persona_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8
        )

        st.markdown("### 🗣️ Avatar Response")
        st.write(completion.choices[0].message.content)
