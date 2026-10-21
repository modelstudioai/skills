# 声音复刻Python SDK参考

本文介绍声音复刻的Python SDK使用方法。

## 接口地址

SDK的接口地址需在初始化前设置为下方地址（包含WorkspaceId）。如需切换到其他地域，请修改 `dashscope.base_http_api_url`为对应地域的URL。

**说明**

-   不同地域的 API Key 不同，调用时需使用对应地域的 API Key。
-   地域配置为全局设置，影响所有 DashScope SDK API 调用。

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

## VoiceEnrollmentService 类

**包路径**：`dashscope.audio.tts_v2.VoiceEnrollmentService`

**功能**：管理 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 复刻音色的生命周期（创建、查询、更新、删除）。

### 构造方法

```
VoiceEnrollmentService()
```

### create\_voice() - 创建音色

**方法签名**：

```
def create_voice(self, target_model: str, prefix: str, url: str,
                 language_hints: List[str] = None,
                 max_prompt_audio_length: float = None,
                 **kwargs) -> str
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

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash。

点击查看各模型支持的语言

-   qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash：
    
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

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

enable\_preprocess

bool

否

是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。

默认值：false。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

enable\_volume\_normalization

bool

否

是否对用于声音复刻的样本音频进行音量归一化。通过关键字参数直接传入。默认值为`False`。设置为`True`后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。

**返回值**：`str`，音色ID（voice\_id）。

### list\_voices() - 查询音色列表

**方法签名**：

```
def list_voices(self, prefix: str = None, page_index: int = 0, page_size: int = 10) -> list
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

**返回值**：`list`，音色列表。

### query\_voice() - 查询音色详情

**方法签名**：

```
def query_voice(self, voice_id: str) -> dict
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

**返回值**：`dict`，音色详情。

### update\_voice() - 更新音色

**方法签名**：

```
def update_voice(self, voice_id: str, url: str) -> None
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

### delete\_voice() - 删除音色

**方法签名**：

```
def delete_voice(self, voice_id: str) -> None
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
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

TARGET_MODEL = 'qwen-audio-3.0-tts-flash'
voice_prefix = 'myvoice'
url = 'https://your-audio-file-url'
service = VoiceEnrollmentService()

# 避免频繁调用。每次调用都会创建新音色，达到配额上限后将无法创建。
voice_id = service.create_voice(
    target_model=TARGET_MODEL,
    prefix=voice_prefix,
    url=url,
    max_prompt_audio_length=10,
    # enable_preprocess=False,
    # enable_volume_normalization=True
)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Voice ID: {voice_id}")
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
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

service = VoiceEnrollmentService()

# 按前缀筛选，或设为None查询所有
voices = service.list_voices(prefix='myvoice', page_index=0, page_size=10)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Found voices: {voices}")
```

### 查询特定音色

```
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

service = VoiceEnrollmentService()
voice_id = 'qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx'

voice_details = service.query_voice(voice_id=voice_id)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Voice Details: {voice_details}")
```

### 更新音色

```
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

service = VoiceEnrollmentService()
service.update_voice(
    voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx',
    url='https://your-new-audio-file-url'
)
print(f"Update submitted. Request ID: {service.get_last_request_id()}")
```

### 删除音色

```
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

service = VoiceEnrollmentService()
service.delete_voice(voice_id='qwen-audio-3.0-tts-flash-myvoice-xxxxxxxx')
print(f"Deletion submitted. Request ID: {service.get_last_request_id()}")
```
