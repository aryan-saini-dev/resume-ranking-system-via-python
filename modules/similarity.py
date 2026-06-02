"""Similarity calculation module using TF-IDF and Cosine Similarity."""

from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from modules.preprocess import TextPreprocessor


class SimilarityCalculator:
    """Calculates similarity between texts using TF-IDF and Cosine Similarity.
    
    This class provides methods to vectorize documents using TF-IDF and compute
    cosine similarity scores between pairs of texts.
    """
    
    def __init__(self) -> None:
        """Initialize SimilarityCalculator with TF-IDF vectorizer and preprocessor."""
        self.vectorizer: TfidfVectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=500,
            min_df=1,
            max_df=0.95,
            ngram_range=(1, 2)
        )
        self.preprocessor: TextPreprocessor = TextPreprocessor()
        self.fitted: bool = False
    
    def fit(self, texts: List[str]) -> None:
        """Fit the TF-IDF vectorizer on a list of texts.
        
        Args:
            texts: List of documents to fit the vectorizer on
            
        Raises:
            ValueError: If texts list is empty or contains invalid data
        """
        if not texts or len(texts) == 0:
            raise ValueError("Texts list must not be empty")
        
        # Preprocess texts before fitting
        preprocessed_texts = [
            self.preprocessor.preprocess(text) for text in texts
        ]
        
        # Fit vectorizer
        self.vectorizer.fit(preprocessed_texts)
        self.fitted = True
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts.
        
        Args:
            text1: First text (usually job description)
            text2: Second text (usually resume)
            
        Returns:
            Similarity score between 0 and 1
            
        Raises:
            RuntimeError: If vectorizer has not been fitted
            ValueError: If either text is invalid
        """
        if not self.fitted:
            raise RuntimeError("Vectorizer must be fitted before calculating similarity")
        
        if not text1 or not isinstance(text1, str):
            raise ValueError("Text1 must be a non-empty string")
        
        if not text2 or not isinstance(text2, str):
            raise ValueError("Text2 must be a non-empty string")
        
        # Preprocess texts
        preprocessed_text1 = self.preprocessor.preprocess(text1)
        preprocessed_text2 = self.preprocessor.preprocess(text2)
        
        # Transform texts to TF-IDF vectors
        vector1 = self.vectorizer.transform([preprocessed_text1])
        vector2 = self.vectorizer.transform([preprocessed_text2])
        
        # Calculate cosine similarity
        similarity: float = cosine_similarity(vector1, vector2)[0][0]
        
        return float(similarity)
    
    def get_vectorizer(self) -> TfidfVectorizer:
        """Get the fitted TF-IDF vectorizer.
        
        Returns:
            The TF-IDF vectorizer instance
            
        Raises:
            RuntimeError: If vectorizer has not been fitted
        """
        if not self.fitted:
            raise RuntimeError("Vectorizer must be fitted first")
        
        return self.vectorizer
