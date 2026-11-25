# Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考

使用 DashScope Python SDK 创建和管理 Qwen-Audio 与 CosyVoice 复刻音色。

<a id="接口地址"></a>

<a id="h2-ps8o5p1u"></a>

## 接口地址

SDK的接口地址由Client构造参数`workspace`/`region`决定（对应下方地址，包含WorkspaceId）。如需切换到其他地域，请修改Client构造参数为对应地域的值。

> **说明**
>
> -   不同地域的 API Key 不同，调用时需使用对应地域的 API Key。
> -   地域配置为Client级设置，影响该Client的所有 DashScope SDK API 调用。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<a id="核心资源-client-audio-voices"></a>

<a id="h3-ps2o8p4q"></a>

## 核心资源（`client.audio.voices`）

**功能**：管理 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 复刻音色的生命周期（创建、查询、更新、删除）。

<a id="client-构造-鉴权与地域"></a>

<a id="h4-ps7y4z9a"></a>

### Client 构造（鉴权与地域）

<a id="code-block"></a>

```python
import os
import dashscope

client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
```

<a id="create-创建音色"></a>

<a id="h4-ps1e7f3g"></a>

### create() - 创建音色

**方法签名**：

<a id="code-block-2"></a>

```python
def create(self, *, target_model: str, prefix: str, url: str,
           language_hints: List[str] = None,
           max_prompt_audio_length: float = None,
           extra_input: Dict = None,
           parameters: Dict = None, ...) -> Voice
```

**参数说明**：

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>target_model</p></td><td><p>str</p></td><td><p>是</p></td><td><p>驱动音色的目标模型。必须与后续使用该音色的模型一致，否则调用失败。</p></td></tr><tr><td><p>prefix</p></td><td><p>str</p></td><td><p>是</p></td><td><p>音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：<code>{target_model}-{prefix}-{唯一标识}</code>。</p></td></tr><tr><td><p>url</p></td><td><p>str</p></td><td><p>是</p></td><td><p>用于复刻音色的参考音频，支持公网可访问的 URL 或 Base64 Data URI，例如 <code>data:audio/wav;base64,...</code>。</p></td></tr><tr><td><p>language_hints</p></td><td><p>List[str]</p></td><td><p>否</p></td><td><p>辅助模型识别样本音频的语种，从而更准确地提取音色特征，提升复刻效果。若设置的语种与实际音频语种不符（例如为中文音频设置 <code>en</code>），系统将忽略该设置并自动检测语种。</p><p>此参数为数组，长度必须为 1。</p><div><div><p><strong>说明</strong>适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash。</p></div></div><a id="accordion-点击查看各模型支持的语言"></a><section><p>点击查看各模型支持的语言</p><div><ul><li><p>qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash：</p><ul><li>zh：中文</li><li>en：英语</li><li>fr：法语</li><li>de：德语</li><li>ja：日语</li><li>ko：韩语</li><li>ru：俄语</li><li>pt：葡萄牙语</li><li>th：泰语</li><li>id：印尼语</li><li>vi：越南语</li><li>it：意大利语</li><li>es：西班牙语</li><li>ms：马来西亚语</li><li>fil：菲律宾语</li><li>ar：阿拉伯语</li></ul></li><li><p>cosyvoice-v3-plus：</p><ul><li>zh：中文</li><li>en：英文</li><li>fr：法语</li><li>de：德语</li><li>ja：日语</li><li>ko：韩语</li><li>ru：俄语</li></ul></li><li><p>cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash：</p><ul><li>zh：中文</li><li>en：英文</li><li>fr：法语</li><li>de：德语</li><li>ja：日语</li><li>ko：韩语</li><li>ru：俄语</li><li>pt：葡萄牙语</li><li>th：泰语</li><li>id：印尼语</li><li>vi：越南语</li></ul></li></ul></div></section><p>默认值：[&quot;zh&quot;]。</p></td></tr><tr><td><p>max_prompt_audio_length</p></td><td><p>float</p></td><td><p>否</p></td><td><p>音频预处理后用于声音复刻的参考音频最大时长（秒）。取值范围：[3.0, 30.0]。</p><p>默认值：10.0。</p><div><div><p><strong>说明</strong>适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。</p></div></div></td></tr><tr><td><p>enable_preprocess</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。</p><p>默认值：false。</p><div><div><p><strong>说明</strong>适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。</p></div></div></td></tr><tr><td><p>enable_volume_normalization</p></td><td><p>bool</p></td><td><p>否</p></td><td><p>是否对用于声音复刻的样本音频进行音量归一化。通过<code>extra_input</code>字典传入。默认值为<code>False</code>。设置为<code>True</code>后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。</p></td></tr></tbody></table>

