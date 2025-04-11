import streamlit as st
import openai

# Optional: Hide Streamlit branding, footer, etc.
st.set_page_config(page_title="Home Value Checker", layout="centered")

# Title & Description
st.markdown("<h1 style='text-align: center;'>🏡 What’s Your Home Worth?</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Fill out the form below and our AI will estimate your home's value.</p>", unsafe_allow_html=True)

# --- Contact Info ---
st.subheader("👤 Your Contact Info")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

# --- Property Details ---
st.subheader("🏠 Property Details")
address = st.text_input("Street Address")
zip_code = st.text_input("ZIP Code")
bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, step=1)
bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, step=1)
condition = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Needs Work"])

# --- Submit Button ---
if st.button("Estimate Home Value"):
    if not all([name, email, phone, address, zip_code]):
        st.warning("Please fill in all fields before continuing.")
    else:
        with st.spinner("Estimating your home's value..."):
            # Simulate an AI response
            estimated_value = "$412,000"  # Placeholder
            st.success(f"✅ Based on our analysis, your home is worth approximately {estimated_value}.")

            # Optional: Show contact info back to the user or log it
            st.info(f"We'll also follow up at {email} or {phone} if you'd like a more detailed report.")
