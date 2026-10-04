# audio api references

百炼平台的 Audio API 提供语音合成、识别、翻译、对话、音乐及通用音频生成等能力，所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应。各功能由专用模型提供服务，需在请求中明确指定 `model` 参数。开发者应优先参考各子功能的独立 API 文档以获取完整参数定义与示例。

## 支持的模型与功能

当前支持以下六大音频处理能力，每个能力对应独立模型和接口路径：

- **语音合成（TTS）**：支持多语种、多音色，模型如 `qwen2-audio-tts-0.5b`；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持长音频转写、标点恢复与说话人分离；详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **语音翻译（ST）**：支持源语言到目标语言的端到端语音翻译，不返回中间文本；详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)  
- **音频生成（Audio Gen）**：基于文本生成环境音、音效等非音乐类音频；参见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **音乐生成（Music Gen）**：支持旋律、风格、时长控制，输出 MP3/WAV；参见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- **语音对话（Voice Conversation）**：实时双工语音交互，需 WebSocket 连接；参见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)

> **注意**：`qwen2-audio-tts-0.5b` 与 `qwen2-audio-tts-1.0b` 均在文档中被提及，但 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中明确说明仅 `qwen2-audio-tts-0.5b` 为当前 GA 版本，`1.0b` 尚处于灰度阶段，调用可能失败。

## 关键参数

所有 Audio API 共享以下基础参数（必填）：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 模型标识符，如 `qwen2-audio-tts-0.5b`、`qwen2-audio-asr-1.0b`；必须与所选功能匹配 |
| `input` | object | 输入数据结构，具体字段依功能而异（如 `audio_url`、`text`、`prompt`）；详见各子文档 |
| `parameters` | object | 可选配置项，如 `voice`（TTS）、`language`（ASR）、`duration`（Music Gen）等 |

部分功能支持 `stream: true` 启用流式响应（如 TTS、ASR、Voice Conversation），此时响应为 SSE 格式；非流式响应统一返回 JSON，含 `output.audio_url` 或 `output.text` 字段。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/audio/<endpoint>`，其中 `<endpoint>` 为功能路径（如 `tts`、`asr`、`music_generation`）  
3. **Body 示例（TTS）**：
   ```json
   {
     "model": "qwen2-audio-tts-0.5b",
     "input": {"text": "你好，欢迎使用百炼音频 API。"},
     "parameters": {"voice": "zhitian_emo"}
   }
   ```
4. 更多调用示例与 SDK 用法，请查阅各功能对应的原始文档，例如 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中提供了 Python 和 cURL 完整示例。

## 限制和注意事项

- 单次请求音频时长上限：ASR 最长 60 分钟，TTS 输出最长 5 分钟，Music Gen 最长 30 秒（[音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 明确标注）  
- 音频格式要求：输入仅支持 `mp3`、`wav`、`m4a`、`flac`；采样率建议 16kHz/44.1kHz，位深 16bit  
- 所有接口均按 token 或音频秒数计费，具体计费规则见控制台配额页  
- > **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中声明支持 `opus` 编码直传，但实际接入时需先转为 `wav` 或通过 SDK 封装，原始 WebSocket 接口暂不接受 raw opus 流 —— 此处与 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 的编码兼容性说明存在不一致，建议以 SDK 实现为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


