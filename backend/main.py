from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
from dotenv import load_dotenv
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#  API KEYS
load_dotenv()
GROQ_API_KEY =os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


#  TEXT AI (Groq Chat)
def ask_groq(prompt):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        if "choices" not in result:
            return f"Groq Error: {result}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)


#  Convert image to base64
def image_to_base64(file):
    image_data = file.file.read()
    return base64.b64encode(image_data).decode("utf-8")


#  IMAGE AI (Groq Vision)
def ask_vision(prompt, image_file):
    try:
        base64_image = image_to_base64(image_file)

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        if "choices" not in result:
            return f"Vision Error: {result}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)


#  LIVE CURRENT AFFAIRS
def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={NEWS_API_KEY}"

        response = requests.get(url)

        data = response.json()
        print(data)
        if "articles" not in data:
            return str(data)

        articles = data["articles"][:5]

        news = ""

        for i, article in enumerate(articles):
            title = article.get("title", "No title")
            news += f"{i+1}. {title}\n"

        return news

    except Exception as e:
        return str(e)


#  MAIN CHAT ROUTE
@app.post("/chat")
async def chat(
    text: str = Form(""),
    image: UploadFile = File(None)
):
    try:

        #  ONLY TEXT
        if text and not image:
            reply = ask_groq(text)
            return {"reply": reply}

        #  ONLY IMAGE
        elif image and not text:
            reply = ask_vision("Describe this image", image)
            return {"reply": reply}

        # TEXT + IMAGE
        elif text and image:
            reply = ask_vision(text, image)
            return {"reply": reply}

        else:
            return {"reply": "Please type message or upload image"}

    except Exception as e:
        return {"reply": str(e)}


#  CURRENT AFFAIRS ROUTE
@app.get("/news")
def news():
    return {
        "news": get_news()
    }


#  HOME ROUTE
@app.get("/")
def home():
    return {
        "message": "AI Backend Running "
    }













