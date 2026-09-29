# GlucoSnap — Project Context

## Project Overview

GlucoSnap is an AI-powered nutrition and healthy blood glucose companion built with Streamlit and Google Gemini.

The application allows a user to:

1. Enter their name and email address.
2. Chat with an AI nutrition assistant.
3. Upload meal photos.
4. Ask nutrition-related questions.
5. Get estimated calories and macronutrients.
6. Send a generated nutrition summary by Email.
7. Connect Telegram and send the same summary through Telegram.

## Current Technology Stack

* Python
* Streamlit
* Google Gemini API
* `google-genai`
* Gmail SMTP using Python standard library
* Telegram Bot API
* `python-telegram-bot`

## Main Files

### `app.py`

Main Streamlit application.

Responsibilities:

* Streamlit UI
* User onboarding
* Gemini chat
* Meal photo upload
* Nutrition analysis
* Gmail delivery
* Telegram connection
* Telegram summary delivery
* Session state management

### `prompts.py`

Contains:

* `SYSTEM_PROMPT`
* `SUMMARY_REQUEST_PROMPT`
* `WELCOME_MESSAGE_TEMPLATE`

Do not remove these imports unless the prompt architecture is intentionally changed.

### `requirements.txt`

Contains the runtime Python dependencies required by the application.

Current expected dependencies:

* streamlit
* google-genai
* python-telegram-bot

## Gemini

Current model:

```python
MODEL_NAME = "gemini-3.5-flash-lite"
```

Gemini is used for:

* Nutrition conversations
* Meal photo analysis
* Calories estimation
* Protein estimation
* Carbohydrate estimation
* Fat estimation
* Daily nutrition summaries

Do not make unnecessary Gemini API calls because API quota/rate limits may apply.

## Email

Gmail SMTP is used instead of Twilio.

The application uses:

```python
smtplib
```

with:

```text
smtp.gmail.com
port 465
SSL
```

Required secrets:

```toml
GMAIL_ADDRESS = "..."
GMAIL_APP_PASSWORD = "..."
```

The normal Gmail account password must never be used.

## Telegram

Telegram is used as a second delivery channel.

Required secret:

```toml
TELEGRAM_BOT_TOKEN = "..."
```

The Telegram bot username is also configured:

```toml
TELEGRAM_BOT_USERNAME = "..."
```

Users should NOT manually enter their Telegram chat ID.

The intended flow is:

```text
GlucoSnap
    ↓
Create Telegram connection
    ↓
Open Telegram bot
    ↓
User presses Start
    ↓
Application receives Telegram update
    ↓
Chat ID is captured automatically
    ↓
Telegram becomes connected
```

Once connected, the user can use:

```text
📧 Send by Email
✈️ Send by Telegram
```

## User Experience

Initial onboarding:

```text
Name
Email
Continue
```

Then:

```text
Connect Telegram
```

After Telegram connection:

```text
📧 Send by Email
✈️ Send by Telegram
```

Meal input supports:

* Text
* JPG
* JPEG
* PNG

## Security

Never commit:

```text
.streamlit/secrets.toml
.env
API keys
Gemini keys
Gmail App Passwords
Telegram Bot Tokens
```

Secrets are configured separately in Streamlit Cloud.

Expected Streamlit secrets:

```toml
GEMINI_API_KEY = "..."
GMAIL_ADDRESS = "..."
GMAIL_APP_PASSWORD = "..."
TELEGRAM_BOT_TOKEN = "..."
TELEGRAM_BOT_USERNAME = "..."
```

## Local Development

Create/activate the virtual environment and install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the application:

```powershell
streamlit run app.py
```

## Git Workflow

Before committing:

```powershell
git status
```

Verify that secrets are not staged.

Then:

```powershell
git add .
git commit -m "Update GlucoSnap"
git push
```

## Deployment

The application is intended to run on Streamlit Community Cloud.

The GitHub repository contains source code only.

Secrets must be configured separately in Streamlit Cloud.

## Important Development Rules

* Preserve existing working functionality when making changes.
* Do not expose secrets in source code.
* Do not require users to manually find their Telegram chat ID.
* Keep Email and Telegram as separate delivery actions.
* Avoid unnecessary Gemini API requests.
* Maintain the existing Streamlit session-state architecture unless there is a clear reason to change it.
* Test the application locally before pushing changes.
* Update `requirements.txt` whenever a new Python package is introduced.

## Current Working Features

* Streamlit onboarding
* Gemini AI chat
* Meal photo upload
* Nutrition analysis
* Calories estimation
* Macro estimation
* Gmail summary delivery
* Telegram connection flow
* Telegram summary delivery
* Separate Email and Telegram buttons
* Streamlit Cloud deployment
