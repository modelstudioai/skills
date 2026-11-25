# Sambert Python SDK

通过 WebSocket 使用 DashScope Python SDK 调用 Sambert。

<a id="model-sambert"></a>

**用户指南：**关于模型介绍和选型建议请参见[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验：**暂不支持。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="前提条件"></a>

<a id="model-sambert-8d31b11222g24"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="模型列表"></a>

<a id="model-sambert-a737f8b6f8gx0"></a>

### 模型列表

> **说明**
>
> 默认采样率代表当前模型的最佳采样率，缺省条件下默认按照该采样率输出，同时支持降采样或升采样。如知妙音色，默认采样率16 kHz，使用时可以降采样到8 kHz，但升采样到48 kHz时不会有额外效果提升。

| 音色 | 音频试听（右键保存音频） | model参数 | 时间戳支持 | 适用场景 | 特色 | 语言 | 默认采样率（Hz） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 知楠 |  | sambert-zhinan-v1 | 是 | 通用场景 | 广告男声 | 中文+英文 | 48k |
| 知琪 |  | sambert-zhiqi-v1 | 是 | 通用场景 | 温柔女声 | 中文+英文 | 48k |
| 知厨 |  | sambert-zhichu-v1 | 是 | 新闻播报 | 舌尖男声 | 中文+英文 | 48k |
| 知德 |  | sambert-zhide-v1 | 是 | 新闻播报 | 新闻男声 | 中文+英文 | 48k |
| 知佳 |  | sambert-zhijia-v1 | 是 | 新闻播报 | 标准女声 | 中文+英文 | 48k |
| 知茹 |  | sambert-zhiru-v1 | 是 | 新闻播报 | 新闻女声 | 中文+英文 | 48k |
| 知倩 |  | sambert-zhiqian-v1 | 是 | 配音解说、新闻播报 | 资讯女声 | 中文+英文 | 48k |
| 知祥 |  | sambert-zhixiang-v1 | 是 | 配音解说 | 磁性男声 | 中文+英文 | 48k |
| 知薇 |  | sambert-zhiwei-v1 | 是 | 阅读产品简介 | 萝莉女声 | 中文+英文 | 48k |
| 知浩 |  | sambert-zhihao-v1 | 是 | 通用场景 | 咨询男声 | 中文+英文 | 16k |
| 知婧 |  | sambert-zhijing-v1 | 是 | 通用场景 | 严厉女声 | 中文+英文 | 16k |
| 知茗 |  | sambert-zhiming-v1 | 是 | 通用场景 | 诙谐男声 | 中文+英文 | 16k |
| 知墨 |  | sambert-zhimo-v1 | 是 | 通用场景 | 情感男声 | 中文+英文 | 16k |
| 知娜 |  | sambert-zhina-v1 | 是 | 通用场景 | 浙普女声 | 中文+英文 | 16k |
| 知树 |  | sambert-zhishu-v1 | 是 | 通用场景 | 资讯男声 | 中文+英文 | 16k |
| 知莎 |  | sambert-zhistella-v1 | 是 | 通用场景 | 知性女声 | 中文+英文 | 16k |
| 知婷 |  | sambert-zhiting-v1 | 是 | 通用场景 | 电台女声 | 中文+英文 | 16k |
| 知笑 |  | sambert-zhixiao-v1 | 是 | 通用场景 | 资讯女声 | 中文+英文 | 16k |
| 知雅 |  | sambert-zhiya-v1 | 是 | 通用场景 | 严厉女声 | 中文+英文 | 16k |
| 知晔 |  | sambert-zhiye-v1 | 是 | 通用场景 | 青年男声 | 中文+英文 | 16k |
| 知颖 |  | sambert-zhiying-v1 | 是 | 通用场景 | 软萌童声 | 中文+英文 | 16k |
| 知媛 |  | sambert-zhiyuan-v1 | 是 | 通用场景 | 知心姐姐 | 中文+英文 | 16k |
| 知悦 |  | sambert-zhiyue-v1 | 是 | 客服 | 温柔女声 | 中文+英文 | 16k |
| 知柜 |  | sambert-zhigui-v1 | 是 | 阅读产品简介 | 直播女声 | 中文+英文 | 16k |
| 知硕 |  | sambert-zhishuo-v1 | 是 | 数字人 | 自然男声 | 中文+英文 | 16k |
| 知妙（多情感） |  | sambert-zhimiao-emo-v1 | 是 | 阅读产品简介、数字人、直播 | 多种情感女声 | 中文+英文 | 16k |
| 知猫 |  | sambert-zhimao-v1 | 是 | 阅读产品简介、配音解说、数字人、直播 | 直播女声 | 中文+英文 | 16k |
| 知伦 |  | sambert-zhilun-v1 | 是 | 配音解说 | 悬疑解说 | 中文+英文 | 16k |
| 知飞 |  | sambert-zhifei-v1 | 是 | 配音解说 | 激昂解说 | 中文+英文 | 16k |
| 知达 |  | sambert-zhida-v1 | 是 | 新闻播报 | 标准男声 | 中文+英文 | 16k |
| Camila |  | sambert-camila-v1 | 否 | 通用场景 | 西班牙语女声 | 西班牙语 | 16k |
| Perla |  | sambert-perla-v1 | 否 | 通用场景 | 意大利语女声 | 意大利语 | 16k |
| Indah |  | sambert-indah-v1 | 否 | 通用场景 | 印尼语女声 | 印尼语 | 16k |
| Clara |  | sambert-clara-v1 | 否 | 通用场景 | 法语女声 | 法语 | 16k |
| Hanna |  | sambert-hanna-v1 | 否 | 通用场景 | 德语女声 | 德语 | 16k |
| Beth |  | sambert-beth-v1 | 是 | 通用场景 | 咨询女声 | 美式英文 | 16k |
| Betty |  | sambert-betty-v1 | 是 | 通用场景 | 客服女声 | 美式英文 | 16k |
| Cally |  | sambert-cally-v1 | 是 | 通用场景 | 自然女声 | 美式英文 | 16k |
| Cindy |  | sambert-cindy-v1 | 是 | 通用场景 | 对话女声 | 美式英文 | 16k |
| Eva |  | sambert-eva-v1 | 是 | 通用场景 | 陪伴女声 | 美式英文 | 16k |
| Donna |  | sambert-donna-v1 | 是 | 通用场景 | 教育女声 | 美式英文 | 16k |
| Brian |  | sambert-brian-v1 | 是 | 通用场景 | 客服男声 | 美式英文 | 16k |
| Waan |  | sambert-waan-v1 | 否 | 通用场景 | 泰语女声 | 泰语 | 16k |

<a id="快速开始"></a>

<a id="model-sambert-4906a3c99bnw8"></a>

## 快速开始

[核心资源（`client.audio.tts`）](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-adcb5e9bddbyq)提供了非流式调用和单向流式调用的接口。请根据业务场景选择合适的调用方式：

-   非流式调用：提交文本后，服务端立即处理并返回完整的语音合成结果。整个过程是阻塞式的，客户端需要等待服务端完成处理后才能继续下一步操作。适合短文本合成场景。
-   单向流式调用：将文本一次发送至服务端并实时接收语音合成结果，不允许将文本分段发送。适用于对实时性要求高的场景。

<a id="非流式调用"></a>

<a id="model-sambert-8341058094tc3"></a>

### 非流式调用

提交单个语音合成任务，进行语音合成（无流式输出中间结果），最终一次性获取完整结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4872835871/CAEQURiBgIDHpsn4phkiIDQ0ZGE2OTk3NmY5NTRhNDVhZDQwNWE3ZGZiMzk4Yjk54709861_20241015153444.149.svg)

