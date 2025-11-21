import streamlit as st
import pandas as pd
import joblib

# Load the trained model pipeline
try:
    pipeline = joblib.load('model.pkl')
except FileNotFoundError:
    st.error("Error: model.pkl not found. Please ensure the model file is in the same directory.")
    st.stop()

# Define the feature columns (used for creating the input DataFrame)
FEATURE_COLUMNS = [
    'gender', 'race/ethnicity', 'parental level of education',
    'lunch', 'test preparation course', 'reading score', 'writing score'
]

# Define the possible values for categorical features
CATEGORICAL_OPTIONS = {
    'gender': ['Female', 'Male'],
    'race/ethnicity': ['Group A', 'Group B', 'Group C', 'Group D', 'Group E'],
    'parental level of education': ["Primary School", "High School", "Some College", "Associate's Degree", "Bachelor's Degree", "Master's Degree"],
    'lunch': ['Standard', 'Free/Reduced'],
    'test preparation course': ['None', 'Completed']
}

# Streamlit App Title and Description
st.title("Student Math Score Predictor")
st.markdown("Enter the student's details to predict their **Math Score**.")

# --- Sidebar for Input Features ---
st.sidebar.header("Student Information")

# Categorical Inputs
gender = st.sidebar.selectbox("Gender", CATEGORICAL_OPTIONS['gender'])
race_ethnicity = st.sidebar.selectbox("Race/Ethnicity", CATEGORICAL_OPTIONS['race/ethnicity'])
parental_education = st.sidebar.selectbox("Parental Level of Education", CATEGORICAL_OPTIONS['parental level of education'])
lunch = st.sidebar.selectbox("Lunch Type", CATEGORICAL_OPTIONS['lunch'])
test_prep = st.sidebar.selectbox("Test Preparation Course", CATEGORICAL_OPTIONS['test preparation course'])

# Numerical Inputs (Scores are between 0 and 100)
reading_score = st.sidebar.slider("Reading Score", 0, 100, 70)
writing_score = st.sidebar.slider("Writing Score", 0, 100, 70)

# --- Prediction Logic ---
if st.sidebar.button("Predict Math Score"):
    # Create a DataFrame from the user inputs
    input_data = pd.DataFrame({
        'gender': [gender],
        'race/ethnicity': [race_ethnicity],
        'parental level of education': [parental_education],
        'lunch': [lunch],
        'test preparation course': [test_prep],
        'reading score': [reading_score],
        'writing score': [writing_score]
    })

    # Ensure the column order matches the training data
    input_data = input_data[FEATURE_COLUMNS]

    # Make prediction
    try:
        prediction = pipeline.predict(input_data)[0]
        
        # Display the result
        st.subheader("Prediction Result")
        st.success(f"The predicted Math Score is: **{prediction:.2f}**")
        
        # Optional: Show the input data for verification
        st.markdown("---")
        st.caption("Input Data Used for Prediction:")
        st.dataframe(input_data)

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# --- Instructions for Deployment ---
st.markdown("---")
st.info("To deploy this app, ensure you have `app.py`, `model.pkl`, and `requirements.txt` in the same folder, and run: `streamlit run app.py`")
