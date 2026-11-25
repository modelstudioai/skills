# Qwen-ASR-Realtime Python SDK

通过 WebSocket 使用 DashScope Python SDK 调用 Qwen-ASR-Realtime。

<a id="model-qwen-asr-realtime"></a>

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="前提条件"></a>

<a id="model-qwen-asr-realtime-b0c7b4e349rvj"></a>

## 前提条件

1.  [安装SDK](../model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于2.0.1。
2.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。
3.  了解[WebSocket API](qwen-asr-realtime-interaction-process-31afcd7f0ef186a0.md)。

<a id="快速开始"></a>

<a id="model-qwen-asr-realtime-qwen-asr-complete-example"></a>

<a id="完整示例"></a>

## 快速开始

> **说明**
>
> 示例代码读取 `your_audio_file.pcm`（PCM16、16 kHz、单声道）。如仅有 MP3/WAV 等格式，可使用 ffmpeg 转换：
>
> <a id="code-block"></a>
>
> ```bash
> ffmpeg -i your_audio.mp3 -ar 16000 -ac 1 -f s16le your_audio_file.pcm
> ```

<a id="code-block-2"></a>

```python
import logging
import os
import signal
import sys
import time
import dashscope
from concurrent.futures import ThreadPoolExecutor

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def setup_logging():
    """配置日志输出"""
    logger = logging.getLogger('dashscope')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def handle_event(event):
    """处理服务端事件"""
    kind = event.get('type')
    if kind == 'session.created':
        print(f"Start session: {event['session']['id']}")
    elif kind == 'conversation.item.input_audio_transcription.completed':
        print(f"Final recognized text: {event['transcript']}")
    elif kind == 'conversation.item.input_audio_transcription.text':
        print(f"Got transcription result: {event['text'] + event['stash']}")
    elif kind == 'input_audio_buffer.speech_started':
        print('======Speech Start======')
    elif kind == 'input_audio_buffer.speech_stopped':
        print('======Speech Stop======')

def receive_events(session):
    """接收并处理服务端事件"""
    for event in session.events():
        handle_event(event)

def read_audio_chunks(file_path, chunk_size=3200):
    """按块读取音频文件"""
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk

def send_audio(session, file_path, delay=0.1):
    """发送音频数据"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file {file_path} does not exist.")

    print("Processing audio file... Press 'Ctrl+C' to stop.")
    for chunk in read_audio_chunks(file_path):
        session.append_audio(chunk)  # bytes 会自动 Base64 编码后发送
        time.sleep(delay)

def main():
    setup_logging()

    audio_file_path = "./your_audio_file.pcm"

    # 进入 with 上下文自动建立连接
    with client.audio.realtime.connect(
        model='qwen3-asr-flash-realtime',
    ) as session:
        def handle_exit(sig, frame):
            print('Ctrl+C pressed, exiting...')
            session.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_exit)

        # 更新会话配置：只输出文本，开启音频转写
        session.update_session(
            output_modalities=['text'],
            enable_input_audio_transcription=True,
            transcription_params={
                'language': 'zh',
                'sample_rate': 16000,
                'input_audio_format': 'pcm',
            },
        )
        # 读取至 session.updated 确认配置生效
        for event in session.events():
            if event.get('type') == 'session.updated':
                break

        with ThreadPoolExecutor(max_workers=1) as pool:
            receiver = pool.submit(receive_events, session)
            try:
                send_audio(session, audio_file_path)
                # send session.finish and wait for finished and close
                session.end_session()
                receiver.result()
            finally:
                # close must run inside the pool context to unblock the receiver
                session.close()
        print("Audio processing completed.")

if __name__ == '__main__':
    main()
```

<a id="请求参数"></a>

<a id="model-qwen-asr-realtime-e80d6aab34svh"></a>

## 请求参数

-   以下参数通过`client.audio.realtime.connect`方法设置。
    
    <a id="accordion-点击查看示例代码"></a>
    
    点击查看示例代码
    
    <a id="code-block-3"></a>
    
    ```python
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    client = dashscope.Client(
        api_key=os.environ.get('DASHSCOPE_API_KEY'),
        # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        workspace="{WorkspaceId}",
        region="cn-beijing",
    )
    
    # 创建实时识别会话：进入 with 上下文自动建立连接
    session = client.audio.realtime.connect(
        model='qwen3-asr-flash-realtime',
    )
    ```
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>model</code></p></td><td><p><code>str</code></p></td><td><p>是</p></td><td><p>指定要使用的<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md">模型</a>名称。</p></td></tr><tr><td><p><code>ws_url</code></p></td><td><p><code>str</code></p></td><td><p>否</p></td><td><p>完整WebSocket端点，未指定时按<code>Client</code>的<code>workspace</code>与<code>region</code>自动选择端点：</p><ul><li><p>华北2（北京）地域：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime</code>。调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></li><li><p>新加坡地域：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime</code>。调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p></li></ul></td></tr></tbody></table>
    
-   以下参数通过`RealtimeSession`的`update_session`方法设置。
    
    <a id="accordion-点击查看示例代码-2"></a>
    
    点击查看示例代码
    
    <a id="code-block-4"></a>
    
    ```python
    session.update_session(
        output_modalities=['text'],
        enable_turn_detection=True,
        turn_detection_type="server_vad",
        turn_detection_threshold=0.0,
        turn_detection_silence_duration_ms=400,
        enable_input_audio_transcription=True,
        transcription_params={
            'language': 'zh',
            'sample_rate': 16000,
            'input_audio_format': 'pcm',
        },
    )
    ```
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>output_modalities</code></p></td><td><p><code>List[str]</code></p></td><td><p>是</p></td><td><p>模型输出模态，固定为<code>[&quot;text&quot;]</code>。</p></td></tr><tr><td><p><code>enable_turn_detection</code></p></td><td><p><code>bool</code></p></td><td><p>否</p></td><td><p>是否开启服务端语音活动检测（VAD）。关闭后，需手动调用<code>commit()</code>方法触发识别。</p><p>默认值：<code>True</code>。</p><p>取值范围：</p><ul><li><p><code>True</code>：开启</p></li><li><p><code>False</code>：关闭</p></li></ul></td></tr><tr><td><p><code>turn_detection_type</code></p></td><td><p><code>str</code></p></td><td><p>否</p></td><td><p>服务端VAD类型，固定为 <code>server_vad</code>。</p></td></tr><tr><td><p><code>turn_detection_threshold</code></p></td><td><p><code>float</code></p></td><td><p>否</p></td><td><div><p>VAD检测阈值。推荐将该值设为<code>0.0</code>。</p><p>默认值：<code>0.5</code>。</p><p>取值范围：<code>[-1, 1]</code>。</p><p>较低的阈值会提高 VAD 的灵敏度，可能将背景噪音误判为语音。较高的阈值则降低灵敏度，有助于在嘈杂环境中减少误触发。</p></div></td></tr><tr><td><p><code>turn_detection_silence_duration_ms</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><div><p>VAD断句检测阈值（ms）。静音持续时长超过该阈值将被认为是语句结束。推荐将该值设为<code>400</code>。</p><p>默认值：<code>800</code>。</p><p>取值范围：<code>[200, 6000]</code>。</p><p>较低的值（如 300ms）可使模型更快响应，但可能导致在自然停顿处发生不合理的断句。较高的值（如 1200ms）可更好地处理长句内的停顿，但会增加整体响应延迟。</p></div></td></tr><tr><td><p><code>transcription_params</code></p></td><td><p><code>dict</code></p></td><td><p>否</p></td><td><p>语音识别相关配置。</p></td></tr></tbody></table>
    
-   以下参数通过`update_session`的`transcription_params`字典设置。
    
    <a id="accordion-点击查看示例代码-3"></a>
    
    点击查看示例代码
    
    <a id="code-block-5"></a>
    
    ```python
    session.update_session(
        output_modalities=['text'],
        enable_input_audio_transcription=True,
        transcription_params={
            'language': 'zh',
            'sample_rate': 16000,
            'input_audio_format': 'pcm',
        },
    )
    ```
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>language</code></p></td><td><p><code>str</code></p></td><td><p>否</p></td><td><div><p>音频源语言。</p><ul><li><p>zh：中文（普通话、四川话、闽南语、吴语）</p></li><li><p>yue：粤语</p></li><li><p>en：英文</p></li><li><p>ja：日语</p></li><li><p>de：德语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>fr：法语</p></li><li><p>pt：葡萄牙语</p></li><li><p>ar：阿拉伯语</p></li><li><p>it：意大利语</p></li><li><p>es：西班牙语</p></li><li><p>hi：印地语</p></li><li><p>id：印尼语</p></li><li><p>th：泰语</p></li><li><p>tr：土耳其语</p></li><li><p>uk：乌克兰语</p></li><li><p>vi：越南语</p></li><li><p>cs：捷克语</p></li><li><p>da：丹麦语</p></li><li><p>fil：菲律宾语</p></li><li><p>fi：芬兰语</p></li><li><p>is：冰岛语</p></li><li><p>ms：马来语</p></li><li><p>no：挪威语</p></li><li><p>pl：波兰语</p></li><li><p>sv：瑞典语</p></li></ul></div></td></tr><tr><td><p><code>sample_rate</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><div><p>音频采样率（Hz）。支持<code>16000</code>和<code>8000</code>。</p><p>默认值：<code>16000</code>。</p><p>设置为 <code>8000</code> 时，服务端会先升采样到16000Hz再进行识别，可能引入微小延迟。建议仅在源音频为8000Hz（如电话线路）时使用。</p></div></td></tr><tr><td><p><code>input_audio_format</code></p></td><td><p><code>str</code></p></td><td><p>否</p></td><td><div><p>音频格式。支持<code>pcm</code>和<code>opus</code>。</p><p>默认值：<code>pcm</code>。</p></div></td></tr></tbody></table>
    

<a id="接口参考"></a>

<a id="model-qwen-asr-realtime-08096516dauq0"></a>

<a id="关键接口"></a>

## 接口参考

<a id="realtimesession-client-audio-realtime-connect"></a>

<a id="model-qwen-asr-realtime-4c4810ff87ofz"></a>

### RealtimeSession（`client.audio.realtime.connect`）

实时识别会话通过`client.audio.realtime.connect(model=...)`创建：进入`with`上下文（或调用会话的`connect()`方法）后建立连接。

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>服务端响应事件（通过<code>events()</code>下发）</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-6"></a><pre class="language-python"><code>def connect(self) -&gt; RealtimeSession
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#2c04b24bc3wlo">session.created</a></p><blockquote><p>会话已创建</p></blockquote><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#4d6ed9dd62vmj">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>和服务端创建连接。进入<code>with</code>上下文时自动调用，勿先<code>connect()</code>再进入同一会话的<code>with</code>。</p></td></tr><tr><td><a id="code-block-7"></a><pre class="language-python"><code>def update_session(self,
                   output_modalities: List[str] = ...,
                   *,
                   voice: str = ...,
                   input_audio_format: str = ...,
                   output_audio_format: str = ...,
                   enable_input_audio_transcription: bool = ...,
                   input_audio_transcription_model: str = ...,
                   enable_turn_detection: bool = ...,
                   turn_detection_type: str = ...,
                   prefix_padding_ms: int = ...,
                   turn_detection_threshold: float = ...,
                   turn_detection_silence_duration_ms: int = ...,
                   turn_detection_param: dict = ...,
                   translation_params: dict = ...,
                   transcription_params: dict = ...,
                   ...) -&gt; None
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#4d6ed9dd62vmj">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注<a href="realtime-websocket-python-sdk-qwen-asr-realtime-281dee62f7074a94.md">请求参数</a>中的涉及到的参数。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-python"><code>def append_audio(self, audio_b64: Union[str, bytes]) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>将音频数据片段追加到云端输入音频缓冲区。<code>str</code>视为已编码的Base64，<code>bytes</code>会自动Base64编码。</p><ul><li><a href="realtime-websocket-python-sdk-qwen-asr-realtime-281dee62f7074a94.md">请求参数</a><code>enable_turn_detection</code>设为<code>True</code>，音频缓冲区用于检测语音，服务端决定何时提交。</li><li><a href="realtime-websocket-python-sdk-qwen-asr-realtime-281dee62f7074a94.md">请求参数</a><code>enable_turn_detection</code>设为<code>False</code>，客户端可以选择每个事件中放置多少音频量，最多放置 15 MiB。 例如，从客户端流式处理较小的数据块可以让 VAD 响应更迅速。</li></ul></td></tr><tr><td><a id="code-block-9"></a><pre class="language-python"><code>def commit(self) -&gt; None
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#1108a3764an0e">input_audio_buffer.committed</a></p><blockquote><p>服务端收到提交的音频</p></blockquote></td><td><p>提交之前通过append_audio添加到云端缓冲区的音视频，如果输入的音频缓冲区为空将产生错误。</p><p><strong>禁用场景：</strong><a href="realtime-websocket-python-sdk-qwen-asr-realtime-281dee62f7074a94.md">请求参数</a><code>enable_turn_detection</code>设为<code>True</code>时。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-python"><code>def end_session(self) -&gt; None
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md#6eaa77339djdv">session.finished</a></p><blockquote><p>服务端完成语音识别，结束会话</p></blockquote></td><td><p>通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音识别。</p><p><strong>调用时机</strong>：</p><ul><li><a href="qwen-asr-realtime-interaction-process-31afcd7f0ef186a0.md#9b49887720jcw">VAD 模式（默认）</a>下，发送完音频后调用该方法</li><li><a href="qwen-asr-realtime-interaction-process-31afcd7f0ef186a0.md#ee09a3493fsuc">Manual 模式</a>下，调用commit方法之后调用该方法</li></ul></td></tr><tr><td><a id="code-block-11"></a><pre class="language-python"><code>def close(self) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>终止任务，并关闭连接（幂等，不发送<code>session.finish</code>）。</p></td></tr><tr><td><a id="code-block-12"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
</code></pre></td><td><p><a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md">服务端事件</a></p><blockquote><p>事件类型位于<code>event[&quot;type&quot;]</code></p></blockquote></td><td><p>连续读取服务端事件。收到<code>session.finished</code>后产出该事件并结束迭代；请由一个接收线程持续消费，不要并发创建多个读取者。</p></td></tr><tr><td><a id="code-block-13"></a><pre class="language-python"><code>session.session_id
session.last_response_id
</code></pre></td><td><p>无</p></td><td><p>获取当前任务的session_id、最近一次response的response_id（属性）。</p></td></tr></tbody></table>

