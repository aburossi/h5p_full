import json
import uuid
import zipfile
import io
import logging
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import streamlit as st

logging.basicConfig(level=logging.INFO)

def generate_uuid():
    return str(uuid.uuid4())

def substitute_sharp_s(text: str) -> str:
    return text.replace('ß', 'ss')

def extract_youtube_id(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        elif parsed_url.hostname in ['youtu.be']:
            return parsed_url.path.lstrip('/')
        else:
            return None
    except Exception as e:
        logging.error(f"Error parsing YouTube URL: {e}")
        return None

def map_multiple_choice(question):
    try:
        h5p_question = {
            "library": "H5P.MultiChoice 1.16",
            "params": {
                "question": question.get("question", "Keine Frage gestellt."),
                "answers": [],
                "behaviour": {
                    "singleAnswer": True,
                    "enableRetry": False,
                    "enableSolutionsButton": False,
                    "enableCheckButton": True,
                    "type": "auto",
                    "singlePoint": False,
                    "randomAnswers": True,
                    "showSolutionsRequiresInput": True,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "autoCheck": False,
                    "passPercentage": 100,
                    "showScorePoints": True
                },
                "media": {"disableImageZooming": False},
                "overallFeedback": [{"from": 0, "to": 100}],
                "UI": {
                    "checkAnswerButton": "Überprüfen",
                    "submitAnswerButton": "Absenden",
                    "showSolutionButton": "Lösung anzeigen",
                    "tryAgainButton": "Wiederholen",
                    "tipsLabel": "Hinweis anzeigen",
                    "scoreBarLabel": "Du hast :num von :total Punkten erreicht.",
                    "tipAvailable": "Hinweis verfügbar",
                    "feedbackAvailable": "Rückmeldung verfügbar",
                    "readFeedback": "Rückmeldung vorlesen",
                    "wrongAnswer": "Falsche Antwort",
                    "correctAnswer": "Richtige Antwort",
                    "shouldCheck": "Hätte gewählt werden müssen",
                    "shouldNotCheck": "Hätte nicht gewählt werden sollen",
                    "noInput": "Bitte antworte, bevor du die Lösung ansiehst",
                    "a11yCheck": "Die Antworten überprüfen. Die Auswahlen werden als richtig, falsch oder fehlend markiert.",
                    "a11yShowSolution": "Die Lösung anzeigen. Die richtigen Lösungen werden in der Aufgabe angezeigt.",
                    "a11yRetry": "Die Aufgabe wiederholen. Alle Versuche werden zurückgesetzt und die Aufgabe wird erneut gestartet."
                },
                "confirmCheck": {
                    "header": "Beenden?",
                    "body": "Ganz sicher beenden?",
                    "cancelLabel": "Abbrechen",
                    "confirmLabel": "Beenden"
                },
                "confirmRetry": {
                    "header": "Wiederholen?",
                    "body": "Ganz sicher wiederholen?",
                    "cancelLabel": "Abbrechen",
                    "confirmLabel": "Bestätigen"
                }
            },
            "subContentId": generate_uuid(),
            "metadata": {
                "contentType": "Multiple Choice",
                "license": "U",
                "title": "Multiple Choice",
                "authors": [],
                "changes": [],
                "extraTitle": "Multiple Choice"
            }
        }
        options = question.get("options", [])
        if not isinstance(options, list):
            st.warning(f"'options' is not a list in question: {question.get('question', 'Keine Frage')}")
            return h5p_question

        for option in options:
            answer = {
                "text": option.get("text", ""),
                "correct": option.get("is_correct", False),
                "tipsAndFeedback": {
                    "tip": "",
                    "chosenFeedback": f"<div>{option.get('feedback', '')}</div>\n",
                    "notChosenFeedback": ""
                }
            }
            h5p_question["params"]["answers"].append(answer)
        return h5p_question
    except Exception as e:
        st.error(f"Error mapping MultipleChoice question: {e}")
        return {}

def map_true_false(question):
    try:
        correct_answer = question.get("correct_answer", False)
        feedback_correct = question.get("feedback_correct", "")
        feedback_incorrect = question.get("feedback_incorrect", "")
        h5p_question = {
            "library": "H5P.TrueFalse 1.8",
            "params": {
                "question": question.get("question", "Keine Frage gestellt."),
                "correct": "true" if correct_answer else "false",
                "behaviour": {
                    "enableRetry": False,
                    "enableSolutionsButton": False,
                    "enableCheckButton": True,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "autoCheck": False,
                    "feedbackOnCorrect": feedback_correct,
                    "feedbackOnWrong": feedback_incorrect
                },
                "media": {"disableImageZooming": False},
                "l10n": {
                    "trueText": "Wahr",
                    "falseText": "Falsch",
                    "score": "Du hast @score von @total Punkten erreicht.",
                    "checkAnswer": "Überprüfen",
                    "submitAnswer": "Absenden",
                    "showSolutionButton": "Lösung anzeigen",
                    "tryAgain": "Wiederholen",
                    "wrongAnswerMessage": "Falsche Antwort",
                    "correctAnswerMessage": "Richtige Antwort",
                    "scoreBarLabel": "Du hast :num von :total Punkten erreicht.",
                    "a11yCheck": "Die Antworten überprüfen. Die Antwort wird als richtig, falsch oder unbeantwortet markiert.",
                    "a11yShowSolution": "Die Lösung anzeigen. Die richtige Lösung wird in der Aufgabe angezeigt.",
                    "a11yRetry": "Die Aufgabe wiederholen. Alle Versuche werden zurückgesetzt, und die Aufgabe wird erneut gestartet."
                },
                "confirmCheck": {
                    "header": "Beenden?",
                    "body": "Ganz sicher beenden?",
                    "cancelLabel": "Abbrechen",
                    "confirmLabel": "Beenden"
                },
                "confirmRetry": {
                    "header": "Wiederholen?",
                    "body": "Ganz sicher wiederholen?",
                    "cancelLabel": "Abbrechen",
                    "confirmLabel": "Bestätigen"
                }
            },
            "subContentId": generate_uuid(),
            "metadata": {
                "contentType": "True/False Question",
                "license": "U",
                "title": "Richtig Falsch",
                "authors": [],
                "changes": [],
                "extraTitle": "Richtig Falsch"
            }
        }
        return h5p_question
    except Exception as e:
        st.error(f"Error mapping TrueFalse question: {e}")
        return {}

def map_questions_to_h5p(questions, source_name):
    h5p_questions = []
    for idx, question in enumerate(questions, start=1):
        q_type = question.get("type", "").strip()
        if q_type == "MultipleChoice":
            mapped = map_multiple_choice(question)
        elif q_type == "TrueFalse":
            mapped = map_true_false(question)
        else:
            st.warning(f"Unsupported question type '{q_type}' in {source_name}. Skipping question #{idx}.")
            continue
        if mapped:
            h5p_questions.append(mapped)
    st.info(f"Mapped {len(h5p_questions)} questions from {source_name}.")
    return h5p_questions

def create_h5p_package(content_json, template_zip_path, title, main_library, user_image_bytes=None):
    try:
        with open(template_zip_path, 'rb') as f:
            template_bytes = f.read()
        with zipfile.ZipFile(io.BytesIO(template_bytes), 'r') as template_zip:
            in_memory_zip = io.BytesIO()
            with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                for item in template_zip.infolist():
                    file_data = template_zip.read(item.filename)
                    new_zip.writestr(item, file_data)
                new_zip.writestr('content/content.json', substitute_sharp_s(content_json).encode('utf-8'))
                if user_image_bytes:
                    image_path = 'content/images/file-_jmSDW4b9EawjImv.png'
                    new_zip.writestr(image_path, user_image_bytes)
                h5p_content = {
                    "embedTypes": ["iframe"],
                    "language": "en",
                    "license": "U",
                    "extraTitle": title,
                    "title": title,
                    "mainLibrary": main_library,
                    "preloadedDependencies": [
                        {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                        {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                        {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                        {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                        {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                        {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5}
                    ],
                    "defaultLanguage": "de"
                }
                if main_library == "H5P.QuestionSet":
                    h5p_content["preloadedDependencies"].append(
                        {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20}
                    )
                elif main_library == "H5P.Column":
                    h5p_content["preloadedDependencies"] = [
                        {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
                        {"machineName": "H5P.Audio", "majorVersion": 1, "minorVersion": 5},
                        {"machineName": "H5P.Video", "majorVersion": 1, "minorVersion": 6},
                        {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                        {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
                        {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3},
                        {"machineName": "H5P.Transition", "majorVersion": 1, "minorVersion": 0},
                        {"machineName": "H5P.FontIcons", "majorVersion": 1, "minorVersion": 0},
                        {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
                        {"machineName": "H5P.Question", "majorVersion": 1, "minorVersion": 5},
                        {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
                        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 18}
                    ]
                h5p_json_str = json.dumps(h5p_content, indent=4)
                new_zip.writestr('h5p.json', h5p_json_str.encode('utf-8'))
        in_memory_zip.seek(0)
        return in_memory_zip.getvalue()
    except FileNotFoundError:
        st.error(f"Template zip file not found at '{template_zip_path}'.")
        return None
    except Exception as e:
        st.error(f"Error creating H5P package: {e}")
        return None
