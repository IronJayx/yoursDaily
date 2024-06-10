import os
import requests
import json
import tiktoken
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class llmClient:
    def __init__(self):
        self.messages = []
    
    def add_message(self, text, role="user"):
        num_tokens = self.num_tokens_from_string(text, "o200k_base")
        if num_tokens > 2000:
            # Split the text into chunks if it's too long
            chunks = self.split_text_into_chunks(text, 2000)
            for chunk in chunks:
                self.messages.append({"role": role, "content": chunk})
        else:
            self.messages.append({"role": role, "content": text})

    def answer(self, max_length=4096):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": self.messages,
            "max_tokens": max_length,
            "temperature": 0.7,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95,
            "stop": None
        }

        response = requests.post(os.environ.get('OPENAI_CHAT_ENDPOINT_URL'), headers=headers, data=json.dumps(data))
        content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()

        if not content or len(content) < 3:
            logger.error(response.json())
            return
        
        return content


    @staticmethod
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    @staticmethod
    def split_text_into_chunks(text: str, max_tokens: int):
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk = encoding.decode(tokens[i:i + max_tokens])
            chunks.append(chunk)
        return chunks
