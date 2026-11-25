# Qwen-Audio-TTS Python SDK

使用 CosyVoice 时，请参见 [CosyVoice Python SDK](cosyvoice-websocket-sdk-python-47e109e34183e539.md)。

<a id="tts-sdk"></a>

Qwen-Audio-TTS 和 CosyVoice 均通过 `client.audio.tts` 合成语音，支持一次性合成、流式输出和双向流式会话。选择模型后，按该模型的要求设置音色和其他参数。

<a id="前提条件"></a>

## 前提条件

-   [安装 Python SDK](../model-api-reference/preparations/install-sdk.md)
-   [获取并配置 API Key](../model-api-reference/preparations/get-api-key.md)

<a id="接口地址"></a>

<a id="model-qwen-audio-tts-h2-1d8e4c7f"></a>

<a id="model-cosyvoice-h2-1d8e4c7f"></a>

### 接口地址

SDK的接口地址由Client构造参数`workspace`/`region`决定（对应下方地址，包含WorkspaceId）。如需切换到其他地域，请修改Client构造参数为对应地域的值。

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

## 快速开始

示例使用北京。将代码中的 `{WorkspaceId}` 替换为实际的[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。运行后，音频保存到当前目录的 `output.mp3`。

<a id="code-block"></a>

```python
# coding=utf-8

import os

import dashscope

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

# 发送待合成文本，获取二进制音频
audio = client.audio.tts.synthesize("今天天气怎么样？", model=model, voice=voice)

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

<a id="qwen-audio-tts"></a>

<a id="model-qwen-audio-tts-8e498a23461om"></a>

<a id="示例代码"></a>

<a id="tts-code-examples"></a>

### Qwen-Audio-TTS

SDK提供了语音合成的关键接口，支持以下几种调用方式：

-   非流式调用：阻塞式，一次性发送完整文本，直接返回完整音频。适合短文本语音合成场景。
-   单向流式调用：非阻塞式，一次性发送完整文本，通过迭代`stream`返回的音频分片接收数据。适用于对实时性要求高的短文本语音合成场景。
-   双向流式调用：非阻塞式，可分多次发送文本片段，通过会话的`audio_chunks()`/`events()`迭代实时接收增量合成的音频流。适合实时性要求高的长文本语音合成场景。

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

<a id="sec-tabs-2"></a>

<a id="非流式调用"></a>

<a id="非流式调用-h4"></a>

#### 非流式调用

<a id="model-qwen-audio-tts-8341058094tc3"></a>

调用 `client.audio.tts.synthesize()` 一次发送完整文本，等待服务端完成合成。方法返回包含完整音频的 `bytes`。

单次调用发送的文本长度不得超过20000字符，超出限制将返回错误。

> **重要**
>
> `synthesize`与`stream`每次调用自建会话，无需复用实例。

<a id="code-block-2"></a>

```python
# coding=utf-8

import os

import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

# 发送待合成文本，获取二进制音频
audio = client.audio.tts.synthesize("今天天气怎么样？", model=model, voice=voice)

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

<a id="sec-tabs-3"></a>

<a id="dashscope-cli"></a>

<a id="dashscope-cli-h4"></a>

#### dashscope CLI

<a id="code-block-3"></a>

```bash
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope speech-synthesis create -m qwen-audio-3.0-tts-flash -t "你好世界" --voice longanhuan_v3.6
```

> **重要**
>
> SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见
>
> [DashScope SDK Expert](../model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](../model-api-reference/preparations/base-url.md)。

<a id="单向流式调用"></a>

<a id="单向流式调用-h4"></a>

#### 单向流式调用

<a id="model-qwen-audio-tts-cc2a504f344s2"></a>

将完整文本一次传给 `client.audio.tts.stream()`，迭代返回值，按顺序读取音频分片。服务端完成合成后，迭代结束。

单次调用发送的文本长度不得超过20000字符，超出限制将返回错误。

> **重要**
>
> `synthesize`与`stream`每次调用自建会话，无需复用实例。

<a id="code-block-4"></a>

```python
# coding=utf-8

import os

from datetime import datetime

import dashscope

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

# 一次性发送待合成文本，逐块接收二进制音频
with open("output.mp3", "wb") as f:
    for chunk in client.audio.tts.stream("今天天气怎么样？", model=model, voice=voice):
        print(get_timestamp() + " 二进制音频长度为：" + str(len(chunk)))
        f.write(chunk)
print("语音合成完成，所有合成结果已被接收：" + get_timestamp())
```

<a id="双向流式调用"></a>

<a id="双向流式调用-h4"></a>

#### 双向流式调用

<a id="model-qwen-audio-tts-ba023aacfbr84"></a>

用 `client.audio.tts.connect()` 建立会话。分次调用 `session.send_text()` 发送文本，同时通过 `session.audio_chunks()` 接收音频，或通过 `session.events()` 接收事件。需要立即合成已缓冲的文本时，可调用 `session.flush()`，之后仍可继续输入。

发送完毕后调用 `session.stop()`，继续读取剩余音频。服务端返回 `task-finished` 后迭代结束；退出 `with` 块时会话关闭。合成失败时，SDK 抛出 `DashScopeError` 并关闭连接。

单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

-   流式输入时可多次调用会话的`send_text`按顺序提交文本片段。服务端接收文本片段后自动进行分句：
    
    -   完整语句立即合成
    -   不完整语句缓存至完整后合成
    
    调用 `stop` 时，服务端会强制合成所有已接收但未处理的文本片段（包括未完成的句子）。
    
-   发送文本片段的间隔不得超过23秒，否则触发“request timeout after 23 seconds”异常。
    
    若无待发送文本，需及时调用 `stop`结束任务。
    
    > **重要**
    >
    > 请务必确保调用`stop`方法，否则可能会导致结尾部分的文本无法成功转换为语音。
    
    > 服务端强制设定23秒超时机制，客户端无法修改该配置。
    

<a id="code-block-5"></a>

```python
# coding=utf-8
#
# pyaudio安装说明：
# 如果是macOS操作系统，执行如下命令：
#   brew install portaudio
#   pip install pyaudio
# 如果是Debian/Ubuntu操作系统，执行如下命令：
#   sudo apt-get install python-pyaudio python3-pyaudio
#   或者
#   pip install pyaudio
# 如果是CentOS操作系统，执行如下命令：
#   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
# 如果是Microsoft Windows，执行如下命令：
#   python -m pip install pyaudio

import os
import time
import pyaudio
from concurrent.futures import ThreadPoolExecutor

import dashscope

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 模型
model = "qwen-audio-3.0-tts-flash"
# 音色
voice = "longanhuan_v3.6"

test_text = [
    "流式文本语音合成SDK，",
    "可以将输入的文本",
    "合成为语音二进制数据，",
    "相比于非流式语音合成，",
    "流式合成的优势在于实时性",
    "更强。用户在输入文本的同时",
    "可以听到接近同步的语音输出，",
    "极大地提升了交互体验，",
    "减少了用户等待时间。",
    "适用于调用大规模",
    "语言模型（LLM），以",
    "流式输入文本的方式",
    "进行语音合成的场景。",
]

# 创建双向流式合成会话：进入 with 上下文时自动建立连接
with client.audio.tts.connect(
        model=model,
        voice=voice,
        format="pcm",
        sample_rate=22050,
) as session:
    # 初始化播放器
    player = pyaudio.PyAudio()
    stream = player.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)

    # 接收线程：迭代音频数据，实时播放
    def receive_audio():
        for chunk in session.audio_chunks():
            print(get_timestamp() + " 二进制音频长度为：" + str(len(chunk)))
            stream.write(chunk)

    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_audio)
        # 流式发送待合成文本
        for text in test_text:
            session.send_text(text)
            time.sleep(0.1)
        # 结束流式语音合成
        session.stop()
        receiver.result()

    print("语音合成完成，所有合成结果已被接收：" + get_timestamp())
    # 停止播放器
    stream.stop_stream()
    stream.close()
    player.terminate()

    # 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
    print('[Metric] 首包延迟为：{}毫秒'.format(session.first_package_delay))
```

<a id="请求参数"></a>

<a id="request-parameters"></a>

## 请求参数

<a id="qwen-audio-tts-2"></a>

<a id="model-qwen-audio-tts-h3-cv-params"></a>

### Qwen-Audio-TTS

以下参数通过`client.audio.tts`的`synthesize`/`stream`/`connect`方法设置，用于控制合成音频的模型、音色、格式和音频特征（`model`、`voice`、`format`、`sample_rate`、`volume`、`rate`、`pitch`、`language_hints`、`enable_ssml`为具名参数，其余参数通过`parameters`字典传入）。

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>model</code></td><td><code>str</code></td><td>是</td><td>模型名称。</td></tr><tr><td><code>voice</code></td><td><code>str</code></td><td>是</td><td>语音合成所使用的音色。<ul><li><strong>系统音色</strong>：参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a></li><li><strong>复刻音色</strong>：通过声音复刻功能定制</li><li><strong>声音设计音色</strong>：通过声音设计功能定制</li></ul></td></tr><tr><td><code>format</code></td><td><code>str</code></td><td>否</td><td>音频编码格式。<p>默认值：mp3。</p><p>支持mp3、wav、pcm等格式；采样率通过<code>sample_rate</code>参数设置，默认22050。</p></td></tr><tr><td><code>volume</code></td><td><code>int</code></td><td>否</td><td>音量。<p>默认值：50。</p><p>取值范围：[0, 100]。</p></td></tr><tr><td><code>rate</code></td><td><code>float</code></td><td>否</td><td>语速。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td><code>pitch</code></td><td><code>float</code></td><td>否</td><td>音调。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td><code>bit_rate</code></td><td><code>int</code></td><td>否</td><td>音频码率（kbps）。音频格式为mp3或opus时，支持通过<code>bit_rate</code>参数调整码率。<p>默认值：32。</p><p>取值范围：[6, 510]。</p><p><code>bit_rate</code>需要通过<code>parameters</code>字典进行设置：</p><a id="code-block-6"></a><pre class="language-python"><code>audio = client.audio.tts.synthesize(
    &quot;待合成文本&quot;,
    model=&quot;qwen-audio-3.0-tts-flash&quot;,
    voice=&quot;longanhuan_v3.6&quot;,
    parameters={&quot;bit_rate&quot;: 128},
)
</code></pre></td></tr><tr><td><code>word_timestamp_enabled</code></td><td><code>bool</code></td><td>否</td><td>是否开启字级别时间戳。<p>默认值：false。</p><p>仅在流式输出模式下可用。支持复刻音色；支持的系统音色请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a>。</p><p><code>word_timestamp_enabled</code>需要通过<code>parameters</code>字典进行设置：</p><a id="code-block-7"></a><pre class="language-python"><code>audio = client.audio.tts.stream(
    &quot;待合成文本&quot;,
    model=&quot;qwen-audio-3.0-tts-flash&quot;,
    voice=&quot;your_voice&quot;,  # 支持字级别时间戳的系统音色或复刻音色
    parameters={&quot;word_timestamp_enabled&quot;: True},
)
</code></pre></td></tr><tr><td><code>seed</code></td><td><code>int</code></td><td>否</td><td>生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。<p>默认值0。</p><p>取值范围：[0, 65535]。</p></td></tr><tr><td><code>language_hints</code></td><td><code>list[str]</code></td><td>否</td><td><div><div><p><strong>说明</strong>使用 qwen-audio-3.1-tts-flash 的多语种与方言音色时，可通过此参数指定语种或方言。具体用法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md#qwen-tts31-language-hints">多语种与方言音色的设置方法</a>。</p></div></div><p>指定语音合成的目标语言，提升合成效果。</p><p>当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：</p><ul><li>数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”</li><li>符号朗读不准确，“@”读成“艾特”而非“at”</li><li>小语种合成效果差，合成不自然</li></ul><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li><p>zh：中文</p></li><li><p>en：英语</p></li><li><p>fr：法语</p></li><li><p>de：德语</p></li><li><p>ja：日语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>pt：葡萄牙语</p></li><li><p>th：泰语</p></li><li><p>id：印尼语</p></li><li><p>vi：越南语</p></li><li><p>es：西班牙语</p></li><li><p>it：意大利语</p></li><li><p>ms：马来语</p></li><li><p>fil：菲律宾语</p></li><li><p>ar：阿拉伯语</p></li><li><p>other：其他语种（适用于 <code>qwen-audio-3.1-tts-flash</code>）</p><p>保加利亚语、荷兰语、匈牙利语、罗马尼亚语、丹麦语、克罗地亚语、希腊语、捷克语、挪威语、瑞典语、印地语、斯洛伐克语、芬兰语、乌尔都语、塞尔维亚语、墨西哥西班牙语、立陶宛语、拉脱维亚语、土耳其语、波斯语、希伯来语、蒙古语、斯洛文尼亚语、阿塞拜疆语、波兰语、加泰罗尼亚语、高棉语、巴西葡萄牙语、老挝语、格鲁吉亚语、南非荷兰语、尼泊尔语、白俄罗斯语、马拉雅拉姆语、卢森堡语、阿尔巴尼亚语、泰米尔语、僧伽罗语、泰卢固语、爱沙尼亚语、宿务语、波斯尼亚语、缅甸语、亚美尼亚语、拉丁语、冰岛语、马耳他语、斯瓦希里语、哈萨克语、塞舌尔克里奥尔语、乌克兰语。</p></li></ul></div></section><div><div><p><strong>说明</strong></p><ul><li>此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。</li><li>此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-create">声音复刻API参考</a>。</li></ul></div></div></td></tr><tr><td><code>instruction</code></td><td><code>str</code></td><td>否</td><td>设置指令，用于控制方言、情感或角色等合成效果。<p>使用说明请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#12884a10929p9">指令控制</a>。</p></td></tr><tr><td><code>enable_aigc_tag</code></td><td><code>bool</code></td><td>否</td><td>是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。<p>默认值：false。</p><p><code>enable_aigc_tag</code>、<code>aigc_propagator</code>和<code>aigc_propagate_id</code>需要通过<code>parameters</code>字典进行设置：</p><a id="code-block-8"></a><pre class="language-python"><code>audio = client.audio.tts.synthesize(
    &quot;待合成文本&quot;,
    model=&quot;qwen-audio-3.0-tts-flash&quot;,
    voice=&quot;longanhuan_v3.6&quot;,
    parameters={
        &quot;enable_aigc_tag&quot;: True,
        &quot;aigc_propagator&quot;: &quot;your_propagator&quot;,
        &quot;aigc_propagate_id&quot;: &quot;your_propagate_id&quot;
    },
)
</code></pre></td></tr><tr><td><code>aigc_propagator</code></td><td><code>str</code></td><td>否</td><td>设置AIGC隐性标识中的 <code>ContentPropagator</code> 字段，用于标识内容的传播者。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。<p>默认值：阿里云UID。</p><p>需要通过<code>parameters</code>字典进行设置，参见<code>enable_aigc_tag</code>的示例。</p></td></tr><tr><td><code>aigc_propagate_id</code></td><td><code>str</code></td><td>否</td><td>设置AIGC隐性标识中的 <code>PropagateID</code> 字段，用于唯一标识一次具体的传播行为。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。<p>默认值：本次语音合成请求Request ID。</p><p>需要通过<code>parameters</code>字典进行设置，参见<code>enable_aigc_tag</code>的示例。</p></td></tr><tr><td><code>hot_fix</code></td><td><code>dict</code></td><td>否</td><td>文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。<p>参数介绍：</p><ul><li>pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。</li><li>replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。</li></ul><p>示例：</p><a id="code-block-9"></a><pre class="language-python"><code>audio = client.audio.tts.synthesize(
    &quot;今天的天气很好。&quot;,
    model=&quot;qwen-audio-3.0-tts-flash&quot;,
    voice=&quot;longanhuan_v3.6&quot;, # 音色
    parameters={
        &quot;hot_fix&quot;: {
            &quot;pronunciation&quot;: [{&quot;天气&quot;: &quot;tian1 qi4&quot;}],
            &quot;replace&quot;: [{&quot;今天&quot;: &quot;明天&quot;}]
        }
    },
)
</code></pre></td></tr><tr><td><p><code>enable_markdown_filter</code></p></td><td><p><code>bool</code></p></td><td><p>否</p></td><td><p>是否启用 Markdown 过滤。启用后，服务会在合成前将 Markdown 转换成适合朗读的文本。</p><p>默认值：<code>False</code>。设为 <code>True</code> 启用。</p><p>通过 <code>parameters={&quot;enable_markdown_filter&quot;: True}</code> 启用。</p></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="sdk-reference"></a>

