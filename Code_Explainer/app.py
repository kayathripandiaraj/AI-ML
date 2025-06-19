import streamlit as st
import google.generativeai as ai
ai.configure(api_key="AIzaSyBDFS0BcCBL95of0WHbswUigMS7T0N-Bmw")
model= ai.GenerativeModel("gemini-1.5-flash")
st.set_page_config(page_title="🤖Code_Explainer",layout="centered")
st.title("🤖Code_Explainer")
st.markdown("This app uses Google Gemini to explain code in natural language. You can paste your code below and get an explanation.")
code=st.text_area("Paste your code here:")
lang = st. text_input("Enter your language:")
if st.button("Explain Code"):
    if code:
        with st.spinner("Generating explanation..."):
            response = model.generate_content(f"Explain the following code in simple words step by step in {lang} language:\n\n{code}")
            st.write(response.text)
    else:
        st.error("Please enter some code to explain.")