直接调用[核心资源（`client.audio.tts`）](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-adcb5e9bddbyq)的`synthesize`方法进行语音合成。`synthesize`方法可对[请求参数](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-fdafc9b5535f3)进行设置。

任务完成后该方法返回完整的音频数据（`bytes`，时间戳信息需通过流式会话获取，参见[响应结果](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-a727da82951p6)）。

<a id="accordion-点击查看完整示例"></a>

点击查看完整示例

以下示例展示了如何使用同步接口调用发音人模型知厨（sambert-zhichu-v1），将文案”今天天气怎么样”合成采样率为48kHz，音频格式为wav的音频，并保存到名为output.wav的文件中。

<a id="code-block"></a>

```python
# coding=utf-8
import os
import sys

import dashscope

# 若没有将API Key配置到环境变量中，需将下行替换为自己的API Key：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
audio = client.audio.tts.synthesize(
    '今天天气怎么样',
    model='sambert-zhichu-v1',
    sample_rate=48000,
    format='wav')
with open('output.wav', 'wb') as f:
    f.write(audio)
print('SUCCESS: get audio data: %dbytes in output.wav' % (sys.getsizeof(audio)))
```

<a id="单向流式调用"></a>

<a id="model-sambert-ba023aacfbr84"></a>

### 单向流式调用

