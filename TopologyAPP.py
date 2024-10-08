#platform.openai.com
from openai import OpenAI
import streamlit as st
#from config import greeting
#from gpt import get_openai_response

client = OpenAI(api_key=open("./source/llm/keys.txt", "r").read().strip())

def chat_with_openai(input_text):
    chat_completion = client.chat.completions.create(
        messages=input_text,
        max_tokens=400,  # Begrenze die Antwortlänge
        temperature=0.5,  # Bestimmt, wie kreativ die Antworten sind (niedriger = deterministischer)
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content

st.title("Your Topology Selector")
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You propose the most suitable power electronics toplogy based on the given requirements. If unclear, you ask for further inputs. Always make sure that voltage ranges (input and output), power level, isolation requirements are given. You can provide options of topologies with some background. Reply with a short explanation why this is the case. Never reply to a question that is not related to power electronics topologies."}
    ]

# User input
st.text_area("","Hello, please provide me with details such as voltage ranges, power levels, isolation requirements, and EMI considerations. Feel free to add any additional information. I will then provide you with a topology proposal.\n")

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


# user_input = st.text_input("You:", key='input')

# if st.button("Send"):
#     if user_input:
#         # User message
#         st.session_state['messages'].append({"role": "user", "content": user_input})

#         # Assistant's response
#         with st.spinner("typing..."):
#             try:
#                 assistant_reply = chat_with_openai(st.session_state['messages'])
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")
#                 assistant_reply = "I'm sorry, but I'm unable to process your request at the moment."

#         #print(assistant_reply)
#         #Append assistant's reply
#         #st.session_state['messages'].append({"role": "assistant", "content": assistant_reply})
#         st.text_area("",assistant_reply, height=300)

#         # # Clear input
#         # st.session_state['input'] = ''

#         # Refresh the app
#         #st.experimental_rerun()

