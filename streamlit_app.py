import streamlit as st
from openai import OpenAI
import requests

# --- Static ZIP Code → Price per Square Foot Mapping ---
zip_price_map = {
    "63130": 195,
    "63141": 225,
    "63119": 240,
    "63104": 215,
    "63109": 230,
    "default": 185
}

# --- Optional API override placeholder ---
def fetch_psf_from_api(zip_code):
    # Placeholder for Redfin, ATTOM, etc.
    return None

def get_price_per_sqft(zip_code):
    psf = zip_price_map.get(zip_code, zip_price_map["default"])
    try:
        live_psf = fetch_psf_from_api(zip_code)
        if live_psf:
            psf = live_psf
    except:
        pass
    return psf

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Home Value Estimator", layout="centered")
st.title("🏡 Instant Home Value Estimator")
st.write("Enter your property details below to get an AI-powered home value estimate.")

# --- Form ---
with st.form("lead_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    address = st.text_input("Property Address")
    zip_code = st.text_input("ZIP Code")
    beds = st.number_input("Bedrooms", min_value=0, max_value=10, step=1)
    baths = st.number_input("Bathrooms", min_value=0, max_value=10, step=1)
    sqft = st.number_input("Square Footage", min_value=100)
    submitted = st.form_submit_button("Get My Estimate")

# --- On Submit ---
if submitted:
    psf = get_price_per_sqft(zip_code)
    value_estimate = int(psf * sqft)
    price_range = f"${value_estimate - 15000:,} – ${value_estimate + 15000:,}"

    prompt = f"""
You are a home valuation expert.

Use the following data to generate an AI-powered home value summary. Include the estimated price range and two personalized recommendations to increase the home's value.

Address: {address}
ZIP Code: {zip_code}
Bedrooms: {beds}
Bathrooms: {baths}
Square Footage: {sqft}
Price per Square Foot Used: ${psf}

Estimated Home Value Range: {price_range}
"""

    # Use OpenAI v1 format
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    result = response.choices[0].message.content

    st.success("✅ Your Home Value Estimate:")
    st.markdown(result)

    # Optional: Save or send the lead
    lead_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "zip_code": zip_code,
        "beds": beds,
        "baths": baths,
        "sqft": sqft,
        "psf_used": psf,
        "price_range": price_range,
        "gpt_summary": result
    }

    # requests.post("https://your-webhook-url.com", json=lead_data)  # Uncomment to use

