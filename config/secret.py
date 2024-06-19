import json

class secret:
    def __init__(self, path:str):
        self.path= path
        # 从文件中加载JSON格式数据
        with open(self.path, "r") as file:
            self.content = json.load(file)
    
    def get(self, name:str, key:str):
        return self.content[name][key]