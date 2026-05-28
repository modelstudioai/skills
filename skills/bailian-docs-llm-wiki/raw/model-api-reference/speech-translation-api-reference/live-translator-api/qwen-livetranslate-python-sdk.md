# 实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考

本文档介绍如何使用 DashScope Python SDK 调用实时音视频翻译（Qwen-LiveTranslate）模型。

## **前提条件**

1.  [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，确保DashScope SDK版本不低于1.25.6。
    
2.  [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

## **请求参数**

-   以下参数通过`OmniRealtimeConversation`的构造方法设置。
    
    **点击查看示例代码**
    
    ```
    from dashscope.audio.qwen_omni import (
        OmniRealtimeConversation,
        OmniRealtimeCallback,
        MultiModality,
    )
    from dashscope.audio.qwen_omni.omni_realtime import TranslationParams
    
    
    class MyCallback(OmniRealtimeCallback):
        """实时翻译回调处理"""
        def __init__(self, conversation=None):
            self.conversation = conversation
            self.handlers = {
                'session.created': self._handle_session_created,
                'response.audio_transcript.done': self._handle_translation_done,
                'response.audio.delta': self._handle_audio_delta,
                'response.done': lambda r: print('======Response Done======'),
                'input_audio_buffer.speech_started': lambda r: print('======Speech Start======'),
                'input_audio_buffer.speech_stopped': lambda r: print('======Speech Stop======'),
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
            print(f"Session created: {response['session']['id']}")
    
        def _handle_translation_done(self, response):
            print(f"Translation result: {response['transcript']}")
    
        def _handle_audio_delta(self, response):
            # 处理增量音频数据
            audio_b64 = response.get('delta', '')
            # 可将音频数据解码后播放或保存
    
    conversation = OmniRealtimeConversation(
        model='qwen3.5-livetranslate-flash-realtime',
        # 以下为中国内地地域url，若使用国际版，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime',
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
    
    指定要使用的模型名称，推荐使用`qwen3.5-livetranslate-flash-realtime`。
    
    > `qwen3-livetranslate-flash-realtime`为旧版模型。
    
    `callback`
    
    `[回调接口（OmniRealtimeCallback）](#lt001callback)`
    
    是
    
    用于处理服务端事件的回调对象实例。
    
    `url`
    
    `str`
    
    是
    
    实时翻译服务地址：
    
    -   中国内地：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
        
    -   国际：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime`
        
    
-   以下参数通过`OmniRealtimeConversation`的`update_session`方法设置。
    
    **点击查看示例代码**
    
    ```
    # 设置翻译参数
    translation_params = TranslationParams(
        language='en',  # 目标语言
        corpus=TranslationParams.Corpus(
            phrases={
                '人工智能': 'Artificial Intelligence',
                '机器学习': 'Machine Learning'
            }
        )
    )
    
    # 更新会话配置
    conversation.update_session(
        output_modalities=[MultiModality.TEXT, MultiModality.AUDIO],
        voice='Tina',
        translation_params=translation_params,
    )
    ```
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `output_modalities`
    
    `List[MultiModality]`
    
    否
    
    模型输出模态。
    
    默认值：`[MultiModality.TEXT, MultiModality.AUDIO]`。
    
    取值范围：
    
    -   `[MultiModality.TEXT]`：仅输出文本
        
    -   `[MultiModality.TEXT, MultiModality.AUDIO]`：输出文本和音频
        
    
    `voice`
    
    `str`
    
    否
    
    生成音频的音色。
    
    默认值：
    
    -   Qwen3.5-LiveTranslate-Flash-Realtime默认音色为： `Tina`
        
    -   Qwen3-LiveTranslate-Flash-Realtime默认音色为： `Cherry`
        
    
    可选值：参见[支持的音色](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#0a5bde7593gdk)。
    
    `input_audio_transcription_model`
    
    `str`
    
    否
    
    将`input_audio_transcription_model`设为`qwen3-asr-flash-realtime`，服务端将返回源语言语音识别结果。
    
    `translation_params`
    
    `TranslationParams`
    
    否
    
    翻译相关配置。
    
-   以下参数通过`TranslationParams`的构造方法设置。
    
    **点击查看示例代码**
    
    ```
    translation_params = TranslationParams(
        language='en',  # 目标语言代码
        corpus=TranslationParams.Corpus(
            phrases={
                '人工智能': 'Artificial Intelligence',  # 源语言词: 目标语言翻译
                '机器学习': 'Machine Learning'
            }
        )
    )
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
    
    `TranslationParams.Corpus`
    
    否
    
    热词配置，用于提升特定词汇的翻译准确性。
    
    `corpus.phrases`
    
    `dict`
    
    否
    
    热词映射表。key 为源语言词汇，value 为目标语言对应翻译。
    
    示例：`{'人工智能': 'Artificial Intelligence'}`
    

## **关键接口**

### **OmniRealtimeConversation类**

OmniRealtimeConversation通过`from dashscope.audio.qwen_omni import OmniRealtimeConversation`方法引入。

**方法签名**

**服务端响应事件（通过回调下发）**

**说明**

```
def connect(self) -> None:
```

[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events#2c04b24bc3wlo)

> 会话已创建

[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events#4d6ed9dd62vmj)

> 会话配置已更新

和服务端创建连接。

```
def update_session(self,
    output_modalities: List[MultiModality],
    voice: str = None,
    translation_params: TranslationParams = None,
    **kwargs) -> None:
```

[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events#4d6ed9dd62vmj)

> 会话配置已更新

用于更新会话配置，建议在连接建立后首先调用该方法进行设置。若未调用该方法，系统将使用默认配置。只需关注`OmniRealtimeConversation`的`update_session`方法涉及的参数。

```
def end_session(self, timeout: int = 20) -> None:
```

[session.finished](https://help.aliyun.com/zh/model-studio/live-translator-server-events#5369266402pgb)

> 服务端完成语音翻译，结束会话

通知服务端结束会话，服务端收到会话结束通知后将完成最后的语音翻译。

```
def append_audio(self, audio_b64: str) -> None:
```

无

将Base64编码后的音频数据片段追加到云端输入音频缓冲区。服务端会自动检测语音起止并触发翻译。

```
def close(self) -> None:
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

### **回调接口（OmniRealtimeCallback）**

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

message：[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events)

收到服务端事件时触发。

```
def on_close(self, close_status_code, close_msg) -> None:
```

close\_status\_code：状态码

close\_msg：WebSocket连接关闭时的日志信息

WebSocket连接关闭时触发。

## **完整示例**

以下示例展示如何从麦克风实时录音并进行翻译。

**麦克风实时翻译示例代码**

```
import os
import sys
import base64
import signal
import pyaudio
from dashscope.audio.qwen_omni import (
    OmniRealtimeConversation,
    OmniRealtimeCallback,
    MultiModality,
)
from dashscope.audio.qwen_omni.omni_realtime import TranslationParams

class Callback(OmniRealtimeCallback):
    """实时翻译回调处理类"""

    def __init__(self, speaker):
        self.speaker = speaker

    def on_open(self):
        print("[连接已建立]")

    def on_close(self, code, msg):
        print(f"[连接已关闭] code: {code}, msg: {msg}")

    def on_event(self, response):
        event_type = response.get("type", "")
        if event_type == "input_audio_buffer.speech_started":
            print("====== 检测到语音输入 ======")
        elif event_type == "input_audio_buffer.speech_stopped":
            print("====== 语音输入结束 ======")
        elif event_type == "conversation.item.input_audio_transcription.completed":
            print(f"[原文] {response.get('transcript', '')}")
        elif event_type == "response.audio_transcript.done":
            print(f"[翻译结果] {response.get('transcript', '')}")
        elif event_type == "response.audio.delta":
            audio_b64 = response.get("delta", "")
            if audio_b64:
                self.speaker.write(base64.b64decode(audio_b64))
        elif event_type == "error":
            print(f"[错误] {response.get('error', {}).get('message', '')}")

def main():
    # 检查 API Key
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("请设置环境变量 DASHSCOPE_API_KEY")
        sys.exit(1)

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

    # 创建回调实例
    callback = Callback(speaker=speaker)

    # 创建实时会话
    conversation = OmniRealtimeConversation(
        model="qwen3.5-livetranslate-flash-realtime",
        # 国际地域使用 wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
        url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime",  
        callback=callback
    )

    # 连接服务端
    conversation.connect()

    # 配置翻译参数
    translation_params = TranslationParams(
        language="en",  # 翻译目标语言：英语
        corpus=TranslationParams.Corpus(
            phrases={
                "人工智能": "Artificial Intelligence",
                "机器学习": "Machine Learning"
            }
        )
    )

    # 更新会话配置
    conversation.update_session(
        output_modalities=[MultiModality.TEXT, MultiModality.AUDIO],
        input_audio_transcription_model="qwen3-asr-flash-realtime",
        voice="Tina",
        translation_params=translation_params,
    )

    # 注册退出信号处理
    def on_exit(sig, frame):
        print("\n[正在退出...]")
        mic.stop_stream()
        mic.close()
        speaker.stop_stream()
        speaker.close()
        pya.terminate()
        conversation.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)

    print("[开始实时翻译] 请对着麦克风说话，按 Ctrl+C 退出")

    # 持续采集麦克风音频并发送
    while True:
        audio_data = mic.read(1600, exception_on_overflow=False)
        conversation.append_audio(base64.b64encode(audio_data).decode("ascii"))

if __name__ == "__main__":
    main()
```
