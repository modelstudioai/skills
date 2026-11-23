# realtime api directory

实时 API 目录汇总了百炼平台支持的低延迟、流式音视频处理能力，适用于语音识别、语音合成、实时翻译、多模态交互等场景。所有接口均基于 WebSocket 协议设计，支持逐帧/逐 token 流式响应。开发者需通过 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 文档入口获取完整子模块索引。

## 支持的模型与功能

当前目录涵盖以下核心能力：
- **实时语音识别（ASR）**：支持中英文混合识别、标点预测、说话人分离（部分模型）  
- **实时语音合成（TTS）**：流式音频输出，支持情感韵律控制与多音色切换  
- **实时多模态交互（Omni）**：融合语音、文本、图像输入的端到端实时推理（见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)）  
- **Qwen-Audio 系列**：包括 `Qwen-Audio-Realtime`（低延迟音频理解）和 `Qwen-Audio-Live`（直播场景优化版），二者接口结构相似但流控策略不同  
- **实时音视频翻译（LiveTranslate）**：支持源语种语音→目标语种语音的端到端流式翻译  

> **注意**：[Qwen-Audio-Live](../../raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory.md) 文档中标注的“默认启用自动静音检测”与 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 中“需显式设置 `enable_silence_detection: true`”存在不一致，以后者为准——该参数必须显式传入才生效。

## 关键参数

通用必需参数（所有实时 API 共享）：
- `model`: 模型标识符（如 `qwen-audio-realtime`, `qwen2-asr-16k`）  
- `stream`: 必须为 `true`  
- `response_format`: 可选 `json`（结构化事件）或 `pcm`（原始音频流，仅 TTS/LiveTranslate 支持）  
- `audio_encoding` / `sample_rate`: 音频输入格式约束（详见各子模型文档）  

模型特有参数示例：
- ASR：`language`, `punctuation_prediction`, `speaker_diarization`  
- TTS：`voice`, `speed`, `pitch`  
- LiveTranslate：`source_lang`, `target_lang`, `translate_mode`（`speech_to_speech` 或 `speech_to_text`）

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/api/v1/realtime/{model}`  
2. 发送 `session.update` 初始化请求（含参数与配置）  
3. 分帧发送 `input.audio` 二进制数据（PCM/WAV 格式，按文档要求切片）  
4. 接收 `output.*` 事件流（文本、音频 chunk 或结构化结果）  
5. 主动发送 `session.terminate` 结束会话  

完整握手与错误码说明请参阅 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 的“连接流程”章节。

## 限制和注意事项

- 单次会话最长 300 秒，超时后连接自动关闭  
- 音频输入需严格满足采样率（如 16kHz）、位深（16-bit）、单声道要求，否则返回 `400 Bad Audio Format`  
- Qwen-Audio-Realtime 与 Qwen-Audio-Live **不可混用同一 `model` 参数调用**，即使路径相同——模型服务后端路由逻辑已分离  
- 所有实时 API **不支持 HTTP 轮询替代 WebSocket**；尝试使用 REST 接口将返回 `405 Method Not Allowed`  
- 流式响应中 `output.text` 事件可能包含中间结果（如 ASR 的 partial transcript），最终结果以 `is_final: true` 字段标识——该行为在 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 和 [Qwen-Audio-Realtime](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 中定义一致，但 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md) 文档未明确说明 `is_final` 含义，建议以实际响应字段为准。

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


