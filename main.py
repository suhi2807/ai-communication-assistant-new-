from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Communication Assistant Running Successfully"}

@app.post("/improve")
def improve(text: dict):

    user_text = text["text"]
    result = f"Could you please {user_text.lower()}?"

    return {"result": result}


@app.post("/analyze")
def analyze(text: dict):

    return {"result": "Tone: Neutral"}


@app.post("/reply")
def reply(text: dict):

    return {"result": "Sure, I will handle it shortly."}