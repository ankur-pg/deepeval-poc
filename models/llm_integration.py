"""
LLM Model integration for DeepEval testing
"""
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class GeminiModel:
    """Wrapper for Google Gemini model integration"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate_response(self, prompt: str, data_payload: Dict[str, Any]) -> str:
        """
        Generate response using Gemini model
        
        Args:
            prompt: The analysis prompt template
            data_payload: Real estate data to analyze
            
        Returns:
            Generated analysis response
        """
        try:
            # Format the prompt with data
            formatted_prompt = prompt.format(data_payload=json.dumps(data_payload, indent=2))
            
            # Generate response
            response = self.model.generate_content(formatted_prompt)
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def __call__(self, prompt: str) -> str:
        """Make the class callable for deepeval compatibility"""
        return self.generate_response(prompt, {})


def load_prompt_template() -> str:
    """Load the real estate analysis prompt template"""
    prompt_path = "prompts/real_estate_analysis_prompt.txt"
    
    with open(prompt_path, 'r', encoding='utf-8') as file:
        return file.read()


def create_test_input(data_payload: Dict[str, Any]) -> str:
    """Create formatted test input with data payload"""
    prompt_template = load_prompt_template()
    return prompt_template.format(data_payload=json.dumps(data_payload, indent=2))
