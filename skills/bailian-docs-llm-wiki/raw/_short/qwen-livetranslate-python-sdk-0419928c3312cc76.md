# 实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考

本文档介绍如何使用 DashScope Python SDK 调用实时音视频翻译（Qwen-LiveTranslate）模型。

## 前提条件

1.  [安装SDK](raw/model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于2.0.1。
2.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：

-   华北2（北京）地域：从 `wss://dashscope.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `wss://dashscope-intl.aliyuncs.com` 迁移至 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

## 请求参数

-   以下参数通过`client.audio.realtime`的`connect`方法设置。服务端事件不再通过回调接收：在接收线程中迭代会话的`events()`处理（见[事件迭代（`events()`）](#lt001callback)）。
    
    点击查看示例代码
    
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
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `model`
    
    `str`
    
    是
    
    指定要使用的模型名称，推荐使用`qwen3.5-livetranslate-flash-realtime`。
    
    `ws_url`
    
    `str`
    
    否
    
    会话端点。缺省时由[Client](raw/model-api-reference/preparations/install-sdk.md)构造参数`workspace`/`region`自动推导实时翻译服务地址（华北2（北京）：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`；新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`）。
    
    调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
    
-   以下参数通过会话的`update_session`方法设置。
    
    点击查看示例代码
    
    ```
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
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `output_modalities`
    
    `List[str]`
    
    否
    
    模型输出模态。
    
    默认值：`["text", "audio"]`。
    
    取值范围：
    
    -   `["text"]`：仅输出文本
        
    -   `["text", "audio"]`：输出文本和音频
        
    
    `voice`
    
    `str`
    
    是
    
    生成音频的音色。
    
    默认值：
    
    -   Qwen3.5-LiveTranslate-Flash-Realtime默认音色为： `Tina`
        
    
    可选值：参见[支持的音色](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#0a5bde7593gdk)。
    
    `input_audio_transcription_model`
    
    `str`
    
    否
    
    将`input_audio_transcription_model`设为`qwen3-asr-flash-realtime`，服务端将返回源语言语音识别结果。
    
    `translation_params`
    
    `Dict`
    
    否
    
    翻译相关配置。
    
    `enable_turn_detection`
    
    `bool`
    
    否
    
    是否启用 VAD（语音活动检测）。
    
    默认值：`True`，即启用 VAD 模式，服务端自动检测语音起止并自动触发翻译。
    
    设为`False`可切换为 Manual 模式，由客户端通过`commit`方法手动提交音频。详细参数说明参见[turn\_detection object （可选） 语音活动检测（VAD，Voice Activity Detection）配置，用于控制语音起止的检测方式： 设为配置对象（默认值）：启用 VAD 模式。服务端自动检测语音起止，自动提交音频缓冲区并触发翻译响应，客户端无需发送input\_audio\_buffer.commit事件。 设为null：启用 Manual 模式。由客户端通过input\_audio\_buffer.commit事件手动提交音频缓冲区，服务端收到后自动开始生成翻译响应。 属性 type string （可选） VAD 类型，固定为server\_vad。 threshold float （可选） VAD 检测灵敏度。值越低，越容易将微弱声音（包括背景噪音）识别为语音；值越高，需要更清晰、音量更大的语音才能触发。 取值范围：\[-1.0, 1.0\]，默认值为 0.2。 silence\_duration\_ms integer （可选） 语音结束后需保持静音的最短时长（毫秒）。超过该时长后判定语音结束，服务端自动提交音频缓冲区并触发翻译响应。 取值范围：\[200, 6000\]，默认值为 1000。](raw/_short/live-translator-client-events-666da53ef8b3942d.md)。
    
-   以下参数通过`update_session`方法的`translation_params`字典设置。
    
    点击查看示例代码
    
    ```
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
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `language`
    
    `str`
    
    否
    
    翻译目标语言代码。
    
    默认值：`en`。
    
    可选值：参见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#4ffd192226f0s)。
    
    `corpus`
    
    `dict`
    
    否
    
    热词配置，用于提升特定词汇的翻译准确性。
    
    `corpus.phrases`
    
    `dict`
    
    否
    
    热词映射表。key 为源语言词汇，value 为目标语言对应翻译。
    
    示例：`{'人工智能': 'Artificial Intelligence'}`
    

## 关键接口

### 会话（RealtimeSession）

实时翻译会话通过`client.audio.realtime.connect(model=...)`创建，进入`with`上下文时自动建立连接（也可调用会话的`connect()`方法手动建立）。

**方法签名**

**服务端响应事件（通过`events()`迭代下发）**

**说明**

```
def connect(self) -> "RealtimeSession"
```

[服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)

> 会话已创建

[服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)

> 会话配置已更新

和服务端创建连接。进入`with`上下文时自动调用。

```
def update_session(self,
    output_modalities: List[str],
    *,
    voice: str = None,
    input_audio_transcription_model: str = None,
    translation_params: Dict[str, Any] = None,
    enable_turn_detection: bool = None,
    **kwargs) -> None:
```

[服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)

> 会话已更新

用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注会话`update_session`方法涉及的参数。

```
def end_session(self) -> None
```

[session.finished](https://help.aliyun.com/zh/model-studio/live-translator-server-events#5369266402pgb)

> 服务端完成语音翻译，结束会话

通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音翻译。

```
def append_audio(self, audio_b64: Union[str, bytes]) -> None
```

无

将音频数据片段追加到云端输入音频缓冲区，支持Base64字符串或原始`bytes`（自动编码）。服务端会自动检测语音起止并触发翻译。

```
def commit(self) -> None
```

[input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/live-translator-server-events#ltcommitted001h2)

> 输入音频缓冲区已提交

Manual 模式下，提交之前通过`append_audio`方法追加到云端缓冲区的音频，服务端收到后自动开始生成翻译响应。VAD 模式下无需调用此方法，服务端会自动提交。

```
def clear_appended_audio(self) -> None
```

[input\_audio\_buffer.cleared](https://help.aliyun.com/zh/model-studio/live-translator-server-events#ltcleared001h2)

> 输入音频缓冲区已清空

清空当前云端缓冲区中尚未提交的音频数据。

```
def close(self) -> None
```

无

终止任务，并关闭连接。退出`with`上下文时自动调用。

```
session.session_id
```

无

获取当前任务的session\_id（从`session.created`事件读取）。

```
session.last_response_id
```

无

获取最近一次response的response\_id（从`response.created`事件读取）。

### 事件迭代（`events()`）

服务端会通过事件的方式，将服务端响应事件和数据返回给客户端。在接收线程中迭代会话的`events()`处理服务端事件，`session.finished`事件后迭代结束。

`error`事件会以`DashScopeError`异常抛出，可在接收线程中使用try/except捕获。

**方法签名**

**参数**

**说明**

```
def events(self) -> Iterator[Dict[str, Any]]
```

event：[服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)

迭代接收服务端事件（`dict`），`session.finished`事件后迭代结束。请由一个接收线程持续消费，不要并发创建多个读取者。

```
def recv_event(self) -> Optional[Dict[str, Any]]
```

event：[服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)

读取一条服务端事件，正常关闭后返回`None`。

## 完整示例

以下示例展示如何从麦克风实时录音并进行翻译。

麦克风实时翻译示例代码

```
import os
import sys
import base64
import signal
import pyaudio
from concurrent.futures import ThreadPoolExecutor

import dashscope
from dashscope.v2 import DashScopeError

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
