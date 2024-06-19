import requests
from config.secret import secret
from tts.voicetts import TTS

#可选，默认值为mp3，可选范围：mp3、wav、pcm、flac、aac
class minimax_tts(TTS):
    def __init__(self, config:secret):
        self.group_id = config.get("minimax", "group_id")
        self.api_key = config.get("minimax", "key")

        self.url = f"https://api.minimax.chat/v1/text_to_speech?GroupId={self.group_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
    def voices(self):
        return {
                    "male-青涩青年音色":"male-qn-qingse",
                    "male-精英青年音色":"male-qn-jingying",
                    "male-霸道青年音色":"male-qn-badao",
                    "male-青年大学生音色":"male-qn-daxuesheng",
                    "少女音色":"female-shaonv",
                    "御姐音色":"female-yujie",
                    "成熟女性音色":"female-chengshu",
                    "甜美女性音色":"female-tianmei",
                    "男性主持人":"presenter_male",
                    "女性主持人":"presenter_female",
                    "男性有声书1":"audiobook_male_1",
                    "男性有声书2":"audiobook_male_2",
                    "女性有声书1":"audiobook_female_1",
                    "女性有声书2":"audiobook_female_2",
                    "male-青涩青年音色-beta":"male-qn-qingse-jingpin",
                    "male-精英青年音色-beta":"male-qn-jingying-jingpin",
                    "male-霸道青年音色-beta":"male-qn-badao-jingpin",
                    "male-青年大学生音色-beta":"male-qn-daxuesheng-jingpin",
                    "少女音色-beta":"female-shaonv-jingpin",
                    "御姐音色-beta":"female-yujie-jingpin",
                    "成熟女性音色-beta":"female-chengshu-jingpin",
                    "甜美女性音色-beta":"female-tianmei-jingpin",
                    "Frantic Youth":"Frantic_Youth",
                    "Tough Boss":"Tough_Boss",
                    "Chatty Girl":"Chatty_Girl",
                    "Fragile Boy":"Fragile_Boy",
                    "Theatrical Actor":"Theatrical_Actor",
                    "Thoughtful Lady":"Thoughtful_Lady",
                    "Sensible Manager":"Sensible_Manager",
                    "Powerful Veteran":"Powerful_Veteran",
                    "Anxious Man":"Anxious_Man",
                    "Compelling Girl":"Compelling_Girl",
                    "Elegant Girl":"Elegant_Girl",
                    "Determined Manager":"Determined_Manager",
                    "Playful Spirit":"Playful_Spirit",
                    "Inspiring Lady":"Inspiring_Lady",
                    "Strict Boss":"Strict_Boss",
                    "Romantic Husband":"Romantic_Husband",
                    "Sentimental Lady":"Sentimental_Lady",
                    "Funny Guy":"Funny_Guy",
                    "Fascinating Boy":"Fascinating_Boy",
                    "Wise Scholar":"Wise_Scholar",
                    "Upset Girl":"Upset_Girl",
                    "Kind-hearted Girl":"Kind-hearted_Girl",
                    "Passionate Warrior":"Passionate_Warrior",
                    "Powerful Soldier":"Powerful_Soldier",
                    "Caring Girlfriend":"Caring_Girlfriend",
                    "Energetic Girl":"Energetic_Girl",
                    "Friendly Neighbor":"Friendly_Neighbor",
                    "Stressed Lady":"Stressed_Lady",
                    "Whimsical Girl":"Whimsical_Girl",
                    "Captivating Storyteller":"Captivating_Storyteller",
                    "Debator":"Debator",
                    "Assertive Queen":"Assertive_Queen",
                    "Naughty Schoolgirl":"Naughty_Schoolgirl",
                    "Comedian":"Comedian",
                    "Mature Partner":"Mature_Partner",
                    "Frank Lady":"Frank_Lady",
                    "Grim Reaper":"Grim_Reaper",
                    "Serene Elder":"Serene_Elder",
                    "Reliable Man":"Reliable_Man",
                    "Energetic Boy":"Energetic_Boy",
                    "Gentle Teacher":"Gentle_Teacher",
                    "Sad Teen":"Sad_Teen",
                    "Charming Queen":"Charming_Queen",
                    "Anime Character":"Anime_Character",
                    "Baritone":"Baritone",
                    "Angry Man":"Angry_Man",
                    "Smart Young Girl":"Smart_Young_Girl",
                    "Deep-Voiced Gentleman":"Deep-Voiced_Gentleman",
                    "Lovely Lady":"Lovely_Lady",
                    "Gorgeous Lady":"Gorgeous_Lady",
                    "Playful Girl":"Playful_Girl",
                    "Soft-spoken Girl":"Soft-spoken_Girl",
                    "Strong-Willed Boy":"Strong-Willed_Boy",
                    "Bossy Leader":"Bossy_Leader",
                    "Thoughtful Man":"Thoughtful_Man",
                    "Confident Woman":"Confident_Woman",
                    "Serene Woman":"Serene_Woman",
                    "Attractive Girl":"Attractive_Girl",
                    "Reserved Young Man":"Reserved_Young_Man",
                    "Cute Elf":"Cute_Elf",
                    "Sweet Girl":"Sweet_Girl",
                    "Deep-toned Man":"Deep-toned_Man",
                    "Rational Man":"Rational_Man",
                    "Calm Leader":"Calm_Leader",
                    "Humorous Elder":"Humorous_Elder",
                    "Godfather":"Godfather",
                    "Ghost":"Ghost",
                    "Charming Lady":"Charming_Lady",
                    "Charming Santa":"Charming_Santa",
                    "Arnold":"Arnold",
                    "Rudolph":"Rudolph",
                    "Grinch":"Grinch",
                    "Santa Claus":"Santa_Claus",
                    "花甲奶奶":"huajia_nainai",
                    "冷淡女王":"lengdan_nvwang",
                    "成熟姐姐":"chengshu_jiejie",
                    "邻居阿姨":"linju_ayi",
                    "搞笑大爷":"gaoxiao_daye",
                    "呆萌青年":"daimeng_qingnian",
                    "稚嫩奶狗":"zhinen_naigou",
                    "假小子":"jia_xiaozi",
                    "女上司":"nv_shangsi",
                    "诡异法师":"guiyi_fashi",
                    "海绵宝宝":"dongman_baobao",
                    "幽默叔叔":"youmo_shushu",
                    "胡同大爷":"hutong_daye",
                    "职场经理":"zhichang_jingli",
                    "病弱少女":"bingruo_shaonv",
                    "活泼女孩":"huopo_nvhai",
                    "女帮主":"nv_bangzhu",
                    "温顺弟弟":"wenshun_didi",
                    "稚嫩学生":"zhinen_xuesheng",
                    "琼瑶男主":"qiongyao_nanzhu",
                    "可爱女生":"keai_nvsheng",
                    "天真女孩":"tianzhen_nvhai",
                    "活力哥哥":"huoli_gege",
                    "病娇皇帝":"bingjiao_huangdi",
                    "女班长":"nv_banzhang",
                    "学霸同桌":"xueba_tongzhuo",
                    "文雅女友":"wenya_nvyou",
                    "贴心男友":"tiexin_nanyou",
                    "娇羞女友":"jiaoxiu_nvyou",
                    "霸道总裁":"badao_zongcai",
                    "调皮公主":"tiaopi_gongzhu",
                    "逍遥剑仙":"xiaoyao_jianxian",
                    "甜美少女":"tianmei_shaonv",
                    "孤傲公子":"guao_gongzi",
                    "性感御姐":"xinggan_yujie",
                    "儒雅总裁":"ruya_zongcai",
                    "温柔医生":"wenrou_yisheng",
                    "柔美女友":"roumei_nvyou",
                    "冷峻上司":"badao_shangsi",
                    "宠溺男友":"chongni_nanyou",
                    "傲娇男友":"aojiao_nanyou",
                    "闷骚女友":"mensao_nvyou",
                    "醋精男友":"cujing_nanyou",
                    "体育系学弟":"tiyuxi_xuedi",
                    "知性老师":"zhixing_laoshi",
                    "暖心学姐":"nuanxin_xuejie",
                    "灵动女孩":"lingdong_nvhai",
                    "病娇姐姐":"bingjiao_jiejie",
                    "病娇哥哥":"bingjiao_gege",
                    "闷骚男友":"mensao_nanyou",
                    "病娇总裁":"bingjiao_zongcai",
                    "病弱公子":"bingruo_gongzi",
                    "温柔同桌":"wenrou_tongzhuo",
                    "优柔帮主":"rouyou_bangzhu",
                    "玄幻剑客":"xuanhuan_jianke",
                    "机械战甲":"jixie_zhanjia",
                    "霸道少爷":"badao_shaoye",
                    "娴静学姐":"xianjing_xuejie",
                    "婉约女友":"wanyue_nvyou",
                    "活泼女友":"huopo_nvyou",
                    "魅力女友":"meili_nvyou",
                    "冷淡兄长":"lengdan_xiongzhang",
                    "淡雅学姐":"danya_xuejie",
                    "嗲嗲学妹":"diadia_xuemei",
                    "纯真学弟":"chunzhen_xuedi",
                    "俊朗男友":"junlang_nanyou",
                    "妩媚御姐":"wumei_yujie",
                    "病娇弟弟":"bingjiao_didi",
                    "俏皮萌妹":"qiaopi_mengmei",
                    "甜心小玲":"tianxin_xiaoling",
                    "率真少年":"shuaizhen_shaonian",
                    "腾展-guigushi_1_ck2":"guigushi_1_ck2",
                    "腾展-tengzhan_guigushi_speech02_516":"tengzhan_guigushi_speech02_516",
                    "腾展-tengzhan_qingsheng_speech02_516":"tengzhan_qingsheng_speech02_516",
                    "腾展-tengzhan_duihua_speech02_516":"tengzhan_duihua_speech02_516",
                }
    
    def format_type(self):
        return "mp3"
    
    def generate(self, text, voiceId, speed:float=1.0):
        data = {
            "voice_id": f"{voiceId}",
            "text": f"{text}",
            "model": "speech-02",
            "speed": speed,
            "vol": 1.0,
            "pitch": 0,
        }

        response = requests.post(self.url, headers=self.headers, json=data, timeout = 10)
        print("trace_id", response.headers.get("Trace-Id"))
        if response.status_code != 200 or "json" in response.headers["Content-Type"]:
            print("调用失败", response.status_code, response.text)
            return None
        return response.content
    
    def generate_mix(self, text, voiceIds, weights, speed:float=1.0):
        timber_weights = []
        for voiceId,weight in zip(voiceIds, weights):
            timber_weights.append({
                "voice_id": f"{voiceId}",
                "weight": weight
            })
            
        data = {
            "text": f"{text}",
            "model": "speech-02",
            "speed": speed,
            "vol": 1.0,
            "pitch": 0,
            "timber_weights": timber_weights,
        }
        
        response = requests.post(self.url, headers=self.headers, json=data, timeout = 10)
        print("trace_id", response.headers.get("Trace-Id"))
        if response.status_code != 200 or "json" in response.headers["Content-Type"]:
            print("调用失败", response.status_code, response.text)
            return None
        return response.content