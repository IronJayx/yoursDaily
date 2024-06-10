import os
import requests
import json
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class TextToSpeech:
    outbound_dir = "data/podcasts"
    outbound_format = ".mp3"

    def __init__(self, voice_id):
        self.voice_id = voice_id
        self.api_key = os.getenv("ELEVEN_LABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"
    
    def run(self, text, transcript_name, stability=0.3, similarity_boost=0.8, style=0.5, use_speaker_boost=True):
        url = f"{self.base_url}/{self.voice_id}/stream"
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost
            }
        }
        
        response = requests.post(url, headers=headers, json=data, stream=True)
        
        if response.ok:
            logger.info("Audio stream saved successfully.")
            return self._save_audio_stream(response, filename=transcript_name)
        else:
            logger.error(f"Error in text-to-speech synthesis: {response.text}")
            return False

    def _save_audio_stream(self, response, filename):
        os.makedirs(self.outbound_dir, exist_ok=True)

        full_path = os.path.join(self.outbound_dir, f"{filename}{self.outbound_format}")
        with open(full_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        return full_path
    
    @staticmethod
    def from_environment(output_path):
        voice_id = os.getenv("VOICE_ID")
        return TextToSpeech(voice_id, output_path)
