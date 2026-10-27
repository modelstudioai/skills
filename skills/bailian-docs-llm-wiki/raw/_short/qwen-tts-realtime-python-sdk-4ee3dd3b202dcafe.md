# Python SDK

本文介绍 DashScope Python SDK 调用[实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)时的关键接口与请求参数。

**用户指南**：关于模型介绍和选型建议请参见[实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)或[非实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/non-realtime-tts-user-guide.md)。

## 前期准备

DashScope Python SDK 版本需要不低于2.0.1。

## 快速开始

server commit模式

```
import os
import base64
import time
from concurrent.futures import ThreadPoolExecutor

import dashscope

text_to_synthesize = [
    '对吧~我就特别喜欢这种超市，',
    '尤其是过年的时候',
    '去逛超市',
    '就会觉得',
    '超级超级开心！',
    '想买好多好多的东西呢！'
]

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 接收线程：迭代服务端事件，音频增量写入文件
def receive_events(session):
    with open('result_24k.pcm', 'wb') as f:
        for event in session.events():
            event_type = event.get('type')
            if event_type == 'session.created':
                print('start session: {}'.format(event['session']['id']))
            elif event_type == 'response.audio.delta':
                f.write(base64.b64decode(event['delta']))
            elif event_type == 'response.done':
                print(f'response {session.last_response_id} done')
            elif event_type == 'session.finished':
                print('session finished')

if __name__  == '__main__':
    print('Initializing ...')

    # 创建实时语音合成会话：进入 with 上下文时自动建立连接
    with client.audio.realtime.connect(
            # 如需使用指令控制功能，请将model替换为qwen3.5-omni-plus-realtime
            model='qwen3-tts-flash-realtime',
    ) as session:
        session.update_session(
            output_modalities=['audio'],
            voice='Cherry',
            format='pcm',
            sample_rate=24000,
            # 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3.5-omni-plus-realtime
            # instructions='语速较快，带有明显的上扬语调，适合介绍时尚产品。',
            # optimize_instructions=True,
            mode='server_commit'
        )
        with ThreadPoolExecutor(max_workers=1) as pool:
            receiver = pool.submit(receive_events, session)
            for text_chunk in text_to_synthesize:
                print(f'send text: {text_chunk}')
                session.send_event({'type': 'input_text_buffer.append', 'text': text_chunk})
                time.sleep(0.1)
            # 通知服务端输入结束（server_commit 模式下服务端自动判断合成时机）
            session.end_session()
            receiver.result()
        print('[Metric] session: {}, first audio delay: {}'.format(
            session.session_id,
            session.last_first_audio_delay,
        ))
```

commit模式

```
import os
import base64
import time
from concurrent.futures import ThreadPoolExecutor

import dashscope

text_to_synthesize = [
    '这是第一句话。',
    '这是第二句话。',
    '这是第三句话。',
]

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 接收线程：迭代服务端事件，音频增量写入文件
def receive_events(session):
    with open('result_24k.pcm', 'wb') as f:
        for event in session.events():
            event_type = event.get('type')
            if event_type == 'session.created':
                print('start session: {}'.format(event['session']['id']))
            elif event_type == 'response.audio.delta':
                f.write(base64.b64decode(event['delta']))
            elif event_type == 'response.done':
                print(f'response {session.last_response_id} done')
            elif event_type == 'session.finished':
                print('session finished')

if __name__  == '__main__':
    print('Initializing ...')

    # 创建实时语音合成会话：进入 with 上下文时自动建立连接
    with client.audio.realtime.connect(
            # 如需使用指令控制功能，请将model替换为qwen3.5-omni-plus-realtime
            model='qwen3-tts-flash-realtime',
    ) as session:
        session.update_session(
            output_modalities=['audio'],
            voice='Cherry',
            format='pcm',
            sample_rate=24000,
            # 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3.5-omni-plus-realtime
            # instructions='语速较快，带有明显的上扬语调，适合介绍时尚产品。',
            # optimize_instructions=True,
            mode='commit'
        )
        with ThreadPoolExecutor(max_workers=1) as pool:
            receiver = pool.submit(receive_events, session)
            for text in text_to_synthesize:
                print(f'send text: {text}')
                session.send_event({'type': 'input_text_buffer.append', 'text': text})
                # commit 模式下由客户端主动触发合成
                session.send_event({'type': 'input_text_buffer.commit'})
                time.sleep(0.1)
            session.end_session()
            receiver.result()
        print('[Metric] session: {}, first audio delay: {}'.format(
            session.session_id,
            session.last_first_audio_delay,
        ))
```

访问[github](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)下载更多示例代码。

## 请求参数

下述请求参数可以通过`client.audio.realtime`的`connect`方法设置。

**参数**

**类型**

**是否必须**

**说明**

model

str

是

模型名称。参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#4a43cc1bb7kxg)。

ws\_url

str

否

会话端点。缺省时由[Client](raw/model-api-reference/preparations/install-sdk.md)构造参数`workspace`/`region`自动推导（华北2（北京）地域：`wss//{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`；新加坡地域：`wss//{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`）。

下述请求参数可以通过会话的`update_session`方法配置（具名参数直接传入，其余参数透传至session.update事件的session对象）。

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

