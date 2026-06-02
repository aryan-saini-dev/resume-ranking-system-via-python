"""CSV export module for ranking results."""

import csv
from typing import List, Dict
from pathlib import Path


class CSVExporter:
    """Exports ranking results to CSV format.
    
    This class handles writing ranking results to CSV files with proper
    formatting and error handling.
    """
    
    def __init__(self, output_dir: str = 'output') -> None:
        """Initialize CSVExporter with output directory.
        
        Args:
            output_dir: Directory to save CSV files (default: 'output')
        """
        self.output_dir = Path(output_dir)
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
    
    def export_results(self, rankings: List[Dict], filename: str = 'ranking_results.csv') -> str:
        """Export ranking results to CSV file.
        
        Args:
            rankings: List of ranking dictionaries with rank, candidate, and match_score
            filename: Output filename (default: 'ranking_results.csv')
            
        Returns:
            Path to the created CSV file
            
        Raises:
            ValueError: If rankings list is empty or invalid
            IOError: If file write fails
        """
        if not rankings or not isinstance(rankings, list):
            raise ValueError("Rankings must be a non-empty list")
        
        if len(rankings) == 0:
            raise ValueError("Rankings list cannot be empty")
        
        # Construct full file path
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Rank', 'Candidate', 'Match Score (%)']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for ranking in rankings:
                    writer.writerow({
                        'Rank': ranking['rank'],
                        'Candidate': ranking['candidate'],
                        'Match Score (%)': ranking['match_score']
                    })
            
            return str(filepath)
        
        except IOError as e:
            raise IOError(f"Failed to write CSV file: {str(e)}")
    
    def export_detailed_results(self, rankings: List[Dict], filename: str = 'ranking_results_detailed.csv') -> str:
        """Export detailed ranking results including similarity scores.
        
        Args:
            rankings: List of ranking dictionaries
            filename: Output filename
            
        Returns:
            Path to the created CSV file
            
        Raises:
            ValueError: If rankings list is empty or invalid
            IOError: If file write fails
        """
        if not rankings or not isinstance(rankings, list):
            raise ValueError("Rankings must be a non-empty list")
        
        if len(rankings) == 0:
            raise ValueError("Rankings list cannot be empty")
        
        # Construct full file path
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Rank', 'Candidate', 'Match Score (%)', 'Similarity Score']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for ranking in rankings:
                    writer.writerow({
                        'Rank': ranking['rank'],
                        'Candidate': ranking['candidate'],
                        'Match Score (%)': ranking['match_score'],
                        'Similarity Score': round(ranking.get('similarity', 0), 4)
                    })
            
            return str(filepath)
        
        except IOError as e:
            raise IOError(f"Failed to write CSV file: {str(e)}")
