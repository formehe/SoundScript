import requests

from config.secret import secret
from tts.voicetts import TTS

#X-Microsoft-OutputFormat:
#audio-16khz-16bit-32kbps-mono-opus
#audio-16khz-32kbitrate-mono-mp3
#audio-16khz-64kbitrate-mono-mp3
#audio-16khz-128kbitrate-mono-mp3
#audio-24khz-16bit-24kbps-mono-opus
#audio-24khz-16bit-48kbps-mono-opus
#audio-24khz-48kbitrate-mono-mp3
#audio-24khz-96kbitrate-mono-mp3
#audio-24khz-160kbitrate-mono-mp3
#audio-48khz-96kbitrate-mono-mp3
#audio-48khz-192kbitrate-mono-mp3
#ogg-16khz-16bit-mono-opus
#ogg-24khz-16bit-mono-opus
#ogg-48khz-16bit-mono-opus
#raw-8khz-8bit-mono-alaw
#raw-8khz-8bit-mono-mulaw
#raw-8khz-16bit-mono-pcm
#raw-16khz-16bit-mono-pcm
#raw-16khz-16bit-mono-truesilk
#raw-22050hz-16bit-mono-pcm
#raw-24khz-16bit-mono-pcm
#raw-24khz-16bit-mono-truesilk
#raw-44100hz-16bit-mono-pcm
#raw-48khz-16bit-mono-pcm
#webm-16khz-16bit-mono-opus
#webm-24khz-16bit-24kbps-mono-opus
#webm-24khz-16bit-mono-opus

#{
#    "Name": "Microsoft Server Speech Text to Speech Voice (bn-IN, BashkarNeural)", 
#    "DisplayName": "Bashkar", 
#    "LocalName": "ভাস্কর", 
#    "ShortName": "bn-IN-BashkarNeural", 
#    "Gender": "Male", 
#    "Locale": "bn-IN", 
#    "LocaleName": "Bengali (India)", 
#    "SampleRateHertz": "48000", 
#    "VoiceType": "Neural", 
#    "Status": "GA", 
#    "WordsPerMinute": "131"
#}

#{
#    "Name": "Microsoft Server Speech Text to Speech Voice (de-DE, FlorianMultilingualNeural)", 
#    "DisplayName": "Florian Multilingual", 
#    "LocalName": "Florian Mehrsprachig", 
#    "ShortName": "de-DE-FlorianMultilingualNeural", 
#    "Gender": "Male", 
#    "Locale": "de-DE", 
#    "LocaleName": "German (Germany)", 
#    "SecondaryLocaleList": [
#        "af-ZA", 
#        "am-ET", 
#        "ar-EG", 
#        "ar-SA", 
#        "az-AZ", 
#        "bg-BG", 
#        "bn-BD", 
#        "bn-IN", 
#        "bs-BA", 
#        "ca-ES", 
#        "cs-CZ", 
#        "cy-GB", 
#        "da-DK", 
#        "de-AT", 
#        "de-CH", 
#        "de-DE", 
#        "el-GR", 
#        "en-AU", 
#        "en-CA", 
#        "en-GB", 
#        "en-IE", 
#        "en-IN", 
#        "en-US", 
#        "es-ES", 
#        "es-MX", 
#        "et-EE", 
#        "eu-ES", 
#        "fa-IR", 
#        "fi-FI", 
#        "fil-PH", 
#        "fr-BE", 
#        "fr-CA", 
#        "fr-CH", 
#        "fr-FR", 
#        "ga-IE", 
#        "gl-ES", 
#        "he-IL", 
#        "hi-IN", 
#        "hr-HR", 
#        "hu-HU", 
#        "hy-AM", 
#        "id-ID", 
#        "is-IS", 
#        "it-IT", 
#        "ja-JP", 
#        "jv-ID", 
#        "ka-GE", 
#        "kk-KZ", 
#        "km-KH", 
#        "kn-IN", 
#        "ko-KR", 
#        "lo-LA", 
#        "lt-LT", 
#        "lv-LV", 
#        "mk-MK", 
#        "ml-IN", 
#        "mn-MN", 
#        "ms-MY", 
#        "mt-MT", 
#        "my-MM", 
#        "nb-NO", 
#        "ne-NP", 
#        "nl-BE", 
#        "nl-NL", 
#        "pl-PL", 
#        "ps-AF", 
#        "pt-BR", 
#        "pt-PT", 
#        "ro-RO", 
#        "ru-RU", 
#        "si-LK", 
#        "sk-SK", 
#        "sl-SI", 
#        "so-SO", 
#        "sq-AL", 
#        "sr-RS", 
#        "su-ID", 
#        "sv-SE", 
#        "sw-KE", 
#        "ta-IN", 
#        "te-IN", 
#        "th-TH", 
#        "tr-TR", 
#        "uk-UA", 
#        "ur-PK", 
#        "uz-UZ", 
#        "vi-VN", 
#        "zh-CN", 
#        "zh-HK", 
#        "zh-TW", 
#        "zu-ZA"
#    ], 
#    "SampleRateHertz": "24000", 
#    "VoiceType": "Neural", 
#    "Status": "GA", 
#    "WordsPerMinute": "190"
#}

class azure_tts(TTS):
    def __init__(self, config: secret):
        self.api_key = config.get("azure", "key")
        self.zone = config.get("azure", "zone")

        self.url = """https://{}.tts.speech.microsoft.com/cognitiveservices/v1""".format(self.zone)
        self.headers = {
            "Ocp-Apim-Subscription-Key": f"{self.api_key}",
            "User-Agent": "curl",
            "X-Microsoft-OutputFormat": "raw-16khz-16bit-mono-pcm",
            "Content-Type": "application/ssml+xml",
        }

        self.data = """<speak version="1.0" xml:lang="zh-CN" xmlns:mstts="https://www.w3.org/2001/mstts">
            <voice name="{}"><prosody rate="{}">{}</prosody></voice>
        </speak>"""
        
    def voices(self):
        get_url = """https://{}.tts.speech.microsoft.com/cognitiveservices/voices/list""".format(self.zone)
        get_headers = {
            "Ocp-Apim-Subscription-Key": f"{self.api_key}",
            "User-Agent": "curl"
        }
        
        response = requests.get(get_url, get_headers, timeout = 10)
        if response.status_code != 200:
            print("fail to get voice")
            return None

        voices = {}
        for voice in response.json():
            voices[voice["Gender"] +"_"+voice["ShortName"]]=voice["ShortName"]
        return voices

    def format_type(self):
        return "pcm"
    
    def generate(self, text, voiceId, speed:float=1.0):
        response = requests.post(self.url, data=self.data.format(voiceId, speed, text).encode("utf-8"), headers=self.headers, timeout = 10)
        if response.status_code != 200 or "json" in response.headers["Content-Type"]:
            print("调用失败", response.status_code, response.text)
            return None
        return response.content