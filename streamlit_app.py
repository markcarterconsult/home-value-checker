import streamlit as st
import openai
import os

# Set up the OpenAI API key securely via Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page settings
st.set_page_config(page_title="Home Value Checker", page_icon="🏡", layout="centered")

# Title and intro
st.markdown("<h1 style='text-align: center;'>🏡 What's Your Home Worth?</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Fill out the form below and our AI will estimate your home's value.</p>", unsafe_allow_html=True)
st.write("")

# Form inputs
address = st.text_input("Street Address")
zip_code = st.text_input("ZIP Code")
bedrooms = st.number_input("Bedrooms", min_value=0, step=1)
bathrooms = st.number_input("Bathrooms", min_value=0, step=1)
condition = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Needs Work"])

# Submit button
if st.button("Estimate Home Value"):
    if address and zip_code:
        with st.spinner("Estimating home value..."):
            # Create a natural language prompt
            prompt = f"""
            You are a real estate assistant AI. Estimate the market value of a home based on the following information:

            Street Address: {address}
            ZIP Code: {zip_code}
            Bedrooms: {bedrooms}
            Bathrooms: {bathrooms}
            Condition: {condition}

            Provide an approximate value in USD (e.g., $425,000) and give a short rationale for the estimate.
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )
                result = response.choices[0].message.content.strip()
                st.success(result)

            except Exception as e:
                st.error(f"Something went wrong while fetching the home value: {e}")
    else:
        st.warning("Please enter both the street address and ZIP code to get a home value estimate.")
