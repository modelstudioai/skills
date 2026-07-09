# Qwen API vs 全双工实时API vs 托管智能体API

百炼平台提供多种 API 接口满足不同开发场景。Qwen API 面向文本生成任务，提供多协议兼容的 HTTP 接口；全双工实时 API（Omni Realtime）基于 WebSocket 实现低延迟的音视频实时对话；托管智能体 API（Managed Agents）则提供完整的智能体托管运行时，由平台负责会话编排与沙箱执行。本文从协议、能力、适用场景等维度帮助开发者做出技术选型。

## 关键维度对比

| 维度 | Qwen API | 全双工实时 API | 托管智能体 API |
| --- | --- | --- | --- |
| 通信协议 | HTTP（REST） | WebSocket（长连接） | HTTP（REST）+ SSE 事件流 |
| 输入格式 | 文本（messages JSON） | 音频流（PCM 16kHz）、图像（Base64） | 文本消息、文件附件 |
| 输出格式 | 文本（支持流式 SSE） | 音频流（PCM 24kHz）+ 文本转录 | 事件流（SSE），含文本、工具调用回执等 |
| 支持模型 | Qwen 系列文本生成模型 | Qwen3.5-Omni-Realtime、Qwen3-Omni-Flash-Realtime、Qwen-Omni-Turbo-Realtime | 可配置任意百炼平台模型 |
| API 端点 | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` 等 | `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime` | `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio` |
| 兼容协议 | OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、DashScope 原生 | 无（百炼专有 WebSocket 协议） | 无（百炼专有 REST 协议） |
| 工具调用 | Responses 接口内置联网搜索/代码解释器/网页提取；其他接口需自定义 | 支持 Function Calling 和联网搜索（仅 Qwen3.5 系列） | 平台托管技能（Skill zip 包），沙箱内执行 |
| 会话管理 | 仅 Responses 接口自动管理历史；其他需客户端维护 | 平台维护 WebSocket 会话上下文 | 平台全托管（Session 状态机：idle → running → idle/terminated） |
| 延迟特性 | 标准 HTTP 请求-响应，流式可逐 token 返回 | 超低延迟（毫秒级音频帧推送） | 异步任务式，SSE 实时推送中间事件 |
| 多模态支持 | 纯文本（部分模型支持图像输入） | 音频 + 视频 + 图像 + 文本 | 文本 + 文件（通过 File 资源挂载） |
| 计费方式 | 按 token 计费（输入/输出分计） | 按音频时长 + token 计费 | 按底层模型 token + 沙箱资源用量计费 |

## 适用场景建议

### Qwen API

- **文本问答与对话**：聊天机器人、客服对话、内容生成等标准 NLP 任务
- **快速迁移**：已有 OpenAI 或 Anthropic 代码的项目，可通过兼容接口低成本切换到 Qwen 模型
- **轻量工具调用**：使用 Responses 接口可直接获得联网搜索、代码解释器能力，无需额外开发
- **批量处理**：适合离线或准实时的文本处理流水线

### 全双工实时 API

- **语音助手**：需要实时语音输入并即时语音回复的场景
- **智能客服**：基于 VAD 自动检测用户说话意图，实现自然的对话轮转
- **多模态交互**：需要同时处理音视频输入的实时应用（如视频通话中的 AI 助手）
- **声音定制**：利用声音复刻能力打造品牌专属语音形象

### 托管智能体 API

- **复杂任务编排**：智能体需要多轮推理、工具调用、代码执行的场景
- **平台托管运行时**：不想自行管理会话状态、沙箱环境和工具执行的团队
- **企业级智能体**：需要版本管理、权限控制、文件交互等完整生命周期管理
- **多技能组合**：通过 Skill 机制灵活组装工具链，且由平台保证安全审核

## 技术选型指引

1. **只需文本生成** → 选择 Qwen API。如已有 OpenAI/Anthropic SDK 代码，使用对应兼容接口可零改动迁移。
2. **需要实时语音交互** → 选择全双工实时 API。它是唯一支持音频流式双向通信的接口，延迟最低。
3. **需要平台托管的智能体运行时** → 选择托管智能体 API。适合需要沙箱执行、多工具编排、会话生命周期管理的复杂 Agent 应用。
4. **组合使用**：三者并非互斥。例如可用托管智能体 API 编排复杂工作流，其底层模型调用仍走 Qwen API；或在语音助手前端使用全双工实时 API，后端通过托管智能体执行复杂任务。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [managed agents api](../api/managed-agents-api.md)


