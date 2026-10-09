# 声音复刻

声音复刻（Voice Cloning）只需提供一段 10~20 秒的音频样本，即可生成高度相似的定制音色，无需模型训练。

## 概述

适用于个性化语音助手、品牌专属播报、有声内容定制化等场景。

阿里云百炼平台提供以下模型系列的声音复刻能力：

-   **Qwen-Audio-TTS** / **CosyVoice**：通过 DashScope SDK 或 HTTP API 创建音色，支持实时与非实时语音合成，可用于华北2（北京）和新加坡地域。
-   **MiniMax**：通过 HTTP API 创建音色，仅支持非实时语音合成，仅限华北2（北京）地域使用。
-   **Qwen-Audio-Realtime**：Qwen-Audio-Realtime 是实时语音对话模型（非语音合成模型），声音复刻用于自定义对话模型回复时的 TTS 音色。通过 DashScope SDK 或 HTTP API 创建音色，仅支持华北2（北京）地域。
-   **Qwen-TTS**：通过 HTTP API 创建音色，支持实时与非实时语音合成，可用于华北2（北京）和新加坡地域。

如需了解各模型系列的详细对比和选型建议，请参见[语音合成](raw/model-user-guide/model-experience/speech-synthesis/tts-model.md)。

## 前提条件

1.  已[配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并将其[设置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
2.  如果通过 DashScope SDK 调用，需要[安装最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。
3.  **准备音频文件**：音频需符合[音频要求](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc02_audio_h2)。

## 快速开始

声音复刻的使用分为以下三步：

1.  **准备音频**：准备一段符合[音频要求](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc02_audio_h2)的音频文件。
2.  **创建音色**：调用声音复刻接口上传音频创建音色，通过`target_model`指定绑定的语音合成模型。
3.  **使用音色合成语音**：调用语音合成接口，传入创建音色时返回的音色 ID。

### Qwen-Audio-TTS 声音复刻

**重要**Qwen-Audio-TTS 声音复刻支持华北2（北京）地域和新加坡地域。

**步骤一：创建音色**

调用声音复刻 API 上传音频并创建音色。`url`参数传入音频文件的可访问 URL 地址，`prefix`参数作为音色名称前缀。

以下为华北2（北京）地域的配置，若使用新加坡地域的模型，需将域名替换为：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`（将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。

```
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "qwen-audio-3.0-tts-flash",
        "prefix": "myvoice",
        "url": "https://your-audio-url.wav"
    }
}'
```
**步骤二：使用复刻音色合成语音**

将上一步返回的`voice_id`值填入以下请求中。

```
# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

# 声音复刻、语音合成要使用相同的模型
model = "qwen-audio-3.0-tts-flash"
# 将voice参数替换为声音复刻生成的专属音色
voice = "voice_id"

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(model=model, voice=voice)
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("今天天气怎么样？")
# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

### Qwen-Audio-Realtime 声音复刻

**重要**Qwen-Audio-Realtime 声音复刻仅支持华北2（北京）地域，音频要求与 Qwen-Audio-TTS 相同。

**步骤一：创建音色**

通过 DashScope SDK 或 HTTP API 调用声音复刻接口，上传音频并创建音色。`target_model` 参数填入实时语音对话模型名称，`prefix` 参数作为音色名称前缀。

#### Python

```
import os
import requests

# 若没有配置环境变量，请用阿里云百炼 API Key 将下行替换为：api_key = "sk-xxx"
api_key = os.environ.get('DASHSCOPE_API_KEY')

# Qwen-Audio-Realtime 仅支持华北2（北京）地域，请将 {WorkspaceId} 替换为真实的业务空间 ID
url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization'

response = requests.post(
    url,
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'voice-enrollment',
        'input': {
            'action': 'create_voice',
            'target_model': 'qwen-audio-3.1-realtime-plus',
            'prefix': 'myvoice',
            'url': 'https://your-audio-url.wav'
        }
    }
)
result = response.json()
print('voice_id:', result['output']['voice_id'])
```

#### cURL

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "qwen-audio-3.1-realtime-plus",
        "prefix": "myvoice",
        "url": "https://your-audio-url.wav"
    }
}'
```

**步骤二：在实时语音对话中使用复刻音色**

将上一步返回的 `voice_id` 填入实时语音对话 `session.update` 事件的 `voice` 参数中，详见[音色配置](https://help.aliyun.com/zh/model-studio/fun-audiochat-realtime#fc60h311)。

```
{
    "type": "session.update",
    "session": {
        "voice": "qwen-audio-3.1-realtime-plus-myvoice-xxxxxx"
    }
}
```

### CosyVoice 声音复刻

**重要**CosyVoice 声音复刻支持华北2（北京）地域（v3.5/v3/v2/v1 系列）和新加坡地域（cosyvoice-v3-plus）。

新加坡地域的 `cosyvoice-v3-flash` 暂不支持使用复刻音色合成语音。如需在新加坡地域使用复刻音色，请改用 `qwen-audio-3.0-tts-flash`。

**步骤一：创建音色**

调用声音复刻 API 上传音频并创建音色。`url`参数传入音频文件的可访问 URL 地址，`prefix`参数作为音色名称前缀。

以下为华北2（北京）地域的配置，若使用新加坡地域的模型，需将域名替换为：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "cosyvoice-v3.5-plus",
        "prefix": "myvoice",
        "url": "https://your-audio-url.wav"
    }
}'
```
**步骤二：使用复刻音色合成语音**

