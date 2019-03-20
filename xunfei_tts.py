
# coding: utf-8

# 讯飞tts的class
# 
# 需要使用以json格式写的API才可以初始化。
# ```json
# {
# "key": "3************c77",
# "id": "5*****5a", 
# "url": "http://api.xfyun.cn/v1/service/v1/tts"
# }
# 
# ```
# 
# 调用例子：
# ```python
# with open('API_setup.txt') as json_file:  
#     api = json.load(json_file)
#     a=Speech(api, voice_name="x_yifeng")
#     a.save("你好","test.mp3")
#     a.play("你好")
# ```

# In[1]:


import re
import base64
import json
import time
import hashlib
import urllib.request
import urllib.parse
import json
import subprocess
import os
import string

from io import BytesIO
from pydub import AudioSegment, playback


# In[2]:


class Speech:

    """ 讯飞TTS """
    MAX_SEGMENT_SIZE = 300
    MIN_SEGMENT_SIZE = 2
    
    def __init__(self, 
                 api,
                 voice_name='aisjiuxu', 
                 audio_type="mp3", #音频编码，raw(生成wav)或lame(生成mp3)
                 speed="60",
                 volume="100",
                 pitch="30",
                 engine_type="aisound", 
                ): 
        '''要使用api进行初始化'''
        self.api=api
        self.split_pattern=__class__.split_pattern()
        self.audio_type=audio_type
        audio_type_dict={"mp3":"lame","wav":"raw"}
        self.text='.'
        self.Param = {
            "auf": "audio/L16;rate=16000",    #音频采样率
            "aue": {"mp3":"lame","wav":"raw"}[audio_type],    #音频编码，raw(生成wav)或lame(生成mp3)
            "voice_name": voice_name,
            "speed": speed,    #语速[0,100]
            "volume": volume,    #音量[0,100]
            "pitch": pitch,    #音高[0,100]
            "engine_type": engine_type    #引擎类型。aisound（普通效果），intp65（中文），intp65_en（英文）
            }
#         self.Param_b64str=self.construct_base64_str()
    
    def split_pattern():
        cn_punc="！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-" #this line is Chinese punctuation
        en_punc=string.punctuation
        useless_chars = frozenset(
                              en_punc 
                              + string.whitespace
                              + cn_punc 
                              )
        split_pattern=re.compile("([\s\S]{"
                 +"{},{}".format(__class__.MIN_SEGMENT_SIZE, __class__.MAX_SEGMENT_SIZE)
                 + "}[useless_chars|(?!.\d+)|(?!,\d+)])")
        
        return split_pattern
        
    def splitText(self,text):
        text+="."
        s=[]
        if len(text)>__class__.MAX_SEGMENT_SIZE:
            s+=self.split_pattern.findall(text)
        else:
            s.append(text)
        return s
    
    def construct_base64_str(Param):
        # 配置参数编码为base64字符串，过程：字典→明文字符串→utf8编码→base64(bytes)→base64字符串
        Param_str = json.dumps(Param)    #得到明文字符串
        Param_utf8 = Param_str.encode('utf8')    #得到utf8编码(bytes类型)
        Param_b64 = base64.b64encode(Param_utf8)    #得到base64编码(bytes类型)
        Param_b64str = Param_b64.decode('utf8')    #得到base64字符串
        return Param_b64str

    def construct_header(api, Param_b64str):
        # 构造HTTP请求的头部
        time_now = str(int(time.time()))
        checksum = (api["key"] + time_now + Param_b64str).encode('utf8')
        checksum_md5 = hashlib.md5(checksum).hexdigest()
        header = {
            "X-Appid": api["id"],
            "X-CurTime": time_now,
            "X-Param": Param_b64str,
            "X-CheckSum": checksum_md5
        }
        return header

    def construct_urlencode_utf8(t):
        # 构造HTTP请求Body
        body = {
            "text": t
        }
        body_urlencode = urllib.parse.urlencode(body)
        body_utf8 = body_urlencode.encode('utf8')
        return body_utf8

    
    def getAudioData(self,text):
        Param=self.Param 
        api=self.api
        
        # 发送HTTP POST请求
        req = urllib.request.Request(
            api["url"], 
            data=__class__.construct_urlencode_utf8(text), 
            headers=__class__.construct_header(api, __class__.construct_base64_str(Param)))
        
        response = urllib.request.urlopen(req)
        response_head = response.headers['Content-Type']
        
        if(response_head == "text/plain"): #出错，返回错误信息
            err_msg=json.loads(response.read().decode('utf8'))
            raise UserWarning("讯飞WebAPI错误: {}".format(err_msg["desc"]))
        else: 
            audio_data=response.read()
            voice = AudioSegment.from_mp3(BytesIO(audio_data))
            return voice
    
    def play(self, text):
        '''play voice'''
        for t in self.splitText(text):
            playback.play(self.getAudioData(t))
            
    def save(self, text, path):
        """ Save audio data to an MP3 file. """
        with open(path, "wb") as f:
            self.savef(text,f)

    def savef(self, text,file):
        """ Write audio data into a file object. """
        combined = AudioSegment.empty()
        for t in self.splitText(text):
            combined += self.getAudioData(t)
        combined.export(file, 
                        format="mp3",
                        codec="libmp3lame")

