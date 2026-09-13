# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式[多模态](../concepts/multi-modal.md)交互接口，支持语音输入、文本理解、语音合成与声音复刻等能力的端到端实时协同。该 API 采用事件驱动模型，通过客户端事件和服务端事件双向通信，适用于智能客服、实时会议助手、虚拟人交互等场景。详细协议规范与交互时序可参考 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api.md)。

## 支持的模型/功能

- **[多模态](../concepts/multi-modal.md)理解与生成**：支持语音转文本（ASR）、文本到语音（TTS）、意图识别与上下文感知响应生成  
- **声音复刻（Voice Cloning）**：支持零样本/少样本声音克隆，需提前注册声纹或上传参考音频，具体能力见 [声音复刻](../../raw/model-api-reference/omni-realtime-api.md)  
- **实时流式处理**：全程端到端延迟控制在 300ms 内（网络正常条件下），支持持续语音流输入与渐进式响应输出  

> **注意**：文档中提及的“Qwen-Omni”为旧版命名，当前服务统一标识为 `qwen-omni-realtime`，SDK 和 API 路径均已更新；请以 [Python SDK](../../raw/model-api-reference/omni-realtime-api.md) 文档中的 model 参数为准，避免使用已弃用的 `qwen-omni` 字符串。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定值 `qwen-omni-realtime`（非 `qwen-omni`） |
| `audio_input_format` | string | 否 | 音频编码格式，支持 `pcm16`（默认）、`opus`；需与实际传输格式一致 |
| `voice_id` | string | 否 | 声音复刻使用的 voice ID；若未提供，则使用默认合成音色 |
| `enable_intermediate_results` | boolean | 否 | 是否启用中间 ASR 结果（用于实时字幕），默认 `false` |

## 使用方式

1. 建立 WebSocket 连接至 `wss://dashscope.aliyuncs.com/realtime/v1/omni`  
2. 发送 `session.create` 消息初始化会话（含 `model`、`voice_id` 等配置）  
3. 通过 `input.audio` 或 `input.text` 发送用户输入；服务端按需返回 `output.audio`、`output.text`、`output.intermediate` 等事件  
4. 客户端需监听并正确处理 [服务端事件](../../raw/model-api-reference/omni-realtime-api.md) 中定义的各类状态码与错误类型（如 `error.no_voice_id`）

## 限制和注意事项

- 单次会话最长 5 分钟，超时后连接自动关闭  
- 音频流需严格按采样率 16kHz、单声道、PCM 小端序（`pcm16`）格式分帧发送，否则触发 `invalid_audio_format` 错误  
- 不支持跨会话复用 `voice_id` 的临时声纹；每次新会话需重新提交声纹注册请求或确保 `voice_id` 已在控制台完成审核  
- 客户端必须实现重连机制，并在收到 `session.expired` 事件后主动重建会话——该行为细节在 [客户端事件](../../raw/model-api-reference/omni-realtime-api.md) 中有明确定义

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


