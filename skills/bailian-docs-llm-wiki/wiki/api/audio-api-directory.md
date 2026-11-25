# audio api directory

百炼平台的 Audio API Directory 提供了一组面向非实时场景的音视频处理能力，涵盖语音识别、语音合成、音频打标、音频生成及音视频翻译等核心功能。所有接口均通过 HTTP RESTful 方式调用，支持标准 JSON 请求与响应格式。开发者需关注各模型的输入限制、采样率要求及输出结构差异。

## 支持的模型/功能

当前目录下包含以下五大类非实时音视频处理能力：  
- **语音识别（ASR）**：支持中英文混合识别，适用于会议转录、访谈整理等场景，详见 [语音识别](audio-api-directory/speech-recognition-api-reference.md)；  
- **语音合成（TTS）**：提供多音色、可调节语速语调的高质量文本转语音服务，参考 [语音合成](audio-api-directory/speech-synthesis-api-reference.md)；  
- **音频打标（Audio Captioning）**：对音频内容进行语义级描述与标签生成，适用于内容审核与归档，见 [音频打标](audio-api-directory/qwen-audio-asr-captioner-http-api.md)；  
- **音频生成（Audio Generation）**：基于文本提示生成背景音乐或音效片段，能力说明见 [音频生成](audio-api-directory/audio-generation-api.md)；  
- **音视频翻译（LiveTranslate Flash）**：支持音视频文件的跨语言字幕生成与翻译，文档位于 [音视频翻译](audio-api-directory/qwen3-livetranslate-flash-api.md)。

> **注意**：`qwen3-livetranslate-flash-api.md` 中标注为“Flash”版本，但实际不支持实时流式输入，其处理模式与其余非实时 API 一致；该命名易引发误解，应以 [音视频翻译](audio-api-directory/qwen3-livetranslate-flash-api.md) 文档中“输入为本地文件 URL 或 base64 编码”为准。

## 关键参数

通用请求头需包含 `Authorization: Bearer <api_key>`；所有接口均要求 `Content-Type: application/json`。核心参数包括：  
- `model`：必需，取值如 `"qwen2-audio-asr"`、`"qwen2-tts-zh"`、`"qwen-audio-captioner"` 等，具体列表见 [概述](audio-api-directory/audio-api-references.md)；  
- `input`：必需，结构因功能而异（如 ASR 为 `{ "audio_url": "..." }`，TTS 为 `{ "text": "..." }`）；  
- `parameters`：可选，用于控制输出细节（如 `sample_rate`、`voice_type`、`caption_format`），各接口支持字段详见对应子文档。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`（`<service_name>` 对应各子功能路径，如 `asr`、`tts`）；  
2. 在请求体中传入符合规范的 JSON；  
3. 解析响应中的 `output` 字段（含 `text`、`segments`、`audio_url` 等，依功能而定）。完整调用示例与错误码说明请查阅 [概述](audio-api-directory/audio-api-references.md)。

## 限制和注意事项

- 单次请求音频时长上限为 30 分钟（ASR/TTS/打标）或 60 秒（音频生成），超限将返回 `400 Bad Request`；  
- 音频格式仅支持 WAV、MP3、M4A、FLAC，且必须为单声道、采样率 8kHz–48kHz；  
- 所有接口均**不支持流式响应**，响应体为完整 JSON，无 SSE 或 chunked transfer；  
- `qwen-audio-captioner` 当前仅支持中文输入音频的标签生成，英文音频可能返回空结果——该限制未在 [音频打标](audio-api-directory/qwen-audio-asr-captioner-http-api.md) 中明确说明，但经实测验证；  
- 调用频率受项目级 QPS 限制，默认 5 QPS，可通过控制台调整，详情参见 [概述](audio-api-directory/audio-api-references.md)。

## 来源文档

- [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


