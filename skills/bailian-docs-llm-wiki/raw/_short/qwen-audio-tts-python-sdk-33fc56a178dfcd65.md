# Qwen-Audio-TTS Python SDK

本文介绍通过DashScope Python SDK进行Qwen-Audio-TTS实时语音合成的类定义、请求参数和示例代码。

## 接口地址

SDK的接口地址由Client构造参数`workspace`/`region`决定（对应下方地址，包含WorkspaceId）。如需切换到其他地域，请修改Client构造参数为对应地域的值。

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

## 核心资源（`client.audio.tts`）

**资源路径**：`client.audio.tts`

**功能**：基于WebSocket的语音合成，提供一次性合成（`synthesize`）、流式合成（`stream`）与双向流式会话（`connect`）三种调用形态。

### 调用入口

```
# 一次性合成：返回完整音频 bytes
audio = client.audio.tts.synthesize(
    text,                      # text 必填（位置参数）
    model="qwen-audio-3.0-tts-flash", # 音色所属模型
    voice="longanhuan_v3.6",   # 音色
    format="mp3",              # 音频编码格式，默认 "mp3"
    sample_rate=22050,         # 采样率，默认 22050
)

# 流式合成：逐块产出音频 bytes（边收边写/播）
for chunk in client.audio.tts.stream(text, model=..., voice=...):
    ...

# 双向流式会话：逐段输入文本，进入 with 上下文时自动建立连接
with client.audio.tts.connect(model=..., voice=...) as session:
    session.send_text(text)    # 可多次调用追加文本
    session.stop()             # 通知服务端输入结束
    for chunk in session.audio_chunks():
        ...
```

### synthesize() - 非流式调用

**方法签名**：

```
def synthesize(self, text: str, *, model: str,
               voice: str, format: str = "mp3",
               sample_rate: int = 22050, volume: int = None,
               rate: float = None, pitch: float = None,
               language_hints: list = None, enable_ssml: bool = None,
               parameters: Dict = None, ...) -> bytes
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

`text`

`str`

是

待合成的完整文本，长度不得超过20000字符。

**返回值**：`bytes`，完整音频数据。

**说明**：非流式调用，阻塞等待并一次性返回完整音频数据。适用于短文本、对实时性无严格要求的场景。`synthesize`与`stream`每次调用自建会话，无需复用实例。

### stream() - 流式调用

**方法签名**：

```
def stream(self, text: str, *, model: str, voice: str,
           format: str = "mp3", sample_rate: int = 22050, ...) -> Iterator[bytes]
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

`text`

`str`

是

待合成的完整文本，长度不得超过20000字符。

**返回值**：`Iterator[bytes]`，逐块产出的音频数据。

