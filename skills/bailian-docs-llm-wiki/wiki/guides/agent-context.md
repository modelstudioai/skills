# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入能力的核心机制，它决定了 Agent 能够感知和利用哪些上下文数据（如历史对话、知识库、外部系统连接等）。该机制通过声明式配置实现，开发者可灵活组合多种上下文源以增强 Agent 的推理与执行能力。其设计遵循“按需注入、隔离可控”原则，避免上下文污染与冗余加载。

## 支持的模型/功能

agent context 本身不依赖特定大模型，但需模型具备多轮上下文理解能力（如 Qwen 系列、Baichuan2、GLM 等主流开源/闭源模型均支持）。当前支持的上下文类型包括：
- **知识库（RAG）**：对接向量数据库，支持实时检索增强 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中描述的 `knowledge-base` 模块；
- **记忆（Memory）**：提供会话级与用户级[长期记忆](../concepts/long-term-memory.md)管理，详见 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档；
- **Connector**：允许接入外部 API、数据库或 SaaS 服务，其元数据注册与调用逻辑由 [Connector](../../raw/application-user-guide/agent-context/overview.md) 定义；
- **ParseX**：结构化文档解析能力，用于将 PDF/Word/Excel 等文件转换为可检索文本片段，属于上下文预处理环节，参见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)。

> **注意**：部分旧版 SDK 示例中将 ParseX 视为独立 context 类型，但自 v3.2.0 起，ParseX 已统一归入 `preprocessor` 阶段，不再作为 runtime context 直接挂载——请以 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 最新说明为准。

## 关键参数

在 `AgentConfig.context` 字段中配置，支持以下关键子字段：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_base_ids` | `string[]` | 否 | 关联的知识库 ID 列表；空数组表示禁用 RAG |
| `memory_config` | `object` | 否 | 启用 memory 时的配置对象，含 `scope`（`session`/`user`）、`ttl_seconds` 等字段 |
| `connector_ids` | `string[]` | 否 | 已注册的 connector ID 列表，运行时自动注入认证与 schema 信息 |
| `preprocessors` | `object[]` | 否 | 当前仅支持 `{"type": "parsex", "config": {...}}`，用于上传文件的预处理 |

## 使用方式

1. 在创建或更新 Agent 时，于 `context` 字段中声明所需上下文源（示例见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)）；
2. 若启用 Memory，需确保已调用 `/v1/memory/init` 初始化对应 scope 的存储空间；
3. Connector 调用无需显式编码，Agent 执行过程中根据 tool call 自动触发，前提是 `connector_ids` 已正确配置且权限就绪；
4. ParseX 预处理仅在 `input_files` 非空时生效，且要求文件 MIME 类型在白名单内（PDF/DOCX/XLSX/TXT）。

## 限制和注意事项

- 单次请求总 context token 数（含 RAG 片段 + memory 记录 + connector 返回摘要）不得超过模型最大上下文长度的 80%，否则触发截断并返回警告日志；
- Knowledge base 检索结果默认最多返回 5 个 chunk，不可通过 context 配置调整，需改用 `retrieval_config` 单独设置；
- Memory 数据默认加密落盘，但 `scope: user` 下的数据跨租户隔离，不支持跨 workspace 共享；
- Connector 调用超时固定为 15 秒，不可覆盖；若需更长等待，请在 connector 实现侧异步化并轮询状态。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


