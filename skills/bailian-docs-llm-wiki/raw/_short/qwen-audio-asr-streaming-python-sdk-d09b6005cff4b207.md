# Qwen-Audio-ASR-Streaming实时语音识别Python SDK

本文介绍Qwen-Audio-ASR-Streaming实时语音识别Python SDK的参数和接口细节。

## 前提条件

-   已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。请配置API Key到环境变量，而非硬编码在代码中，防范因代码泄露导致的安全风险。
-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 快速开始

[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#d6bc1f133f871)提供了非流式调用和双向流式调用等接口。请根据实际需求选择合适的调用方式：

-   非流式调用（`recognize_file`）：针对本地文件进行识别，SDK自动分块发送音频并驱动到任务结束。适合处理录制好的音频。
-   双向流式调用（`recognize`会话）：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

#### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

调用[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#d6bc1f133f871)的`recognize_file`方法绑定请求参数并传入本地文件路径，迭代服务端事件获取识别结果。

```
import os
import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 识别本地语音文件：recognize_file自动分块发送音频并驱动到任务结束
for event in client.audio.asr.recognize_file(
        '{YOUR_AUDIO_FILE}',
        model='qwen-audio-3.1-asr-flash-streaming',
        format='wav',
        sample_rate=16000):
    payload = event.get('payload') or {}
    sentence = (payload.get('output') or {}).get('sentence') or {}
    if sentence.get('text') and not sentence.get('heartbeat'):
        print('识别结果：', sentence['text'])
```

#### 双向流式调用

提交单个语音实时转写任务，通过迭代事件的方式流式输出实时识别结果。

1.  启动流式语音识别
    
    调用[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#d6bc1f133f871)的`recognize`方法创建识别会话并绑定请求参数，进入`with`上下文（自动调用`start`方法建立连接并发送任务）启动流式语音识别。
    
2.  流式传输
    
    循环调用会话的`send_audio_frame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。发送与接收需并发进行：接收线程通过会话的`events()`方法迭代服务端事件，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用会话的`stop`方法结束语音识别。
    
    该方法只通知服务端输入结束；接收线程需继续消费`events()`直到`task-finished`事件以获得最后的识别结果和统计信息。ws层的错误会以`DashScopeError`异常抛出，可在发送/接收处使用try/except捕获。
    

识别传入麦克风的语音

```
import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
import sys

import dashscope
import pyaudio
from concurrent.futures import ThreadPoolExecutor

mic = None
stream = None

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer

# Real-time speech recognition event receiver
def receive_events(rec):
    for event in rec.events():
        payload = event.get('payload') or {}
        sentence = (payload.get('output') or {}).get('sentence') or {}
        if sentence.get('text') and not sentence.get('heartbeat'):
            print('Recognition text: ', sentence['text'])
            if sentence.get('sentence_end'):
                print(
                    'Recognition sentence end, request_id:%s, usage:%s'
                    % (rec.request_id, rec.usage))

def signal_handler(sig, frame):
    print('Ctrl+C pressed, stop recognition ...')
    # Stop recognition
    recognition.stop()
    print('Recognition stopped.')
    print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
            recognition.request_id,
            recognition.first_package_delay,
            recognition.last_package_delay,
        ))
    # Forcefully exit the program
    sys.exit(0)

# main function
if __name__ == '__main__':
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    client = dashscope.Client(
        api_key=os.environ.get('DASHSCOPE_API_KEY'),
        # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        workspace="{WorkspaceId}",
        region="cn-beijing",
    )

    # Call recognition service, you can customize the recognition parameters, like model, format,
    # sample_rate
    with client.audio.asr.recognize(
            model='qwen-audio-3.0-asr-flash-streaming',
            format=format_pcm,
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=sample_rate,
            # support 8000, 16000
    ) as recognition:
        # Open the microphone
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)
        with ThreadPoolExecutor(max_workers=1) as pool:
            receiver = pool.submit(receive_events, recognition)
            try:
                # Send audio from the microphone until "Ctrl+C" is pressed
                while stream:
                    data = stream.read(3200, exception_on_overflow=False)
                    recognition.send_audio_frame(data)
                recognition.stop()
                receiver.result()
            finally:
                # close must run inside the pool context to unblock the receiver
                recognition.close()
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None
```

识别本地语音文件

```
import os
import time
import dashscope
from concurrent.futures import ThreadPoolExecutor

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# Real-time speech recognition event receiver
def receive_events(rec):
    for event in rec.events():
        payload = event.get('payload') or {}
        sentence = (payload.get('output') or {}).get('sentence') or {}
        if sentence.get('text') and not sentence.get('heartbeat'):
            print(get_timestamp() + ' Recognition text: ', sentence['text'])
        if sentence.get('sentence_end'):
            print(get_timestamp() +
                  'Recognition sentence end, request_id:%s, usage:%s'
                  % (rec.request_id, rec.usage))

