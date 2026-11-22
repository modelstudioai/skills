# audio api directory

百炼平台的 Audio API Directory 提供了一组非实时音视频处理能力，涵盖语音识别、语音合成、音频生成及音视频翻译等核心场景。所有接口均采用 RESTful 设计，支持标准 HTTP 请求与 JSON 响应格式。开发者需通过 API Key 进行身份认证，并遵循各接口的输入约束与输出规范。

## 支持的模型/功能

当前目录下包含以下四类功能模块：  
- **语音识别（ASR）**：支持多语种、高精度离线转写，适用于会议记录、字幕生成等场景；  
- **语音合成（TTS）**：提供多种音色与语速调节能力，支持 SSML 标签控制发音细节；  
- **音频生成**：基于文本生成高质量背景音乐或音效，不支持人声克隆；  
- **音视频翻译**：仅支持 Qwen3-LiveTranslate-Flash 模型，专为跨语言音视频内容批量翻译设计，[音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md) 中明确将其归类为“非实时”能力，而非流式服务。

## 关键参数

所有接口共用以下基础参数：  
- `model`: 必填，取值须来自 [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md) 等子文档所列的合法模型名；  
- `input`: 必填，结构因功能而异（如 ASR 传 `audio_url` 或 `audio_bytes`，TTS 传 `text`）；  
- `response_format`: 可选，支持 `json`（默认）或 `vtt`（仅 ASR）；  
- `language`: 部分接口必填（如 ASR、翻译），需严格匹配 [音频生成](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md) 文档中定义的语言代码表。

> **注意**：`qwen3-livetranslate-flash` 接口文档中声明支持 `stream=true` 参数，但 [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md) 明确指出该模型属于“非实时”范畴，实际调用时启用流式参数将被忽略并返回警告。请以主目录文档为准。

## 使用方式

1. 构造 POST 请求至对应接口 URL（如 `/v1/audio/transcriptions`）；  
2. 在 Header 中设置 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；  
3. Body 中按子接口要求组织 JSON 数据，例如 ASR 需提供 `audio_url` 或 base64 编码的 `audio_bytes`；  
4. 解析响应体中的 `output` 字段（结构详见各子文档），错误时检查 `code` 与 `message`。

## 限制和注意事项

- 单次请求音频时长上限为 60 分钟（ASR/TTS）、30 秒（音频生成）、10 分钟（音视频翻译）；  
- 所有音频文件需为 PCM、WAV、MP3、M4A 或 FLAC 格式，采样率建议 16kHz/44.1kHz；  
- 免费试用额度按调用次数计费，超出后需绑定付费账户；  
- 音频生成接口暂不支持自定义音色或情感参数，相关描述见 [音频生成](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)；  
- 若同时调用多个子接口，请确保 `model` 参数与目标功能严格匹配，混用会导致 `400 Bad Request`。

## 来源文档

- [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


