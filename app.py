# Actually this is the frontend of the log Analyzer, build in using Streamlit

import streamlit as st
from agent import run_agent


#------------------------------- page setup ------------------------------------------
st.set_page_config(page_title="Network Log Agent", page_icon="📡")
st.title("🤖 Network Log Analyzer Agent 🤖")
st.sidebar.markdown("**Try:**\n- What's the problem in Network?\n- Tell me the status of router-delhi-01\n- optical-mumbai-02 me kya issue hai?") #you can talk in Hindi as well


# ------------------------------Chat Show-Up and Session Talk--------------------------------

# Streamlit reruns the Python script whenever a user interacts with the application.
# If we store chat history in a normal Python variable, its data may reset during a rerun.
# st.session_state stores data that remains available across reruns within the same user's Streamlit session

if "chat" not in st.session_state: #Checks whether a variable named "chat" already exists in st.session_state.
    # If not then make an enpty list [] to store one streamlit session chat
    st.session_state.chat = []

# This loop is useful to show the previous chats on the screen
# m = {
#     "role": "user",
#     "content": "Tell me the status of router-delhi-01"
# }

# role="user": User message.
# role="assistant" : AI response.
# .write(): display the message content

for m in st.session_state.chat:
    st.chat_message(m["role"]).write(m["content"])


# -------------------------------------------------------------------------------------------
# st.chat_input(): This creates an input box at the bottom of the chat interface where the user can type their question.
# := Walrus operator;  It assigns the value and immediately returns it

if q := st.chat_input("Ask About Network?..."):
    st.chat_message("user").write(q) # to display user query message

    with st.spinner("Agent Thinking..."): # when agent is thingking at that time spinner displays the loading message i.e. "Agent Thinking"
        ans, trace = run_agent(q, history=st.session_state.chat) # q: current question, history: previous conversation

    # agent final answer
    with st.chat_message("assistant"): # assistant chat section
        for name, args, res in trace:   # tool name, the arguments given to tools, result of tool
            with st.expander(f"🔧 Tool: {name}({args})"): #expandable section for user to see the result by expanding the chat section
                st.json(res)
        st.write(ans) # agent final answer

    st.session_state.chat += [{"role": "user", "content": q}, {"role": "assistant", "content": ans}] #now add the conversation into chat history
