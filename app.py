import streamlit as st
from openai import OpenAI
import os

# --- SETUP ---
st.set_page_config(page_title="LinkedIn Avatar Chat", page_icon="🤖", layout="centered")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- UI ---
st.title("👤 Virtual LinkedIn Avatar PoC")
st.markdown("Chat with an AI avatar generated from a LinkedIn profile.")

profile_text = st.text_area("""Marketing leader with over 10+ years of experience in leading marketing and growth functions, crafting consumer journeys, and optimizing marketing funnels to achieve better ROI. I specialize in digital and performance marketing, brand marketing, and go-to-market strategies across various industries and geographies. 

My expertise stems from my diverse and global perspective, having managed marketing campaigns in B2C EdTech, B2B Fintech, Healthcare, Real Estate, and D2C FMCG sectors. My work has spanned key markets in the US, UK, Canada, UAE, and India. My experience involves managing multi-channel marketing campaigns on platforms like Google/SEM, Facebook, Instagram/paid social/SMM, LinkedIn, and TikTok, SEO. 

As a results-oriented leader, I thrive on leading cross-functional teams and driving them towards shared goals. I am also deeply passionate about leveraging data and emerging technologies to make informed decisions and drive sustainable growth. 

My mission is to create value for customers and stakeholders through innovative and impactful marketing solutions.""", height=150)

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
