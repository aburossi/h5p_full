# 📝 **Anleitung zur Nutzung der H5P-Generator-App auf Streamlit**  

Diese Anleitung hilft dir, die App auf **Streamlit.io** zu nutzen, um **interaktive H5P-Quizinhalte** zu erstellen.  

---

## 🚀 **1. Öffne die App**  
1. Besuche die gehostete **Streamlit-App** in deinem Browser. *(Den Link erhältst du vom Betreiber der App.)*  
2. Nach dem Laden der Seite siehst du die **Benutzeroberfläche** mit verschiedenen Eingabefeldern und Auswahloptionen.

---

## 🎯 **2. Wähle den Quiz-Typ**  
Im linken Seitenmenü kannst du zwischen **zwei Quiz-Typen** wählen:  

✅ **Simple Question Set** → Reines Fragenset ohne Medien.  
✅ **Media Quiz** → Fragenset mit Video- oder Audioeinbettung.  

Sobald du eine Option auswählst, passen sich die Eingabefelder automatisch an.

---

## 🏗 **3. Quiz-Einstellungen festlegen**  
Je nach gewähltem Quiz-Typ musst du folgende **Einstellungen** vornehmen:

### 📝 **Allgemeine Einstellungen (für beide Quiz-Typen)**  
🔹 **Titel** – Vergib einen Namen für dein Quiz.  
🔹 **Randomize Questions** – Wähle, ob die Fragen in zufälliger Reihenfolge erscheinen sollen.  
🔹 **Number of Questions per Round** – Bestimme, wie viele Fragen pro Durchlauf angezeigt werden (1–20).  
🔹 **Passing Percentage** – Lege fest, ab welchem Prozentsatz das Quiz als bestanden gilt (50%, 60%, 66%, 75%, 100%).  
🔹 **Upload Title Image** *(optional)* – Lade ein Titelbild für dein Quiz hoch.  

### 🎥 **Zusätzliche Einstellungen für Media Quiz**  
Wenn du **Media Quiz** gewählt hast, erscheinen weitere Felder:  
🔹 **Media Type** – Wähle, ob du ein **Video** oder eine **Audio**-Datei nutzen möchtest.  
🔹 **Media URL** – Gib die URL eines **YouTube-Videos** oder einer **MP3-Datei** ein.  

---

## 📌 **4. Fragen hinzufügen (JSON-Format)**  
Die App erwartet die **Fragen im JSON-Format**.  

🔹 **Kopiere dein JSON in das Eingabefeld "Paste JSON Content"**  
🔹 Falls du noch kein JSON hast, kannst du das folgende Beispiel als Vorlage nutzen:  

### Beispiel für **Multiple Choice** & **True/False**-Fragen:
```json
{
  "questions": [
    {
      "type": "MultipleChoice",
      "question": "Was ist die Hauptstadt von Frankreich?",
      "options": [
        {"text": "Berlin", "is_correct": false},
        {"text": "Paris", "is_correct": true},
        {"text": "Madrid", "is_correct": false}
      ]
    },
    {
      "type": "TrueFalse",
      "question": "Die Sonne dreht sich um die Erde.",
      "correct_answer": false,
      "feedback_correct": "Richtig! Die Erde dreht sich um die Sonne.",
      "feedback_incorrect": "Falsch! Tatsächlich ist es umgekehrt."
    }
  ]
}
```
🔹 **Achte darauf, dass dein JSON korrekt formatiert ist**, da fehlerhafte JSON-Dateien nicht verarbeitet werden können.

💡 **Fragen automatisch generieren lassen?**  
Nutze diesen GPT: **[H5P MF-TF Question Generator](https://chatgpt.com/g/g-67738981e5e081919b6fc8e93e287453-h5p-mf-tf)**, um **Multiple Choice & True/False-Fragen** im richtigen Format zu erstellen! 🚀  

---

## ⚡ **5. H5P-Paket erstellen**  
1. Klicke auf den Button **"Generate H5P Package"**.  
2. Falls es Probleme gibt (z. B. falsches JSON-Format), erhältst du eine **Fehlermeldung**.  
3. Sobald das Paket erfolgreich erstellt wurde, erscheint der Button **"Download H5P Package"**.  
4. Klicke darauf, um die `.h5p`-Datei herunterzuladen.

---

## 🎓 **6. H5P-Paket nutzen**  
Die heruntergeladene `.h5p`-Datei kannst du in folgende Plattformen hochladen:  
🔹 **Moodle** *(H5P-Plugin erforderlich)*  
🔹 **WordPress** *(H5P-Plugin erforderlich)*  
🔹 **H5P.com** *(Direkter Upload möglich)*  

Dort kannst du dein interaktives Quiz weiter bearbeiten oder direkt in Lernmodule einbinden.  

---

## ❓ **Häufige Fragen (FAQ)**  
**❓ Meine JSON-Datei wird nicht akzeptiert. Was kann ich tun?**  
🔹 Überprüfe, ob die Klammern `{}` und `[]` korrekt gesetzt sind.  
🔹 Nutze einen **Online-JSON-Validator** (z. B. [jsonlint.com](https://jsonlint.com/)).  

**❓ Die H5P-Datei lässt sich nicht in Moodle/WordPress hochladen.**  
🔹 Stelle sicher, dass das **H5P-Plugin** korrekt installiert ist.  
🔹 Falls es nicht funktioniert, überprüfe, ob die Datei beschädigt wurde.  

---

## ✅ **Fazit**  
Mit dieser App kannst du **schnell und einfach H5P-Quizinhalte** erstellen – direkt im Browser, ohne zusätzliche Software. Viel Erfolg beim Erstellen interaktiver Lerninhalte! 🚀
