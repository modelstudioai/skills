# 非实时语音合成

通过 HTTP 将完整文本转换为语音，了解模型特性、快速调用方法和合成效果优化方式。

## 功能介绍

非实时语音合成通过 HTTP 一次提交完整文本，支持非流式和 SSE 流式输出。非流式返回的音频 URL 有效期为 24 小时，请及时下载保存；链接过期后可重新合成。流式输出逐段返回音频数据。

-   **多语言与方言**：根据目标语言选择模型和音色，也可通过指令指定方言。参见[方言](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#8a7604d333kut)。
-   **表现力控制**：通过自然语言指令调整语速、情感等表达，或在文本中插入情感与富语言标签。参见[指令控制](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_instruct_h3)和[情感与富语言标签](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_emtag_h3)。
-   **自定义音色**：通过[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)从音频样本创建音色，或通过[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)使用文字描述创建音色。
-   **精细控制与公式朗读**：使用 [SSML 与 LaTeX](raw/model-user-guide/model-experience/speech-synthesis/ssml-latex-user-guide.md)控制停顿、发音等效果，或将公式转换为语音。

**说明**

-   各模型及音色支持的能力有所不同，使用前请核对对应功能的支持范围。
-   需要分批输入文本时，请使用[实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)。

## 开始使用

-   [获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置到环境变量](https://help.aliyun.com/zh/model-studio/get-api-key#20b17d4430qvt) `DASHSCOPE_API_KEY`。使用与示例地域对应的 API Key。
    
-   使用业务空间专属域名时，将代码中的 `YOUR_WORKSPACE_ID` 替换为该地域的[业务空间 ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。
    
-   安装示例依赖：
    
    ```
    pip install requests
    ```
    

#### Qwen-Audio-TTS（推荐）

以下使用华北2（北京）地域的 `qwen-audio-3.1-tts-flash` 和系统音色 `longanhuan_v3.1`，演示非流式和流式输出。

#### 非流式输出

```
import os
import requests

response = requests.post(
    'https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer',
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
    json={
        "model": "qwen-audio-3.1-tts-flash",
        "input": {
            "text": "你好，欢迎使用阿里云百炼。",
            "voice": "longanhuan_v3.1",
            "format": "wav",
            "sample_rate": 24000
        }
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

运行后，音频保存在当前目录的 `output.wav` 文件中。

#### 流式输出

以下示例逐行打印 SSE 返回事件。事件中的 `output.audio.data` 为 Base64 编码的音频片段。

```
import os
import requests

response = requests.post(
    'https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer',
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}", "X-DashScope-SSE": "enable"},
    json={
        "model": "qwen-audio-3.1-tts-flash",
        "input": {
            "text": "你好，欢迎使用阿里云百炼。",
            "voice": "longanhuan_v3.1",
            "format": "wav",
            "sample_rate": 24000
        }
    },
    stream=True,
    timeout=60,
)
response.raise_for_status()
for line in response.iter_lines():
    print(line.decode("utf-8"))
response.close()
```

#### CosyVoice

以下使用北京地域的 `cosyvoice-v3-flash` 和系统音色 `longanyang`，演示非流式和流式输出。

#### 非流式输出

```
import os
import requests

response = requests.post(
    'https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer',
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
    json={
        "model": "cosyvoice-v3-flash",
        "input": {
            "text": "你好，欢迎使用阿里云百炼。",
            "voice": "longanyang",
            "format": "wav",
            "sample_rate": 24000
        }
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

运行后，音频保存在当前目录的 `output.wav` 文件中。

#### 流式输出

以下示例逐行打印 SSE 返回事件。事件中的 `output.audio.data` 为 Base64 编码的音频片段。

```
import os
import requests

response = requests.post(
    'https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer',
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}", "X-DashScope-SSE": "enable"},
    json={
        "model": "cosyvoice-v3-flash",
        "input": {
            "text": "你好，欢迎使用阿里云百炼。",
            "voice": "longanyang",
            "format": "wav",
            "sample_rate": 24000
        }
    },
    stream=True,
    timeout=60,
)
response.raise_for_status()
for line in response.iter_lines():
    print(line.decode("utf-8"))
response.close()
```

#### MiniMax

#### 非流式输出

```
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "MiniMax/speech-2.8-hd",
  "input": {
    "text": "今天天气真不错，适合出去走走。",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1,
      "vol": 1,
      "pitch": 0,
      "emotion": "happy"
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

#### 流式输出

```
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
  "model": "MiniMax/speech-2.8-hd",
  "input": {
    "text": "今天天气真不错，适合出去走走。",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1,
      "vol": 1,
      "pitch": 0,
      "emotion": "happy"
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

## 合成效果优化

### 语言与发音

数字、缩写或符号的读法不符合预期时，可通过 `language_hints` 指定合成目标语言，或通过 `hot_fix` 定义词语发音与文本替换。参数适用模型和配置方法请参见对应的 [Qwen-Audio-TTS API](raw/_short/qwen-audio-tts-http-api-6a5232db21a53ba2.md)或 [CosyVoice API](raw/_short/cosyvoice-tts-http-api-5bce129a0403d285.md)。

需要控制停顿、数字读法或字词发音时，可使用 SSML。Qwen-Audio-TTS 和 CosyVoice 的适用模型、音色、接口与标签用法，请参见 [SSML 与 LaTeX](raw/model-user-guide/model-experience/speech-synthesis/ssml-latex-user-guide.md)。

### 指令控制

在请求的 `input` 中增加 `instruction`，用自然语言描述语速、情感或说话方式，控制合成语音的表现。

**说明**如需创建具有特定性别、年龄或音色特质的新音色，或参考声音描述的编写建议与示例，请参见[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)。

#### Qwen-Audio-TTS

`qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash` 的系统音色、复刻音色和设计音色均支持在合成请求中通过 `instruction` 设置自然语言指令。

在 Qwen-Audio-TTS 的开始使用示例中，为 `input` 增加以下字段，可放慢语速：

```
{"instruction": "请用非常缓慢的语速说话，每个字都慢慢说。"}
```

#### CosyVoice

**说明**CosyVoice 的 `instruction` 长度不能超过 100 个字符。计数时，汉字（包括简体、繁体汉字、日文汉字和韩文汉字）按 2 个字符计算，其他字符（包括标点符号、字母、数字、假名和谚文）按 1 个字符计算。

**模型**

**可使用的音色**

**指令要求**

**指令文本语言**

`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`

复刻音色、设计音色

无系统音色。

自然语言指令。

中文、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语。

`cosyvoice-v3-plus`

系统音色

按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)中的固定格式和内容填写。

复刻音色、设计音色不支持指令控制。

按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)指定的语言填写。

`cosyvoice-v3-flash`

系统音色

按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)中的固定格式和内容填写。

中文。

复刻音色、设计音色

自然语言指令。

中文、英文、法语、德语、日语、韩语、俄语。

MiniMax 通过 `input.voice_setting.speed`、`pitch` 和 `emotion` 设置语速、音调和情感，具体取值请参见 [API 参考](raw/_short/minimax-synchronous-speech-synthesis-api-bbe4c9f0093c0534.md)。

### 方言

通过方言功能，可将文本合成为河南话、四川话等中文方言语音。方言的选择方式取决于模型和音色类型。

#### Qwen-Audio-TTS

-   **系统音色**：从 [Qwen-Audio-TTS 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)中选择支持目标方言的音色。直接支持该方言的音色无需额外设置；支持方言指令的音色使用指令控制参数 `instruction` 指定。
-   **复刻音色**：通过指令控制参数 `instruction` 指定方言。
-   **设计音色**：暂不支持方言。

对于支持方言指令的音色，在请求的 `input` 中设置 `instruction="请讲上海话。"`，可将中文文本合成为上海话。

#### CosyVoice

-   **系统音色**：选择直接支持目标方言的音色，例如 `longshange_v3`；或选择支持方言指令的音色，例如 `longanhuan_v3`，按[音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)的格式填写指令。
-   **复刻音色**：使用支持指令控制的模型，通过 `instruction` 指定方言。
-   **设计音色**：暂不支持方言。

**说明**`cosyvoice-v3-plus` 的复刻音色不支持通过指令指定方言。

使用 CosyVoice 的开始使用示例时，将 `input` 替换为以下内容，可使用 `longanhuan_v3` 输出河南话：

```
{
  "text": "叫你去买盐，你买回来一袋面，这不是弄啥嘞吗！",
  "voice": "longanhuan_v3",
  "format": "wav",
  "sample_rate": 24000,
  "instruction": "请用河南话表达。"
}
```

Qwen3-TTS 使用支持目标方言的系统音色，参见 [Qwen3-TTS 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-tts-voice-list.md)。

### 情感与富语言标签

**说明**适用于 `qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus` 和 `qwen-audio-3.0-tts-flash`。

情感与富语言标签可控制语音的情感和风格，并在指定位置加入笑声、叹息等拟声效果。将标签直接写入待合成文本 `text`，无需额外参数。

#### 使用示例

以下文本先使用兴奋语气，在指定位置插入笑声后继续合成正文：

```
[excited]今天的天气真不错！[laughing]我们一起出去玩吧！
```

以下文本在第二句切换为兴奋语气：

```
[serious]请注意安全事项。[excited]好了，现在让我们开始吧！
```

#### 支持标签

#### 控制类标签

控制类标签设置后续文本的情感或风格，直到出现下一个控制类标签；长句被自动切分时，作用范围以切分后的文本为界。

**标签**

**说明**

`[sad]`

悲伤

`[amazed]`

惊叹

`[deep and loud shouting]`

深沉大声呐喊

`[trembling]`

颤抖

`[angry]`

愤怒

`[excited]`

兴奋

`[sarcastic]`

讽刺

`[curious]`

好奇

`[like dracula]`

吸血鬼语气

`[bored]`

无聊

`[tired]`

疲倦

`[scornful]`

轻蔑

`[shouting]`

大喊

`[asmr]`

ASMR 轻声

`[panicked]`

惊慌

`[mischievously]`

调皮

`[empathetic]`

共情

`[whispers]`

低声耳语

`[reluctantly]`

不情愿

`[crying]`

哭泣

`[serious]`

严肃

`[very slowly]`

非常缓慢

`[very fast]`

非常快速

#### 富语言类标签

富语言类标签在当前位置插入拟声效果，不改变前后文本的情感风格。

**标签**

**说明**

`[gasp]`

倒吸气

`[sighing]`

叹息

`[clears throat]`

清嗓

`[giggles]`

咯咯笑

`[laughing]`

大笑

`[cough]`

咳嗽

`[snorts]`

哼声、嗤笑

## 支持模型

#### 华北2（北京）

使用该地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 和[接入域名](raw/model-user-guide/get-started-with-models/regions.md)调用以下模型：

-   **Qwen-Audio-TTS**：`qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`
-   **CosyVoice**：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`、`cosyvoice-v2`
-   **Qwen3-TTS**：`qwen3-tts-flash`
-   **MiniMax**：`MiniMax/speech-2.8-hd`、`MiniMax/speech-02-hd`、`MiniMax/speech-2.8-turbo`、`MiniMax/speech-02-turbo`

#### 新加坡

使用该地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 和[接入域名](raw/model-user-guide/get-started-with-models/regions.md)调用以下模型：

-   **Qwen-Audio-TTS**：`qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`
-   **Qwen3-TTS**：`qwen3-tts-flash`

系统音色与试听分别参见 [Qwen-Audio-TTS](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)、[CosyVoice](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)和 [Qwen3-TTS](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-list#261bc7f209ri2) 音色列表。使用复刻或设计音色时，合成模型须与创建音色时指定的目标模型一致。

## API 参考

-   [Qwen-Audio-TTS HTTP API](raw/_short/qwen-audio-tts-http-api-6a5232db21a53ba2.md)
-   [CosyVoice HTTP API](raw/_short/cosyvoice-tts-http-api-5bce129a0403d285.md)
-   [Qwen3-TTS API](raw/_short/qwen-tts-api-88cc336b17a3a583.md)
-   [MiniMax 同步语音合成 API](raw/_short/minimax-synchronous-speech-synthesis-api-bbe4c9f0093c0534.md)