## 接口参考

<a id="核心资源-client-audio-tts"></a>

<a id="model-qwen-audio-tts-h2-cosyvoice-synth"></a>

<a id="model-cosyvoice-h2-cosyvoice-synth"></a>

### 核心资源（`client.audio.tts`）

**资源路径**：`client.audio.tts`

**功能**：基于WebSocket的语音合成，提供一次性合成（`synthesize`）、流式合成（`stream`）与双向流式会话（`connect`）三种调用形态。

<a id="调用入口"></a>

<a id="model-qwen-audio-tts-h3-5e8c3f2d"></a>

<a id="model-cosyvoice-h3-5e8c3f2d"></a>

#### 调用入口

下方示例使用 Qwen-Audio-TTS。使用 CosyVoice 时，可将 `model` 改为 `cosyvoice-v3-plus`，将 `voice` 改为 `longanyang`。

<a id="code-block-10"></a>

```python
# 一次性合成：返回完整音频 bytes
audio = client.audio.tts.synthesize(
    text,                      # text 必填（位置参数）
    model="qwen-audio-3.0-tts-flash", # 音色所属模型
    voice="longanhuan_v3.6",   # 音色
    format="mp3",              # 音频编码格式，默认 "mp3"
    sample_rate=22050,         # 采样率，默认 22050
)

# 流式合成：逐块产出音频 bytes（边收边写/播）
for chunk in client.audio.tts.stream(text, model=..., voice=...):
    ...

# 双向流式会话：逐段输入文本，进入 with 上下文时自动建立连接
with client.audio.tts.connect(model=..., voice=...) as session:
    session.send_text(text)    # 可多次调用追加文本
    session.stop()             # 通知服务端输入结束
    for chunk in session.audio_chunks():
        ...
```

