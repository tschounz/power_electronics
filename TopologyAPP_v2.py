#platform.openai.com
import streamlit as st
from openai import OpenAI
from config_v2 import *

#client = OpenAI(api_key=open("./keys.txt", "r").read().strip())
client = OpenAI(api_key=st.secrets["DB_TOKEN"])

def chat_with_openai(input_text):
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            *input_text
            ],
        max_tokens=400,  # Begrenze die Antwortlänge
        temperature=0.25,  # Bestimmt, wie kreativ die Antworten sind (niedriger = deterministischer)
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
vin = st.text_input("Input Voltage Range (Please do not forget to indicate whether it is AC or DC)", "")
vout = st.text_input("Output Voltage Range (AC or DC? Alternatively, you can mention a standard like USB-C instead of a voltage value)", "")
power = st.text_input("Power", "")
galvanic_isolation = st.checkbox("Galvanically isolated?")
anything = st.text_input("Anything else to be considered?", "")

st.session_state.messages.append({"role": "user", "content": f"Vin: {vin}, Vout: {vout}, Power: {power}, Galvanically isolated: {'Yes' if galvanic_isolation else 'No'}, {anything}"})

if 'button_labels' not in st.session_state:
    st.session_state.button_labels = []

# Button to start the analysis
if st.button("Get Topology Proposal"):
    with st.spinner("Thinking..."):
        response = chat_with_openai(st.session_state.messages)
    st.session_state.button_labels = response.split(";")
    j = len(st.session_state.button_labels)
    #print(st.session_state.button_labels)

if st.session_state.button_labels:
    st.write("The topologies that suite your requirements best are:")
    for label in st.session_state.button_labels:
        if st.button(label):
            with st.spinner("Thinking..."):
                st.session_state.messages.append({"role": "user", "content": f"Why you chose {label}? (keep the answer short; in case a AC/DC input stage is needed, mention this)"})
                response_why = chat_with_openai(st.session_state.messages)
                st.session_state.messages.append({"role": "user", "content": f"What controller IC would suite best for above topologie(s)? (keep the answer short and provide only a list of manufacturers and ICs, each on a new line.)"}) #when asked from ICs, only propose products from https://www.renesas.com; 
                response_controller = chat_with_openai(st.session_state.messages)
            st.write(response_why)
            st.write("[Click here for a detailed topology analysis](https://frenetic.ai/)")
            st.subheader("Possible Controllers")
            st.write(response_controller)   