将上一步返回的`voice_id`值填入以下请求中。

```
# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_websocket_api_url='wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

# 声音复刻、语音合成要使用相同的模型
model = "cosyvoice-v3.5-plus"
# 将voice参数替换为声音复刻生成的专属音色
voice = "voice_id"

# 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
synthesizer = SpeechSynthesizer(model=model, voice=voice)
# 发送待合成文本，获取二进制音频
audio = synthesizer.call("今天天气怎么样？")
# 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

# 将音频保存至本地
with open('output.mp3', 'wb') as f:
    f.write(audio)
```

### MiniMax 声音复刻

MiniMax 声音复刻仅在华北2（北京）地域可用。提交复刻请求后，系统会生成一段试听音频（按同步语音合成单价计费）。首次使用复刻音色进行语音合成时，需支付 9.9 元音色解锁费用。

**步骤一：创建音色**

调用音色复刻 API 上传音频并创建音色。`voice_id`参数用于指定新音色的 ID，`audio_url`参数传入音频文件的可访问 URL 地址。

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json; charset=utf-8' \
-d '{
    "input": {
      "action": "voice_clone",
      "voice_id": "my-custom-voice",
      "audio_url": "https://your-audio-url.wav",
      "text": "你说是什么就是什么"
    },
    "model": "MiniMax/speech-2.8-turbo"
  }'
```
**步骤二：使用复刻音色合成语音**

将上一步指定的`voice_id`值填入以下请求中。

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "MiniMax/speech-2.8-turbo",
  "input": {
    "text": "今天天气怎么样？",
    "voice_setting": {
      "voice_id": "my-custom-voice",
      "speed": 1,
      "vol": 1,
      "pitch": 0
    },
    "audio_setting": {
      "sample_rate": 32000,
      "bitrate": 128000,
      "format": "mp3",
      "channel": 1
    }
  }
}'
```

### Qwen-TTS 声音复刻

示例使用本地音频文件`voice.mp3`，运行时请替换为实际路径。

**重要**创建音色时的`target_model`必须与语音合成时使用的模型完全一致，否则合成将失败。

#### Python

