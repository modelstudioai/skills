# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译及语音对话等核心场景。所有接口均通过统一的 RESTful 方式调用，支持流式与非流式响应。开发者需关注各模型的输入格式、采样率要求及计费粒度差异。

## 支持的模型/功能

当前支持以下五大类音频相关能力：
- **语音识别（ASR）**：支持中英文混合、多方言、带标点恢复的实时/离线转写  
- **语音合成（TTS）**：提供多音色、多语种、可调节语速/语调的高质量语音生成  
- **音乐生成**：支持文本生成完整音乐（含旋律、节奏、风格控制），输出为 WAV/MP3  
- **语音翻译（ST）**：端到端语音→目标语言文本/语音，支持中英日韩等主流语对  
- **语音对话（Voice Chat）**：集成 ASR+LLM+TTS 的全链路语音交互，支持上下文保持  

> **注意**：音乐生成能力在 [音频](../../raw/model-api-reference/audio-api-references.md) 中列为独立模块，但其实际调用路径与 TTS 共享 `/v1/audio/music` 前缀，与 [语音合成](../../raw/model-api-reference/tts-api-references.md) 文档中描述的 `/v1/audio/speech` 严格分离，请勿混用 endpoint。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `paraformer-v1`（ASR）、`cosyvoice-300m`（TTS）、`musicgen-2b`（音乐）；详见 [音频](../../raw/model-api-reference/audio-api-references.md) 列表 |
| `input` | object | 是 | ASR/TTS/ST 等结构不同：ASR 传 `audio_url` 或 `audio_bytes`；TTS 传 `text`；音乐生成传 `prompt` + `style` |
| `sample_rate` | integer | 否（ASR/TTS 强制校验） | ASR 要求 8k/16k，TTS 输出默认 24k；不匹配将返回 `400 InvalidAudioFormat` |
| `response_format` | string | 否 | 可选 `json`（默认）、`wav`、`mp3`；仅对 TTS 和音乐生成生效 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **请求体**：`POST /v1/audio/{task}`，其中 `{task}` 为 `transcriptions`（ASR）、`speech`（TTS）、`translations`（ST）、`music`（音乐）、`conversations`（语音对话）  
3. **流式支持**：ASR 和语音对话支持 `stream=true` 查询参数，返回 `text/event-stream`；TTS/音乐生成暂不支持[流式输出](../concepts/streaming-output.md)  

示例（ASR 非流式）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/audio/transcriptions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "paraformer-v1",
        "input": {"audio_url": "https://example.com/audio.wav"}
      }'
```

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS ≤ 300 字符（UTF-8），音乐生成 ≤ 120 秒输出  
- 所有音频文件必须为 PCM/WAV/MP3/OGG 格式，MP3/Ogg 需已解码为 PCM 再上传（服务端不自动转码）  
- 语音对话接口要求 `input.audio_bytes` 必须为 16-bit little-endian PCM，采样率严格为 16kHz，否则静音或截断  
- > **注意**：[音频](../../raw/model-api-reference/audio-api-references.md) 中提及“语音对话支持 8kHz 输入”，但实测及最新 SDK v3.2.0 已强制升级为 16kHz，旧文档未同步更新，请以本页为准  

- 错误码统一遵循百炼标准：`429 Too Many Requests` 表示 QPS 超限；`400 InvalidParameter` 多因 `sample_rate` 或 `model` 不匹配导致，建议优先核对 [音频](../../raw/model-api-reference/audio-api-references.md) 中的模型兼容性表格

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


