# 实时语音合成CosyVoice Python SDK

本文介绍通过DashScope Python SDK进行CosyVoice实时语音合成的类定义、请求参数和示例代码。

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **服务端点**

SDK默认使用**北京地域**的服务端点。如需切换到其他地域，需在初始化前修改 `dashscope.base_websocket_api_url`。

### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`wss://dashscope.aliyuncs.com/api-ws/v1/inference`

### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference`

**切换到新加坡地域**：

```
import dashscope

# 在代码开头设置
dashscope.base_websocket_api_url = 'wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference'
```

## **SpeechSynthesizer**

**包路径**：`dashscope.audio.tts_v2.SpeechSynthesizer`

### **构造方法**

```
SpeechSynthesizer(
    model: str,
    voice: str,
    format: AudioFormat = AudioFormat.MP3_22050HZ_MONO_256KBPS,
    volume: int = 50,
    speech_rate: float = 1.0,
    pitch_rate: float = 1.0,
    callback: ResultCallback = None)
```

### **call() - 非流式调用**

**方法签名**：

```
def call(self, text: str) -> bytes
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

text

str

是

待合成的完整文本，长度不得超过20000字符。

**返回值**：`bytes`，完整音频数据。

**说明**：非流式调用，阻塞等待并一次性返回完整音频数据。适用于短文本、对实时性无严格要求的场景。每次调用前需重新初始化SpeechSynthesizer实例。

### **streaming\_call() - 流式调用**

**方法签名**：

```
def streaming_call(self, text: str) -> None
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

text

str

是

当前待合成的文本片段。可多次调用以追加文本，单次不超过20000字符，累计不超过20万字符。

**说明**：双向流式调用，支持分片提交文本并通过回调实时获取合成音频。适用于与大语言模型对接、边生成文本边合成语音的场景。发送完毕后需调用streaming\_complete()结束合成。

### **streaming\_complete() - 结束流式合成**

**方法签名**：

```
def streaming_complete(self) -> None
```

**说明**：通知服务端所有文本已发送完毕，阻塞当前线程直到剩余文本合成完成并返回所有音频数据。未调用此方法可能导致尾部文本无法转换为语音。

### **get\_last\_request\_id() - 获取请求ID**

**方法签名**：

```
def get_last_request_id(self) -> str
```

**返回值**：`str`，最近一次请求的request\_id，可用于问题排查和日志关联。

### **get\_first\_package\_delay() - 获取首包延迟**

**方法签名**：

```
def get_first_package_delay(self) -> int
```

**返回值**：`int`，从发送文本到收到第一块音频数据的延迟时间（毫秒）。需在合成完成后调用。

### **get\_response() - 获取响应消息**

**方法签名**：

```
def get_response(self) -> str
```

**返回值**：`str`，最近一次合成任务的JSON格式响应消息，包含请求状态和输出信息。

### **构造参数**

以下参数通过SpeechSynthesizer构造方法设置，用于控制合成音频的模型、音色、格式和音频特征。

**参数**

**类型**

**是否必须**

**说明**

model

str

是

模型名称。

voice

str

是

**voice** `_string_` **（必选）**

语音合成所使用的音色。

-   **系统音色**：参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
    
-   **复刻音色**：通过声音复刻功能定制
    
-   **声音设计音色**：通过声音设计功能定制
    

format

enum

否

音频编码格式及采样率。

`cosyvoice-v1`不支持opus格式。

默认值：AudioFormat.MP3\_22050HZ\_MONO\_256KBPS。

AudioFormat枚举类的包路径：`dashscope.audio.tts_v2`，支持MP3、WAV、PCM等格式。

volume

int

否

音量。

默认值：50。

取值范围：\[0, 100\]。

speech\_rate

float

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

pitch\_rate

float

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

bit\_rate

int

否

音频码率（kbps）。音频格式为opus时，支持通过`bit_rate`参数调整码率。

默认值：32。

取值范围：\[6, 510\]。

`cosyvoice-v1`模型不支持该参数。

**说明**

`bit_rate`需要通过`additional_params`参数进行设置：

```
synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3-flash",
    voice="longanyang",
    additional_params={"bit_rate": 128000}
)
```

word\_timestamp\_enabled

