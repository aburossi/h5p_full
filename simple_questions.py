import json
from pathlib import Path
import streamlit as st
from utils import map_questions_to_h5p, create_h5p_package

def create_simple_content(h5p_questions, title, randomization, pool_size, pass_percentage):
    content = {
        "introPage": {
            "showIntroPage": True,
            "startButtonText": "Quiz starten",
            "title": title,
            "introduction": (
                f"<p style='text-align:center'><strong>Starten Sie das Quiz, um Ihr Wissen zu testen.</strong></p>"
                f"<p style='text-align:center'><strong>Pro Runde werden zufällig {pool_size} Fragen angezeigt.</strong></p>"
                "<p style='text-align:center'><strong>Wiederholen Sie die Übung, um weitere Fragen zu beantworten.</strong></p>"
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
    }
    return content

def process_simple_question_set(json_data, template_zip_path, title, randomization, pool_size, pass_percentage, user_image_bytes=None):
    try:
        if not isinstance(json_data, dict):
            st.error("Invalid JSON data format.")
            return None
        questions = json_data.get("questions", [])
        if not isinstance(questions, list) or not questions:
            st.error("No questions found or questions is not a list.")
            return None
        h5p_questions = map_questions_to_h5p(questions, "Simple_Questions")
        if not h5p_questions:
            st.error("No valid questions mapped.")
            return None
        content = create_simple_content(h5p_questions, title, randomization, pool_size, pass_percentage)
        content_json_str = json.dumps(content, ensure_ascii=False, indent=4)
        package = create_h5p_package(content_json_str, template_zip_path, title, "H5P.QuestionSet", user_image_bytes)
        return package
    except Exception as e:
        st.error(f"Error processing simple question set: {e}")
        return None
