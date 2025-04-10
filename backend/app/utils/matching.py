import google.generativeai as genai
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from .. import models
from typing import List
import numpy as np
from dotenv import load_dotenv
import os  # To load environment variables

# Load environment variables from .env file
load_dotenv()

# Define the embedding model to use
EMBEDDING_MODEL = "models/text-embedding-004"  # Replace with the best available model

def process_job_description(job_id: int) -> None:
    """
    Process and analyze job description after creation
    """
    # This function is called from the jobs router
    # Add your job processing logic here
    pass

def calculate_skill_match(required_skills: List[str], candidate_skills: List[str]) -> float:
    try:
        # Load the API key from the environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

        # Configure Gemini API
        genai.configure(api_key=api_key)

        # Convert skills to embeddings using Gemini, specifying the model
        required_emb = [genai.embed_content(model=EMBEDDING_MODEL, content=skill)["embedding"]
                        for skill in required_skills]
        candidate_emb = [genai.embed_content(model=EMBEDDING_MODEL, content=skill)["embedding"]
                         for skill in candidate_skills]

        # Handle potential empty lists
        if not required_emb or not candidate_emb:
            return 0.0

        # Calculate cosine similarity
        similarity_scores = []
        for req_emb in required_emb:
            # Ensure embeddings are valid numpy arrays before calculations
            req_emb_np = np.array(req_emb)
            scores = [np.dot(req_emb_np, np.array(cand_emb)) / (np.linalg.norm(req_emb_np) * np.linalg.norm(np.array(cand_emb)))
                      if np.linalg.norm(req_emb_np) > 0 and np.linalg.norm(np.array(cand_emb)) > 0 else 0.0
                      for cand_emb in candidate_emb]
            similarity_scores.append(max(scores) if scores else 0.0)

        # Return the average similarity score
        return sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0

    except Exception as e:
        # Log the original error for better debugging if needed
        raise ValueError(f"Error with Gemini API or calculation: {str(e)}")

def calculate_experience_match(required_years: int, candidate_experience: dict) -> float:
    try:
        # Ensure candidate_experience is a dictionary
        if not isinstance(candidate_experience, dict):
            raise ValueError("candidate_experience must be a dictionary.")

        # Calculate total years of experience
        total_years = sum(float(exp.get('years', 0)) for exp in candidate_experience.values())
        return min(total_years / required_years, 1.0)
    except Exception as e:
        raise ValueError(f"Error in calculate_experience_match: {str(e)}")

def calculate_match_score(job: models.JobDescription, candidate: models.Candidate) -> float:
    # Calculate different aspects of the match
    skill_score = calculate_skill_match(job.required_skills, candidate.skills)
    experience_score = calculate_experience_match(job.min_experience, candidate.experience)
    
    # Define weights for different aspects
    weights = {
        'skills': 0.6,
        'experience': 0.4
    }
    
    # Calculate final weighted score
    final_score = (
        skill_score * weights['skills'] +
        experience_score * weights['experience']
    )
    
    return round(final_score, 2)