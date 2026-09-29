# GlucoSnap 🩸

> **Your AI-powered blood glucose companion and meal analyzer.**

GlucoSnap is an interactive, multimodal health assistant built with **Streamlit** and **Google Gemini**. It helps users track and understand blood glucose readings, analyzes meal photos to estimate carbohydrates, calories, and macronutrients, and delivers detailed daily summaries directly via **Gmail** and **Telegram**.

---

## 🌟 Key Features

- **📸 Multimodal Meal Analysis**: Upload food photos (`.jpg`, `.jpeg`, `.png`) to receive instant estimates for:
  - Ingredients and food breakdown
  - Estimated Carbohydrates & Calories
  - Macronutrients (Protein, Fat)
  - Potential blood glucose impact (Lower, Moderate, or Higher impact)
  - Practical suggestions to make meals more glucose-friendly
- **🩸 Glucose Context & Tracking**: Log and discuss blood glucose readings across different contexts (fasting, pre-meal, post-meal, random) with simple, educational explanations.
- **📧 Gmail Summary Delivery**: Send your complete daily nutrition and glucose recap to your email with a single click using secure Gmail SMTP.
- **✈️ Seamless Telegram Integration**: Connect your Telegram account automatically via deep link (no manual Chat ID entry needed) and receive instant summaries in your Telegram chat.
- **🛡️ Built-in Safety Guardrails**: Follows strict non-diagnostic guidelines—focusing on nutrition education and habit awareness without prescribing medications or replacing doctors.
- **⚡ Rate-Limit Resilience**: Gracefully manages Gemini API rate limits (`RESOURCE_EXHAUSTED` / 429) with friendly user notifications.

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
                      (Multimodal Chat)|              |(Summary Delivery)
                                       v              +--------------------+
               +-------------------------+            |                    |
               |   Google Gemini Model   |            v                    v
               | (gemini-3.5-flash-lite) |    +---------------+    +---------------+
               +-------------------------+    |  Gmail SMTP   |    | Telegram Bot  |
                                              |  (Port 465)   |    |      API      |
                                              +-------+-------+    +-------+-------+
                                                      |                    |
                                                      v                    v
                                                User's Inbox         User's Telegram
```

- **Frontend & UI**: [Streamlit](https://streamlit.io/)
- **AI / LLM Engine**: [Google GenAI SDK](https://github.com/googleapis/python-genai) (`gemini-3.5-flash-lite`)
- **Email Delivery**: Python standard library `smtplib` (Gmail SMTP over SSL)
- **Telegram Bot**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (Telegram Bot API)
- **Language**: Python 3.10+

---

## 📁 Project Structure

```text
GlucoSnap/
├── .streamlit/
│   └── secrets.toml          # API keys & configuration secrets (local only)
├── app.py                    # Main Streamlit web application & session management
├── prompts.py                # System instructions, welcome message, & summary prompts
├── requirements.txt          # Runtime Python dependencies
├── .gitignore                # Git exclusions (secrets, venv, cache)
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher installed on your system
- A [Google AI Studio API Key](https://aistudio.google.com/)
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) enabled
- A Telegram Bot created via [@BotFather](https://t.me/botfather)

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

Create a `.streamlit/secrets.toml` file in the project root:

```toml
# Google Gemini API Key
GEMINI_API_KEY = "your_google_gemini_api_key_here"

# Gmail SMTP Configuration
GMAIL_ADDRESS = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_gmail_16_char_app_password"

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_BOT_USERNAME = "your_telegram_bot_username"
```

> ⚠️ **Security Warning**: Never commit `.streamlit/secrets.toml` or API keys to GitHub. It is protected by `.gitignore`.

---

## 💻 Running the Application

Launch the Streamlit web server:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📖 How It Works

1. **Onboarding**: Enter your name and email address to begin.
2. **Connect Telegram (Optional)**: Click **Create Telegram Connection**, open the bot in Telegram, and hit **Start**. The app automatically detects your connection without requiring you to look up your chat ID.
3. **Chat & Inquire**:
   - Ask questions about food choices, carb counting, or blood glucose readings.
   - Mention your readings (e.g., *"Fasting glucose was 105 mg/dL"*).
4. **Upload Meal Photos**: Attach photos of your meals (`.jpg`, `.jpeg`, `.png`) for automated food identification and nutrition estimation.
5. **Send Nutrition Summary**:
   - Click **📧 Send by Email** to receive your session summary in your inbox.
   - Click **✈️ Send by Telegram** to receive the same summary in your Telegram chat.

---

## ⚠️ Medical Disclaimer

> **IMPORTANT**: GlucoSnap is an educational and informational tool powered by artificial intelligence. It **does not** provide medical advice, diagnosis, or treatment plans. Nutrition estimates from photographs are approximate. Users should always consult qualified healthcare professionals or their physician regarding any medical conditions, medication management, or insulin dosage adjustments. In emergencies or severe hypoglycemia/hyperglycemia symptoms, seek urgent medical care immediately.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
