from fastapi import UploadFile
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import PyPDF2
import json
import io
from ..config import settings
from .logging import candidate_logger

async def parse_resume(file: UploadFile) -> dict:
    try:
        # Read PDF content
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

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
            {
                "name": "",
                "email": "",
                "skills": [],
                "experience": {},
                "education": []
            }
            """
        )

        # Initialize LLM chain
        llm = OpenAI(api_key=settings.OPENAI_API_KEY)
        chain = LLMChain(llm=llm, prompt=prompt)

        # Process resume text
        result = chain.run(resume_text=text)
        parsed_data = json.loads(result)

        candidate_logger.info(f"Successfully parsed resume for {parsed_data['name']}")
        return parsed_data

    except Exception as e:
        candidate_logger.error(f"Error parsing resume: {str(e)}")
        raise Exception(f"Failed to parse resume: {str(e)}")