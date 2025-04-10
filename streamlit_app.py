import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="🏡 Home Value Checker", layout="centered")
st.title("🏡 What's Your Home Worth?")
st.write("Fill out the form below and our AI will estimate your home's value.")

# Form inputs
address = st.text_input("Street Address")
zip_code = st.text_input("ZIP Code")
bedrooms = st.number_input("Bedrooms", min_value=0)
bathrooms = st.number_input("Bathrooms", min_value=0)
condition = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Needs Work"])

# Button triggers AI
if st.button("Estimate Home Value"):
    with st.spinner("Estimating..."):
        prompt = f"""
        Estimate the value of a home with the following details:
        Address: {address}
        ZIP: {zip_code}
        Bedrooms: {bedrooms}
        Bathrooms: {bathrooms}
        Condition: {condition}
        Give an approximate home value in USD with a short explanation.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            value = response.choices[0].message.content
            st.success(value)

        except Exception as e:
            st.error(f"Error: {e}")
if st.button("Estimate Home Value"):
    if address and zip_code:
        with st.spinner("Estimating home value..."):
            prompt = f"""
            Estimate the market value of a home with the following details:

            Street Address: {address}
            ZIP Code: {zip_code}
            Bedrooms: {bedrooms}
            Bathrooms: {bathrooms}
            Condition: {condition}

            Provide an approximate value in USD and a brief explanation why.
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                result = response.choices[0].message.content
                st.success(result)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter at least the address and ZIP code.")
