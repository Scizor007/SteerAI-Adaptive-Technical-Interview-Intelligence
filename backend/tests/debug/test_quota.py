import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Testing Gemini API access...")
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content('Say hello in one word')
    print(f'✓ SUCCESS: {response.text}')
    print(f'✓ Model gemini-2.0-flash is accessible')
except Exception as e:
    print(f'✗ ERROR: {e}')
