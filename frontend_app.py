
import streamlit as st
import requests
import pandas as pd

# --------------------------------
# FastAPI Configuration
# --------------------------------
API_URL = "http://127.0.0.1:8000/predict"

# --------------------------------
# City Lists
# --------------------------------
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
    "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly",
    "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida",
    "Guntur", "Asansol", "Siliguri"
]

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

# --------------------------------
# Custom CSS
# --------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #9CA3AF;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .prediction-card {
        padding: 22px;
        border: 1px solid rgba(128, 128, 128, 0.35);
        border-radius: 14px;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .prediction-label {
        font-size: 15px;
        color: #9CA3AF;
        margin-bottom: 8px;
    }

    .prediction-value {
        font-size: 30px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------
# Header
# --------------------------------
st.markdown(
    '<div class="main-title">🏥 Insurance Premium Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict an insurance premium category using Machine Learning.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------
# Input Form
# --------------------------------
with st.form("insurance_form"):

    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age (years)",
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

    st.subheader("🏃 Lifestyle Information")

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

    st.subheader("📍 Location")

    city_options = sorted(
        set(tier_1_cities + tier_2_cities)
    )

    city_choice = st.selectbox(
        "Select your city",
        options=city_options + ["Other"]
    )

    # Form inputs are submitted together.
    # If Other is selected, show a separate city input
    # outside this form below.

    submitted = st.form_submit_button(
        "Predict Insurance Premium",
        type="primary",
        use_container_width=True
    )

# --------------------------------
# Optional Custom City Input
# --------------------------------
# Streamlit forms submit their fields together, so a custom
# city input is placed outside the form.
custom_city = ""

if city_choice == "Other":
    custom_city = st.text_input(
        "Enter your city name",
        key="custom_city"
    )

# --------------------------------
# Prediction Logic
# --------------------------------
if submitted:

    city = (
        custom_city.strip()
        if city_choice == "Other"
        else city_choice
    )

    if not city:
        st.error("Please enter your city.")

    else:
        payload = {
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "income_lpa": float(income_lpa),
            "smoker": smoker == "Yes",
            "city": city,
            "occupation": occupation
        }

        with st.spinner("Analyzing your information..."):

            try:
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=30
                )

                if response.ok:

                    result = response.json()

                    # --------------------------------
                    # Extract API Response
                    # Supports your nested API response:
                    # {
                    #   "predicted_category": {
                    #       "predicted_category": "Low",
                    #       "confidence": 0.46,
                    #       "class_probabilities": {...}
                    #   }
                    # }
                    # --------------------------------
                    prediction_data = result.get(
                        "predicted_category", result
                    )

                    if isinstance(prediction_data, dict):
                        predicted_category = prediction_data.get(
                            "predicted_category", "N/A"
                        )

                        confidence = prediction_data.get(
                            "confidence",
                            result.get("confidence")
                        )

                        class_probabilities = prediction_data.get(
                            "class_probabilities",
                            result.get("class_probabilities", {})
                        )

                    else:
                        predicted_category = prediction_data

                        confidence = result.get("confidence")

                        class_probabilities = result.get(
                            "class_probabilities", {}
                        )

                    # --------------------------------
                    # Prediction Result
                    # --------------------------------
                    st.divider()
                    st.header("📊 Prediction Results")

                    # Field 1: Predicted Category
                    st.markdown(
                        f"""
                        <div class="prediction-card">
                            <div class="prediction-label">
                                Predicted Premium Category
                            </div>
                            <div class="prediction-value">
                                {predicted_category}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Field 2: Confidence
                    if confidence is not None:

                        confidence_value = float(confidence)

                        # Convert decimal probability to percentage.
                        confidence_percent = (
                            confidence_value * 100
                            if 0 <= confidence_value <= 1
                            else confidence_value
                        )

                        st.metric(
                            label="Model Confidence",
                            value=f"{confidence_percent:.2f}%"
                        )

                        st.progress(
                            max(
                                0.0,
                                min(1.0, confidence_percent / 100)
                            )
                        )

                    # Field 3: Class Probabilities
                    if (
                        isinstance(class_probabilities, dict)
                        and class_probabilities
                    ):
                        st.subheader("Class Probabilities")

                        probability_rows = []

                        for category, probability in (
                            class_probabilities.items()
                        ):
                            probability_value = float(probability)

                            probability_percent = (
                                probability_value * 100
                                if 0 <= probability_value <= 1
                                else probability_value
                            )

                            probability_rows.append({
                                "Category": str(category),
                                "Probability (%)": probability_percent
                            })

                        probability_df = pd.DataFrame(
                            probability_rows
                        ).sort_values(
                            by="Probability (%)",
                            ascending=False
                        )

                        # Display each category and its probability
                        for _, row in probability_df.iterrows():

                            category = row["Category"]
                            probability_percent = row[
                                "Probability (%)"
                            ]

                            st.write(
                                f"**{category}:** "
                                f"{probability_percent:.2f}%"
                            )

                            st.progress(
                                max(
                                    0.0,
                                    min(
                                        1.0,
                                        probability_percent / 100
                                    )
                                )
                            )

                        # Probability summary table
                        st.dataframe(
                            probability_df.style.format({
                                "Probability (%)": "{:.2f}%"
                            }),
                            use_container_width=True,
                            hide_index=True
                        )

                    # --------------------------------
                    # Submitted User Details
                    # --------------------------------
                    with st.expander("View submitted details"):

                        st.write(f"**Age:** {age} years")
                        st.write(f"**Weight:** {weight} kg")
                        st.write(f"**Height:** {height} m")

                        bmi = weight / (height ** 2)

                        st.write(f"**BMI:** {bmi:.2f}")

                        st.write(
                            f"**Smoker:** "
                            f"{'Yes' if smoker == 'Yes' else 'No'}"
                        )

                        st.write(
                            f"**Annual Income:** ₹{income_lpa} LPA"
                        )

                        st.write(
                            f"**Occupation:** "
                            f"{occupation.replace('_', ' ').title()}"
                        )

                        st.write(f"**City:** {city}")

                else:
                    st.error(
                        f"API Error: {response.status_code}"
                    )
                    st.code(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to FastAPI. "
                    "Start your backend on port 8000."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The prediction request timed out. "
                    "Please try again."
                )

            except (
                ValueError,
                TypeError,
                KeyError
            ) as error:
                st.error(
                    f"Invalid API response: {error}"
                )

            except requests.exceptions.RequestException as error:
                st.error(f"Request failed: {error}")

# --------------------------------
# Footer
# --------------------------------
st.divider()

st.caption(
    "Machine Learning-powered prediction for informational purposes. "
    "This is not an official insurance quote."
)