提交单个语音合成任务，流式输出中间结果，合成结果通过[流式合成会话](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-3639e1cb40mxi)的`events()`/`audio_chunks()`迭代获取。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4872835871/CAEQVRiBgMDd6_yhrBkiIDUyZGFlNTkwOGRlYTQwZjQ4ODI4ZGY2ZTQxYmNiMTVm4709861_20241015153444.149.svg)

1.  调用[核心资源（`client.audio.tts`）](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-adcb5e9bddbyq)的`connect`方法创建流式合成会话，进入`with`上下文时自动建立连接。
2.  调用会话的`send_text`方法发送待合成文本，`stop`方法通知服务端输入结束。
3.  在接收线程中迭代会话的`events()`（音频`bytes`与JSON事件，含时间戳）或`audio_chunks()`（仅音频）获取合成结果。

<a id="accordion-点击查看完整示例-2"></a>

点击查看完整示例

以下示例展示了如何使用流式接口调用发音人模型知厨（sambert-zhichu-v1）将文案”今天天气怎么样”合成采样率为48kHz，默认音频格式（wav）的流式音频，并获取对应时间戳。

<a id="code-block-2"></a>

```python
# coding=utf-8

import os
import sys

import dashscope

# 若没有将API Key配置到环境变量中，需将下行替换为自己的API Key：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 创建流式合成会话：进入 with 上下文时自动建立连接
with client.audio.tts.connect(
        model='sambert-zhichu-v1',
        sample_rate=48000,
        parameters={'word_timestamp_enabled': True,
                    'phoneme_timestamp_enabled': True},
) as session:
    session.send_text('今天天气怎么样')
    # 通知服务端输入结束
    session.stop()
    # events() 同时产出音频 bytes 与服务端 JSON 事件（含时间戳）
    for event in session.events():
        if isinstance(event, bytes):
            print('audio result length:', sys.getsizeof(event))
        else:
            output = (event.get('payload') or {}).get('output') or {}
            if output.get('timestamp') is not None:
                print('timestamp result:', str(output.get('timestamp')))
```

<a id="请求参数"></a>

<a id="model-sambert-fdafc9b5535f3"></a>

## 请求参数

