import asyncio
import smtplib
import uuid
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types
from telegram import Bot

from prompts import (
    SUMMARY_REQUEST_PROMPT,
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
)


# ============================================================
# CONFIG
# ============================================================

MODEL_NAME = "gemini-3.5-flash-lite"

st.set_page_config(
    page_title="GlucoSnap",
    page_icon="🩸",
    layout="wide",
)


# ============================================================
# SECRETS
# ============================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]

TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
TELEGRAM_BOT_USERNAME = st.secrets["TELEGRAM_BOT_USERNAME"]


# ============================================================
# GEMINI
# ============================================================

@st.cache_resource
def get_gemini_client():
    return genai.Client(
        api_key=GEMINI_API_KEY
    )


gemini_client = get_gemini_client()


# ============================================================
# EMAIL
# ============================================================

def send_email(to_address, subject, body):

    message = MIMEText(
        body,
        "plain",
        "utf-8"
    )

    message["Subject"] = subject
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_address

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD
        )

        server.send_message(message)


# ============================================================
# TELEGRAM
# ============================================================

async def telegram_send_async(chat_id, message):

    async with Bot(
        token=TELEGRAM_BOT_TOKEN
    ) as bot:

        await bot.send_message(
            chat_id=chat_id,
            text=message
        )


def send_telegram(chat_id, message):

    max_length = 4000

    chunks = [
        message[i:i + max_length]
        for i in range(
            0,
            len(message),
            max_length
        )
    ]

    for chunk in chunks:

        asyncio.run(
            telegram_send_async(
                chat_id,
                chunk
            )
        )


# ============================================================
# TELEGRAM CONNECTION
# ============================================================

async def get_telegram_updates_async():

    async with Bot(
        token=TELEGRAM_BOT_TOKEN
    ) as bot:

        updates = await bot.get_updates(
            timeout=1,
            allowed_updates=["message"]
        )

        return updates


def get_telegram_updates():

    return asyncio.run(
        get_telegram_updates_async()
    )


def create_telegram_connection():

    token = uuid.uuid4().hex[:16]

    st.session_state.telegram_connection_token = token

    st.session_state.telegram_connected = False

    return token


def check_telegram_connection():

    connection_token = (
        st.session_state.get(
            "telegram_connection_token"
        )
    )

    if not connection_token:
        return None

    updates = get_telegram_updates()

    for update in updates:

        message = update.message

        if not message:
            continue

        text = message.text or ""

        expected_text = (
            f"/start {connection_token}"
        )

        if text.strip() == expected_text:

            chat_id = message.chat.id

            st.session_state.telegram_chat_id = (
                chat_id
            )

            st.session_state.telegram_connected = True

            # Confirm connection
            try:

                send_telegram(
                    chat_id,
                    "✅ Telegram connected to GlucoSnap!\n\n"
                    "Your nutrition summaries can now "
                    "be sent here."
                )

            except Exception:
                pass

            return chat_id

    return None


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(parts):

    try:

        if not parts:
            return (
                "Please send a message or "
                "upload a meal photo."
            )

        response = (
            st.session_state.chat.send_message(
                parts
            )
        )

        return response.text

    except Exception as error:

        error_text = str(error)

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "rate limit" in error_text.lower()
            or "quota" in error_text.lower()
        ):

            return (
                "⚠️ Gemini is temporarily "
                "rate-limited.\n\n"
                "Please wait a little and try again."
            )

        return (
            f"Sorry, something went wrong:\n\n"
            f"{error_text}"
        )


# ============================================================
# CHAT
# ============================================================

def render_message(message):

    with st.chat_message(
        message["role"]
    ):

        if message["kind"] == "text":

            st.write(
                message["content"]
            )

        elif message["kind"] == "image":

            st.image(
                message["content"]
            )


def add_message(
    role,
    kind,
    content
):

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
# INITIAL STATE
# ============================================================

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if "telegram_connected" not in st.session_state:
    st.session_state.telegram_connected = False


# ============================================================
# ONBOARDING
# ============================================================

if not st.session_state.onboarded:

    st.title("GlucoSnap 🩸")

    st.caption(
        "Healthy blood glucose companion"
    )

    with st.form("onboarding_form"):

        name = st.text_input(
            "What's your name?"
        )

        email_address = st.text_input(
            "What's your email address?",
            placeholder="you@example.com"
        )

        submit_button = st.form_submit_button(
            "Continue"
        )

        if submit_button:

            name = name.strip()
            email_address = email_address.strip()

            if not name:

                st.error(
                    "Please enter your name."
                )

            elif (
                "@" not in email_address
                or "." not in email_address
            ):

                st.error(
                    "Please enter a valid email address."
                )

            else:

                st.session_state.name = name

                st.session_state.email_address = (
                    email_address
                )

                st.session_state.chat = (
                    gemini_client.chats.create(
                        model=MODEL_NAME,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT
                        ),
                    )
                )

                st.session_state.messages = []

                st.session_state.onboarded = True

                st.rerun()

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("GlucoSnap 🩸")