<a id="synthesize-非流式调用"></a>

<a id="model-qwen-audio-tts-h4-py-cv-call"></a>

<a id="model-cosyvoice-h4-py-cv-call"></a>

#### synthesize() - 非流式调用

以下签名展示 Qwen-Audio-TTS 的参数。CosyVoice 的 `synthesize()` 签名中，`model` 默认值为 `cosyvoice-v1`，`voice` 默认值为 `longxiaochun`。

**方法签名**：

<a id="code-block-11"></a>

```python
def synthesize(self, text: str, *, model: str,
               voice: str, format: str = "mp3",
               sample_rate: int = 22050, volume: int = None,
               rate: float = None, pitch: float = None,
               language_hints: list = None, enable_ssml: bool = None,
               parameters: Dict = None, ...) -> bytes
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `text` | `str` | 是 | 待合成的完整文本，长度不得超过20000字符。 |

**返回值**：`bytes`，完整音频数据。

**说明**：非流式调用，阻塞等待并一次性返回完整音频数据。适用于短文本、对实时性无严格要求的场景。`synthesize`与`stream`每次调用自建会话，无需复用实例。

<a id="stream-流式调用"></a>

<a id="model-qwen-audio-tts-h4-py-cv-streaming"></a>

<a id="model-cosyvoice-h4-py-cv-streaming"></a>

#### stream() - 流式调用

**方法签名**：

<a id="code-block-12"></a>

```python
def stream(self, text: str, *, model: str, voice: str,
           format: str = "mp3", sample_rate: int = 22050, ...) -> Iterator[bytes]
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `text` | `str` | 是 | 待合成的完整文本，长度不得超过20000字符。 |

