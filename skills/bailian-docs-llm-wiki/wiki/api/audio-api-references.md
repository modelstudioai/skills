# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、语音翻译、音频/音乐生成及语音对话等核心能力。所有接口均基于 RESTful 设计，支持流式响应与非流式调用，并通过 `Authorization` 头进行身份认证。开发者需根据具体任务选择对应模型与参数组合，详见各子模块文档。

## 支持的模型/功能

当前支持以下六大音频处理能力，每个能力对应独立的 API 端点与模型选型：

- **语音合成（TTS）**：支持多语种、多音色、可控语速与情感表达，模型包括 `qwen2-audio-tts-v1` 等  
- **语音识别（ASR）**：支持中英文混合识别、标点自动恢复、方言适配（如粤语、四川话），模型如 `qwen2-audio-asr-v1`  
- **语音翻译（ST）**：支持实时语音到文本翻译（如中文语音→英文文本），暂不支持语音到语音直译  
- **音频生成（Audio Generation）**：面向环境音、音效、人声旁白等非音乐类音频，输入为文本提示词  
- **音乐生成（Music Generation）**：支持旋律、风格、BPM、时长控制，输出为 WAV/MP3 格式  
- **语音对话（Voice Conversation）**：端到端语音交互，集成 ASR + LLM + TTS，需启用 `enable_streaming` 以获得低延迟体验  

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中提及的 `input_format=wav16k` 与 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 当前要求的 `input_format=pcm16k` 存在格式不一致说明，实际调用请以 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 的 PCM 格式为准，语音对话接口内部已自动完成格式转换。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 模型标识符（如 `qwen2-audio-tts-v1`），不可省略  
- `input`: 输入内容结构体，类型依能力而异（如 ASR 为 `{"audio": "base64_encoded"}`，TTS 为 `{"text": "你好"}`）  
- `response_format`: 可选 `json`（默认）或 `wav`/`mp3`（仅部分生成类接口支持二进制响应）  

能力特有参数示例：
- TTS：`voice`, `speed`, `pitch`, `emotion`  
- 音乐生成：`style`, `bpm`, `duration_sec`, `instrumentation`  
- ASR：`language`, `add_punctuation`, `word_timestamps`  
- 语音翻译：`source_lang`, `target_lang`（目前仅支持 `zh→en`, `en→zh`）  

详细参数定义请参阅 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 等各子文档。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：向对应 endpoint 发送 POST 请求（如 TTS：`POST /v1/audio/speech`）  
3. **音频编码**：上传音频需 Base64 编码（除流式上传外），采样率与位深须符合模型要求（常见为 16kHz/16bit PCM）  
4. **响应处理**：非流式返回 JSON；流式接口（如 `/v1/audio/conversation/stream`）需按 SSE 或分块传输解析  

示例 cURL（TTS）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/audio/speech \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2-audio-tts-v1","input":{"text":"今天天气很好"},"voice":"zhitian_001"}'
```

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 60 秒，TTS ≤ 300 字符，音乐生成 ≤ 30 秒，语音对话单轮 ≤ 90 秒  
- 所有音频接口均**不支持跨区域调用**，需确保 API Endpoint 与模型部署地域一致（如 `dashscope.aliyuncs.com` 仅支持中国内地）  
- 流式响应中，语音对话接口的 `first_token_latency` 受 LLM 推理影响较大，建议搭配 `temperature=0.3` 降低不确定性  
- 二进制响应（如 `response_format=wav`）不返回 `usage` 字段，计费仍按实际 token/音频秒数计算  
- [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档中声明的“支持 8-bit WAV 输出”为历史版本遗留描述，当前仅支持 16-bit WAV 与 MP3，该信息已在最新 SDK 中同步修正

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


