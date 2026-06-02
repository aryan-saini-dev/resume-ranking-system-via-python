# Intelligent Resume Ranking System

An intelligent application that ranks candidate resumes based on how well they match a given Job Description using TF-IDF and Cosine Similarity.

## 📋 Project Overview

This project automates the resume screening process by:
- Analyzing job descriptions and candidate resumes
- Extracting and comparing key skills and qualifications
- Ranking candidates by their match percentage
- Providing visualizations and CSV export of results

## ✨ Features

### 1. **Text Preprocessing**
   - Lowercasing
   - Punctuation removal
   - Stopword removal (English NLTK stopwords)
   - Extra whitespace cleanup
   - Basic tokenization

### 2. **Keyword Extraction**
   - TF-IDF Vectorizer for importance ranking
   - Extracts keywords from both job descriptions and resumes
   - Identifies critical qualifications

### 3. **Similarity Calculation**
   - TF-IDF-based text vectorization
   - Cosine Similarity metric
   - Normalized match scores (0-100%)

### 4. **Candidate Ranking**
   - Ranked list from highest to lowest match
   - Displays rank, candidate name, and match percentage
   - Tie-breaking with stable sorting

### 5. **CSV Export**
   - Exports results to `ranking_results.csv`
   - Includes rank, candidate name, and match score
   - Ready for further analysis

### 6. **Streamlit UI**
   - **Sidebar**: Upload job description and multiple resumes
   - **Main Page**: Display ranking table and visualizations
   - **Download Button**: Export results as CSV
   - **Chart**: Interactive bar chart using Plotly

## 📁 Project Structure

```
resume-ranking-system-via-python/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── modules/
│   ├── __init__.py
│   ├── preprocess.py              # Text preprocessing utilities
│   ├── ranker.py                  # Ranking engine
│   ├── similarity.py              # Similarity calculation
│   └── exporter.py                # CSV export functionality
│
├── data/
│   ├── job_description.txt        # Sample job description
│   └── resumes/
│       ├── priya_resume.txt       # Sample resume 1
│       ├── aman_resume.txt        # Sample resume 2
│       ├── rahul_resume.txt       # Sample resume 3
│       ├── sarah_resume.txt       # Sample resume 4
│       ├── vikram_resume.txt      # Sample resume 5
│       └── ananya_resume.txt      # Sample resume 6
│
└── output/
    └── ranking_results.csv        # Generated results
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aryan-saini-dev/resume-ranking-system-via-python.git
   cd resume-ranking-system-via-python
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK stopwords** (one-time setup)
   ```bash
   python -c "import nltk; nltk.download('stopwords')"
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Using with Sample Data

1. Click **"Upload Job Description"** in the sidebar
2. Select `data/job_description.txt`
3. Click **"Upload Resumes"** in the sidebar
4. Select all resume files from `data/resumes/`
5. View results on the main page
6. Download results as CSV using the **Download CSV** button

### Using with Your Own Data

1. Prepare your job description as a `.txt` file
2. Prepare resume files as `.txt` files
3. Upload files through the Streamlit UI
4. Results are displayed instantly

## 🔧 Module Documentation

### `modules/preprocess.py`
**TextPreprocessor Class**
- `__init__()`: Initialize preprocessor
- `preprocess(text: str) -> str`: Clean and tokenize text
- `get_tokens(text: str) -> List[str]`: Extract tokens

### `modules/similarity.py`
**SimilarityCalculator Class**
- `__init__()`: Initialize TF-IDF vectorizer
- `fit(texts: List[str]) -> None`: Fit vectorizer on texts
- `calculate_similarity(text1: str, text2: str) -> float`: Compute cosine similarity (0-1)

### `modules/ranker.py`
**ResumeRanker Class**
- `__init__(job_desc: str, resumes: Dict[str, str])`: Initialize ranker
- `rank_resumes() -> List[Dict]`: Generate rankings
- `get_rankings() -> List[Dict]`: Get sorted results

### `modules/exporter.py`
**CSVExporter Class**
- `export_results(rankings: List[Dict], filename: str) -> None`: Export to CSV

## 📊 Sample Output

```
Rank | Candidate | Match Score
-----|-----------|-------------
1    | Priya     | 89%
2    | Aman      | 82%
3    | Rahul     | 74%
4    | Sarah     | 68%
5    | Vikram    | 61%
6    | Ananya    | 55%
```

## 🎓 Key Algorithms

### TF-IDF (Term Frequency-Inverse Document Frequency)
- Measures importance of keywords in documents
- Higher weight for rare but relevant terms
- Reduces bias toward common words

### Cosine Similarity
- Compares angle between text vectors
- Range: 0 (no similarity) to 1 (perfect match)
- Normalized to 0-100% for display

## ⚙️ Technical Details

### Code Quality
- ✅ Type hints throughout
- ✅ Comprehensive error handling
- ✅ Clean, well-commented code
- ✅ OOP design principles
- ✅ Modular architecture
- ✅ Production-ready structure

### Dependencies
- **streamlit**: Web UI framework
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: ML algorithms (TF-IDF, Cosine Similarity)
- **nltk**: Natural language processing
- **plotly**: Interactive visualizations

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💼 About

Created as an educational project to demonstrate:
- Natural Language Processing (NLP)
- Text similarity algorithms
- Streamlit web applications
- Python best practices
- Data export and visualization

---

**Happy Ranking! 🎉**
