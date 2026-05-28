# 声音复刻Python SDK参考

本文介绍声音复刻的Python SDK使用方法。

**用户指南：**[声音复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)。

## **服务地址**

SDK默认使用**北京地域**的服务端点。如需切换到其他地域，需在初始化前修改 `dashscope.base_http_api_url`。

### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`https://dashscope.aliyuncs.com/api/v1`

### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`https://dashscope-intl.aliyuncs.com/api/v1`

**切换到新加坡地域**：

```
import dashscope

# 在代码开头设置
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
```

**注意**：

-   不同地域的 API Key 不同，请确保使用对应地域的 API Key
    
-   地域配置为全局设置，影响所有 DashScope SDK 的 API 调用
    

## **VoiceEnrollmentService 类**

**包路径**：`dashscope.audio.tts_v2.VoiceEnrollmentService`

**功能**：管理CosyVoice复刻音色的生命周期（创建、查询、更新、删除）。

### **构造方法**

```
VoiceEnrollmentService()
```

### **create\_voice() - 创建音色**

**方法签名**：

```
def create_voice(self, target_model: str, prefix: str, url: str,
                 language_hints: List[str] = None,
                 max_prompt_audio_length: float = None,
                 enable_preprocess: bool = None) -> str
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

target\_model

str

是

驱动音色的语音合成模型。必须与后续调用语音合成接口时使用的模型一致，否则合成会失败。

prefix

str

是

音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-{prefix}-{唯一标识}`。

url

str

是

用于复刻音色的音频文件URL，要求公网可访问。

language\_hints

List\[str\]

否

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash、v3-plus和v3-flash模型支持。

辅助模型识别样本音频的语种，从而更准确地提取音色特征，提升复刻效果。若设置的语种与实际音频语种不符（例如为中文音频设置 `en`），系统将忽略该设置并自动检测语种。

此参数为数组，但当前版本仅处理第一个元素。

取值范围（因模型而异）：

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

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash和v3-flash模型支持。

音频预处理后用于声音复刻的参考音频最大时长（秒）。取值范围：\[3.0, 30.0\]。时间越长效果越好。

默认值：10.0。

enable\_preprocess

bool

否

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash和v3-flash模型支持。

是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。

默认值：false。

**返回值**：`str`，音色ID（voice\_id）。

### **list\_voice() - 查询音色列表**

**方法签名**：

```
def list_voice(self, prefix: str = None, page_index: int = 0, page_size: int = 10) -> list
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

### **query\_voice() - 查询音色详情**

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

### **update\_voice() - 更新音色**

**方法签名**：

```
def update_voice(self, voice_id: str, url: str, language_hints: List[str] = None,
                 max_prompt_audio_length: float = None, enable_preprocess: bool = None) -> None
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

新的音频文件URL。

language\_hints

List\[str\]

否

样本音频语种提示。

max\_prompt\_audio\_length

float

否

参考音频最大时长。

enable\_preprocess

bool

否

是否开启音频预处理。

### **delete\_voice() - 删除音色**

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

## **示例代码**

### **创建音色**

```
from dashscope.audio.tts_v2 import VoiceEnrollmentService

service = VoiceEnrollmentService()

# 避免频繁调用。每次调用都会创建新音色，达到配额上限后将无法创建。
voice_id = service.create_voice(
    target_model='cosyvoice-v3-plus',
    prefix='myvoice',
    url='https://your-audio-file-url'
    # language_hints=['zh'],
    # max_prompt_audio_length=10.0,
    # enable_preprocess=False
)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Voice ID: {voice_id}")
```

### **查询音色列表**

```
from dashscope.audio.tts_v2 import VoiceEnrollmentService

service = VoiceEnrollmentService()

# 按前缀筛选，或设为None查询所有
voices = service.list_voices(prefix='myvoice', page_index=0, page_size=10)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Found voices: {voices}")
```

### **查询特定音色**

```
from dashscope.audio.tts_v2 import VoiceEnrollmentService

service = VoiceEnrollmentService()
voice_id = 'cosyvoice-v3-plus-myvoice-xxxxxxxx'

voice_details = service.query_voice(voice_id=voice_id)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Voice Details: {voice_details}")
```

### **更新音色**

```
from dashscope.audio.tts_v2 import VoiceEnrollmentService

service = VoiceEnrollmentService()
service.update_voice(
    voice_id='cosyvoice-v3-plus-myvoice-xxxxxxxx',
    url='https://your-new-audio-file-url'
)
print(f"Update submitted. Request ID: {service.get_last_request_id()}")
```

### **删除音色**

```
from dashscope.audio.tts_v2 import VoiceEnrollmentService

service = VoiceEnrollmentService()
service.delete_voice(voice_id='cosyvoice-v3-plus-myvoice-xxxxxxxx')
print(f"Deletion submitted. Request ID: {service.get_last_request_id()}")
```
