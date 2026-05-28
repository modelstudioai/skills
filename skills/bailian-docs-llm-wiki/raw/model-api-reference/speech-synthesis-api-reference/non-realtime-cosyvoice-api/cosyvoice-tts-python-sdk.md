# 非实时语音合成CosyVoice Python SDK参考

本文介绍非实时语音合成CosyVoice的Python SDK调用方法，支持非流式和流式两种调用模式。

**用户指南**：参见[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

**重要**

该功能仅在[中国内地部署范围](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)（北京地域）下可用。

## **前提条件**

-   已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并将其[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
    
-   已安装符合版本要求的DashScope Java SDK，建议[安装最新版](https://help.aliyun.com/zh/model-studio/install-sdk)，SDK版本需≥1.25.17
    

## **HttpSpeechSynthesizer 类**

**包路径**：`dashscope.audio.http_tts.http_speech_synthesizer.HttpSpeechSynthesizer`

**功能**：基于HTTP的语音合成，通过`stream`参数控制非流式或流式调用模式。

### **call() - 语音合成调用**

**方法签名**：

```
@classmethod
def call(cls, model: str, text: str, voice: str,
         format: str = "wav", sample_rate: int = 24000,
         volume: int = 50, rate: float = 1.0, pitch: float = 1.0,
         bit_rate: int = 32, enable_ssml: bool = False,
         word_timestamp_enabled: bool = False,
         seed: int = 0, language_hints: list = None,
         instruction: str = None,
         enable_aigc_tag: bool = False,
         aigc_propagator: str = None,
         aigc_propagate_id: str = None,
         hot_fix: dict = None,
         enable_markdown_filter: bool = False,
         stream: bool = False,
         api_key: str = None, **kwargs)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

model

str

是

语音合成模型。

取值范围：

-   cosyvoice-v3.5-plus
    
-   cosyvoice-v3.5-flash
    
-   cosyvoice-v3-plus
    
-   cosyvoice-v3-flash
    
-   cosyvoice-v2
    

text

str

是

待合成文本。

支持 SSML 和 LaTeX 格式输入。将待合成文本替换为对应格式即可。

-   使用 SSML 时，需同时将 `enable_ssml` 设置为 `True`。支持的 SSML 标签及用法，请参见[SSML标记语言介绍](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。
    
-   使用 LaTeX 时，将待合成文本替换为 LaTeX 格式即可，无需额外配置。支持的 LaTeX 语法及用法，请参见[LaTeX 公式转语音](https://help.aliyun.com/zh/model-studio/latex-capability-support-description)。
    

voice

str

是

音色。

取值范围：

-   系统音色：参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
    
-   声音复刻音色：如何创建音色请参见[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)
    
-   声音设计音色：如何创建音色请参见[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)
    

format

str

否

音频编码格式。

默认值：mp3。

取值范围：

-   mp3
    
-   pcm
    
-   wav
    
-   opus
    

sample\_rate

int

否

音频采样率（Hz）。

取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。

volume

int

否

音量。

默认值：50。

取值范围：\[0, 100\]。

rate

float

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

pitch

float

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

bit\_rate

int

否

音频码率（单位：kbps）。

默认值：32。

取值范围：\[6, 510\]。

**重要**

仅在`format`为`opus`时支持使用该参数。

enable\_ssml

bool

否

是否开启SSML功能。当`text`使用SSML格式时，需设为`True`。默认为`False`。支持的SSML标签及用法，请参考[SSML标签](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。

word\_timestamp\_enabled

bool

否

是否开启字级别时间戳。

默认值：False。

-   True：开启。
    
-   False：关闭。
    

该功能仅适用于cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色。

seed

int

否

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

language\_hints

list

否

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
    
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见声音复刻API参考。
    

指定语音合成的目标语言，提升合成效果。

当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：

-   数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”
    
-   符号朗读不准确，“@”读成“艾特”而非“at”
    
-   小语种合成效果差，合成不自然
    

取值范围：

-   zh：中文
    
-   en：英文
    
-   fr：法语
    
-   de：德语
    
-   ja：日语
    
-   ko：韩语
    
-   ru：俄语
    
-   pt：葡萄牙语
    
-   th：泰语
    
-   id：印尼语
    
-   vi：越南语
    

instruction

str

否

设置指令，用于控制方言、情感或角色等合成效果。

具体用法请参见[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

enable\_aigc\_tag

bool

否

是否在生成的音频中添加AIGC隐性标识。设置为True时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

aigc\_propagator

str

否

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `True` 时生效。

默认值：阿里云UID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

aigc\_propagate\_id

str

否

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `True` 时生效。

默认值：本次语音合成请求Request ID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

hot\_fix

dict

否

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

cosyvoice-v2不支持该功能。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
    
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。
    

示例：

```
"hot_fix": {
  "pronunciation": [
    {"天气": "tian1 qi4"}
  ],
  "replace": [
    {"今天": "金天"}
  ]
}
```

enable\_markdown\_filter

bool

否

是否启用 Markdown 过滤。启用该功能后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号，避免将其朗读为文字内容。仅cosyvoice-v3-flash复刻音色支持该功能。

默认值：False。

取值范围：

-   True：启用Markdown过滤
    
-   False：禁用Markdown过滤
    

stream

bool

否

是否启用流式模式。设为`False`时为非流式调用，返回包含音频URL的结果对象；设为`True`时为流式调用，返回音频数据分片的迭代器。默认为`False`。

api\_key

str

否

API Key。如果未指定，SDK会自动从环境变量`DASHSCOPE_API_KEY`中读取。

**返回值**：

-   **非流式模式**（`stream=False`）：返回结果对象，包含以下属性：
    
    -   `audio_url`：音频下载URL（有效期有限）。
        
    -   `audio_id`：音频ID。
        
    -   `expires_at`：URL过期时间。
        
-   **流式模式**（`stream=True`）：返回迭代器，每个元素包含以下属性：
    
    -   `audio_data`：当前分片的音频二进制数据（bytes）。
        
    -   `sentences`：句子级别的合成信息（如有）。
        
    
    **重要**
    
    流式模式下，迭代器的最后一个元素除了包含音频数据分片外，还会额外返回`audio_url`（完整音频的下载地址）。如果在拼接音频数据时不跳过该元素，会导致最终生成的音频中同一段内容重复播放。因此在遍历迭代器时，需通过`not chunk.audio_url`条件过滤包含完整音频URL的最后一个元素。
    

## **示例代码**

以下示例展示CosyVoice语音合成的非流式和流式调用方式。运行前请确保已设置环境变量`DASHSCOPE_API_KEY`。

**重要**

不同模型版本需使用对应版本的音色。例如`cosyvoice-v3-flash`和`cosyvoice-v3-plus`使用`longanhuan`等音色，`cosyvoice-v2`使用`longxiaochun_v2`等音色。更换模型时请同步更换为对应版本的音色。此外，每个音色支持的语言不同，合成非中文语言时，需选择支持对应语言的音色。具体的模型与音色对应关系，请参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)。

### **非流式调用**

非流式调用设置`stream=False`，等待合成完成后返回音频URL，通过URL下载音频文件。

```
# -*- coding: utf-8 -*-
import os
from dashscope.audio.http_tts.http_speech_synthesizer import HttpSpeechSynthesizer

# 未配置环境变量时，将下行替换为：api_key = "sk-xxx"，即替换为实际的API Key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 非流式调用，返回音频URL
result = HttpSpeechSynthesizer.call(
    model="cosyvoice-v3-flash",  # 更换模型时，需同步更换为对应版本的音色
    text="今天是个好日子，适合构建人们喜爱的产品！",
    voice="longanhuan",  # 该音色适用于cosyvoice-v3系列，cosyvoice-v2请使用longxiaochun_v2等v2音色
    format="wav",
    sample_rate=24000,
    stream=False,
    api_key=api_key,
)

# 获取音频URL
print(f"音频 URL: {result.audio_url}")
print(f"音频 ID: {result.audio_id}")
if result.audio_id:
    request_id = result.audio_id.removeprefix("audio_")
    print(f"请求 Id: {request_id}")
print(f"过期时间: {result.expires_at}")
```

### **流式调用**

流式调用设置`stream=True`，返回迭代器，逐段获取音频数据。适用于对首包延迟有要求的实时播放场景。流式模式下，迭代器的最后一个元素会额外返回完整音频的`audio_url`，遍历时需通过`not chunk.audio_url`过滤该元素，避免音频内容重复。

```
# -*- coding: utf-8 -*-
import os
from dashscope.audio.http_tts.http_speech_synthesizer import HttpSpeechSynthesizer

# 未配置环境变量时，将下行替换为：api_key = "sk-xxx"，即替换为实际的API Key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 流式调用，逐段返回音频数据
stream_result = HttpSpeechSynthesizer.call(
    model="cosyvoice-v3-flash",  # 更换模型时，需同步更换为对应版本的音色
    text="今天是个好日子，适合构建人们喜爱的产品！",
    voice="longanhuan",  # 该音色适用于cosyvoice-v3系列，cosyvoice-v2请使用longxiaochun_v2等v2音色
    format="wav",
    sample_rate=24000,
    stream=True,
    api_key=api_key,
)

# 遍历迭代器，逐段接收音频数据
audio_chunks = []
for chunk in stream_result:
    if not chunk.audio_url and chunk.audio_data:  # 过滤最后一个包含完整音频URL的chunk，避免音频重复
        audio_chunks.append(chunk.audio_data)
        print(f"收到音频数据块，大小: {len(chunk.audio_data)} bytes")

    if chunk.sentences:
        print(f"句子信息: {chunk.sentences}")
    
    if chunk.audio_id:
        print(f"Audio ID: {chunk.audio_id}")
        request_id = chunk.audio_id.removeprefix("audio_")
        print(f"请求 Id: {request_id}")

# 合并所有音频数据并保存
full_audio = b"".join(audio_chunks)
print(f"总音频大小: {len(full_audio)} bytes")

with open("output.wav", "wb") as f:
    f.write(full_audio)
print("音频已保存到 output.wav")
```
