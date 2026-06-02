# 📝 Project Overview: Resume Ranking System

This document explains what this project is and how it works in simple, easy-to-understand words.

## 🎯 What does this project do?
Imagine you are hiring for a job and receive 100 resumes. Reading all of them takes a lot of time! 
This system reads a **Job Description** and a bunch of **Candidate Resumes**, and automatically tells you which candidates are the best match for the job. It gives everyone a "Match Score" from 0% to 100% and ranks them from best to worst.

---

## 🛠️ Tech Stack (The Tools We Used)
- **Python**: The main programming language.
- **Streamlit**: A tool that turns our Python code into a beautiful, interactive website.
- **Scikit-Learn**: The brain of the app. It does the complex math to compare words.
- **Pandas**: Used to organize the final scores into neat rows and columns (like a spreadsheet).
- **Plotly**: Draws the colorful bar charts so you can see the results easily.
- **PDFPlumber & PyTesseract**: Special tools used to read text out of PDF files (even scanned images!).

---

## 🧩 Modules (How the pieces fit together)

The project is split into small chunks (modules) so the code stays clean and organized.

### 1. `app.py` (The Front Door)
This is the main website file. It creates the sleek, dark-themed webpage you see on your screen. It handles file uploads, shows the charts, and gives you buttons to download the results.

### 2. `modules/preprocess.py` (The Cleaner)
Before we can compare documents, we have to clean the text. This module removes useless words (like "the", "and", "a") and makes everything lowercase so the math works perfectly.

### 3. `modules/similarity.py` (The Math Brain)
This is where the magic happens! It uses two concepts:
- **TF-IDF:** Counts which important words appear in the job description and the resumes.
- **Cosine Similarity:** Calculates the exact percentage of how closely the resume's words match the job description's words.

### 4. `modules/ranker.py` (The Sorter)
Once the math brain calculates the scores, this module simply sorts everyone. It puts the person with the highest score at Rank #1.

### 5. `modules/pdf_processor.py` (The Reader)
If you upload a PDF file instead of a simple text file, this module opens it and extracts the words. If the PDF is just a scanned picture, it uses **OCR** (Optical Character Recognition) to "read" the image and pull the text out.

### 6. `modules/exporter.py` (The Saver)
When you are done, you might want to save the rankings to share with your boss. This module packages the final scoreboard into a `.csv` file so you can open it in Excel.
