# Paraformer Python SDK

通过 WebSocket 使用 DashScope Python SDK 调用 Paraformer。

<a id="model-paraformer"></a>

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

**用户指南：**关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

<a id="前提条件"></a>

<a id="model-paraformer-8a24f2ed09vr0"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)。
>
> 与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
>
> 使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="模型列表"></a>

<a id="model-paraformer-1e173d999c1th"></a>

### 模型列表

<table><thead><tr><th></th><th><strong>paraformer-realtime-v2（推荐）</strong></th><th><strong>paraformer-realtime-8k-v2（推荐）</strong></th></tr></thead><tbody><tr><td><strong>适用场景</strong></td><td><p>直播、会议等场景</p></td><td><p>电话客服、语音信箱等 8kHz 音频的识别场景</p></td></tr><tr><td><strong>采样率</strong></td><td><p>任意</p></td><td><p>8kHz</p></td></tr><tr><td><strong>语种</strong></td><td><p>中文（包含中文普通话和各种方言）、英文、日语、韩语、德语、法语、俄语</p><p>支持的中文方言：上海话、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、江西话、宁夏话、山西话、陕西话、山东话、四川话、天津话、云南话、粤语</p></td><td><p>中文</p></td></tr><tr><td><strong>标点符号预测</strong></td><td><p>默认支持，无需配置</p></td><td><p>默认支持，无需配置</p></td></tr><tr><td><strong>逆文本正则化（ITN）</strong></td><td><p>默认支持，无需配置</p></td><td><p>默认支持，无需配置</p></td></tr><tr><td><strong>定制热词</strong></td><td><p>参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a></p></td><td><p>参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a></p></td></tr><tr><td><strong>指定待识别语种</strong></td><td><p>通过<code>language_hints</code>参数指定</p></td><td><p>不支持</p></td></tr><tr><td><strong>情感识别</strong></td><td><p>不支持</p></td><td><a id="accordion-点击查看使用方式"></a><section><p>点击查看使用方式</p><div><p>情感识别遵循如下约束：</p><ul><li>仅限<code>paraformer-realtime-8k-v2</code>模型。</li><li>必须关闭语义断句（可通过<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-555007db2033f">请求参数</a><code>semantic_punctuation_enabled</code>控制）。语义断句默认为关闭状态。</li><li>只有在<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-bc3e1a43d6hhy">识别结果（RecognitionResult）</a>的<code>is_sentence_end</code>方法返回结果为<code>True</code>时才显示情感识别结果。</li></ul><p>情感识别结果获取方式：通过<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-f28f50b035qtn">单句信息（Sentence）</a>的<code>emo_tag</code>和<code>emo_confidence</code>字段分别获取当前句子的情感和情感置信度。</p></div></section></td></tr></tbody></table>

<a id="快速开始"></a>

<a id="model-paraformer-e056c0babdrkw"></a>

## 快速开始

[核心资源（`client.audio.asr`）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-d6bc1f133f871)提供了非流式调用和双向流式调用接口。请根据实际需求选择合适的调用方式：

-   非流式调用（`recognize_file`）：针对本地文件进行识别，SDK自动分块发送音频并驱动到任务结束。适合处理录制好的音频。
-   双向流式调用（`recognize`会话）：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

<a id="非流式调用"></a>

<a id="model-paraformer-8341058094tc3"></a>

### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8535166871/CAEQURiBgMDS0c2RpxkiIDNmYjBlMTE3ODQxYTQ3Nzk4MGMxNTc5MjY3OWVjZjlj4709861_20241015153444.149.svg)

调用[核心资源（`client.audio.asr`）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-d6bc1f133f871)的`recognize_file`方法绑定[请求参数](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-555007db2033f)并传入本地文件路径，迭代服务端事件获取[识别结果（RecognitionResult）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-bc3e1a43d6hhy)。

<a id="accordion-点击查看完整示例"></a>

点击查看完整示例

