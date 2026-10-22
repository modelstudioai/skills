# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频生成、语音对话及语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前支持以下五类音频处理能力，对应独立的 API 端点与模型标识：

- **语音合成（TTS）**：支持多语种、多音色，模型如 `qwen-audio-tts-v1`  
- **语音识别（ASR）**：支持长音频转写、实时流式识别，模型如 `qwen-audio-asr-v1`  
- **音频生成（Audio Generation）**：支持文本到音频（如环境音、音乐片段），模型如 `qwen-audio-gen-v1`  
- **语音对话（Voice Conversation）**：端到端语音交互，含唤醒、理解、合成闭环，模型如 `qwen-voice-conversation-v1`  
- **语音翻译（Speech Translation）**：支持源语音→目标语言文本/语音双路径输出，模型如 `qwen-speech-translate-v1`  

各能力详情请参阅 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 和 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 的独立参考文档。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 模型 ID（如 `qwen-audio-asr-v1`），不可省略  
- `input.audio`: Base64 编码的音频数据（WAV/MP3/FLAC，采样率 ≥ 8kHz，单文件 ≤ 100MB）  
- `input.text`（部分接口可选）：用于 TTS 或语音翻译的提示文本  

常用可选参数：
- `stream`: 布尔值，启用流式响应（仅 ASR、TTS、Voice Conversation 支持）  
- `response_format`: `"json"`（默认）或 `"wav"`（TTS 专用）  
- `language`: 指定音频语言（ASR/TTS 必须显式声明，详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)）  

> **注意**：`sample_rate` 参数在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中被列为必填，但实际调用时若未提供，服务端将自动降级为默认值 24000Hz；该行为与 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中明确要求客户端指定采样率的说明存在不一致，建议始终显式传入以确保兼容性。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求方法**：全部使用 `POST`  
3. **Endpoint**：统一为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`，其中 `<service_name>` 对应 `tts` / `asr` / `audio-generation` / `voice-conversation` / `speech-translation`  
4. **示例（TTS）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/tts" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-audio-tts-v1",
           "input": {"text": "你好，欢迎使用百炼音频 API。"},
           "parameters": {"voice": "zhitian_emo", "sample_rate": 24000}
         }'
   ```

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 60 秒，Audio Generation ≤ 10 秒，Voice Conversation 单轮 ≤ 30 秒  
- 频率限制：默认 5 QPS（企业版可申请提升），超出返回 `429 Too Many Requests`  
- 音频格式：仅接受 PCM（WAV）、MP3、FLAC；不支持 AMR、AAC 等编码  
- 错误码统一遵循 [百炼通用错误规范](../../raw/common/error-codes.md)，音频类特有错误见各子文档末尾的“错误响应”章节  
- 流式响应需设置 `Accept: text/event-stream` 头，且仅部分模型支持——具体支持情况请严格参照 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中的“流式能力说明”表格

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


