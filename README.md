# GlucoSnap 🩸

> **Your AI-powered blood glucose companion and meal analyzer.**

GlucoSnap is an interactive, multimodal health assistant designed to help individuals understand their blood glucose readings, analyze food choices, and estimate glycemic impact. Powered by **Google Gemini** and **Streamlit**, with instant daily summaries delivered directly to **WhatsApp via Twilio**.

---

## 🌟 Key Features

- **📸 Multimodal Meal Analysis**: Upload photos of your meals to receive instant estimates for:
  - Food & ingredient breakdown
  - Estimated Carbohydrates & Calories
  - Macronutrients (Protein, Fat)
  - Potential blood glucose impact (Lower, Moderate, or Higher impact)
  - Practical suggestions to make meals more glucose-friendly
- **🩸 Glucose Context & Tracking**: Log and discuss blood glucose readings across different contexts (fasting, pre-meal, post-prandial, random) with simple, educational explanations.
- **📲 One-Click WhatsApp Summaries**: Generate a concise, WhatsApp-optimized summary of your logged meals, glucose readings, and dietary patterns, and send it straight to your phone.
- **🛡️ Built-in Safety Guardrails**: Follows strict safety rules—focusing on nutrition education and habit awareness without diagnosing conditions or prescribing medical dosages.
- **⚡ Error & Rate-Limit Handling**: Gracefully handles Gemini API rate limits and connection issues with intuitive user feedback.

---

## 🏗️ Architecture & Tech Stack

```
                                +---------------------------+
                                |      User / Browser       |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                |   Streamlit Frontend UI   |
                                |         (app.py)          |
                                +------+--------------+-----+
                                       |              |
                      (Multimodal Chat)|              |(WhatsApp Summary)
                                       v              v
               +-------------------------+          +-------------------------+
               |   Google Gemini Model   |          |    Twilio REST API      |
               | (gemini-3.5-flash-lite) |          |  (WhatsApp Messaging)   |
               +-------------------------+          +-------------------------+
                                                              |
                                                              v
                                                    +-------------------+
                                                    |  User's WhatsApp  |
                                                    +-------------------+
```

- **Frontend & UI**: [Streamlit](https://streamlit.io/)
- **AI / LLM Engine**: [Google GenAI SDK](https://github.com/googleapis/python-genai) (`gemini-3.5-flash-lite`)
- **Messaging Integration**: [Twilio REST API](https://www.twilio.com/docs/whatsapp) (Content Templates)
- **Language**: Python 3.10+

---

## 📁 Project Structure

```text
GlucoSnap/
├── .streamlit/
│   └── secrets.toml          # API keys & Twilio configuration (local/private)
├── app.py                    # Main Streamlit web application & session management
├── prompts.py                # System instructions, welcome message, & summary prompts
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusions (secrets, venv, cache)
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher installed on your system
- A [Google AI Studio API Key](https://aistudio.google.com/)
- A [Twilio Account](https://www.twilio.com/) with WhatsApp Sandbox / Business Messaging enabled

### 2. Clone the Repository

```bash
git clone https://github.com/balaji-nalam/GlucoSnap.git
cd GlucoSnap
```

### 3. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.streamlit/secrets.toml` file in the root directory:

```toml
# Google Gemini API Key
GEMINI_API_KEY = "your_google_gemini_api_key_here"

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID = "your_twilio_account_sid_here"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token_here"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"  # Example: Twilio Sandbox number
TWILIO_CONTENT_SID = "your_twilio_content_template_sid_here"
```

> ⚠️ **Security Warning**: Never commit `.streamlit/secrets.toml` to version control. It is already included in `.gitignore`.

### Twilio Content Template Variables
If using a Twilio Content Template with variables:
- `{{1}}`: User Name
- `{{2}}`: Summarized Nutrition and Glucose Insights

---

## 💻 Running the Application

Launch the Streamlit web server:

```bash
streamlit run app.py
```

Once started, open your browser and navigate to `http://localhost:8501`.

---

## 📖 How It Works

1. **Onboarding**: Enter your name and WhatsApp number (with international country code, e.g., `+91XXXXXXXXXX`).
2. **Chat & Inquire**:
   - Type questions regarding blood glucose ranges, food substitutions, or general nutrition.
   - Enter your readings (e.g., *"My fasting glucose was 110 mg/dL today"*).
3. **Upload Meal Photos**: Use the camera/file attachment button to upload images of your food (`.jpg`, `.jpeg`, `.png`). GlucoSnap will detect the food items and estimate carbs, calories, and glucose impact.
4. **Send to WhatsApp**: Click the **📤 Send to WhatsApp** button in the header at any time to receive a mobile summary of your session.

---

## ⚠️ Medical Disclaimer

> **IMPORTANT**: GlucoSnap is an educational and informational tool powered by artificial intelligence. It **does not** provide medical advice, diagnosis, or treatment plans. Nutrition estimates from photographs are approximate. Users should always consult qualified healthcare professionals or their physician regarding any medical conditions, medication management, or insulin dosage adjustments. In emergencies or severe hypoglycemia/hyperglycemia symptoms, seek urgent medical care immediately.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) (or your preferred license).
