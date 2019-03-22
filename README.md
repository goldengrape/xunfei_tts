让使用讯飞TTS稍微方便一些。

讯飞TTS对单句的长度有一定限制，本方案除了包装打扫一些调用所需的常规外，主要是自动对长句子进行切分，使之满足讯飞TTS对于句子长度的要求，然后再合并成连贯的语音。并且在切分时务求在标点断句处进行切分，以避免诡异的语音中断。

# 安装

我还没有搞定pip和conda的安装包（谁来教教我），所以您可以简单git clone，或者干脆把xunfei_tts.py 下载下来即可。

# 依赖
* [Pydub](https://github.com/jiaaro/pydub)
    * 注意pydub是基于ffmpeg的，所以还需要安装ffmpeg。
    * 在anaconda环境中，有可能ffmpeg调用出错，建议在所需env下使用conda进行ffmpeg的安装，`conda install -c menpo ffmpeg ` 比使用homebrew还要更好一些，各种解码器都自动装上了。

# 使用前准备

要使用讯飞TTS, 应先注册讯飞开放平台, 获得相应的key和ID, 并在讯飞填入自己的IP地址. 挺麻烦的, [参考这里](https://segmentfault.com/a/1190000013953185)

如果要将代码上载到公共网络，例如github，建议讲API信息单独存储为txt文件，例如API_sample.txt中演示的：

```json
{
"key": "这里写入APIKey",
"id": "这里写入APPID", 
"url": "http://api.xfyun.cn/v1/service/v1/tts"
}
```
如果不是使用的固定IP地址，那么每次更换IP以后都要去讯飞的控制平台上修改许可IP列表，修改后要过一两分钟才能生效。

# 使用示例

## 基础应用
```python
from xunfei_tts import Speech as xf_Speech

# 需要导入API信息
with open('API_sample.txt') as json_file:  
    api = json.load(json_file)

s=xf_Speech(api)
text="你好世界，hello world"
s.play(text)
s.save(text,"hello_world.mp3")
```
## 指定语音参数

如果需要指定TTS中的参数，可以分别指定
* voice_name：
    发音人：讯飞免费自带的有：xiaoyan，aisjiuxu，aisxping，aisjinger，aisbabyxu。还有很多更高质量的语音，可以免费试用15天。默认 voice_name='aisjiuxu'
* audio_type：
    从讯飞取回音频的格式：mp3或wav，默认 audio_type="mp3"
* speed：
    朗读速度，0-100，默认 speed="60"
* volume：
    音量：0-100，默认 volume=100
* pitch:
    音高：0-100，默认 pitch="30"
* engine_type：
    引擎类型。aisound（普通效果），intp65（中文），intp65_en（英文），后两种似乎免费版用不了。默认 engine_type="aisound"

```python
from xunfei_tts import Speech as xf_Speech

# 需要导入API信息
with open('API_sample.txt') as json_file:  
    api = json.load(json_file)

# 个性化设定语音
s=xf_Speech(api,
            voice_name='aisjiuxu',
            speed="80",
            pitch="50")

text="你好世界，hello world"
s.play(text)
s.save(text,"hello_world.mp3")
```

## 将语音放入内存中准备后续处理：

```python
from xunfei_tts import Speech as xf_Speech
from io import BytesIO

# 需要导入API信息
with open('API_sample.txt') as json_file:  
    api = json.load(json_file)

# 个性化设定语音
s=xf_Speech(api,
            voice_name='aisjiuxu',
            speed="80",
            pitch="50")

text="你好世界，hello world"
s.play(text)
f=BytesIO()
s.savef(text,f)
```
# 使用限制

## API调用次数限制
讯飞TTS在使用上有一定限制，其中每日API调用次数是500次，注意是次数，不是语句长度。

## 单句长度限制
对于每句话的长度要求是："待合成文本，使用utf-8编码，需urlencode，长度小于1000字节"，大约是300-450个中文单字。我在代码中以 MAX_SEGMENT_SIZE = 300进行了限定。

不过如果每次充分利用300多字的长度，每天也可以念出十万字左右。一般个人使用也够了。

## IP地址限制
如果不是使用的固定IP地址，那么每次更换IP以后都要去讯飞的控制平台上修改许可IP列表，修改后要过一两分钟才能生效。

# 参考

[讯飞开发文档](https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.html)