from io import BytesIO
from pydub import AudioSegment
from config.secret import secret
from dao.audio_dao import Audio_DAO
from effectivesound.es import ES, STORE

class mysql_es(ES,STORE):
    def __init__(self, config: secret):
        self.dao = Audio_DAO(config)
    
    def generate_sound(self, text:str):
        raw_audio = self.dao.get_audio_by_description(text)
        audio = AudioSegment.from_mp3(BytesIO(raw_audio.audio_data))
        return audio
    
    def upload(self, text:str, audio: bytes):
        self.dao.add_audio(description=text, audio_data = audio)

    def get_sounds_information(self, text:str):
        return self.dao.get_all_audio_by_description(text)
            
    def get_sound_audio(self, text:str):
        return self.dao.get_audio_by_description(text)