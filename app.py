import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Network Log Agent", page_icon="📡")
st.title("Network Log Analyzer Agent")
# key = st.sidebar.text_input("Groq API Key", type="password")
# st.sidebar.caption("Ya terminal me GROQ_API_KEY env variable set karo.")
st.sidebar.markdown("**Try karo:**\n- Network me kya problems hain?\n- router-delhi-01 ka status batao\n- optical-mumbai-02 me kya issue hai?")

if "chat" not in st.session_state:
    st.session_state.chat = []
for m in st.session_state.chat:
    st.chat_message(m["role"]).write(m["content"])

if q := st.chat_input("Network ke baare me kuch poocho..."):
    st.chat_message("user").write(q)
    with st.spinner("Agent soch raha hai..."):
        # ans, trace = run_agent(q, history=st.session_state.chat, api_key=key or None)
        ans, trace = run_agent(q, history=st.session_state.chat)
    with st.chat_message("assistant"):
        for name, args, res in trace:
            with st.expander(f"🔧 Tool: {name}({args})"):
                st.json(res)
        st.write(ans)
    st.session_state.chat += [{"role": "user", "content": q}, {"role": "assistant", "content": ans}]
