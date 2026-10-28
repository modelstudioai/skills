# 声音复刻

根据音频样本创建自定义音色，用于语音合成或实时语音对话。

## 功能介绍

声音复刻适用于个性化语音助手、品牌专属播报和有声内容定制等场景，无需训练模型。

**说明**如需通过自然语言描述创建音色，无需提供音频样本，请使用[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)。

## 准备工作

-   [获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并将其[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) `DASHSCOPE_API_KEY`。
    
-   获取业务空间 ID，将示例中的 `YOUR_WORKSPACE_ID`（SDK 示例中的 `{WorkspaceId}`）替换为真实值。获取方式请参见[地域与接入域名](raw/model-user-guide/get-started-with-models/regions.md)。
    
-   使用 HTTP 方式时，安装 Python HTTP 库 `requests`：
    
    ```
    pip install requests
    ```
    
-   使用 Python SDK 方式时，安装 [DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)（需 2.0.1 及以上版本）：
    
    ```
    # 本文档示例基于 DashScope Python SDK 2.0 编写，需 2.0.1 及以上版本
    pip install -U "dashscope>=2.0.1"
    ```
    
-   准备符合[音频要求](#vc02_audio_h2)的音频文件。Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 支持公网 URL 或 Base64 Data URI；MiniMax 仍使用公网 URL。以下示例使用[示例音频](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav)的 URL，本地音频的编码和传参方式请参见 [HTTP API](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-create-enrollment)。
    

## 开始使用

**说明**Qwen-Audio-TTS / Qwen-Audio-Realtime / CosyVoice 的复刻音色在创建时绑定到 `target_model`，不能跨模型使用。如需让多个模型使用同一段音频的声音，应为每个模型分别创建音色。

#### Qwen-Audio-TTS / CosyVoice

Qwen-Audio-TTS 和 CosyVoice 使用相同的音色创建和基础合成流程。以下以 `qwen-audio-3.1-tts-plus` 为例。

1.  **创建音色**：传入参考音频 URL（HTTP 方式还支持 Base64 Data URI，SDK 方式使用公网 URL），`target_model` 指定目标模型，`prefix` 为音色名称前缀。
2.  **合成语音**：将返回的音色 ID 传入 `voice`，使用同一个目标模型合成语音并保存音频。

#### Python SDK

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

target_model = "qwen-audio-3.1-tts-plus"

# 创建音色。
voice = client.audio.voices.create(
    target_model=target_model,
    prefix="myvoice",
    url="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav",
)
voice_id = voice.voice_id
print(f"voice_id: {voice_id}")

# 使用绑定模型和返回的音色 ID 合成语音。
audio = client.audio.tts.synthesize(
    "今天天气晴朗，适合外出散步。祝你度过愉快的一天。",
    model=target_model,
    voice=voice_id,
    format="wav",
    sample_rate=24000,
)
with open("output.wav", "wb") as f:
    f.write(audio)
```

#### HTTP

```
import os
import time
import requests

workspace_id = "YOUR_WORKSPACE_ID"
target_model = "qwen-audio-3.1-tts-plus"
base_url = f"https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1"
headers = {"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"}

response = requests.post(
    f"{base_url}/services/audio/tts/customization",
    headers=headers,
    json={
        "model": "voice-enrollment",
        "input": {
            "action": "create_voice",
            "target_model": target_model,
            "prefix": "myvoice",
            "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav",
        },
    },
    timeout=60,
)
response.raise_for_status()
voice_id = response.json()["output"]["voice_id"]
print(f"voice_id: {voice_id}")

for _ in range(30):
    response = requests.post(
        f"{base_url}/services/audio/tts/customization",
        headers=headers,
        json={
            "model": "voice-enrollment",
            "input": {"action": "query_voice", "voice_id": voice_id},
        },
        timeout=60,
    )
    response.raise_for_status()
    status = response.json()["output"]["status"]
    if status == "OK":
        break
    if status != "DEPLOYING":
        raise RuntimeError(f"Voice status: {status}")
    time.sleep(1)
else:
    raise TimeoutError("Voice is not ready")

response = requests.post(
    f"{base_url}/services/audio/tts/SpeechSynthesizer",
    headers=headers,
    json={
        "model": target_model,
        "input": {
            "text": "今天天气晴朗，适合外出散步。祝你度过愉快的一天。",
            "voice": voice_id,
            "format": "wav",
            "sample_rate": 24000,
        },
    },
    timeout=60,
)
response.raise_for_status()
audio_url = response.json()["output"]["audio"]["url"]
audio_response = requests.get(audio_url, timeout=60)
audio_response.raise_for_status()
with open("output.wav", "wb") as f:
    f.write(audio_response.content)
```

运行后，合成音频保存为 `output.wav`。保存打印的音色 ID，后续可继续使用。

#### Qwen-Audio-Realtime

Qwen-Audio-Realtime 的复刻音色用于自定义实时语音对话的回复声音。以下以 `qwen-audio-3.1-realtime-plus` 为例创建音色。

#### Python SDK

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

target_model = "qwen-audio-3.1-realtime-plus"

# 创建音色。
voice = client.audio.voices.create(
    target_model=target_model,
    prefix="myvoice",
    url="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav",
)
print(f"voice_id: {voice.voice_id}")
```

#### HTTP

```
import os
import time
import requests

workspace_id = "YOUR_WORKSPACE_ID"
target_model = "qwen-audio-3.1-realtime-plus"
base_url = f"https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1"
headers = {"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"}

response = requests.post(
    f"{base_url}/services/audio/tts/customization",
    headers=headers,
    json={
        "model": "voice-enrollment",
        "input": {
            "action": "create_voice",
            "target_model": target_model,
            "prefix": "myvoice",
            "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav",
        },
    },
    timeout=60,
)
response.raise_for_status()
voice_id = response.json()["output"]["voice_id"]
print(f"voice_id: {voice_id}")

for _ in range(30):
    response = requests.post(
        f"{base_url}/services/audio/tts/customization",
        headers=headers,
        json={
            "model": "voice-enrollment",
            "input": {"action": "query_voice", "voice_id": voice_id},
        },
        timeout=60,
    )
    response.raise_for_status()
    status = response.json()["output"]["status"]
    if status == "OK":
        break
    if status != "DEPLOYING":
        raise RuntimeError(f"Voice status: {status}")
    time.sleep(1)
else:
    raise TimeoutError("Voice is not ready")
```

建立实时语音对话连接后，在**首次** `session.update` 事件中，将 `session.voice` 设置为返回的音色 ID（替换下方的 `VOICE_ID`）。会话模型必须与创建音色时的 `target_model` 一致。

```
{
    "type": "session.update",
    "session": {
        "voice": "VOICE_ID"
    }
}
```

#### MiniMax

MiniMax 通过 HTTP API 创建音色，并支持非实时语音合成。

**创建音色**：用 `voice_id` 指定新音色的 ID，`audio_url` 指定可访问的音频 URL，`text` 指定试听文本。请求返回试听音频，费用见[计费说明](#vc07_billing_h3)。

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

**合成语音**：将创建时指定的 `voice_id` 传入 `voice_setting.voice_id`。

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

更多声音复刻参数与示例请参见 [HTTP API](raw/_short/voice-clone-design-http-api-8f39943e5a676aae.md)、[Python SDK](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/sound-reengraving/voice-clone-python-sdk.md)和 [Java SDK](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/sound-reengraving/voice-clone-java-sdk.md)。

使用复刻音色进行语音合成或实时语音对话的调用方式，请参见：

-   **Qwen-Audio-TTS**：[模型接入方式](raw/_short/qwen-audio-tts-model-access-6e664ddb54b00e5d.md)
-   **CosyVoice**：[模型接入方式](raw/_short/cosyvoice-model-access-80a06b5339b1723a.md)
-   **Qwen-Audio-Realtime**：[模型接入方式](raw/_short/qwen-audio-realtime-model-access-82f1eed54dbb343f.md)
-   **MiniMax**：[非实时语音合成 API 参考](raw/_short/minimax-speech-synthesis-36f3b02a593324ef.md)

## 音频要求

输入音频的质量会影响音色的相似度和自然度。按目标模型的规格准备样本，并参照下方录音建议减少噪声、混响和其他人声。

#### Qwen-Audio-TTS / Qwen-Audio-Realtime / CosyVoice

**项目**

**要求**

支持格式

WAV（16-bit）、MP3、M4A

音频时长

推荐 10～20 秒，最长不超过 60 秒。

文件大小

≤ 10 MB

采样率

≥ 16 kHz

声道

单声道或双声道。双声道音频仅处理首声道，首声道需包含有效人声。

内容

至少包含 5 秒连续清晰的朗读内容，其余部分仅允许短暂停顿（≤ 2 秒）。避免背景音乐、环境噪声和其他人声。使用正常语速的说话音频，不使用歌曲或唱歌录音。

支持语言

-   **Qwen-Audio-TTS / Qwen-Audio-Realtime**：中文（普通话、广东话、重庆话、东北话、甘肃话、贵州话、浙江话、河北话、河南话、湖北话、湖南话、江西话、宁波话、宁夏话、青岛话、陕西话、山西话、山东话、上海话、四川话、云南话）、英语、日语、韩语、俄语、法语、德语、葡萄牙语、泰语、印尼语、越南语、西班牙语、意大利语、马来西亚语、菲律宾语、阿拉伯语
-   **CosyVoice**：参考音频支持的语言因驱动音色的目标模型而异。

点击查看 CosyVoice 各模型支持的语言

-   **cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
-   **cosyvoice-v3-plus**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语
-   **cosyvoice-v2**：中文（普通话）、英文

#### MiniMax

**项目**

**要求**

支持格式

MP3、M4A、WAV

音频时长

不低于 10 秒，最长不超过 5 分钟

文件大小

≤ 20 MB

内容

音频应包含连续清晰的朗读内容（无背景音），停顿时长不超过 2 秒。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。

支持语言

无特殊限制

清晰、自然的录音有助于获得高质量的参考音频并保留声音特征。录音前可参考以下录音与操作建议。

点击查看录音与操作建议

**录音设备**

可使用手机、数字录音笔、专业录音机等。建议使用支持高采样率（≥ 24 kHz）录音的设备，以满足音频要求。

**录音环境**

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

**录音文案**

-   内容无特殊限制，建议与目标应用场景一致。
-   避免短句（如你好、是的），应使用完整句子。
-   保持语义连贯，朗读时避免频繁停顿（建议至少连续 3 秒无中断）。
-   录音全程保持一致的语速，避免开头或结尾语速过快导致合成时出现卡顿。
-   可加入适当情绪表达（如温暖、亲切、严肃），避免机械朗读。
-   不包含敏感词汇（如政治、色情、暴力相关内容），否则会导致复刻失败。

**操作建议**

以普通卧室为例，完成降噪和混响控制后：

1.  提前熟悉文案，设定角色语气，自然演绎。
2.  与录音设备保持约 10 厘米距离，避免喷麦或信号过弱。

## 音色管理

Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 使用相同的音色查询、更新与删除接口。具体接口与参数请参见[声音复刻 HTTP API 参考](raw/_short/voice-clone-design-http-api-8f39943e5a676aae.md)。

-   **查询音色列表**：查看账号下已有的自定义音色。
-   **查询音色详情**：查看创建时间、绑定模型等信息。
-   **更新音色**：替换参考音频，保留原有音色 ID。
-   **删除音色**：删除不再使用的音色，释放配额。

创建的音色默认长期有效。保存音色 ID，需要时可通过查询接口确认音色是否可用。

**说明**MiniMax 的音色查询与删除请参见[声音管理](https://help.aliyun.com/zh/model-studio/sound-management)。

## 支持模型

#### 华北2（北京）

使用该地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key) 调用以下模型：

-   **Qwen-Audio-TTS**：qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
    
-   **Qwen-Audio-Realtime**：qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash
    
-   **CosyVoice**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2
    
-   **MiniMax**：MiniMax/speech-2.8-hd、MiniMax/speech-02-hd、MiniMax/speech-2.8-turbo、MiniMax/speech-02-turbo
    

#### 新加坡

使用该地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key) 调用以下模型：

-   **Qwen-Audio-TTS**：qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
    
-   **CosyVoice**：cosyvoice-v3-plus、cosyvoice-v3-flash
    

## 配额与限制

-   **音色数量**：每个阿里云百炼账号的自定义音色总数上限为 1000 个。声音复刻和声音设计共用该配额，不按模型分别计算。
    
    **说明**
    
    -   达到上限后，新的声音复刻或声音设计创建请求将失败。需先删除不再使用的音色，释放配额后再创建。
    -   MiniMax 创建的音色不受上述数量配额约束。
    

## 计费说明

-   **Qwen-Audio-TTS / Qwen-Audio-Realtime / CosyVoice**：创建音色免费。使用复刻音色合成语音或进行实时语音对话时，按目标模型计费。具体费用请参见[模型计费](raw/model-user-guide/test-1/model-pricing.md)。
    
-   **MiniMax**：声音复刻本身不计费。复刻请求生成的试听音频按同步语音合成单价计费；首次使用复刻音色进行语音合成时，扣除 9.9 元音色解锁费用，且无免费额度。
