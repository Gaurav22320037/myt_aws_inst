import streamlit as st
import pandas as pd
import requests
import pickle
import os
import sqlite3
from PIL import Image
import bcrypt
import hashlib
import numpy as np



# API credentials
API_KEY = "661e31209c95328976a7cdc51aebf03f"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"



# Load models
with open('best_rfc.pkl', 'rb') as crop_model_file:
    crop_model = pickle.load(crop_model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)



# Crop dictionary
crop_dict = {
    0: 'Rice', 1: 'Maize', 2: 'Jute', 3: 'Cotton', 4: 'Coconut', 5: 'Papaya', 6: 'Orange', 7: 'Apple',
    8: 'Muskmelon', 9: 'Watermelon', 10: 'Grapes', 11: 'Mango', 12: 'Banana', 13: 'Pomegranate',
    14: 'Lentil', 15: 'Blackgram', 16: 'MungBean', 17: 'MothBeans', 18: 'PigeonPeas', 19: 'KidneyBeans',
    20: 'ChickPea', 21: 'Coffee'
}

# Reverse mapping for nutrient prediction
reverse_crop_dict = {v: k for k, v in crop_dict.items()}

# Function to fetch 5-day weather forecast
def fetch_weather_data(city_name):
    try:
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        temp = [forecast['main']['temp'] for forecast in data['list']]
        humidity = [forecast['main']['humidity'] for forecast in data['list']]
        avg_temp = sum(temp) / len(temp)
        avg_humidity = sum(humidity) / len(humidity)
        return avg_temp, avg_humidity
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None, None

    


#Database setup
DB_FILE = "users.db"
FEEDBACK_TABLE = "feedback"

# Initialize the SQLite database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")


# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User authentication functions
def signup_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    return cursor.fetchone() is not None

# start of the app
st.set_page_config(page_title="Crop & Nutrient Recommendation", layout="wide")