bool

否

是否开启字级别时间戳。

默认值：false。

仅适用于cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色。

**说明**

`word_timestamp_enabled`需要通过`additional_params`参数进行设置：

```
synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3-flash",
    voice="your_voice",
    additional_params={"word_timestamp_enabled": True}
)
```

seed

int

否

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

cosyvoice-v1不支持该参数。

language\_hints

list\[str\]

否

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
    
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见声音复刻API参考。
    

指定语音合成的目标语言，提升合成效果。cosyvoice-v1不支持该功能。

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

使用说明请参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

enable\_aigc\_tag

bool

否

是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**说明**

`enable_aigc_tag`、`aigc_propagator`和`aigc_propagate_id`需要通过`additional_params`参数进行设置：

```
synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3-flash",
    voice="longanyang",
    additional_params={
        "enable_aigc_tag": True,
        "aigc_propagator": "your_propagator",
        "aigc_propagate_id": "your_propagate_id"
    }
)
```

aigc\_propagator

str

否

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

需要通过`additional_params`参数进行设置，参见`enable_aigc_tag`的示例。

aigc\_propagate\_id

str

否

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

需要通过`additional_params`参数进行设置，参见`enable_aigc_tag`的示例。

hot\_fix

dict

否

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

cosyvoice-v2、cosyvoice-v1不支持该功能。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
    
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。
    

示例：

```
synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3-flash",
    voice="your_voice", # 替换成cosyvoice-v3-flash复刻音色
    hot_fix={
        "pronunciation": [{"天气": "tian1 qi4"}],
        "replace": [{"今天": "金天"}]
    }
)
```

enable\_markdown\_filter

bool

否

**重要**

仅cosyvoice-v3-flash复刻音色支持该功能。

是否启用 Markdown 过滤。启用该功能后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号，避免将其朗读为文字内容。

默认值：false。

取值范围：

-   true：启用Markdown过滤
    
-   false：禁用Markdown过滤
    

**说明**

`enable_markdown_filter`需要通过`additional_params`参数进行设置：

```
synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3-flash",
    voice="your_voice", # 替换成cosyvoice-v3-flash复刻音色
    additional_params={"enable_markdown_filter": True}
)
```

callback

ResultCallback

否

回调函数实例，用于异步接收合成音频和事件通知。设置此参数时，call()方法以流式模式运行，音频数据通过on\_data回调返回；不设置时，call()以非流式模式运行，直接返回完整音频的bytes数据。

## **ResultCallback**

**包路径**：`dashscope.audio.tts_v2.ResultCallback`

### **on\_open() - 连接建立**

**方法签名**：

```
def on_open(self) -> None
```

**触发时机**：WebSocket连接成功建立时触发。可在此回调中初始化音频输出流或打开文件等资源。

### **on\_event() - 接收服务端回复**

**方法签名**：

```
def on_event(self, message: str) -> None
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

message

str

是

服务端响应事件（JSON格式），包含`header`（请求信息）和`payload`（输出信息）。其中`payload.output`包含事件类型、原始文本等信息，详见[on\_event消息中的output字段](#sec-py-output-info)。

**触发时机**：接收到服务端回复时触发。消息为JSON字符串，包含合成事件的输出信息（事件类型、原始文本、句子信息等）。可通过`json.loads(message)`解析后访问`payload.output`获取详细信息。

### **on\_complete() - 合成完成**

**方法签名**：

```
def on_complete(self) -> None
```

**触发时机**：所有文本合成完成且音频数据已全部通过on\_data返回后触发。可在此回调中调用get\_first\_package\_delay()获取性能指标。

### **on\_data() - 接收音频数据**

**方法签名**：

```
def on_data(self, data: bytes) -> None
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

data

bytes

是

当前批次的音频二进制数据片段，格式由构造参数format指定。

**触发时机**：每接收到一块音频数据时触发，合成过程中会被多次调用。可在此回调中将数据写入文件或送入播放设备。

### **on\_error() - 发生错误**

**方法签名**：

