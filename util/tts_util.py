import io
import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pydub import AudioSegment

from config.secret import secret
from tts.chatgpt_tts import chatgpt_tts
from tts.elevenlab_tts import elevenlab_tts
from tts.minimax_tts import minimax_tts
from tts.v2_minimax_tts import v2_minimax_tts
from tts.azure_tts import azure_tts

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='用命令行工具生成指定模型的音频到指定位置')

    # 添加命令行选项
    parser.add_argument(
        '--text', 
        type = str,
        help='输入文件内容',
        required=True,
        default="This is an example"
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        help='音频的生成目录',
        default="/tmp/output"
    )
    
    # 添加参数，指定 nargs='*' 或 nargs='+' 表示该参数可以接受任意数量的值
    parser.add_argument(
        '--models', 
        nargs='+', 
        help='支持minimax/minimax_v2/openai/elevenlab/azure',
        default=["openai"]
    )
    
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
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    models = {
        "minimax":minimax_tts(config),
        "minimax_v2":v2_minimax_tts(config),
        "elevenlab":elevenlab_tts(config),
        "openai":chatgpt_tts(config),
        "azure":azure_tts(config)
    } 
    
    for model in args.models:
        if models[model] :
            voices = models[model].voices()
        else :
            print("not support {}", model)
            continue
        for voice_name, voice_id in voices.items():
            audio = models[model].generate(args.text, voice_id)
            if not audio :
                print("fail to generate audio")
                continue
            if models[model].format_type() == "mp3":
                audio1 = AudioSegment.from_mp3(io.BytesIO(audio))
            else:
                audio1 = AudioSegment.from_raw(io.BytesIO(audio), sample_width=2, frame_rate=16000, channels=1)
            audio_name = model + "_" + voice_name + ".mp3"
            file_name = os.path.join(args.output, audio_name)
            audio1.export(file_name, format="mp3")