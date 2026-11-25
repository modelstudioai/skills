# Qwen-Audio-ASR-Streaming Python SDK

其他模型 — [Qwen-Audio-ASR-Message Python SDK](qwen-asr-message-websocket-sdk-python-06f03701cdddda13.md) · [Fun-ASR-Realtime Python SDK](fun-asr-realtime-websocket-sdk-python-56ba4399a24fcf69.md)

<a id="asr-sdk"></a>

Streaming、Message 和 Fun-ASR-Realtime 均使用 `client.audio.asr`。用 `recognize_file` 识别本地文件，或用 `recognize` 创建双向流式识别会话。

<a id="前提条件"></a>

<a id="model-qwen-audio-asr-streaming-8a24f2ed09vr0"></a>

<a id="model-qwen-audio-asr-message-8a24f2ed09vr0"></a>

<a id="model-fun-asr-realtime-8a24f2ed09vr0"></a>

## 前提条件

-   已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请配置API Key到环境变量，而非硬编码在代码中，防范因代码泄露导致的安全风险。
-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="接口地址"></a>

<a id="model-qwen-audio-asr-streaming-h2-1d8e4c7f"></a>

<a id="model-qwen-audio-asr-message-h2-1d8e4c7f"></a>

<a id="model-fun-asr-realtime-h2-1d8e4c7f"></a>

### 接口地址

SDK的实时识别走WebSocket接口，端点由`Client`的`workspace`与`region`自动决定（包含WorkspaceId）。如需切换到其他地域，构造`Client`时设置对应地域的`region`即可。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<a id="快速开始"></a>

<a id="model-qwen-audio-asr-streaming-841b5223db8wu"></a>

<a id="model-qwen-audio-asr-message-841b5223db8wu"></a>

<a id="model-fun-asr-realtime-841b5223db8wu"></a>

## 快速开始

将示例中的 `{WorkspaceId}` 换成实际的业务空间 ID，`{YOUR_AUDIO_FILE}` 换成本地 16 kHz WAV 文件路径。运行后，终端输出识别结果。

<a id="code-block"></a>

```python
import os
import dashscope

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

<a id="更多示例"></a>

### 更多示例

示例使用 Qwen-Audio-ASR-Streaming。调用同组其他模型时，替换 `model`，并按对应模型的要求设置采样率。

| 模型 | 示例中的 `model` 值 |
| --- | --- |
| Qwen-Audio-ASR-Streaming | `qwen-audio-3.1-asr-flash-streaming`。下方麦克风示例使用 `qwen-audio-3.0-asr-flash-streaming`。 |
| Qwen-Audio-ASR-Message | `qwen-audio-3.1-asr-flash-message`，采样率仅支持 16000 Hz。 |
| Fun-ASR-Realtime | `fun-asr-realtime`。 |

[核心资源（`client.audio.asr`）](#model-qwen-audio-asr-streaming-d6bc1f133f871)提供了非流式调用和双向流式调用等接口。请根据实际需求选择合适的调用方式：

-   非流式调用（`recognize_file`）：针对本地文件进行识别，SDK自动分块发送音频并驱动到任务结束。适合处理录制好的音频。
-   双向流式调用（`recognize`会话）：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。

<a id="model-qwen-audio-asr-streaming-8341058094tc3"></a>

<a id="model-qwen-audio-asr-message-8341058094tc3"></a>

<a id="model-fun-asr-realtime-8341058094tc3"></a>

<a id="model-qwen-audio-asr-streaming-9d1e5f6852jr8"></a>

<a id="model-qwen-audio-asr-message-9d1e5f6852jr8"></a>

<a id="model-fun-asr-realtime-9d1e5f6852jr8"></a>

<a id="sec-tabs-2"></a>

<a id="非流式调用"></a>

<a id="非流式调用-h4"></a>

#### 非流式调用

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

调用[核心资源（`client.audio.asr`）](#model-qwen-audio-asr-streaming-d6bc1f133f871)的`recognize_file`方法绑定请求参数并传入本地文件路径，迭代服务端事件获取识别结果。

<a id="code-block-2"></a>

```python
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

<a id="双向流式调用"></a>

<a id="双向流式调用-h4"></a>

#### 双向流式调用

提交单个语音实时转写任务，通过迭代事件的方式流式输出实时识别结果。

