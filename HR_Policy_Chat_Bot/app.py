import streamlit as st
from backend import HRBotBackend

st.set_page_config(page_title="HR Policy Bot", page_icon="🤖")

# Initialize Backend once using session state
if "bot" not in st.session_state:
    with st.spinner("Loading Please wait..."):
        st.session_state.bot = HRBotBackend()
        st.session_state.bot.prepare_database()
    st.session_state.messages = []

st.title("🏢 HR Policy Assistant")
st.markdown("Ask me anything about company policies, leave, or benefits.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How many annual leaves do I have?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and show assistant response
    with st.chat_message("assistant"):
        response = st.session_state.bot.ask(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})