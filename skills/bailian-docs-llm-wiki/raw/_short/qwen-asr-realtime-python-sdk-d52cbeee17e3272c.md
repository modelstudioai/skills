# 实时语音识别（Qwen-ASR-Realtime）Python SDK-API参考

本文档介绍如何使用 DashScope Python SDK 调用实时语音识别（Qwen-ASR-Realtime）模型。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

## 前提条件

1.  [安装SDK](raw/model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于2.0.1。
2.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
3.  了解[WebSocket API](raw/_short/qwen-asr-realtime-interaction-process-c2a1fb44670529dd.md)。

## 完整示例

**说明**示例代码读取 `your_audio_file.pcm`（PCM16、16 kHz、单声道）。如仅有 MP3/WAV 等格式，可使用 ffmpeg 转换：

```
ffmpeg -i your_audio.mp3 -ar 16000 -ac 1 -f s16le your_audio_file.pcm
```

```
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

## 请求参数

-   以下参数通过`client.audio.realtime.connect`方法设置。
    
    点击查看示例代码
    
    ```
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
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `model`
    
    `str`
    
    是
    
    指定要使用的[模型](raw/model-user-guide/model-experience/speech-recognition/real-time-speech-recognition-user-guide.md)名称。
    
    `ws_url`
    
    `str`
    
    否
    
    完整WebSocket端点，未指定时按`Client`的`workspace`与`region`自动选择端点：
    
    -   华北2（北京）地域：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
        
    -   新加坡地域：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`。调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
        
    
-   以下参数通过`RealtimeSession`的`update_session`方法设置。
    
    点击查看示例代码
    
    ```
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
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `output_modalities`
    
    `List[str]`
    
    是
    
    模型输出模态，固定为`["text"]`。
    
    `enable_turn_detection`
    
    `bool`
    
    否
    
    是否开启服务端语音活动检测（VAD）。关闭后，需手动调用`commit()`方法触发识别。
    
    默认值：`True`。
    
    取值范围：
    
    -   `True`：开启
        
    -   `False`：关闭
        
    
    `turn_detection_type`
    
    `str`
    
    否
    
    服务端VAD类型，固定为 `server_vad`。
    
    `turn_detection_threshold`
    
    `float`
    
    否
    
    VAD检测阈值。推荐将该值设为`0.0`。
    
    默认值：`0.5`。
    
    取值范围：`[-1, 1]`。
    
    较低的阈值会提高 VAD 的灵敏度，可能将背景噪音误判为语音。较高的阈值则降低灵敏度，有助于在嘈杂环境中减少误触发。
    
    `turn_detection_silence_duration_ms`
    
    `int`
    
    否
    
    VAD断句检测阈值（ms）。静音持续时长超过该阈值将被认为是语句结束。推荐将该值设为`400`。
    
    默认值：`800`。
    
    取值范围：`[200, 6000]`。
    
    较低的值（如 300ms）可使模型更快响应，但可能导致在自然停顿处发生不合理的断句。较高的值（如 1200ms）可更好地处理长句内的停顿，但会增加整体响应延迟。
    
    `transcription_params`
    
    `dict`
    
    否
    
    语音识别相关配置。
    
-   以下参数通过`update_session`的`transcription_params`字典设置。
    
    点击查看示例代码
    
    ```
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
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `language`
    
    `str`
    
    否
    
    音频源语言。
    
    -   zh：中文（普通话、四川话、闽南语、吴语）
        
    -   yue：粤语
        
    -   en：英文
        
    -   ja：日语
        
    -   de：德语
        
    -   ko：韩语
        
    -   ru：俄语
        
    -   fr：法语
        
    -   pt：葡萄牙语
        
    -   ar：阿拉伯语
        
    -   it：意大利语
        
    -   es：西班牙语
        
    -   hi：印地语
        
    -   id：印尼语
        
    -   th：泰语
        
    -   tr：土耳其语
        
    -   uk：乌克兰语
        
    -   vi：越南语
        
    -   cs：捷克语
        
    -   da：丹麦语
        
    -   fil：菲律宾语
        
    -   fi：芬兰语
        
    -   is：冰岛语
        
    -   ms：马来语
        
    -   no：挪威语
        
    -   pl：波兰语
        
    -   sv：瑞典语
        
    
    `sample_rate`
    
    `int`
    
    否
    
    音频采样率（Hz）。支持`16000`和`8000`。
    
    默认值：`16000`。
    
    设置为 `8000` 时，服务端会先升采样到16000Hz再进行识别，可能引入微小延迟。建议仅在源音频为8000Hz（如电话线路）时使用。
    
    `input_audio_format`
    
    `str`
    
    否
    
    音频格式。支持`pcm`和`opus`。
    
    默认值：`pcm`。
    

## 关键接口

### RealtimeSession（`client.audio.realtime.connect`）

实时识别会话通过`client.audio.realtime.connect(model=...)`创建：进入`with`上下文（或调用会话的`connect()`方法）后建立连接。

**方法签名**

**服务端响应事件（通过`events()`下发）**

**说明**

```
def connect(self) -> RealtimeSession
```

[session.created](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#2c04b24bc3wlo)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#4d6ed9dd62vmj)

> 会话配置已更新

和服务端创建连接。进入`with`上下文时自动调用，勿先`connect()`再进入同一会话的`with`。

```
def update_session(self,
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
                   ...) -> None
```

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#4d6ed9dd62vmj)

> 会话配置已更新

用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注[请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)中的涉及到的参数。

```
def append_audio(self, audio_b64: Union[str, bytes]) -> None
```

无

将音频数据片段追加到云端输入音频缓冲区。`str`视为已编码的Base64，`bytes`会自动Base64编码。

-   [请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)`enable_turn_detection`设为`True`，音频缓冲区用于检测语音，服务端决定何时提交。
-   [请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)`enable_turn_detection`设为`False`，客户端可以选择每个事件中放置多少音频量，最多放置 15 MiB。 例如，从客户端流式处理较小的数据块可以让 VAD 响应更迅速。

```
def commit(self) -> None
```

[input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#1108a3764an0e)

> 服务端收到提交的音频

提交之前通过append\_audio添加到云端缓冲区的音视频，如果输入的音频缓冲区为空将产生错误。

**禁用场景：**[请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)`enable_turn_detection`设为`True`时。

```
def end_session(self) -> None
```

[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)

> 服务端完成语音识别，结束会话

通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音识别。

**调用时机**：

-   [VAD 模式（默认）](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#9b49887720jcw)下，发送完音频后调用该方法
-   [Manual 模式](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#ee09a3493fsuc)下，调用commit方法之后调用该方法

```
def close(self) -> None
```

无

终止任务，并关闭连接（幂等，不发送`session.finish`）。

```
def events(self) -> Iterator[Dict]
```

[服务端事件](raw/_short/qwen-asr-realtime-server-events-2783fe3d4d23766f.md)

> 事件类型位于`event["type"]`

连续读取服务端事件。收到`session.finished`后产出该事件并结束迭代；请由一个接收线程持续消费，不要并发创建多个读取者。

```
session.session_id
session.last_response_id
```

无

获取当前任务的session\_id、最近一次response的response\_id（属性）。

### 事件迭代（`events()`）

服务端会通过事件的方式，将服务端响应事件和数据返回给客户端。您需要在接收线程中迭代会话的`events()`，按`event["type"]`分发处理（完整事件列表参见[服务端事件](raw/_short/qwen-asr-realtime-server-events-2783fe3d4d23766f.md)）。

```
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

**方法签名**

**参数**

**说明**

```
def events(self) -> Iterator[Dict]
```

event：[服务端事件](raw/_short/qwen-asr-realtime-server-events-2783fe3d4d23766f.md)

连续读取并逐个产出服务端事件（`dict`）。连接关闭或收到`session.finished`后迭代结束。

```
def recv_event(self) -> Optional[Dict]
```

无

阻塞读取单条服务端事件，不自动循环；无事件（连接关闭）时返回`None`。