```
import os
import requests
import base64
import pathlib
import dashscope

# ======= 常量配置 =======
DEFAULT_TARGET_MODEL = "qwen3-tts-vc-2026-01-22"  # 声音复刻、语音合成要使用相同的模型
DEFAULT_PREFERRED_NAME = "guanyu"
DEFAULT_AUDIO_MIME_TYPE = "audio/mpeg"
VOICE_FILE_PATH = "voice.mp3"  # 用于声音复刻的本地音频文件的相对路径

def create_voice(file_path: str,
                 target_model: str = DEFAULT_TARGET_MODEL,
                 preferred_name: str = DEFAULT_PREFERRED_NAME,
                 audio_mime_type: str = DEFAULT_AUDIO_MIME_TYPE) -> str:
    """
    创建音色，并返回 voice 参数
    """
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    file_path_obj = pathlib.Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"音频文件不存在: {file_path}")

    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f"data:{audio_mime_type};base64,{base64_str}"

    # 以下为华北2（北京）地域的配置。
    url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
    payload = {
        "model": "qwen-voice-enrollment", # 不要修改该值
        "input": {
            "action": "create",
            "target_model": target_model,
            "preferred_name": preferred_name,
            "audio": {"data": data_uri}
        }
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"创建 voice 失败: {resp.status_code}, {resp.text}")

    try:
        return resp.json()["output"]["voice"]
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"解析 voice 响应失败: {e}")

if __name__ == '__main__':
    # 以下为华北2（北京）地域的配置。
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    text = "今天天气怎么样？"
    response = dashscope.MultiModalConversation.call(
        model=DEFAULT_TARGET_MODEL,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice=create_voice(VOICE_FILE_PATH), # 将voice参数替换为复刻生成的专属音色
        stream=False
    )
    print(response)
```

#### cURL

**步骤一：创建音色**

将`data`替换为实际音频文件的公网 URL 或 Base64 编码的 Data URI（格式为 `data:{MIME_type};base64,{base64_data}`）。

以下为华北2（北京）地域的配置。

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "create",
        "target_model": "qwen3-tts-vc-2026-01-22",
        "preferred_name": "guanyu",
        "audio": {
            "data": "https://xxx.wav"
        }
    }
}'
```
**步骤二：使用复刻音色合成语音**

将 `YOUR_VOICE_ID` 替换为上一步返回的 `voice` 值。

Qwen-TTS 系列创建音色接口的返回体中，音色 ID 位于 `output.voice` 字段；其他模型系列的创建音色接口返回的是 `voice_id` 字段，两者均表示音色 ID，注意字段名差异。

以下为华北2（北京）地域的配置。

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-tts-vc-2026-01-22",
    "input": {
        "text": "今天天气怎么样？",
        "voice": "YOUR_VOICE_ID"
    }
}'
```

## 音频要求

输入音频的质量直接决定复刻效果。不同模型系列对音频的具体要求有所差异，请按照目标模型的要求准备音频样本。

#### Qwen-Audio-TTS / Qwen-Audio-Realtime

**项目**

**要求**

**支持格式**

WAV (16bit)、MP3、M4A

**音频时长**

推荐 10~20 秒，最长不超过 60 秒

**文件大小**

≤ 10 MB

**采样率**

≥ 16 kHz

**声道**

单声道或双声道。双声道音频仅处理首声道，请确保首声道包含有效人声。

**内容**

音频必须包含至少 5 秒连续清晰的朗读内容（无背景音），其余部分仅允许短暂停顿（≤ 2 秒）。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。

**支持语言**

中文（普通话、广东话、重庆话、东北话、甘肃话、贵州话、浙江话、河北话、河南话、湖北话、湖南话、江西话、宁波话、宁夏话、青岛话、陕西话、山西话、山东话、上海话、四川话、云南话）、英语、日语、韩语、俄语、法语、德语、葡萄牙语、泰语、印尼语、越南语、西班牙语、意大利语、马来西亚语、菲律宾语、阿拉伯语

#### CosyVoice

**项目**

**要求**

**支持格式**

WAV (16bit)、MP3、M4A

**音频时长**

推荐 10~20 秒，最长不超过 60 秒

**文件大小**

≤ 10 MB

**采样率**

≥ 16 kHz

**声道**

单声道或双声道。双声道音频仅处理首声道，请确保首声道包含有效人声。

**内容**

音频必须包含至少 5 秒连续清晰的朗读内容（无背景音），其余部分仅允许短暂停顿（≤ 2 秒）。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。

**支持语言**

因驱动音色的语音合成模型（通过 `target_model` 参数指定）而异：

