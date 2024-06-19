from io import BytesIO

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

from config.secret import secret
from tts.voicetts import TTS

#mp3_22050_32 - output format, mp3 with 22.05kHz sample rate at 32kbps
#pcm_16000 - PCM format (S16LE) with 16kHz sample rate
#ulaw_8000 - μ-law format (sometimes written mu-law, often approximated as u-law) with 8kHz sample rate.
#mp3_22050_32
#mp3_44100_32
#mp3_44100_64
#mp3_44100_96
#mp3_44100_128
#mp3_44100_192
#pcm_16000
#pcm_22050
#pcm_24000
#pcm_44100
#ulaw_8000

#{
#	"voice_id": "JBFqnCBsd6RMkjVDRZzb",
#	"name": "George",
#	"samples": null,
#	"category": "premade",
#	"fine_tuning": {
#		"is_allowed_to_fine_tune": true,
#		"finetuning_state": "fine_tuned",
#		"verification_failures": [],
#		"verification_attempts_count": 0,
#		"manual_verification_requested": false,
#		"language": "en",
#		"finetuning_progress": {},
#		"message": null,
#		"dataset_duration_seconds": null,
#		"verification_attempts": null,
#		"slice_ids": null,
#		"manual_verification": null
#	},
#	"labels": {
#		"accent": "british",
#		"description": "warm",
#		"age": "middle-aged",
#		"gender": "male",
#		"use case": "narration"
#	},
#	"description": null,
#	"preview_url": "https://storage.googleapis.com/eleven-public-prod/premade/voices/JBFqnCBsd6RMkjVDRZzb/365e8ae8-5364-4b07-9a3b-1bfb4a390248.mp3",
#	"available_for_tiers": [],
#	"settings": null,
#	"sharing": null,
#	"high_quality_base_model_ids": ["eleven_turbo_v2"],
#	"safety_control": null,
#	"voice_verification": {
#		"requires_verification": false,
#		"is_verified": false,
#		"verification_failures": [],
#		"verification_attempts_count": 0,
#		"language": null,
#		"verification_attempts": null
#	},
#	"owner_id": null,
#	"permission_on_resource": null
#}

class elevenlab_tts(TTS):
    def __init__(self, config: secret):
        self.api_key = config.get("elevenlab", "key")
        self.client = ElevenLabs(
            api_key=self.api_key,
            timeout=10,
        )

    def voices(self):
        voices_detail = self.client.voices.get_all()
        voices= {}
        for voice in voices_detail.voices:
            if "gender" not in voice.labels:
                voices[voice.name]=voice.voice_id
            else:
                voices[voice.labels["gender"]+"-"+voice.name]=voice.voice_id

        return voices
    
    def format_type(self):
        return "mp3"
    
    def generate(self, text, voiceId, speed:float=1.0):
        """
        Converts text to speech and returns the audio data as a byte stream.

        This function invokes a text-to-speech conversion API with specified parameters, including
        voice ID and various voice settings, to generate speech from the provided text. Instead of
        saving the output to a file, it streams the audio data into a BytesIO object.

        Args:
            text (str): The text content to be converted into speech.

        Returns:
            IO[bytes]: A BytesIO stream containing the audio data.
        """
        try:
            # Perform the text-to-speech conversion
            response = self.client.text_to_speech.convert(
                voice_id = voiceId,  # Adam pre-made voice
                optimize_streaming_latency="0",
                output_format="mp3_22050_32",
                #output_format="pcm_16000",
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.8,
                    style=0.0,
                    use_speaker_boost=True,
                ),
                seed = 123,
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
            print("generate voice Caught exception:", e, voiceId)
        # Return the stream for further use
        return audio_stream.getvalue()