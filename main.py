import streamlit as st
from agent import asla_brain

st.set_page_config(page_title="Artemis ASLA", page_icon="🚀")

st.title("👨‍🚀 Artemis Surface Log Agent")
st.subheader("Lunar Field Operations Interface")

# Input from the Astronaut
if "messages" not in st.session_state:
    st.session_state.messages = []

user_description = st.chat_input("Describe the sample (e.g., 'Dark, glass-like rock found near Shackleton Crater')")

# Create a persistant session ID in Streamlit
if  "thread_id" not in st.session_state:
    import uuid
    st.session_state.thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": st.session_state.thread_id}}


if user_description:
    # 1. Initialize the State
    initial_state = {
        "user_input": user_description,
        "analysis": "",
        "log_entry": "",
        "steps": []
    }

    # 2. Run the "Brain"
    with st.spinner("Accessing Mission Memory..."):
        final_output = asla_brain.invoke(initial_state, config=config)

    #3. Display results
    st.write("### 📜 Mission Log Generated")
    st.code(final_output['log_entry'], language="json")

    st.write("### 🧠 Analysis Detail")
    st.info(final_output['analysis'])

    st.write("### 🛰️ Execution Trace")
    st.caption(" -> ".join(final_output['steps']))