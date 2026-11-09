# audio api directory

百炼平台的 Audio API Directory 提供了一组面向非实时场景的音频处理能力，涵盖语音识别、语音合成、音频生成及音视频翻译等核心功能。所有接口均通过 RESTful 方式调用，支持标准 HTTP 请求与 JSON 响应格式。该目录不包含实时流式音频处理能力，相关需求请参考 [实时音频 API](../../raw/model-api-reference/realtime-audio-api-directory.md) 文档。

## 支持的模型与功能

当前 Audio API Directory 支持以下四类功能：

- **语音识别（ASR）**：支持中英文混合识别，基于 Qwen-Audio-ASR 系列模型，适用于录音文件转写场景  
- **语音合成（TTS）**：提供多音色、多语种（含中文普通话、粤语、英语等）的高质量语音生成能力  
- **音频生成（Audio Generation）**：支持文本到音频（如环境音、音效）及简单音乐片段生成，基于 Qwen-Audio-Gen 模型  
- **音视频翻译（Livetranslate Flash）**：专为短视频字幕与配音设计，支持源音轨识别 + 目标语种合成一体化输出，详见 [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)

> **注意**：文档中提及的 `qwen3-livetranslate-flash-api.md` 实际对应模型版本为 Qwen2-Audio-LiveTranslate，而非 Qwen3；该命名属历史遗留，功能实现与模型能力以 [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 中描述为准，但需注意其输入限制为单次 ≤ 60 秒音视频文件。

## 关键参数

所有 Audio API 共享以下通用参数（部分接口有扩展）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-asr-v1`、`qwen-tts-v2-zh`、`qwen-audio-gen-v1`；完整列表见 [概述](../../raw/model-api-reference/audio-api-directory/audio-api-references.md) |
| `input` | object | 是 | 输入结构体，含 `audio_url`（公网可访问的音频 URL）或 `audio_bytes`（Base64 编码二进制）；`audio_url` 优先级高于 `audio_bytes` |
| `parameters` | object | 否 | 功能定制参数，如 `language`（ASR/TTS）、`voice`（TTS）、`duration_seconds`（Audio Generation）等 |

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`，其中 `<service_name>` 对应 `speech_recognition`、`speech_synthesis`、`audio_generation` 或 `livetranslate_flash`  
3. **响应结构**：统一返回 `output.result` 字段（字符串或对象），错误时返回 `error.code` 与 `error.message`；详细字段定义参见 [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md) 等子文档  

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 180 秒，Audio Generation ≤ 30 秒，Livetranslate Flash ≤ 60 秒  
- 音频格式仅支持 MP3、WAV、M4A（AAC 编码），采样率建议 16kHz 或 44.1kHz，单声道优先  
- 所有接口均不支持分块上传或流式响应；若需处理长音频，请自行切片并串行/并行调用  
- `audio_url` 必须为公网可直连地址（不支持私有 OSS bucket 的临时签名 URL，除非已配置跨域与公开读）；替代方案请参考 [概述](../../raw/model-api-reference/audio-api-directory/audio-api-references.md) 中的预签名上传指引

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


