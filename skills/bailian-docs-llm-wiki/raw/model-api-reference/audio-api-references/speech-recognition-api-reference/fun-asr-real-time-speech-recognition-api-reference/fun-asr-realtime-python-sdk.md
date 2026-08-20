# Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime实时语音识别Python SDK

本文介绍Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime实时语音识别Python SDK的参数和接口细节。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](raw/model-user-guide/model-experience/asr-model.md)。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](raw/model-api-reference/preparations/get-api-key.md)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 快速开始

[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)提供了非流式调用和双向流式调用等接口。请根据实际需求选择合适的调用方式：

-   非流式调用：针对本地文件进行识别，并一次性返回完整的处理结果。适合处理录制好的音频。
-   双向流式调用：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

实例化[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)绑定[请求参数](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#555007db2033f)，调用`call`进行识别/翻译并最终获取[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)。

点击查看完整示例

```
from http import HTTPStatus
import dashscope
from dashscope.audio.asr import Recognition
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

recognition = Recognition(model='qwen-audio-3.0-asr-flash-streaming',
                          format='wav',
                          sample_rate=16000,
                          callback=None)
result = recognition.call('{YOUR_AUDIO_FILE}')
if result.status_code == HTTPStatus.OK:
    print('识别结果：')
    print(result.get_sentence())
else:
    print('Error: ', result.message)

print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay(),
        recognition.get_last_package_delay(),
    ))
```

### 双向流式调用

提交单个语音实时转写任务，通过实现回调接口的方式流式输出实时识别结果。

1.  启动流式语音识别
    
    实例化[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)绑定[请求参数](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#555007db2033f)和[回调接口（RecognitionCallback）](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#cec6e96138swr)，调用`start`方法启动流式语音识别。
    
2.  流式传输
    
    循环调用[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)的`send_audio_frame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。
    
    在发送音频数据的过程中，服务端会通过[回调接口（RecognitionCallback）](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#cec6e96138swr)的`on_event`方法，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)的`stop`方法结束语音识别。
    
    该方法会阻塞当前线程，直到[回调接口（RecognitionCallback）](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#cec6e96138swr)的`on_complete`或者`on_error`回调触发后才会释放线程阻塞。
    

点击查看完整示例

识别传入麦克风的语音

```
import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
import sys

import dashscope
import pyaudio
from dashscope.audio.asr import *

mic = None
stream = None

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer

# Real-time speech recognition callback
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic
        global stream
        print('RecognitionCallback open.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)

    def on_close(self) -> None:
        global mic
        global stream
        print('RecognitionCallback close.')
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

    def on_complete(self) -> None:
        print('RecognitionCallback completed.')  # recognition completed

    def on_error(self, message) -> None:
        print('RecognitionCallback task_id: ', message.request_id)
        print('RecognitionCallback error: ', message.message)
        # Stop and close the audio stream if it is running
        if 'stream' in globals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    'RecognitionCallback sentence end, request_id:%s, usage:%s'
                    % (result.get_request_id(), result.get_usage(sentence)))

def signal_handler(sig, frame):
    print('Ctrl+C pressed, stop recognition ...')
    # Stop recognition
    recognition.stop()
    print('Recognition stopped.')
    print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
            recognition.get_last_request_id(),
            recognition.get_first_package_delay(),
            recognition.get_last_package_delay(),
        ))
    # Forcefully exit the program
    sys.exit(0)

# main function
if __name__ == '__main__':
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

    # Create the recognition callback
    callback = Callback()

    # Call recognition service by async mode, you can customize the recognition parameters, like model, format,
    # sample_rate
    recognition = Recognition(
        model='qwen-audio-3.0-asr-flash-streaming',
        format=format_pcm,
        # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
        sample_rate=sample_rate,
        # support 8000, 16000
        semantic_punctuation_enabled=False,
        callback=callback)

    # Start recognition
    recognition.start()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")
    # Create a keyboard listener until "Ctrl+C" is pressed

    while True:
        if stream:
            data = stream.read(3200, exception_on_overflow=False)
            recognition.send_audio_frame(data)
        else:
            break

    recognition.stop()
