# Qwen-TTS-Realtime Python SDK

通过 WebSocket 使用 DashScope Python SDK 调用 Qwen-TTS-Realtime。

<a id="model-qwen-tts-realtime"></a>

本文介绍 DashScope Python SDK 调用 Qwen-TTS-Realtime 系列模型时的关键接口与请求参数。

<a id="前提条件"></a>

<a id="model-qwen-tts-realtime-8779ce97deiou"></a>

<a id="前期准备"></a>

## 前提条件

DashScope Python SDK 版本需要不低于2.0.1。

<a id="快速开始"></a>

<a id="model-qwen-tts-realtime-3dc1a29b077gt"></a>

## 快速开始

<a id="fig-code-group"></a>

<a id="fig-code-group-server-commit模式-tab"></a>

server commit模式

<a id="code-code-group-server-commit模式"></a>

```python
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
            model='qwen3-tts-flash-realtime',
    ) as session:
        session.update_session(
            output_modalities=['audio'],
            voice='Cherry',
            response_format='pcm',
            sample_rate=24000,
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

<a id="fig-code-group-commit模式-tab"></a>

commit模式

<a id="code-code-group-commit模式"></a>

```python
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
            model='qwen3-tts-flash-realtime',
    ) as session:
        session.update_session(
            output_modalities=['audio'],
            voice='Cherry',
            response_format='pcm',
            sample_rate=24000,
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

<a id="请求参数"></a>

<a id="model-qwen-tts-realtime-0ce39f0139nb1"></a>

## 请求参数

下述请求参数可以通过`client.audio.realtime`的`connect`方法设置。

| 参数 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| model | str | 是 | 模型名称。参见[支持的模型](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#4a43cc1bb7kxg)。 |
| ws\_url | str | 否 | 会话端点。缺省时由[Client](../model-api-reference/preparations/install-sdk.md)构造参数`workspace`/`region`自动推导（华北2（北京）地域：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`；新加坡地域：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`）。 |

下述请求参数可以通过会话的`update_session`方法配置（具名参数直接传入，其余参数透传至session.update事件的session对象）。

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>voice</p></td><td><p>str</p></td><td><p>是</p></td><td><p>语音合成所使用的音色。参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-tts-voice-list.md">Qwen-TTS音色列表</a>。</p></td></tr><tr><td><p>language_type</p></td><td><p>str</p></td><td><p>否</p></td><td><div><p>指定合成音频的语种，默认为 <code>Auto</code>。</p><ul><li><p><code>Auto</code>：适用无法确定文本的语种或文本包含多种语言的场景，模型会自动为文本中的不同语言片段匹配各自的发音，但无法保证发音完全精准。</p></li><li><p>指定语种：适用于文本为单一语种的场景，此时指定为具体语种，能显著提升合成质量，效果通常优于 <code>Auto</code>。可选值包括：</p><ul><li><p><code>Chinese</code></p></li><li><p><code>English</code></p></li><li><p><code>German</code></p></li><li><p><code>Italian</code></p></li><li><p><code>Portuguese</code></p></li><li><p><code>Spanish</code></p></li><li><p><code>Japanese</code></p></li><li><p><code>Korean</code></p></li><li><p><code>French</code></p></li><li><p><code>Russian</code></p></li></ul></li></ul></div></td></tr><tr><td><p>mode</p></td><td><p>str</p></td><td><p>否</p></td><td><div><p>交互模式，可选值：</p><ul><li><p><code>server_commit</code>（默认）：服务端自动判断合成时机，平衡延迟与质量，推荐大多数场景使用</p></li><li><p><code>commit</code>：客户端手动触发合成，延迟最低，但需自行管理句子完整性</p></li></ul></div></td></tr><tr><td><p>response_format</p></td><td><p>str</p></td><td><p>否</p></td><td><div><p>模型输出音频的格式。</p><p>支持的格式：</p><ul><li><p><code>pcm</code>（默认）</p></li><li><p><code>wav</code></p></li><li><p><code>mp3</code></p></li><li><p><code>opus</code></p></li></ul></div></td></tr><tr><td><p>sample_rate</p></td><td><p>int</p></td><td><p>否</p></td><td><div><p>模型输出音频的采样率（Hz）。</p><p>支持的采样率：</p><ul><li><p>8000</p></li><li><p>16000</p></li><li><p>24000（默认）</p></li><li><p>48000</p></li></ul></div></td></tr><tr><td><p>speech_rate</p></td><td><p>float</p></td><td><p>否</p></td><td><div><p>音频的语速。1.0为正常语速，小于1.0为慢速，大于1.0为快速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p>volume</p></td><td><p>int</p></td><td><p>否</p></td><td><div><p>音频的音量。</p><p>取值范围：[0, 100]。</p></div></td></tr><tr><td><p>pitch_rate</p></td><td><p>float</p></td><td><p>否</p></td><td><div><p>合成音频的语调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p>bit_rate</p></td><td><p>int</p></td><td><p>否</p></td><td><div><p>指定音频的<a href="https://opus-codec.org/">码率</a>（kbps）。码率越大，音质越好，音频文件体积越大。仅在音频格式（<code>response_format</code>）为<code>opus</code>时可用。</p><p>默认值：128。</p><p>取值范围：[6, 510]。</p></div></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="model-qwen-tts-realtime-08096516dauq0"></a>

<a id="关键接口"></a>

## 接口参考

<a id="会话-realtimesession"></a>

<a id="model-qwen-tts-realtime-4c4810ff87ofz"></a>

### 会话（RealtimeSession）

实时语音合成会话通过`client.audio.realtime.connect(model=...)`创建，进入`with`上下文时自动建立连接（也可调用会话的`connect()`方法手动建立）。

<table><thead><tr><th><p>方法签名</p></th><th><p>服务端响应事件（通过<code>events()</code>迭代下发）</p></th><th><p>说明</p></th></tr></thead><tbody><tr><td><a id="code-block"></a><pre class="language-python"><code>def connect(self) -&gt; &quot;RealtimeSession&quot;
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#05bb97c283l2n">session.created</a></p><blockquote><p>会话已创建</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#58f078ab61di5">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>和服务端创建连接。进入<code>with</code>上下文时自动调用。</p></td></tr><tr><td><a id="code-block-2"></a><pre class="language-python"><code>def update_session(self,
                   output_modalities: List[str],
                   *,
                   voice: str = None,
                   **kwargs) -&gt; None
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#58f078ab61di5">session.updated</a></p><blockquote><p>会话配置已更新</p></blockquote></td><td><p>更新本次会话交互的默认配置。参数配置请参考《请求参数》章节。</p><p>在您建立链接，服务端会及时返回用于此会话的默认输出输入配置。如果您需要更新默认会话配置，我们也推荐您总是在建立链接后即刻调用此接口。</p><p>服务端在收到session.update事件后，会进行参数校验，如果参数不合法则返回错误，否则更新服务端侧的会话配置。</p></td></tr><tr><td><a id="code-block-3"></a><pre class="language-python"><code>def send_event(self,
               event: Dict[str, Any]) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>发送原始事件。文本输入通过<code>input_text_buffer</code>系列事件完成：将文本片段追加到云端输入文本缓冲区（<code>{&quot;type&quot;: &quot;input_text_buffer.append&quot;, &quot;text&quot;: ...}</code>）。缓冲区是你可以写入并稍后提交的临时存储。</p><ul><li>&quot;server_commit&quot;模式下，服务器决定何时提交并合成文本缓冲区中的文本。</li><li>&quot;commit&quot;模式下，客户端需要主动发送<code>input_text_buffer.commit</code>事件触发语音合成。</li></ul></td></tr><tr><td><a id="code-block-4"></a><pre class="language-python"><code>def send_event(self,
               event: Dict[str, Any]) -&gt; None
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#7a04edb8840o7">input_text_buffer.cleared</a></p><blockquote><p>清空服务端收到的文本</p></blockquote></td><td><p>发送<code>{&quot;type&quot;: &quot;input_text_buffer.clear&quot;}</code>事件，删除当前云端缓冲区的文本。</p></td></tr><tr><td><a id="code-block-5"></a><pre class="language-python"><code>def send_event(self,
               event: Dict[str, Any]) -&gt; None
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#76abc25665qt8">input_text_buffer.committed</a></p><blockquote><p>提交文本并触发语音合成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#efd58c096b3bv">response.output_item.added</a></p><blockquote><p>响应时有新的输出内容</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#141bec9bb11yi">response.content_part.added</a></p><blockquote><p>新的输出内容添加到assistant message 项</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#a2b95643bdvnl">response.audio.delta</a></p><blockquote><p>模型增量生成的音频</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#faa3f9bc106tj">response.audio.done</a></p><blockquote><p>完成音频生成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#5244e1dbc9vw6">response.content_part.done</a></p><blockquote><p>Assistant message 的音频内容流式输出完成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#a922404106vzd">response.output_item.done</a></p><blockquote><p>Assistant message 的整个输出项流式传输完成</p></blockquote><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#91f767e7440pc">response.done</a></p><blockquote><p>响应完成</p></blockquote></td><td><p>发送<code>{&quot;type&quot;: &quot;input_text_buffer.commit&quot;}</code>事件，提交之前通过append添加到云端缓冲区的文本，并立刻合成所有文本。如果输入的文本缓冲区为空将产生错误。</p><ul><li>&quot;server_commit&quot;模式下，客户端不需要发送此事件，服务器会自动提交文本缓冲区。</li><li>&quot;commit&quot;模式下，客户端必须通过commit触发语音合成。</li></ul></td></tr><tr><td><a id="code-block-6"></a><pre class="language-python"><code>def end_session(self) -&gt; None
</code></pre></td><td><p><a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md#ac332f7d78oxg">session.finished</a></p><blockquote><p>响应完成</p></blockquote></td><td><p>发送session.finish事件，终止任务。之后继续消费<code>events()</code>直到<code>session.finished</code>事件。</p></td></tr><tr><td><a id="code-block-7"></a><pre class="language-python"><code>def close(self, ) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>关闭连接。退出<code>with</code>上下文时自动调用。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-python"><code>session.session_id
</code></pre></td><td><p>无</p></td><td><p>获取当前任务的session_id。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-python"><code>session.last_response_id
</code></pre></td><td><p>无</p></td><td><p>获取最近一次response的response_id。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-python"><code>session.last_first_audio_delay
</code></pre></td><td><p>无</p></td><td><p>获取首包音频延迟。</p></td></tr></tbody></table>

