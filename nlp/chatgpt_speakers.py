
import json

from openai import OpenAI
from config.secret import secret
from nlp.speaker import SPEAKERS

#prompt
# Step 1: 提取涉及对话或者心理过程的句子
# 以下是提取的涉及对话或心理过程的句子：

# 1. "这个药丸……不会是迷药或者春药之类的东西吧？我怎么闻着香味儿和两位姐姐说的那么相似？嗯，你该不会……想对我图谋不轨吧？"
# 2. "看样子，你好像说的是真的。不过，我还是要把它拿去给二姐检验下才能用，毕竟我们女儿家，要小心为上。"
# 3. "咳，咳，呃随便你了。"
# 4. "哼哼，不过，如果这药真像你所说的那么好用，那就算你过关啦！今后师兄在莫府有什么为难的事，尽管可以来找彩环帮忙。我只要收些小小的报酬，就肯定能帮你完全解决。"
# 5. "行啊，师妹，师兄有事，一定找你帮忙。"
# 6. 韩立心里呀，却在恶狠狠地想到：“找你这个小财迷才怪了。”

# Step 2: 说明每个句子的发言者
# 1. 发言者：未明确，但从上下文推测，这可能是彩环的疑问或担忧。
# 2. 发言者：彩环，她在表达自己的谨慎，并提到要将药丸给二姐检验。
# 3. 发言者：韩立，他在无言以对时，只能干咳几声。
# 4. 发言者：彩环，她在提出如果药丸有效，她愿意帮助韩立，并提到需要报酬。
# 5. 发言者：韩立，他在表面上接受了彩环的帮助提议。
# 6. 发言者：韩立，这是他的内心想法，没有直接说出来。

# 最终输出，发言者:句子
# - 彩环/未明确: "这个药丸……不会是迷药或者春药之类的东西吧？我怎么闻着香味儿和两位姐姐说的那么相似？嗯，你该不会……想对我图谋不轨吧？"
# - 彩环: "看样子，你好像说的是真的。不过，我还是要把它拿去给二姐检验下才能用，毕竟我们女儿家，要小心为上。"
# - 韩立: "咳，咳，呃随便你了。"
# - 彩环: "哼哼，不过，如果这药真像你所说的那么好用，那就算你过关啦！今后师兄在莫府有什么为难的事，尽管可以来找彩环帮忙。我只要收些小小的报酬，就肯定能帮你完全解决。"
# - 韩立: "行啊，师妹，师兄有事，一定找你帮忙。"
# - 韩立: 心里想法——“找你这个小财迷才怪了。”

# 根据文本按照以下步骤工作：
# Step 1: 提取涉及对话或者心理过程的句子
# Step 2: 说明每个句子的发言者，发言者必须填，选择可能性最大的发言者
# 最终输出，发言者:句子。
# 文本如下："“这个药丸……不会是迷药或者春药之类的东西吧？我怎么闻着香味儿和两位姐姐说的那么相似？嗯，你该不会……想对我图谋不轨吧？”韩立闻言是愣了半天呐，他现在突然有种吐血三碗的感觉，这女孩儿的心思也太难以捉摸了吧，竟然能把迎香丸，联想到春药上。哎呀韩立现在也不知是该佩服对方的谨慎小心，还是应该为自己的无故蒙冤，而大呼三声了。“看样子，你好像说的是真的。不过，我还是要把它拿去给二姐检验下才能用，毕竟我们女儿家，要小心为上。”“咳，咳，呃随便你了。”韩立无言，只能干咳几声，掩饰一下自己脸上的窘迫，他现在觉得呀，自己还是离这个小妖精远点的好，否则，不知什么时候就要被她给郁闷死了。“哼哼，不过，如果这药真像你所说的那么好用，那就算你过关啦！今后师兄在莫府有什么为难的事，尽管可以来找彩环帮忙。我只要收些小小的报酬，就肯定能帮你完全解决。”“行啊，师妹，师兄有事，一定找你帮忙。”韩立这时也恢复了常态，皮笑肉不笑地回应着此话，心里呀，却在恶狠狠地想到：“找你这个小财迷才怪了。”"


class chatgpt_speakers(SPEAKERS):
    def __init__(self, config: secret):
        self.api_key = config.get("openai", "key")
    
    def extract(self, text:str):
        prompt = f"""你是文本阅读理解专家，能提炼出文本中既是活跃角色又有对话的说话人，要求返回为json格式，并将说话人存放在字段roles。以下是文本：\r\n{text}"""
        print(prompt)
        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            # model="gpt-4-vision-preview",
        )
        
        data = json.loads(chat_completion.choices[0].message.content)
        roles = data.get('roles',[])
        print(roles)
        return roles
    
    def recognize_dialog_speaker(self, text:str, dialog:str):
        prompt = f"""你善于文本阅读理解，可以根据对话内容识别出对话说话人，要求返回为json格式，并将说话人存放在字段role。以下是文本：\r\n{text}，以下是对话内容：\r\n{dialog}"""
        print(prompt)
        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            #model="gpt-4-vision-preview",
        )
        
        print(chat_completion.choices[0].message.content)
        data = json.loads(chat_completion.choices[0].message.content)
        role = data.get('role')
        return role