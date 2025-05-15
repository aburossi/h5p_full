import json
from pathlib import Path
import streamlit as st
from utils import extract_youtube_id, map_questions_to_h5p, create_h5p_package

def create_media_content(h5p_questions, media_url, media_type, title, randomization, pool_size, pass_percentage, custom_intro_text=None):
    # Use custom_intro_text if provided and not empty, otherwise use defaults
    if custom_intro_text:
        intro_text_to_use = custom_intro_text
    elif media_type == "video":
        intro_text_to_use = "<p>Schauen Sie das Video und beantworten Sie die Verständnisfragen unterhalb des Videos</p>"
    else: # audio
        intro_text_to_use = "<p>Hören Sie den Audiobeitrag und beantworten Sie die Verständnisfragen.</p>"
    
    content_list = []
    intro_block = {
        "content": {
            "params": {"text": intro_text_to_use}, # Use the determined intro text
            "library": "H5P.AdvancedText 1.1",
            "metadata": {
                "contentType": "Text",
                "license": "U",
                "title": "Intro Text", # This title is for the H5P content block itself
                "authors": [],
                "changes": []
            },
            "subContentId": "intro-" + title # Ensure title here refers to the quiz title for uniqueness
        },
        "useSeparator": "auto"
    }
    content_list.append(intro_block)
    
    if media_type == "video":
        youtube_id = extract_youtube_id(media_url)
        if youtube_id:
            reconstructed_url = f"https://www.youtube.com/watch?v={youtube_id}"
        else:
            st.error("Invalid YouTube URL format. Please provide a valid YouTube link.")
            return None
        media_block = {
            "content": {
                "params": {
                    "visuals": {"fit": True, "controls": True},
                    "playback": {"autoplay": False, "loop": False},
                    "l10n": {
                        "name": "Video",
                        "loading": "Videoplayer lädt...",
                        "noPlayers": "Keine Videoplayer gefunden, die das vorliegende Videoformat unterstützen.",
                        "noSources": "Es wurden für das Video keine Quellen angegeben.",
                        "aborted": "Das Abspielen des Videos wurde abgebrochen.",
                        "networkFailure": "Netzwerkfehler.",
                        "cannotDecode": "Dekodierung des Mediums nicht möglich.",
                        "formatNotSupported": "Videoformat wird nicht unterstützt.",
                        "mediaEncrypted": "Medium verschlüsselt.",
                        "unknownError": "Unbekannter Fehler.",
                        "invalidYtId": "Ungültige YouTube-ID.",
                        "unknownYtId": "Video mit dieser YouTube-ID konnte nicht gefunden werden.",
                        "restrictedYt": "Der Besitzer dieses Videos erlaubt kein Einbetten."
                    },
                    "sources": [{
                        "path": reconstructed_url,
                        "mime": "video/YouTube",
                        "copyright": {"license": "U"},
                        "aspectRatio": "16:9"
                    }]
                },
                "library": "H5P.Video 1.6",
                "metadata": {
                    "contentType": "Video",
                    "license": "U",
                    "title": "Video Content",
                    "authors": [],
                    "changes": [],
                    "extraTitle": "Video Content"
                },
                "subContentId": "media-" + title # Ensure title here refers to the quiz title
            },
            "useSeparator": "auto"
        }
    else: # audio
        media_block = {
            "content": {
                "params": {
                    "playerMode": "full",
                    "fitToWrapper": False,
                    "controls": True,
                    "autoplay": False,
                    "playAudio": "Audio abspielen",
                    "pauseAudio": "Audio pausieren",
                    "contentName": "Audio",
                    "audioNotSupported": "Dein Browser unterstützt diese Tondatei nicht.",
                    "files": [{
                        "path": media_url,
                        "mime": "audio/mp3",
                        "copyright": {"license": "U"}
                    }]
                },
                "library": "H5P.Audio 1.5",
                "metadata": {
                    "contentType": "Audio",
                    "license": "U",
                    "title": "Audio Content",
                    "authors": [],
                    "changes": [],
                    "extraTitle": "Audio Content"
                },
                "subContentId": "media-" + title # Ensure title here refers to the quiz title
            },
            "useSeparator": "auto"
        }
    content_list.append(media_block)
    
    question_set = {
        "useSeparator": "auto",
        "content": {
            "library": "H5P.QuestionSet 1.20",
            "params": {
                "introPage": {
                    "showIntroPage": True,
                    "startButtonText": "Quiz starten",
                    "title": title, # This is the title displayed on the intro page of the QuestionSet
                    "introduction": (
                        f"<p style='text-align:center'><strong>Starten Sie das Quiz zu diesem {'Video' if media_type == 'video' else 'Audio'}inhalt.</strong></p>"
                        f"<p style='text-align:center'>Es werden zufällig {pool_size} Fragen angezeigt.</p>"
                    ),
                    "backgroundImage": {
                        "path": "images/file-_jmSDW4b9EawjImv.png",
                        "mime": "image/png",
                        "copyright": {"license": "U"},
                        "width": 52,
                        "height": 52
                    }
                },
                "progressType": "textual",
                "passPercentage": pass_percentage,
                "disableBackwardsNavigation": True,
                "randomQuestions": randomization,
                "endGame": {
                    "showResultPage": True,
                    "showSolutionButton": True,
                    "showRetryButton": True,
                    "noResultMessage": "Quiz beendet",
                    "message": "Dein Ergebnis:",
                    "scoreBarLabel": "Du hast @score von @total Punkten erreicht.",
                    "overallFeedback": [
                        {"from": 0, "to": 50, "feedback": "Kein Grund zur Sorge! Tipp: Schau dir die Lösungen an, bevor du in die nächste Runde startest."},
                        {"from": 51, "to": 75, "feedback": "Du weisst schon einiges über das Thema. Mit jeder Wiederholung kannst du dich steigern."},
                        {"from": 76, "to": 100, "feedback": "Gut gemacht!"}
                    ],
                    "solutionButtonText": "Lösung anzeigen",
                    "retryButtonText": "Nächste Runde",
                    "finishButtonText": "Beenden",
                    "submitButtonText": "Absenden",
                    "showAnimations": False,
                    "skippable": False,
                    "skipButtonText": "Video überspringen"
                },
                "override": {"checkButton": True},
                "texts": {
                    "prevButton": "Zurück",
                    "nextButton": "Weiter",
                    "finishButton": "Beenden",
                    "submitButton": "Absenden",
                    "textualProgress": "Frage @current von @total",
                    "jumpToQuestion": "Frage %d von %total",
                    "questionLabel": "Frage",
                    "readFeedback": "Rückmeldung vorlesen",
                    "unansweredText": "Unbeantwortet",
                    "answeredText": "Beantwortet",
                    "currentQuestionText": "Aktuelle Frage",
                    "navigationLabel": "Fragen"
                },
                "poolSize": pool_size,
                "questions": h5p_questions
            },
            "metadata": {
                "contentType": "Question Set",
                "license": "U",
                "title": title, # This is the metadata title for the QuestionSet
                "authors": [],
                "changes": []
            },
            "subContentId": "qs-" + title # Ensure title here refers to the quiz title
        }
    }
    content_list.append(question_set)
    return {"content": content_list}

