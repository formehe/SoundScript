from io import BytesIO
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs
from config.secret import secret
from effectivesound.es import ES


class elevenlab_es(ES):
    def __init__(self, config: secret):
        self.api_key = config.get("elevenlab", "key")
        self.client = ElevenLabs(
            api_key=self.api_key,
            timeout=10,
        )
    
    def generate_sound(self, text:str):
        try:
            # Perform the text-to-speech conversion
            response = self.client.text_to_sound_effects.convert(
                text=text,
                duration_seconds=5,
                prompt_influence=0.3
            )
            
            # Create a BytesIO object to hold audio data
            audio_stream = BytesIO()

            # Write each chunk of audio data to the stream
            for chunk in response:
                if chunk:
                    audio_stream.write(chunk)

            # Reset stream position to the beginning
            audio_stream.seek(0)
        except Exception as e:
            print("generate sound Caught exception:", e)
        # Return the stream for further use
        
        if not audio_stream.getvalue() :
            print("fail to generate audio")
            return None, None
        audio = AudioSegment.from_mp3(BytesIO(audio_stream.getvalue()))
        return audio