<a id="code-block"></a>

```python
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

`recognize_file`逐个产出**服务端事件**（`Dict[str, Any]`）：事件类型位于`event['header']['event']`，识别文本位于`event['payload']['output']['sentence']`（`sentence_end`为`true`表示该句已结束，`begin_time` / `end_time`为时间戳、`words`为字时间戳等字段见[单句信息（Sentence）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-f28f50b035qtn)）。心跳与空文本事件仍会产出，可按需忽略。

双向流式会话中除`events()`外，还可通过`results()`只迭代识别结果帧（返回类型化的[识别结果（RecognitionResult）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-bc3e1a43d6hhy)，心跳帧已过滤），详见`get_sentence`方法说明。

<a id="双向流式调用"></a>

<a id="model-paraformer-9d1e5f6852jr8"></a>

### 双向流式调用

提交单个语音实时转写任务，通过迭代事件的方式流式输出实时识别结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8535166871/CAEQURiBgIDvi..2pxkiIGE4NTc3Njg4ZGM2YzQ2NzVhZGI3MzE2YWUwYTA3OGEy4709861_20241015153444.149.svg)

1.  启动流式语音识别
    
    调用[核心资源（`client.audio.asr`）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-d6bc1f133f871)的`recognize`方法创建识别会话并绑定[请求参数](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-555007db2033f)，进入`with`上下文（自动调用`start`方法建立连接并发送任务）启动流式语音识别。
    
2.  流式传输
    
    循环调用会话的`send_audio_frame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。发送与接收需并发进行：接收线程通过[事件迭代（`events()`/`results()`）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-85d698b9f9g8s)迭代服务端事件，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用会话的`stop`方法结束语音识别。
    
    该方法只通知服务端输入结束；接收线程需继续消费`events()`直到`task-finished`事件以获得最后的识别结果和统计信息。ws层的错误会以`DashScopeError`异常抛出，可在发送/接收处使用try/except捕获。
    

<a id="accordion-点击查看完整示例-2"></a>

点击查看完整示例

<a id="fig-code-group"></a>

<a id="fig-code-group-识别传入麦克风的语音-tab"></a>

识别传入麦克风的语音

<a id="code-code-group-识别传入麦克风的语音"></a>

```python
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

<a id="fig-code-group-识别本地语音文件-tab"></a>

识别本地语音文件

<a id="code-code-group-识别本地语音文件"></a>

```python
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

<a id="并发调用"></a>

<a id="model-paraformer-ea8503736dlf7"></a>

### 并发调用