**返回值**：`Voice`对象，其`voice_id`为音色ID，`request_id`为请求ID。

<a id="list-查询音色列表"></a>

<a id="h4-ps2u8v4w"></a>

### list() - 查询音色列表

**方法签名**：

<a id="code-block-3"></a>

```python
def list(self, *, prefix: str = None, page_index: int = 0, page_size: int = 10, ...) -> VoiceList
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| prefix | str | 否 | 按音色名称前缀筛选。 |
| page\_index | int | 否 | 页码索引，默认0。 |
| page\_size | int | 否 | 每页条数，默认10。 |

**返回值**：`VoiceList`对象，其`voices`为音色列表，`request_id`为请求ID。列表项为字典，通过 `voice.get("target_model")` 获取目标模型 ID。

<a id="get-查询音色详情"></a>

<a id="h4-ps3i9j5k"></a>

### get() - 查询音色详情

**方法签名**：

<a id="code-block-4"></a>

```python
def get(self, voice_id: str, ...) -> Voice
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| voice\_id | str | 是 | 要查询的音色ID。 |

**返回值**：`Voice`对象，音色详情。通过 `voice.target_model` 获取目标模型 ID。

<a id="update-更新音色"></a>

<a id="h4-ps2i8j4k"></a>

### update() - 更新音色

**方法签名**：

<a id="code-block-5"></a>

```python
def update(self, voice_id: str, *, url: str, ...) -> JobStatus
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| voice\_id | str | 是 | 要更新的音色ID。 |
| url | str | 是 | 新的参考音频，支持公网可访问的 URL 或 Base64 Data URI，例如 `data:audio/wav;base64,...`。 |

<a id="delete-删除音色"></a>

<a id="h4-ps8y5z1a"></a>

### delete() - 删除音色

**方法签名**：

<a id="code-block-6"></a>

```python
def delete(self, voice_id: str, ...) -> JobStatus
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| voice\_id | str | 是 | 要删除的音色ID。 |

<a id="示例代码"></a>

<a id="h2-py2d4e5f"></a>

## 示例代码

<a id="创建音色"></a>

<a id="h3-py4j8k9l"></a>

### 创建音色

<a id="code-block-7"></a>

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

TARGET_MODEL = 'qwen-audio-3.1-tts-plus'
voice_prefix = 'myvoice'
url = 'https://your-audio-file-url'

# 避免频繁调用。每次调用都会创建新音色，达到配额上限后将无法创建。
voice = client.audio.voices.create(
    target_model=TARGET_MODEL,
    prefix=voice_prefix,
    url=url,
    max_prompt_audio_length=10,
    # extra_input={'enable_preprocess': False, 'enable_volume_normalization': True}
)

print(f"Request ID: {voice.request_id}")
print(f"Voice ID: {voice.voice_id}")
```

使用本地 WAV 音频时，将上述 `url` 赋值替换为以下代码，再调用 `client.audio.voices.create()`。更新音色时，也通过 `client.audio.voices.update()` 的 `url` 参数传入 Data URI。将 `sample.wav` 替换为本地音频路径。

<a id="code-block-8"></a>

```python
import base64
from pathlib import Path

url = "data:audio/wav;base64," + base64.b64encode(
    Path("sample.wav").read_bytes()
).decode("ascii")
```

<a id="查询音色列表"></a>

<a id="h3-py7s5t6u"></a>

### 查询音色列表

<a id="code-block-9"></a>

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

# 按前缀筛选，或设为None查询所有
voices = client.audio.voices.list(prefix='myvoice', page_index=0, page_size=10)

print(f"Request ID: {voices.request_id}")
print(f"Found voices: {voices.voices}")
for voice in voices.voices:
    print(f"Target model: {voice.get('target_model')}")
```

<a id="查询特定音色"></a>

<a id="h3-py1b3c4d"></a>

### 查询特定音色

<a id="code-block-10"></a>

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

voice_id = 'qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx'

voice_details = client.audio.voices.get(voice_id=voice_id)

print(f"Request ID: {voice_details.request_id}")
print(f"Voice Details: {voice_details}")
print(f"Target model: {voice_details.target_model}")
```

<a id="更新音色"></a>

<a id="h3-py4k9l1m"></a>

### 更新音色

<a id="code-block-11"></a>

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

result = client.audio.voices.update(
    voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx',
    url='https://your-new-audio-file-url'
)
print(f"Update submitted. Request ID: {result.request_id}")
```

<a id="删除音色"></a>

<a id="h3-py7t6u7v"></a>

### 删除音色

<a id="code-block-12"></a>

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

result = client.audio.voices.delete(voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx')
print(f"Deletion submitted. Request ID: {result.request_id}")
```