```

识别本地语音文件

```
import os
import time
import dashscope
from dashscope.audio.asr import *

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

class Callback(RecognitionCallback):
    def on_complete(self) -> None:
        print(get_timestamp() + ' Recognition completed')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('Recognition task_id: ', result.request_id)
        print('Recognition error: ', result.message)
        exit(0)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print(get_timestamp() + ' RecognitionCallback text: ', sentence['text'])
        if RecognitionResult.is_sentence_end(sentence):
            print(get_timestamp() +
                  'RecognitionCallback sentence end, request_id:%s, usage:%s'
                  % (result.get_request_id(), result.get_usage(sentence)))

callback = Callback()

recognition = Recognition(model='qwen-audio-3.0-asr-flash-streaming',
                          format='wav',
                          sample_rate=16000,
                          callback=callback)

try:
    audio_data: bytes = None
    f = open("{YOUR_AUDIO_FILE}", 'rb')
    if os.path.getsize("{YOUR_AUDIO_FILE}"):
        # 一次性将文件数据全部读入buffer
        file_buffer = f.read()
        f.close()
        print("Start Recognition")
        recognition.start()

        # 从buffer中间隔3200字节发送一次
        buffer_size = len(file_buffer)
        offset = 0
        chunk_size = 3200

        while offset < buffer_size:
            # 计算本次要发送的数据块大小
            remaining_bytes = buffer_size - offset
            current_chunk_size = min(chunk_size, remaining_bytes)

            # 从buffer中提取当前数据块
            audio_data = file_buffer[offset:offset + current_chunk_size]

            # 发送音频数据帧
            recognition.send_audio_frame(audio_data)
            # 更新偏移量
            offset += current_chunk_size

            # 添加延迟模拟实时传输
            time.sleep(0.1)

        recognition.stop()
    else:
        raise Exception(
            'The supplied file was empty (zero bytes long)')
except Exception as e:
    raise e

print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay(),
        recognition.get_last_package_delay(),
    ))
```

## 接口地址

SDK的接口地址需在初始化前设置为下方地址（包含WorkspaceId）。如需切换到其他地域，请修改 `dashscope.base_websocket_api_url`为对应地域的URL。

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**切换到新加坡地域**：

```
import dashscope

# 调用时请将"{WorkspaceId}"替换为真实的业务空间ID
dashscope.base_websocket_api_url = 'wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference'
```

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。现有域名仍可正常使用。

## 请求参数

请求参数通过[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)的构造方法（_init_）进行设置。

**参数**

**类型**

**是否必须**

**说明**

model

str

是

指定模型名。支持Qwen-Audio-3.0-ASR-Flash-Streaming和Fun-ASR-Realtime系列模型，详情请参见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#4a43cc1bb7kxg)。

sample\_rate

int

是

采样率（Hz）。

取值范围：8k模型仅支持 8000 Hz，其他模型支持任意采样率。

format

str

是

音频格式。

取值范围：

-   `pcm`
-   `wav`
-   `mp3`
-   `opus`
-   `speex`
-   `aac`
-   `amr`

**重要**opus/speex：必须使用Ogg封装；

wav：必须为PCM编码；

amr：仅支持AMR-NB类型。

vocabulary\_id

str

否

预编译热词列表 ID。

需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。

适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。

使用方法请参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。

vocabulary

dict

否

即时热词。

以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5\] 或 50：取 \[1, 5\] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。

适用于临时性、会话级别的热词优化。

与预编译热词同时配置时，仅即时热词生效。使用方法请参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。

**重要**仅`qwen-audio-3.0-asr-flash-streaming`支持即时热词。

示例：

```
from dashscope.audio.asr import Recognition

vocab = {"张三": 5, "李四": 5}
recognition = Recognition(
    model='qwen-audio-3.0-asr-flash-streaming',
    format='wav',
    sample_rate=16000,
    vocabulary=vocab,
    callback=None)
