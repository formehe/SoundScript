import whisper_timestamped as whisper
import torch
from asr.asr import ASR
import torchaudio
from io import BytesIO
from pydub import AudioSegment, silence

#timestamp mark
class timestamped_whisper_asr(ASR):
    model             = None
    
    def __init__(self):
        model_id = "openai/whisper-large-v3"
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.model = whisper.load_model(model_id)#, device="cpu")
        
    def __split__(self, audio_path, tail_silence_duration):
        audio = AudioSegment.from_file(audio_path, format="mp3")
        audio = audio.set_frame_rate(16*1000)
        segments = silence.detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-35)
        silence_segment = AudioSegment.silent(duration=tail_silence_duration)
        chunks = []
        pre_start = 0
        for _, end in segments:
            chunks.append(audio[pre_start:end]+silence_segment)
            pre_start = end
        return chunks
            
    def recognize(self, audio_path): 
        not_silence_ranges = self.__split__(audio_path, 500)
        transcribe = {"text":"", "words":[], "langs":[]}
        duration_seconds = 0.0
        for segment in not_silence_ranges:
            audio_byte_array = BytesIO()
            segment.export(audio_byte_array, format="mp3")
            audio_byte_array.seek(0)
            
            audio, sr = torchaudio.load(audio_byte_array)
            audio = audio.mean(dim=0).numpy()
            try:
                result = whisper.transcribe(
                        self.model, 
                        audio, 
                        condition_on_previous_text=True,
                        #initial_prompt="以下是普通話的句子,请以简体输出。",
                        initial_prompt="ignore the background sound of the music and only transcribe the part with the human voice.",
                        #initial_prompt="ignore noise, white space, musical background sounds, and transcribe the part that speaks.",
                        #initial_prompt="This is a meeting, transcribe the voice of the conversation in the meeting and ignore the noise.",
                        seed = 123,
                        remove_empty_words = True,
                        beam_size = 5,
                        no_speech_threshold = 0.8,
                        vad = True
                )
                
                transcribe["text"] = transcribe["text"] + result["text"]
                transcribe["langs"].append(result["language"])
                for segment_i in result["segments"]:
                    for word in segment_i["words"]:
                        word["start"] = word["start"] + duration_seconds
                        word["end"] = word["end"] + duration_seconds
                        transcribe["words"].append(word)
                audio_byte_array.close()
            except AssertionError as error:
                print(f"捕获到 AssertionError：{error}")
            except Exception as exception:
                print(f"捕获到 Exception{exception}")
            finally:                
                # 转换为秒，精度优化
                duration_seconds = duration_seconds + (len(segment) - 500) / 1000.0
                
        return transcribe