# Background style
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://www.transparenttextures.com/patterns/fancy-deboss.png");
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# User session management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Login/Signup system
if not st.session_state.logged_in:
    with st.sidebar:
        st.header("Authentication")
        choice = st.radio("Select Action", ["Login", "Signup"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Submit"):
            if choice == "Login":
                if login_user(username, password):
                    st.success("Logged in successfully!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                else:
                    st.error("Invalid username or password.")
            elif choice == "Signup":
                if signup_user(username, password):
                    st.success("Account created successfully!")
                else:
                    st.error("Username already exists.")



# Apply custom CSS for a transparent background image
st.markdown("""
    <style>
        body {
            background-image: url("https://i.imgur.com/ZvX3Xs6.png"); 
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }
        .transparent {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)
if st.session_state.logged_in:
    # Tabs for app navigation
    homepage, tab1, tab2,feedback_tab = st.tabs(["🏠 Home", "📋 Predict Crop", "🧪 Predict Nutrients","💬feedback"])
    with st.sidebar:
        st.header(f"Welcome, {st.session_state.username}!")
        if st.button("logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.experimental_rerun()
    # Home Tab
    with homepage:
        st.markdown("""
                    <div class="transparent">
                    <h1 style="text-align: center;">🌾 Welcome to the Crop & Nutrient Recommendation System 🌾</h1>
                    <p style="text-align: center; font-size: 18px;">
                    This platform provides recommendations for the best crops based on soil nutrients and weather conditions.
                    Additionally, it predicts the optimal nutrient requirements for selected crops to boost agricultural yields.
                    </p>
                    <div style="text-align: center;">
                    <a href="https://github.com/maliabhi23/i" target="_blank" style="margin: 0 10px;">🌐 GitHub</a>
                </div>
            </div>
                """, unsafe_allow_html=True)
    # Tab 1: Predict Crop
    with tab1:
        st.header("1️⃣ Soil Nutrient Details")
        nitrogen = st.number_input("Nitrogen (N)", min_value=0, max_value=200, step=1)
        phosphorus = st.number_input("Phosphorus (P)", min_value=0, max_value=200, step=1)
        potassium = st.number_input("Potassium (K)", min_value=0, max_value=200, step=1)
        ph_value = st.slider("pH Value", min_value=0.0, max_value=14.0, step=0.1)
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, step=0.1)
        st.header("2️⃣ Weather Details")
        weather_input_method = st.radio("How would you like to provide weather details?",
                                     options=["Enter manually", "Fetch using city name"])
        if weather_input_method == "Enter manually":
            temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, step=0.1)
            humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, step=1)
        else:
            city_name = st.text_input("Enter City Name:")
            if city_name:
                avg_temp, avg_humidity= fetch_weather_data(city_name)
                if avg_temp is not None:
                    st.write(f"🌡️ Average Temperature (°C): {avg_temp:.2f}")
                    st.write(f"💧 Average Humidity (%): {avg_humidity:.2f}")
                    temperature = avg_temp
                    humidity = avg_humidity
                else:
                    st.warning("Unable to fetch weather data. Please try again.")

        if st.button("Predict Crop"):
            if temperature is not None and humidity is not None and rainfall is not None:
                input_data = scaler.transform([[nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall]])
                prediction = crop_model.predict(input_data)
                predicted_crop = crop_dict.get(prediction[0], "Unknown Crop")
                st.success(f"🌱 The recommended crop for your field is: **{predicted_crop}**")
            else:
                st.warning("Please provide all the required inputs.")

    # Tab 2: Predict Nutrients
    with tab2:
        st.header("🌾 Select Crop to Predict Nutrient Requirements")
        crop_name = st.selectbox("Select a Crop", options=list(reverse_crop_dict.keys()))

  
        df = pd.read_csv(r"E:\Datasets\Crop_Recommendation.csv")

        # function for fetching the nutrients
        def fetch(crop):
            sp_crop_df = df[df["Crop"] == crop]
            nutrient_range = dict()
            for col in sp_crop_df.columns:
                if col == "Crop":
                    continue
                nutrient_range[col] = (
                    np.percentile(sp_crop_df[col], 25),
                    np.percentile(sp_crop_df[col], 75),
                )
            return nutrient_range

        # Fetch nutrient ranges for the selected crop
        dict_range = fetch(crop_name)

        if st.button("Recommend Nutrients"):
            st.markdown("### 🧪 Recommended Nutrient Requirements and Conditions")

            with st.expander("🌱 Nitrogen (N)"):
                st.write("Essential for plant growth, particularly for leaf development and green foliage. Helps in chlorophyll synthesis.")
                st.write(f"**Range:** `{dict_range['Nitrogen'][0]:.2f} - {dict_range['Nitrogen'][1]:.2f}`")

            with st.expander("🧪 Phosphorus (P)"):
                st.write("Crucial for root development, flower, and seed production. Involved in energy transfer and photosynthesis.")
                st.write(f"**Range:** `{dict_range['Phosphorus'][0]:.2f} - {dict_range['Phosphorus'][1]:.2f}`")

            with st.expander("🟤 Potassium (K)"):
                st.write("Improves drought resistance, strengthens stems, and enhances overall crop quality.")
                st.write(f"**Range:** `{dict_range['Potassium'][0]:.2f} - {dict_range['Potassium'][1]:.2f}`")

            with st.expander("🌡️ Temperature (°C)"):
                st.write("Affects germination, growth rate, and overall crop yield.")
                st.write(f"**Range:** `{dict_range['Temperature'][0]:.2f} - {dict_range['Temperature'][1]:.2f}`")

            with st.expander("💧 Humidity (%)"):
                st.write("Impacts evapotranspiration and overall plant hydration.")
                st.write(f"**Range:** `{dict_range['Humidity'][0]:.2f} - {dict_range['Humidity'][1]:.2f}`")

            with st.expander("⚗️ pH Value"):
                st.write("Determines nutrient availability and microbial activity in the soil.")
                st.write(f"**Range:** `{dict_range['pH_Value'][0]:.2f} - {dict_range['pH_Value'][1]:.2f}`")

            with st.expander("☔ Rainfall (mm)"):
                st.write("Provides necessary water for crop growth and soil moisture.")
                st.write(f"**Range:** `{dict_range['Rainfall'][0]:.2f} - {dict_range['Rainfall'][1]:.2f}`")


   
    # Feedback Tab
    with feedback_tab:
        st.header("💬 We Value Your Feedback!")
        
        st.write(
            """
            Please provide your feedback by filling out the form below.
            The feedback will be submitted to our Google Form.
            """
        )
        
        # Embed Google Form using HTML
        google_form_url = "https://forms.gle/X72FoTrD74FgB4YN8" 
        form_iframe = f"""
        <iframe src="{google_form_url}" width="640" height="800" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
        """
        st.markdown(form_iframe, unsafe_allow_html=True)
        
        st.write(
            """
            Alternatively, you can open the form in a new tab by clicking [here](https://forms.gle/X72FoTrD74FgB4YN8).
            """
        )
