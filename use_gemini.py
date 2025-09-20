import google.generativeai as genai

def use_gemini(prompt):
    try:
        genai.configure(api_key="AIzaSyBN7rug51EVTphC3uSOzNFj66LwAHGmEGQ")
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        print(f"Gemini API 오류: {e}")
        return None