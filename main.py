import os
import streamlit as st
import openai
import time

# Ensure the OPENAI_API_KEY environment variable is set in your deployment environment.
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=openai_api_key)

# Replace these with your actual Assistant ID and a method to generate or retrieve thread IDs dynamically
assistant_id = "asst_lMPPUjeM30PUEMntQgWABJE8"
thread_id = "thread_KVDnas2AMxbT9AljutOLc0IU"

# Streamlit page setup
st.set_page_config(page_title="Senior Design Assistant - Chat and Learn", page_icon=":pencil:")
st.title("Senior Design Assistant")
st.write("Efficiently increase productivity in design workflow")

# Initialize 'messages' in session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display all previous messages
for message in st.session_state["messages"]:
    role = "You" if message["role"] == "user" else "Assistant"
    st.markdown(f'<span style="color: grey;">**{role}:** {message["content"]}</span>', unsafe_allow_html=True)

# Input box for new user message, changed to text_area for text wrapping
user_input = st.text_area("Ask something...", key="user_input", height=75)

if st.button("Send"):
    if user_input.strip():  # Ensure input is not just whitespace
        st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
        client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input.strip())

        with st.spinner("Hm...Thinking...Don't Rush me..."):
            run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
            while True:
                time.sleep(1)
                run_update = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
                if run_update.status == "completed":
                    messages = client.beta.threads.messages.list(thread_id=thread_id, limit=1, order="desc")
                    latest_message = messages.data[0]
                    if latest_message:
                        st.session_state["messages"].append({"role": "assistant", "content": latest_message.content[0].text.value})
                    break

        # Clear the input box after sending the message
        st.experimental_rerun()

# Note: If using Streamlit Sharing, set your OPENAI_API_KEY as a secret in the app settings.

