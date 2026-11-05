# agent context

`agent context` 是百炼平台中用于增强 Agent 推理能力的上下文注入机制，支持将外部知识、历史记忆、结构化数据源等动态注入到 LLM 的 [prompt](prompt.md) 中。它不依赖模型微调，而是通过运行时上下文拼接实现领域适配与状态感知，是构建生产级 Agent 的核心基础设施之一。其设计与 [RAG](raw/application-user-guide/knowledge-base.md)、[Memory](raw/application-user-guide/agent-context/memory-library-overview.md) 和 [Connector](raw/application-user-guide/agent-context/overview.md) 深度协同。

## 支持的模型与功能

- **模型兼容性**：当前仅支持百炼托管的 `qwen-max`、`qwen-plus` 及 `qwen-turbo`（v20240815+）；开源模型（如本地部署的 Qwen2-7B）暂不支持自动 context 注入，需手动拼接。
- **上下文类型**：
  - 知识库检索结果（对接 RAG pipeline）
  - [长期记忆](../concepts/long-term-memory.md)（基于 Memory Library 的会话级/用户级记忆）
  - 外部系统数据（通过 Connector 同步的数据库、API 或文件内容）
  - 结构化输入（ParseX 解析后的 JSON 表单、表格或日志片段）

> **注意**：文档 [ParseX](raw/application-user-guide/agent-context/getting-started-overview.md) 中提及“支持任意文本格式解析”，但实际仅支持 JSON Schema 明确声明的字段；未声明字段将被静默丢弃，该限制未在原文中说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context_sources` | array | 是 | 指定上下文来源列表，元素为 `{ "type": "knowledge_base", "id": "kb-xxx" }` 等格式，详见 [Connector](raw/application-user-guide/agent-context/overview.md) 定义 |
| `context_max_tokens` | integer | 否 | 总上下文 token 上限（含 [prompt](prompt.md)），默认 4096，超出部分按 LRU 截断 |
| `memory_enabled` | boolean | 否 | 是否启用 Memory Library 自动注入，默认 `true`；设为 `false` 时需显式传入 `memory_history` |

## 使用方式

1. 在 Agent 配置 YAML 中声明 `context_sources`：
   ```yaml
   context_sources:
     - type: knowledge_base
       id: kb-12345
     - type: memory
       scope: user
   ```
2. 调用 SDK 时传入 runtime context（如用户 ID、会话 ID），触发 Memory 和 Connector 动态加载；
3. 系统自动完成 RAG 检索、Memory 查询、Connector 数据拉取，并按优先级合并去重后注入 [prompt](prompt.md) —— 全过程对模型透明，无需修改提示词模板。

## 限制和注意事项

- 单次请求最多支持 5 个 `context_sources`，超过将报错 `CONTEXT_SOURCE_LIMIT_EXCEEDED`；
- Knowledge Base 源仅支持已发布（Published）状态的知识库，草稿库不可用；
- Memory 注入默认仅包含最近 10 轮交互（可配置 `memory_window_size`），但 [Memory](raw/application-user-guide/agent-context/memory-library-overview.md) 文档未明确说明该默认值；
- 所有 context 内容在注入前经敏感词过滤与长度归一化处理，原始格式可能丢失（如 Markdown 表格转为纯文本）；
- 不支持跨 workspace 的 context source 引用（例如 workspace A 的 knowledge_base 无法在 workspace B 的 Agent 中直接引用）。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


