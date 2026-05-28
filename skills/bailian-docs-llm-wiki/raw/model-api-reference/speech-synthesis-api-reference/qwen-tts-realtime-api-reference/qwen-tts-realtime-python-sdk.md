# Python SDK

本文介绍 DashScope Python SDK 调用[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)时的关键接口与请求参数。

**用户指南**：关于模型介绍和选型建议请参见[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)或[语音合成-千问](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

## **前期准备**

DashScope Python SDK 版本需要不低于1.25.11。

## **快速开始**

## **server commit模式**

```
import os
import base64
import threading
import time
import dashscope
from dashscope.audio.qwen_tts_realtime import *

qwen_tts_realtime: QwenTtsRealtime = None
text_to_synthesize = [
    '对吧~我就特别喜欢这种超市，',
    '尤其是过年的时候',
    '去逛超市',
    '就会觉得',
    '超级超级开心！',
    '想买好多好多的东西呢！'
]

DO_VIDEO_TEST = False

def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = 'your-dashscope-api-key'  # set API-key manually

class MyCallback(QwenTtsRealtimeCallback):
    def __init__(self):
        self.complete_event = threading.Event()
        self.file = open('result_24k.pcm', 'wb')

    def on_open(self) -> None:
        print('connection opened, init player')

    def on_close(self, close_status_code, close_msg) -> None:
        self.file.close()
        print('connection closed with code: {}, msg: {}, destroy player'.format(close_status_code, close_msg))

    def on_event(self, response: str) -> None:
        try:
            global qwen_tts_realtime
            type = response['type']
            if 'session.created' == type:
                print('start session: {}'.format(response['session']['id']))
            if 'response.audio.delta' == type:
                recv_audio_b64 = response['delta']
                self.file.write(base64.b64decode(recv_audio_b64))
            if 'response.done' == type:
                print(f'response {qwen_tts_realtime.get_last_response_id()} done')
            if 'session.finished' == type:
                print('session finished')
                self.complete_event.set()
        except Exception as e:
            print('[Error] {}'.format(e))
            return

    def wait_for_finished(self):
        self.complete_event.wait()

if __name__  == '__main__':
    init_dashscope_api_key()

    print('Initializing ...')

    callback = MyCallback()

    qwen_tts_realtime = QwenTtsRealtime(
        # 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime
        model='qwen3-tts-flash-realtime',
        callback=callback, 
        # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
        )

    qwen_tts_realtime.connect()
    qwen_tts_realtime.update_session(
        voice = 'Cherry',
        response_format = AudioFormat.PCM_24000HZ_MONO_16BIT,
        # 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash-realtime
        # instructions='语速较快，带有明显的上扬语调，适合介绍时尚产品。',
        # optimize_instructions=True,
        mode = 'server_commit'        
    )
    for text_chunk in text_to_synthesize:
        print(f'send text: {text_chunk}')
        qwen_tts_realtime.append_text(text_chunk)
        time.sleep(0.1)
    qwen_tts_realtime.finish()
    callback.wait_for_finished()
    print('[Metric] session: {}, first audio delay: {}'.format(
                    qwen_tts_realtime.get_session_id(), 
                    qwen_tts_realtime.get_first_audio_delay(),
                    ))
```

## **commit模式**

```
import base64
import os
import threading
import dashscope
from dashscope.audio.qwen_tts_realtime import *

qwen_tts_realtime: QwenTtsRealtime = None
text_to_synthesize = [
    '这是第一句话。',
    '这是第二句话。',
    '这是第三句话。',
]

DO_VIDEO_TEST = False

def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = 'your-dashscope-api-key'  # set API-key manually

class MyCallback(QwenTtsRealtimeCallback):
    def __init__(self):
        super().__init__()
        self.response_counter = 0
        self.complete_event = threading.Event()
        self.file = open(f'result_{self.response_counter}_24k.pcm', 'wb')

    def reset_event(self):
        self.response_counter += 1
        self.file = open(f'result_{self.response_counter}_24k.pcm', 'wb')
        self.complete_event = threading.Event()

    def on_open(self) -> None:
        print('connection opened, init player')

    def on_close(self, close_status_code, close_msg) -> None:
        print('connection closed with code: {}, msg: {}, destroy player'.format(close_status_code, close_msg))

    def on_event(self, response: str) -> None:
        try:
            global qwen_tts_realtime
            type = response['type']
            if 'session.created' == type:
                print('start session: {}'.format(response['session']['id']))
            if 'response.audio.delta' == type:
                recv_audio_b64 = response['delta']
                self.file.write(base64.b64decode(recv_audio_b64))
            if 'response.done' == type:
                print(f'response {qwen_tts_realtime.get_last_response_id()} done')
                self.complete_event.set()
                self.file.close()
            if 'session.finished' == type:
                print('session finished')
                self.complete_event.set()
        except Exception as e:
            print('[Error] {}'.format(e))
            return

    def wait_for_response_done(self):
        self.complete_event.wait()

if __name__  == '__main__':
    init_dashscope_api_key()

    print('Initializing ...')

    callback = MyCallback()

    qwen_tts_realtime = QwenTtsRealtime(
        # 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash-realtime
        model='qwen3-tts-flash-realtime',
        callback=callback,
        # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
        )

    qwen_tts_realtime.connect()
    qwen_tts_realtime.update_session(
        voice = 'Cherry',
        response_format = AudioFormat.PCM_24000HZ_MONO_16BIT,
        # 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash-realtime
        # instructions='语速较快，带有明显的上扬语调，适合介绍时尚产品。',
        # optimize_instructions=True,
        mode = 'commit'        
    )
    print(f'send text: {text_to_synthesize[0]}')
    qwen_tts_realtime.append_text(text_to_synthesize[0])
    qwen_tts_realtime.commit()
    callback.wait_for_response_done()
    callback.reset_event()
    
    print(f'send text: {text_to_synthesize[1]}')
    qwen_tts_realtime.append_text(text_to_synthesize[1])
    qwen_tts_realtime.commit()
    callback.wait_for_response_done()
    callback.reset_event()

    print(f'send text: {text_to_synthesize[2]}')
    qwen_tts_realtime.append_text(text_to_synthesize[2])
    qwen_tts_realtime.commit()
    callback.wait_for_response_done()
    
    qwen_tts_realtime.finish()
    print('[Metric] session: {}, first audio delay: {}'.format(
                    qwen_tts_realtime.get_session_id(), 
                    qwen_tts_realtime.get_first_audio_delay(),
                    ))
```

访问[github](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)下载更多示例代码。

## **请求参数**

下述请求参数可以通过QwenTtsRealtime的构造方法进行设置。

**参数**

**类型**

**是否必须**

**说明**

model

str

是

模型名称。参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#d2ad2470a394c)。

url

str

是

中国内地：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`

国际：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime`

下述请求参数可以通过update\_session接口配置。

**参数**

**类型**

**是否必须**

**说明**

voice

str

是

语音合成所使用的音色。参见[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#bac280ddf5a1u)。

支持系统音色和专属音色：

-   **系统音色**：仅限千问3-TTS-Instruct-Flash-Realtime、千问3-TTS-Flash-Realtime和千问-TTS-Realtime系列模型。音色效果请参见：[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#bac280ddf5a1u)。
    
-   **专属音色**
    
    -   [声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)功能定制的音色：仅限千问3-TTS-VC-Realtime系列模型
        
    -   [声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)功能定制的音色：仅限千问3-TTS-VD-Realtime系列模型
        

language\_type

str

否

指定合成音频的语种，默认为 `Auto`。

-   `Auto`：适用无法确定文本的语种或文本包含多种语言的场景，模型会自动为文本中的不同语言片段匹配各自的发音，但无法保证发音完全精准。
    
-   指定语种：适用于文本为单一语种的场景，此时指定为具体语种，能显著提升合成质量，效果通常优于 `Auto`。可选值包括：
    
    -   `Chinese`
        
    -   `English`
        
    -   `German`
        
    -   `Italian`
        
    -   `Portuguese`
        
    -   `Spanish`
        
    -   `Japanese`
        
    -   `Korean`
        
    -   `French`
        
    -   `Russian`
        

mode

str

否

交互模式，可选值：

-   `server_commit`（默认）：服务端自动判断合成时机，平衡延迟与质量，推荐大多数场景使用
    
-   `commit`：客户端手动触发合成，延迟最低，但需自行管理句子完整性
    

format

str

否

模型输出音频的格式。

支持的格式：

-   `pcm`（默认）
    
-   `wav`
    
-   `mp3`
    
-   `opus`
    

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）仅支持`pcm`。

sample\_rate

int

否

模型输出音频的采样率（Hz）。

支持的采样率：

-   8000
    
-   16000
    
-   24000（默认）
    
-   48000
    

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）仅支持24000。

speech\_rate

float

否

音频的语速。1.0为正常语速，小于1.0为慢速，大于1.0为快速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

volume

int

否

音频的音量。

默认值：50。

取值范围：\[0, 100\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

pitch\_rate

float

否

合成音频的语调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

bit\_rate

int

否

指定音频的[码率](https://opus-codec.org/)（kbps）。码率越大，音质越好，音频文件体积越大。仅在音频格式（`response_format`）为`opus`时可用。

默认值：128。

取值范围：\[6, 510\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

instructions

str

否

设置指令，参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

默认值：无默认值，不设置不生效。

长度限制：长度不得超过 1600 Token。

支持语言：仅支持中文和英文。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash-Realtime系列模型。

optimize\_instructions

bool

否

是否对 `instructions` 进行优化，以提升语音合成的自然度和表现力。

默认值：False

行为说明：当设置为 True 时，系统将对 `instructions` 的内容进行语义增强与重写，生成更适合语音合成的内部指令。

适用场景：推荐在追求高品质、精细化语音表达的场景下开启。

依赖关系：此参数依赖于 `instructions` 参数被设置。如果 `instructions` 为空，此参数不生效。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash-Realtime系列模型。

## **关键接口**

### **QwenTtsRealtime类**

QwenTtsRealtime通过`from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime`方法引入。

方法签名

服务端响应事件（通过回调下发）

说明

```
def connect(self) -> None
```

[session.created](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#05bb97c283l2n)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#58f078ab61di5)

> 会话配置已更新

和服务端创建连接。

```
def update_session(self,
                       voice: str,
                       response_format: AudioFormat = AudioFormat.
                       PCM_24000HZ_MONO_16BIT,
                       mode: str = 'server_commit',
                       language_type : str = "Chinese",
                       **kwargs) -> None
```

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#58f078ab61di5)

> 会话配置已更新

更新本次会话交互的默认配置。参数配置请参考《请求参数》章节。

在您建立链接，服务端会及时返回用于此会话的默认输出输入配置。如果您需要更新默认会话配置，我们也推荐您总是在建立链接后即刻调用此接口。

服务端在收到session.update事件后，会进行参数校验，如果参数不合法则返回错误，否则更新服务端侧的会话配置。

```
def append_text(self, text: str) -> None
```

无

将文本片段追加到云端输入文本缓冲区。 缓冲区是你可以写入并稍后提交的临时存储。

-   "server\_commit"模式下，服务器决定何时提交并合成文本缓冲区中的文本。
    
-   "commit"模式下，客户端需要主动通过commit触发语音合成。
    

```
def clear_appended_text(self, ) -> None
```

[input\_text\_buffer.cleared](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#7a04edb8840o7)

> 清空服务端收到的文本

删除当前云端缓冲区的文本。

```
def commit(self, ) -> None
```

[input\_text\_buffer.committed](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#76abc25665qt8)

> 提交文本并触发语音合成

[response.output\_item.added](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#efd58c096b3bv)

> 响应时有新的输出内容

[response.content\_part.added](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#141bec9bb11yi)

> 新的输出内容添加到assistant message 项

[response.audio.delta](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#a2b95643bdvnl)

> 模型增量生成的音频

[response.audio.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#faa3f9bc106tj)

> 完成音频生成

[response.content\_part.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#5244e1dbc9vw6)

> Assistant message 的音频内容流式输出完成

[response.output\_item.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#a922404106vzd)

> Assistant message 的整个输出项流式传输完成

[response.done](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#91f767e7440pc)

> 响应完成

提交之前通过append添加到云端缓冲区的文本，并立刻合成所有文本。如果输入的文本缓冲区为空将产生错误。

-   "server\_commit"模式下，客户端不需要发送此事件，服务器会自动提交文本缓冲区。
    
-   "commit"模式下，客户端必须通过commit触发语音合成。
    

```
def finish(self, ) -> None
```

[session.finished](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#ac332f7d78oxg)

> 响应完成

终止任务。

```
def close(self, ) -> None
```

无

关闭连接。

```
def get_session_id(self) -> str
```

无

获取当前任务的session\_id。

```
def get_last_response_id(self) -> str
```

无

获取最近一次response的response\_id。

```
def get_first_audio_delay(self)
```

无

获取首包音频延迟。

### **回调接口（**QwenTtsRealtimeCallback**）**

服务端会通过回调的方式，将服务端响应事件和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

通过`from dashscope.audio.qwen_tts_realtime import QwenTtsRealtimeCallback`引入。

方法

参数

返回值

描述

```
def on_open(self) -> None
```

无

无

当和服务端建立连接完成后，该方法立刻被回调。

```
def on_event(self, message: str) -> None
```

message：服务端响应事件。

无

包括对接口调用的回复响应和模型生成的文本和音频。具体可以参考：[服务端事件](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events)

```
def on_close(self, close_status_code, close_msg) -> None
```

close\_status\_code：关闭WebSocket的状态码。

close\_msg：关闭WebSocket的关闭信息。

无

当服务已经关闭连接后进行回调。
