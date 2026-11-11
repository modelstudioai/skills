# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入的关键机制，它决定了 Agent 在执行任务过程中可感知的知识范围、历史交互记忆及可访问的外部数据源。通过合理配置上下文，开发者可显著提升 Agent 的准确性、连贯性与领域适应性。其核心由知识库（RAG）、记忆（Memory）和连接器（Connector）三类组件协同构成。

## 支持的模型与功能

- 所有支持 `agent` 类型调用的模型（如 `qwen-plus`、`qwen-max`、`qwen2.5-72b` 等）均原生兼容 agent context 机制；  
- 功能上覆盖：基于知识库的实时检索增强（RAG）、多轮对话状态维护（Memory）、第三方系统/数据库/API 的安全接入（Connector），以及结构化文档解析能力（ParseX）；  
- 各功能模块可独立启用或组合使用，具体能力边界详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 关键参数

在创建或更新 Agent 时，需通过 `context` 字段显式声明上下文配置，主要参数包括：

| 参数 | 类型 | 说明 |
|------|------|------|
| `knowledge_base_ids` | string[] | 指定关联的知识库 ID 列表，用于 RAG 检索；支持最多 5 个知识库同时生效 |
| `memory_config.enabled` | boolean | 是否启用对话记忆；若为 `true`，需配合 `memory_config.ttl_seconds`（默认 3600）控制生命周期 |
| `connectors` | object[] | 定义 Connector 配置数组，每个对象含 `id`、`auth_type` 和 `config` 字段；详情见 [Connector](../../raw/application-user-guide/agent-context/overview.md) |
| `parsex_enabled` | boolean | 是否启用 ParseX 文档解析（仅对上传文件类输入生效）；该参数在 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 中有完整说明 |

> **注意**：`memory_config.ttl_seconds` 最大值为 86400（24 小时），但部分旧版 SDK 示例中误标为 172800，应以 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档为准。

## 使用方式

1. **API 调用**：在 `POST /v1/agents/{agent_id}/invoke` 请求体中，将上下文配置嵌入 `input.context` 字段（非顶层 `context`）；  
2. **控制台配置**：在 Agent 编辑页的「上下文」标签页中，可视化勾选知识库、开启记忆、添加 Connector 并保存；  
3. **动态覆盖**：每次调用均可传入临时 `context`，优先级高于 Agent 全局配置，适用于多租户场景下的上下文隔离。

## 限制和注意事项

- 单次 RAG 检索最大返回 chunk 数为 10，总 token 上限约 4096（受模型 context window 限制）；  
- Memory 仅保留当前 session 内的用户与 Agent 交互历史，不跨 session 共享；  
- Connector 的认证凭据（如 API Key）必须通过百炼密钥管理服务注入，禁止硬编码；  
- 当同时启用 RAG 与 ParseX 且输入含文件时，ParseX 解析结果会作为额外上下文参与 RAG 检索——该行为已在 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md) 文档中明确说明，但未在早期版本的 overview 中体现，需特别留意。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


