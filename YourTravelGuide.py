import streamlit as st
from openai import OpenAI
from TravelConfig import *

client = OpenAI(api_key=open("./keys.txt", "r").read().strip())
#client = OpenAI(api_key=st.secrets["DB_TOKEN"])

def chat_with_openai(input_text):
    chat_completion = client.chat.completions.create(
        model="o1-preview-2024-09-12",
        #model="gpt-4o",
        messages=[
            {"role": "user", "content": system_prompt},
            *input_text
            ],
    )
    return chat_completion.choices[0].message.content

# Title for the app
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "user", "content": greeting}
    ]

# Sidebar for input parameters
st.sidebar.title("Your Travel Agent")
#st.sidebar.header("")
#st.sidebar.markdown("Please do not forget to indicate whether it is AC or DC. Alternatively, you can mention a standard like USB-C instead of a voltage value.")

# Input fields
where = st.sidebar.text_input("Where do you want to go? Tell me as much as you think is of interest for me to plan your trip.", "")
duration = st.sidebar.text_input("How long will your trip be?", "")
who = st.sidebar.text_input("Who are you? How many? What are your interests? Tell me about yourself...", "")
why = st.sidebar.text_input("Why you do this trip? Adventure, Relaxation, ...?", "")
price = st.sidebar.text_input("How much are you willing to spend? Feel free to answer qualitatively", "")
#galvanic_isolation = st.sidebar.checkbox("Galvanically isolated?")
anything = st.sidebar.text_input("Anything else to be considered?", "")

st.session_state.messages.append({"role": "user", "content": f"Where: {where}, Who: {who}, Duration: {duration}, Why: {why}, Price: {price}, {anything}"})

if 'button_labels' not in st.session_state:
    #st.session_state.button_labels = []
    response = ""

# Button to start the analysis
if st.sidebar.button("Suggest Trip"):
    with st.spinner("Thinking..."):
        response = chat_with_openai(st.session_state.messages)
        #print(response)
    #st.session_state.button_labels = response.split(";")
    #j = len(st.session_state.button_labels)

#st.write("Here my trip for you:")
st.write(response)

# if st.session_state.button_labels:
#     st.write("The topologies that suite your requirements best are (click for more details):")
#     for label in st.session_state.button_labels:
#         if st.button(label):
#             with st.spinner("Thinking..."):
#                 st.session_state.messages.append({"role": "user", "content": f"Why you chose {label}? (keep the answer short; in case a AC/DC input stage is needed, mention this)"})
#                 response_why = chat_with_openai(st.session_state.messages)
#                 st.session_state.messages.append({"role": "user", "content": f"What controller IC would suite best for above topologie(s)? (keep the answer short and provide only a list of manufacturers and ICs, each on a new line.)"}) #Only use controllers from https://www.renesas.com/en; say if you don't find any.
#                 response_controller = chat_with_openai(st.session_state.messages)
#                 st.session_state.messages.append({"role": "user", "content": f"List things such as switching frequency, DCM vs. CCM, L and C values, turn ratios, etc. for the {label}; always build a table that has multiple options of switching frequency, duty cycle and turns ratio as parameters, and show the related other parameters (output/input current, magnetizing inductance, and other if applicable). Only show feasable designs. if some parameters are not important for a topology, ignore it. ONLY show the table or multiple tables if two converters are to be connected. No explaining text!"})
#                 circuit_design = chat_with_openai(st.session_state.messages)
#             st.write(response_why)
#             st.subheader("Circuit Design Choices")
#             st.markdown(circuit_design)   
#             st.write("[Click here for a detailed topology analysis with above settings](https://frenetic.ai/)")
#             st.subheader("Possible Controllers")
#             st.write(response_controller)   