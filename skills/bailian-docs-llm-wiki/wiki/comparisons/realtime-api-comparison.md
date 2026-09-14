# 实时 API 方案对比：Realtime API 与 Omni Realtime API

为帮助开发者在百炼平台中快速识别并选用最适合业务需求的实时交互接口，本文对两种核心实时 API 方案——**Realtime API** 与 **Omni Realtime API**——进行系统性对比分析。二者均面向低延迟、流式响应场景设计，但在架构定位、能力边界、协议约束及适用范式上存在本质差异。本对比基于当前（2024年Q3）正式发布版本（v2024.09+），所有信息以控制台实际可用能力及最新 API 文档为准。

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **定位与目标场景** | 通用型流式大模型交互接口，聚焦「文本/多模态内容生成」的实时化交付 | 端到端实时多模态交互引擎，聚焦「语音↔文本↔语音」闭环的毫秒级协同（ASR+LLM+TTS 全链路） |
| **输入格式** | 支持结构化 `messages` 数组（含 `image_url`、`audio` 字段）；支持 base64 图像、PCM 音频帧（仅 `qwen2-audio`）；HTTP/2 或 WebSocket 帧传输 | 仅支持 WebSocket；以事件流方式持续接收 `input_audio_buffer`（PCM16/Opus）、`input_text`、`session.update` 等事件；不接受 JSON 请求体 |
| **输出格式** | SSE 格式事件流（`message_start` / `content_block_delta` / `tool_use` / `message_stop` 等），纯文本或结构化 content block | WebSocket 二进制/文本混合事件流：`response_text_delta`（文本增量）、`audio_chunk`（原始 PCM 音频字节）、`input_audio_transcript`（ASR 结果）、`voice_cloned_audio` 等 |
| **支持模型** | `qwen-max`、`qwen-plus`、`qwen-turbo`（stream=true）、`qwen2-audio`；**不支持 `qwen-omni-realtime`** | **仅支持 `qwen-omni-realtime`（v1.0+）**；不兼容 `qwen-max`、`qwen2-audio` 等其他模型 |
| **协议支持** | ✅ WebSocket（`wss://.../realtime/v1/chat`）<br>✅ HTTP/2（`POST https://.../realtime/v1/chat`） | ✅ WebSocket **仅此一种**（`wss://.../realtime/v1/omni`）<br>❌ 不支持 HTTP/1.1、HTTP/2、轮询等任何替代协议 |
| **流式控制能力** | 支持 `input_interrupt` 事件实现服务端即时中断；支持工具调用（function calling）与结构化输出；支持 `system` 消息与完整对话上下文管理 | 支持全双工持续音频输入（无需等待响应结束）；支持 `cancel_response` 中断当前 TTS/生成；支持 `input_text` 插入文本指令；**不提供 function calling 或 tool 调用能力** |
| **多模态能力** | ✅ 图像理解（`qwen-vl` 已下线，当前仅 `qwen2-audio` 支持音频输入）<br>✅ 多图/多轮图像混合输入（需模型支持） | ✅ 原生 ASR（语音转文本）<br>✅ 原生 TTS（文本转语音）<br>✅ 可选声音复刻（Voice Cloning）<br>❌ 不支持图像输入/理解 |
| **计费方式** | 按 **输入 token + 输出 token** 分别计费（含 system [prompt](../guides/prompt.md)、messages、tools、audio/image 编码开销）；音频/图像按等效 token 折算 | 按 **会话时长（秒） + 音频输入时长（秒） + 文本输出 token** 组合计费；声音复刻额外收取参考音处理费用；**无独立输入 token 计费项** |
| **典型场景** | • 实时客服对话机器人（带图片上传）<br>• 代码辅助 IDE 插件（流式补全+工具调用）<br>• 音频问答（语音提问 → 文本回答，`qwen2-audio`）<br>• 多轮图文混合创作助手 | • 智能车载语音助手（说即所得，边说边答边播）<br>• 实时会议纪要+发言人语音复述<br>• 视障用户无障碍交互终端（语音输入→文本摘要→语音播报）<br>• 客服语音坐席实时辅助（ASR 实时转写 + LLM 话术建议 + TTS 播报） |

## 各方案适用场景建议

### ✅ 选择 Realtime API 当且仅当：
- 你的核心诉求是**低延迟获取大模型文本/结构化输出**，且可能涉及图像理解、[函数调用](../concepts/function-calling.md)、复杂对话状态管理；
- 输入以文本为主，辅以偶尔的图片或短音频（如用户上传截图或语音问题）；
- 需要灵活部署方式（可选 HTTP/2 降低客户端接入门槛）；
- 对 ASR/TTS 能力无原生依赖，或已自建语音前后处理链路；
- 业务逻辑需强上下文控制（如 `system` 角色设定、多轮 `tool` 调用编排）。

### ✅ 选择 Omni Realtime API 当且仅当：
- 你构建的是**端到端语音优先的实时交互产品**，要求“说话即响应、响应即播放”，对端到端延迟（P95 < 800ms）有硬性要求；
- 必须同时使用 ASR（语音转写）、LLM（语义理解与生成）、TTS（语音播报）三者，并期望由平台统一调度、共享上下文、避免模块间数据转换损耗；
- 需要声音复刻能力，为特定角色/品牌定制合成音色；
- 客户端具备稳定 WebSocket 连接能力，且可处理二进制音频流收发与事件驱动状态机；
- 不需要图像理解、不依赖 function calling，也不需将模型响应嵌入非语音工作流。

> ⚠️ 注意：二者**不可混用或级联**。`qwen-omni-realtime` 模型无法通过 Realtime API 调用；反之，`qwen-max` 等模型也无法接入 Omni Realtime API 协议。

## 技术选型参考（面向开发者）

| 评估项 | Realtime API | Omni Realtime API | 建议动作 |
|----------|--------------|-------------------|----------|
| **是否必须支持图像输入？** | 是 → ✅ | 否 → ❌ | 选 Realtime API |
| **是否必须原生支持语音输入+语音输出闭环？** | 否（需自行集成 ASR/TTS） | 是 → ✅ | 选 Omni Realtime API |
| **是否需要 function calling 或 JSON Schema 输出？** | 是 → ✅ | 否 → ❌ | 选 Realtime API |
| **客户端能否稳定维持 WebSocket 连接？** | 可选 HTTP/2，容错性更高 | 必须 WebSocket，需实现重连/心跳/二进制帧解析 | 若弱网环境多，优先评估 Realtime API 的 HTTP/2 路径 |
| **对端到端语音延迟敏感度（如车载/会议）？** | 通常 ≥ 1.2s（ASR+LLM+TTS 分离链路） | P95 < 800ms（全链路融合优化） | 高敏感 → 选 Omni Realtime API |
| **是否需复刻特定人声？** | 不支持 | ✅（需提前注册 voice_id） | 选 Omni Realtime API |

**最终决策口诀**：  
🔹 **“要智能，选 Realtime；要声临其境，选 Omni”**  
🔹 **“图文/工具/灵活协议” → Realtime API**  
🔹 **“语音入口、语音出口、声纹定制” → Omni Realtime API**

如需进一步验证性能指标或进行沙箱压测，建议通过百炼控制台「API 调用」页分别创建两个 API Key 配额，结合 [Python SDK 示例](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start) 进行端到端延迟与稳定性实测。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


