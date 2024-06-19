import io
import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pydub import AudioSegment
from config.secret import secret
from tts.v2_minimax_tts import v2_minimax_tts

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
        '--voiceId1', 
        type=str, 
        help='1号声音',
        default="male-qn-jingying"
    )
    
    parser.add_argument(
        '--voiceId2', 
        type=str, 
        help='2号声音',
        default="huopo_nvhai"
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        help='音频的生成目录',
        default="/tmp/output"
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
    
    minimax = v2_minimax_tts(config)
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    for weight2 in range(40):
        voices = [args.voiceId1, args.voiceId2]
        weights = [100 - weight2, weight2]
        audio = minimax.generate_mix(args.text, voices, weights)
        if minimax.format_type() == "mp3":
            audio1 = AudioSegment.from_mp3(io.BytesIO(audio))
        else:
            audio1 = AudioSegment.from_raw(io.BytesIO(audio), sample_width=2, frame_rate=16000, channels=1)
        audio_name = "minimax" + "_" + args.voiceId1 + "_" + str(100-weight2) + "_" + args.voiceId2 + "_" + str(weight2) + ".mp3"
        file_name = os.path.join(args.output, audio_name)
        audio1.export(file_name, format="mp3")