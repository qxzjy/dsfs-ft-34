import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

st.set_page_config(page_title="My wannabe bot")
st.title("My wannabe bot 🤖")

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

model = ChatMistralAI(model="mistral-small-2402")

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)
            
question = st.chat_input("Type your message here...")

if question:
    st.session_state.chat_history.append(HumanMessage(question))

    with st.chat_message("User"):
        st.markdown(question)

    with st.chat_message("AI"): # Using AI here adds an incon 
        ai_response = model.invoke(question).content
        st.markdown(model.invoke(question).content)

    st.session_state.chat_history.append(AIMessage(ai_response))