import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

# --- CONFIGURATION ---
gemini_key = st.secrets['api_keys']['yt_key']
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="YouTube Summarizer", page_icon="📺", layout="centered")

# --- FUNCTIONS ---
def extract_video_id(url):
    return url.split('=')[-1]if '=' in url else url.split('/')[-1]

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=['en','hi'])
        return transcript
    except:
        return None

def summarize_with_gemini(text):
    response = model.generate_content(f"Summarize the following YouTube transcript into list of main events in brief and short note in english, remove intro,remove outro and remove promotions:\n\n{text}")
    return response.text.strip()

# --- UI ---
st.title("📺 YouTube Video Summarizer with Gemini")
st.markdown("Paste a **YouTube video URL** below and get a quick AI summary of the transcript.")

url = st.text_input("Enter YouTube video URL:")

if st.button("Summarize"):
    video_id = extract_video_id(url).strip()
    if not video_id:
        st.error("Invalid YouTube URL format.")
    else:
        with st.spinner("Fetching transcript..."): 
            transcript = fetch_transcript(video_id)
            if not transcript:
                st.error("No transcript available for this video.")
            else:
                with st.spinner("Summarizing with Gemini..."):
                    summary = summarize_with_gemini(transcript)
                    st.success("Summary generated!")

                    st.subheader("Summary:")
                    st.write(summary)

                    # Download button
                    st.download_button(
                        label="Download Summary as TXT",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )

# Optional Footer
st.markdown("---")
st.caption("Made with Streamlit + Gemini by Dheeraj")

