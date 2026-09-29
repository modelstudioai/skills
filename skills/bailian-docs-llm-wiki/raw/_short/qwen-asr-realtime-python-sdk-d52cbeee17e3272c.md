# 实时语音识别（Qwen-ASR-Realtime）Python SDK-API参考

本文档介绍如何使用 DashScope Python SDK 调用实时语音识别（Qwen-ASR-Realtime）模型。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

## 前提条件

1.  [安装SDK](raw/model-api-reference/preparations/install-sdk.md)，确保DashScope SDK版本不低于1.25.6。
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
import base64
import signal
import sys
import time
import dashscope
from dashscope.audio.qwen_omni import *
from dashscope.audio.qwen_omni.omni_realtime import TranscriptionParams

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

def init_api_key():
    """初始化 API Key"""
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY', 'YOUR_API_KEY')
    if dashscope.api_key == 'YOUR_API_KEY':
        print('[Warning] Using placeholder API key, set DASHSCOPE_API_KEY environment variable.')

class MyCallback(OmniRealtimeCallback):
    """实时识别回调处理"""
    def __init__(self, conversation):
        self.conversation = conversation
        self.handlers = {
            'session.created': self._handle_session_created,
            'conversation.item.input_audio_transcription.completed': self._handle_final_text,
            'conversation.item.input_audio_transcription.text': self._handle_transcription_text,
            'input_audio_buffer.speech_started': lambda r: print('======Speech Start======'),
            'input_audio_buffer.speech_stopped': lambda r: print('======Speech Stop======')
        }

    def on_open(self):
        print('Connection opened')

    def on_close(self, code, msg):
        print(f'Connection closed, code: {code}, msg: {msg}')

    def on_event(self, response):
        try:
            handler = self.handlers.get(response['type'])
            if handler:
                handler(response)
        except Exception as e:
            print(f'[Error] {e}')

    def _handle_session_created(self, response):
        print(f"Start session: {response['session']['id']}")

    def _handle_final_text(self, response):
        print(f"Final recognized text: {response['transcript']}")

    def _handle_transcription_text(self, response):
        print(f"Got transcription result: {response['text'] + response['stash']}")

def read_audio_chunks(file_path, chunk_size=3200):
    """按块读取音频文件"""
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk

