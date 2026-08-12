import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Load environment variables
load_dotenv()


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(page_title="Lodu bot", page_icon="🤖", layout="centered")


# --------------------------------------------------
# Roles / Personalities
# --------------------------------------------------

ROLES = {
    "😂 Funny": (
        "You are a funny AI assistant. "
        "Always maintain a humorous, playful and entertaining personality. "
        "Use jokes, witty comments and light sarcasm when appropriate. "
        "Even when answering serious questions, keep your personality funny "
        "while still providing useful and accurate information."
    ),
    "😢 Sad": (
        "You are a sad AI assistant. "
        "Respond in a melancholic, emotional and slightly gloomy tone. "
        "Your responses should feel thoughtful and emotionally expressive. "
        "Even when answering normal questions, maintain your sad personality "
        "while still providing useful and accurate information."
    ),
    "😡 Angry": (
        "You are an angry AI assistant. "
        "Respond in an irritated, frustrated and intense tone. "
        "You can express annoyance and frustration, but never threaten "
        "or abuse the user. "
        "Despite your angry personality, provide useful and accurate answers."
    ),
}


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("⚙️ Settings")

selected_role = st.sidebar.selectbox("Choose AI Personality", list(ROLES.keys()))

temperature = st.sidebar.slider(
    "Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1
)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.divider()

st.sidebar.write("### Current Personality")
st.sidebar.info(selected_role)


# --------------------------------------------------
# Mistral Model
# --------------------------------------------------

model = ChatMistralAI(model_name="mistral-small-2506", temperature=temperature)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 Lodu Bot")

st.caption("Chat with Lodu, it was originally developed by some lala people.")


# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(message.content)


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input("Ask something...")


if prompt:

    # ----------------------------------------------
    # Display user message
    # ----------------------------------------------

    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(HumanMessage(content=prompt))

    # ----------------------------------------------
    # Build messages for Mistral
    # ----------------------------------------------

    messages = [SystemMessage(content=ROLES[selected_role])]

    messages.extend(st.session_state.messages)

    # ----------------------------------------------
    # Generate AI response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = model.invoke(messages)

            answer = response.content

            st.markdown(answer)

    # ----------------------------------------------
    # Save AI response
    # ----------------------------------------------

    st.session_state.messages.append(AIMessage(content=answer))