**返回值**：`Iterator[bytes]`，逐块产出的音频数据。

**说明**：流式合成，一次性发送完整文本并逐块产出音频（`Iterator[bytes]`）。适用于对实时性要求高的短文本语音合成场景。需要分片提交文本时请使用[双向流式会话（`connect`）](#model-qwen-audio-tts-h4-py-cv-sendtext)。

<a id="send-text-流式输入-会话方法"></a>

<a id="model-qwen-audio-tts-h4-py-cv-sendtext"></a>

<a id="model-cosyvoice-h4-py-cv-sendtext"></a>

#### send\_text() - 流式输入（会话方法）

双向流式会话（`client.audio.tts.connect(...)`）中分片提交文本。

**方法签名**：

<a id="code-block-13"></a>

```python
def send_text(self, text: str) -> None
```

**参数说明**：`text`为当前待合成的文本片段。可多次调用`send_text`以追加文本，单次不超过20000字符，累计不超过20万字符。发送文本与接收音频需并发进行（配合`audio_chunks()`/`events()`和`stop`使用）。

<a id="stop-结束流式输入-会话方法"></a>

<a id="model-qwen-audio-tts-h4-py-cv-complete"></a>

<a id="model-cosyvoice-h4-py-cv-complete"></a>

#### stop() - 结束流式输入（会话方法）

**方法签名**：

<a id="code-block-14"></a>

```python
def stop(self) -> None
```

**说明**：通知服务端所有文本已发送完毕。调用后不阻塞当前线程，接收线程需继续消费`audio_chunks()`/`events()`直到剩余文本合成完成并返回所有音频数据。未调用此方法可能导致尾部文本无法转换为语音。

<a id="cancel-取消流式合成-会话方法"></a>

<a id="model-cosyvoice-h4-py-cv-cancel"></a>

<a id="model-qwen-audio-tts-h4-py-cv-cancel"></a>

#### cancel() - 取消流式合成（会话方法）

**方法签名**：

<a id="code-block-15"></a>

```python
def cancel(self) -> None
```

**说明**：取消当前轮次的流式语音合成任务。调用后，SDK 会立即结束当前任务。取消后当前会话不能再发送文本，如需继续合成请新建会话。

> **重要**
>
> **模型限制**：
>
> -   华北2（北京）地域：CosyVoice 系列模型仅 v2 及以上版本支持该功能。
> -   新加坡地域：CosyVoice 系列模型不支持该功能。

<a id="会话指标与响应-会话属性"></a>

<a id="model-qwen-audio-tts-h4-py-cv-getreqid"></a>

<a id="model-cosyvoice-h4-py-cv-getreqid"></a>

<a id="model-qwen-audio-tts-h4-py-cv-getdelay"></a>

<a id="model-cosyvoice-h4-py-cv-getdelay"></a>

<a id="model-qwen-audio-tts-h4-py-cv-getresp"></a>

<a id="model-cosyvoice-h4-py-cv-getresp"></a>

#### 会话指标与响应（会话属性）

<a id="code-block-16"></a>

```python
session.first_package_delay
session.usage
session.last_response
```

-   `first_package_delay`：`float`，从发送文本到收到第一块音频数据的延迟时间（毫秒）。需在合成完成后读取。
-   `usage`：`dict`，最近一次合成任务的用量信息。
-   `last_response`：`dict`，最近一次合成任务的响应消息（含 `header`/`payload` 键）。最近一次请求的request\_id可从`session.last_response`的`header`中获取，可用于问题排查和日志关联。

<a id="会话与事件迭代"></a>

<a id="model-qwen-audio-tts-h2-callback-cosyvoice"></a>

<a id="model-cosyvoice-h2-callback-cosyvoice"></a>

### 会话与事件迭代

流式合成不再使用回调接口：音频与服务端事件通过会话的迭代方法接收。`stream()`/`synthesize()`无需会话管理；双向流式会话（`client.audio.tts.connect(...)`）的生命周期为：进入`with`上下文自动建立连接 → 多次`send_text()` → `stop()` → 读完全部结果 → 退出上下文自动关闭。

<a id="audio-chunks-迭代音频数据"></a>

<a id="model-qwen-audio-tts-h4-py-cvcb-ondata"></a>

<a id="model-cosyvoice-h4-py-cvcb-ondata"></a>

#### audio\_chunks() - 迭代音频数据

**方法签名**：

<a id="code-block-17"></a>

```python
def audio_chunks(self) -> Iterator[bytes]
```

**返回值**：`Iterator[bytes]`，逐块产出的音频二进制数据片段，格式由`format`参数指定。

**说明**：在接收线程中迭代，逐块接收音频数据，合成过程中会产出多块。可将数据写入文件或送入播放设备。同一会话只允许一个`events()`或`audio_chunks()`读取者。

<a id="events-迭代服务端事件"></a>

<a id="model-qwen-audio-tts-h4-py-cvcb-onevent"></a>

<a id="model-cosyvoice-h4-py-cvcb-onevent"></a>

#### events() - 迭代服务端事件

**方法签名**：

<a id="code-block-18"></a>

```python
def events(self) -> Generator[Union[Dict, bytes], None, None]
```

**返回值**：同时产出服务端响应事件（`dict`，包含`header`（请求信息）和`payload`（输出信息））与音频`bytes`。其中`payload.output`包含事件类型、原始文本等信息，详见[events()事件中的output字段](#model-qwen-audio-tts-h2-py-output-info)。

**说明**：在接收线程中迭代服务端回复，包含合成事件的输出信息（事件类型、原始文本、句子信息等），可直接访问`payload.output`获取详细信息。

<a id="错误处理"></a>

<a id="model-qwen-audio-tts-h4-py-cvcb-onerror"></a>

<a id="model-cosyvoice-h4-py-cvcb-onerror"></a>

#### 错误处理

合成过程中发生错误时，ws层会以`DashScopeError`异常抛出，异常触发后连接将自动关闭。可在发送/接收处使用try/except捕获并记录错误日志以便排查问题：

<a id="code-block-19"></a>

```python
from dashscope import DashScopeError

try:
    ...
except DashScopeError as e:
    print(e.code, e.message, e.request_id)
```

<a id="会话生命周期"></a>

<a id="model-qwen-audio-tts-h4-py-cvcb-onopen"></a>

<a id="model-cosyvoice-h4-py-cvcb-onopen"></a>

<a id="model-qwen-audio-tts-h4-py-cvcb-oncomplete"></a>

<a id="model-cosyvoice-h4-py-cvcb-oncomplete"></a>

<a id="model-qwen-audio-tts-h4-py-cvcb-onclose"></a>

<a id="model-cosyvoice-h4-py-cvcb-onclose"></a>

#### 会话生命周期

-   进入`with`上下文时自动建立连接（可在此前初始化音频输出流或打开文件等资源）。
-   所有文本合成完成且音频数据已全部产出后，`events()`/`audio_chunks()`迭代结束；此后可读取`first_package_delay`等性能指标。
-   退出`with`上下文时自动关闭连接（可在此后释放音频播放设备等资源）。

<a id="events-事件中的output字段"></a>

<a id="model-qwen-audio-tts-h2-py-output-info"></a>

<a id="model-cosyvoice-h2-py-output-info"></a>

### events()事件中的output字段

会话`events()`迭代产出的事件`dict`中，`payload.output`包含合成事件的输出信息，可用于跟踪合成进度和获取逐句信息。以下为`output`字段的结构说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `type` | `str` | 事件类型。取值为`sentence-begin`（句子合成开始）、`sentence-synthesis`（句子合成中）或`sentence-end`（句子合成结束）。 |
| `original_text` | `str` | 当前句子的原始文本。在`sentence-begin`和`sentence-end`事件中返回。 |
| `sentence` | `dict` | 句子信息。包含`index`（句子序号）和`words`（词列表，开启`word_timestamp_enabled`时返回时间戳信息）。 |

**消息示例**：

<a id="code-block-20"></a>

```json
{
  "header": {
    "task_id": "xxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "type": "sentence-begin",
      "original_text": "今天天气怎么样？",
      "sentence": {
        "index": 0,
        "words": []
      }
    }
  }
}
```

**解析示例**：

<a id="code-block-21"></a>

```python
def handle_event(event):
    output = (event.get('payload') or {}).get('output') or {}
    event_type = output.get('type', '')
    original_text = output.get('original_text', '')
    if event_type:
        print(f'事件类型: {event_type}, 原始文本: {original_text}')
```

<a id="qwen-audio-tts-3"></a>

<a id="model-qwen-audio-tts"></a>

### Qwen-Audio-TTS

调用方法见本组的[核心资源](#model-qwen-audio-tts-h2-cosyvoice-synth)。
