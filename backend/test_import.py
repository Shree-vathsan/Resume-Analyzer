# backend/test_import.py
import sys
import os

print("--- sys.path ---")
for p in sys.path:
    print(p)
print("----------------")

try:
    import google
    print("Successfully imported 'google'")
    print(f"Path of 'google' package: {google.__path__}")
except ImportError as e:
    print(f"FAILED to import 'google': {e}")
    print("Please ensure 'google-generativeai' is installed in the active virtual environment.")

print("\n--- Testing google.generativeai ---")
try:
    import google.generativeai as genai
    print("Successfully imported 'google.generativeai'")
    # Ensure you have a GEMINI_API_KEY in your backend/.env
    # or set it here for the test, but DO NOT commit your real key
    # genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_DUMMY_API_KEY_HERE"))
    # Using a dummy key here to avoid dependency on .env for just testing import
    genai.configure(api_key="sk-AbCDEFGHIjKLMnoPQRSTUVWXYZ0123456789")
    print("genai.configure called (dummy key)")
except ImportError as e:
    print(f"FAILED to import 'google.generativeai': {e}")
except Exception as e:
    print(f"Other error with google.generativeai: {e}")

print("\n--- Script finished ---")