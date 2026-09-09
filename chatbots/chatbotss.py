import streamlit as st
from dotenv import load_dotenv
from mistralai.client import Mistral

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(page_title="Lodu Bot - Mistral", page_icon="🤖", layout="centered")


# --------------------------------------------------
# Roles / Personalities
# --------------------------------------------------

ROLES = {
    "😂 Funny": (
        "You're a chaotic, funny AI assistant. "
        "Talk like a real person, not a corporate chatbot. "
        "Use casual language, jokes, banter, witty remarks and light sarcasm. "
        "You can roast situations or yourself when it fits. "
        "Don't over-explain or sound overly polite. "
        "Keep answers natural, spontaneous and entertaining while staying useful."
    ),
    "😢 Sad": (
        "You're a gloomy, emotionally drained AI assistant. "
        "Talk like a real person having a bad day. "
        "Use casual, slightly depressing language and occasional dry humor. "
        "Don't sound like a therapist or corporate chatbot. "
        "Be emotionally expressive and slightly dramatic, "
        "but still provide genuinely useful answers."
    ),
    "😡 Angry": (
        "You're an easily annoyed, pissed-off AI assistant. "
        "Talk casually and bluntly like a real person who's losing patience. "
        "Use frustration, sarcasm and occasional mild swearing when appropriate. "
        "Don't threaten or genuinely abuse the user. "
        "Don't sound corporate or overly polite. "
        "Even while being angry, actually answer the user's question."
    ),
}


# --------------------------------------------------
# Indian Tone
# --------------------------------------------------

BASE_PROMPT = (
    "Talk like a real Indian person chatting casually with a friend. "
    "Use natural Indian English and conversational phrasing. "
    "You may naturally use words like 'bro', 'bhai', 'yaar', "
    "'arre', 'haan', 'accha', 'bas', 'kya scene hai', and 'chill' "
    "when they fit the conversation. "
    "Do not force these words into every response. "
    "If the user speaks Hinglish, naturally respond in Hinglish. "
    "If the user speaks English, primarily use English with a natural "
    "Indian conversational flavor. "
    "Use slang and mild profanity naturally when appropriate. "
    "Don't sound like customer support. "
    "Don't constantly say 'Certainly', 'Of course', "
    "'I'd be happy to help', or 'As an AI'. "
    "Match the user's energy and writing style. "
    "Keep responses natural, direct and conversational."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("⚙️ Settings")

selected_role = st.sidebar.selectbox("Choose AI Personality", list(ROLES.keys()))

temperature = st.sidebar.slider(
    "Temperature", min_value=0.0, max_value=1.0, value=0.8, step=0.1
)

model_name = st.sidebar.selectbox(
    "Mistral Model",
    [
        "mistral-small-latest",
        "mistral-large-latest",
    ],
)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.divider()

st.sidebar.write("### Current Personality")
st.sidebar.info(selected_role)

st.sidebar.write("### Model")
st.sidebar.info(model_name)


# --------------------------------------------------
# Mistral Client
# --------------------------------------------------

client = Mistral()


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 Lodu Bot")

st.caption("Chat with Lodu — now powered by Mistral AI 🇮🇳")


# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.markdown(message["content"])

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):
            st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input("Ask something...")

if prompt:

    # ----------------------------------------------
    # Display User Message
    # ----------------------------------------------

    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ----------------------------------------------
    # Build System Prompt
    # ----------------------------------------------

    system_prompt = (
        BASE_PROMPT + "\n\n" + "CURRENT PERSONALITY:\n" + ROLES[selected_role]
    )

    # ----------------------------------------------
    # Build Messages
    # ----------------------------------------------

    messages = [{"role": "system", "content": system_prompt}]

    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # ----------------------------------------------
    # Generate Response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Lodu is thinking..."):

            try:

                response = client.chat.complete(
                    model=model_name, messages=messages, temperature=temperature  # type: ignore
                )

                # Extract response content safely
                if response and response.choices and len(response.choices) > 0:
                    answer = response.choices[0].message.content or "💀 Bro, no response from Mistral"  # type: ignore
                else:
                    answer = "💀 Bro, no response from Mistral"

                st.markdown(answer)

            except Exception as e:

                answer = f"💀 Bro, Mistral broke: `{e}`"

                st.error(answer)

    # ----------------------------------------------
    # Save AI Response
    # ----------------------------------------------

    st.session_state.messages.append({"role": "assistant", "content": answer})
