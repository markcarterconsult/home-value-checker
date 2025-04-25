import streamlit as st
from openai import OpenAI
import requests
import re

st.set_page_config(page_title="Home Value Estimator", layout="centered")

# ✅ Use system UI font stack
st.markdown("""
<style>
html, body, div, p, span, h1, h2, h3, h4, h5, h6, li, ul {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 18px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

zip_price_map = {
    "63130": 195,
    "63141": 225,
    "63119": 240,
    "63104": 215,
    "63109": 230,
    "default": 185
}

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

def build_html_summary(address, beds, baths, sqft, psf, price_range, result):
    bullets = re.findall(r"\d+\.\s+(.*)", result)
    html = f'''
    <h3 style='margin-bottom: 0.5em;'>Home Value Estimate for {address.title()}</h3>
    <p>Your home – featuring <strong>{beds} bedrooms</strong>, <strong>{baths} bathrooms</strong>, and <strong>{sqft:,} sqft</strong> of interior space – is currently estimated to be worth between:</p>
    <h2 style='font-size: 26px; margin: 0.5em 0;'>${price_range}</h2>
    <p>This estimate is based on a baseline price of <strong>${psf} per square foot</strong>.</p>
    <hr style='margin: 1.5em 0;' />
    <h4 style='margin-top: 1em;'>Recommendations to Increase Home Value</h4>
    <ul>
    '''
    if bullets:
        for tip in bullets:
            html += f"<li>{tip.strip()}</li>"
    else:
        html += f"<li>{result.strip()}</li>"
    html += '''
    </ul>
    <p style='margin-top: 2em; font-size: 14px; color: #666;'>Note: Market conditions vary. Consult a licensed real estate professional before starting major projects.</p>
    '''
    return html

st.markdown("<h1>Home Value Estimator</h1>", unsafe_allow_html=True)
st.write("Enter your property details below to get an AI-powered home value estimate.")

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

if submitted:
    psf = get_price_per_sqft(zip_code)
    value_estimate = int(psf * sqft)
    price_range = f"${value_estimate - 15000:,} – ${value_estimate + 15000:,}"

    prompt = f'''
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
'''

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    result = response.choices[0].message.content

    summary_html = build_html_summary(address, beds, baths, sqft, psf, price_range, result)

    copy_html = f'''
<div style='
    font-size: 18px;
    line-height: 1.6;
    padding: 1.5em;
    background-color: #f8fff4;
    border-left: 5px solid #4CAF50;
    border-radius: 6px;
'>
    <h2 style='margin-top: 0;'>Your Home Value Estimate</h2>
    {summary_html}
</div>
'''
    st.markdown(copy_html, unsafe_allow_html=True)
    with st.expander("📋 Copy HTML Output"):
        st.code(copy_html, language='html')
        st.button("Copy to Clipboard (Cmd+C / Ctrl+C)")
