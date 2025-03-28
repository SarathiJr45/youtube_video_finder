import google.generativeai as genai
from config import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)

def analyze_titles_with_gemini(video_titles):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""
    You are an AI that evaluates YouTube video titles based on their relevance and engagement.
    Given the following titles, choose the best one and explain why:

    {video_titles}

    Return the best title along with its reasoning.
    """
    
    response = model.generate_content(prompt)
    return response.text
