"""
Ollama AI integration for Bible study assistance.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class OllamaAI:
    """Integration with Ollama for AI-assisted Bible study."""
    
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama2")
    
    def is_available(self):
        """Check if Ollama is available."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False
    
    def analyze_verse(self, verse_text, language="pt", context=""):
        """Analyze a Bible verse with AI assistance."""
        if not self.is_available():
            return {
                "success": False,
                "error": "Ollama AI is not available. Please make sure Ollama is running locally.",
                "message": "Install and run Ollama from https://ollama.ai"
            }
        
        prompt = self._build_analysis_prompt(verse_text, language, context)
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "analysis": result.get("response", "")
                }
            else:
                return {
                    "success": False,
                    "error": f"Ollama returned status code {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error communicating with Ollama: {str(e)}"
            }
    
    def answer_question(self, question, verse_text="", language="pt"):
        """Answer a question about a Bible verse or topic."""
        if not self.is_available():
            return {
                "success": False,
                "error": "Ollama AI is not available. Please make sure Ollama is running locally.",
                "message": "Install and run Ollama from https://ollama.ai"
            }
        
        prompt = self._build_question_prompt(question, verse_text, language)
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result.get("response", "")
                }
            else:
                return {
                    "success": False,
                    "error": f"Ollama returned status code {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error communicating with Ollama: {str(e)}"
            }
    
    def _build_analysis_prompt(self, verse_text, language, context):
        """Build a prompt for verse analysis."""
        lang_instruction = {
            "pt": "Responda em português.",
            "en": "Answer in English.",
            "es": "Responde en español.",
            "fr": "Répondez en français.",
            "de": "Antworten Sie auf Deutsch.",
        }.get(language, "Answer in English.")
        
        prompt = f"""You are a biblical scholar and theologian. Analyze the following Bible verse and provide insights.

Verse: "{verse_text}"

{f"Context: {context}" if context else ""}

Please provide:
1. A brief explanation of the verse's meaning
2. Historical and cultural context
3. Key theological themes
4. Practical application for modern readers

{lang_instruction}
"""
        return prompt
    
    def _build_question_prompt(self, question, verse_text, language):
        """Build a prompt for answering questions."""
        lang_instruction = {
            "pt": "Responda em português.",
            "en": "Answer in English.",
            "es": "Responde en español.",
            "fr": "Répondez en français.",
            "de": "Antworten Sie auf Deutsch.",
        }.get(language, "Answer in English.")
        
        prompt = f"""You are a biblical scholar and theologian. Answer the following question about the Bible.

Question: {question}

{f'Bible verse for reference: "{verse_text}"' if verse_text else ""}

Please provide a thoughtful, biblically-grounded answer.

{lang_instruction}
"""
        return prompt