<a id="事件迭代-events"></a>

<a id="model-qwen-tts-realtime-9d08669109iwx"></a>

### 事件迭代（`events()`）

服务端会通过事件的方式，将服务端响应事件和数据返回给客户端。在接收线程中迭代会话的`events()`处理服务端事件，`session.finished`事件后迭代结束；`error`事件会以`DashScopeError`异常抛出，可使用try/except捕获。

<table><thead><tr><th><p>方法</p></th><th><p>参数</p></th><th><p>返回值</p></th><th><p>描述</p></th></tr></thead><tbody><tr><td><a id="code-block-11"></a><pre class="language-python"><code>def events(self) -&gt; Iterator[Dict]
</code></pre></td><td><p>event：服务端响应事件（<code>dict</code>）。</p></td><td><p>迭代器</p></td><td><p>包括对接口调用的回复响应和模型生成的文本和音频，<code>session.finished</code>事件后迭代结束。具体可以参考：<a href="qwen-tts-realtime-server-events-a0bed3a00638ceea.md">服务端事件</a></p></td></tr><tr><td><a id="code-block-12"></a><pre class="language-python"><code>def recv_event(self) -&gt; Optional[Dict]
</code></pre></td><td><p>event：服务端响应事件（<code>dict</code>）。</p></td><td><p>事件或<code>None</code></p></td><td><p>读取一条服务端事件，正常关闭后返回<code>None</code>。</p></td></tr></tbody></table>
