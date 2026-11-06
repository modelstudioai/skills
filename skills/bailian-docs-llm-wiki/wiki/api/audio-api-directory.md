# audio api directory

本目录汇总百炼平台提供的所有非实时音频处理 API，涵盖语音识别、语音合成、音频生成及音视频翻译四大能力。所有接口均通过 RESTful 方式调用，支持标准 HTTP 请求与 JSON 响应格式。开发者需根据具体任务选择对应模型，并注意各接口的输入约束与计费粒度。

## 支持的模型/功能

当前支持以下四类音频处理能力：
- **语音识别（ASR）**：将音频文件转为文本，支持多语种及带标点/时间戳输出；模型包括 `qwen2-audio` 等；
- **语音合成（TTS）**：将文本转为自然语音，支持音色选择、语速调节及 SSML 控制；
- **音频生成**：基于文本提示生成背景音乐、音效或人声片段，适用于内容创作场景；
- **音视频翻译**：对输入音视频流进行跨语言翻译并输出目标语言语音（如中→英），目前由 `qwen3-livetranslate-flash` 模型提供，[音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 文档详述其工作模式。

> **注意**：`qwen3-livetranslate-flash` 虽在文档中归类为“音视频翻译”，但实际仅支持**离线文件输入**（非真正实时流），与名称存在偏差；请以 [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 中的 `input_type` 和 `file_url` 字段说明为准。

## 关键参数

通用关键参数包括：
- `model`: 必填，指定模型标识符（如 `qwen2-audio`, `qwen2-tts`, `qwen2-audio-gen`）；
- `input`: 必填，结构因能力而异：ASR 传 `{"file_url": "..."}`，TTS 传 `{"text": "...", "voice": "zh-CN-Xiaoxiao"}`；
- `parameters`: 可选，控制质量、时长、采样率等（如 `sample_rate: 16000`, `enable_punctuation: true`）；
- `response_format`: 可选，支持 `json`（默认）或 `wav`（仅 TTS/AudioGen 输出二进制音频流）。

详细字段定义请参考 [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md) 和 [音频生成](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md) 的参数表格。

## 使用方式

1. 通过 `POST /v1/audio/{task}` 调用（`{task}` 为 `transcriptions`, `speech`, `generation`, `translate` 之一）；
2. 请求头需携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
3. 输入文件须先上传至百炼对象存储（OSS）并获取可公开访问的 `file_url`，或使用 base64 编码内联（仅限 ≤1MB 小文件）；
4. 响应含 `request_id` 用于问题排查，[异步任务](../concepts/asynchronous-task.md)返回 `status: "processing"` 并提供 `result_url` 轮询。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 600 秒，AudioGen ≤ 30 秒，音视频翻译 ≤ 180 秒；
- 文件格式支持：MP3/WAV/FLAC/M4A（ASR/TTS），WAV/MP3（AudioGen），MP4/MOV/AVI（音视频翻译）；
- 所有音频接口**不支持 WebSocket 或流式响应**，均为全量输入-全量输出模式；
- 计费按调用次数 + 音频时长（秒）组合计费，具体见 [概述](../../raw/model-api-reference/audio-api-directory/audio-api-references.md) 中的定价说明。

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