-   **cosyvoice-v3.5-plus、cosyvoice-v3.5-flash**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
    
-   **cosyvoice-v3-plus**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语
    
-   **cosyvoice-v3-flash**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
    
-   **cosyvoice-v1、****cosyvoice-v2**：中文（普通话）、英文
    

#### MiniMax

**项目**

**要求**

**支持格式**

MP3、M4A、WAV

**音频时长**

不低于 10 秒，最长不超过 5 分钟

**文件大小**

≤ 20 MB

**内容**

音频应包含连续清晰的朗读内容（无背景音），停顿时长不超过 2 秒。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。

**支持语言**

无特殊限制

#### Qwen-TTS

**项目**

**要求**

**支持格式**

WAV (16bit)、MP3、M4A

**音频时长**

推荐 10~20 秒，最长不超过 60 秒

**文件大小**

≤ 10 MB

**采样率**

≥ 24 kHz

**声道**

单声道

**内容**

音频必须包含至少 3 秒连续清晰的朗读内容（无背景音），其余部分仅允许短暂停顿（≤ 2 秒）。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。

**支持语言**

中文、英文、德语、意大利语、葡萄牙语、西班牙语、日语、韩语、法语、俄语

**说明**为获得最佳复刻效果，建议参照[录音建议](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc_rec_h2)准备样本。

## 录音建议

高质量的输入音频是获得优质复刻效果的基础。

### 录音设备

可使用手机、数字录音笔、专业录音机等。建议使用支持高采样率（≥ 24 kHz）录音的设备，以满足音频要求。

### 录音环境

**场地**

-   建议在 10 平方米以内的小型封闭空间录音。
-   优先选择配有吸音材料（如吸音棉、地毯、窗帘）的房间。
-   避免空旷大厅、会议室、教室等高混响场所。

**噪音控制**

-   室外噪音：关闭门窗，避免交通、施工等干扰。
-   室内噪音：关闭空调、风扇、日光灯镇流器等设备；可通过手机录制环境音并放大播放，识别潜在噪音源。

**混响控制**

-   混响会导致声音模糊、清晰度下降。
-   减少光滑表面反射：拉上窗帘、打开衣柜门、铺放衣物或床单覆盖桌面/柜面。
-   利用不规则物体（如书架、软包家具）实现声波漫反射。

### 录音文案

-   内容无特殊限制，建议与目标应用场景一致。
-   避免短句（如你好、是的），应使用完整句子。
-   保持语义连贯，朗读时避免频繁停顿（建议至少连续 3 秒无中断）。
-   录音全程保持一致的语速，避免开头或结尾语速过快导致合成时出现卡顿。
-   可加入适当情绪表达（如温暖、亲切、严肃），避免机械朗读。
-   不包含敏感词汇（如政治、色情、暴力相关内容），否则会导致复刻失败。

### 操作建议

以普通卧室为例，完成降噪和混响控制后：

1.  提前熟悉文案，设定角色语气，自然演绎。
2.  与录音设备保持约 10 厘米距离，避免喷麦或信号过弱。

## 管理自定义音色

音色创建完成后，您可以通过 API 对已有音色进行查询和管理（Qwen-Audio-TTS、Qwen-Audio-Realtime、Qwen-TTS 和 CosyVoice 支持）。Qwen-Audio-Realtime 的音色查询与删除接口与 Qwen-Audio-TTS 完全相同。

**重要**MiniMax 仅支持创建音色，不支持查询和删除等音色管理操作。

-   **查询音色列表**：获取当前账号下所有自定义音色的列表。
-   **查询音色详情**（仅 Qwen-Audio-TTS / Qwen-Audio-Realtime / CosyVoice）：查看指定音色的详细信息，如创建时间、绑定的语音合成模型等。
-   **删除音色**：删除不再需要的自定义音色，释放配额。

各模型的 API 接口和参数详情请参见[API 参考](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc06_apiref_h2)。

## 配额与计费

### 音色配额与自动清理

