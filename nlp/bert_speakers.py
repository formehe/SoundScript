import torch

from transformers import pipeline, BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

#ner = pipeline("ner", model="ckiplab/bert-base-chinese-ner")
#ner = pipeline("ner", grouped_entities=True)
#tokenizer = BertTokenizerFast.from_pretrained("bert-base-chinese")
#model = AutoModel.from_pretrained("ckiplab/bert-base-chinese-ner")
model = BertModel.from_pretrained("bert-base-chinese")
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

# 示例文本1
text = """
    “这个药丸……不会是迷药或者春药之类的东西吧？我怎么闻着香味儿和两位姐姐说的那么相似？嗯，你该不会……想对我图谋不轨吧？”韩立闻言是愣了半天呐，他现在突然有种吐血三碗的感觉，这女孩儿的心思也太难以捉摸了吧，竟然能把迎香丸，联想到春药上。哎呀韩立现在也不知是该佩服对方的谨慎小心，还是应该为自己的无故蒙冤，而大呼三声了。
    “看样子，你好像说的是真的。不过，我还是要把它拿去给二姐检验下才能用，毕竟我们女儿家，要小心为上。”“咳，咳，呃随便你了。”韩立无言，只能干咳几声，掩饰一下自己脸上的窘迫，他现在觉得呀，自己还是离这个小妖精远点的好，否则，不知什么时候就要被她给郁闷死了。
    “哼哼，不过，如果这药真像你所说的那么好用，那就算你过关啦！今后师兄在莫府有什么为难的事，尽管可以来找彩环帮忙。我只要收些小小的报酬，就肯定能帮你完全解决。”“行啊，师妹，师兄有事，一定找你帮忙。”韩立这时也恢复了常态，皮笑肉不笑地回应着此话，心里呀，却在恶狠狠地想到：“找你这个小财迷才怪了。”
"""

text ="""韩立听别人说"""
text1 ="""韩立闻言是愣了半天呐，他现在突然有种吐血三碗的感觉，这女孩儿的心思也太难以捉摸了吧，竟然能把迎香丸，联想到春药上。哎呀韩立现在也不知是该佩服对方的谨慎小心，还是应该为自己的无故蒙冤，而大呼三声了"""
text2 ="""韩立自己说"""

# 添加特殊的标记，表示句子的开始和结束
# 分词并添加特殊标记
encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
encoded_input1 = tokenizer(text1, return_tensors='pt', padding=True, truncation=True, max_length=128)
encoded_input2 = tokenizer(text2, return_tensors='pt', padding=True, truncation=True, max_length=128)

# marked_text = "[CLS] " + text + " [SEP]"
# tokenized_text = tokenizer.tokenize(marked_text)
# indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
# tokens_tensor = torch.tensor([indexed_tokens])

# marked_text1 = "[CLS] " + text1 + " [SEP]"
# tokenized_text1 = tokenizer.tokenize(marked_text1)
# indexed_tokens1 = tokenizer.convert_tokens_to_ids(tokenized_text1)
# tokens_tensor1 = torch.tensor([indexed_tokens1])

# marked_text2 = "[CLS] " + text2 + " [SEP]"
# tokenized_text2 = tokenizer.tokenize(marked_text2)
# indexed_tokens2 = tokenizer.convert_tokens_to_ids(tokenized_text2)
# tokens_tensor2 = torch.tensor([indexed_tokens2])

with torch.no_grad():
    outputs = model(**encoded_input)
    sentence_embedding = outputs.last_hidden_state[:, 0, :]
    
    outputs = model(**encoded_input1)
    sentence_embedding1 = outputs.last_hidden_state[:, 0, :]


    outputs = model(**encoded_input2)
    sentence_embedding2= outputs.last_hidden_state[:, 0, :]

# 计算余弦相似度
similarity = cosine_similarity(sentence_embedding, sentence_embedding1)
print(f"句子相似度为：{similarity[0][0]}")

similarity = cosine_similarity(sentence_embedding, sentence_embedding2)
print(f"句子相似度为：{similarity[0][0]}")


# 示例文本
#text = """
#　　有一个计程车司机在计程车行工作。有一天的深夜，他正开车经过一片很荒凉的地方，四周一片漆黑；忽然看见前面荒地里有一座大厦，亮着昏暗的灯。他正在奇怪那里什么时候起了这样一座楼，就>看到路边有一个小姐招手要坐他的车回家，那个小姐坐上车後，他就把车门关起来，开始开车，过了一会儿，他觉得很奇怪，为什么那个小姐都没说话，结果他往後照镜一看，哪有什么小姐，仅有一个洋>娃娃坐在那里，他吓个半死，抓起洋娃娃往窗外丢出去，回家後就大病了三个月。
#　　等他病好了以後，他回去计程车行工作，结果他的同事对他说：“你真不够意思，有一个漂亮的小姐过来投诉说她上次要坐你的车，结果她才刚把洋娃娃丢进去，你就把车门关起来开走了。”
#"""
#results = ner(text)
#print(results)

# for i, entity in enumerate(lac_result[1]):
#     if entity == 'PER':
#         print(lac_result[0][i])