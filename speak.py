#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse
from xunfei_tts import Speech as xf_Speech
import json

# 创建解析步骤
parser = argparse.ArgumentParser(description='Process TTS')

# 添加参数步骤
parser.add_argument('-t','--text',  type=str, 
                   help='text to speak')
parser.add_argument('-f','--file',  type=str, 
                   help='text file name to speak')
parser.add_argument('-o','--output',  type=str,
                   help='output file name')
parser.add_argument('-v','--voice',  type=str, default='aisjiuxu',
                   help='the voice of tts')
parser.add_argument('-a','--api',  type=str, default='API_setup.txt',
                   help='setup the api filename')
parser.add_argument('-s','--speak', action="store_true",
                   help='speak')

# 解析参数步骤  
args = parser.parse_args()


# In[ ]:


# 要说的话
if args.text:
    text=args.text
elif args.file:
    with open(args.file) as text_file:
        text=text_file.read()

# 初始化讯飞引擎
with open(args.api) as json_file:  
    api = json.load(json_file)
    ve = xf_Speech(api, voice_name=args.voice)         
# 朗读
if args.speak: 
    ve.play(text)
# 存储
if args.output:
    ve.save(text,args.output)