with client.audio.asr.recognize(
        model='qwen-audio-3.1-asr-flash-streaming',
        format='wav',
        sample_rate=16000,
) as recognition:
    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_events, recognition)
        try:
            audio_data: bytes = None
            f = open("{YOUR_AUDIO_FILE}", 'rb')
            if os.path.getsize("{YOUR_AUDIO_FILE}"):
                # 一次性将文件数据全部读入buffer
                file_buffer = f.read()
                f.close()
                print("Start Recognition")

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
                receiver.result()
            else:
                raise Exception(
                    'The supplied file was empty (zero bytes long)')
        finally:
            # close must run inside the pool context to unblock the receiver
            recognition.close()

print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
        recognition.request_id,
        recognition.first_package_delay,
        recognition.last_package_delay,
    ))
```

## 接口地址

SDK的实时识别走WebSocket接口，端点由`Client`的`workspace`与`region`自动决定（包含WorkspaceId）。如需切换到其他地域，构造`Client`时设置对应地域的`region`即可。

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

## 请求参数

请求参数通过[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#d6bc1f133f871)的`recognize`/`recognize_file`方法进行设置：`model`、`format`、`sample_rate`、`vocabulary_id`为具名参数，其余参数（如`language_hints`）通过`parameters`字典传入。

**参数**

**类型**

**是否必须**

**说明**

`model`

`str`

是

模型名称。

`sample_rate`

`int`

是

采样率（Hz），支持任意采样率。

`format`

`str`

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

`keep_dialect`

`bool`

否

仅 `qwen-audio-3.1-asr-flash-streaming` 支持。默认 `false`，将方言转写为普通话；设为 `true` 时保留方言表达。作为同名关键字参数传入。完整参数说明请参见[客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-1bae8548d2be6bc5.md)。

`vad_model`

`str`

否

仅 `qwen-audio-3.1-asr-flash-streaming` 支持。可选 `near_meeting_16k`（近场）或 `far_field_meeting_16k`（远场，默认值）。作为同名关键字参数传入。完整参数说明请参见[客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-1bae8548d2be6bc5.md)。

`vocabulary_id`

`str`

否

预编译热词列表 ID。

需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。

适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。

使用方法请参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。

`vocabulary`

`dict`

否

即时热词。

以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5\] 或 50：取 \[1, 5\] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。

适用于临时性、会话级别的热词优化。

与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。

示例：

```
import os
import dashscope

client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