指定合成音频的语种，默认为 `Auto`。

-   `Auto`：适用无法确定文本的语种或文本包含多种语言的场景，模型会自动为文本中的不同语言片段匹配各自的发音，但无法保证发音完全精准。
    
-   指定语种：适用于文本为单一语种的场景，此时指定为具体语种，能显著提升合成质量，效果通常优于 `Auto`。可选值包括：
    
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
    

千问-TTS-Realtime（参见[支持的模型](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)）仅支持`pcm`。

sample\_rate

int

否

模型输出音频的采样率（Hz）。

支持的采样率：

-   8000
    
-   16000
    
-   24000（默认）
    
-   48000
    

千问-TTS-Realtime（参见[支持的模型](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)）仅支持24000。

speech\_rate

float

否

音频的语速。1.0为正常语速，小于1.0为慢速，大于1.0为快速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)）不支持该参数。

volume

int

否

音频的音量。

默认值：50。

取值范围：\[0, 100\]。

千问-TTS-Realtime（参见[支持的模型](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)）不支持该参数。

pitch\_rate

float

否

合成音频的语调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)）不支持该参数。

bit\_rate

int

否

指定音频的[码率](https://opus-codec.org/)（kbps）。码率越大，音质越好，音频文件体积越大。仅在音频格式（`response_format`）为`opus`时可用。

默认值：128。

取值范围：\[6, 510\]。

千问-TTS-Realtime（参见[支持的模型](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)）不支持该参数。

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

## 关键接口

### 会话（RealtimeSession）

实时语音合成会话通过`client.audio.realtime.connect(model=...)`创建，进入`with`上下文时自动建立连接（也可调用会话的`connect()`方法手动建立）。

方法签名

服务端响应事件（通过`events()`迭代下发）

说明

```
def connect(self) -> "RealtimeSession"
```

[session.created](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#05bb97c283l2n)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#58f078ab61di5)

> 会话配置已更新

和服务端创建连接。进入`with`上下文时自动调用。

```
def update_session(self,
                   output_modalities: List[str],
                   *,
                   voice: str = None,
                   input_audio_transcription_model: str = None,
                   **kwargs) -> None
```

[session.updated](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#58f078ab61di5)

> 会话配置已更新

更新本次会话交互的默认配置。参数配置请参考《请求参数》章节。

在您建立链接，服务端会及时返回用于此会话的默认输出输入配置。如果您需要更新默认会话配置，我们也推荐您总是在建立链接后即刻调用此接口。

服务端在收到session.update事件后，会进行参数校验，如果参数不合法则返回错误，否则更新服务端侧的会话配置。

```
def send_event(self,
               event: Dict[str, Any]) -> None
```

无

发送原始事件。文本输入通过`input_text_buffer`系列事件完成：将文本片段追加到云端输入文本缓冲区（`{"type": "input_text_buffer.append", "text": ...}`）。缓冲区是你可以写入并稍后提交的临时存储。

-   "server\_commit"模式下，服务器决定何时提交并合成文本缓冲区中的文本。
-   "commit"模式下，客户端需要主动发送`input_text_buffer.commit`事件触发语音合成。

```
def send_event(self,
               event: Dict[str, Any]) -> None
```

[input\_text\_buffer.cleared](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#7a04edb8840o7)

> 清空服务端收到的文本

发送`{"type": "input_text_buffer.clear"}`事件，删除当前云端缓冲区的文本。

```
def send_event(self,
               event: Dict[str, Any]) -> None
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

发送`{"type": "input_text_buffer.commit"}`事件，提交之前通过append添加到云端缓冲区的文本，并立刻合成所有文本。如果输入的文本缓冲区为空将产生错误。

-   "server\_commit"模式下，客户端不需要发送此事件，服务器会自动提交文本缓冲区。
-   "commit"模式下，客户端必须通过commit触发语音合成。

```
def end_session(self) -> None
```

[session.finished](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#ac332f7d78oxg)

> 响应完成

发送session.finish事件，终止任务。之后继续消费`events()`直到`session.finished`事件。

```
def close(self, ) -> None
```

无

关闭连接。退出`with`上下文时自动调用。

```
session.session_id
```

无

获取当前任务的session\_id。

```
session.last_response_id
```

无

获取最近一次response的response\_id。

```
session.last_first_audio_delay
```

无

获取首包音频延迟。

### 事件迭代（`events()`）

服务端会通过事件的方式，将服务端响应事件和数据返回给客户端。在接收线程中迭代会话的`events()`处理服务端事件，`session.finished`事件后迭代结束；`error`事件会以`DashScopeError`异常抛出，可使用try/except捕获。

方法

参数

返回值

描述

```
def events(self) -> Iterator[Dict]
```

event：服务端响应事件（`dict`）。

迭代器

包括对接口调用的回复响应和模型生成的文本和音频，`session.finished`事件后迭代结束。具体可以参考：[服务端事件](raw/_short/qwen-tts-realtime-server-events-8ed037c725703737.md)

```
def recv_event(self) -> Optional[Dict]
```

event：服务端响应事件（`dict`）。

事件或`None`

读取一条服务端事件，正常关闭后返回`None`。