1.  启动流式语音识别
    
    调用[核心资源（`client.audio.asr`）](#model-qwen-audio-asr-streaming-d6bc1f133f871)的`recognize`方法创建识别会话并绑定请求参数，进入`with`上下文（自动调用`start`方法建立连接并发送任务）启动流式语音识别。
    
2.  流式传输
    
    循环调用会话的`send_audio_frame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。发送与接收需并发进行：接收线程通过会话的`events()`方法迭代服务端事件，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用会话的`stop`方法结束语音识别。
    
    该方法只通知服务端输入结束；接收线程需继续消费`events()`直到`task-finished`事件以获得最后的识别结果和统计信息。ws层的错误会以`DashScopeError`异常抛出，可在发送/接收处使用try/except捕获。
    

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

mic = None
stream = None

# Set recording parameters
sample_rate = 16000  # 麦克风与请求使用相同的采样率。Qwen-Audio-ASR-Message 仅支持 16000 Hz。
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
    ) as recognition:
        # Open the microphone
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=sample_rate,
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

<a id="请求参数"></a>

## 请求参数

<a id="qwen-audio-asr-streaming"></a>

<a id="model-qwen-audio-asr-streaming"></a>

<a id="model-qwen-audio-asr-streaming-555007db2033f"></a>

### Qwen-Audio-ASR-Streaming

调用示例见本组的[快速开始](#model-qwen-audio-asr-streaming-841b5223db8wu)。返回字段见[Streaming 与 Fun-ASR 的响应结果](#model-qwen-audio-asr-streaming-843fb17087zct)。

请求参数通过[核心资源（`client.audio.asr`）](#model-qwen-audio-asr-streaming-d6bc1f133f871)的`recognize`/`recognize_file`方法进行设置：`model`、`format`、`sample_rate`、`vocabulary_id`可直接传入。通过 `parameters` 字典传入 `language_hints`。

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>model</code></td><td><code>str</code></td><td>是</td><td>模型名称。</td></tr><tr><td><code>sample_rate</code></td><td><code>int</code></td><td>是</td><td><p>采样率（Hz），支持任意采样率。</p></td></tr><tr><td><code>format</code></td><td><code>str</code></td><td>是</td><td>音频格式。<p>取值范围：</p><ul><li><code>pcm</code></li><li><code>wav</code></li><li><code>mp3</code></li><li><code>opus</code></li><li><code>speex</code></li><li><code>aac</code></li><li><code>amr</code></li></ul><div><div><p><strong>重要</strong>opus/speex：必须使用Ogg封装；</p><p>wav：必须为PCM编码；</p><p>amr：仅支持AMR-NB类型。</p></div></div></td></tr><tr><td><code>keep_dialect</code></td><td><code>bool</code></td><td>否</td><td>仅 <code>qwen-audio-3.1-asr-flash-streaming</code> 支持。默认 <code>false</code>，将方言转写为普通话；设为 <code>true</code> 时保留方言表达。通过 <code>parameters</code> 字典传入。完整参数说明请参见<a href="qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md">客户端事件</a>。</td></tr><tr><td><code>vad_model</code></td><td><code>str</code></td><td>否</td><td>仅 <code>qwen-audio-3.1-asr-flash-streaming</code> 支持。可选 <code>near_meeting_16k</code>（近场）或 <code>far_field_meeting_16k</code>（远场，默认值）。通过 <code>parameters</code> 字典传入。完整参数说明请参见<a href="qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md">客户端事件</a>。</td></tr><tr><td><code>vocabulary_id</code></td><td><code>str</code></td><td>否</td><td>预编译热词列表 ID。<p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><code>vocabulary</code></td><td><code>dict</code></td><td>否</td><td>即时热词。<p>以键值对形式传入，键为热词文本（<code>string</code>），值为热词权重（<code>integer</code>），无需预先创建热词列表。权重取值范围为 [1, 5] 或 50：取 [1, 5] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。</p><p>适用于临时性、会话级别的热词优化。</p><p>与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p><p>示例：</p><a id="code-block-3"></a><pre class="language-python"><code>import os
import dashscope

client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

# 即时热词通过parameters传入
vocab = {&quot;张三&quot;: 5, &quot;李四&quot;: 5}
recognition = client.audio.asr.recognize(
    model='qwen-audio-3.1-asr-flash-streaming',
    format='wav',
    sample_rate=16000,
    parameters={&quot;vocabulary&quot;: vocab},
)
</code></pre></td></tr><tr><td><code>max_sentence_silence</code></td><td><code>int</code></td><td>否</td><td>VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。<p>默认值：800。</p><p>取值范围：[200, 6000]。</p></td></tr><tr><td><code>multi_threshold_mode_enabled</code></td><td><code>bool</code></td><td>否</td><td><p>是否启用多阈值模式。启用后可防止 VAD 断句切割过长。</p><p>默认值：False。</p></td></tr><tr><td><code>punctuation_prediction_enabled</code></td><td><code>bool</code></td><td>否</td><td>设置是否在识别结果中自动添加标点：<ul><li>True（默认）：是，不支持修改。</li></ul></td></tr><tr><td><code>heartbeat</code></td><td><code>bool</code></td><td>否</td><td>是否启用心跳包。<p>默认值：False。</p><ul><li>True：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</li><li>False（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</li></ul><p>静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。</p><p>使用该字段时，SDK版本不能低于2.0.1。</p></td></tr><tr><td><code>language_hints</code></td><td><code>list[str]</code></td><td>否</td><td>待识别音频语种。无默认值，不设置时模型自动识别。<p>最多支持设置 4 个值，超出时仅前 4 个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></div></section></td></tr><tr><td><code>speech_noise_threshold</code></td><td><code>float</code></td><td>否</td><td>语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。<p>取值范围：[-1.0, 1.0]。</p><p>取值说明：</p><ul><li>取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写</li><li>取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤</li></ul><p>此参数为高级配置参数，调整可能显著影响识别效果，建议：</p><ul><li>调整前充分测试验证效果</li><li>根据实际音频环境小幅度调整（建议步长 0.1）</li></ul></td></tr><tr><td><code>special_word_filter</code></td><td><code>str</code></td><td>否</td><td>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md#rt03_sensitive_h3">敏感词过滤</a>。</td></tr></tbody></table>

使用 `recognize` 创建识别会话时，通过 `input` 传入上下文。

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>input</code></td><td><code>dict</code></td><td>否</td><td>输入对象，用于传入对话上下文（context）。上下文用于辅助识别、提升专有词汇的识别准确率。使用方法详见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md">提升识别准确率</a>。<p>dict 中需包含 <code>context</code> 键，值为消息列表（list[dict]），每条消息包含以下字段：</p><ul><li><code>role</code>（str，必选）：消息角色。<code>user</code> 表示前几轮用户语音的识别结果或领域相关的词表；<code>assistant</code> 表示前几轮大语言模型的回复内容。</li><li><code>content</code>（list[dict]，必选）：消息内容列表。每个元素包含 <code>type</code>（str，role 为 user 时填 <code>input_text</code>，role 为 assistant 时填 <code>text</code>）和 <code>text</code>（str，文本内容）。</li></ul><div><div><p><strong>重要</strong>上下文消息（<code>input_text</code> 和 <code>text</code> 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度不超过 400 个字符，超出部分从末尾截断。</p></div></div><div><div><p><strong>重要</strong>携带上下文时，<code>context</code> 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 <code>user</code>（<code>input_text</code> 类型）必须在对应的 <code>assistant</code>（<code>text</code> 类型）之前。</p></div></div><div><div><p><strong>说明</strong>使用该字段时，SDK版本不能低于2.0.1。</p></div></div><a id="code-block-4"></a><pre class="language-python"><code># 构建 input 传入数据
input_context = {
    &quot;context&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;你好啊&quot;
                }
            ]
        },
        {
            &quot;role&quot;: &quot;assistant&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;text&quot;,
                    &quot;text&quot;: &quot;你好啊，我是通义千问，有什么可以帮助你的？&quot;
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
</code></pre></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="model-qwen-audio-asr-streaming-cc1002f2d5met"></a>

<a id="model-qwen-audio-asr-message-cc1002f2d5met"></a>

<a id="model-fun-asr-realtime-cc1002f2d5met"></a>

<a id="关键接口"></a>

## 接口参考

<a id="核心资源-client-audio-asr"></a>

<a id="model-qwen-audio-asr-streaming-d6bc1f133f871"></a>

<a id="model-qwen-audio-asr-message-d6bc1f133f871"></a>

<a id="model-fun-asr-realtime-d6bc1f133f871"></a>

### 核心资源（`client.audio.asr`）

实时语音识别能力挂载在`client.audio.asr`资源上：`recognize`创建双向流式识别会话（`Recognition`），`recognize_file`对本地文件一次性识别。

<table><thead><tr><th><strong>成员方法</strong></th><th><strong>方法签名</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>recognize</p></td><td><a id="code-block-5"></a><pre class="language-python"><code>def recognize(self,
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
</code></pre></td><td><p>创建双向流式识别会话，进入<code>with</code>上下文时自动调用<code>start</code>建立连接并发送任务。</p><p>发送音频与消费事件需并发进行（配合<code>send_audio_frame</code>、<code>events()</code>/<code>results()</code>和<code>stop</code>使用）。</p></td></tr><tr><td><p>recognize_file</p></td><td><a id="code-block-6"></a><pre class="language-python"><code>def recognize_file(self,
                   path: str,
                   *,
                   model: str,
                   format: str = &quot;pcm&quot;,
                   sample_rate: int = 16000,
                   ...) -&gt; Iterator[Dict]
</code></pre></td><td><p>基于本地文件的非流式调用：自动分块发送音频并驱动到任务结束，逐个产出服务端事件。该方法要求所识别文件具有可读权限。</p></td></tr><tr><td><p>start</p></td><td><a id="code-block-7"></a><pre class="language-python"><code>def start(self)
</code></pre></td><td><p>开始语音识别：建立连接、发送任务并等待<code>task-started</code>。进入<code>with</code>上下文时自动调用，启动成功后才能发送音频。</p></td></tr><tr><td><p>send_audio_frame</p></td><td><a id="code-block-8"></a><pre class="language-python"><code>def send_audio_frame(self, buffer: bytes)
</code></pre></td><td><p>推送音频。每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。</p><p>识别结果通过<a href="#model-qwen-audio-asr-streaming-85d698b9f9g8s">事件迭代（<code>events()</code>/<code>results()</code>）</a>获取。</p></td></tr><tr><td><p>stop</p></td><td><a id="code-block-9"></a><pre class="language-python"><code>def stop(self)
</code></pre></td><td><p>停止语音识别：只通知服务端输入结束，接收线程需继续消费<code>events()</code>直到<code>task-finished</code>事件。</p></td></tr><tr><td><p>events / results</p></td><td><a id="code-block-10"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
def results(self) -&gt; Iterator[RecognitionResult]
</code></pre></td><td><p>迭代服务端事件：<code>events()</code>产出原始事件<code>dict</code>（识别文本位于<code>payload.output.sentence</code>）；<code>results()</code>只产出识别结果帧，返回<a href="#asr-recognition-result">识别结果（RecognitionResult）</a>类型化对象（心跳帧已过滤）。</p></td></tr><tr><td><p>close</p></td><td><a id="code-block-11"></a><pre class="language-python"><code>def close(self)
</code></pre></td><td><p>关闭识别会话。退出<code>with</code>上下文时自动调用。</p></td></tr><tr><td><p>request_id / first_package_delay / last_package_delay / last_response</p></td><td><a id="code-block-12"></a><pre class="language-python"><code>rec.request_id
rec.first_package_delay
rec.last_package_delay
rec.last_response
</code></pre></td><td><p>获取request_id、首包延迟（从发送第一包音频到收到首包识别结果延迟）和尾包延迟（发送<code>stop</code>指令到最后一包识别结果下发耗时），在任务完成后使用；<code>last_response</code>为最近一次成功读取的原始报文，可用于获取task-failed报错。会话关闭后仍可读取。</p></td></tr></tbody></table>

<a id="事件迭代-events-results"></a>

<a id="model-qwen-audio-asr-streaming-85d698b9f9g8s"></a>

<a id="model-qwen-audio-asr-message-85d698b9f9g8s"></a>

<a id="model-fun-asr-realtime-85d698b9f9g8s"></a>

### 事件迭代（`events()`/`results()`）

[双向流式调用](#model-qwen-audio-asr-streaming-9d1e5f6852jr8)时，服务端会通过事件的方式，将关键流程信息和数据返回给客户端。您需要在接收线程中迭代会话的`events()`（原始事件`dict`）或`results()`（类型化识别结果帧），处理服务端返回的信息或者数据。

<a id="code-block-13"></a>

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

<table><thead><tr><th><strong>事件/迭代方法</strong></th><th><strong>产出内容</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-14"></a><pre class="language-python"><code>event[&quot;header&quot;][&quot;event&quot;] == &quot;task-started&quot;
</code></pre></td><td><p><code>task-started</code>事件</p></td><td><p>无</p></td><td><p>由<code>start()</code>内部读取，启动返回时保存在<code>last_response</code>中，不会由<code>events()</code>再次产出。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
</code></pre></td><td><p><code>event</code>：服务端事件<code>dict</code></p></td><td><p>迭代器</p></td><td><p>当服务有回复时产出事件。识别结果位于<code>payload.output.sentence</code>，可能为心跳或空文本事件，应用可按需忽略。请由一个接收线程持续消费，不要并发创建多个读取者。</p></td></tr><tr><td><a id="code-block-16"></a><pre class="language-python"><code>def results(self) -&gt; Iterator[RecognitionResult]
</code></pre></td><td><p><code>result</code>：识别结果（<code>RecognitionResult</code>）</p></td><td><p>迭代器</p></td><td><p>只产出识别结果帧（心跳帧已过滤），全部识别结果返回后迭代结束。</p></td></tr><tr><td><a id="code-block-17"></a><pre class="language-python"><code>try:
    ...
except DashScopeError as e:
    print(e.code, e.message, e.request_id)
</code></pre></td><td><p><code>DashScopeError</code>异常</p></td><td><p>无</p></td><td><p>发生异常时在发送/接收线程中抛出，可使用try/except捕获。</p></td></tr><tr><td><a id="code-block-18"></a><pre class="language-python"><code>event[&quot;header&quot;][&quot;event&quot;] == &quot;task-finished&quot;
</code></pre></td><td><p><code>task-finished</code>事件</p></td><td><p>无</p></td><td><p>当服务已经完成全部识别后由<code>events()</code>产出，随后迭代结束；发送<code>stop()</code>后仍须读取此事件。</p></td></tr></tbody></table>

<a id="streaming-与-fun-asr-的响应结果"></a>

<a id="model-qwen-audio-asr-streaming-843fb17087zct"></a>

<a id="model-fun-asr-realtime-843fb17087zct"></a>

### Streaming 与 Fun-ASR 的响应结果

<a id="识别结果-recognitionresult"></a>

<a id="asr-recognition-result"></a>

<a id="model-qwen-audio-asr-streaming-bc3e1a43d6hhy"></a>

<a id="model-fun-asr-realtime-bc3e1a43d6hhy"></a>

#### 识别结果（`RecognitionResult`）

`RecognitionResult`代表会话`results()`迭代产出的一次识别结果帧（双向流式调用与非流式调用均可使用；`events()`产出的是原始事件`dict`，如需该类型化视图请改用`results()`）。

<table><thead><tr><th><strong>成员方法</strong></th><th><strong>方法签名</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>get_sentence</code></td><td><a id="code-block-19"></a><pre class="language-python"><code>def get_sentence(self) -&gt; Union[Dict[str, Any], List[Any]]
</code></pre></td><td>获取当前识别的句子及时间戳信息，此方法返回类型为Dict[str, Any]（单句信息）。<p>详情请参见<a href="#model-qwen-audio-asr-streaming-f28f50b035qtn">单句信息（Sentence）</a>。</p></td></tr><tr><td><code>request_id</code></td><td><a id="code-block-20"></a><pre class="language-python"><code>result.request_id
</code></pre></td><td>当前事件对应的请求request_id。</td></tr><tr><td><code>is_sentence_end</code></td><td><a id="code-block-21"></a><pre class="language-python"><code>def is_sentence_end(self) -&gt; bool
</code></pre></td><td>判断当前句子是否已经结束。该方法通过检查 <code>get_sentence()</code> 返回的单句信息中 <code>end_time</code> 字段是否为 <code>None</code> 来判定——<code>end_time</code> 不为 <code>None</code> 时表示句子已结束。</td></tr></tbody></table>

<a id="单句信息-sentence"></a>

<a id="model-qwen-audio-asr-streaming-f28f50b035qtn"></a>

<a id="model-fun-asr-realtime-f28f50b035qtn"></a>

#### 单句信息（`Sentence`）

Sentence类成员如下：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `begin_time` | `int` | 句子开始时间，单位为ms。 |
| `end_time` | `int` | 句子结束时间，单位为ms。 |
| `text` | `str` | 识别文本。 |
| `words` | [字时间戳信息（Word）](#model-qwen-audio-asr-streaming-b55a7391caxxe)的list集合 | 字时间戳信息。 |

<a id="字时间戳信息-word"></a>

<a id="model-qwen-audio-asr-streaming-b55a7391caxxe"></a>

<a id="model-fun-asr-realtime-b55a7391caxxe"></a>

#### 字时间戳信息（`Word`）

Word类成员如下：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `begin_time` | `int` | 字开始时间，单位为ms。 |
| `end_time` | `int` | 字结束时间，单位为ms。 |
| `text` | `str` | 字。 |
| `punctuation` | `str` | 标点。 |

<a id="错误码"></a>

<a id="model-qwen-audio-asr-streaming-605d5ca873bnd"></a>

<a id="model-qwen-audio-asr-message-605d5ca873bnd"></a>

<a id="model-fun-asr-realtime-605d5ca873bnd"></a>

## 错误码

如遇报错问题，请参见[错误码](../model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，可加入[语音 SDK 示例仓库](https://github.com/aliyun/alibabacloud-bailian-speech-demo)中列出的开发者群反馈问题，并提供Request ID，以便进一步排查问题。