-   **音色总数限制**：每个阿里云百炼账号下，Qwen-Audio-TTS / Qwen-Audio-Realtime / CosyVoice 与 Qwen-TTS 分别最多可创建 1000 个自定义音色（两类配额独立计算）。达到上限后，新的创建请求将直接失败并返回错误，系统不会自动删除最早创建的复刻音色。如需创建新音色，请先删除不需要的音色以释放配额，或等待未被使用的音色自动清理（详见下方自动清理规则）。
-   **上限后创建行为**：达到 1000 个音色上限后，继续调用创建音色接口将直接返回失败错误，系统不会自动淘汰最早创建的复刻音色来腾出空间。需手动删除不需要的音色释放配额后才能继续创建。
-   **自动清理规则**：若单个音色在过去 1 年内未被用于任何语音合成请求，系统将自动删除该音色。

**重要**MiniMax 创建的音色不受上述配额与清理规则约束。

### 计费规则

-   **Qwen-Audio-TTS** / **Qwen-Audio-Realtime** / **CosyVoice**：创建音色免费。
    
-   **MiniMax**：声音复刻本身不计费。首次使用复刻音色进行语音合成时，扣除 9.9 元音色解锁费用，且无免费额度。
    
-   **Qwen-TTS**：按 0.01 元/个 计费，创建失败不计费。
    
    **免费额度**（仅北京地域提供）：
    
    -   阿里云百炼开通后 90 天内，可享 1000 次免费音色创建机会。
    -   创建失败不占用免费次数。
    -   删除音色不会恢复免费次数。
    -   免费额度用完或超出 90 天有效期后，创建音色将按 0.01 元/个 的价格计费。

## 支持的模型与地域

#### 华北2（北京）

调用以下模型时，请选择北京地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-TTS：**qwen-audio-3.0-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash
    
-   **Qwen-Audio-Realtime：**qwen-audio-3.1-realtime-plus、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash
    
-   **CosyVoice：**cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2、cosyvoice-v1
    
-   **MiniMax**：MiniMax/speech-2.8-hd、MiniMax/speech-02-hd、MiniMax/speech-2.8-turbo、MiniMax/speech-02-turbo
    
-   **Qwen-TTS**：
    
    -   **Qwen3-TTS-VC-Realtime：**qwen3-tts-vc-realtime-2026-01-15（最新快照版）、qwen3-tts-vc-realtime-2025-11-27（快照版）
    -   **Qwen3-TTS-VC**：qwen3-tts-vc-2026-01-22（最新快照版）

#### 新加坡

调用以下模型时，请选择新加坡地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-TTS**：qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
    
-   **CosyVoice**：cosyvoice-v3-plus（`cosyvoice-v3-flash` 暂不支持在新加坡地域使用复刻音色合成语音，请改用 `qwen-audio-3.0-tts-flash`）
    
-   **Qwen-TTS**：
    
    -   **Qwen3-TTS-VC-Realtime：**qwen3-tts-vc-realtime-2026-01-15（最新快照版）、qwen3-tts-vc-realtime-2025-11-27（快照版）
    -   **Qwen3-TTS-VC**：qwen3-tts-vc-2026-01-22（最新快照版）

## API 参考

[声音复刻API参考](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/sound-reengraving.md)

## 常见问题

### Q：创建音色后可以用于不同的语音合成模型吗？

不可以。音色在创建时通过`target_model`绑定到特定的语音合成模型，不能跨模型使用。如果您需要在多个模型上使用同一段音频的声音，请为每个模型分别创建音色。

### Q：复刻音色的有效期是多久？

Qwen-Audio-TTS、Qwen-Audio-Realtime、Qwen-TTS 和 CosyVoice 创建的音色默认长期有效。若单个音色在过去 1 年内未被用于任何语音合成请求，系统将自动删除该音色，详情请参见[音色配额与自动清理](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_count_h3)。建议妥善保存音色 ID，需要时可通过查询接口确认音色是否仍然可用。

### Q：音频质量不好会影响复刻效果吗？

输入音频的质量直接影响复刻效果。背景噪音、混响、多人声等问题都会降低复刻音色的相似度和自然度。建议参照[音频要求](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc02_audio_h2)和[录音建议](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc_rec_h2)准备样本。