# 即时热词通过parameters传入
vocab = {"张三": 5, "李四": 5}
recognition = client.audio.asr.recognize(
    model='qwen-audio-3.1-asr-flash-streaming',
    format='wav',
    sample_rate=16000,
    parameters={"vocabulary": vocab},
)
```

`max_sentence_silence`

`int`

否

VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。

默认值：800。

取值范围：\[200, 6000\]。

`multi_threshold_mode_enabled`

`bool`

否

是否启用多阈值模式。启用后可防止 VAD 断句切割过长。

默认值：False。

`punctuation_prediction_enabled`

`bool`

否

设置是否在识别结果中自动添加标点：

-   True（默认）：是，不支持修改。

`heartbeat`

`bool`

否

是否启用心跳包。

默认值：False。

-   True：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
-   False（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

使用该字段时，SDK版本不能低于2.0.1。

`language_hints`

`list[str]`

否

待识别音频语种。无默认值，不设置时模型自动识别。

最多支持设置 4 个值，超出时仅前 4 个生效。

点击查看支持的语言代码

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

`speech_noise_threshold`

`float`

否

语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。

取值范围：\[-1.0, 1.0\]。

取值说明：

-   取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写
-   取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤

此参数为高级配置参数，调整可能显著影响识别效果，建议：

-   调整前充分测试验证效果
-   根据实际音频环境小幅度调整（建议步长 0.1）

`special_word_filter`

`str`

否

指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见[敏感词过滤](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_sensitive_h3)。

以下参数通过`recognize`/`recognize_file`方法的`input`关键字参数传入。

**参数**

**类型**

**是否必须**

**说明**

`input`

`dict`

否

输入对象，用于传入对话上下文（context）。上下文用于辅助识别、提升专有词汇的识别准确率。使用方法详见[提升识别准确率](raw/model-user-guide/model-experience/speech-recognition/improve-asr-accuracy.md)。

dict 中需包含 `context` 键，值为消息列表（list\[dict\]），每条消息包含以下字段：

-   `role`（str，必选）：消息角色。`user` 表示前几轮用户语音的识别结果或领域相关的词表；`assistant` 表示前几轮大语言模型的回复内容。
-   `content`（list\[dict\]，必选）：消息内容列表。每个元素包含 `type`（str，role 为 user 时填 `input_text`，role 为 assistant 时填 `text`）和 `text`（str，文本内容）。

**重要**上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度不超过 400 个字符，超出部分从末尾截断。

**重要**携带上下文时，`context` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

**说明**使用该字段时，SDK版本不能低于2.0.1。

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

# 创建识别会话时通过 input 参数传入
recognition = client.audio.asr.recognize(
    model='qwen-audio-3.1-asr-flash-streaming',
    format='wav',
    sample_rate=16000,
    input=input_context,
)
```

## 关键接口

### 核心资源（`client.audio.asr`）

实时语音识别能力挂载在`client.audio.asr`资源上：`recognize`创建双向流式识别会话（`Recognition`），`recognize_file`对本地文件一次性识别。

**成员方法**

**方法签名**

**说明**

recognize

```
def recognize(self,
              *,
              model: str,
              format: str = "pcm",
              sample_rate: int = 16000,
              vocabulary_id: str = None,
              disfluency_removal_enabled: bool = None,
              diarization_enabled: bool = None,
              parameters: Dict = None,
              input: Dict = None,
              phrase_id: str = None,
              ...) -> Recognition
```

创建双向流式识别会话，进入`with`上下文时自动调用`start`建立连接并发送任务。

发送音频与消费事件需并发进行（配合`send_audio_frame`、`events()`/`results()`和`stop`使用）。

recognize\_file

```
def recognize_file(self,
                   path: str,
                   *,
                   model: str,
                   format: str = "pcm",
                   sample_rate: int = 16000,
                   ...) -> Iterator[Dict]
```

基于本地文件的非流式调用：自动分块发送音频并驱动到任务结束，逐个产出服务端事件。该方法要求所识别文件具有可读权限。

start

```
def start(self)
```

开始语音识别：建立连接、发送任务并等待`task-started`。进入`with`上下文时自动调用，启动成功后才能发送音频。

send\_audio\_frame

```
def send_audio_frame(self, buffer: bytes)
```

推送音频。每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。

