
import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"

# City lists
tier_1_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Kolkata", "Hyderabad", "Pune"
]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow",
    "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot",
    "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra",
    "Dehradun", "Mysore", "Jabalpur", "Guwahati",
    "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli",
    "Belgaum", "Salem", "Vijayawada",
    "Tiruchirappalli", "Bhavnagar", "Gwalior",
    "Dhanbad", "Bareilly", "Aligarh", "Gaya",
    "Kozhikode", "Warangal", "Kolhapur", "Bilaspur",
    "Jalandhar", "Noida", "Guntur", "Asansol",
    "Siliguri"
]

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

# Page title
st.title("🏥 Insurance Premium Predictor")
st.write(
    "Enter your details below to predict your "
    "insurance premium category using Machine Learning."
)

st.divider()

# Input form
with st.form("insurance_form"):

    st.subheader("Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=119,
            value=25,
            step=1
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.1,
            value=70.0,
            step=0.5
        )

    with col2:
        height = st.number_input(
            "Height (meters)",
            min_value=0.1,
            max_value=2.49,
            value=1.70,
            step=0.01,
            format="%.2f"
        )

        income_lpa = st.number_input(
            "Annual Income (LPA)",
            min_value=0.1,
            value=5.0,
            step=0.5
        )

    st.subheader("Lifestyle Information")

    smoker = st.radio(
        "Do you smoke?",
        options=["No", "Yes"],
        horizontal=True
    )

    occupation = st.selectbox(
        "Occupation",
        options=[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job"
        ],
        format_func=lambda x: x.replace("_", " ").title()
    )

    st.subheader("Location")

    city_options = sorted(set(tier_1_cities + tier_2_cities))

    city = st.selectbox(
        "Select your city",
        options=city_options + ["Other"]
    )

    if city == "Other":
        city = st.text_input("Enter your city name")

    submitted = st.form_submit_button(
        "Predict Insurance Premium",
        type="primary",
        use_container_width=True
    )

# Handle prediction
if submitted:

    if not city or not city.strip():
        st.error("Please enter or select a city.")

    else:
        # Send only the input fields.
        # FastAPI computes BMI, age group,
        # lifestyle risk and city tier itself.
        payload = {
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "income_lpa": float(income_lpa),
            "smoker": smoker == "Yes",
            "city": city.strip(),
            "occupation": occupation
        }

        with st.spinner("Predicting insurance premium..."):

            try:
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=30
                )

                if response.ok:
                    result = response.json()

                    st.success("Prediction completed!")

                    st.subheader("Prediction Result")

                    st.metric(
                        label="Predicted Premium Category",
                        value=str(result["predicted_category"])
                    )

                    bmi = weight / (height ** 2)

                    with st.expander("View submitted details"):
                        st.write(f"**Age:** {age}")
                        st.write(f"**Weight:** {weight} kg")
                        st.write(f"**Height:** {height} m")
                        st.write(f"**BMI:** {bmi:.2f}")
                        st.write(
                            f"**Smoker:** {'Yes' if smoker == 'Yes' else 'No'}"
                        )
                        st.write(
                            f"**Annual Income:** ₹{income_lpa} LPA"
                        )
                        st.write(
                            f"**Occupation:** {occupation.replace('_', ' ').title()}"
                        )
                        st.write(f"**City:** {city}")

                else:
                    st.error(
                        f"API Error ({response.status_code})"
                    )
                    st.code(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to FastAPI. "
                    "Please start your backend on port 8000."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The prediction request timed out. "
                    "Please try again."
                )

            except (ValueError, KeyError):
                st.error(
                    "The API returned an unexpected response. "
                    "Check your backend output."
                )

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

st.divider()

st.caption(
    "Machine Learning-powered prediction. "
    "The result is an estimate, not an official insurance quote."
)
