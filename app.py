import re
import io
import argparse
import tempfile
import numpy as np
import gradio as gr
import pandas as pd

from bs4 import BeautifulSoup
from pydub import AudioSegment, silence

from config.secret import secret
from tts.chatgpt_tts import chatgpt_tts
from tts.elevenlab_tts import elevenlab_tts
from tts.v2_minimax_tts import v2_minimax_tts
from tts.minimax_tts import minimax_tts
from tts.azure_tts import azure_tts
from asr.timestamped_whisper_asr import timestamped_whisper_asr as whisper_asr
from effectivesound.elevenlab_es import elevenlab_es
from effectivesound.mysql_es import mysql_es
from nlp.chatgpt_speakers import *

# <backgroundaudio src="mysql://街道声" volume="+5" fadein="500" fadeout="500">
# 阳光透过高楼间的缝隙，洒在熙熙攘攘的街道上。人声鼎沸，汽车的喇叭声此起彼伏，小贩的叫卖声和过往行人的交谈声交织在一起，
# 构成了这座城市独有的交响乐。杰克穿梭在人群中，眉头紧锁，他的目光在寻找着什么，或是在逃避着什么。
# 突然，他的目光定格在街角的一家古董店。店铺的门面并不显眼，但那扇半掩的木门却仿佛有着魔力，吸引着他不由自主地走了进去。
# <backgroundaudio src="prompt://After people walked into the room, the door closed with a squeak" volume="+5" fadein="500" fadeout="500">
# </backgroundaudio>
# </backgroundaudio>
# 隔绝了外界的喧嚣。店内灯光昏暗，空气中弥漫着旧书和古木的混合香味，一切都显得异常静谧。
    
def splitChapter(text, progress=gr.Progress(track_tqdm=True)):
    #segments = re.findall(r'“([^“”]*)”|([^“”？。！]*)|"([^"]*)"|([^"?.!]*)', text)
    #segments = re.findall(r'["“]([^"“”]*)["”]|([^"“”？。！?.!]*)', text)
    segments = re.findall(r'["“]([^"“”<]*)["”]|([^<"“”？。！?.!]*)|(<[^<]*>)', text)
    data =  {"role":[], "content": []}
    data1 =  {"role":[], "voice id": []}
    data1["role"].append("旁白")
    data1["voice id"].append("audiobook_female_1")
    for segment in progress.tqdm(segments, "generating"):
        if segment[0] :
            role = nlp.recognize_dialog_speaker(text, segment[0].strip())
            data["role"].append(role)
            data["content"].append(segment[0].strip())
            data1["role"].append(role)
            data1["voice id"].append("")
        if segment[1]:
            data["content"].append(segment[1].strip())
            data["role"].append("旁白")
        if segment[2]:
            data["content"].append(segment[2].strip())
            data["role"].append("标签")
    df = pd.DataFrame(data)
    df1 = pd.DataFrame(data1)
    df1_uni = df1.drop_duplicates(subset=['role'], keep='first')
    return df1_uni,df

def insert_background(original_audio, background_audio, insert_position):
    original_audio = AudioSegment.from_mp3(original_audio)
    insert_audio = AudioSegment.from_mp3(background_audio)
    position = int(insert_position * 1000)  # 将秒转换为毫秒
    edited_audio = original_audio.overlay(insert_audio, position=position)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
        edited_audio.export(fp.name, format="mp3")
        out_path = fp.name
    return out_path

def generate_sound(prompt):
    audio1 = sounds_models["prompt"].generate_sound(prompt)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
        audio1.export(fp.name, format="mp3")
        out_path = fp.name
        return out_path, out_path
    