识别结果通过[事件迭代（`events()`/`results()`）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#85d698b9f9g8s)获取。

stop

```
def stop(self)
```

停止语音识别：只通知服务端输入结束，接收线程需继续消费`events()`直到`task-finished`事件。

events / results

```
def events(self) -> Iterator[Dict]
def results(self) -> Iterator[RecognitionResult]
```

迭代服务端事件：`events()`产出原始事件`dict`（识别文本位于`payload.output.sentence`）；`results()`只产出识别结果帧，返回[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#bc3e1a43d6hhy)类型化对象（心跳帧已过滤）。

close

```
def close(self)
```

关闭识别会话。退出`with`上下文时自动调用。

request\_id / first\_package\_delay / last\_package\_delay / last\_response

```
rec.request_id
rec.first_package_delay
rec.last_package_delay
rec.last_response
```

获取request\_id、首包延迟（从发送第一包音频到收到首包识别结果延迟）和尾包延迟（发送`stop`指令到最后一包识别结果下发耗时），在任务完成后使用；`last_response`为最近一次成功读取的原始报文，可用于获取task-failed报错。会话关闭后仍可读取。

### 事件迭代（`events()`/`results()`）

[双向流式调用](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#9d1e5f6852jr8)时，服务端会通过事件的方式，将关键流程信息和数据返回给客户端。您需要在接收线程中迭代会话的`events()`（原始事件`dict`）或`results()`（类型化识别结果帧），处理服务端返回的信息或者数据。

```
# 迭代原始事件：识别文本位于 payload.output.sentence
def receive_events(rec):
    for event in rec.events():
        payload = event.get('payload') or {}
        sentence = (payload.get('output') or {}).get('sentence') or {}
        if sentence.get('text') and not sentence.get('heartbeat'):
            print('识别文本：', sentence['text'])

# 或只迭代识别结果帧（返回 RecognitionResult，心跳帧已过滤）
def receive_results(rec):
    for result in rec.results():
        sentence = result.get_sentence()
        if sentence and 'text' in sentence:
            print('识别文本：', sentence['text'])
```

**事件/迭代方法**

**产出内容**

**返回值**

**描述**

```
event["header"]["event"] == "task-started"
```

`task-started`事件

无

由`start()`内部读取，启动返回时保存在`last_response`中，不会由`events()`再次产出。

```
def events(self) -> Iterator[Dict]
```

`event`：服务端事件`dict`

迭代器

当服务有回复时产出事件。识别结果位于`payload.output.sentence`，可能为心跳或空文本事件，应用可按需忽略。请由一个接收线程持续消费，不要并发创建多个读取者。

```
def results(self) -> Iterator[RecognitionResult]
```

`result`：识别结果（`RecognitionResult`）

迭代器

只产出识别结果帧（心跳帧已过滤），全部识别结果返回后迭代结束。

```
try:
    ...
except DashScopeError as e:
    print(e.code, e.message, e.request_id)
```

`DashScopeError`异常

无

发生异常时在发送/接收线程中抛出，可使用try/except捕获。

```
event["header"]["event"] == "task-finished"
```

`task-finished`事件

无

当服务已经完成全部识别后由`events()`产出，随后迭代结束；发送`stop()`后仍须读取此事件。

## 响应结果

### 识别结果（`RecognitionResult`）

`RecognitionResult`代表会话`results()`迭代产出的一次识别结果帧（双向流式调用与非流式调用均可使用；`events()`产出的是原始事件`dict`，如需该类型化视图请改用`results()`）。

**成员方法**

**方法签名**

**说明**

`get_sentence`

```
def get_sentence(self) -> Union[Dict[str, Any], List[Any]]
```

获取当前识别的句子及时间戳信息，此方法返回类型为Dict\[str, Any\]（单句信息）。

详情请参见[单句信息（Sentence）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#f28f50b035qtn)。

`request_id`

```
result.request_id
```

当前事件对应的请求request\_id。

`is_sentence_end`

```
def is_sentence_end(self) -> bool
```

判断当前句子是否已经结束。该方法通过检查 `get_sentence()` 返回的单句信息中 `end_time` 字段是否为 `None` 来判定——`end_time` 不为 `None` 时表示句子已结束。

### 单句信息（`Sentence`）

Sentence类成员如下：

**参数**

**类型**

**说明**

`begin_time`

`int`

句子开始时间，单位为ms。

`end_time`

`int`

句子结束时间，单位为ms。

`text`

`str`

识别文本。

`words`

[字时间戳信息（Word）](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-python-sdk#b55a7391caxxe)的list集合

字时间戳信息。

### 字时间戳信息（`Word`）

Word类成员如下：

**参数**

**类型**

**说明**

`begin_time`

`int`

字开始时间，单位为ms。

`end_time`

`int`

字结束时间，单位为ms。

`text`

`str`

字。

`punctuation`

`str`

标点。

## 错误码

如遇报错问题，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，可加入[语音 SDK 示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo)中列出的开发者群反馈问题，并提供Request ID，以便进一步排查问题。

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
    
    参见非流式调用，调用`recognize_file`方法传入文件路径对录音文件直接进行识别。
    
-   将本地文件转成二进制流进行识别：此种方式一边识别文件一边流式获取识别结果，适合即时反馈的场景。
    
    参见双向流式调用，通过识别会话的`send_audio_frame`方法向服务端发送二进制流对其进行识别。
    

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
