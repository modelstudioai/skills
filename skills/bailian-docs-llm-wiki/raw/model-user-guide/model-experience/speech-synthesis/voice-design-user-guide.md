# 声音设计

通过自然语言描述创建自定义音色，试听预览后用于语音合成。

## 功能介绍

声音设计适用于快速原型验证、创意内容生产、游戏角色配音等场景。

**说明**创建音色无需提供音频样本。如需根据已有音频样本还原其声音，请使用[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)。

## 准备工作

-   [获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并将其[配置到环境变量](https://help.aliyun.com/zh/model-studio/get-api-key#20b17d4430qvt) `DASHSCOPE_API_KEY`。
    
-   获取业务空间 ID，将示例中的 `YOUR_WORKSPACE_ID` 替换为真实值。获取方式请参见[选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。
    
-   安装 [DashScope SDK](raw/model-api-reference/preparations/install-sdk.md) 和 `requests`：
    
    ```
    pip install -U dashscope requests
    ```
    

## 开始使用

Qwen-Audio-TTS 和 CosyVoice 使用相同的音色创建、预览和基础合成流程。以下以 `qwen-audio-3.1-tts-flash` 为例。

1.  **创建音色**：设置声音描述 `voice_prompt`、预览文本 `preview_text` 和目标模型 `target_model`，获取音色 ID。
2.  **保存预览音频**：解码返回的 `preview_audio.data`，保存为 WAV 文件，用于试听。
3.  **合成语音**：将创建音色时返回的 `voice_id` 作为 `voice`，使用绑定模型合成语音。

```
import base64
import os

import dashscope
import requests
from dashscope.audio.tts_v2 import AudioFormat, SpeechSynthesizer

api_key = os.environ["DASHSCOPE_API_KEY"]
workspace_id = "YOUR_WORKSPACE_ID"
target_model = "qwen-audio-3.1-tts-flash"

# 创建音色，并将返回的预览音频保存到本地。
response = requests.post(
    f"https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "voice-enrollment",
        "input": {
            "action": "create_voice",
            "target_model": target_model,
            "voice_prompt": "沉稳的中年男性播音员，音色低沉浑厚，富有磁性，语速平稳，吐字清晰，适合用于新闻播报或纪录片解说。",
            "preview_text": "各位听众朋友，大家好，欢迎收听晚间新闻。",
            "prefix": "announcer",
            "language_hints": ["zh"],
        },
        "parameters": {"sample_rate": 24000, "response_format": "wav"},
    },
    timeout=120,
)
response.raise_for_status()
output = response.json()["output"]
voice_id = output["voice_id"]
print(f"voice_id: {voice_id}")
with open("preview.wav", "wb") as f:
    f.write(base64.b64decode(output["preview_audio"]["data"]))

# 使用创建音色时指定的模型和返回的音色 ID 合成语音。
dashscope.api_key = api_key
dashscope.base_websocket_api_url = (
    f"wss://{workspace_id}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"
)
synthesizer = SpeechSynthesizer(
    model=target_model,
    voice=voice_id,
    format=AudioFormat.WAV_24000HZ_MONO_16BIT,
)
audio = synthesizer.call("今天天气晴朗，适合外出散步。祝你度过愉快的一天。")
with open("output.wav", "wb") as f:
    f.write(audio)
```

运行示例后，`preview.wav` 为预览音频，`output.wav` 为合成音频。保存打印的音色 ID，后续可使用该 ID 调用语音合成。

HTTP 请求示例、可选参数和返回字段请参见[声音设计 API 参考](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/voice-design-api-references.md)；合成参数请参见 [Qwen-Audio-TTS 客户端事件](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-client-events#h3runtask)。

## 声音描述指南

声音描述（`voice_prompt`）用于指定期望的声音特质。清晰、具体的描述有助于生成符合需求的音色。

### 描述建议

-   **具体**：使用“低沉”“清脆”“语速偏快”等声音特征，避免“好听”“普通”等模糊评价。
-   **多维**：组合性别、年龄、音调、语速和情感等维度，仅写“女声”难以描述出有特色的声音。
-   **客观**：描述可感知的声音特征，例如“音调偏高、充满活力”，避免“我最喜欢的声音”等主观表达。
-   **原创**：描述声音特质，不要求模仿名人、演员等特定人物。模型不支持指定模仿，相关请求也可能涉及版权风险。
-   **简洁**：减少重复的同义词和无意义的修饰。

可组合以下维度编写声音描述：

**维度**

**描述示例**

性别

男性、女性、中性

年龄

儿童 (5-12 岁)、青少年 (13-18 岁)、青年 (19-35 岁)、中年 (36-55 岁)、老年 (55 岁以上)

音调

高音、中音、低音、偏高、偏低

语速

快速、中速、缓慢、偏快、偏慢

情感

开朗、沉稳、温柔、严肃、活泼、冷静、治愈

特点

有磁性、清脆、沙哑、圆润、甜美、浑厚、有力

用途

新闻播报、广告配音、有声书、动画角色、语音助手、纪录片解说

### 描述示例

-   标准播音风格：吐字清晰精准，字正腔圆
-   年轻活泼的女性声音，语速较快，带有明显的上扬语调，适合介绍时尚产品
-   沉稳的中年男性，语速缓慢，音色低沉有磁性，适合朗读新闻或纪录片解说
-   温柔知性的女性，30 岁左右，语调平和，适合有声书朗读
-   可爱的儿童声音，大约 8 岁女孩，说话略带稚气，适合动画角色配音

**说明**相同描述可能生成不同的音色。创建后先试听预览音频；需要比较效果时，可多次生成后择优使用。

## 音色管理

-   **查询音色列表**：查看已有的自定义音色。
-   **查询音色详情**：查看音色绑定的模型、状态等信息。
-   **删除音色**：删除不再使用的音色，释放配额。

接口与参数说明请参见[声音设计 API 参考](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/voice-design-api-references.md)。

## 支持模型

#### 华北2（北京）

使用该地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key) 调用以下模型：

-   **Qwen-Audio-TTS**：qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
    
-   **CosyVoice**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash
    

**说明**CosyVoice 声音设计基于 FunAudioGen-VD 模型能力。

## 配额与限制

-   **音色数量**：每个阿里云百炼账号的自定义音色总数上限为 1000 个。声音复刻和声音设计共用该配额，不按模型分别计算。
    
    **说明**达到上限后，新的声音复刻或声音设计创建请求将失败。需先删除不再使用的音色，释放配额后再创建。
    
-   **声音描述**：`voice_prompt` 仅支持中文和英文，最大长度为 500 个字符。
    
-   **预览文本**：`preview_text` 仅支持中文和英文，长度为 15～200 个字符。
    
-   **模型绑定**：音色在创建时通过 `target_model` 绑定到语音合成模型，后续合成必须使用同一模型。
    

生成的音色可用于合成多种语言的语音，具体支持范围以目标语音合成模型为准。

## 计费说明

创建音色免费。

使用设计音色合成语音时，按目标语音合成模型计费。具体费用请参见[模型计费](raw/model-user-guide/test-1/model-pricing.md)。
