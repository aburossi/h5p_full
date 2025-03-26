import streamlit as st
import json
from pathlib import Path
from simple_questions import process_simple_question_set
from media_quiz import process_media_quiz
import streamlit.components.v1 as components

# Set the page title and favicon
st.set_page_config(page_title="H5P Package Generator", page_icon="📦")

def main():
    st.title("H5P Package Generator")

    # How-to guide section
    with st.expander("How to Use"):
        st.markdown('<a href="https://github.com/aburossi/h5p_full/tree/main#readme" target="_blank">Bedienungsanleitung</a>', unsafe_allow_html=True)
        st.markdown('<a href="https://github.com/aburossi/h5p_full/blob/main/README_en.md" target="_blank">How-To-Guide</a>', unsafe_allow_html=True)
    
    st.markdown("""
    **Generate JSON Content using CustomGPT:**  
    Content for the package generator may be created using this CustomGPT [h5p-mf-tf](https://chatgpt.com/g/g-67738981e5e081919b6fc8e93e287453-h5p-mf-tf) or via this [fobizz Chatbot](https://tools.fobizz.com/ai/chats/public_assistants/fb5dfcca-6773-4da2-a468-a10daf149c42?token=969f9f7ef6be8cdabb3258da9155f943).
    """)
    
    st.markdown("""
    **Transcription:**  
    mp3-Files can be transcribed with this app [-MP3](https://-mp3.streamlit.app/).
    """)
    
    st.markdown("""
    **In the sidebar, follow these steps to generate your H5P package:**  
    1. **Select H5P Package Type:** Choose either *Simple Question Set* or *Media Quiz* from the sidebar.  
    2. **Provide Package Details:** Enter the title, randomization settings, number of questions per round, and passing percentage.  
    3. **For Media Quiz (if selected):** Enter the media type and its URL.  
       *~For YouTube videos, you can fetch the transcript below.~*  
    4. **Paste JSON Content:** Input the JSON content (which can be generated using GPT) into the text area.  
    5. **Generate Package:** Click the *Generate H5P Package* button to download your package.
    """)

    # Sidebar settings
    st.sidebar.markdown("# Sidebar")
    mode = st.sidebar.radio("👉1️⃣ Select H5P Package Type", ["Simple Question Set", "Media Quiz"])
    title = st.sidebar.text_input("👉2️⃣ Title", "Generated Quiz")
    randomization = st.sidebar.checkbox("👉2️⃣ Randomize Questions", True)
    pool_size = st.sidebar.slider("👉2️⃣ Number of Questions per Round", min_value=1, max_value=20, value=7)
    pass_percentage = st.sidebar.selectbox("👉2️⃣ Passing Percentage", options=[50, 60, 66, 75, 100], index=1)
    user_image_file = st.sidebar.file_uploader("👉2️⃣ Upload Title Image", type=["png", "jpg", "jpeg"])
    user_image_bytes = user_image_file.read() if user_image_file else None

    # Media Quiz specific settings and transcript fetching
    if mode == "Media Quiz":
        media_type = st.radio("3️⃣ Select Media Type", ["video", "audio"])
        media_url = st.text_input(f"👉3️⃣ Enter {media_type.capitalize()} URL")
        
        # Transcript explanation for YouTube videos
        if media_type == "video":
            st.markdown("**Note:** For YouTube videos, you can fetch the transcript below using the provided button.")

        # Transcript fetching section (only for video)
        if media_type == "video" and media_url:
            if st.button("Fetch Transcript"):
                try:
                    from youtube_transcriber import YouTubeTranscriber
                    transcriber = YouTubeTranscriber()
                    transcript = transcriber.extract_transcript(media_url)
                    st.session_state.transcript = transcript
                    st.success("Transcript fetched successfully!")
                except Exception as e:
                    st.error(f"Could not fetch transcript: {e}")
            if "transcript" in st.session_state:
                st.text_area("Transcript", st.session_state.transcript, height=200, disabled=True)
                # Create a copy button using an HTML component with JavaScript
                transcript_js = json.dumps(st.session_state.transcript)
                copy_html = f"""
                <html>
                  <head>
                    <script>
                      function copyTranscript() {{
                        var text = {transcript_js};
                        navigator.clipboard.writeText(text).then(function() {{
                          alert("Transcript copied to clipboard!");
                        }}, function(err) {{
                          alert("Failed to copy transcript: " + err);
                        }});
                      }}
                    </script>
                  </head>
                  <body>
                    <button onclick="copyTranscript()">Copy Transcript</button>
                  </body>
                </html>
                """
                components.html(copy_html, height=70)
    
    # Fobizz content generation section moved above the JSON content box.
    st.header("Generate content with Fobizz")
    st.markdown("You can copy and paste the transcript into the Fobizz bot, or use the GPT link above to generate JSON content for your quiz.")
    if st.button("Open Fobizz"):
        components.iframe(
            "https://tools.fobizz.com/ai/chats/public_assistants/fb5dfcca-6773-4da2-a468-a10daf149c42?token=969f9f7ef6be8cdabb3258da9155f943",
            height=600,
            scrolling=True
        )
    
    # JSON input for quiz questions
    json_input = st.text_area("👉4️⃣ Paste JSON Content", height=300, help="JSON format generated from your questions.")
    
    # Package generation
    if st.button("👉5️⃣ Generate H5P Package"):
        if not json_input.strip():
            st.error("Please provide JSON content.")
            return
        try:
            json_data = json.loads(json_input)
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {e}")
            return
        
        if mode == "Simple Question Set":
            template_path = Path(__file__).parent / "templates" / "MC_TF.zip"
            package = process_simple_question_set(json_data, template_path, title, randomization, pool_size, pass_percentage, user_image_bytes)
            filename = "simple_question_set.h5p"
        else:
            template_path = Path(__file__).parent / "templates" / "col_vid_mc_tf.zip"
            package = process_media_quiz(media_url, media_type, json_data, template_path, title, randomization, pool_size, pass_percentage, user_image_bytes)
            filename = "media_quiz.h5p"
        
        if package:
            st.download_button("Download H5P Package", data=package, file_name=filename, mime="application/zip")
            st.warning("⚠️ This H5P file **does NOT work with Lumi Desktop**. Please use an alternative H5P player or a compatible LMS.")
        else:
            st.error("Failed to generate H5P package.")
    
if __name__ == "__main__":
    main()
