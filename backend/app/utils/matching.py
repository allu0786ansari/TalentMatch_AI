from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from .. import models
from typing import List
import numpy as np

def process_job_description(job_id: int) -> None:
    """
    Process and analyze job description after creation
    """
    # This function is called from the jobs router
    # Add your job processing logic here
    pass

def calculate_skill_match(required_skills: List[str], candidate_skills: List[str]) -> float:
    embeddings = OpenAIEmbeddings()
    
    # Convert skills to embeddings
    required_emb = embeddings.embed_documents(required_skills)
    candidate_emb = embeddings.embed_documents(candidate_skills)
    
    # Calculate cosine similarity
    similarity_scores = []
    for req_emb in required_emb:
        scores = [np.dot(req_emb, cand_emb) / (np.linalg.norm(req_emb) * np.linalg.norm(cand_emb))
                 for cand_emb in candidate_emb]
        similarity_scores.append(max(scores))
    
    return sum(similarity_scores) / len(similarity_scores)

def calculate_experience_match(required_years: int, candidate_experience: dict) -> float:
    total_years = sum(float(exp.get('years', 0)) for exp in candidate_experience.values())
    return min(total_years / required_years, 1.0)

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