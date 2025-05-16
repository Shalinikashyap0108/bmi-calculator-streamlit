# streamlit_bmi_app.py

import streamlit as st
import pandas as pd

# Title and layout
st.set_page_config(page_title="BMI Calculator", layout="centered")
st.title("🧮 BMI Calculator")
st.markdown("Enter your height (in cm) and weight (in kg) to calculate your Body Mass Index (BMI).")

# Initialize session state for history if not already present
if "bmi_history" not in st.session_state:
    st.session_state.bmi_history = []

# Input fields
col1, col2 = st.columns(2)
with col1:
    height_cm = st.number_input("Height (cm)", min_value=0.0, step=0.1)
with col2:
    weight_kg = st.number_input("Weight (kg)", min_value=0.0, step=0.1)

# Calculate BMI
def calculate_bmi(height_cm, weight_kg):
    if height_cm <= 0 or weight_kg <= 0:
        return None, "Invalid input"
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
        color = "blue"
    elif bmi < 25:
        category = "Normal weight"
        color = "green"
    elif bmi < 30:
        category = "Overweight"
        color = "orange"
    else:
        category = "Obese"
        color = "red"
    return round(bmi, 2), (category, color)

if st.button("Calculate BMI"):
    bmi, result = calculate_bmi(height_cm, weight_kg)
    if bmi is None:
        st.error("Please enter valid height and weight.")
    else:
        category, color = result
        st.markdown(f"### Your BMI is **{bmi}**")
        st.markdown(f"<span style='color:{color}'>**Category: {category}**</span>", unsafe_allow_html=True)

        # Store in history
        st.session_state.bmi_history.append({
            "Height (cm)": height_cm,
            "Weight (kg)": weight_kg,
            "BMI": bmi,
            "Category": category
        })

# Display history
if st.session_state.bmi_history:
    st.subheader("📜 History")
    df = pd.DataFrame(st.session_state.bmi_history)
    st.dataframe(df, use_container_width=True)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download History as CSV",
        data=csv,
        file_name='bmi_history.csv',
        mime='text/csv'
    )