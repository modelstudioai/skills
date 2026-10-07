# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的一套轻量、安全、可扩展的标准化接口协议，用于在大模型推理过程中**按需、动态、结构化地注入外部上下文数据**（如知识库检索结果、用户画像、实时API响应、会话状态等），从而增强模型对当前任务的理解深度与生成准确性。MCP 不修改模型权重或提示工程逻辑，而是通过模型与外部服务间的显式协商机制，在 [prompt](../guides/prompt.md) 构造阶段完成上下文的安全拼接。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 场景**：当调用知识库问答服务时，MCP 可替代传统硬编码的 context 拼接方式。开发者只需在 `messages` 中声明 `{context: kb-search}` 占位符，MCP 服务将自动触发知识库检索，并按预定义 JSON Schema 返回结构化切片，精准注入到指定位置，避免冗余文本污染 [prompt](../guides/prompt.md)。
  
- **智能体（Agent）应用**：在 Agent 编排中，MCP 是连接“规划”与“执行”的关键桥梁。例如，当模型识别出需查询用户历史订单时，可协商调用 `user-profile` 或 `order-history` MCP 服务，而非依赖插件（tool call）进行异步动作——MCP 注入的是**同步、确定性、只读的上下文信息**，适用于决策前的信息补全。

- **插件协同场景**：MCP 与插件能力正交互补。插件用于**主动执行动作**（如调用计算器、生成图片），而 MCP 用于**被动提供背景信息**（如“当前用户所在城市为杭州”，供插件参数生成参考）。二者可共存于同一请求中：MCP 提供上下文 → 模型基于上下文规划 → 插件执行动作。

- **自定义服务集成**：开发者可通过实现符合 MCP 规范的 HTTP 服务（需支持 `/schema` 和 `/invoke` 接口），将任意业务系统（CRM、ERP、监控告警）接入模型上下文流。该服务经平台注册后，即可被 `mcp_services` 白名单引用，无需修改模型调用代码。

- **控制台 Playground 调试**：在 RAG 或智能体 Playground 中启用 MCP 后，系统自动高亮显示注入的上下文块，并在响应元数据中返回 `mcp_context_used` 字段，便于快速验证上下文是否命中、内容是否合规。

## 关键参数和配置

启用 MCP 需在 `/v1/chat/completions` 请求体中显式配置以下参数（均位于顶层，非嵌套在 `messages` 或 `tools` 内）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `mcp_enabled` | boolean | 是 | 设为 `true` 才启动上下文协商流程；设为 `false` 或省略则完全跳过 MCP。 |
| `mcp_services` | string[] | 否 | 允许调用的 MCP 服务 ID 列表，如 `["kb-search", "user-profile"]`；为空时使用平台默认服务集（含基础知识库服务）。**强烈推荐显式声明白名单，避免意外调用。** |
| `mcp_timeout_ms` | integer | 否 | 单个 MCP 服务调用超时毫秒数，默认 `3000`，范围 `100–10000`；超时后该服务被跳过，不影响其他服务及主推理。 |

> ✅ **占位符语法**：在 `messages.content` 中使用 `{context: <service_id>}` 格式（如 `"请结合{context: kb-search}回答"`），MCP 服务返回的 JSON 对象将被序列化后原样插入此处。多个相同 service_id 占位符共享一次调用结果。

## 面向开发者，简洁实用

- **仅限特定模型**：当前仅 `qwen-max`、`qwen-plus`、`qwen-turbo`（v2024.06+）支持 MCP；调用前请确认模型版本，`qwen-vl-plus` 等多模态模型暂不支持。
- **严格长度限制**：所有注入上下文总长（JSON 序列化后）≤ 8192 字符，超长部分静默截断并记录警告日志。
- **强约束调用频次**：单次请求最多触发 **3 个独立 MCP 服务调用**，超出者被静默忽略。
- **非流式前提**：MCP 所有注入操作在首 token 生成前完成，**不支持 `stream: true` 场景下的动态上下文注入**。
- **安全责任边界**：平台不代理敏感字段过滤或鉴权。自定义 MCP 服务必须自行完成身份校验、数据脱敏与权限控制。
- **调试必查字段**：响应中 `mcp_context_used` 数组明确列出本次实际注入的服务 ID、返回字段数及耗时，是排查上下文缺失的第一依据。

> 💡 提示：首次集成建议从官方 `kb-search` 服务入手，在 Playground 中开启 MCP 并观察占位符替换效果；再逐步接入自定义服务。详细错误码与链路追踪请参考 [MCP 外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 文档。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [knowledge base](../guides/knowledge-base.md)
- [plug in](../guides/plug-in.md)
- [rag api](../api/rag-api.md)
- [application support](../guides/application-support.md)


