import logging
from datetime import datetime
import os
from pathlib import Path

class CustomLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create handlers
        file_handler = logging.FileHandler(
            f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        console_handler = logging.StreamHandler()
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        self.logger.info(message)
        
    def error(self, message: str):
        self.logger.error(message)
        
    def warning(self, message: str):
        self.logger.warning(message)
        
    def debug(self, message: str):
        self.logger.debug(message)

# Create logger instances for different components
job_logger = CustomLogger("jobs")
candidate_logger = CustomLogger("candidates")
matching_logger = CustomLogger("matching")
interview_logger = CustomLogger("interviews")