```

semantic\_punctuation\_enabled

bool

否

是否启用语义断句。

默认值：False。

-   True：开启语义断句，关闭 VAD 断句。
-   False（默认）：开启 VAD 断句，关闭语义断句。

语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。

max\_sentence\_silence

int

否

VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。当`semantic_punctuation_enabled`为true时，不作为`sentence_end`返回依据，但设置过小可能会影响识别效果。

默认值：1300。

取值范围：\[200, 6000\]。

multi\_threshold\_mode\_enabled

bool

否

**重要**仅在`semantic_punctuation_enabled`参数为false时生效。

是否启用多阈值模式。启用后可防止 VAD 断句切割过长。

默认值：False。

punctuation\_prediction\_enabled

bool

否

设置是否在识别结果中自动添加标点：

-   True（默认）：是，不支持修改。

heartbeat

bool

否

是否启用心跳包。

默认值：False。

-   True：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
-   False（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

使用该字段时，SDK版本不能低于1.23.1。

language\_hints

list\[str\]

否

待识别音频语种。无默认值，不设置时模型自动识别。

对于 Qwen-Audio-3.0-ASR-Flash-Streaming 系列模型，最多支持设置 4 个值，即便设置超出 4 个，也仅前 4 个生效；对于 Fun-ASR-Realtime 系列模型，仅支持设置 1 个值，即便设置多个，也仅第一个生效。

点击查看支持的语言代码

-   qwen-audio-3.0-asr-flash-streaming、fun-asr-realtime、fun-asr-realtime-2025-11-07：
    
    -   zh: 中文
    -   en: 英文
    -   ja: 日语
    -   ko：韩语
    -   vi：越南语
    -   th：泰语
    -   id：印尼语
    -   ms：马来语
    -   tl：菲律宾语
    -   hi：印地语
    -   ar：阿拉伯语
    -   fr：法语
    -   de：德语
    -   es：西班牙语
    -   pt：葡萄牙语
    -   ru：俄语
    -   it：意大利语
    -   nl：荷兰语
    -   sv：瑞典语
    -   da：丹麦语
    -   fi：芬兰语
    -   no：挪威语
    -   el：希腊语
    -   pl：波兰语
    -   cs：捷克语
    -   hu：匈牙利语
    -   ro：罗马尼亚语
    -   bg：保加利亚语
    -   hr：克罗地亚语
    -   sk：斯洛伐克语
-   fun-asr-realtime-2026-02-28：
    
    -   zh: 中文
    -   en: 英文
    -   ja: 日语
-   fun-asr-realtime-2025-09-15：
    
    -   zh: 中文
    -   en: 英文
-   fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：
    
    -   zh: 中文

speech\_noise\_threshold

float

否

语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。

取值范围：\[-1.0, 1.0\]。

取值说明：

-   取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写
-   取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤

此参数为高级配置参数，调整可能显著影响识别效果，建议：

-   调整前充分测试验证效果
-   根据实际音频环境小幅度调整（建议步长 0.1）

special\_word\_filter

str

否

指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见[敏感词过滤](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_sensitive_h3)。

callback

RecognitionCallback

否

[回调接口（RecognitionCallback）](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#cec6e96138swr)。

以下参数通过`Recognition`实例的`call`或`start`方法的关键字参数传入。

**参数**

**类型**

**是否必须**

**说明**

raw\_input

dict

否

输入对象，用于传入对话上下文（context）。上下文用于辅助识别、提升专有词汇的识别准确率。使用方法详见[快速开始](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx_quickstart_sec)。

**重要**仅 `qwen-audio-3.0-asr-flash-streaming`、`fun-asr-realtime` 和 `fun-asr-realtime-2025-11-07` 模型支持 context 参数。

dict 中需包含 `context` 键，值为消息列表（list\[dict\]），每条消息包含以下字段：

-   `role`（str，必选）：消息角色。`user` 表示前几轮用户语音的识别结果或领域相关的词表；`assistant` 表示前几轮大语言模型的回复内容。
-   `content`（list\[dict\]，必选）：消息内容列表。每个元素包含 `type`（str，role 为 user 时填 `input_text`，role 为 assistant 时填 `text`）和 `text`（str，文本内容）。

**重要**约束：上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度不超过 400 个字符，超出部分从末尾截断。

**重要**携带上下文时，`context` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

**说明**使用该字段时，SDK版本不能低于1.25.23。

`raw_input`通过`Recognition`实例的`start`或`call`方法传入：

```
# 构建 input 传入数据
input_context = {
    "context": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "你好啊"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "你好啊，我是通义千问，有什么可以帮助你的？"
                }
            ]
        }
    ]
}

