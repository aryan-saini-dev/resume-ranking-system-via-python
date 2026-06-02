"""Main Streamlit application for Resume Ranking System."""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List, Optional
import io
from modules.ranker import ResumeRanker
from modules.exporter import CSVExporter

# Configure page
st.set_page_config(
    page_title="Resume Ranking System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .header-text {
        color: #1f77b4;
        font-size: 28px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def load_uploaded_file(uploaded_file) -> str:
    """Load content from uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        File content as string
    """
    if uploaded_file is None:
        return ""
    return uploaded_file.read().decode('utf-8')


def extract_candidate_name(filename: str) -> str:
    """Extract candidate name from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        Cleaned candidate name
    """
    # Remove extension and clean up
    name = filename.replace('.txt', '').replace('_resume', '').replace('_', ' ')
    return name.title()


def create_ranking_dataframe(rankings: List[Dict]) -> pd.DataFrame:
    """Create a pandas DataFrame from rankings.
    
    Args:
        rankings: List of ranking dictionaries
        
    Returns:
        Pandas DataFrame with rankings
    """
    data = [
        {
            'Rank': r['rank'],
            'Candidate': r['candidate'],
            'Match Score (%)': f"{r['match_score']}%"
        }
        for r in rankings
    ]
    return pd.DataFrame(data)


def create_visualization(rankings: List[Dict]) -> None:
    """Create and display ranking visualization.
    
    Args:
        rankings: List of ranking dictionaries
    """
    df = pd.DataFrame(rankings)
    
    # Create bar chart
    fig = px.bar(
        df,
        x='candidate',
        y='match_score',
        title='Resume Ranking by Match Score',
        labels={'candidate': 'Candidate', 'match_score': 'Match Score (%)'},
        color='match_score',
        color_continuous_scale='Viridis',
        text='match_score',
        height=500
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        xaxis_title='Candidate Name',
        yaxis_title='Match Score (%)',
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    """Main application function."""
    
    # Header
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        st.emoji(":clipboard:")
    with col2:
        st.title("Intelligent Resume Ranking System")
    
    st.markdown("""
    Analyze and rank candidate resumes based on job description match using
    **TF-IDF** and **Cosine Similarity** algorithms.
    """)
    
    st.divider()
    
    # Sidebar for file uploads
    with st.sidebar:
        st.header("📤 Upload Files")
        
        # Job Description Upload
        st.subheader("Job Description")
        job_desc_file = st.file_uploader(
            "Upload Job Description (TXT)",
            type=['txt'],
            key='job_desc',
            help="Upload the job description file"
        )
        
        st.divider()
        
        # Resumes Upload
        st.subheader("Candidate Resumes")
        resume_files = st.file_uploader(
            "Upload Resumes (TXT)",
            type=['txt'],
            accept_multiple_files=True,
            key='resumes',
            help="Upload multiple resume files (minimum 2 resumes)"
        )
        
        st.divider()
        st.info(
            "📌 **Tips:**\n"
            "• Ensure all files are in TXT format\n"
            "• Minimum 2 resumes required\n"
            "• Files should contain clear text content"
        )
    
    # Main content area
    if job_desc_file is None:
        st.warning("⚠️ Please upload a job description to get started.")
        return
    
    if not resume_files or len(resume_files) < 2:
        st.warning("⚠️ Please upload at least 2 resume files.")
        return
    
    # Load files
    job_description = load_uploaded_file(job_desc_file)
    
    if not job_description.strip():
        st.error("❌ Job description file is empty. Please upload a valid file.")
        return
    
    # Create resumes dictionary
    resumes: Dict[str, str] = {}
    for resume_file in resume_files:
        candidate_name = extract_candidate_name(resume_file.name)
        resume_content = load_uploaded_file(resume_file)
        
        if resume_content.strip():
            resumes[candidate_name] = resume_content
    
    if len(resumes) < 2:
        st.error("❌ At least 2 valid resume files required. Please upload files with content.")
        return
    
    # Display job description preview
    with st.expander("📄 Job Description Preview", expanded=False):
        st.text_area(
            "Job Description",
            value=job_description[:500] + "..." if len(job_description) > 500 else job_description,
            height=150,
            disabled=True,
            label_visibility="collapsed"
        )
    
    # Perform ranking
    st.subheader("🔄 Analyzing Resumes...")
    
    try:
        with st.spinner("Calculating similarity scores..."):
            # Initialize ranker and rank resumes
            ranker = ResumeRanker(job_description, resumes)
            rankings = ranker.rank_resumes()
        
        st.success("✅ Ranking complete!")
        
        # Display metrics
        st.divider()
        st.subheader("📊 Summary Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Candidates", len(rankings))
        
        with col2:
            avg_score = sum(r['match_score'] for r in rankings) / len(rankings)
            st.metric("Average Match", f"{avg_score:.1f}%")
        
        with col3:
            top_score = rankings[0]['match_score']
            st.metric("Highest Match", f"{top_score:.1f}%")
        
        with col4:
            bottom_score = rankings[-1]['match_score']
            st.metric("Lowest Match", f"{bottom_score:.1f}%")
        
        st.divider()
        
        # Display ranking table
        st.subheader("🏆 Candidate Rankings")
        
        ranking_df = create_ranking_dataframe(rankings)
        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        # Display visualization
        st.subheader("📈 Match Score Visualization")
        create_visualization(rankings)
        
        st.divider()
        
        # Export options
        st.subheader("💾 Export Results")
        
        col1, col2 = st.columns(2)
        
        # CSV Export
        with col1:
            try:
                exporter = CSVExporter()
                
                # Create CSV in memory
                csv_buffer = io.StringIO()
                csv_df = pd.DataFrame([
                    {
                        'Rank': r['rank'],
                        'Candidate': r['candidate'],
                        'Match Score (%)': r['match_score']
                    }
                    for r in rankings
                ])
                csv_df.to_csv(csv_buffer, index=False)
                csv_content = csv_buffer.getvalue()
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_content,
                    file_name="ranking_results.csv",
                    mime="text/csv",
                    help="Download ranking results as CSV file"
                )
            except Exception as e:
                st.error(f"Error preparing CSV export: {str(e)}")
        
        # Detailed Export
        with col2:
            try:
                detailed_csv_buffer = io.StringIO()
                detailed_df = pd.DataFrame([
                    {
                        'Rank': r['rank'],
                        'Candidate': r['candidate'],
                        'Match Score (%)': r['match_score'],
                        'Similarity Score': f"{r['similarity']:.4f}"
                    }
                    for r in rankings
                ])
                detailed_df.to_csv(detailed_csv_buffer, index=False)
                detailed_content = detailed_csv_buffer.getvalue()
                
                st.download_button(
                    label="📥 Download Detailed CSV",
                    data=detailed_content,
                    file_name="ranking_results_detailed.csv",
                    mime="text/csv",
                    help="Download detailed results including similarity scores"
                )
            except Exception as e:
                st.error(f"Error preparing detailed CSV export: {str(e)}")
        
        st.divider()
        
        # Display top candidate details
        st.subheader("⭐ Top Candidate")
        top_candidate = rankings[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rank", "🥇 1st")
        with col2:
            st.metric("Candidate", top_candidate['candidate'])
        with col3:
            st.metric("Match Score", f"{top_candidate['match_score']}%")
        
    except Exception as e:
        st.error(f"❌ Error during ranking: {str(e)}")
        st.info("Please check your uploaded files and try again.")


if __name__ == "__main__":
    main()
