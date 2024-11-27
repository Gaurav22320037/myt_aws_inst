# 🌾 Crop & Nutrient Recommendation System

This project provides a user-friendly web application that assists farmers and agricultural enthusiasts in making informed decisions about crop selection and nutrient requirements. The system uses soil nutrient data, weather conditions, and a machine learning model to recommend the most suitable crop for a given field and predict the optimal nutrient levels for selected crops.

---

## 🚀 Features

- **Crop Prediction:** Recommends the best crop based on soil nutrients, weather conditions, and rainfall.
- **Nutrient Recommendation:** Provides nutrient range recommendations for specific crops to optimize yield.
- **Weather Data Integration:** Fetches real-time weather data (temperature and humidity) using the OpenWeatherMap API.
- **User Authentication:** Login/Signup system with secure password hashing.
- **Feedback System:** Collects user feedback and displays it within the app.
- **Interactive UI:** Intuitive interface powered by Streamlit for seamless user experience.

---

## 🖥 Technologies Used

| Component              | Technology/Library                             |
|-------------------------|-----------------------------------------------|
| **Frontend**           | Streamlit (Python-based web framework)       |
| **Backend**            | SQLite (for user authentication and feedback)|
| **Machine Learning**   | Random Forest Classifier, Nutrient range estimation |
| **API**                | OpenWeatherMap API (for weather forecasting) |
| **Python Libraries**   | Pandas, NumPy, Scikit-learn, bcrypt, hashlib, Requests |

---

## 📁 Project Structure

```
Crop_Nutrient_Recommendation/
├── app.py                       # Main Streamlit application
├── best_rfc.pkl                 # Trained Random Forest Classifier model
├── scaler.pkl                   # StandardScaler object for preprocessing
├── users.db                     # SQLite database for user authentication
├── feedback.csv                 # CSV file to store feedback data
├── images/
│   └── farmer.jpg               # Background image for the app
├── Crop_Recommendation.csv      # Dataset used for nutrient range prediction
└── README.md                    # Project documentation
```

---

## ⚙ Setup Instructions

### Prerequisites

- Python 3.8 or later
- Streamlit installed (`pip install streamlit`)
- API Key for OpenWeatherMap (sign up at [OpenWeatherMap](https://openweathermap.org/))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maliabhi23/myt_aws_inst.git
   cd crop-nutrient-recommendation
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your OpenWeatherMap API key:
   - Replace `API_KEY` in `app.py` with your OpenWeatherMap API key.

4. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 📊 Dataset Details

| Feature             | Description                                      |
|----------------------|--------------------------------------------------|
| **Soil Nutrients**  | Nitrogen (N), Phosphorus (P), Potassium (K)      |
| **Environmental**   | Temperature (°C), Humidity (%), pH, Rainfall (mm)|
| **Target**          | Crop (21 classes)                               |

- **Dataset Name:** Crop_Recommendation.csv

---

## 🌐 Live Demo

Link to your hosted application (if applicable): [Crop & Nutrient Recommendation System](#)

---

## 🛠 Future Enhancements

- Add advanced nutrient optimization based on real-time soil testing.
- Integrate satellite-based soil monitoring for large-scale recommendations.
- Enable multilingual support for wider accessibility.

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test thoroughly.
4. Submit a pull request with a detailed description of the changes.

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

- OpenWeatherMap API for weather data
- Streamlit for the amazing web framework
- Dataset creators for providing high-quality agricultural data use
