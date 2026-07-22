import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# testing our model
# ///////////////////////////////////
print("=" * 50)
print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))
print("=" * 50)
# /////////////////////////////////

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-3.1-flash-lite")


def ask_ai(prompt: str):

    response = model.generate_content(prompt)

    if hasattr(response, "text"):
        return response.text

    return "Sorry, I couldn't generate a response."