def __merge_background(stack):
    local_stack=[]
    audio = None
    while stack:
        tmp = stack.pop()
        if tmp["type"] != "标签":
            local_stack.append(tmp)
        else:
            soup = BeautifulSoup(tmp["value"], 'html.parser')
            # 查找所有<mstts:backgroundaudio>标签
            backgroundaudio_tags = soup.find_all('backgroundaudio')
            if 'src' not in backgroundaudio_tags[0].attrs:
                return None
            
            location = backgroundaudio_tags[0]['src']
            match = re.match(r'(\w+)://(.+)', location)
            if match:
                schema, description = match.groups()
                
                if schema == "mysql" or schema == "prompt": 
                    audio = sounds_models[schema].generate_sound(description)
                else:
                    print("not support")
                    return None
            else:
                print("Invalid URL format")
                return None
            
            start_end = silence.detect_silence(audio, 500, -50, 1)
            soundstat = 0
            soundend = len(audio)
            for o in start_end:
                if o[1] == len(audio):
                    soundend = o[0]
                if o[0] == 0:
                    soundstat = o[1]
            audio = audio[soundstat:soundend]
            audio = audio.apply_gain(float(backgroundaudio_tags[0]['volume']))
            break
        
    combined_audio = None
    while local_stack:
        audio1 = local_stack.pop()
        if combined_audio is None:
            combined_audio = audio1["value"]
        else:
            combined_audio += audio1["value"]
            
    if audio is None:
        return combined_audio
            
    if combined_audio is not None and audio is not None:
        num_loops = len(combined_audio) // len(audio) + 1
        backgroundaudio = audio.fade_in(int(backgroundaudio_tags[0]['fadein']))
        for _ in range(num_loops - 1):
            backgroundaudio = backgroundaudio.append(audio, crossfade=800)
        backgroundaudio = backgroundaudio.fade_out(int(backgroundaudio_tags[0]['fadeout']))
        audio =  backgroundaudio

        if 'channel' in backgroundaudio_tags[0].attrs:
            empty = AudioSegment.silent(duration= len(combined_audio))
            audio = empty.overlay(audio, position=0)
            audio = audio.pan(float(backgroundaudio_tags[0]['channel']))
            combined_audio = combined_audio.pan(float(backgroundaudio_tags[0]['channel']) * -1)
            audio = combined_audio.overlay(audio, position=0)
        else:
            audio = combined_audio.overlay(audio * num_loops, position=0)
    elif audio is not None:
        backgroundaudio = audio.fade_in(int(backgroundaudio_tags[0]['fadein']))
        backgroundaudio = backgroundaudio.fade_out(int(backgroundaudio_tags[0]['fadeout']))
        audio = backgroundaudio
        if 'channel' in backgroundaudio_tags[0].attrs:
            audio = audio.pan(float(backgroundaudio_tags[0]['channel']))
            
    return audio
    

def run_tts(dataFrame, roleFrame, model, speed, progress=gr.Progress(track_tqdm=True)):
    combined_audio = None
    progress(0, desc="开始...")
    global_stack = []
    for row in progress.tqdm(dataFrame.values, "generating"):
        if row[0] == "标签":
            if row[1].startswith("</"):
                global_stack.append({"type":"音频", "value":__merge_background(global_stack)})
            else:
                global_stack.append({"type":"标签", "value":row[1]})
            continue
        voice = roleFrame.loc[roleFrame['role']==row[0], 'voice id'].iloc[0]
        segments = re.findall(r'[^:,]+', voice)
        if len(segments) == 0:
            return None,None
        elif (len(segments) == 1):
            audio = models[model].generate(row[1], voice, speed)
        else :
            voiceIds = []
            weights = []
            for i, segment in enumerate(segments):
                if i % 2 != 0:
                    weights.append(int(segment))
                else:
                    voiceIds.append(segment)
                    
            audio = models[model].generate_mix(row[1], voiceIds, weights, speed)
        
        if not audio :
            print("fail to generate audio")
            return None, None
        if models[model].format_type() == "mp3":
            audio1 = AudioSegment.from_mp3(io.BytesIO(audio))
        else:
            audio1 = AudioSegment.from_raw(io.BytesIO(audio), sample_width=2, frame_rate=16000, channels=1)
        global_stack.append({"type":"音频", "value":audio1})
            
    combined_audio = __merge_background(global_stack)  
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
        combined_audio.export(fp.name, format="mp3")
        out_path = fp.name
    return out_path, out_path

def change_model(model):
    return gr.Dropdown(choices=list(models[model].voices().keys()), value=list(models[model].voices().keys())[0], interactive=True)

def display(model,voice):
    return models[model].voices()[voice]

def recognize_audio(audio):
    recognized_text = whisper_asr().recognize(audio)
    return recognized_text

def upload_audio(audio, text):
    audio = AudioSegment.from_mp3(audio)
    buffer = io.BytesIO()
    audio.export(buffer, format="mp3")
    sounds_models["mysql"].upload(text, buffer.getvalue())
    
def get_audio(text):
    sounds = sounds_models["mysql"].get_sounds_information(text)
    data =  {"id":[], "description":[]}
    if len(sounds) == 0:
        return None,(None,np.array([]))
    for sound in sounds:
        data["id"].append(sound[0])
        data["description"].append(sound[1])
    df = pd.DataFrame(data)
    
    raw_audio = sounds_models["mysql"].get_sound_audio(sounds[0][1])
    
    # 使用AudioSegment读取音频数据
    audio_segment = AudioSegment.from_mp3(io.BytesIO(raw_audio.audio_data))
    
    # # 获取采样率
    sample_rate = audio_segment.frame_rate
    # 将AudioSegment转换为NumPy数组
    samples = audio_segment.get_array_of_samples()
    numpy_array = np.array(samples)
    
    return df, (sample_rate, numpy_array)

