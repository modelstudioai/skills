# Qwen-LiveTranslate-Realtime Python SDK

通过 WebSocket 使用 DashScope Python SDK 调用 Qwen-LiveTranslate-Realtime。

<a id="model-qwen-livetranslate-realtime"></a>

连接与鉴权参见 [WebSocket 接入](livetranslate-realtime-websocket-access-c83c6ed44456849c.md)；事件字段与 JSON 示例参见[客户端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)和[服务端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)。

<a id="前提条件"></a>

<a id="model-qwen-livetranslate-realtime-lt001prereqh2"></a>

## 前提条件

1.  [安装SDK](../model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于2.0.1。
2.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `wss://dashscope.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `wss://dashscope-intl.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="快速开始"></a>

<a id="model-qwen-livetranslate-realtime-lt001exampleh2"></a>

<a id="完整示例"></a>

## 快速开始

以下示例展示如何从麦克风实时录音并进行翻译。

<a id="accordion-麦克风实时翻译示例代码"></a>

麦克风实时翻译示例代码

<a id="code-block"></a>

```python
import os
import sys
import base64
import signal
import pyaudio
from concurrent.futures import ThreadPoolExecutor

import dashscope
from dashscope import DashScopeError

def main():
    # 检查 API Key
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("请设置环境变量 DASHSCOPE_API_KEY")
        sys.exit(1)

    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    client = dashscope.Client(
        # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
        api_key=os.environ["DASHSCOPE_API_KEY"],
        workspace="{WorkspaceId}",
        region="cn-beijing",
    )

    # 初始化 PyAudio
    pya = pyaudio.PyAudio()

    # 初始化扬声器（用于播放翻译后的语音）
    speaker = pya.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=24000,
        output=True,
        frames_per_buffer=2400
    )

    # 初始化麦克风（用于采集语音输入）
    mic = pya.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1600
    )

    # 创建实时翻译会话：进入 with 上下文时自动建立连接
    with client.audio.realtime.connect(
            model="qwen3.5-livetranslate-flash-realtime",
    ) as session:
        # 更新会话配置（建议连接建立后首先调用）
        session.update_session(
            output_modalities=["text", "audio"],
            input_audio_transcription_model="qwen3-asr-flash-realtime",
            voice="Tina",
            translation_params={
                "language": "en",  # 翻译目标语言：英语
                "corpus": {
                    "phrases": {
                        "人工智能": "Artificial Intelligence",
                        "机器学习": "Machine Learning"
                    }
                }
            },
        )

        # 接收线程：迭代服务端事件
        def receive_events():
            try:
                for event in session.events():
                    event_type = event.get("type", "")
                    if event_type == "input_audio_buffer.speech_started":
                        print("====== 检测到语音输入 ======")
                    elif event_type == "input_audio_buffer.speech_stopped":
                        print("====== 语音输入结束 ======")
                    elif event_type == "conversation.item.input_audio_transcription.completed":
                        print(f"[原文] {event.get('transcript', '')}")
                    elif event_type == "response.audio_transcript.done":
                        print(f"[翻译结果] {event.get('transcript', '')}")
                    elif event_type == "response.audio.delta":
                        audio_b64 = event.get("delta", "")
                        if audio_b64:
                            speaker.write(base64.b64decode(audio_b64))
            except DashScopeError as e:
                print(f"[错误] {e.message}")

        with ThreadPoolExecutor(max_workers=1) as pool:
            receiver = pool.submit(receive_events)

            # 注册退出信号处理
            def on_exit(sig, frame):
                print("\n[正在退出...]")
                session.end_session()
                session.close()
                mic.stop_stream()
                mic.close()
                speaker.stop_stream()
                speaker.close()
                pya.terminate()
                sys.exit(0)

            signal.signal(signal.SIGINT, on_exit)

            print("[开始实时翻译] 请对着麦克风说话，按 Ctrl+C 退出")

            # 持续采集麦克风音频并发送（append_audio 也接受原始 bytes，自动编码）
            try:
                while True:
                    audio_data = mic.read(1600, exception_on_overflow=False)
                    session.append_audio(audio_data)
            finally:
                session.end_session()
                receiver.result()

if __name__ == "__main__":
    main()
```

<a id="请求参数"></a>

<a id="model-qwen-livetranslate-realtime-lt001paramsh2"></a>

## 请求参数

-   以下参数通过`client.audio.realtime`的`connect`方法设置。服务端事件不再通过回调接收：在接收线程中迭代会话的`events()`处理（见[事件迭代（`events()`）](#model-qwen-livetranslate-realtime-lt001callback)）。
    
    <a id="accordion-点击查看示例代码"></a>
    
    点击查看示例代码
    
    <a id="code-block-2"></a>
    
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
    
    # 创建实时翻译会话：进入 with 上下文时自动建立连接
    with client.audio.realtime.connect(
        model='qwen3.5-livetranslate-flash-realtime',
    ) as session:
        # 接收线程：迭代服务端事件
        for event in session.events():
            event_type = event.get('type', '')
            if event_type == 'session.created':
                print(f"Session created: {event['session']['id']}")
            elif event_type == 'response.audio_transcript.done':
                print(f"Translation result: {event['transcript']}")
            elif event_type == 'response.audio.delta':
                # 处理增量音频数据（base64）
                audio_b64 = event.get('delta', '')
                # 可将音频数据解码后播放或保存
            elif event_type == 'response.done':
                print('======Response Done======')
            elif event_type == 'input_audio_buffer.speech_started':
                print('======Speech Start======')
            elif event_type == 'input_audio_buffer.speech_stopped':
                print('======Speech Stop======')
    ```
    
    | 参数 | 类型 | 是否必须 | 说明 |
    | --- | --- | --- | --- |
    | `model` | `str` | 是 | 指定要使用的模型名称，推荐使用`qwen3.5-livetranslate-flash-realtime`。 |
    | `ws_url` | `str` | 否 | 会话端点。缺省时由[Client](../model-api-reference/preparations/install-sdk.md)构造参数`workspace`/`region`自动推导实时翻译服务地址（华北2（北京）：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`；新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`）。<br><br>指定 `ws_url` 时，将域名替换为业务空间对应的 [API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)，保留协议和路径。 |
    
-   以下参数通过会话的`update_session`方法设置。
    
    <a id="accordion-点击查看示例代码-2"></a>
    
    点击查看示例代码
    
    <a id="code-block-3"></a>
    
    ```python
    # 设置翻译参数
    translation_params = {
        'language': 'en',  # 目标语言
        'corpus': {
            'phrases': {
                '人工智能': 'Artificial Intelligence',
                '机器学习': 'Machine Learning'
            }
        }
    }
    
    # 更新会话配置
    session.update_session(
        output_modalities=['text', 'audio'],
        voice='Tina',
        translation_params=translation_params,
    )
    ```
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>output_modalities</code></p></td><td><p><code>List[str]</code></p></td><td><p>否</p></td><td><p>模型输出模态。</p><p>默认值：<code>[&quot;text&quot;, &quot;audio&quot;]</code>。</p><p>取值范围：</p><ul><li><p><code>[&quot;text&quot;]</code>：仅输出文本</p></li><li><p><code>[&quot;text&quot;, &quot;audio&quot;]</code>：输出文本和音频</p></li></ul></td></tr><tr><td><p><code>voice</code></p></td><td><p><code>str</code></p></td><td><p>是</p></td><td><p>生成音频的音色。</p><p>默认值：</p><ul><li><p>Qwen3.5-LiveTranslate-Flash-Realtime默认音色为： <code>Tina</code></p></li></ul><p>可选值：参见<a href="../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#0a5bde7593gdk">支持的音色</a>。</p></td></tr><tr><td><p><code>input_audio_transcription_model</code></p></td><td><p><code>str</code></p></td><td><p>否</p></td><td><p>将<code>input_audio_transcription_model</code>设为<code>qwen3-asr-flash-realtime</code>，服务端将返回源语言语音识别结果。</p></td></tr><tr><td><p><code>translation_params</code></p></td><td><p><code>Dict</code></p></td><td><p>否</p></td><td><p>翻译相关配置。</p></td></tr><tr><td><p><code>enable_turn_detection</code></p></td><td><p><code>bool</code></p></td><td><p>否</p></td><td><p>是否启用 VAD（语音活动检测）。</p><p>默认值：<code>True</code>，即启用 VAD 模式，服务端自动检测语音起止并自动触发翻译。</p><p>设为<code>False</code>可切换为 Manual 模式，由客户端通过<code>commit</code>方法手动提交音频。详细参数说明参见<a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md">turn_detection object （可选） 语音活动检测（VAD，Voice Activity Detection）配置，用于控制语音起止的检测方式： 设为配置对象（默认值）：启用 VAD 模式。服务端自动检测语音起止，自动提交音频缓冲区并触发翻译响应，客户端无需发送input_audio_buffer.commit事件。 设为null：启用 Manual 模式。由客户端通过input_audio_buffer.commit事件手动提交音频缓冲区，服务端收到后自动开始生成翻译响应。 属性 type string （可选） VAD 类型，固定为server_vad。 threshold float （可选） VAD 检测灵敏度。值越低，越容易将微弱声音（包括背景噪音）识别为语音；值越高，需要更清晰、音量更大的语音才能触发。 取值范围：[-1.0, 1.0]，默认值为 0.2。 silence_duration_ms integer （可选） 语音结束后需保持静音的最短时长（毫秒）。超过该时长后判定语音结束，服务端自动提交音频缓冲区并触发翻译响应。 取值范围：[200, 6000]，默认值为 1000。</a>。</p></td></tr></tbody></table>
    
-   以下参数通过`update_session`方法的`translation_params`字典设置。
    
    <a id="accordion-点击查看示例代码-3"></a>
    
    点击查看示例代码
    
    <a id="code-block-4"></a>
    
    ```python
    translation_params = {
        'language': 'en',  # 目标语言代码
        'corpus': {
            'phrases': {
                '人工智能': 'Artificial Intelligence',  # 源语言词: 目标语言翻译
                '机器学习': 'Machine Learning'
            }
        }
    }
    ```
    
    | 参数 | 类型 | 是否必须 | 说明 |
    | --- | --- | --- | --- |
    | `language` | `str` | 否 | 翻译目标语言代码。<br><br>默认值：`en`。<br><br>可选值：参见[支持的语种](../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#4ffd192226f0s)。 |
    | `corpus` | `dict` | 否 | 热词配置，用于提升特定词汇的翻译准确性。 |
    | `corpus.phrases` | `dict` | 否 | 热词映射表。key 为源语言词汇，value 为目标语言对应翻译。<br><br>示例：`{'人工智能': 'Artificial Intelligence'}` |
    

<a id="接口参考"></a>

<a id="model-qwen-livetranslate-realtime-lt001interfacesh2"></a>

<a id="关键接口"></a>

## 接口参考

<a id="会话-realtimesession"></a>

<a id="model-qwen-livetranslate-realtime-lt001conversationh3"></a>

### 会话（RealtimeSession）

实时翻译会话通过`client.audio.realtime.connect(model=...)`创建，进入`with`上下文时自动建立连接（也可调用会话的`connect()`方法手动建立）。

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>服务端响应事件（通过<code>events()</code>迭代下发）</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-5"></a><pre class="language-python"><code>def connect(self) -&gt; &quot;RealtimeSession&quot;
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p><blockquote><p>会话已创建</p></blockquote><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>和服务端创建连接。进入<code>with</code>上下文时自动调用。</p></td></tr><tr><td><a id="code-block-6"></a><pre class="language-python"><code>def update_session(self,
    output_modalities: List[str],
    *,
    voice: str = None,
    input_audio_transcription_model: str = None,
    translation_params: Dict[str, Any] = None,
    enable_turn_detection: bool = None,
    **kwargs) -&gt; None:
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p><blockquote><p>会话已更新</p></blockquote></td><td><p>用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注会话<code>update_session</code>方法涉及的参数。</p></td></tr><tr><td><a id="code-block-7"></a><pre class="language-python"><code>def end_session(self) -&gt; None
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md#5369266402pgb">session.finished</a></p><blockquote><p>服务端完成语音翻译，结束会话</p></blockquote></td><td><p>通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音翻译。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-python"><code>def append_audio(self, audio_b64: Union[str, bytes]) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>将音频数据片段追加到云端输入音频缓冲区，支持Base64字符串或原始<code>bytes</code>（自动编码）。服务端会自动检测语音起止并触发翻译。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-python"><code>def commit(self) -&gt; None
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md#ltcommitted001h2">input_audio_buffer.committed</a></p><blockquote><p>输入音频缓冲区已提交</p></blockquote></td><td><p>Manual 模式下，提交之前通过<code>append_audio</code>方法追加到云端缓冲区的音频，服务端收到后自动开始生成翻译响应。VAD 模式下无需调用此方法，服务端会自动提交。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-python"><code>def clear_appended_audio(self) -&gt; None
</code></pre></td><td><p><a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md#ltcleared001h2">input_audio_buffer.cleared</a></p><blockquote><p>输入音频缓冲区已清空</p></blockquote></td><td><p>清空当前云端缓冲区中尚未提交的音频数据。</p></td></tr><tr><td><a id="code-block-11"></a><pre class="language-python"><code>def close(self) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>终止任务，并关闭连接。退出<code>with</code>上下文时自动调用。</p></td></tr><tr><td><a id="code-block-12"></a><pre class="language-python"><code>session.session_id
</code></pre></td><td><p>无</p></td><td><p>获取当前任务的session_id（从<code>session.created</code>事件读取）。</p></td></tr><tr><td><a id="code-block-13"></a><pre class="language-python"><code>session.last_response_id
</code></pre></td><td><p>无</p></td><td><p>获取最近一次response的response_id（从<code>response.created</code>事件读取）。</p></td></tr></tbody></table>

<a id="事件迭代-events"></a>

<a id="model-qwen-livetranslate-realtime-lt001callback"></a>

### 事件迭代（`events()`）

服务端会通过事件的方式，将服务端响应事件和数据返回给客户端。在接收线程中迭代会话的`events()`处理服务端事件，`session.finished`事件后迭代结束。

`error`事件会以`DashScopeError`异常抛出，可在接收线程中使用try/except捕获。

**捕获异常后如何继续接收事件**

<a id="model-qwen-livetranslate-realtime-lt-sdk-error-receive"></a>

捕获 `DashScopeError` 后，原来的 `events()` 迭代已经结束。仅在外层使用 `try/except` 捕获异常，不会让它自动继续接收事件。

如果 WebSocket 连接仍可用，修正请求后重新调用 `events()`，或用 `recv_event()` 逐条接收。连接已关闭时，先[重新建连并配置会话](../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#faq-livetranslate-reconnect)，再开始接收。

排查错误原因时，可从异常的 `body` 读取服务端返回的原始错误事件。

<table><thead><tr><th><strong>方法签名</strong></th><th><strong>参数</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><a id="code-block-14"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict[str, Any]]
</code></pre></td><td><p>event：<a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p></td><td><p>迭代接收服务端事件（<code>dict</code>），<code>session.finished</code>事件后迭代结束。请由一个接收线程持续消费，不要并发创建多个读取者。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-python"><code>def recv_event(self) -&gt; Optional[Dict[str, Any]]
</code></pre></td><td><p>event：<a href="../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md">服务端事件</a></p></td><td><p>读取一条服务端事件，正常关闭后返回<code>None</code>。</p></td></tr></tbody></table>