def process_media_quiz(media_url, media_type, json_data, template_zip_path, title, randomization, pool_size, pass_percentage, user_image_bytes=None):
    try:
        if not isinstance(json_data, dict):
            st.error("Invalid JSON data format.")
            return None
        
        # Extract questions
        questions = json_data.get("questions", [])
        if not isinstance(questions, list) or not questions:
            st.error("No questions found or questions is not a list.")
            return None
            
        # Extract custom intro text (optional)
        custom_intro_text = json_data.get("customIntroText") # This will be None if the key doesn't exist or the value is null

        h5p_questions = map_questions_to_h5p(questions, "Media_Quiz")
        if not h5p_questions:
            st.error("No valid questions mapped.")
            return None
        
        # Pass the custom_intro_text to create_media_content
        # Note: The 'title' argument passed here is from the Streamlit sidebar.
        # If you want the title from the JSON to be used, you'd need to extract json_data.get("title")
        # and decide how it interacts with the sidebar 'title'. For now, custom_intro_text is the focus.
        content = create_media_content(
            h5p_questions, 
            media_url, 
            media_type, 
            title, # This 'title' comes from the Streamlit UI
            randomization, 
            pool_size, 
            pass_percentage,
            custom_intro_text=custom_intro_text # Pass the extracted custom text
        )
        
        if content is None:
            return None
            
        content_json_str = json.dumps(content, ensure_ascii=False, indent=4)
        package = create_h5p_package(content_json_str, template_zip_path, title, "H5P.Column", user_image_bytes)
        return package
    except Exception as e:
        st.error(f"Error processing media quiz: {e}")
        return None