<a id="事件迭代-events"></a>

<a id="model-qwen-asr-realtime-9d08669109iwx"></a>

### 事件迭代（`events()`）

服务端会通过事件的方式，将服务端响应事件和数据返回给客户端。您需要在接收线程中迭代会话的`events()`，按`event["type"]`分发处理（完整事件列表参见[服务端事件](qwen-asr-realtime-server-events-5dc40b9e8a313c98.md)）。

<a id="code-block-14"></a>

```python
def receive_events(session):
    for event in session.events():
        kind = event.get('type')
        if kind == 'session.created':
            print(f"Start session: {event['session']['id']}")
        elif kind == 'conversation.item.input_audio_transcription.completed':
            print(f"Final recognized text: {event['transcript']}")
        elif kind == 'conversation.item.input_audio_transcription.text':
            print(f"Got transcription result: {event['text'] + event['stash']}")
```

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>参数</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-15"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
</code></pre></td><td><p>event：<a href="qwen-asr-realtime-server-events-5dc40b9e8a313c98.md">服务端事件</a></p></td><td><p>连续读取并逐个产出服务端事件（<code>dict</code>）。连接关闭或收到<code>session.finished</code>后迭代结束。</p></td></tr><tr><td><a id="code-block-16"></a><pre class="language-python"><code>def recv_event(self) -&gt; Optional[Dict]
</code></pre></td><td><p>无</p></td><td><p>阻塞读取单条服务端事件，不自动循环；无事件（连接关闭）时返回<code>None</code>。</p></td></tr></tbody></table>
