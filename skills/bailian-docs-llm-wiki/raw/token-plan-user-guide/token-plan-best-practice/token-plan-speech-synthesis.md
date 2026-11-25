# 接入语音合成模型

在 Agent 工具中调用 Token Plan 语音合成模型，将文本转为音频并下载到本地。

<a id="支持的模型"></a>

<a id="tp-tts-models"></a>

## 支持的模型

| 模型 | 能力 |
| --- | --- |
| `qwen-audio-3.0-tts-plus` | 语音合成 |

更多模型以 [个人版](../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)和[团队版](../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持的模型 为准。

<a id="前提"></a>

<a id="tp-tts-prereq"></a>

## 前提

-   已订阅 Token Plan，并获取以 `sk-sp-` 开头的 API Key。获取方式见[接入概览](token-plan-integration-overview.md#tp-ext-prereq)。
-   本地已安装 Python 3.9 及以上版本。
-   使用的 AI 编程工具支持 Slash Command。其他工具的配置路径见[其他工具](token-plan-integration-overview.md#tp-ext-tools)。

<a id="接口"></a>

<a id="tp-tts-endpoint"></a>

## 接口

`POST https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`

请求头使用 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`。响应返回音频 URL。

<a id="步骤一-创建-slash-command"></a>

<a id="tp-tts-step1"></a>

## 步骤一：创建 Slash Command

将套餐 API Key 配置为环境变量 `$ANTHROPIC_AUTH_TOKEN`。

在项目根目录创建 `.claude/commands/text-to-speech.md`，写入以下内容：

<a id="code-block"></a>

````text
调用 Token Plan 语音合成 API，将文本转为音频文件并下载到本地。

待合成文本：$ARGUMENTS

## 步骤

1. 提取 text（待合成文本）、voice（默认 longanhuan_v3.6）、format（默认 mp3）、sample_rate（默认 22050）。如果指定了模型，使用指定的模型名；否则默认 qwen-audio-3.0-tts-plus。
2. 使用 Bash 工具执行以下命令合成语音并下载：

```bash
RESPONSE=$(curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-audio-3.0-tts-plus",
    "input": {
      "text": "<text>",
      "voice": "<voice>",
      "format": "<format>",
      "sample_rate": <sample_rate>
    }
  }')

AUDIO_URL=$(printf '%s' "$RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["output"]["audio"]["url"])')
curl -s -o "speech_$(date +%Y%m%d_%H%M%S).<format>" "$AUDIO_URL"
```

3. 输出下载后的音频文件路径。
````

<a id="步骤二-合成语音"></a>

<a id="tp-tts-step2"></a>

## 步骤二：合成语音

在 Claude Code 中输入 `/text-to-speech 你好，欢迎使用百炼`。如需更换音色，在指令中写明音色，例如 `/text-to-speech 用 longanlingxin 说：你好`。

<a id="请求参数"></a>

<a id="tp-tts-params"></a>

## 请求参数

| 参数 | 必选 | 说明 |
| --- | --- | --- |
| `model` | 是 | 语音合成模型 ID。 |
| `input.text` | 是 | 待合成文本。 |
| `input.voice` | 是 | 音色，例如 `longanhuan_v3.6`。 |
| `input.format` | 否 | 音频格式，支持 `mp3`、`pcm`、`wav`、`opus`，默认 `mp3`。 |
| `input.sample_rate` | 否 | 采样率，默认 `22050`。 |

更多参数见 [Qwen-Audio-TTS 语音合成 HTTP API](../../_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)，音色列表见 [Qwen-Audio-TTS 音色列表](../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。

<a id="返回结果"></a>

<a id="tp-tts-response"></a>

## 返回结果

-   音频 URL：`output.audio.url`。
-   URL 过期时间：`output.audio.expires_at`。
-   计费字符数：`usage.characters`。
-   音频 URL 有时效，生成后及时下载。

<a id="限制"></a>

<a id="tp-tts-limits"></a>

## 限制

-   音色需要与模型版本匹配，可用的音色以音色列表为准。
-   计费按有效字符数计算，具体以控制台[用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)为准。

<a id="其他工具"></a>

<a id="tp-tts-other-tools"></a>

## 其他工具

其他工具的扩展机制和配置路径见[接入概览](token-plan-integration-overview.md#tp-ext-tools)。将上面的 Slash Command 内容保存到对应路径即可。
