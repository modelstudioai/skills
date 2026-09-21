# audio api references

百炼平台的 Audio API 提供语音识别、语音合成、音频生成、音乐生成、语音翻译和语音对话六大核心能力，覆盖从语音到文本、文本到语音、语音到语音等多模态音频处理场景。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需关注模型选型、输入格式及配额限制，以确保服务稳定可用。

## 支持的模型/功能

当前支持以下六大类音频处理能力，每类对应独立的 API 接口与专用模型：

- **语音识别（ASR）**：支持中文、英文及多语种实时/离线转写，模型包括 `paraformer-realtime-v1` 和 `paraformer-v2`  
- **语音合成（TTS）**：提供多音色、多语速、情感可控的合成能力，主力模型为 `cosyvoice-300m` 和 `sambert-zh-cn`  
- **音频生成**：基于文本生成环境音、音效等非语音类音频，模型为 `audio-gen-1.0`  
- **音乐生成**：支持歌词驱动或风格描述驱动的完整音乐片段生成，模型为 `music-gen-pro`  
- **语音翻译**：端到端语音→目标语言语音/文本，支持中英互译等 8 种语言对，模型为 `speech-translate-v2`  
- **语音对话**：集成 ASR+LLM+TTS 的全链路语音交互，模型为 `voice-dialogue-2.5`  

详细能力说明请参见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 和 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)。

## 关键参数

通用必填参数（适用于所有音频 API）：

- `model`: 字符串，指定模型 ID（如 `paraformer-v2`），不可省略  
- `input.audio_url` 或 `input.audio_bytes`: 二选一，推荐使用 `audio_url`（支持 HTTPS 公网可访问 URL，有效期 ≥10 分钟）；若传 `audio_bytes`，需 Base64 编码且总大小 ≤25 MB  
- `output_format`: 可选 `json`（默认）或 `stream`（仅部分接口支持，如 TTS、ASR 流式）  

功能特有参数示例：
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`pitch`（-50–50）  
- 音乐生成：`lyrics`（可选）、`style`（如 `"jazz"`、`"lofi"`）、`duration`（秒，最大 120）  
- 语音翻译：`source_language`、`target_language`（必须显式声明，不支持自动检测）

> **注意**：[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中提及的 `prompt_mode: "advanced"` 参数已在 v2.3.0 版本中废弃，实际请求中传入将被忽略；请改用 `prompt_config` 对象配置——该变更未在 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档中同步更新。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`（`<service_name>` 如 `speech-to-text`、`text-to-speech` 等）  
3. **请求体**：JSON 格式，结构遵循各子文档定义，例如语音识别请求体需包含 `input.audio_url` 和 `model`  
4. **响应解析**：成功时返回 `200 OK`，结果位于 `output.text`（ASR）、`output.audio_url`（TTS）或 `output.audio_id`（异步任务）字段中  

完整调用示例与错误码说明见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 600 秒，音乐生成 ≤ 120 秒，语音对话单轮 ≤ 180 秒  
- 并发限制：免费版 ≤ 2 QPS，企业版按配额配置（详见控制台）  
- 音频格式要求：ASR/TTS 仅支持 `wav`/`mp3`/`m4a`/`flac`；音乐生成仅接受 `wav`（44.1kHz, 16-bit, mono/stereo）  
- 所有音频 URL 必须为 HTTPS 且可公开访问；内网或带鉴权的链接将导致 400 错误  
- 异步接口（如音乐生成）需轮询 `GET /api/v1/tasks/{task_id}` 获取结果，超时时间为 30 分钟  

请务必查阅各子能力文档确认最新兼容性与行为细节，例如 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中关于低资源语言延迟的特别说明。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


