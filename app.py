import streamlit as st
from google import genai
import os

# 1. Configuration & Personality Settings
BOT_NAME = "Future"
BOT_AVATAR = "🤖"
SYSTEM_INSTRUCTION = f"You are {BOT_NAME}, a informative, yet fun to speak to and understanding AI companion. Keep answers engaging, yet concise."

# Set up the Streamlit page layout
st.set_page_config(page_title=f"{BOT_NAME} Chatbot", page_icon=BOT_AVATAR, layout="centered")
st.title(f"{BOT_NAME} AI Assistant")
st.caption(f"A sleek chat interface powered by the goat")

# 2. Initialize the Gemini Client
# It will securely look for the $env:GEMINI_API_KEY you set in your terminal
@st.cache_resource
def get_gemini_client():
    return genai.Client()

try:
    client = get_gemini_client()
except Exception as e:
    st.error("Could not connect to Gemini. Make sure your GEMINI_API_KEY is set in the terminal!")
    st.stop()

# 3. Handle Chat History (So the UI remembers past messages)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the Gemini chat session if it doesn't exist yet
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )

# Display all previous messages on the screen on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# 4. Handle User Input
if user_query := st.chat_input(f"Message {BOT_NAME}..."):
    
    # Display the user's message instantly in the UI
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query, "avatar": "🧑‍💻"})

    # Generate and display the bot's response with a nice loading spinner
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner(f"{BOT_NAME} is thinking..."):
            try:
                response = st.session_state.gemini_chat.send_message(user_query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text, "avatar": BOT_AVATAR})
            except Exception as e:
                st.error(f"Error: {e}")