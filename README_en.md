# 📝 **Guide to Using the H5P Generator App on Streamlit**

This guide helps you use the **Streamlit.io** app to create **interactive H5P quiz content**.

---

## 🚀 **1. Open the App**
1. Visit the hosted **[Streamlit App](https://h5p-content.streamlit.app/)** in your browser.
2. Once the page loads, you will see the **user interface** with various input fields and selection options.

---

## 🎯 **2. Select the Quiz Type**
In the left sidebar, you can choose between **two quiz types**:

✅ **Simple Question Set** → A basic set of questions without media.  
✅ **Media Quiz** → A question set with embedded video or audio.

Once you select an option, the input fields adjust accordingly.

---

## 🏗 **3. Configure Quiz Settings**
Depending on the selected quiz type, you must set the following **parameters**:

### 📝 **General Settings (for both quiz types)**
🔹 **Title** – Name your quiz.  
🔹 **Randomize Questions** – Choose whether the questions appear in a random order.  
🔹 **Number of Questions per Round** – Set how many questions should be displayed per session (1–20).  
🔹 **Passing Percentage** – Define the required score to pass (50%, 60%, 66%, 75%, 100%).  
🔹 **Upload Title Image** *(optional)* – Upload a title image for your quiz.  

### 🎥 **Additional Settings for Media Quiz**
If you selected **Media Quiz**, additional fields appear:  
🔹 **Media Type** – Choose whether to use a **video** or **audio** file.  
🔹 **Media URL** – Enter the URL of a **YouTube video** or an **MP3 file**.  

---

## 📌 **4. Add Questions (JSON Format)**
The app requires **questions in JSON format**.

>💡 **Need help generating questions?**  
>Use this GPT: **[H5P MF-TF Question Generator](https://chatgpt.com/g/g-67738981e5e081919b6fc8e93e287453-h5p-mf-tf)** to create **Multiple Choice & True/False questions** in the correct format! 🚀  
>Also available on [Fobizz](https://tools.fobizz.com/ai/chats/public_assistants/fb5dfcca-6773-4da2-a468-a10daf149c42?token=969f9f7ef6be8cdabb3258da9155f943).  

🔹 **Copy your JSON into the "Paste JSON Content" input field.**  
🔹 If you don’t have JSON ready, use the following example as a template:  

### Example for **Multiple Choice** & **True/False** Questions:
```json
{
  "questions": [
    {
      "type": "MultipleChoice",
      "question": "What is the capital of France?",
      "options": [
        {"text": "Berlin", "is_correct": false},
        {"text": "Paris", "is_correct": true},
        {"text": "Madrid", "is_correct": false}
      ]
    },
    {
      "type": "TrueFalse",
      "question": "The sun revolves around the Earth.",
      "correct_answer": false,
      "feedback_correct": "Correct! The Earth revolves around the sun.",
      "feedback_incorrect": "Incorrect! Actually, it's the other way around."
    }
  ]
}
```
🔹 **Make sure your JSON is correctly formatted**, as incorrect JSON files cannot be processed.

---

## ⚡ **5. Generate the H5P Package**
1. Click the **"Generate H5P Package"** button.  
2. If there are any issues (e.g., incorrect JSON format), you will receive an **error message**.  
3. Once the package is successfully created, the **"Download H5P Package"** button will appear.  
4. Click it to download the `.h5p` file.

---

## 🎓 **6. Use the H5P Package**
The downloaded `.h5p` file can be uploaded to the following platforms:
🔹 **Moodle** *(H5P plugin required)*  
🔹 **WordPress** *(H5P plugin required)*  
🔹 **H5P.com** *(Direct upload possible)*  

There, you can further edit your interactive quiz or embed it directly into learning modules.

---

## ❓ **Frequently Asked Questions (FAQ)**
**❓ My JSON file is not accepted. What can I do?**  
🔹 Check if brackets `{}` and `[]` are correctly placed.  
🔹 Use an **online JSON validator** (e.g., [jsonlint.com](https://jsonlint.com/)).  

**❓ The H5P file won’t upload to Moodle/WordPress.**  
🔹 Ensure the **H5P plugin** is installed correctly.  
🔹 If it doesn’t work, check if the file is corrupted.  

---

## ✅ **Conclusion**
With this app, you can **quickly and easily create H5P quiz content**—directly in your browser, without additional software. Good luck creating interactive learning content! 🚀

