import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ No API key found in .env file!")
else:
    print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content("Say 'Hello' in Hindi")
        print(f"✓ API key works!")
        print(f"Test response: {response.text}")
    except Exception as e:
        print(f"❌ API key doesn't work: {e}")