# ============================================================
# TELEGRAM CONNECTION
# ============================================================

with st.expander(
    "✈️ Connect Telegram",
    expanded=not st.session_state.telegram_connected
):

    if st.session_state.telegram_connected:

        st.success(
            "Telegram connected ✅"
        )

    else:

        st.write(
            "Connect Telegram once so GlucoSnap "
            "can send your summaries there."
        )

        if st.button(
            "🔗 Create Telegram Connection"
        ):

            token = create_telegram_connection()

            telegram_link = (
                f"https://t.me/"
                f"{TELEGRAM_BOT_USERNAME}"
                f"?start={token}"
            )

            st.session_state.telegram_link = (
                telegram_link
            )

        if "telegram_link" in st.session_state:

            st.link_button(
                "1️⃣ Open Telegram Bot",
                st.session_state.telegram_link
            )

            st.write(
                "In Telegram, press Start. "
                "Then come back here."
            )

            if st.button(
                "2️⃣ Check Telegram Connection"
            ):

                try:

                    chat_id = (
                        check_telegram_connection()
                    )

                    if chat_id:

                        st.success(
                            "Telegram connected successfully! ✅"
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "I haven't received the "
                            "Telegram connection yet. "
                            "Open the bot and press Start, "
                            "then try again."
                        )

                except Exception as error:

                    st.error(
                        f"Telegram connection failed: {error}"
                    )


# ============================================================
# USER INFO
# ============================================================

telegram_status = (
    "Connected ✅"
    if st.session_state.telegram_connected
    else "Not connected"
)

st.caption(
    f"Logged in as {st.session_state.name} "
    f"| Email: {st.session_state.email_address} "
    f"| Telegram: {telegram_status}"
)


# ============================================================
# SEPARATE SEND BUTTONS
# ============================================================

st.subheader("Send your nutrition summary")

email_col, telegram_col = st.columns(2)

send_disabled = (
    len(st.session_state.messages) <= 1
)


# ============================================================
# EMAIL BUTTON
# ============================================================

with email_col:

    if st.button(
        "📧 Send by Email",
        disabled=send_disabled,
        use_container_width=True
    ):

        with st.spinner(
            "Creating summary..."
        ):

            summary = ask_gemini(
                [SUMMARY_REQUEST_PROMPT]
            )

        try:

            send_email(
                st.session_state.email_address,
                "🩸 Your GlucoSnap Nutrition Summary",
                summary
            )

            st.success(
                "Email sent successfully! ✅"
            )

        except Exception as error:

            st.error(
                f"Email failed: {error}"
            )


# ============================================================
# TELEGRAM BUTTON
# ============================================================

with telegram_col:

    telegram_disabled = (
        send_disabled
        or not st.session_state.telegram_connected
    )

    if st.button(
        "✈️ Send by Telegram",
        disabled=telegram_disabled,
        use_container_width=True
    ):

        with st.spinner(
            "Creating summary..."
        ):

            summary = ask_gemini(
                [SUMMARY_REQUEST_PROMPT]
            )

        try:

            send_telegram(
                st.session_state.telegram_chat_id,
                summary
            )

            st.success(
                "Telegram message sent successfully! ✅"
            )

        except Exception as error:

            st.error(
                f"Telegram failed: {error}"
            )


# ============================================================
# CHAT HISTORY
# ============================================================

if not st.session_state.messages:

    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        )
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
        "png"
    ]
)


# ============================================================
# PROCESS INPUT
# ============================================================

if user_input:

    photo = (
        user_input.files[0]
        if user_input.files
        else None
    )

    text = user_input.text

    parts = []


    # --------------------------------------------------------
    # PHOTO
    # --------------------------------------------------------

    if photo is not None:

        photo_bytes = photo.getvalue()

        add_message(
            "user",
            "image",
            photo_bytes
        )

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type
            )
        )


    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    if text:

        add_message(
            "user",
            "text",
            text
        )

        parts.append(text)


    # --------------------------------------------------------
    # PHOTO ONLY
    # --------------------------------------------------------

    elif photo is not None:

        parts.append(
            (
                "Analyze this meal from the image.\n\n"
                "Identify:\n"
                "1. What the meal contains\n"
                "2. Estimated calories\n"
                "3. Estimated protein\n"
                "4. Estimated carbohydrates\n"
                "5. Estimated fat\n\n"
                "Clearly explain that these are estimates."
            )
        )


    # --------------------------------------------------------
    # GEMINI
    # --------------------------------------------------------

    if parts:

        with st.spinner(
            "Crunching the numbers... 🧮"
        ):

            answer = ask_gemini(
                parts
            )

        add_message(
            "assistant",
            "text",
            answer
        )


