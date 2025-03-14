import streamlit as st
import json
from pathlib import Path
from simple_questions import process_simple_question_set
from media_quiz import process_media_quiz

# Set the page title and favicon
st.set_page_config(page_title="H5P Generator", page_icon="📦")

def main():
    st.title("H5P Package Generator")

    # Dropdown with a link to the README
    with st.expander("How to Use"):
        st.markdown('<a href="https://github.com/aburossi/h5p_full/tree/main#readme" target="_blank">Bedienungsanleitung</a>', unsafe_allow_html=True)
        st.markdown('<a href="https://github.com/aburossi/h5p_full/blob/main/README_en.md" target="_blank">How-To-Guide</a>', unsafe_allow_html=True)
    
    # Explanation text with GPT link
    st.markdown("""
    **Generate JSON Content using CustomGPT:**  
    Content for the package generator may be created using this CustomGPT [h5p-mf-tf](https://chatgpt.com/g/g-67738981e5e081919b6fc8e93e287453-h5p-mf-tf) or via this [fobizz Chatbot](https://tools.fobizz.com/ai/chats/public_assistants/fb5dfcca-6773-4da2-a468-a10daf149c42?token=969f9f7ef6be8cdabb3258da9155f943).
    """)

        # Explanation text with GPT link
    st.markdown("""
    **Transcription:**  
    mp3-Files can be transcribed with this app [Transcript-MP3](https://transcript-mp3.streamlit.app/).
    """)
    
    # Step-by-step guide with emoji numbers in the main area
    st.markdown("""
    **In the sidebar, follow these steps to generate your H5P package:**  
    1. **Select H5P Package Type:** Choose either *Simple Question Set* or *Media Quiz* from the sidebar.  
    2. **Provide Package Details:** Enter the title, randomization settings, number of questions per round, and passing percentage.  
    3. **For Media Quiz (if selected):** Enter the media type and its URL.  
    4. **Paste JSON Content:** Input the JSON content (which can be generated using GPT) into the text area.  
    5. **Generate Package:** Click the *Generate H5P Package* button to download your package.
    """)
    
    # Add sidebar heading
    st.sidebar.markdown("# Sidebar")
    
    # Sidebar elements with corresponding emojis
    mode = st.sidebar.radio("👉1️⃣ Select H5P Package Type", ["Simple Question Set", "Media Quiz"])
    
    title = st.sidebar.text_input("👉2️⃣ Title", "Generated Quiz")
    randomization = st.sidebar.checkbox("👉2️⃣ Randomize Questions", True)
    pool_size = st.sidebar.slider("👉2️⃣ Number of Questions per Round", min_value=1, max_value=20, value=7)
    pass_percentage = st.sidebar.selectbox("👉2️⃣ Passing Percentage", options=[50, 60, 66, 75, 100], index=1)
    user_image_file = st.sidebar.file_uploader("👉2️⃣ Upload Title Image", type=["png", "jpg", "jpeg"])
    user_image_bytes = user_image_file.read() if user_image_file else None

    if mode == "Media Quiz":
        media_type = st.radio("3️⃣ Select Media Type", ["video", "audio"])
        media_url = st.text_input(f"👉3️⃣ Enter {media_type.capitalize()} URL")
    
    json_input = st.text_area("👉4️⃣ Paste JSON Content", height=300, help="JSON format generated from your questions.")
    
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
        else:
            st.error("Failed to generate H5P package.")
    

if __name__ == "__main__":
    main()
