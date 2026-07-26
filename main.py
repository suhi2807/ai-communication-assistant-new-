from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os

# Load .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI(title="AI Communication Assistant")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "status": "Running",
        "message": "AI Communication Assistant Backend"
    }


def ask_ai(prompt):

    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional AI Communication Assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        if response.status_code != 200:
            return f"Groq Error:\n{result}"

        if "error" in result:
            return result["error"]["message"]

        if "choices" not in result:
            return str(result)

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)


@app.post("/analyze")
def analyze(msg: Message):

    prompt = f"""
Analyze the following message.

Message:
{msg.text}

Give the answer in this format.

Tone:

Reason:

Intent:

Suggestion:

Sentiment:
"""

    return {
        "result": ask_ai(prompt)
    }


@app.post("/improve")
def improve(msg: Message):

    prompt = f"""
Rewrite this message professionally.

Keep the meaning same.

Message:

{msg.text}
"""

    return {
        "result": ask_ai(prompt)
    }


@app.post("/reply")
def reply(msg: Message):

    prompt = f"""
Write a professional reply for this message.

Message:

{msg.text}
"""

    return {
        "result": ask_ai(prompt)
    }


@app.post("/sentiment")
def sentiment(msg: Message):

    prompt = f"""
You are an expert sentiment classifier.

Your task is to classify the message into EXACTLY ONE of these categories:

POSITIVE
NEGATIVE
NEUTRAL

Rules:

1. Work-related requests, reminders, instructions, questions, deadlines, follow-ups and informational messages are ALWAYS NEUTRAL.

Examples:
- Please send me the report by today.
- Can you share the meeting link?
- Kindly update the document.
- Submit the assignment before 5 PM.
- Let's schedule a meeting tomorrow.

These are NOT negative.

2. Messages expressing gratitude, appreciation, happiness, congratulations or encouragement are POSITIVE.

Examples:
- Thank you so much!
- Great work!
- Excellent presentation!
- I'm happy with the results.

3. Messages expressing anger, frustration, disappointment, blame, insults, complaints or threats are NEGATIVE.

Examples:
- I'm very disappointed.
- This is unacceptable.
- Your work is terrible.
- I am frustrated with this delay.

Return ONLY ONE WORD.

Either

POSITIVE

or

NEGATIVE

or

NEUTRAL

Message:

{msg.text}
"""

    result = ask_ai(prompt).strip().upper()

    if "POSITIVE" in result:
        result = "POSITIVE"

    elif "NEGATIVE" in result:
        result = "NEGATIVE"

    elif "NEUTRAL" in result:
        result = "NEUTRAL"

    else:
        result = "NEUTRAL"

    return {"result": result}