在Python中，由于存在[全局解释器锁](https://docs.python.org/zh-cn/3/glossary.html#term-global-interpreter-lock)，同一时刻只有一个线程可以执行Python代码（虽然某些性能导向的库可能会去除此限制）。如果您想更好地利用多核心计算机的计算资源，推荐您使用[multiprocessing](https://docs.python.org/zh-cn/3.11/library/multiprocessing.html#module-multiprocessing)或[concurrent.futures.ProcessPoolExecutor](https://docs.python.org/zh-cn/3.11/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor)。 多线程在较高并发下会显著增加SDK调用延迟。

<a id="请求参数"></a>

<a id="model-paraformer-555007db2033f"></a>

## 请求参数

请求参数通过[核心资源（`client.audio.asr`）](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-d6bc1f133f871)的`recognize`/`recognize_file`方法进行设置：`model`、`format`、`sample_rate`、`vocabulary_id`、`disfluency_removal_enabled`为具名参数，其余参数（如`language_hints`、`semantic_punctuation_enabled`）通过`parameters`字典传入。

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>默认值</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>str</p></td><td><p>-</p></td><td><p>是</p></td><td><p>用于实时语音识别的模型（参见<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-1e173d999c1th">模型列表</a>）。</p></td></tr><tr><td><p>sample_rate</p></td><td><p>int</p></td><td><p>-</p></td><td><p>是</p></td><td><div><p>设置待识别音频采样率（单位Hz）。</p><p>因模型而异：</p><ul><li><p>paraformer-realtime-v2支持任意采样率。</p></li><li><p>paraformer-realtime-8k-v2仅支持8000Hz采样率。</p></li></ul></div></td></tr><tr><td><p>format</p></td><td><p>str</p></td><td><p>-</p></td><td><p>是</p></td><td><div><p>设置待识别音频格式。</p><div><p>支持的音频格式：pcm、wav、mp3、opus、speex、aac、amr。</p><div><p>opus/speex：必须使用Ogg封装；</p><p>wav：必须为PCM编码；</p><p>amr：仅支持AMR-NB类型。</p></div></div></div></td></tr><tr><td><p>vocabulary_id</p></td><td><p>str</p></td><td><p>-</p></td><td><p>否</p></td><td><div><p>设置热词ID，若未设置则不生效。v2及更高版本模型设置热词ID时使用该字段。</p><p>在本次语音识别中，将应用与该热词ID对应的热词信息。具体使用方法请参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a>。</p></div></td></tr><tr><td><p>disfluency_removal_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><div><p>设置是否过滤语气词：</p><ul><li><p>true：过滤语气词</p></li><li><p>false（默认）：不过滤语气词</p></li></ul></div></td></tr><tr><td><p>language_hints</p></td><td><p>list[str]</p></td><td><p>[&quot;zh&quot;, &quot;en&quot;]</p></td><td><p>否</p></td><td><div><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。</p><p>目前支持的语言代码：</p><ul><li><p>zh: 中文</p></li><li><p>en: 英文</p></li><li><p>ja: 日语</p></li><li><p>yue: 粤语</p></li><li><p>ko: 韩语</p></li><li><p>de：德语</p></li><li><p>fr：法语</p></li><li><p>ru：俄语</p></li></ul></div><p>该参数仅对支持多语言的模型生效（参见<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-1e173d999c1th">模型列表</a>）。</p></td></tr><tr><td><p>semantic_punctuation_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><div><p>设置是否开启语义断句，默认关闭。</p><ul><li><p>true：开启语义断句，关闭VAD（Voice Activity Detection，语音活动检测）断句。</p></li><li><p>false（默认）：开启VAD（Voice Activity Detection，语音活动检测）断句，关闭语义断句。</p></li></ul><p>语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。</p><p>通过调整<code>semantic_punctuation_enabled</code>参数，可以灵活切换语音识别的断句方式以适应不同场景需求。</p><p>该参数仅在模型为v2及更高版本时生效。</p></div></td></tr><tr><td><p>max_sentence_silence</p></td><td><p>int</p></td><td><p>800</p></td><td><p>否</p></td><td><div><p>设置VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。</p><p>当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。</p><p>参数范围为200ms至6000ms，默认值为800ms。</p><p>该参数仅在<code>semantic_punctuation_enabled</code>参数为false（VAD断句）且模型为v2及更高版本时生效。</p></div></td></tr><tr><td><p>multi_threshold_mode_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><div><p>该开关打开时（true）可以防止VAD断句切割过长。默认关闭。</p><p>该参数仅在<code>semantic_punctuation_enabled</code>参数为false（VAD断句）且模型为v2及更高版本时生效。</p></div></td></tr><tr><td><p>punctuation_prediction_enabled</p></td><td><p>bool</p></td><td><p>True</p></td><td><p>否</p></td><td><div><p>设置是否在识别结果中自动添加标点：</p><ul><li><p>true（默认）：是</p></li><li><p>false：否</p></li></ul><p>该参数仅在模型为v2及更高版本时生效。</p></div></td></tr><tr><td><p>heartbeat</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><div><p>当需要与服务端保持长连接时，可通过该开关进行控制：</p><ul><li><p>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</p></li><li><p>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</p><div><p>静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。</p></div></li></ul><p>该参数仅在模型为v2及更高版本时生效。</p></div><p>该字段自 SDK 1.23.1 引入，2.0.1 及以上版本已包含。</p></td></tr><tr><td><p>inverse_text_normalization_enabled</p></td><td><p>bool</p></td><td><p>True</p></td><td><p>否</p></td><td><div><p>设置是否开启ITN（Inverse Text Normalization，逆文本正则化）。</p><p>默认开启（true）。开启后，中文数字将转换为阿拉伯数字。</p><p>该参数仅在模型为v2及更高版本时生效。</p></div></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="model-paraformer-cc1002f2d5met"></a>

<a id="关键接口"></a>

## 接口参考

<a id="核心资源-client-audio-asr"></a>

<a id="model-paraformer-d6bc1f133f871"></a>

### 核心资源（`client.audio.asr`）

实时语音识别能力挂载在`client.audio.asr`资源上：`recognize`创建双向流式识别会话（`Recognition`），`recognize_file`对本地文件一次性识别。

<table><thead><tr><th><strong>成员方法</strong></th><th><strong>方法签名</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>recognize</p></td><td><a id="code-block-2"></a><pre class="language-python"><code>def recognize(self,
              *,
              model: str,
              format: str = &quot;pcm&quot;,
              sample_rate: int = 16000,
              vocabulary_id: str = None,
              disfluency_removal_enabled: bool = None,
              diarization_enabled: bool = None,
              parameters: Dict = None,
              input: Dict = None,
              phrase_id: str = None,
              ...) -&gt; Recognition
</code></pre></td><td><p>创建双向流式识别会话，进入<code>with</code>上下文时自动调用<code>start</code>建立连接并发送任务。</p><p>发送音频与消费事件需并发进行（配合<code>send_audio_frame</code>、<code>events()</code>/<code>results()</code>和<code>stop</code>使用）。</p></td></tr><tr><td><p>recognize_file</p></td><td><a id="code-block-3"></a><pre class="language-python"><code>def recognize_file(self,
                   path: str,
                   *,
                   model: str,
                   format: str = &quot;pcm&quot;,
                   sample_rate: int = 16000,
                   ...) -&gt; Iterator[Dict]
</code></pre></td><td><p>基于本地文件的非流式调用：自动分块发送音频并驱动到任务结束，逐个产出服务端事件。该方法要求所识别文件具有可读权限。</p></td></tr><tr><td><p>start</p></td><td><a id="code-block-4"></a><pre class="language-python"><code>def start(self)
</code></pre></td><td><p>开始语音识别：建立连接、发送任务并等待<code>task-started</code>。进入<code>with</code>上下文时自动调用，启动成功后才能发送音频。</p></td></tr><tr><td><p>send_audio_frame</p></td><td><a id="code-block-5"></a><pre class="language-python"><code>def send_audio_frame(self, buffer: bytes)
</code></pre></td><td><p>推送音频。每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。</p><p>识别结果通过<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-85d698b9f9g8s">事件迭代（<code>events()</code>/<code>results()</code>）</a>获取。</p></td></tr><tr><td><p>stop</p></td><td><a id="code-block-6"></a><pre class="language-python"><code>def stop(self)
</code></pre></td><td><p>停止语音识别：只通知服务端输入结束，接收线程需继续消费<code>events()</code>直到<code>task-finished</code>事件。</p></td></tr><tr><td><p>events / results</p></td><td><a id="code-block-7"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
def results(self) -&gt; Iterator[RecognitionResult]
</code></pre></td><td><p>迭代服务端事件：<code>events()</code>产出原始事件<code>dict</code>（识别文本位于<code>payload.output.sentence</code>）；<code>results()</code>只产出识别结果帧，返回<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-bc3e1a43d6hhy">识别结果（RecognitionResult）</a>类型化对象（心跳帧已过滤）。</p></td></tr><tr><td><p>close</p></td><td><a id="code-block-8"></a><pre class="language-python"><code>def close(self)
</code></pre></td><td><p>关闭识别会话。退出<code>with</code>上下文时自动调用。</p></td></tr><tr><td><p>request_id / first_package_delay / last_package_delay</p></td><td><a id="code-block-9"></a><pre class="language-python"><code>rec.request_id
rec.first_package_delay
rec.last_package_delay
</code></pre></td><td><p>获取request_id、首包延迟（从发送第一包音频到收到首包识别结果延迟）和尾包延迟（发送<code>stop</code>指令到最后一包识别结果下发耗时）。在任务完成后使用，会话关闭后仍可读取。</p></td></tr></tbody></table>

<a id="事件迭代-events-results"></a>

<a id="model-paraformer-85d698b9f9g8s"></a>

### 事件迭代（`events()`/`results()`）

[双向流式调用](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-9d1e5f6852jr8)时，服务端会通过事件的方式，将关键流程信息和数据返回给客户端。您需要在接收线程中迭代会话的`events()`（原始事件`dict`）或`results()`（类型化识别结果帧），处理服务端返回的信息或者数据。

<a id="accordion-点击查看示例"></a>

点击查看示例

<a id="code-block-10"></a>

```python
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

<table><thead><tr><th><strong>事件/迭代方法</strong></th><th><strong>产出内容</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-11"></a><pre class="language-python"><code>event[&quot;header&quot;][&quot;event&quot;] == &quot;task-started&quot;
</code></pre></td><td><p><code>task-started</code>事件</p></td><td><p>无</p></td><td><p>由<code>start()</code>内部读取，启动返回时保存在<code>last_response</code>中，不会由<code>events()</code>再次产出。</p></td></tr><tr><td><a id="code-block-12"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
</code></pre></td><td><p><code>event</code>：服务端事件<code>dict</code></p></td><td><p>迭代器</p></td><td><p>当服务有回复时产出事件。识别结果位于<code>payload.output.sentence</code>，可能为心跳或空文本事件，应用可按需忽略。请由一个接收线程持续消费，不要并发创建多个读取者。</p></td></tr><tr><td><a id="code-block-13"></a><pre class="language-python"><code>def results(self) -&gt; Iterator[RecognitionResult]
</code></pre></td><td><p><code>result</code>：<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-bc3e1a43d6hhy">识别结果（RecognitionResult）</a></p></td><td><p>迭代器</p></td><td><p>只产出识别结果帧（心跳帧已过滤），全部识别结果返回后迭代结束。</p></td></tr><tr><td><a id="code-block-14"></a><pre class="language-python"><code>try:
    ...
except DashScopeError as e:
    print(e.code, e.message, e.request_id)
</code></pre></td><td><p><code>DashScopeError</code>异常</p></td><td><p>无</p></td><td><p>发生异常时在发送/接收线程中抛出，可使用try/except捕获。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-python"><code>event[&quot;header&quot;][&quot;event&quot;] == &quot;task-finished&quot;
</code></pre></td><td><p><code>task-finished</code>事件</p></td><td><p>无</p></td><td><p>当服务已经完成全部识别后由<code>events()</code>产出，随后迭代结束；发送<code>stop()</code>后仍须读取此事件。</p></td></tr></tbody></table>

<a id="响应结果"></a>

<a id="model-paraformer-843fb17087zct"></a>

### 响应结果

<a id="识别结果-recognitionresult"></a>

<a id="model-paraformer-bc3e1a43d6hhy"></a>

#### 识别结果（`RecognitionResult`）

`RecognitionResult`代表会话`results()`迭代产出的一次识别结果帧（[双向流式调用](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-9d1e5f6852jr8)与[非流式调用](realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-8341058094tc3)均可使用；`events()`产出的是原始事件`dict`，如需该类型化视图请改用`results()`）。

<table><thead><tr><th><strong>成员方法</strong></th><th><strong>方法签名</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>get_sentence</p></td><td><a id="code-block-16"></a><pre class="language-python"><code>def get_sentence(self) -&gt; Union[Dict[str, Any], List[Any]]
</code></pre></td><td><p>获取当前识别的句子及时间戳信息，此方法返回类型为Dict[str, Any]（单句信息）。</p><p>详情请参见<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-f28f50b035qtn">单句信息（Sentence）</a>。</p></td></tr><tr><td><p>request_id</p></td><td><a id="code-block-17"></a><pre class="language-python"><code>result.request_id
</code></pre></td><td><p>当前事件对应的请求request_id。</p></td></tr><tr><td><p>is_sentence_end</p></td><td><a id="code-block-18"></a><pre class="language-python"><code>def is_sentence_end(self) -&gt; bool
</code></pre></td><td><p>判断当前句子是否已经结束（句子携带<code>end_time</code>时为<code>True</code>）。</p></td></tr></tbody></table>

<a id="单句信息-sentence"></a>

<a id="model-paraformer-f28f50b035qtn"></a>

#### 单句信息（`Sentence`）

Sentence类成员如下：

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>begin_time</p></td><td><p>int</p></td><td><p>句子开始时间，单位为ms。</p></td></tr><tr><td><p>end_time</p></td><td><p>int</p></td><td><p>句子结束时间，单位为ms。</p></td></tr><tr><td><p>text</p></td><td><p>str</p></td><td><p>识别文本。</p></td></tr><tr><td><p>words</p></td><td><p><a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-b55a7391caxxe">字时间戳信息（Word）</a>的list集合</p></td><td><p>字时间戳信息。</p></td></tr><tr><td><p>emo_tag</p></td><td><p>str</p></td><td><p>当前句子的情感：</p><ul><li><p>positive：正面情感，如开心、满意</p></li><li><p>negative：负面情感，如愤怒、沉闷</p></li><li><p>neutral：无明显情感</p></li></ul><div><p>情感识别遵循如下约束：</p><ul><li><p>仅限<code>paraformer-realtime-8k-v2</code>模型。</p></li><li><p>必须关闭语义断句（可通过<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-555007db2033f">请求参数</a><code>semantic_punctuation_enabled</code>控制）。语义断句默认为关闭状态。</p></li><li><p>只有在<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-bc3e1a43d6hhy">识别结果（RecognitionResult）</a>的<code>is_sentence_end</code>方法返回结果为<code>True</code>时才显示情感识别结果。</p></li></ul></div></td></tr><tr><td><p>emo_confidence</p></td><td><p>float</p></td><td><p>当前句子识别情感的置信度，取值范围：[0.0,1.0]。值越大表示置信度越高。</p><div><p>情感识别遵循如下约束：</p><ul><li><p>仅限<code>paraformer-realtime-8k-v2</code>模型。</p></li><li><p>必须关闭语义断句（可通过<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-555007db2033f">请求参数</a><code>semantic_punctuation_enabled</code>控制）。语义断句默认为关闭状态。</p></li><li><p>只有在<a href="realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md#model-paraformer-bc3e1a43d6hhy">识别结果（RecognitionResult）</a>的<code>is_sentence_end</code>方法返回结果为<code>True</code>时才显示情感识别结果。</p></li></ul></div></td></tr></tbody></table>

<a id="字时间戳信息-word"></a>

<a id="model-paraformer-b55a7391caxxe"></a>

#### 字时间戳信息（`Word`）

Word类成员如下：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| begin\_time | int | 字开始时间，单位为ms。 |
| end\_time | int | 字结束时间，单位为ms。 |
| text | str | 字。 |
| punctuation | str | 标点。 |

<a id="更多示例"></a>

<a id="model-paraformer-a197604bf2kyv"></a>

## 更多示例

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

<a id="错误码"></a>

<a id="model-paraformer-605d5ca873bnd"></a>

## 错误码

如遇报错问题，请参见[错误码](../model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。
