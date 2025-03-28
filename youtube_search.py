import os
import googleapiclient.discovery
import googleapiclient.errors
import speech_recognition as sr
from gemini_analyze import analyze_titles_with_gemini
from config import YOUTUBE_API_KEY


def search_youtube(query):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=20,  # Increased to 20
        type="video",
        publishedAfter="2024-03-13T00:00:00Z",  # Last 14 days
        videoDuration="medium"  # 4-20 minutes
    )
    
    response = request.execute()
    
    videos = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": url})
    
    return videos


def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say your search query (English/Hindi):")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language="hi-IN")  # Added Hindi support
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError:
        print("API error.")
        return None


def main():
    mode = input("Choose Input Mode - Type (1) / Voice (2): ")
    
    if mode == "2":
        query = get_voice_input()
    else:
        query = input("Enter your YouTube search query: ")
    
    if not query:
        print("No input received.")
        return
    
    videos = search_youtube(query)
    if not videos:
        print("No videos found.")
        return

    video_titles = [v['title'] for v in videos]
    best_video = analyze_titles_with_gemini(video_titles) 
    
    print("\nBest Video Recommendation:")
    print(best_video)


if __name__ == "__main__":
    main()
