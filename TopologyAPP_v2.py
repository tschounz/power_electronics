#platform.openai.com
import streamlit as st
from openai import OpenAI
from config_v2 import *

#client = OpenAI(api_key=open("./source/llm/keys.txt", "r").read().strip())
client = OpenAI(api_key=st.secrets["DB_TOKEN"])

def chat_with_openai(input_text):
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            *input_text
            ],
        max_tokens=800,  # Begrenze die Antwortlänge
        temperature=0.1,  # Bestimmt, wie kreativ die Antworten sind (niedriger = deterministischer)
    )
    return chat_completion.choices[0].message.content

# Title for the app
st.title("Topology Finder")
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": greeting}
    ]

# Text
st.write(greeting)

# Input fields
vin = st.text_input("Input Voltage (Please do not forget to indicate whether it is AC or DC)", "")
vout = st.text_input("Output Voltage (AC or DC?)", "")
power = st.text_input("Power", "")
galvanic_isolation = st.checkbox("Galvanically isolated?")
anything = st.text_input("Anything else to be considered?", "")

st.session_state.messages.append({"role": "user", "content": f"Vin: {vin}, Vout: {vout}, Power: {power}, Galvanically isolated: {'Yes' if galvanic_isolation else 'No'}, {anything}"})

if 'button_labels' not in st.session_state:
    st.session_state.button_labels = []

# Button to start the analysis
if st.button("Start Analysis"):
    with st.spinner("Thinking..."):
        response = chat_with_openai(st.session_state.messages)
    st.session_state.button_labels = response.split(";")
    j = len(st.session_state.button_labels)
    print(st.session_state.button_labels)

if st.session_state.button_labels:
    st.write("The topology/topologies that suite your requirements best is/are:")
    for label in st.session_state.button_labels[:-1]:
        if st.button(label):
            st.session_state.messages.append({"role": "user", "content": f"Why you chose {label} and what controller IC would suite best for above topologie(s)? (keep the answer short and put a distance between the two answers)"})
            with st.spinner("Thinking..."):
                response = chat_with_openai(st.session_state.messages)
            st.write("[Click here for a detailed topology analysis](https://frenetic.ai/)")
            st.text_area(response)
            

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

# # Button for more details
# if st.session_state.button_labels:
#     if st.button("Explanation of choice"):
#         with st.spinner("Thinking..."):
#             st.write(st.session_state.button_labels[-1])

# # Suggest IC controllers button and text field
# # Button for more details
# if st.session_state.button_labels:
#     if st.button("Suggest IC controllers"):
#         st.session_state.messages.append({"role": "user", "content": "What Controller IC would suite best for above topologie(s)?"})
#         with st.spinner("Thinking..."):
#             response = chat_with_openai(st.session_state.messages)
#         st.write("Based on your inputs, the following IC controllers are suggested:")
#         st.text_area(response)