请求参数通过[核心资源（`client.audio.tts`）](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-adcb5e9bddbyq)的`synthesize`/`stream`/`connect`方法进行设置（具名参数直接传入，`word_timestamp_enabled`、`phoneme_timestamp_enabled`通过`parameters`字典传入）。

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>默认值</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>str</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>指定用于语音合成的音色模型名，完整列表参见<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-a737f8b6f8gx0">模型列表</a>。</p></td></tr><tr><td><p>text</p></td><td><p>str</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>指定待合成文本，要求采用UTF-8编码且不能为空。</p><p>最高字符限制：1万字符。</p><blockquote><p>字符计算规则：1个汉字、1个英文字母、1个标点或1个句子中间空格均算作1个字符。</p></blockquote><p>支持SSML格式。SSML标记语言的使用请参见<a href="https://help.aliyun.com/zh/isi/developer-reference/ssml-overview">SSML标记语言介绍</a>。</p></td></tr><tr><td><p>format</p></td><td><p>str</p></td><td><p>wav</p></td><td><p>否</p></td><td><p>指定合成音频的编码格式，支持<code>pcm</code>、<code>wav</code>和<code>mp3</code>这三种格式。</p></td></tr><tr><td><p>sample_rate</p></td><td><p>int</p></td><td><p>16000</p></td><td><p>否</p></td><td><p>指定合成音频的采样率（单位：Hz），建议使用模型默认采样率（参见<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-a737f8b6f8gx0">模型列表</a>），如果不匹配，服务会进行必要的升降采样处理。</p></td></tr><tr><td><p>volume</p></td><td><p>int</p></td><td><p>50</p></td><td><p>否</p></td><td><p>指定合成音频的音量，取值范围是0~100。</p></td></tr><tr><td><p>rate</p></td><td><p>float</p></td><td><p>1.0</p></td><td><p>否</p></td><td><p>指定合成音频的语速，取值范围：0.5~2。</p><ul><li>0.5：表示默认语速的0.5倍速。</li><li>1：表示默认语速。默认语速是指模型默认输出的合成语速，语速会因发音人不同而略有不同。约每秒钟4个字。</li><li>2：表示默认语速的2倍速。</li></ul></td></tr><tr><td><p>pitch</p></td><td><p>float</p></td><td><p>1.0</p></td><td><p>否</p></td><td><p>指定合成音频的语调，取值范围：0.5~2。</p></td></tr><tr><td><p>word_timestamp_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><p>是否开启字级别时间戳。默认不开启。</p></td></tr><tr><td><p>phoneme_timestamp_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><p>在开启字级别时间戳（<code>word_timestamp_enabled</code>）的基础上，生成音素级别时间戳信息。默认不开启。</p></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="model-sambert-843fb17087zct"></a>

<a id="关键接口"></a>

## 接口参考

<a id="核心资源-client-audio-tts"></a>

<a id="model-sambert-adcb5e9bddbyq"></a>

### 核心资源（`client.audio.tts`）

语音合成能力挂载在`client.audio.tts`资源上：`synthesize`一次性返回完整音频，`stream`流式产出音频分片，`connect`创建流式合成会话。它的关键接口如下：

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-3"></a><pre class="language-python"><code>def synthesize(self,
               text: str,
               *,
               model: str,
               voice: str = &quot;longxiaochun&quot;,
               format: str = &quot;mp3&quot;,
               sample_rate: int = 22050,
               volume: int = None,
               rate: float = None,
               pitch: float = None,
               parameters: Dict = None,
               ...) -&gt; bytes
</code></pre></td><td><ul><li><code>text</code>：待合成文本</li><li><code>model</code>：模型名，参见<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-a737f8b6f8gx0">模型列表</a></li><li>其余为<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-fdafc9b5535f3">请求参数</a>，如<code>format</code>等</li></ul></td><td><p>完整的音频数据（<code>bytes</code>）</p></td><td><p>开启语音合成任务，在语音合成完成后返回完整音频数据。</p><p><code>synthesize</code>方法能够对<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-fdafc9b5535f3">请求参数</a>进行设置。</p></td></tr><tr><td><a id="code-block-4"></a><pre class="language-python"><code>def stream(self,
           text: str,
           *,
           model: str,
           ...) -&gt; Iterator[bytes]
