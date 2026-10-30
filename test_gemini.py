
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
else:
    client = genai.Client(api_key=api_key)

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents="Explain artificial intelligence in 2 simple sentences."
            )
            print(response.text)
            break
        except errors.APIError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(5)
            else:
                print("Gemini is unavailable right now. Try again later.")
