import re
from bs4 import BeautifulSoup

#marked_text = """
#但我现在对这个职业的热爱还是非常的,<backgroundaudio src="https://contoso.com/sample.wav" volume="0.7" fadein="3000" fadeout="4000">呵呵，非常的,嗯，怎么说呢？日月可鉴的，
#<backgroundaudio src="https://contoso.com/sample.wav" volume="0.7" fadein="3000" fadeout="4000">哈哈</backgroundaudio>，
#嗯还是希望可以把这个职业做下去或者做这个声音相关领域的工作，嗯，就是把自己的优势发挥的大一点，尽可能能用到自己擅长的东西，而不是为了工作，为了挣钱而工作。</backgroundaudio>
#"""

def parse(text):
    # 使用BeautifulSoup解析SSML文本
    soup = BeautifulSoup(text, 'html.parser')
    # 查找所有<mstts:backgroundaudio>标签
    backgroundaudio_tags = soup.find_all('backgroundaudio')
    start_pos = 0
    # 遍历每个<backgroundaudio>标签，获取其内容和属性值
    for backgroundaudio_tag in backgroundaudio_tags:
        segments = re.findall(r'<[^<]*>|[^<]*<', backgroundaudio_tag)
        print(segments)
        print(f"Tag name is:{backgroundaudio_tag.name}")
        print(backgroundaudio_tag)
        tag_str = str(backgroundaudio_tag)
        # 从上一个标签的结束位置开始查找
        position = text.find(tag_str, start_pos)
        # 更新下一次查找的起始位置为当前标签的结束位置
        
        start_pos = position + len(tag_str)
        audio_src = backgroundaudio_tag['prompt']
        audio_volume = backgroundaudio_tag['volume']
        audio_fadein = backgroundaudio_tag['fadein']
        audio_fadeout = backgroundaudio_tag['fadeout']
        parent_tag = backgroundaudio_tag.parent.name
        content = backgroundaudio_tag.get_text()
        print(f"Tag: {tag_str}")
        print(f"Parent Tag: {parent_tag}")
        print(f"Audio Source: {audio_src}")
        print(f"Volume: {audio_volume}")
        print(f"Fade In: {audio_fadein}")
        print(f"Fade Out: {audio_fadeout}")
        print(f"Content: {content}")
        print(f"标签位置：{position}")
        
        print("Children tags:")
        children_tags = backgroundaudio_tag.find_all()
        for child_tag in children_tags:
            print(child_tag.name)
            
