# audio api references

百炼平台提供覆盖语音合成、识别、翻译、对话及音频/音乐生成的全链路音频 API，支持开发者构建多模态语音交互与内容创作应用。所有接口均基于 RESTful 设计，统一使用 `POST /v1/audio/*` 路径前缀，并通过 `Authorization: Bearer <api_key>` 认证。详细协议规范与错误码定义请参阅 [音频](../../raw/model-api-reference/audio-api-references.md) 主文档。

## 支持的模型与功能

当前支持以下六大音频处理能力，各能力对应独立子接口与专用模型：

- **语音合成（TTS）**：支持中英文多音色、语速/语调调节，底层模型为 `qwen-audio-tts-v1`  
- **语音识别（ASR）**：支持长语音流式识别与离线文件转写，模型为 `qwen-audio-asr-v2`  
- **语音翻译（ST）**：支持中↔英实时口音翻译，输出文本与时间戳，模型为 `qwen-audio-st-v1`  
- **语音对话（Voice Chat）**：端到端语音输入→理解→语音响应，需配合 `qwen-audio-chat-v1` 模型使用  
- **音频生成（Audio Generation）**：基于文本生成环境音、SFX 等非乐音音频，模型为 `qwen-audio-gen-v1`  
- **音乐生成（Music Generation）**：支持歌词/风格描述生成 30s–90s 原创音乐，模型为 `qwen-music-gen-v2`  

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中提及的 `qwen-audio-chat-v1` 模型暂不支持自定义角色音色，该能力已在 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中单独实现，二者不可混用。

## 关键参数

所有音频 API 共享以下基础参数（必填项标 `*`）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model*` | string | 是 | 模型标识符，如 `qwen-audio-asr-v2`；必须与所调用子接口匹配 |
| `input*` | object | 是 | 输入结构体，具体字段依接口而异（如 ASR 的 `audio_url` 或 `audio_bytes`） |
| `parameters` | object | 否 | 控制生成质量/时长/风格等，例如 `speech_synth` 下的 `voice_type`、`speed` |

各子接口特有参数详见对应文档，例如 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 要求 `parameters.duration`（单位秒），而 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 则需 `parameters.style` 和 `parameters.lyrics`（可选）。

## 使用方式

1. **请求示例（ASR）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/audio/asr" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-audio-asr-v2",
           "input": {"audio_url": "https://example.com/audio.wav"},
           "parameters": {"language": "zh", "enable_punctuation": true}
         }'
   ```

2. **响应结构**：统一返回 `output.result`（文本结果）、`output.task_id`（用于轮询长任务）及 `usage` 字段（含 token/音频时长统计）  
3. **流式响应**：仅 ASR 与 Voice Chat 支持 `Accept: text/event-stream`，其余接口均为同步 JSON 响应  

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS ≤ 300 秒，Music Generation ≤ 90 秒，Audio Generation ≤ 30 秒  
- 音频格式要求：WAV/MP3/FLAC/M4A（采样率 ≥ 8kHz，推荐 16kHz/44.1kHz；单声道优先）  
- 所有音频 URL 必须为公网可访问 HTTPS 地址，且有效期 ≥ 10 分钟  
- > **注意**：[语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 文档中“支持日韩法西语”的描述已过时；当前仅正式支持中↔英双向翻译，其他语种处于灰度测试阶段，调用可能返回 `400 Unsupported language` 错误。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


