# realtime api directory

百炼平台的 Realtime API Directory 是一组面向低延迟、高并发音视频场景的实时模型服务接口集合，覆盖语音识别（ASR）、语音合成（TTS）、语音对话、音视频翻译及多模态交互等核心能力。所有接口均基于 WebSocket 协议设计，支持流式输入/输出与双向实时交互。开发者需通过 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md) 或 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 接入，不支持 HTTP 轮询调用。

## 支持的模型/功能

- **实时语音识别（ASR）**：支持中英文混合、多方言（如粤语、四川话）及噪声环境鲁棒识别，详见 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md)  
- **实时语音合成（TTS）**：提供多音色、情感可控、端到端低延迟合成，支持 SSML 标记；注意：部分音色仅限企业版开通，具体以 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md) 文档为准  
- **实时语音对话（Audio Chat）**：集成 ASR+LLM+TTS 全链路，支持上下文感知的流式对话，底层协议见 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md)  
- **实时音视频翻译（LiveTranslate）**：支持双语字幕同步生成与音频实时转译，当前仅开放中↔英、中↔日、中↔韩三组语向  
- **多模态交互**：通过 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 支持音视频+文本+视觉事件（如唇动、手势）联合建模，适用于智能座舱、远程医疗等场景  

> **注意**：[实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 文档中提及的“视觉流帧内推理”功能尚未全量上线，当前仅对白名单客户开放，正式商用时间请以控制台公告为准。

## 关键参数

- `model`: 必填，取值如 `asr-general-v2`、`tts-zeus-zh`、`audio-chat-v3`，需与所选 SDK 版本兼容（v3 SDK 不兼容 v1 模型 ID）  
- `stream`: 布尔值，必须为 `true`；Realtime API 不提供非流式模式  
- `sample_rate`: 音频采样率，ASR/TTS 接口要求 `16000`，Audio Chat 要求 `24000`（详见 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md)）  
- `enable_intermediate_result`: ASR 专用，启用后返回中间识别结果（含 `is_final=false` 的分片），默认 `false`  
- `voice`: TTS 专用，指定音色 ID，须在控制台「语音合成」页申请并获取授权  

## 使用方式

1. 在百炼控制台开通对应实时 API 权限，并获取 API Key 与 Endpoint（如 `wss://realtime.api.bailian.aliyuncs.com/v1`）  
2. 初始化 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md) 实例，传入 `endpoint`、`api_key` 和 `model`  
3. 建立连接后，按协议发送 `{"type": "config", ...}` 初始化帧，再持续推送音频二进制数据（PCM 编码，小端序）  
4. 服务端通过 `{"type": "result"}` 或 `{"type": "error"}` 帧响应；错误码定义参考 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md) 附录  

## 限制和注意事项

- 单连接最大时长：15 分钟（超时将主动断连，需客户端重连）  
- 音频流必须连续，中断超过 3 秒将触发会话重置（ASR 清空上下文，TTS 中断播放）  
- 同一 `api_key` 下，ASR/TTS/Audio Chat 三类服务共享 QPS 限额（默认 50 QPS），不可单独提升某一项  
- > **注意**：[实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 文档中“支持 48kHz 输入”的描述已过时；自 2024 年 7 月起，所有 ASR 接口统一要求 `16000Hz`，48kHz 输入将被自动重采样，可能引入额外延迟与失真  
- 所有实时 API 均不支持跨区域调用（如华东1区密钥不可用于华北2区 endpoint），区域绑定信息在控制台「API 管理」页可查

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