</code></pre></td><td><p>同<code>synthesize</code></p></td><td><p>逐块产出的音频数据（<code>Iterator[bytes]</code>）</p></td><td><p>开启语音合成任务，一次性发送文本并逐块产出音频分片。只输出音频，不暴露逐条JSON元数据（需时间戳请使用<code>connect</code>会话）。</p></td></tr><tr><td><a id="code-block-5"></a><pre class="language-python"><code>def connect(self,
            *,
            model: str,
            format: str = &quot;mp3&quot;,
            sample_rate: int = 22050,
            parameters: Dict = None,
            ...) -&gt; SynthesisSession
</code></pre></td><td><ul><li><code>model</code>：模型名，参见<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-a737f8b6f8gx0">模型列表</a></li><li>其余为<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-fdafc9b5535f3">请求参数</a></li></ul></td><td><p><code>SynthesisSession</code>流式合成会话</p></td><td><p>创建流式合成会话，进入<code>with</code>上下文时自动建立连接。配合<code>send_text</code>、<code>stop</code>、<code>events()</code>/<code>audio_chunks()</code>使用（见<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-3639e1cb40mxi">事件迭代</a>）。</p></td></tr></tbody></table>

<a id="事件迭代-events-audio-chunks"></a>

<a id="model-sambert-3639e1cb40mxi"></a>

### 事件迭代（`events()`/`audio_chunks()`）

[单向流式调用](realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-ba023aacfbr84)时，服务端会通过事件的方式，将关键流程信息和数据返回给客户端。在接收线程中迭代会话的`events()`或`audio_chunks()`处理服务端返回的信息或者数据。

<a id="accordion-点击查看示例"></a>

点击查看示例

<a id="code-block-6"></a>

```python
# events() 同时产出音频 bytes 与服务端 JSON 事件（含时间戳）
for event in session.events():
    if isinstance(event, bytes):
        print('收到二进制音频数据：', event)
    else:
        output = (event.get('payload') or {}).get('output') or {}
        if output.get('timestamp') is not None:
            print('收到时间戳数据：', str(output.get('timestamp')))

# 或只迭代音频（仍更新会话的 last_response 与 usage）
for chunk in session.audio_chunks():
    print('收到二进制音频数据：', chunk)
```

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-7"></a><pre class="language-python"><code>def send_text(self, text: str) -&gt; None
</code></pre></td><td><p><code>text</code>：待合成文本</p></td><td><p>无</p></td><td><p>发送待合成文本。发送文本与接收结果需并发进行。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-python"><code>def stop(self) -&gt; None
</code></pre></td><td><p>无</p></td><td><p>无</p></td><td><p>通知服务端输入结束，之后继续消费<code>events()</code>/<code>audio_chunks()</code>直到剩余音频全部返回。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-python"><code>def events(self) -&gt; Generator[Union[Dict, bytes], None, None]
</code></pre></td><td><p>无</p></td><td><p><code>Dict</code>（JSON事件）或<code>bytes</code>（音频）</p></td><td><p>当服务端返回合成数据时逐个产出：音频为<code>bytes</code>帧，元数据（时间戳等）为JSON事件<code>dict</code>。同一会话只允许一个<code>events()</code>或<code>audio_chunks()</code>读取者。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-python"><code>def audio_chunks(self) -&gt; Iterator[bytes]
</code></pre></td><td><p>无</p></td><td><p><code>bytes</code></p></td><td><p>只迭代音频数据，仍更新会话的<code>last_response</code>与<code>usage</code>。</p></td></tr><tr><td><a id="code-block-11"></a><pre class="language-python"><code>session.first_package_delay
</code></pre></td><td><p>无</p></td><td><p><code>float</code></p></td><td><p>从发送文本到收到第一块音频数据的延迟时间（毫秒），任务完成后读取。</p></td></tr></tbody></table>

<a id="响应结果"></a>

<a id="model-sambert-2a2a707975o22"></a>

### 响应结果

<a id="合成结果-音频数据与时间戳"></a>

<a id="model-sambert-a727da82951p6"></a>

#### 合成结果（音频数据与时间戳）