def send_audio(conversation, file_path, delay=0.1):
    """发送音频数据"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file {file_path} does not exist.")

    print("Processing audio file... Press 'Ctrl+C' to stop.")
    for chunk in read_audio_chunks(file_path):
        audio_b64 = base64.b64encode(chunk).decode('ascii')
        conversation.append_audio(audio_b64)
        time.sleep(delay)

def main():
    setup_logging()
    init_api_key()

    audio_file_path = "./your_audio_file.pcm"
    callback = MyCallback(conversation=None)
    conversation = OmniRealtimeConversation(
        model='qwen3-asr-flash-realtime',
        # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime',
        callback=callback,
    )
    callback.conversation = conversation  # 把 conversation 注入回调，用于回调中调用其方法

    def handle_exit(sig, frame):
        print('Ctrl+C pressed, exiting...')
        conversation.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)

    conversation.connect()

    transcription_params = TranscriptionParams(
        language='zh',
        sample_rate=16000,
        input_audio_format="pcm"
    )

    conversation.update_session(
        output_modalities=[MultiModality.TEXT],
        enable_input_audio_transcription=True,
        transcription_params=transcription_params
    )

    try:
        send_audio(conversation, audio_file_path)
        # send session.finish and wait for finished and close
        conversation.end_session()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conversation.close()
        print("Audio processing completed.")

if __name__ == '__main__':
    main()
```

## 请求参数

-   以下参数通过`OmniRealtimeConversation`的构造方法设置。
    
    点击查看示例代码
    
    ```
    class MyCallback(OmniRealtimeCallback):
        """实时识别回调处理"""
        def __init__(self, conversation):
            self.conversation = conversation
            self.handlers = {
                'session.created': self._handle_session_created,
                'conversation.item.input_audio_transcription.completed': self._handle_final_text,
                'conversation.item.input_audio_transcription.text': self._handle_stash_text,
                'input_audio_buffer.speech_started': lambda r: print('======Speech Start======'),
                'input_audio_buffer.speech_stopped': lambda r: print('======Speech Stop======')
            }
    
        def on_open(self):
            print('Connection opened')
    
        def on_close(self, code, msg):
            print(f'Connection closed, code: {code}, msg: {msg}')
    
        def on_event(self, response):
            try:
                handler = self.handlers.get(response['type'])
                if handler:
                    handler(response)
            except Exception as e:
                print(f'[Error] {e}')
    
        def _handle_session_created(self, response):
            print(f"Start session: {response['session']['id']}")
    
        def _handle_final_text(self, response):
            print(f"Final recognized text: {response['transcript']}")
    
        def _handle_stash_text(self, response):
            print(f"Got stash result: {response['stash']}")
    
    conversation = OmniRealtimeConversation(
            model='qwen3-asr-flash-realtime',
            # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
            url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime',
            callback=MyCallback(conversation=None)  # 暂时传None，稍后注入
        )
    # 注入自身到回调
    conversation.callback.conversation = conversation
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `model`
    
    `str`
    
    是
    
    指定要使用的[模型](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)名称。
    
    `callback`
    
    `OmniRealtimeCallback`
    
    是
    
    用于处理服务端事件的回调对象实例。
    
    `url`
    
    `str`
    
    是
    
    语音识别服务地址：
    
    -   华北2（北京）地域：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
        
    -   新加坡地域：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`。调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
        
    
-   以下参数通过`OmniRealtimeConversation`的`update_session`方法设置。
    
    点击查看示例代码
    
    ```
    transcription_params = TranscriptionParams(
        language='zh',
        sample_rate=16000,
        input_audio_format="pcm"
    )
    
    conversation.update_session(
        output_modalities=[MultiModality.TEXT],
        enable_turn_detection=True,
        turn_detection_type="server_vad",
        turn_detection_threshold=0.0,
        turn_detection_silence_duration_ms=400,
        enable_input_audio_transcription=True,
        transcription_params=transcription_params
    )
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `output_modalities`
    
    `List[MultiModality]`
    
    是
    
    模型输出模态，固定为`[MultiModality.TEXT]`。
    
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
    
    `TranscriptionParams`
    
    否
    
    语音识别相关配置。
    
-   以下参数通过`TranscriptionParams`的构造方法设置。
    
    点击查看示例代码
    
    ```
    transcription_params = TranscriptionParams(
        language='zh',
        sample_rate=16000,
        input_audio_format="pcm"
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

### OmniRealtimeConversation类

OmniRealtimeConversation通过`from dashscope.audio.qwen_omni import OmniRealtimeConversation`方法引入。

**方法签名**

**服务端响应事件（通过回调下发）**

**说明**

```
def connect(self,) -> None:
```

[session.created](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#2c04b24bc3wlo)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#4d6ed9dd62vmj)

> 会话配置已更新

和服务端创建连接。

```
def update_session(self,
                       output_modalities: List[MultiModality],
                       voice: str = None,
                       input_audio_format: AudioFormat = AudioFormat.PCM_16000HZ_MONO_16BIT,
                       output_audio_format: AudioFormat = AudioFormat.PCM_24000HZ_MONO_16BIT,
                       enable_input_audio_transcription: bool = True,
                       input_audio_transcription_model: str = None,
                       enable_turn_detection: bool = True,
                       turn_detection_type: str = 'server_vad',
                       prefix_padding_ms: int = 300,
                       turn_detection_threshold: float = 0.2,
                       turn_detection_silence_duration_ms: int = 800,
                       turn_detection_param: dict = None,
                       translation_params: TranslationParams = None,
                       transcription_params: TranscriptionParams = None,
                       **kwargs) -> None:
```

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#4d6ed9dd62vmj)

> 会话配置已更新

用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注[请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)中的涉及到的参数。

```
def append_audio(self, audio_b64: str) -> None:
```

无

将Base64编码后的音频数据片段追加到云端输入音频缓冲区。

-   [请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)`enable_turn_detection`设为`True`，音频缓冲区用于检测语音，服务端决定何时提交。
-   [请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)`enable_turn_detection`设为`False`，客户端可以选择每个事件中放置多少音频量，最多放置 15 MiB。 例如，从客户端流式处理较小的数据块可以让 VAD 响应更迅速。

```
def commit(self, ) -> None:
```

[input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#1108a3764an0e)

> 服务端收到提交的音频

提交之前通过append添加到云端缓冲区的音视频，如果输入的音频缓冲区为空将产生错误。

**禁用场景：**[请求参数](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)`enable_turn_detection`设为`True`时。

```
def end_session(self, timeout: int = 20) -> None:
```

[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)

> 服务端完成语音识别，结束会话

通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音识别。

**调用时机**：

-   [VAD 模式（默认）](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#9b49887720jcw)下，发送完音频后调用该方法
-   [Manual 模式](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#ee09a3493fsuc)下，调用commit方法之后调用该方法

`end_session_async` 是 `end_session` 的异步版本，两者功能完全相同。

```
def close(self, ) -> None:
```

无

终止任务，并关闭连接。

```
def get_session_id(self) -> str:
```

无

获取当前任务的session\_id。

```
def get_last_response_id(self) -> str:
```

无

获取最近一次response的response\_id。

### 回调接口（OmniRealtimeCallback）

服务端会通过回调的方式，将服务端响应事件和数据返回给客户端。

继承此类并实现相应方法以处理服务端事件。

通过`from dashscope.audio.qwen_omni import OmniRealtimeCallback`引入。

**方法签名**

**参数**

**说明**

```
def on_open(self) -> None:
```

无

WebSocket连接成功建立时触发。

```
def on_event(self, message: dict) -> None:
```

message：[服务端事件](raw/_short/qwen-asr-realtime-server-events-2783fe3d4d23766f.md)

收到服务端事件时触发。

```
def on_close(self, close_status_code, close_msg) -> None:
```

close\_status\_code：状态码

close\_msg：WebSocket连接关闭时的日志信息

WebSocket连接关闭时触发。
