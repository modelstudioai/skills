# realtime api directory

realtime api directory 是百炼平台提供的实时音视频处理能力的统一入口，涵盖语音识别（ASR）、语音合成（TTS）、多模态理解与生成、实时翻译等低延迟交互场景。所有接口均面向流式输入/输出设计，适用于智能客服、实时会议、无障碍交互等对端到端延迟敏感的应用。该目录结构化组织了当前可用的实时模型及其调用规范，是开发者集成实时音视频能力的首要参考。

## 支持的模型与功能

当前目录覆盖以下核心实时能力模块：
- 实时语音识别（ASR）：支持中文、英文及多语种流式识别，含标点恢复与说话人分离选项  
- 实时语音合成（TTS）：提供多音色、可控语速与情感韵律的流式音频生成  
- 实时多模态（Omni-Realtime）：融合音频、文本、部分视觉信号的联合建模接口  
- Qwen-Audio-Realtime 与 Qwen-Audio-Live：面向不同延迟与精度权衡的专用音频大模型  
- 实时音视频翻译（LiveTranslate）：支持双语实时字幕与语音转译  

各模型详情请参阅 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 中的子目录链接；其中 [实时语音识别](../../raw/realtime-api-directory/realtime-asr-model-apis.md) 和 [实时语音合成](../../raw/realtime-api-directory/realtime-tts-model-apis.md) 的参数定义与返回格式具有典型代表性，建议优先查阅。

## 关键参数

所有实时 API 均采用 WebSocket 协议，关键参数包括：
- `model`: 必填，如 `qwen-audio-realtime-v1`、`qwen2-tts-realtime-v1`，需严格匹配 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 中公布的模型 ID  
- `audio_format`: 音频编码格式（`pcm16` / `opus` / `aac`），必须与实际传输数据一致  
- `sample_rate`: 采样率（Hz），常见值为 `16000` 或 `48000`，需与 `audio_format` 兼容  
- `enable_intermediate_results`: 控制是否返回中间识别结果（ASR）或分段合成音频（TTS）  
- `language`: ASR/TTS 场景下必填，如 `zh-CN`、`en-US`；多语种混合识别需显式声明主语言  

> **注意**：部分旧文档中将 `streaming_mode` 列为可选参数，但根据最新 [实时多模态](../../raw/realtime-api-directory/omni-realtime-api-directory.md) 规范，该字段已废弃，应统一使用 `enable_intermediate_results` 控制流式行为。

## 使用方式

1. 建立 WebSocket 连接，Endpoint 格式为 `wss://dashscope.aliyuncs.com/api/v1/realtime/{model}`  
2. 发送 `{"type": "config", ...}` 初始化消息（含参数）  
3. 持续发送 `{"type": "audio", "data": "base64..."}` 或 `{"type": "text", ...}` 数据帧  
4. 接收服务端推送的 `{"type": "result" | "error" | "final"}` 响应  

完整握手流程与错误码说明见 [实时语音识别](../../raw/realtime-api-directory/realtime-asr-model-apis.md) 的“连接与协议”章节。

## 限制和注意事项

- 单次会话最长持续 30 分钟，超时后连接自动关闭  
- 音频流需保持恒定采样率与格式，突发格式切换将导致 `400 Bad Request`  
- TTS 接口不支持实时变声或动态音色切换，需在初始化时固定 `voice_id`  
- Qwen-Audio-Live 模型仅支持 `pcm16` + `16000Hz` 输入，与其他模型参数兼容性存在差异，详见 [Qwen-Audio-Live](../../raw/realtime-api-directory/qwen-audio-live-api-directory.md) 文档  
- 所有实时 API 均不支持 HTTP 轮询调用，仅限 WebSocket；尝试使用 REST 方式将返回 `405 Method Not Allowed`

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


