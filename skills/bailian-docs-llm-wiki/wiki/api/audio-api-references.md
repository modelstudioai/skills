# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful API 调用，支持标准 HTTP 请求与 JSON 响应格式。开发者需使用有效的 API Key 并遵循各模型的输入/输出规范。

## 支持的模型与功能

当前音频类 API 包含以下功能模块（按生产可用性排序）：
- **语音识别（ASR）**：支持中英文混合识别、实时流式识别及离线音频转写  
- **语音合成（TTS）**：提供多音色、多语种、可调节语速/语调的高质量语音生成  
- **音乐生成**：支持文本描述驱动的短音乐片段生成（最长 30 秒），暂不支持歌词对齐  
- **语音翻译（ST）**：支持语音输入→目标语言文本输出（如中文语音→英文文本），**暂不支持语音→语音直译**  
- **语音对话（Voice Chat）**：端到端语音交互能力，集成 ASR + LLM + TTS 流程，适用于智能硬件场景  

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references.md) 文档中提及的“支持双语实时互译”与 [语音翻译](../../raw/model-api-reference/audio-api-references.md) 的能力边界存在表述重叠；实际以 [语音翻译](../../raw/model-api-reference/audio-api-references.md) 定义的纯文本输出为准，语音对话模块输出为合成语音，不返回中间文本。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 模型标识符（如 `paraformer-realtime-v1`、`cosyvoice-300m`、`musicgen-small`）  
- `input.audio_url` 或 `input.audio_bytes`: 音频数据源，推荐使用 `audio_url`（HTTPS 可公开访问的 URL）；若传 `audio_bytes`，需 Base64 编码且总大小 ≤ 10 MB  
- `parameters`: 功能相关配置对象，例如：  
  - ASR：`{ "language": "zh", "enable_punctuation": true }`  
  - TTS：`{ "voice": "zhitian_emo", "speed": 1.0 }`  
  - 音乐生成：`{ "duration": 15.0 }`（单位：秒，范围 5–30）  

## 使用方式

1. 发起 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio`  
2. Header 中设置：  
   - `Authorization: Bearer <api_key>`  
   - `Content-Type: application/json`  
3. Body 示例（ASR）：
```json
{
  "model": "paraformer-realtime-v1",
  "input": {
    "audio_url": "https://example.com/audio.wav"
  },
  "parameters": {
    "language": "zh"
  }
}
```
完整请求示例与响应结构详见 [语音识别](../../raw/model-api-reference/audio-api-references.md) 和 [语音合成](../../raw/model-api-reference/audio-api-references.md) 的官方参考文档。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 60 秒；音乐生成 ≤ 30 秒；语音对话单轮 ≤ 45 秒  
- 音频格式要求：WAV（PCM, 16-bit, 16kHz/44.1kHz）、MP3、M4A；不支持 FLAC 或 AMR  
- 所有音频 URL 必须支持 `HEAD` 请求且无鉴权跳转，否则返回 `400 InvalidAudioUrl`  
- 语音对话接口默认启用流式响应（`Accept: text/event-stream`），若需完整 JSON 响应，需显式设置 `stream: false`  
- 错误码统一遵循百炼平台标准（如 `InvalidParameter`、`AudioTooLong`），具体含义请查阅 [语音翻译](../../raw/model-api-reference/audio-api-references.md) 文档末尾的错误码附录

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


