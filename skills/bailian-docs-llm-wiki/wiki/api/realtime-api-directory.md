# realtime api directory

实时 API 目录汇总了百炼平台支持的低延迟、流式交互类音视频模型能力，涵盖语音识别（ASR）、语音合成（TTS）、多模态理解与生成、实时翻译等场景。所有接口均面向流式输入/输出设计，适用于通话助手、实时字幕、虚拟人交互等对端到端延迟敏感的应用。开发者需结合具体模型文档确认能力边界与调用细节。

## 支持的模型与功能

当前目录包含以下核心能力模块：
- 实时多模态交互：支持音频+文本联合输入与响应，详见 [实时多模态](../../raw/realtime-api-directory/omni-realtime-api-directory.md)  
- 实时语音识别（ASR）：流式语音转文本，支持多语种与标点恢复  
- 实时语音合成（TTS）：低延迟音频流生成，支持情感与语速调节  
- Qwen-Audio-Realtime：专为高并发实时音频理解优化的轻量模型，见 [Qwen-Audio-Realtime](../../raw/realtime-api-directory/audio-realtime-api-directory.md)  
- Qwen-Audio-Live：面向直播/会议场景的增强型音频模型，含回声抑制与说话人分离能力，参见 [Qwen-Audio-Live](../../raw/realtime-api-directory/qwen-audio-live-api-directory.md)  
- 实时音视频翻译：支持源音视频流→目标语言文本/语音的端到端翻译，参考 [实时音视频翻译](../../raw/realtime-api-directory/livetranslate-realtime-api-directory.md)

> **注意**：[Qwen-Audio-Live](../../raw/realtime-api-directory/qwen-audio-live-api-directory.md) 文档中声明支持“实时双语字幕”，但 [实时音视频翻译](../../raw/realtime-api-directory/livetranslate-realtime-api-directory.md) 当前版本未开放对应字段；实际使用请以后者最新参数说明为准。

## 关键参数

通用关键参数（各子接口可能扩展）：
- `model`: 必填，模型标识符（如 `qwen-audio-realtime-v1`），须与 [实时多模态](../../raw/realtime-api-directory/omni-realtime-api-directory.md) 等对应文档一致  
- `stream`: 布尔值，必须设为 `true`（实时 API 不支持非流式调用）  
- `input_format` / `output_format`: 指定音频编码（如 `pcm16`、`opus`），需与 SDK 或客户端配置匹配  
- `max_latency_ms`: 可选，建议值 200–800，影响响应速度与识别准确率权衡  

## 使用方式

1. 通过 `POST /v1/realtime/chat/completions`（或对应子路径如 `/v1/realtime/asr`）发起请求  
2. 使用 `Content-Type: application/json`，携带上述关键参数及音频分块数据（Base64 编码或 WebSocket 流式帧）  
3. 响应以 Server-Sent Events（SSE）或 WebSocket 消息流返回，每帧含 `delta` 或 `final` 字段标识增量/终局结果  
4. 客户端需按 [概述](../../raw/realtime-api-directory/realtime-api-overview.md) 中定义的帧协议处理连接生命周期（如心跳、重连、超时）

## 限制和注意事项

- 单次会话最长持续 30 分钟，超时后连接自动关闭  
- 音频采样率须严格匹配模型要求（常见为 16kHz PCM，不支持 44.1kHz 直接输入）  
- WebSocket 连接需在 5 秒内完成鉴权握手，否则断连；重连间隔建议 ≥1s  
- 所有实时接口暂不支持 `response_format` 结构化输出（如 JSON mode），仅返回文本或音频流  
- 多模态与 ASR/TTS 接口的 `temperature` 参数行为不一致：前者影响推理多样性，后者仅作用于 TTS 语音自然度——详见 [实时多模态](../../raw/realtime-api-directory/omni-realtime-api-directory.md) 与 [实时语音合成](../../raw/realtime-api-directory/realtime-tts-model-apis.md) 文档说明

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