```
def on_error(self, message: str) -> None
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

message

str

是

错误描述信息，包含错误码和详细原因。

**触发时机**：合成过程中发生错误时触发。触发后连接将自动关闭，建议在此回调中记录错误日志以便排查问题。

### **on\_close() - 连接关闭**

**方法签名**：

```
def on_close(self) -> None
```

**触发时机**：WebSocket连接关闭时触发（无论正常结束还是异常断开）。可在此回调中释放音频播放设备等资源。

## **on\_event消息中的output字段**

`on_event`回调接收的JSON消息中，`payload.output`包含合成事件的输出信息，可用于跟踪合成进度和获取逐句信息。以下为`output`字段的结构说明：

**字段**

**类型**

**说明**

type

str

事件类型。取值为`sentence-begin`（句子合成开始）、`sentence-synthesis`（句子合成中）或`sentence-end`（句子合成结束）。

original\_text

str

当前句子的原始文本。在`sentence-begin`和`sentence-end`事件中返回。

sentence

dict

句子信息。包含`index`（句子序号）和`words`（词列表，开启`word_timestamp_enabled`时返回时间戳信息）。

**消息示例**：

```
{
  "header": {
    "task_id": "xxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "type": "sentence-begin",
      "original_text": "今天天气怎么样？",
      "sentence": {
        "index": 0,
        "words": []
      }
    }
  }
}
```

**解析示例**：

```
import json

def on_event(self, message):
    data = json.loads(message)
    output = data.get('payload', {}).get('output', {})
    event_type = output.get('type', '')
    original_text = output.get('original_text', '')
    if event_type:
        print(f'事件类型: {event_type}, 原始文本: {original_text}')
```

## **示例代码**

SDK提供了语音合成的关键接口，支持以下几种调用方式：

-   非流式调用：阻塞式，一次性发送完整文本，直接返回完整音频。适合短文本语音合成场景。
    
-   单向流式调用：非阻塞式，一次性发送完整文本，通过回调函数接收音频数据（可能分片）。适用于对实时性要求高的短文本语音合成场景。
    
-   双向流式调用：非阻塞式，可分多次发送文本片段，通过回调函数实时接收增量合成的音频流。适合实时性要求高的长文本语音合成场景。
    

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

### **非流式调用**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8043679771/CAEQURiBgMDRr9T4phkiIGNmYzBiZjFkZjQ4MDQzZGU4NDIyZDU2NWJjYjkyZTQ04709861_20241015153444.149.svg)

单次调用发送的文本长度不得超过20000字符，超出限制将返回错误。

**重要**

每次调用`call`方法前，需要重新初始化`SpeechSynthesizer`实例。

```
# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

# 模型
model = "cosyvoice-v3-flash"
# 音色
voice = "longanyang"

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(model=model, voice=voice)
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("今天天气怎么样？")
# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

### **单向流式调用**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8043679771/CAEQVRiBgIDv9fShrBkiIDhmNTk5YmQ1ZDgwNzRjZjRiN2VlMTU5YzI1ZGMwMTlm4709861_20241015153444.149.svg)

单次调用发送的文本长度不得超过20000字符，超出限制将返回错误。

**重要**

每次调用`call`方法前，需要重新初始化`SpeechSynthesizer`实例。

```
# coding=utf-8

import os
import json
import dashscope
from dashscope.audio.tts_v2 import *

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

# 模型
model = "cosyvoice-v3-flash"
# 音色
voice = "longanyang"

# 定义回调接口
class Callback(ResultCallback):
    _player = None
    _stream = None

    def on_open(self):
        self.file = open("output.mp3", "wb")
        print("连接建立：" + get_timestamp())

    def on_complete(self):
        print("语音合成完成，所有合成结果已被接收：" + get_timestamp())
        # 当任务完成（on_complete 回调触发）后，才可调用 get_first_package_delay 获取延迟
        # 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
            synthesizer.get_last_request_id(),
            synthesizer.get_first_package_delay()))

    def on_error(self, message: str):
        print(f"语音合成出现异常：{message}")

    def on_close(self):
        print("连接关闭：" + get_timestamp())
        self.file.close()

    def on_event(self, message):
        # 解析服务端事件，获取输出信息
        data = json.loads(message)
        output = data.get('payload', {}).get('output', {})
        event_type = output.get('type', '')
        original_text = output.get('original_text', '')
        if event_type:
            print(f"事件类型: {event_type}, 原始文本: {original_text}")

    def on_data(self, data: bytes) -> None:
        print(get_timestamp() + " 二进制音频长度为：" + str(len(data)))
        self.file.write(data)

callback = Callback()

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(
    model=model,
    voice=voice,
    callback=callback,
)

# 发送待合成文本，在回调接口的on_data方法中实时获取二进制音频
synthesizer.call("今天天气怎么样？")
```

