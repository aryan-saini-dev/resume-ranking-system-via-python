"""Text preprocessing module for resume ranking system."""

import re
from typing import List, Set
from nltk.corpus import stopwords
import nltk

# Download stopwords if not already present
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')


class TextPreprocessor:
    """Handles text preprocessing for resume and job description analysis.
    
    This class provides utilities for cleaning and standardizing text data
    including lowercasing, punctuation removal, stopword removal, and tokenization.
    """
    
    def __init__(self) -> None:
        """Initialize TextPreprocessor with English stopwords."""
        self.stop_words: Set[str] = set(stopwords.words('english'))
    
    def preprocess(self, text: str) -> str:
        """Preprocess text by cleaning and tokenizing.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Cleaned and preprocessed text
            
        Raises:
            ValueError: If text is None or empty
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        # Step 1: Convert to lowercase
        text = text.lower()
        
        # Step 2: Remove special characters and punctuation
        # Keep only alphanumeric characters and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Step 3: Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Step 4: Tokenize and remove stopwords
        tokens = text.split()
        tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        
        # Step 5: Join tokens back into string
        cleaned_text = ' '.join(tokens)
        
        return cleaned_text
    
    def get_tokens(self, text: str) -> List[str]:
        """Extract tokens from text after preprocessing.
        
        Args:
            text: Raw text to tokenize
            
        Returns:
            List of preprocessed tokens
            
        Raises:
            ValueError: If text is None or empty
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        cleaned_text = self.preprocess(text)
        tokens = cleaned_text.split()
        
        return tokens
    
    def get_stopwords(self) -> Set[str]:
        """Get the set of English stopwords.
        
        Returns:
            Set of stopwords
        """
        return self.stop_words
