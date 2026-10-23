# agent context

agent context 是百炼平台中用于管理 Agent 运行时环境信息的核心机制，它决定了 Agent 能够感知和利用的外部知识、历史交互与数据源。该机制通过结构化上下文注入，支持动态增强 LLM 的推理能力，适用于 RAG、记忆回溯、多步骤工具调用等场景。其设计兼顾灵活性与可控性，开发者可通过参数精细调控上下文构成与生命周期。

## 支持的模型/功能

- 当前仅 [Qwen-Max](../../raw/application-user-guide/agent-context.md)、[Qwen-Plus](../../raw/application-user-guide/agent-context.md) 和 [Qwen2.5-72B](../../raw/application-user-guide/agent-context.md) 等部分大模型支持完整的 agent context 注入能力；其他模型（如 Qwen1.5 系列）仅支持基础 [prompt](prompt.md) 上下文拼接，不支持 memory 或 connector 的自动解析。
- 支持三大上下文来源：RAG 检索结果（来自知识库）、Memory（会话级或用户级历史摘要）、Connector（实时接入的数据库/API 数据）。ParseX 作为可选预处理模块，用于结构化非文本输入（如 PDF 表格、JSON Schema），详见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `context_type` | string | `"auto"` | 可选 `"auto"`（平台自动选择最优组合）、`"rag"`、`"memory"`、`"connector"` 或数组形式如 `["rag", "memory"]` |
| `context_ttl` | integer | `3600` | 上下文缓存有效期（秒），仅对 memory 和 connector 生效；RAG 结果不缓存，每次请求重新检索 |
| `max_context_length` | integer | `4096` | 最大注入 token 数（含系统提示），超出部分按优先级截断（RAG > memory > connector） |

> **注意**：`context_ttl` 在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中标注为“单位为毫秒”，但实际 API 接收秒级整数——请以 SDK 示例和 OpenAPI 规范为准，该处为文档过时描述。

## 使用方式

1. 在创建 Agent 时，于 `configuration.context` 字段中声明配置对象；
2. 若启用 RAG，需预先绑定知识库 ID；若启用 Memory，需指定 `memory_id` 或启用自动会话记忆；
3. Connector 需在平台控制台完成数据源授权与 schema 映射，其上下文内容由运行时 query 动态生成；
4. ParseX 处理需显式设置 `parsex_enabled: true` 并提供原始二进制或 base64 编码内容，参考 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 快速入门。

## 限制和注意事项

- 单次请求中，RAG 检索结果最多返回 10 个 chunk，且每个 chunk 原始长度不可超过 2048 token；
- Memory 上下文仅保留最近 50 轮对话摘要（经 LLM 压缩），不保留原始 message list；
- Connector 查询受速率限制（默认 5 QPS/Agent），超限请求将被拒绝并返回 `429 Too Many Requests`；
- 所有上下文内容在进入 LLM 前均经过敏感词过滤与脱敏处理，开发者需确保原始数据已符合合规要求——详见 [Connector](../../raw/application-user-guide/agent-context/overview.md) 安全说明。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


