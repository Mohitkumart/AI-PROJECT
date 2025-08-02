# 🧭 AI - Trip Planner Application

This is an AI-powered trip planner that helps users plan travel itineraries using various intelligent tools and APIs.

---

## 📦 Environment Setup

Create a `.env` file in the root directory with the following content:

```env
GROQ_API_KEY = ""
TAVILY_API_KEY =""
LANGSMITH_API_KEY = ""
GOOGLE_API_KEY = ""
GPLACE_API_KEY = ""  # for real-time places
FOURSQUARE_API_KEY = "" # if GPLACE key is not available
EXCHANGE_RATE_API_KEY = ""
OPENWEATHERMAP_API_KEY = ""
```

Make sure you replace `""` with your actual API keys.

---

## 🚀 Run the Application

Use the following commands to start both the Streamlit frontend and the FastAPI backend:

### ▶️ Start the Streamlit App:

```bash
streamlit run .\streamlit_app.py
```

### 🌐 Start the FastAPI Backend Server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📚 Features

- 🌍 Destination recommendation
- ☁️ Weather forecasts
- 💱 Currency exchange rate support
- 📍 Real-time place lookups (Google Places or Foursquare)
- 📅 Itinerary creation
- 🧠 AI-generated travel plans using GROQ, Tavily, and LangChain agents

---

## ✅ Requirements

Ensure the following Python packages are installed (use `requirements.txt` if provided):

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributions

Feel free to fork, improve, and send a pull request!

---


"llama3-8b-8192"