# 通过 raw_input 参数传入
recognition.start(raw_input=input_context)
# 或者
recognition.call(raw_input=input_context)
```

## 关键接口

### `Recognition`类

`Recognition`通过“`from dashscope.audio.asr import *`”方式引入。

**成员方法**

**方法签名**

**说明**

call

```
def call(self, file: str, phrase_id: str = None, **kwargs) -> RecognitionResult
```

基于本地文件的非流式调用，该方法会阻塞当前线程直到全部音频读完，该方法要求所识别文件具有可读权限。

识别结果以`RecognitionResult`类型数据返回。

start

```
def start(self, phrase_id: str = None, **kwargs)
```

开始语音识别。

基于回调形式的流式实时识别，该方法不会阻塞当前线程。需要配合`send_audio_frame`和`stop`使用。

send\_audio\_frame

```
def send_audio_frame(self, buffer: bytes)
```

推送音频。每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。

识别结果通过[回调接口（RecognitionCallback）](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#cec6e96138swr)的on\_event方法获取。

stop

```
def stop(self)
```

停止语音识别，阻塞到服务将收到的音频都识别后结束任务。

get\_last\_request\_id

```
def get_last_request_id(self)
```

获取request\_id，在构造函数调用（创建对象）后可以使用。

get\_first\_package\_delay

```
def get_first_package_delay(self)
```

获取首包延迟，从发送第一包音频到收到首包识别结果延迟，在任务完成后使用。

get\_last\_package\_delay

```
def get_last_package_delay(self)
```

获得尾包延迟，发送`stop`指令到最后一包识别结果下发耗时，在任务完成后使用。

get\_response

```
def get_response(self)
```

获取最后一次报文，可以用于获取task-failed报错。

### 回调接口（`RecognitionCallback`）

[双向流式调用](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#7b019225eeqet)时，服务端会通过回调的方式，将关键流程信息和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

点击查看示例

```
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        print('连接成功')

    def on_event(self, result: RecognitionResult) -> None:
        # 实现接收识别结果的逻辑
        pass

    def on_complete(self) -> None:
        print('任务完成')

    def on_error(self, result: RecognitionResult) -> None:
        print('出现异常：', result)

    def on_close(self) -> None:
        print('连接关闭')

