# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful 设计对外暴露，支持流式与非流式调用。开发者需根据具体任务选择对应模型及参数配置。

## 支持的模型/功能

当前支持以下五类音频相关模型与功能：
- **语音识别（ASR）**：支持中英文多语种实时/离线转写，详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **语音合成（TTS）**：提供多音色、可控语速与情感表达的文本转语音能力，详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **音乐生成**：支持文本描述驱动的短音乐片段生成（最长30秒），详见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- **语音翻译**：端到端实现语音输入→目标语言语音输出（如中文语音→英文语音），支持 12 种语言对，详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)  
- **语音对话**：集成 ASR+LLM+TTS 的全链路语音交互能力，适用于智能助手类应用，详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)

> **注意**：语音对话接口要求 `input_format` 必须为 `wav` 或 `pcm`，而语音识别接口在 v2.3+ 版本中已扩展支持 `mp3` 和 `m4a`；该差异在 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 与 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档中未明确同步，请以各接口最新参数说明为准。

## 关键参数

通用关键参数（适用于多数音频接口）：
- `model`: 模型标识符（如 `paraformer-realtime-v1`、`cosyvoice-300m`、`musicgen-small`），必须与功能类型匹配  
- `audio_url` 或 `audio`: 二进制音频数据（Base64 编码）或可公开访问的 HTTPS 音频 URL  
- `sample_rate`: 音频采样率（Hz），推荐 16000（ASR/TTS）、44100（音乐生成）  
- `response_format`: 返回格式，支持 `json`（默认）、`wav`、`mp3`（仅 TTS/音乐生成等输出音频的接口）  

部分接口特有参数：
- ASR：`language`, `enable_punctuation`, `diarization`  
- TTS：`voice`, `speed`, `pitch`, `emotion`  
- 音乐生成：`duration`（单位秒，取值范围 5–30），`style`（如 `"pop"`, `"lofi"`）

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`  
2. **请求方法**：`POST /v1/audio/<endpoint>`，其中 `<endpoint>` 对应功能路径（如 `/transcriptions`, `/speech`, `/music`, `/translation`, `/conversation`）  
3. **请求体**：JSON 格式，含模型名与音频输入（`audio_url` 优先于 `audio` 字段）  
4. **响应**：成功时返回 `200 OK`，含 `result` 字段（文本结果或音频二进制 Base64）；流式接口使用 `Content-Type: text/event-stream`

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 120 秒，音乐生成 ≤ 30 秒，语音翻译 ≤ 60 秒，语音对话单轮 ≤ 45 秒  
- 音频格式要求：WAV（PCM 封装）、MP3、M4A、OGG；不支持 FLAC、AAC 容器（即使内部为 PCM）  
- 流式响应仅支持 ASR 和语音对话接口，且需显式设置 `stream: true`  
- 所有音频接口均不支持跨区域调用（如华东节点仅接受华东地域内 `audio_url` 域名白名单资源）  
- 错误码 `422 Unprocessable Entity` 常见于 `sample_rate` 与模型训练配置不匹配，建议优先查阅 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中的兼容性表格

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


