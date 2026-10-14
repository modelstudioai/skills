# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与配额限制。

## 支持的模型与功能

当前支持以下六大音频处理能力，对应独立的 API 端点与模型标识：

- **语音合成（TTS）**：支持多语种、多音色，可调节语速、音调、停顿；参考 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持实时流式识别与离线文件识别，中文识别准确率高；参考 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成**：基于文本生成环境音、音效等非音乐类音频；参考 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **音乐生成**：支持歌词+风格描述生成完整音乐片段（MP3/WAV），时长上限 30 秒；  
- **语音对话**：端到端语音交互，支持唤醒词、上下文保持与自然中断恢复；  
- **语音翻译**：支持中英互译的实时语音转译（含字幕同步输出），仅限双语场景。

> **注意**：[音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档中提及的“支持 5 分钟长音频”与当前生产环境实际限制（≤30 秒）不符，以控制台配额页和 API 响应 `400` 错误提示为准。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 模型标识符（如 `qwen2-audio-tts-16k`、`qwen2-audio-asr-zh`），详见各子文档模型列表  
- `input`: 输入结构体，格式因能力而异（如 ASR 为 `{"audio_url": "..."}`，TTS 为 `{"text": "...", "voice": "zhitian"}`）  
- `parameters`: 可选配置对象，常见字段包括 `sample_rate`（默认 24000）、`response_format`（`mp3`/`wav`/`pcm`）、`stream`（布尔值）  

部分能力特有参数：
- TTS：`voice`, `speed`, `pitch`, `volume`  
- ASR：`language`, `word_timestamps`, `diarization`  
- 音乐生成：`lyrics`, `style`, `bpm`, `instrumentation`

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：POST 到对应端点（如 TTS 为 `/v1/audio/speech`，ASR 为 `/v1/audio/transcriptions`）  
3. **输入音频**：优先使用 `audio_url`（公网可访问的 HTTPS URL）；若传原始二进制数据，需设 `Content-Type: audio/wav` 并将音频 Base64 编码后置于 `input.audio` 字段  
4. **响应**：非流式返回 JSON（含 `output.url` 或 `output.data`）；流式响应按 SSE 格式推送 chunk，参考 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 的流式示例

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS ≤ 1000 字符（约 5 分钟语音），音乐生成 ≤ 30 秒  
- 文件大小限制：URL 方式无显式限制（但超时时间为 120 秒），Base64 方式 ≤ 25 MB  
- 所有音频 API 均不支持跨区域调用（如华东节点仅接受华东上传的 `audio_url`）  
- 语音翻译暂不支持方言识别与三语以上混合场景  
- 错误码 `429` 表示 QPS 超限，`400` 多因参数缺失或格式错误（建议严格校验 `input` 结构）

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


