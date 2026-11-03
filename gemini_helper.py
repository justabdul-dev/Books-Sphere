import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Check API key
if not API_KEY:
    raise ValueError("Gemini API key not found in .env file")

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

import time

def ask_gemini(question):

    for attempt in range(3):

        try:
            response = client.interactions.create(
                model="gemini-3.8-flash",
                input=question
            )

            return response.output_text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue

            return f"Gemini Error: {e}"

    return "Gemini is temporarily unavailable. Please try again."
