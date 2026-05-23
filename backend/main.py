from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests
import os
from dotenv import load_dotenv
from backend.attack_logger import log_attack

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("BACKEND LOADED")


# ====================
# Models
# ====================

class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    message: str


# ====================
# Login
# ====================

def authenticate_user(username, password):

    with open("data/users.json", "r") as f:

        users = json.load(f)

    for user in users:

        if (
            user["username"] == username
            and
            user["password"] == password
        ):

            return {

                "success": True,
                "role": user["role"]

            }

    return {

        "success": False

    }


@app.post("/login")
def login(req: LoginRequest):

    return authenticate_user(
        req.username,
        req.password
    )


# ====================
# Chat
# ====================

@app.post("/chat")
def chat(req: ChatRequest):

    print("\nMESSAGE RECEIVED:")
    print(req.message)

    # Attack detection
    if "ignore previous instructions" in req.message.lower():

        print("ATTACK DETECTED")

        print("CALLING LOGGER")

        log_attack(
            "hari",
            req.message,
            "Prompt Injection"
        )

        print("LOGGER FINISHED")

        return {

            "response":
            "⚠️ Security policy triggered"

        }


    # Normal chatbot flow

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {

        "Authorization":
        f"Bearer {GROQ_API_KEY}",

        "Content-Type":
        "application/json"
    }

    payload = {

        "model": "llama-3.3-70b-versatile",

        "messages": [

            {
                "role": "system",
                "content": "You are a secure AI assistant."
            },

            {
                "role": "user",
                "content": req.message
            }

        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    result = response.json()

    return {

        "response":
        result["choices"][0]["message"]["content"]

    }


@app.get("/")
def home():

    return {

        "message":
        "Backend running"

    }