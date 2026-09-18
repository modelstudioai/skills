# audio api references

百炼平台的 Audio API 提供语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心能力，所有接口均通过统一的 RESTful API 调用，支持流式与非流式响应。各能力由专用音频模型提供，需按场景选择对应模型并传入符合规范的音频数据。详细行为与兼容性请以各子模块文档为准。

## 支持的模型/功能

当前支持以下五类音频处理能力，每类对应独立的模型与 API 端点：

- **语音识别（ASR）**：支持中英文混合识别，实时流式识别延迟低至 300ms；模型包括 `paraformer-realtime-v1` 和 `paraformer-v2`  
- **语音合成（TTS）**：提供多音色、可调节语速/语调的高质量合成，支持 SSML 标签；主力模型为 `cosyvoice-300m` 和 `cosyvoice-1b`  
- **音乐生成**：支持文本生成完整音乐（含旋律、节奏、风格控制），输出格式为 WAV/MP3；模型为 `musicgen-pro-v1`  
- **语音翻译**：端到端中英互译，支持识别+翻译联合建模，不返回中间识别文本；模型为 `speech-translate-zh2en-v1` 和 `speech-translate-en2zh-v1`  
- **语音对话**：集成 ASR + LLM + TTS 的全链路语音交互，需配合对话上下文管理；模型为 `voice-dialog-pro-v1`

> **注意**：`voice-dialog-pro-v1` 当前仅支持单轮唤醒后 60 秒内连续语音输入，多轮上下文保持能力弱于 [语音识别](raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 与 [语音合成](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 的分步调用组合，建议高可靠性场景优先采用分步方案。

## 关键参数

所有 Audio API 共享以下基础参数（必填项标 `*`）：

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `model*` | string | 是 | 模型标识符，如 `paraformer-v2`、`cosyvoice-300m`，必须与所选能力匹配 |
| `audio*` | string (base64) 或 object | 是 | 音频数据：`base64` 编码字符串，或 `{ url: "https://..." }`（公网可访问） |
| `audio_format*` | string | 是 | 音频格式，支持 `wav`、`mp3`、`m4a`、`flac`；采样率建议 16kHz，单声道 |
| `sample_rate` | integer | 否 | 显式声明采样率（Hz），默认 `16000`；若 `audio_format=wav` 且含 RIFF 头，将自动解析 |
| `response_format` | string | 否 | 返回格式，`json`（默认）或 `stream`（仅部分 ASR/TTS 接口支持） |

此外，各能力有专属参数，例如：
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`ssml`（布尔值，启用 SSML 解析）
- 音乐生成：`duration`（秒数，5–30）、`style`（`pop`/`lofi`/`orchestral` 等）
- 语音翻译：`source_lang` / `target_lang`（`zh`/`en`）

详情见 [语音识别](raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)、[语音合成](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 和 [音乐生成](raw/model-api-reference/audio-api-references/music-generation-references.md) 的参数章节。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：向 `https://dashscope.aliyuncs.com/api/v1/audio/<capability>` 发送 POST 请求（`<capability>` 如 `asr`, `tts`, `music`）  
3. **示例（ASR）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/audio/asr" \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "paraformer-v2",
           "audio": {"url": "https://example.com/audio.wav"},
           "audio_format": "wav"
         }'
   ```

流式响应需设置 `response_format=stream` 并使用 SSE 解析；非流式响应直接解析 JSON body。错误码统一遵循 [API 错误码规范](../../raw/model-api-reference/error-codes.md)。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 60 秒，音乐生成 ≤ 30 秒，语音翻译 ≤ 60 秒，语音对话 ≤ 90 秒  
- 音频文件大小上限：50 MB（URL 方式无此限制，但源站需支持 `HEAD` 和 `Range` 请求）  
- 所有音频输入必须为有效编码，损坏或静音占比 >80% 的文件将返回 `InvalidAudio` 错误  
- `sample_rate` 若显式指定，必须与实际音频一致；否则可能导致识别/合成质量下降  
- 语音对话接口暂不支持自定义 LLM 模型，固定使用 `qwen-audio-7b` 作为对话引擎 —— 此行为与 [语音对话](raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档描述一致，但与早期 [语音识别](raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中提及的“可插拔 ASR+LLM+TTS”架构存在演进差异，请以本页及最新子文档为准

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


