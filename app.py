import json

import streamlit as st
from google import genai
from google.genai import types
from twilio.rest import Client

from prompts import (
    SUMMARY_REQUEST_PROMPT,
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-3.5-flash-lite"


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="GlucoSnap",
    page_icon="🩸",
    layout="wide",
)


# ============================================================
# API KEYS / SECRETS
# ============================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FROM = st.secrets["TWILIO_WHATSAPP_FROM"]
TWILIO_CONTENT_SID = st.secrets["TWILIO_CONTENT_SID"]


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_gemini_client():
    return genai.Client(
        api_key=GEMINI_API_KEY
    )


gemini_client = get_gemini_client()


# ============================================================
# TWILIO CLIENT
# ============================================================

@st.cache_resource
def get_twilio_client():
    return Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN
    )


twilio_client = get_twilio_client()


# ============================================================
# CHAT DISPLAY
# ============================================================

def render_message(message):

    with st.chat_message(message["role"]):

        if message["kind"] == "text":
            st.write(message["content"])

        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):

    st.session_state.messages.append(
        {
            "role": role,
            "kind": kind,
            "content": content,
        }
    )

    render_message(
        st.session_state.messages[-1]
    )


# ============================================================
# GEMINI REQUEST
# ============================================================

def ask_gemini(parts):

    try:

        if not parts:
            return "Please send a message or upload a meal photo."

        response = st.session_state.chat.send_message(parts)

        return response.text

    except Exception as error:

        error_text = str(error)

        # Handle Gemini rate limits
        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "rate limit" in error_text.lower()
            or "quota" in error_text.lower()
        ):
            return (
                "⚠️ Gemini is temporarily rate-limited.\n\n"
                "Please wait a little and try again."
            )

        return (
            f"Sorry, something went wrong:\n\n"
            f"{error_text}"
        )


# ============================================================
# WHATSAPP TEXT CLEANING
# ============================================================

def clean_whatsapp_text(text):

    if not text:
        return "No nutrition summary available."

    text = " ".join(text.split())

    if len(text) > 1500:
        return text[:1500] + "..."

    return text


# ============================================================
# SEND WHATSAPP
# ============================================================

def send_whatsapp(to_number, user_name, summary):

    try:

        # Twilio Content Template:
        # {{1}} = user name
        # {{2}} = nutrition summary

        content_variables = json.dumps(
            {
                "1": user_name,
                "2": clean_whatsapp_text(summary),
            },
            ensure_ascii=False,
        )

        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to_number}",
            content_sid=TWILIO_CONTENT_SID,
            content_variables=content_variables,
        )

        return True, message.sid

    except Exception as error:

        return False, str(error)


# ============================================================
# ONBOARDING
# ============================================================

if "onboarded" not in st.session_state:

    st.session_state.onboarded = False


if not st.session_state.onboarded:

    st.title("GlucoSnap 🩸")

    st.caption(
        "Healthy blood glucose companion"
    )

    with st.form("onboarding_form"):

        name = st.text_input(
            "What's your name?"
        )

        whatsapp_number = st.text_input(
            "What's your WhatsApp number?",
            placeholder="+91xxxxxxxxxx",
            help=(
                "Include your country code. "
                "Example: +91XXXXXXXXXX"
            ),
        )

        submit_button = st.form_submit_button(
            "Submit"
        )

        if submit_button:

            if not name or not whatsapp_number:

                st.error(
                    "Please fill in both your name "
                    "and WhatsApp number."
                )

            else:

                # Save user information
                st.session_state.name = name

                st.session_state.whatsapp_number = (
                    whatsapp_number
                )

                # Create Gemini chat
                st.session_state.chat = (
                    gemini_client.chats.create(
                        model=MODEL_NAME,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT
                        ),
                    )
                )

                # Initialize messages
                st.session_state.messages = []

                # Mark onboarding completed
                st.session_state.onboarded = True

                st.success(
                    f"Thanks {name}! "
                    "You're all set to use GlucoSnap 🩸."
                )

                st.rerun()

    st.stop()


# ============================================================
# MAIN CHAT INTERFACE
# ============================================================

header_col, button_col = st.columns(
    [5, 2],
    vertical_alignment="center"
)


# ============================================================
# HEADER
# ============================================================

with header_col:

    st.title("GlucoSnap 🩸")


# ============================================================
# WHATSAPP BUTTON
# ============================================================

with button_col:

    send_disabled = (
        len(st.session_state.messages) <= 1
    )

    if st.button(
        "📤 Send to WhatsApp",
        disabled=send_disabled,
        use_container_width=True,
    ):

        with st.spinner(
            "Summarizing your day..."
        ):

            summary = ask_gemini(
                [SUMMARY_REQUEST_PROMPT]
            )

        success, info = send_whatsapp(
            st.session_state.whatsapp_number,
            st.session_state.name,
            summary,
        )

        if success:

            st.success(
                "Sent! Check your WhatsApp 📲"
            )

        else:

            st.error(
                f"Couldn't send that: {info}"
            )


# ============================================================
# USER ACCOUNT INFO
# ============================================================

st.caption(
    f"Logged in as {st.session_state.name} "
    f"- updates go to "
    f"{st.session_state.whatsapp_number}"
)


# ============================================================
# DISPLAY EXISTING CHAT
# ============================================================

if not st.session_state.messages:

    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        ),
    )

else:

    for message in st.session_state.messages:

        render_message(message)


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal",
    accept_file=True,
    file_type=[
        "jpg",
        "jpeg",
        "png",
    ],
)


# ============================================================
# PROCESS NEW USER MESSAGE
# ============================================================

if user_input:

    # --------------------------------------------------------
    # Get uploaded photo
    # --------------------------------------------------------

    photo = (
        user_input.files[0]
        if user_input.files
        else None
    )

    # --------------------------------------------------------
    # Get text
    # --------------------------------------------------------

    text = user_input.text

    # --------------------------------------------------------
    # Gemini content
    # --------------------------------------------------------

    parts = []


    # --------------------------------------------------------
    # PHOTO
    # --------------------------------------------------------

    if photo is not None:

        photo_bytes = photo.getvalue()

        # Display uploaded image
        add_message(
            "user",
            "image",
            photo_bytes,
        )

        # Send image to Gemini
        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type,
            )
        )


    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    if text:

        add_message(
            "user",
            "text",
            text,
        )

        parts.append(text)


    # --------------------------------------------------------
    # PHOTO WITHOUT TEXT
    # --------------------------------------------------------

    elif photo is not None:

        parts.append(
            (
                "Analyze this meal from the image. "
                "Identify the food and estimate:\n"
                "1. What the meal contains\n"
                "2. Calories\n"
                "3. Protein\n"
                "4. Carbohydrates\n"
                "5. Fat\n\n"
                "Clearly state that the nutrition values "
                "are estimates."
            )
        )


    # --------------------------------------------------------
    # CALL GEMINI ONLY WHEN THERE IS INPUT
    # --------------------------------------------------------

    if parts:

        with st.spinner(
            "Crunching the numbers... 🧮"
        ):

            answer = ask_gemini(parts)

        add_message(
            "assistant",
            "text",
            answer,
        )
