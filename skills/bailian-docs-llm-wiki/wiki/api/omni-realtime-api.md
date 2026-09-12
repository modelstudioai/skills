# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式[多模态](../concepts/multi-modal.md)交互接口，支持语音输入、文本理解、语音合成与声音复刻的端到端实时协同。该 API 采用事件驱动架构，通过客户端和服务端双向事件流实现毫秒级响应，适用于智能客服、实时会议助手、交互式教育等场景。详细协议规范和事件定义请参考 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。

## 支持的模型与功能

- **基础模型**：仅支持 `qwen-omni-realtime` 系列专属模型（如 `qwen-omni-realtime-202410`），不兼容通用大模型（如 `qwen-max` 或 `qwen-plus`）。
- **核心能力**：
  - 实时语音识别（ASR）与语义理解（NLU）联合处理；
  - 流式文本生成（LLM）与语音合成（TTS）同步输出；
  - 声音复刻（Voice Cloning）支持用户上传 30 秒以上参考音频，生成个性化语音；具体流程见 [声音复刻](../../raw/model-api-reference/omni-realtime-api.md)。
- **注意**：文档中提及的“支持图像输入”为过时描述——当前 `omni realtime api` **不支持图像或视频模态输入**，仅处理音频+文本。该矛盾已在 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api.md) 的最新修订版中修正。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-omni-realtime-202410`（以实际控制台可用版本为准） |
| `audio_input_format` | string | 否 | 默认 `pcm16`；支持 `pcm16`、`opus`；需与客户端采样率一致（推荐 16kHz） |
| `voice_clone_id` | string | 否 | 声音复刻 ID，需提前通过 `/v1/voice-clones` 创建；详见 [声音复刻](../../raw/model-api-reference/omni-realtime-api.md) |
| `enable_interim_results` | boolean | 否 | 默认 `false`；设为 `true` 时返回 ASR 中间结果（含 `is_final=false` 事件） |

## 使用方式

1. **建立 WebSocket 连接**：  
   请求地址为 `wss://dashscope.aliyuncs.com/api/v1/omni-realtime`，需携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Date` 时间戳头。
2. **发送初始化事件**：  
   客户端首帧必须为 `session.init` 事件，包含 `model`、`audio_input_format` 等参数。
3. **流式交互**：  
   - 音频数据以二进制帧（非 Base64）分块发送，每帧 ≤ 20ms PCM 数据；
   - 服务端按需返回 `response.text.delta`、`response.audio.delta`、`response.voice_clone.status` 等事件；
   - 完整事件定义请查阅 [客户端事件](../../raw/model-api-reference/omni-realtime-api.md) 与 [服务端事件](../../raw/model-api-reference/omni-realtime-api.md)。

## 限制和注意事项

- **连接时长**：单次会话最长 180 秒，超时后连接自动关闭；
- **并发限制**：免费版限 2 路并发；企业版按配额计费，需在控制台查看实时用量；
- **音频质量**：输入音频信噪比应 ≥ 15dB，静音段建议 ≤ 500ms，否则可能触发误中断；
- **注意**：Python SDK 与 Java SDK 的默认重连策略不同（Python 自动重试 3 次，Java 不重连），生产环境务必显式配置重连逻辑——该差异未在 [Python SDK](../../raw/model-api-reference/omni-realtime-api.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api.md) 文档中明确对比说明，需开发者自行验证。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)