def on_row_click(evt: gr.SelectData, df: pd.DataFrame):
    row = evt.index[0]
    
    raw_audio = sounds_models["mysql"].get_sound_audio(df.iloc[row][1])
    audio_segment = AudioSegment.from_mp3(io.BytesIO(raw_audio.audio_data))
    if audio_segment.channels == 2:
        audio_segment = audio_segment.split_to_mono()[0]  # 只选择一个声道     
    
    ## 获取采样率
    sample_rate = audio_segment.frame_rate
    # 将AudioSegment转换为NumPy数组
    samples = audio_segment.get_array_of_samples()
    numpy_array = np.array(samples)
    return (sample_rate, numpy_array)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='启动参数')

    # 添加命令行选项
    parser.add_argument(
        '--config', 
        type = str,
        required=True,
        help='配置路径位置'
    )
    
    # 解析命令行参数
    args = parser.parse_args()
    config = secret(args.config)
    
    models = {
        "minimax":minimax_tts(config),
        "minimax_v2":v2_minimax_tts(config),
        "elevenlab":elevenlab_tts(config),
        "openai":chatgpt_tts(config),
        "azure":azure_tts(config)
    }
    
    sounds_models = {
        "prompt": elevenlab_es(config),
        "mysql": mysql_es(config)
    }
    
    nlp = chatgpt_speakers(config)
    
    with gr.Blocks() as demo:
        with gr.Tab("1 - Text to speech"):
            model = gr.Dropdown(choices=list(models.keys()), label='model', value=list(models.keys())[0])
            voice = gr.Dropdown(choices=list(models[model.value].voices().keys()), value=list(models[model.value].voices().keys())[0], label='Voice', interactive=True)
            model.change(change_model, inputs=[model], outputs=[voice])
            split = gr.Interface(
                display, 
                inputs=[model,voice], 
                outputs = [gr.Text(label="voice id")],
                allow_flagging = "never",
                description="display id")
                        
            data =  {"role":[], "voice id": []}
            data["role"].append("旁白")
            data["voice id"].append("audiobook_female_1")
            df = pd.DataFrame(data)
            roleFrame = gr.Dataframe(
                value = df,
                headers=["role", "voice id"],
                datatype=["str", "str"],
                interactive = True,
                label = "1-2 config <role,voice id> pair",
                height=200)
            
            frame = gr.Dataframe(
                headers=["role", "content"],
                datatype=["str", "str"],
                interactive = True,
                label = "sentences",
                height=300)
            
            input_text = gr.Textbox(label="textual", max_lines=15)
            split = gr.Interface(
                splitChapter,
                input_text,
                outputs = [roleFrame, frame],
                allow_flagging = "never",
                description="1-1 split text into sentence")
            speed = gr.Slider(minimum=0.5, maximum=2.0, step=0.1, value=1.0, label="Speed")
            generatorButton = gr.Button(value="1-3 generate")
            audition = gr.Audio("Audio")
            
        with gr.Tab("2 - Generate background audio"):
            prompt = gr.Textbox(label="prompt", max_lines=15)
            generator_background_button = gr.Button(value="1-3 generate")
            sound=gr.Audio(label="Generated Audio.")
        
        with gr.Tab("3 - Merge background audio"):
            original=gr.Audio(sources="upload",
                label="Select here the original audio file!",
                type="filepath")
            
            background=gr.Audio(sources="upload",
                label="Select here the background audio file!",
                type="filepath")
            
            combined=gr.Audio(label="Generated Audio.")
                    
            insert_interface = gr.Interface(fn=insert_background, 
                inputs = [original, background, gr.Slider(minimum=0, maximum=1800, step=0.1, label="Insert Position (seconds)")], 
                outputs = combined,
                description = "Insert audio file into original audio at specified position",
                allow_flagging = "never")
        
        with gr.Tab("4 - Recognize audio"):
            wait_for_audio =gr.Audio(sources="upload",
                label="Select here the background audio file!",
                type="filepath")
            
            recognized_text = gr.Text(label="recognized text")
            
            recognize_interface = gr.Interface(fn=recognize_audio, 
                        inputs=[wait_for_audio], 
                        outputs=recognized_text,
                        description="recognize audio",
                        allow_flagging = "never")
        
        with gr.Tab("5 - upload&&get effect sound"):
            upload_effect_sound =gr.Audio(sources="upload",
                label="insert here the background audio file!",
                type="filepath")
            
            sound_text = gr.Text(label="audio description")
            
            upload_interface = gr.Interface(fn=upload_audio, 
                inputs=[upload_effect_sound, sound_text],
                outputs=[],
                description="upload effect sound",
                allow_flagging = "never")
            
            effect_sound_text = gr.Text(label="description")
            effect_sound = gr.Audio(label="listen")
            
            sounds = gr.Dataframe(
                headers=["id", "description"],
                datatype=["str", "str"],
                interactive = False,
                label = "sounds",
                height=200)
            
            get_audio_interface = gr.Interface(fn=get_audio,
                inputs=[effect_sound_text],
                outputs=[sounds, effect_sound],
                description="get effect sound",
                allow_flagging = "never")

            sounds.select(on_row_click, inputs=[sounds], outputs=[effect_sound])
        
        generator_background_button.click(generate_sound, inputs=[prompt], outputs=[sound, background])
        generatorButton.click(run_tts, inputs=[frame, roleFrame, model, speed], outputs=[audition, original])
            
    demo.launch(
        share=True,
        debug=True,
        server_name="0.0.0.0",
        server_port=9002
    )