### **双向流式调用**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8043679771/CAEQVRiBgMDb7PahrBkiIDVkNjEwOTMxYjEwOTRmOWFhMmI1OTRiY2Q3ZDgzZmE54709861_20241015153444.149.svg)

单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

-   流式输入时可多次调用`streaming_call`按顺序提交文本片段。服务端接收文本片段后自动进行分句：
    
    -   完整语句立即合成
        
    -   不完整语句缓存至完整后合成
        
    
    调用 `streaming_complete` 时，服务端会强制合成所有已接收但未处理的文本片段（包括未完成的句子）。
    
-   发送文本片段的间隔不得超过23秒，否则触发“request timeout after 23 seconds”异常。
    
    若无待发送文本，需及时调用 `streaming_complete`结束任务。
    
    **重要**
    
    请务必确保调用`streaming_complete`方法，否则可能会导致结尾部分的文本无法成功转换为语音。
    
    > 服务端强制设定23秒超时机制，客户端无法修改该配置。
    

```
# coding=utf-8
#
# pyaudio安装说明：
# 如果是macOS操作系统，执行如下命令：
#   brew install portaudio
#   pip install pyaudio
# 如果是Debian/Ubuntu操作系统，执行如下命令：
#   sudo apt-get install python-pyaudio python3-pyaudio
#   或者
#   pip install pyaudio
# 如果是CentOS操作系统，执行如下命令：
#   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
# 如果是Microsoft Windows，执行如下命令：
#   python -m pip install pyaudio

import os
import time
import pyaudio
import json
import dashscope
from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse
from dashscope.audio.tts_v2 import *

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

# 模型
model = "cosyvoice-v3-flash"
# 音色
voice = "longanyang"

# 定义回调接口
class Callback(ResultCallback):
    _player = None
    _stream = None

    def on_open(self):
        print("连接建立：" + get_timestamp())
        self._player = pyaudio.PyAudio()
        self._stream = self._player.open(
            format=pyaudio.paInt16, channels=1, rate=22050, output=True
        )

    def on_complete(self):
        print("语音合成完成，所有合成结果已被接收：" + get_timestamp())

    def on_error(self, message: str):
        print(f"语音合成出现异常：{message}")

    def on_close(self):
        print("连接关闭：" + get_timestamp())
        # 停止播放器
        self._stream.stop_stream()
        self._stream.close()
        self._player.terminate()

    def on_event(self, message):
        # 解析服务端事件，获取输出信息
        data = json.loads(message)
        output = data.get('payload', {}).get('output', {})
        event_type = output.get('type', '')
        original_text = output.get('original_text', '')
        if event_type:
            print(f"事件类型: {event_type}, 原始文本: {original_text}")

    def on_data(self, data: bytes) -> None:
        print(get_timestamp() + " 二进制音频长度为：" + str(len(data)))
        self._stream.write(data)

callback = Callback()

test_text = [
    "流式文本语音合成SDK，",
    "可以将输入的文本",
    "合成为语音二进制数据，",
    "相比于非流式语音合成，",
    "流式合成的优势在于实时性",
    "更强。用户在输入文本的同时",
    "可以听到接近同步的语音输出，",
    "极大地提升了交互体验，",
    "减少了用户等待时间。",
    "适用于调用大规模",
    "语言模型（LLM），以",
    "流式输入文本的方式",
    "进行语音合成的场景。",
]

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(
    model=model,
    voice=voice,
    format=AudioFormat.PCM_22050HZ_MONO_16BIT,  
    callback=callback,
)

# 流式发送待合成文本。在回调接口的on_data方法中实时获取二进制音频
for text in test_text:
    synthesizer.streaming_call(text)
    time.sleep(0.1)
# 结束流式语音合成
synthesizer.streaming_complete()

# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))
```
