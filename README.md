# SmartRecruit-AI

**A Scalable, AI-Powered Recruitment Automation Platform**

---

## Overview

**SmartRecruit-AI** is an end-to-end recruitment automation system designed to streamline and optimize the hiring process for modern organizations. Leveraging AI, NLP, and scalable backend technologies, it automates job description parsing, resume parsing, candidate-job matching, interview scheduling, and notifications—all via a robust API and a responsive, user-friendly React.js frontend.

---

## Features

### Backend (Python, FastAPI, Gemini, LangChain, RabbitMQ)

- **Automated Recruitment Workflow:**  
  End-to-end automation of job posting, candidate application, parsing, matching, and scheduling.
- **AI-Powered Resume Parsing:**  
  Utilizes Google Generative AI APIs and LangChain for advanced NLP-based extraction of structured data from resumes.
- **Intelligent Candidate Matching:**  
  Custom scoring algorithm matches candidates to job descriptions based on skills, experience, and qualifications.
- **Scalable & Reliable Architecture:**  
  Asynchronous task handling using RabbitMQ for email notifications and background processes.
- **Database Management:**  
  Uses SQLAlchemy for ORM and robust data handling.
- **Configuration Management:**  
  Managed via Pydantic for type-safe, environment-based configurations.
- **Testing & Quality Assurance:**  
  Comprehensive unit tests for all modules (jobs, candidates, matches, interviews) using Pytest.

### Frontend (React.js)

- **Intuitive Dashboard:**  
  Visualize and manage job postings, candidate pipelines, and interview schedules.
- **Job Posting Management:**  
  Create, edit, and archive job descriptions with rich text support.
- **Resume Upload & Parsing:**  
  Candidates can upload resumes; parsed data is displayed for review and editing.
- **Candidate Matching Visualization:**  
  View AI-generated candidate-job match scores and detailed breakdowns.
- **Interview Scheduling:**  
  Schedule interviews with calendar integration and automated email notifications.
- **Real-Time Notifications:**  
  Receive instant updates on candidate status, interview confirmations, and more.
- **Admin & Recruiter Roles:**  
  Role-based access controls for different user types.
- **Responsive Design:**  
  Mobile-friendly UI for recruiters and candidates on the go.

---

## Tech Stack

- **Backend:** Python, FastAPI, LangChain, Gemini (Google Generative AI APIs), SQLAlchemy, Pydantic, RabbitMQ, Pytest
- **Frontend:** React.js, Redux Toolkit, Material UI, Axios
- **Database:** mysqllite
- **Messaging:** RabbitMQ

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- RabbitMQ
- PostgreSQL

### Backend Setup
- git clone https://github.com/yourusername/smartrecruit-ai.git
- cd smartrecruit-ai/backend
- pip install -r requirements.txt
- cp .env.example .env # Update environment variables
- uvicorn app.main:app --reload

### Frontend Setup
- cd ../frontend
- npm install
- npm start
  
### Testing the each modules using pytest

