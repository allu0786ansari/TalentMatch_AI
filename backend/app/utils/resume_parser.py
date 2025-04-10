from fastapi import UploadFile
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pypdf import PdfReader
import json
import io
from ..config import settings
from .logging import candidate_logger

# Define a mock Gemini class for the purpose of testing
class Gemini:
    def __init__(self, api_key: str, temperature: float, model_name: str):
        self.api_key = api_key
        self.temperature = temperature
        self.model_name = model_name

    def run(self, resume_text: str) -> str:
        # Mock implementation for testing
        return json.dumps({
            "name": "John Doe",
            "email": "john.doe@example.com",
            "skills": ["Python", "FastAPI"],
            "experience": {"Tech Co": 4},
            "education": [{"degree": "BSc Computer Science", "institution": "Test University"}]
        })

async def parse_resume(file: UploadFile, llm: Gemini) -> dict:
    try:
        # Read PDF content
        content = await file.read()
        if not isinstance(content, (bytes, bytearray)):
            raise TypeError("Uploaded file content must be bytes-like.")

        pdf_reader = PdfReader(io.BytesIO(content))

        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text

        if not text.strip():
            raise ValueError("The uploaded PDF contains no readable text.")

        # Define prompt template for GPT
        prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
            Extract the following information from the resume text in JSON format:
            - Full Name
            - Email Address
            - Skills (as a list)
            - Work Experience (as a dictionary with company names as keys and years as values)
            - Education (as a list of dictionaries with 'degree' and 'institution')

            Resume text: {resume_text}

            Response Format:
            {{
                "name": "",
                "email": "",
                "skills": [],
                "experience": {},
                "education": []
            }}
            """
        )

        # Initialize LLM chain with the provided llm instance
        chain = LLMChain(llm=llm, prompt=prompt)

        # Process resume text
        result = chain.run(resume_text=text)
        parsed_data = json.loads(result)

        candidate_logger.info(f"Successfully parsed resume for {parsed_data.get('name', 'Unknown')}")
        return parsed_data

    except json.JSONDecodeError as e:
        candidate_logger.error(f"Error parsing JSON response: {str(e)}")
        raise Exception("Failed to parse LLM response into JSON format")
    except Exception as e:
        candidate_logger.error(f"Error parsing resume: {str(e)}")
        raise Exception(f"Failed to parse resume: {str(e)}")