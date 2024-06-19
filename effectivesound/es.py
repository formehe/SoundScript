from config.secret import secret
class ES:
    def __init__(self, config:secret):
        pass

    def generate_sound(self, text:str):
        pass

class STORE:
    def __init__(self):
        pass
    
    def upload(self, text:str, audio: bytes):
        pass

    def get_sounds_information(self, text:str):
        pass
            
    def get_sound_audio(self, text:str):
        pass