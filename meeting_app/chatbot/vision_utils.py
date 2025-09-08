# chatbot/vision_utils.py
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()  


def gemini_vision_response(image_path, prompt="Explain this image."):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        image = Image.open(image_path)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return f"Sorry, I couldn't analyze the image. Error: {str(e)}"
