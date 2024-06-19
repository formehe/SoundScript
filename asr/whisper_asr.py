from transformers import (pipeline, AutoFeatureExtractor, AutoProcessor, AutoTokenizer)
import torch
from asr.asr import ASR
import librosa
import torchaudio
import numpy as np
from io import BytesIO
from pydub import AudioSegment
import pydub

# todo
class whisper_asr(ASR):
    pipe              = None
    feature_extractor = None
    processor         = None
    tokenizer         = None
    
    def __init__(self):
        model_id = "openai/whisper-large-v3"  # update with your model id
        #self.pipe = pipeline("automatic-speech-recognition", model=model_id, return_timestamps = True)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(model_id)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        self.pipe = pipeline(
            "automatic-speech-recognition", 
            model=model_id, 
            return_timestamps = 'word',
            #feature_extractor = self.feature_extractor,
            device_map = "auto",
            return_language = True)
    
    def recognize(self, audio_path):
        audio_segment = AudioSegment.from_file(audio_path, format="mp3")
        not_silence_ranges = pydub.silence.split_on_silence(audio_segment, 
                                    min_silence_len=550,
                                    silence_thresh=-40, 
                                    keep_silence=550)
        
        transcribe = {"text":"", "chunks":[]}
        
        for segment in not_silence_ranges:
            audio_byte_array = BytesIO()
            segment.export(audio_byte_array, format="mp3")
            audio_byte_array.seek(0)
            
            audio, _ = torchaudio.load(audio_byte_array)
            
            audio = audio.mean(dim=0).numpy()
            output = self.pipe(
                audio,
                max_new_tokens=256,
                generate_kwargs={
                    "task": "transcribe",
                    "language": "chinese",
                },  # update with the language you've fine-tuned on
                chunk_length_s=30,
                batch_size=8,
            )
            transcribe["text"]= transcribe["text"] + output["text"]
            transcribe["chunks"].append(output["chunks"])
            audio_byte_array.close()
            print(output)
        
        return transcribe