callback = Callback()
```

**方法**

**参数**

**返回值**

**描述**

```
def on_open(self) -> None
```

无

无

当和服务端建立连接完成后，该方法立刻被回调。

```
def on_event(self, result: RecognitionResult) -> None
```

`result`：[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)

无

当服务有回复时会被回调。

```
def on_complete(self) -> None
```

无

无

当所有识别结果全部返回后进行回调。

```
def on_error(self, result: RecognitionResult) -> None
```

`result`：[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)

无

发生异常时该方法被回调。

```
def on_close(self) -> None
```

无

无

当服务已经关闭连接后进行回调。

## 响应结果

### 识别结果（`RecognitionResult`）

`RecognitionResult`代表[双向流式调用](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#9d1e5f6852jr8)中一次实时识别或[非流式调用](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#8341058094tc3)的识别结果。

**成员方法**

**方法签名**

**说明**

get\_sentence

```
def get_sentence(self) -> Union[Dict[str, Any], List[Any]]
```

获取当前识别的句子及时间戳信息。回调中返回的是单句信息，所以此方法返回类型为Dict\[str, Any\]。

详情请参见[单句信息（Sentence）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#f28f50b035qtn)。

get\_request\_id

```
def get_request_id(self) -> str
```

获取请求的request\_id。

is\_sentence\_end

```
@staticmethod
def is_sentence_end(sentence: Dict[str, Any]) -> bool
```

判断给定句子是否已经结束。该方法通过检查 `sentence` 中 `end_time` 字段是否为 `None` 来判定——`end_time` 不为 `None` 时表示句子已结束。调用方式为 `RecognitionResult.is_sentence_end(sentence)`，其中 `sentence` 为 `get_sentence()` 返回的单句信息 dict，而非 `Sentence` 实例的布尔字段。

### 单句信息（`Sentence`）

Sentence类成员如下：

**参数**

**类型**

**说明**

begin\_time

int

句子开始时间，单位为ms。

end\_time

int

句子结束时间，单位为ms。

text

str

识别文本。

words

[字时间戳信息（Word）](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#b55a7391caxxe)的list集合

字时间戳信息。

### 字时间戳信息（`Word`）

Word类成员如下：

**参数**

**类型**

**说明**

begin\_time

int

字开始时间，单位为ms。

end\_time

int

字结束时间，单位为ms。

text

str

字。

punctuation

str

标点。

## 错误码

如遇报错问题，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。

## 常见问题

### 功能特性

#### Q：在长时间静默的情况下，如何保持与服务端长连接？

将请求参数`heartbeat`设置为true，并持续向服务端发送静音音频。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

#### Q：如何将音频格式转换为满足要求的格式？

可使用[FFmpeg工具](https://ffmpeg.en.lo4d.com/download)，更多用法请参见FFmpeg官网。

```
# 基础转换命令（万能模板）
# -i，作用：输入文件路径，常用值示例：audio.wav
# -c:a，作用：音频编码器，常用值示例：aac, libmp3lame, pcm_s16le
# -b:a，作用：比特率（音质控制），常用值示例：192k, 320k
# -ar，作用：采样率，常用值示例：44100 (CD), 48000, 16000
# -ac，作用：声道数，常用值示例：1(单声道), 2(立体声)
# -y，作用：覆盖已存在文件(无需值)
ffmpeg -i input_audio.ext -c:a 编码器名 -b:a 比特率 -ar 采样率 -ac 声道数 output.ext

# 例如：WAV → MP3（保持原始质量）
ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3
# 例如：MP3 → WAV（16bit PCM标准格式）
ffmpeg -i input.mp3 -c:a pcm_s16le -ar 44100 -ac 2 output.wav
# 例如：M4A → AAC（提取/转换苹果音频）
ffmpeg -i input.m4a -c:a copy output.aac  # 直接提取不重编码
ffmpeg -i input.m4a -c:a aac -b:a 256k output.aac  # 重编码提高质量
# 例如：FLAC无损 → Opus（高压缩）
ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on output.opus
```

#### Q：如何识别本地文件（录音文件）？

识别本地文件有两种方式：

-   直接传入本地文件路径：此种方式在最终识别结束后获取完整识别结果，不适合即时反馈的场景。
    
    参见[非流式调用](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#881157aa56lll)，在[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)的`call`方法中传入文件路径对录音文件直接进行识别。
    
-   将本地文件转成二进制流进行识别：此种方式一边识别文件一边流式获取识别结果，适合即时反馈的场景。
    
    参见[双向流式调用](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#7b019225eeqet)，通过[Recognition类](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk#44f87473bfp2m)的`send_audio_frame`方法向服务端发送二进制流对其进行识别。
    

### 故障排查

#### Q：无法识别语音（无识别结果）是什么原因？

1.  请检查请求参数中的音频格式（`format`）和采样率（`sampleRate`/`sample_rate`）设置是否正确且符合参数约束。以下为常见错误示例：
    
    -   音频文件扩展名为 .wav，但实际为 MP3 格式，而请求参数 `format` 设置为 mp3（参数设置错误）。
    -   音频采样率为 3600Hz，但请求参数 `sampleRate`/`sample_rate` 设置为 48000（参数设置错误）。
    
    可以使用[ffprobe](https://ffmpeg.org/ffprobe.html)工具获取音频的容器、编码、采样率、声道等信息：
    

```
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
```

2.  若以上检查均无问题，可通过定制热词提升对特定词语的识别效果。
