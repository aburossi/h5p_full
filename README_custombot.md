# 📘 Anleitung: Erstellung von H5P-Quizinhalten mit GPT und Streamlit

Diese Anleitung beschreibt den Workflow zur Erstellung von interaktiven H5P-Quizinhalten mithilfe eines Custom GPTs und der Streamlit-App.

---

## 🧠 1. Fragen mit dem Custom GPT generieren

Nutzen Sie den **Custom GPT** [H5P MF-TF Question Generator](https://chatgpt.com/g/g-6804997575948191acd2d7acfebf1c3d-h5p-mc-t-f), um ein vollständiges Set an Fragen zu erstellen.

### Vorgaben an den GPT:

- Sprache: Deutsch (Sie-Form), Zielgruppe: 15–20 Jahre (Schweiz)
- **Fragentypen**:
  - **Multiple Choice**:
    - 5 Fragen auf **Bloom-Level "Erinnern"**
    - 5 Fragen auf **Bloom-Level "Verstehen"**
  - **True/False**:
    - 3 Fragen auf **Bloom-Level "Erinnern"**
    - 3 Fragen auf **Bloom-Level "Verstehen"**

> 📌 **Wichtig:**  
> Nach dem Generieren den vollständigen JSON-Code kopieren und im nächsten Schritt einfügen.

---

## 🧩 2. H5P-Generator-App öffnen

👉 [Zur Streamlit-App](https://h5p-content.streamlit.app/)

---

## 🛠️ 3. Quiz-Typ auswählen

In der linken Seitenleiste:

- ✅ **Simple Question Set** – Nur Fragen
- ✅ **Media Quiz** – Mit eingebettetem Video oder Audio

---

## ⚙️ 4. Einstellungen anpassen

### Allgemein:

- **Titel** des Quizzes
- **Zufällige Reihenfolge** aktivieren
- **Fragen pro Runde** festlegen (1–20)
- **Bestehensgrenze** auswählen (50% – 100%)
- Optional: **Titelbild** hochladen

### Nur bei Media Quiz:

- **Media Type**: Video oder Audio
- **Media URL**: YouTube-Link oder MP3-Datei

---

## 📝 5. JSON-Fragen einfügen

Fügen Sie den generierten JSON-Code in das Feld **"Paste JSON Content"** ein.


---

## 📦 6. H5P-Datei generieren

1. Klicken Sie auf **"Generate H5P Package"**.
2. Nach erfolgreicher Erstellung erscheint **"Download H5P Package"**.
3. Laden Sie die `.h5p`-Datei herunter.

> ⚠️ **Hinweis:** Diese Datei ist **nicht mit Lumi Desktop** kompatibel. Nutzen Sie Moodle, WordPress oder [lumi.education](https://app.lumi.education/).

---

## ⬆️ 7. Verwendung der H5P-Datei

Sie können die `.h5p`-Datei in folgenden Plattformen verwenden:

- [lumi.education](https://app.lumi.education/)
- **Moodle** (mit H5P-Plugin)
- **WordPress** (mit H5P-Plugin)
- **H5P.com** (direkter Upload)

---

## ℹ️ Zusätzliche Tools

- **Alternative GPT-Instanz:** [Fobizz AI Bot](https://tools.fobizz.com/ai/chats/public_assistants/fb5dfcca-6773-4da2-a468-a10daf149c42?token=969f9f7ef6be8cdabb3258da9155f943)

---

## ✅ Fazit

Mit diesem Workflow können Sie effizient und standardisiert interaktive H5P-Inhalte erstellen und in Ihre Lernplattform integrieren.
