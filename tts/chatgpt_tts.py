import requests
from config.secret import secret
from tts.voicetts import TTS

class chatgpt_tts(TTS):
    def __init__(self, config: secret):
        self.api_key = config.get("openai", "key")

        self.url = f"https://api.openai.com/v1/audio/speech"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
    def voices(self):
        return {
                "alloy":"alloy", 
                "echo":"echo", 
                "fable":"fable", 
                "onyx":"onyx", 
                "nova":"nova", 
                "shimmer":"shimmer"
        }
    
    def format_type(self):
        return "mp3"
    
    def generate(self, text, voiceId, speed:float=1.0):
        data = {
            "voice": f"{voiceId}",
            "input": f"{text}",
            "model": "tts-1-hd",
            "speed": speed,
        }

        response = requests.post(self.url, headers=self.headers, json=data, timeout = 10)
        if response.status_code != 200 or "json" in response.headers["Content-Type"]:
            print("调用失败", response.status_code, response.text)
            return None
        return response.content