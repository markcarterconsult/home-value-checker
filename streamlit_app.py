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
    beds = st.number_input("Bedrooms", min_value=0, max_value=10)
    baths = st.number_input("Bathrooms", min_value=0, max_value=10)
    sqft = st.number_input("Interior Square Footage", min_value=100)
    lot_size = st.number_input("Lot Size (sqft)", min_value=0)
    pool = st.selectbox("Pool?", ["No", "Yes"])
    garage_type = st.selectbox("Garage Type", ["None", "Detached", "Attached"])
    garage_capacity = st.selectbox("Garage Capacity", ["N/A", "1-car", "2-car", "3-car", "4+ cars"])
    basement = st.selectbox("Basement", ["None", "Unfinished", "Finished"])
    condition = st.selectbox("Overall Condition", ["Excellent", "Good", "Fair", "Needs Work"])
    upgrades = st.text_area("Recent Renovations or Upgrades (optional)")
    submitted = st.form_submit_button("Get My Estimate")

# --- On Submit ---
if submitted:
    psf = get_price_per_sqft(zip_code)
    value_estimate = int(psf * sqft)
    price_range = f"${value_estimate - 15000:,} – ${value_estimate + 15000:,}"

    prompt = f"""
You are a home valuation expert.

Use the following data to generate an AI-powered home value summary. Provide a realistic price range and personalized recommendations to increase the value of this home.

Address: {address}
ZIP Code: {zip_code}
Bedrooms: {beds}
Bathrooms: {baths}
Interior Square Footage: {sqft}
Lot Size: {lot_size} sqft
Has Pool: {pool}
Garage Type: {garage_type}
Garage Capacity: {garage_capacity}
Basement: {basement}
Overall Condition: {condition}
Recent Upgrades: {upgrades}

Use ${psf}/sqft as a baseline for price calculation.

Estimated Home Value Range: {price_range}
"""

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    result = response.choices[0].message.content

    st.success("✅ Your Home Value Estimate:")
    st.markdown(result)

    lead_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "zip_code": zip_code,
        "beds": beds,
        "baths": baths,
        "sqft": sqft,
        "lot_size": lot_size,
        "pool": pool,
        "garage_type": garage_type,
        "garage_capacity": garage_capacity,
        "basement": basement,
        "condition": condition,
        "upgrades": upgrades,
        "psf_used": psf,
        "price_range": price_range,
        "gpt_summary": result
    }

    # Optional: Send to a webhook
    # requests.post("https://your-webhook-url.com", json=lead_data)

    # requests.post("https://your-webhook-url.com", json=lead_data)  # Uncomment to use


