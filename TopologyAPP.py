#platform.openai.com
from openai import OpenAI
import streamlit as st
from config import *

client = OpenAI(api_key=open("./keys.txt", "r").read().strip())

def chat_with_openai(input_text):
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            *input_text
            ],
        max_tokens=400,  # Begrenze die Antwortlänge
        temperature=0.5,  # Bestimmt, wie kreativ die Antworten sind (niedriger = deterministischer)
    )
    return chat_completion.choices[0].message.content

st.title("Your Topology Selector")
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": greeting}
    ]

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"<div style='text-align:right;'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f"<div style='text-align:left;'>{message['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("..."):
    with st.chat_message("user"):
        st.markdown(f"<div style='text-align:right;'>{prompt}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        response = chat_with_openai(st.session_state.messages)

    with st.chat_message("assistant"):
        st.markdown(f"<div style='text-align:left;'>{response}</div>", unsafe_allow_html=True)

    # Add assistant's message to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
