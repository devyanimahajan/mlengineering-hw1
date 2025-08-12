# streamlit_headline_app.py
# Author: Devyani Mahajan
# Date: 12.8.25
# Port: 9012 

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8012/analyze"  

st.set_page_config(page_title="Headline Sentiment Analyser", layout="centered")
st.markdown(
    "<h1 style='color:pink;'>🪷Headline Sentiment Analyser🪷</h1>",
    unsafe_allow_html=True
)
st.write("This web app analyses the sentiment of news headlines from the New York Times and the Chicago Tribune")
st.write("Headlines are rated as either Optimistic, Pessimistic, or Neutral.")
st.write("Enter headlines below and then click **Analyse Headlines**.")

# Store headlines 
if "headlines" not in st.session_state:
    st.session_state.headlines = [""]

# Add headline input fields 
for i in range(len(st.session_state.headlines)):
    st.session_state.headlines[i] = st.text_input(
        f"Headline {i+1}", st.session_state.headlines[i], key=f"headline_{i}"
    )

# Buttons to add/remove headlines
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add Headline"):
        st.session_state.headlines.append("")
with col2:
    if st.button("➖ Remove Last Headline") and len(st.session_state.headlines) > 1:
        st.session_state.headlines.pop()

st.divider()

# Submit to API
if st.button("Analyse Headlines"):
    headlines_to_send = [h for h in st.session_state.headlines if h.strip()]
    if not headlines_to_send:
        st.warning("Please enter at least one headline.")
    else:
        try:
            response = requests.post(API_URL, json={"headlines": headlines_to_send})
            if response.status_code == 200:
                predictions = response.json().get("predictions", [])
                st.subheader("Results")
                for h, p in zip(headlines_to_send, predictions):
                    st.write(f"**{h}** → Sentiment: `{p}`")
            else:
                st.error(f"API Error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to API. Is it running?")