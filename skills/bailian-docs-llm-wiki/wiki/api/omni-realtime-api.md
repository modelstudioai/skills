# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态交互接口，支持语音、文本、图像等模态的实时输入与模型响应。该 API 采用 WebSocket 协议实现双向实时通信，适用于语音助手、实时翻译、多模态对话等场景。其设计强调端到端延迟可控、事件语义清晰，并与百炼统一鉴权和配额体系集成。

## 支持的模型与功能

当前仅支持 `qwen-omni-realtime-202410` 模型（v2.1+），该模型支持语音流式输入（ASR + LLM + TTS 端到端联合推理）、文本指令注入、图像帧增量上传及跨模态上下文感知。不支持历史会话回溯或离线批量处理。详细能力边界请参阅 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 文档。

## 关键参数

- `model`: 必填，固定为 `qwen-omni-realtime-202410`  
- `audio_encoding` / `sample_rate`: 音频输入格式参数，仅当发送 `input_audio` 事件时生效；必须与 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中定义的 `input_audio` schema 严格一致  
- `enable_interim_results`: 布尔值，启用中间语音识别结果（ASR partial），默认 `false`；开启后将触发额外 `interim_transcript` 服务端事件  
- `max_duration_sec`: 单次会话最大持续时间，取值范围 `30–300`，超时后连接强制关闭  

> **注意**：原始文档中 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 提到支持 `qwen-omni-realtime-202408`，但该版本已于 2024-11-01 下线，实际调用将返回 `404 model_not_found`；请以控制台模型列表或 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 主文档为准。

## 使用方式

1. 通过 `wss://dashscope.aliyuncs.com/realtime/v1/omni` 建立 WebSocket 连接（需携带 `Authorization: Bearer <api_key>`）  
2. 发送 `session.update` 初始化会话（含 `model`、`max_duration_sec` 等配置）  
3. 按需发送客户端事件，如 `input_audio`、`input_text` 或 `input_image`（参考 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）  
4. 接收服务端事件，包括 `response.text_delta`、`response.audio_delta`、`error` 等（详见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）  
5. 主动发送 `session.terminate` 或等待超时/错误自动断连  

## 限制和注意事项

- 单连接最大并发请求数：1（不支持复用连接发送多个独立会话）  
- 音频流必须按 20ms 分片（16kHz PCM 编码），且连续分片时间戳不得跳变或重复  
- 图像输入仅支持 JPEG/PNG，单帧尺寸 ≤ 1024×1024，总带宽建议 ≤ 2 Mbps（含音频）  
- 错误重连需重新建立 WebSocket 连接，不可复用旧连接 ID；重试间隔应 ≥ 1s 以避免触发限流  
- 所有事件字段名、类型及触发条件均以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 文档为权威依据，SDK 实现须严格校验 JSON Schema。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


