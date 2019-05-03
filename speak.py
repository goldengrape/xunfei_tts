#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
from xunfei_tts import Speech as xf_Speech
import json
import os

# 创建解析步骤
parser = argparse.ArgumentParser(description='Process TTS')

# 添加参数步骤
parser.add_argument('-t','--text',  type=str, 
                   help='text to speak')
parser.add_argument('-f','--file',  type=str, 
                   help='text file name to speak')
parser.add_argument('-e','--epub', type = str,
                   help='epub file name to speak')
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


def speak_simple_text(args):
    # 要说的话
    text=args.text
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


# # speak epub

# In[ ]:


def speak_epub(args):
    from process_epub import split_epub
    filename=args.epub
    text_list=split_epub(filename)
    with open(args.api) as json_file:  
        api = json.load(json_file)
        ve = xf_Speech(api, voice_name=args.voice)         

    # 存储
    if args.output:
        output_base, ext=os.path.splitext(args.output)            
        for i in range(len(text_list)):
            ve.save(text_list[i],output_base+"_{:03d}".format(i)+ext)


# In[ ]:


def speak_txt(args):
    filename=args.file
    with open(filename,'r') as f:
        text=f.read()
        with open(args.api) as json_file:  
            api = json.load(json_file)
            ve = xf_Speech(api, voice_name=args.voice)         
        # 朗读
        if args.speak: 
            ve.play(text)
        # 存储
        if args.output:
            ve.save(text,args.output)


# In[ ]:


if args.text:
    speak_simple_text(args)
elif args.file:
    speak_txt(args)
elif args.epub:
    speak_epub(args)


        
        
# # 初始化讯飞引擎
# with open(args.api) as json_file:  
#     api = json.load(json_file)
#     ve = xf_Speech(api, voice_name=args.voice)         
# # 朗读
# if args.speak: 
#     ve.play(text)
# # 存储
# if args.output:
#     ve.save(text,args.output)