`synthesize`返回完整的音频`bytes`；流式调用通过`stream`或会话的`audio_chunks()`逐块接收音频`bytes`；时间戳信息通过会话`events()`产出的JSON事件获取（`payload.output.timestamp`）。

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-12"></a><pre class="language-python"><code>audio = client.audio.tts.synthesize(...)
</code></pre></td><td><p>无</p></td><td><p>完整的二进制音频数据</p></td><td><p>非流式合成中，获取完整的二进制音频数据。</p></td></tr><tr><td><a id="code-block-13"></a><pre class="language-python"><code>for chunk in session.audio_chunks():
</code></pre></td><td><p>无</p></td><td><p>当前合成的二进制音频数据片段</p></td><td><p>流式合成中，逐块接收当前合成的音频帧数据。</p></td></tr><tr><td><a id="code-block-14"></a><pre class="language-python"><code>output = (event.get('payload') or {}).get('output') or {}
output.get('timestamp')
</code></pre></td><td><p>无</p></td><td><p>当前合成的句子对应的<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-6a6d7363490w6">时间戳信息</a></p></td><td><p>流式合成中，从<code>events()</code>产出的JSON事件里获取当前合成的句子对应的时间戳信息。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-python"><code>timestamps = [
    ((e.get('payload') or {}).get('output') or {}).get('timestamp')
    for e in json_events if ...
]
</code></pre></td><td><p>无</p></td><td><p>所有句子对应的<a href="realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md#model-sambert-6a6d7363490w6">时间戳信息</a></p></td><td><p>流式合成中，累积<code>events()</code>产出的各句时间戳即为所有句子对应的时间戳信息。</p></td></tr></tbody></table>

<a id="时间戳信息"></a>

<a id="model-sambert-6a6d7363490w6"></a>

#### 时间戳信息

会话`events()`产出的JSON事件中，`payload.output.timestamp`为当前合成的句子的时间戳信息，累积各句即为所有句子的时间戳信息。

单个句子的时间戳信息示例如下所示，其中`words`对应的是字级别时间戳信息。`phonemes`对应的是音素级别时间戳信息：

<a id="code-block-16"></a>

```json
{
    "begin_time":0,
    "end_time":1412,
    "words":[
        {
            "text":"今",
            "begin_time":0,
            "end_time":200,
            "phonemes":[
                {
                    "begin_time":0,
                    "end_time":82,
                    "text":"j_c",
                    "tone":1
                },
                {
                    "begin_time":82,
                    "end_time":200,
                    "text":"in_c",
                    "tone":1
                }
            ]
        }
    ]
}
```

各参数含义如下所示：

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>begin_time</p></td><td><p>int</p></td><td><p>句子、字、音素开始时间，单位为ms。</p></td></tr><tr><td><p>end_time</p></td><td><p>int</p></td><td><p>句子、字、音素结束时间，单位为ms。</p></td></tr><tr><td><p>words</p></td><td><p>list</p></td><td><p>包含的字级别时间戳信息，需要请求中<code>word_timestamp_enabled</code>也设置为true<em>。</em></p></td></tr><tr><td><p>text</p></td><td><p>str</p></td><td><p>文本信息。</p></td></tr><tr><td><p>phonemes</p></td><td><p>list</p></td><td><p>包含的音素级别时间戳信息，需要请求中<code>phoneme_timestamp_enabled</code>也设置为true<em>。</em></p></td></tr><tr><td><p>tone</p></td><td><p>str</p></td><td><p>音调。</p><ul><li><p>英文中，0、1、2分别代表轻音、重音和次重音。</p></li><li><p>拼音中，1、2、3、4、5分别代表一声、二声、三声、四声和轻声。</p></li></ul></td></tr></tbody></table>

<a id="更多示例"></a>

<a id="model-sambert-4b46ba65680pp"></a>

## 更多示例

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

<a id="错误码"></a>

<a id="model-sambert-a370386972oa4"></a>

## 错误码

在使用API过程中，如果调用失败并返回错误信息，请参见[错误码](../model-api-reference/preparations/error-code.md)进行解决。
