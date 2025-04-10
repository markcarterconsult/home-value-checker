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

