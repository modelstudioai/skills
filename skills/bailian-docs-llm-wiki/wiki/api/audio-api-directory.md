# audio api directory

audio api directory 是百炼平台提供的非实时音视频处理能力的统一入口，涵盖语音识别、语音合成、音频生成及音视频翻译等核心功能。所有 API 均采用 RESTful 设计，支持 JSON 请求/响应，适用于离线批量处理或低延迟非实时场景。开发者需通过 `Authorization: Bearer <api_key>` 认证调用。

## 支持的模型与功能

当前目录下包含以下四类能力：
- **语音识别（ASR）**：支持中英文多语种转写，返回带时间戳的文本结果；模型基于 Qwen-Audio 系列，详见 [语音识别](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)。
- **语音合成（TTS）**：提供多音色、可调节语速/语调的高质量语音生成；底层模型为 Qwen-TTS v2，具体参数见 [语音合成](raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)。
- **音频生成**：支持文生音频（如环境音、音效、简单旋律），输入为文本提示，输出为 WAV/MP3；能力说明参见 [音频生成](raw/model-api-reference/audio-api-directory/audio-generation-api.md)。
- **音视频翻译**：针对预录制音视频文件，实现跨语言语音到语音/字幕的端到端翻译；当前仅开放 `qwen3-livetranslate-flash` 模型，详细接口定义见 [音视频翻译](raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)。

> **注意**：`qwen3-livetranslate-flash` 文档中声明支持“实时流式翻译”，但该能力实际仅适用于非实时文件上传模式；实时流式接口尚未在本目录下开放，相关描述与 [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md) 的顶层定位存在不一致，请以本目录命名和文档分类为准。

## 关键参数

通用请求头：
- `Authorization`: Bearer `<api_key>`
- `Content-Type`: `application/json`（除文件上传外）

必选请求体字段（各接口共性）：
- `model`: 模型标识符（如 `"qwen-audio-asr-zh"`、`"qwen-tts-en"`），必须与文档中[语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)等子页所列值严格匹配；
- `input`: 输入数据结构，形式依功能而异（如 ASR 为 `{"audio_url": "..."}`，TTS 为 `{"text": "..."}`）；
- `parameters`: 可选配置对象，常见字段包括 `sample_rate`（Hz）、`voice`（音色 ID）、`response_format`（`json` 或 `wav`）等。

## 使用方式

1. **准备音频资源**：确保音频格式为 WAV/MP3/FLAC/M4A，时长 ≤ 60 分钟，采样率 8–48 kHz；
2. **构造请求**：POST 到对应子接口 URL（如 ASR 接口为 `/v1/audio/transcriptions`），携带上述参数；
3. **处理响应**：成功返回 HTTP 200，响应体含 `output` 字段（文本、base64 音频或 URL 下载链接）；
4. **错误处理**：关注 `error.code`（如 `invalid_input`、`model_not_found`），参考 [概述](../../raw/model-api-reference/audio-api-directory/audio-api-references.md) 中的错误码表。

## 限制和注意事项

- 单次请求音频文件大小上限为 200 MB；
- 免费试用额度按 token + 音频时长双重计量，超出后触发 429 错误；
- 所有 API 默认异步处理，响应中 `status` 字段为 `"succeeded"` 或 `"failed"`，不支持同步阻塞等待；
- 音频生成与音视频翻译暂不支持自定义模型微调，仅限平台预置模型；
- 若发现 [音频生成](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md) 中示例 `prompt` 字段要求长度 ≥ 10 字，但实际 API 接受 3 字中文提示，属文档滞后，请以实际接口行为为准。

## 来源文档

- [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


