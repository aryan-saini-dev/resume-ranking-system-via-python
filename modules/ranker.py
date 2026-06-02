"""Resume ranking engine module."""

from typing import List, Dict
from modules.similarity import SimilarityCalculator


class ResumeRanker:
    """Ranks resumes based on similarity to job description.
    
    This class compares each resume against a job description and generates
    a ranked list of candidates with match percentages.
    """
    
    def __init__(self, job_description: str, resumes: Dict[str, str]) -> None:
        """Initialize ResumeRanker with job description and resumes.
        
        Args:
            job_description: Text of the job description
            resumes: Dictionary with candidate names as keys and resume text as values
            
        Raises:
            ValueError: If job_description or resumes are invalid
        """
        if not job_description or not isinstance(job_description, str):
            raise ValueError("Job description must be a non-empty string")
        
        if not resumes or not isinstance(resumes, dict):
            raise ValueError("Resumes must be a non-empty dictionary")
        
        if len(resumes) < 1:
            raise ValueError("At least one resume must be provided")
        
        self.job_description: str = job_description
        self.resumes: Dict[str, str] = resumes
        self.rankings: List[Dict] = []
        self.similarity_calculator: SimilarityCalculator = SimilarityCalculator()
    
    def rank_resumes(self) -> List[Dict]:
        """Calculate rankings for all resumes.
        
        Returns:
            List of dictionaries with rank, candidate name, and match score
            
        Raises:
            RuntimeError: If ranking calculation fails
        """
        try:
            # Prepare all texts for fitting
            all_texts = [self.job_description] + list(self.resumes.values())
            
            # Fit similarity calculator
            self.similarity_calculator.fit(all_texts)
            
            # Calculate similarity for each resume
            candidate_scores: List[Dict] = []
            
            for candidate_name, resume_text in self.resumes.items():
                similarity_score = self.similarity_calculator.calculate_similarity(
                    self.job_description,
                    resume_text
                )
                
                # Convert to percentage (0-100)
                match_percentage = round(similarity_score * 100, 2)
                
                candidate_scores.append({
                    'candidate': candidate_name,
                    'match_score': match_percentage,
                    'similarity': similarity_score
                })
            
            # Sort by match score (descending)
            candidate_scores.sort(key=lambda x: x['match_score'], reverse=True)
            
            # Add rank
            self.rankings = [
                {
                    'rank': idx + 1,
                    'candidate': score['candidate'],
                    'match_score': score['match_score'],
                    'similarity': score['similarity']
                }
                for idx, score in enumerate(candidate_scores)
            ]
            
            return self.rankings
        
        except Exception as e:
            raise RuntimeError(f"Failed to rank resumes: {str(e)}")
    
    def get_rankings(self) -> List[Dict]:
        """Get the current rankings.
        
        Returns:
            List of ranked candidates (empty if not yet ranked)
        """
        return self.rankings
    
    def get_top_candidates(self, n: int = 3) -> List[Dict]:
        """Get top N candidates.
        
        Args:
            n: Number of top candidates to return
            
        Returns:
            List of top N candidates
            
        Raises:
            ValueError: If n is invalid
        """
        if n < 1:
            raise ValueError("n must be at least 1")
        
        if not self.rankings:
            raise RuntimeError("Rankings must be calculated first")
        
        return self.rankings[:n]
