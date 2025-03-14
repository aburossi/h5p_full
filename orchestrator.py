import streamlit as st
import json
from pathlib import Path
from simple_questions import process_simple_question_set
from media_quiz import process_media_quiz

def main():
    st.title("H5P Package Generator - Orchestrator")
    st.write("Select the type of H5P package you want to generate.")

    mode = st.sidebar.radio("Select H5P Package Type", ["Simple Question Set", "Media Quiz"])
    
    # Common inputs
    title = st.sidebar.text_input("Title", "Generated Quiz")
    randomization = st.sidebar.checkbox("Randomize Questions", True)
    pool_size = st.sidebar.slider("Number of Questions per Round", min_value=1, max_value=20, value=7)
    pass_percentage = st.sidebar.selectbox("Passing Percentage", options=[50, 60, 66, 75, 100], index=1)
    user_image_file = st.sidebar.file_uploader("Upload Title Image", type=["png", "jpg", "jpeg"])
    user_image_bytes = user_image_file.read() if user_image_file else None

    json_input = st.text_area("Paste JSON Content", height=300, help="JSON format generated from your questions.")
    
    if mode == "Media Quiz":
        media_type = st.radio("Select Media Type", ["video", "audio"])
        media_url = st.text_input(f"Enter {media_type.capitalize()} URL")
    
    if st.button("Generate H5P Package"):
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
