from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_image(file_path):
    try:
        print("🔹 Starting OCR process...")

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        print("🔹 Creating Gemini client...")
        client = genai.Client(api_key=api_key)

        print("🔹 Checking file path...")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"🔹 Reading file: {file_path}")

        print("🔹 Uploading file to Gemini...")
        uploaded_file = client.files.upload(file=file_path)

        print("🔹 File uploaded successfully")
        print("🔹 Sending request to Gemini model...")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Extract all text from this image exactly as written.",
                uploaded_file
            ]
        )

        print("🔹 Response received from Gemini")

        return response.text

    except FileNotFoundError as e:
        print("❌ File Error:", e)
        return ""

    except ValueError as e:
        print("❌ Environment Error:", e)
        return ""

    except Exception as e:
        print("❌ Unexpected Error:", e)
        return ""


# Test
file_path = "./sample_text_image.jpg"

print("🔹 Calling OCR function...\n")
text = extract_text_from_image(file_path)

print("\n🔹 Extracted Text:")
print(text)