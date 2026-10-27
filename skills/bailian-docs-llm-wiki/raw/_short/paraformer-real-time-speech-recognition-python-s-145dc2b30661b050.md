# Paraformer实时语音识别Python SDK

本文介绍Paraformer实时语音识别Python SDK的参数和接口细节。

**重要**阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

**用户指南：**关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 模型列表

**paraformer-realtime-v2（推荐）**

**paraformer-realtime-8k-v2（推荐）**

**适用场景**

直播、会议等场景

电话客服、语音信箱等 8kHz 音频的识别场景

**采样率**

任意

8kHz

**语种**

中文（包含中文普通话和各种方言）、英文、日语、韩语、德语、法语、俄语

支持的中文方言：上海话、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、江西话、宁夏话、山西话、陕西话、山东话、四川话、天津话、云南话、粤语

中文

**标点符号预测**

默认支持，无需配置

默认支持，无需配置

**逆文本正则化（ITN）**

默认支持，无需配置

默认支持，无需配置

**定制热词**

参见[定制热词](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words.md)

参见[定制热词](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words.md)

**指定待识别语种**

通过`language_hints`参数指定

不支持

**情感识别**

不支持

点击查看使用方式

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
-   必须关闭语义断句（可通过[请求参数](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#555007db2033f)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
-   只有在[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)的`is_sentence_end`方法返回结果为`True`时才显示情感识别结果。

情感识别结果获取方式：通过[单句信息（Sentence）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#f28f50b035qtn)的`emo_tag`和`emo_confidence`字段分别获取当前句子的情感和情感置信度。

## 快速开始

[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#d6bc1f133f871)提供了非流式调用和双向流式调用接口。请根据实际需求选择合适的调用方式：

-   非流式调用（`recognize_file`）：针对本地文件进行识别，SDK自动分块发送音频并驱动到任务结束。适合处理录制好的音频。
-   双向流式调用（`recognize`会话）：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8535166871/CAEQURiBgMDS0c2RpxkiIDNmYjBlMTE3ODQxYTQ3Nzk4MGMxNTc5MjY3OWVjZjlj4709861_20241015153444.149.svg)

调用[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#d6bc1f133f871)的`recognize_file`方法绑定[请求参数](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#555007db2033f)并传入本地文件路径，迭代服务端事件获取[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)。

点击查看完整示例

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 识别本地语音文件：recognize_file自动分块发送音频并驱动到任务结束
for event in client.audio.asr.recognize_file(
        '{YOUR_AUDIO_FILE}',
        model='paraformer-realtime-v2',
        format='wav',
        sample_rate=16000,
        # “language_hints”只支持paraformer-realtime-v2模型
        parameters={'language_hints': ['zh', 'en']}):
    payload = event.get('payload') or {}
    sentence = (payload.get('output') or {}).get('sentence') or {}
    if sentence.get('text') and not sentence.get('heartbeat'):
        print('识别结果：', sentence['text'])
```

`recognize_file`逐个产出**服务端事件**（`Dict[str, Any]`）：事件类型位于`event['header']['event']`，识别文本位于`event['payload']['output']['sentence']`（`sentence_end`为`true`表示该句已结束，`begin_time` / `end_time`为时间戳、`words`为字时间戳等字段见[单句信息（Sentence）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#f28f50b035qtn)）。心跳与空文本事件仍会产出，可按需忽略。

双向流式会话中除`events()`外，还可通过`results()`只迭代识别结果帧（返回类型化的[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)，心跳帧已过滤），详见`get_sentence`方法说明。

### 双向流式调用

提交单个语音实时转写任务，通过迭代事件的方式流式输出实时识别结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8535166871/CAEQURiBgIDvi..2pxkiIGE4NTc3Njg4ZGM2YzQ2NzVhZGI3MzE2YWUwYTA3OGEy4709861_20241015153444.149.svg)

1.  启动流式语音识别
    
    调用[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#d6bc1f133f871)的`recognize`方法创建识别会话并绑定[请求参数](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#555007db2033f)，进入`with`上下文（自动调用`start`方法建立连接并发送任务）启动流式语音识别。
    
2.  流式传输
    
    循环调用会话的`send_audio_frame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。发送与接收需并发进行：接收线程通过[事件迭代（`events()`/`results()`）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#85d698b9f9g8s)迭代服务端事件，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用会话的`stop`方法结束语音识别。
    
    该方法只通知服务端输入结束；接收线程需继续消费`events()`直到`task-finished`事件以获得最后的识别结果和统计信息。ws层的错误会以`DashScopeError`异常抛出，可在发送/接收处使用try/except捕获。
    

点击查看完整示例

识别传入麦克风的语音

```
import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
import sys

import dashscope
import pyaudio
from concurrent.futures import ThreadPoolExecutor

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

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
    print('Initializing ...')

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")

    # Call recognition service, you can customize the recognition parameters, like model, format,
    # sample_rate
    with client.audio.asr.recognize(
            model='paraformer-realtime-v2',
            format=format_pcm,
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=sample_rate,
            # support 8000, 16000
            parameters={'semantic_punctuation_enabled': False},
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

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
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
        model='paraformer-realtime-v2',
        format='wav',
        sample_rate=16000,
        # “language_hints”只支持paraformer-realtime-v2模型
        parameters={'language_hints': ['zh', 'en']},
) as recognition:
    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_events, recognition)
        try:
            audio_data: bytes = None
            f = open("{YOUR_AUDIO_FILE}", 'rb')
            if os.path.getsize("{YOUR_AUDIO_FILE}"):
                while True:
                    audio_data = f.read(3200)
                    if not audio_data:
                        break
                    else:
                        recognition.send_audio_frame(audio_data)
                    time.sleep(0.1)
            else:
                raise Exception(
                    'The supplied file was empty (zero bytes long)')
            f.close()
            recognition.stop()
            receiver.result()
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

### 并发调用

在Python中，由于存在[全局解释器锁](https://docs.python.org/zh-cn/3/glossary.html#term-global-interpreter-lock)，同一时刻只有一个线程可以执行Python代码（虽然某些性能导向的库可能会去除此限制）。如果您想更好地利用多核心计算机的计算资源，推荐您使用[multiprocessing](https://docs.python.org/zh-cn/3.11/library/multiprocessing.html#module-multiprocessing)或[concurrent.futures.ProcessPoolExecutor](https://docs.python.org/zh-cn/3.11/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor)。 多线程在较高并发下会显著增加SDK调用延迟。

## 请求参数

请求参数通过[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#d6bc1f133f871)的`recognize`/`recognize_file`方法进行设置：`model`、`format`、`sample_rate`、`vocabulary_id`、`disfluency_removal_enabled`为具名参数，其余参数（如`language_hints`、`semantic_punctuation_enabled`）通过`parameters`字典传入。

**参数**

**类型**

**默认值**

**是否必须**

**说明**

model

str

\-

是

用于实时语音识别的模型（参见[模型列表](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#1e173d999c1th)）。

sample\_rate

int

\-

是

设置待识别音频采样率（单位Hz）。

因模型而异：

-   paraformer-realtime-v2支持任意采样率。
    
-   paraformer-realtime-8k-v2仅支持8000Hz采样率。
    

format

str

\-

是

设置待识别音频格式。

支持的音频格式：pcm、wav、mp3、opus、speex、aac、amr。

opus/speex：必须使用Ogg封装；

wav：必须为PCM编码；

amr：仅支持AMR-NB类型。

vocabulary\_id

str

\-

否

设置热词ID，若未设置则不生效。v2及更高版本模型设置热词ID时使用该字段。

在本次语音识别中，将应用与该热词ID对应的热词信息。具体使用方法请参见[定制热词](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words.md)。

disfluency\_removal\_enabled

bool

False

否

设置是否过滤语气词：

-   true：过滤语气词
    
-   false（默认）：不过滤语气词
    

language\_hints

list\[str\]

\["zh", "en"\]

否

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。

目前支持的语言代码：

-   zh: 中文
    
-   en: 英文
    
-   ja: 日语
    
-   yue: 粤语
    
-   ko: 韩语
    
-   de：德语
    
-   fr：法语
    
-   ru：俄语
    

该参数仅对支持多语言的模型生效（参见[模型列表](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#1e173d999c1th)）。

semantic\_punctuation\_enabled

bool

False

否

设置是否开启语义断句，默认关闭。

-   true：开启语义断句，关闭VAD（Voice Activity Detection，语音活动检测）断句。
    
-   false（默认）：开启VAD（Voice Activity Detection，语音活动检测）断句，关闭语义断句。
    

语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。

通过调整`semantic_punctuation_enabled`参数，可以灵活切换语音识别的断句方式以适应不同场景需求。

该参数仅在模型为v2及更高版本时生效。

max\_sentence\_silence

int

800

否

设置VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。

当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。

参数范围为200ms至6000ms，默认值为800ms。

该参数仅在`semantic_punctuation_enabled`参数为false（VAD断句）且模型为v2及更高版本时生效。

multi\_threshold\_mode\_enabled

bool

False

否

该开关打开时（true）可以防止VAD断句切割过长。默认关闭。

该参数仅在`semantic_punctuation_enabled`参数为false（VAD断句）且模型为v2及更高版本时生效。

punctuation\_prediction\_enabled

bool

True

否

设置是否在识别结果中自动添加标点：

-   true（默认）：是
    
-   false：否
    

该参数仅在模型为v2及更高版本时生效。

heartbeat

bool

False

否

当需要与服务端保持长连接时，可通过该开关进行控制：

-   true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
    
-   false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。
    
    静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。
    

该参数仅在模型为v2及更高版本时生效。

该字段自 SDK 1.23.1 引入，2.0.1 及以上版本已包含。

inverse\_text\_normalization\_enabled

bool

True

否

设置是否开启ITN（Inverse Text Normalization，逆文本正则化）。

默认开启（true）。开启后，中文数字将转换为阿拉伯数字。

该参数仅在模型为v2及更高版本时生效。

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

识别结果通过[事件迭代（`events()`/`results()`）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#85d698b9f9g8s)获取。

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

迭代服务端事件：`events()`产出原始事件`dict`（识别文本位于`payload.output.sentence`）；`results()`只产出识别结果帧，返回[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)类型化对象（心跳帧已过滤）。

close

```
def close(self)
```

关闭识别会话。退出`with`上下文时自动调用。

request\_id / first\_package\_delay / last\_package\_delay

```
rec.request_id
rec.first_package_delay
rec.last_package_delay
```

获取request\_id、首包延迟（从发送第一包音频到收到首包识别结果延迟）和尾包延迟（发送`stop`指令到最后一包识别结果下发耗时）。在任务完成后使用，会话关闭后仍可读取。

### 事件迭代（`events()`/`results()`）

[双向流式调用](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#9d1e5f6852jr8)时，服务端会通过事件的方式，将关键流程信息和数据返回给客户端。您需要在接收线程中迭代会话的`events()`（原始事件`dict`）或`results()`（类型化识别结果帧），处理服务端返回的信息或者数据。

点击查看示例

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

`result`：[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)

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

`RecognitionResult`代表会话`results()`迭代产出的一次识别结果帧（[双向流式调用](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#9d1e5f6852jr8)与[非流式调用](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#8341058094tc3)均可使用；`events()`产出的是原始事件`dict`，如需该类型化视图请改用`results()`）。

**成员方法**

**方法签名**

**说明**

get\_sentence

```
def get_sentence(self) -> Union[Dict[str, Any], List[Any]]
```

获取当前识别的句子及时间戳信息，此方法返回类型为Dict\[str, Any\]（单句信息）。

详情请参见[单句信息（Sentence）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#f28f50b035qtn)。

request\_id

```
result.request_id
```

当前事件对应的请求request\_id。

is\_sentence\_end

```
def is_sentence_end(self) -> bool
```

判断当前句子是否已经结束（句子携带`end_time`时为`True`）。

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

[字时间戳信息（Word）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#b55a7391caxxe)的list集合

字时间戳信息。

emo\_tag

str

当前句子的情感：

-   positive：正面情感，如开心、满意
    
-   negative：负面情感，如愤怒、沉闷
    
-   neutral：无明显情感
    

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#555007db2033f)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)的`is_sentence_end`方法返回结果为`True`时才显示情感识别结果。
    

emo\_confidence

float

当前句子识别情感的置信度，取值范围：\[0.0,1.0\]。值越大表示置信度越高。

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#555007db2033f)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[识别结果（RecognitionResult）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#bc3e1a43d6hhy)的`is_sentence_end`方法返回结果为`True`时才显示情感识别结果。
    

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

## 更多示例

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

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

##### Q：是否支持查看每句话对应的时间范围？

支持。语音识别结果中会包含每句话的开始时间戳和结束时间戳，可通过它们确定每句话的时间范围。

#### Q：如何识别本地文件（录音文件）？

识别本地文件有两种方式：

-   直接传入本地文件路径：此种方式在最终识别结束后获取完整识别结果，不适合即时反馈的场景。
    
    参见[非流式调用](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#8341058094tc3)，调用[核心资源（`client.audio.asr`）](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#d6bc1f133f871)的`recognize_file`方法传入文件路径对录音文件直接进行识别。
    
-   将本地文件转成二进制流进行识别：此种方式一边识别文件一边流式获取识别结果，适合即时反馈的场景。
    
    参见[双向流式调用](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk#9d1e5f6852jr8)，通过识别会话的`send_audio_frame`方法向服务端发送二进制流对其进行识别。
    

### 故障排查

#### Q：无法识别语音（无识别结果）是什么原因？

1.  请检查请求参数中的音频格式（`format`）和采样率（`sampleRate`/`sample_rate`）设置是否正确且符合参数约束。以下为常见错误示例：
    
    -   音频文件扩展名为 .wav，但实际为 MP3 格式，而请求参数 `format` 设置为 `wav`（参数设置错误）。
    -   音频采样率为 3600Hz，但请求参数 `sampleRate`/`sample_rate` 设置为 48000（参数设置错误）。
    
    可以使用[ffprobe](https://ffmpeg.org/ffprobe.html)工具获取音频的容器、编码、采样率、声道等信息：
    

```
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
```

2.  使用`paraformer-realtime-v2`模型时，请检查`language_hints`设置的语言是否与音频实际语言一致。
    
    例如：音频实际为中文，但`language_hints`设置为`en`（英文）。
    
3.  若以上检查均无问题，可通过定制热词提升对特定词语的识别效果。
    

#### Q：音频格式参数设置错误导致无识别结果，如何处理？

`format`为必填参数，必须与音频的**实际格式**匹配。例如，对于实际格式为 MP3、扩展名为`.wav`的音频文件，应设置`format='mp3'`。

1.  **检查音频实际格式**：使用`ffprobe`工具查看音频的容器、编码、采样率和声道信息。
    
    ```
    ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 your_audio_file
    ```
    
2.  **设置请求参数**：将`format`设置为音频的实际格式，并确保`sample_rate`与音频的实际采样率一致，且符合所用模型的参数要求。
    
3.  **按需转换音频格式**：如需将音频转换为 WAV，可使用以下命令生成 PCM 编码、16 kHz、单声道的 WAV 文件。
    
    ```
    ffmpeg -i input_file -c:a pcm_s16le -ar 16000 -ac 1 output.wav
    ```
    
    转换后，设置`format='wav'`和`sample_rate=16000`。
    

**重要**使用`format='wav'`时，音频必须为 PCM 编码的 WAV 文件。
