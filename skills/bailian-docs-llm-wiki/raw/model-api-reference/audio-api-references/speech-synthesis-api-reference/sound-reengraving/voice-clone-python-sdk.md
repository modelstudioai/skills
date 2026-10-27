# 声音复刻Python SDK参考

本文介绍声音复刻的Python SDK使用方法。

## 接口地址

SDK的接口地址由Client构造参数`workspace`/`region`决定（对应下方地址，包含WorkspaceId）。如需切换到其他地域，请修改Client构造参数为对应地域的值。

**说明**

-   不同地域的 API Key 不同，调用时需使用对应地域的 API Key。
-   地域配置为Client级设置，影响该Client的所有 DashScope SDK API 调用。

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

## 核心资源（`client.audio.voices`）

**资源路径**：`client.audio.voices`

**功能**：管理 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 复刻音色的生命周期（创建、查询、更新、删除）。

### Client 构造（鉴权与地域）

```
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

### create() - 创建音色

**方法签名**：

```
def create(self, *, target_model: str, prefix: str, url: str,
           language_hints: List[str] = None,
           max_prompt_audio_length: float = None,
           extra_input: Dict = None,
           parameters: Dict = None, ...) -> Voice
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

target\_model

str

是

驱动音色的目标模型。必须与后续使用该音色的模型一致，否则调用失败。

prefix

str

是

音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-{prefix}-{唯一标识}`。

url

str

是

用于复刻音色的参考音频，支持公网可访问的 URL 或 Base64 Data URI，例如 `data:audio/wav;base64,...`。

language\_hints

List\[str\]

否

辅助模型识别样本音频的语种，从而更准确地提取音色特征，提升复刻效果。若设置的语种与实际音频语种不符（例如为中文音频设置 `en`），系统将忽略该设置并自动检测语种。

此参数为数组，长度必须为 1。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash。

点击查看各模型支持的语言

-   qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash：
    
    -   zh：中文
    -   en：英语
    -   fr：法语
    -   de：德语
    -   ja：日语
    -   ko：韩语
    -   ru：俄语
    -   pt：葡萄牙语
    -   th：泰语
    -   id：印尼语
    -   vi：越南语
    -   it：意大利语
    -   es：西班牙语
    -   ms：马来西亚语
    -   fil：菲律宾语
    -   ar：阿拉伯语
-   cosyvoice-v3-plus：
    
    -   zh：中文
    -   en：英文
    -   fr：法语
    -   de：德语
    -   ja：日语
    -   ko：韩语
    -   ru：俄语
-   cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash：
    
    -   zh：中文
    -   en：英文
    -   fr：法语
    -   de：德语
    -   ja：日语
    -   ko：韩语
    -   ru：俄语
    -   pt：葡萄牙语
    -   th：泰语
    -   id：印尼语
    -   vi：越南语

默认值：\["zh"\]。

max\_prompt\_audio\_length

float

否

音频预处理后用于声音复刻的参考音频最大时长（秒）。取值范围：\[3.0, 30.0\]。

默认值：10.0。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

enable\_preprocess

bool

否

是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。

默认值：false。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

enable\_volume\_normalization

bool

否

是否对用于声音复刻的样本音频进行音量归一化。通过`extra_input`字典传入。默认值为`False`。设置为`True`后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。

**返回值**：`Voice`对象，其`voice_id`为音色ID，`request_id`为请求ID。

### list() - 查询音色列表

**方法签名**：

```
def list(self, *, prefix: str = None, page_index: int = 0, page_size: int = 10, ...) -> VoiceList
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

prefix

str

否

按音色名称前缀筛选。

page\_index

int

否

页码索引，默认0。

page\_size

int

否

每页条数，默认10。

**返回值**：`VoiceList`对象，其`voices`为音色列表，`request_id`为请求ID。

### get() - 查询音色详情

**方法签名**：

```
def get(self, voice_id: str, ...) -> Voice
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

voice\_id

str

是

要查询的音色ID。

**返回值**：`Voice`对象，音色详情。

### update() - 更新音色

**方法签名**：

```
def update(self, voice_id: str, *, url: str, ...) -> JobStatus
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

voice\_id

str

是

要更新的音色ID。

url

str

是

新的参考音频，支持公网可访问的 URL 或 Base64 Data URI，例如 `data:audio/wav;base64,...`。

### delete() - 删除音色

**方法签名**：

```
def delete(self, voice_id: str, ...) -> JobStatus
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

voice\_id

str

是

要删除的音色ID。

## 示例代码

### 创建音色

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

使用本地 WAV 音频时，将上述 `url` 赋值替换为以下代码，再调用 `create_voice`。更新音色时，也通过 `update_voice` 的 `url` 参数传入 Data URI。将 `sample.wav` 替换为本地音频路径。

```
import base64
from pathlib import Path

url = "data:audio/wav;base64," + base64.b64encode(
    Path("sample.wav").read_bytes()
).decode("ascii")
```

### 查询音色列表

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

# 按前缀筛选，或设为None查询所有
voices = client.audio.voices.list(prefix='myvoice', page_index=0, page_size=10)

print(f"Request ID: {voices.request_id}")
print(f"Found voices: {voices.voices}")
```

### 查询特定音色

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

voice_id = 'qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx'

voice_details = client.audio.voices.get(voice_id=voice_id)

print(f"Request ID: {voice_details.request_id}")
print(f"Voice Details: {voice_details}")
```

### 更新音色

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

result = client.audio.voices.update(
    voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx',
    url='https://your-new-audio-file-url'
)
print(f"Update submitted. Request ID: {result.request_id}")
```

### 删除音色

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

result = client.audio.voices.delete(voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx')
print(f"Deletion submitted. Request ID: {result.request_id}")
```