**说明**：流式合成，一次性发送完整文本并逐块产出音频（`Iterator[bytes]`）。适用于对实时性要求高的短文本语音合成场景。需要分片提交文本时请使用[双向流式会话（`connect`）](#h4-py-cv-sendtext)。

### send\_text() - 流式输入（会话方法）

双向流式会话（`client.audio.tts.connect(...)`）中分片提交文本。

**方法签名**：

```
def send_text(self, text: str) -> None
```

**参数说明**：`text`为当前待合成的文本片段。可多次调用`send_text`以追加文本，单次不超过20000字符，累计不超过20万字符。发送文本与接收音频需并发进行（配合`audio_chunks()`/`events()`和`stop`使用）。

### stop() - 结束流式输入（会话方法）

**方法签名**：

```
def stop(self) -> None
```

**说明**：通知服务端所有文本已发送完毕。调用后不阻塞当前线程，接收线程需继续消费`audio_chunks()`/`events()`直到剩余文本合成完成并返回所有音频数据。未调用此方法可能导致尾部文本无法转换为语音。

### cancel() - 取消流式合成（会话方法）

**方法签名**：

```
def cancel(self) -> None
```

**说明**：取消当前轮次的流式语音合成任务。调用后，SDK 会立即结束当前任务。取消后当前会话不能再发送文本，如需继续合成请新建会话。

### 会话指标与响应（会话属性）

```
session.first_package_delay
session.usage
session.last_response
```

-   `first_package_delay`：`float`，从发送文本到收到第一块音频数据的延迟时间（毫秒）。需在合成完成后读取。
-   `usage`：`dict`，最近一次合成任务的用量信息。
-   `last_response`：`dict`，最近一次合成任务的响应消息（含 `header`/`payload` 键）。最近一次请求的request\_id可从`session.last_response`的`header`中获取，可用于问题排查和日志关联。

### 请求参数

以下参数通过`client.audio.tts`的`synthesize`/`stream`/`connect`方法设置，用于控制合成音频的模型、音色、格式和音频特征（`model`、`voice`、`format`、`sample_rate`、`volume`、`rate`、`pitch`、`language_hints`、`enable_ssml`为具名参数，其余参数通过`parameters`字典传入）。

**参数**

**类型**

**是否必须**

**说明**

`model`

`str`

是

模型名称。

`voice`

`str`

是

语音合成所使用的音色。

-   **系统音色**：参见[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)
-   **复刻音色**：通过声音复刻功能定制
-   **声音设计音色**：通过声音设计功能定制

`format`

`str`

否

音频编码格式。

默认值：mp3。

支持mp3、wav、pcm等格式；采样率通过`sample_rate`参数设置，默认22050。

`volume`

`int`

否

音量。

默认值：50。

取值范围：\[0, 100\]。

`rate`

`float`

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`pitch`

`float`

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`bit_rate`

`int`

否

音频码率（kbps）。音频格式为mp3或opus时，支持通过`bit_rate`参数调整码率。

默认值：32。

取值范围：\[6, 510\]。

`bit_rate`需要通过`parameters`字典进行设置：

```
audio = client.audio.tts.synthesize(
    "待合成文本",
    model="qwen-audio-3.0-tts-flash",
    voice="longanhuan_v3.6",
    parameters={"bit_rate": 128},
)
```

`word_timestamp_enabled`

`bool`

否

是否开启字级别时间戳。

默认值：false。

仅在流式输出模式下可用。支持复刻音色；支持的系统音色请参见[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。

`word_timestamp_enabled`需要通过`parameters`字典进行设置：

```
audio = client.audio.tts.stream(
    "待合成文本",
    model="qwen-audio-3.0-tts-flash",
    voice="your_voice",  # 支持字级别时间戳的系统音色或复刻音色
    parameters={"word_timestamp_enabled": True},
)
```

`seed`

`int`

否

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

`language_hints`

`list[str]`

否

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见[声音复刻API参考](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-create)。

指定语音合成的目标语言，提升合成效果。

当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：

-   数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”
-   符号朗读不准确，“@”读成“艾特”而非“at”
-   小语种合成效果差，合成不自然

取值范围

-   zh：中文
-   en：英语
-   fr：法语
-   de：德语
-   ja：日语
-   ko：韩语
-   ru：俄语
-   pt：葡萄牙语
-   th：泰语
-   id：印尼语
-   vi：越南语
-   es：西班牙语
-   it：意大利语
-   ms：马来西亚语
-   fil：菲律宾语
-   ar：阿拉伯语

`instruction`

`str`

否

设置指令，用于控制方言、情感或角色等合成效果。

使用说明请参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

`enable_aigc_tag`

`bool`

否

是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

`enable_aigc_tag`、`aigc_propagator`和`aigc_propagate_id`需要通过`parameters`字典进行设置：

```
audio = client.audio.tts.synthesize(
    "待合成文本",
    model="qwen-audio-3.0-tts-flash",
    voice="longanhuan_v3.6",
    parameters={
        "enable_aigc_tag": True,
        "aigc_propagator": "your_propagator",
        "aigc_propagate_id": "your_propagate_id"
    },
)
```

`aigc_propagator`

`str`

否

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

需要通过`parameters`字典进行设置，参见`enable_aigc_tag`的示例。

`aigc_propagate_id`

`str`

否

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

需要通过`parameters`字典进行设置，参见`enable_aigc_tag`的示例。

`hot_fix`

`dict`

否

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。

示例：

```
audio = client.audio.tts.synthesize(
    "待合成文本",
    model="qwen-audio-3.0-tts-flash",
    voice="longanhuan_v3.6", # 音色
    parameters={
        "hot_fix": {
            "pronunciation": [{"天气": "tian1 qi4"}],
            "replace": [{"今天": "金天"}]
        }
    },
)
```

## 会话与事件迭代

流式合成不再使用回调接口：音频与服务端事件通过会话的迭代方法接收。`stream()`/`synthesize()`无需会话管理；双向流式会话（`client.audio.tts.connect(...)`）的生命周期为：进入`with`上下文自动建立连接 → 多次`send_text()` → `stop()` → 读完全部结果 → 退出上下文自动关闭。

### audio\_chunks() - 迭代音频数据

**方法签名**：

```
def audio_chunks(self) -> Iterator[bytes]
```

**返回值**：`Iterator[bytes]`，逐块产出的音频二进制数据片段，格式由`format`参数指定。

**说明**：在接收线程中迭代，逐块接收音频数据，合成过程中会产出多块。可将数据写入文件或送入播放设备。同一会话只允许一个`events()`或`audio_chunks()`读取者。

### events() - 迭代服务端事件

**方法签名**：

```
def events(self) -> Generator[Union[Dict, bytes], None, None]
```

**返回值**：同时产出服务端响应事件（`dict`，包含`header`（请求信息）和`payload`（输出信息））与音频`bytes`。其中`payload.output`包含事件类型、原始文本等信息，详见[events()事件中的output字段](#h2-py-output-info)。

**说明**：在接收线程中迭代服务端回复，包含合成事件的输出信息（事件类型、原始文本、句子信息等），可直接访问`payload.output`获取详细信息。

### 错误处理

合成过程中发生错误时，ws层会以`DashScopeError`异常抛出，异常触发后连接将自动关闭。可在发送/接收处使用try/except捕获并记录错误日志以便排查问题：

```
from dashscope.v2 import DashScopeError

try:
    ...
except DashScopeError as e:
    print(e.code, e.message, e.request_id)
```

### 会话生命周期

-   进入`with`上下文时自动建立连接（可在此前初始化音频输出流或打开文件等资源）。
-   所有文本合成完成且音频数据已全部产出后，`events()`/`audio_chunks()`迭代结束；此后可读取`first_package_delay`等性能指标。
-   退出`with`上下文时自动关闭连接（可在此后释放音频播放设备等资源）。

## events()事件中的output字段

会话`events()`迭代产出的事件`dict`中，`payload.output`包含合成事件的输出信息，可用于跟踪合成进度和获取逐句信息。以下为`output`字段的结构说明：

**字段**

**类型**

**说明**

`type`

`str`

事件类型。取值为`sentence-begin`（句子合成开始）、`sentence-synthesis`（句子合成中）或`sentence-end`（句子合成结束）。

`original_text`

`str`

当前句子的原始文本。在`sentence-begin`和`sentence-end`事件中返回。

`sentence`

`dict`

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
def handle_event(event):
    output = (event.get('payload') or {}).get('output') or {}
    event_type = output.get('type', '')
    original_text = output.get('original_text', '')
    if event_type:
        print(f'事件类型: {event_type}, 原始文本: {original_text}')
```

## 示例代码

SDK提供了语音合成的关键接口，支持以下几种调用方式：

-   非流式调用：阻塞式，一次性发送完整文本，直接返回完整音频。适合短文本语音合成场景。
-   单向流式调用：非阻塞式，一次性发送完整文本，通过迭代`stream`返回的音频分片接收数据。适用于对实时性要求高的短文本语音合成场景。
-   双向流式调用：非阻塞式，可分多次发送文本片段，通过会话的`audio_chunks()`/`events()`迭代实时接收增量合成的音频流。适合实时性要求高的长文本语音合成场景。

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

#### 非流式调用

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6892567871/CAEQURiBgMDRr9T4phkiIGNmYzBiZjFkZjQ4MDQzZGU4NDIyZDU2NWJjYjkyZTQ04709861_20241015153444.149.svg)

单次调用发送的文本长度不得超过20000字符，超出限制将返回错误。

**重要**`synthesize`与`stream`每次调用自建会话，无需复用实例。

```
# coding=utf-8

import os

import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

# 发送待合成文本，获取二进制音频
audio = client.audio.tts.synthesize("今天天气怎么样？", model=model, voice=voice)

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

#### dashscope CLI

```
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope speech-synthesis create -m qwen-audio-3.0-tts-flash -t "你好世界" --voice longanhuan_v3.6
```

**重要**SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见

[DashScope SDK Expert](raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

#### 单向流式调用

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6892567871/CAEQVRiBgIDv9fShrBkiIDhmNTk5YmQ1ZDgwNzRjZjRiN2VlMTU5YzI1ZGMwMTlm4709861_20241015153444.149.svg)

单次调用发送的文本长度不得超过20000字符，超出限制将返回错误。

**重要**`synthesize`与`stream`每次调用自建会话，无需复用实例。

```
# coding=utf-8

import os

from datetime import datetime

import dashscope

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

# 一次性发送待合成文本，逐块接收二进制音频
with open("output.mp3", "wb") as f:
    for chunk in client.audio.tts.stream("今天天气怎么样？", model=model, voice=voice):
        print(get_timestamp() + " 二进制音频长度为：" + str(len(chunk)))
        f.write(chunk)
print("语音合成完成，所有合成结果已被接收：" + get_timestamp())
```

#### 双向流式调用

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6892567871/CAEQVRiBgMDb7PahrBkiIDVkNjEwOTMxYjEwOTRmOWFhMmI1OTRiY2Q3ZDgzZmE54709861_20241015153444.149.svg)

单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

-   流式输入时可多次调用会话的`send_text`按顺序提交文本片段。服务端接收文本片段后自动进行分句：
    
    -   完整语句立即合成
    -   不完整语句缓存至完整后合成
    
    调用 `stop` 时，服务端会强制合成所有已接收但未处理的文本片段（包括未完成的句子）。
    
-   发送文本片段的间隔不得超过23秒，否则触发“request timeout after 23 seconds”异常。
    
    若无待发送文本，需及时调用 `stop`结束任务。
    
    **重要**请务必确保调用`stop`方法，否则可能会导致结尾部分的文本无法成功转换为语音。
    
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
from concurrent.futures import ThreadPoolExecutor

import dashscope

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

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

# 创建双向流式合成会话：进入 with 上下文时自动建立连接
with client.audio.tts.connect(
        model=model,
        voice=voice,
        format="pcm",
        sample_rate=22050,
) as session:
    # 初始化播放器
    player = pyaudio.PyAudio()
    stream = player.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)

    # 接收线程：迭代音频数据，实时播放
    def receive_audio():
        for chunk in session.audio_chunks():
            print(get_timestamp() + " 二进制音频长度为：" + str(len(chunk)))
            stream.write(chunk)

    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_audio)
        # 流式发送待合成文本
        for text in test_text:
            session.send_text(text)
            time.sleep(0.1)
        # 结束流式语音合成
        session.stop()
        receiver.result()

    print("语音合成完成，所有合成结果已被接收：" + get_timestamp())
    # 停止播放器
    stream.stop_stream()
    stream.close()
    player.terminate()

    # 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
    print('[Metric] 首包延迟为：{}毫秒'.format(session.first_package_delay))
```
