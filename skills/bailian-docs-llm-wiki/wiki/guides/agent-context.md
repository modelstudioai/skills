# agent context

`agent context` 是百炼平台中用于为 Agent 提供运行时上下文信息的核心机制，它决定了 Agent 在执行任务时可访问的知识、历史记忆、外部数据源及结构化解析能力。该机制通过统一的上下文注入框架，将 RAG 检索结果、[长期记忆](../concepts/long-term-memory.md)、Connector 接入的实时数据以及 ParseX 解析的文档内容动态组装为模型输入。其设计目标是提升 Agent 的事实准确性、状态一致性与多步推理能力。

## 支持的模型与功能

当前 `agent context` 机制完整支持所有百炼平台上的 **Agent-optimized 模型**（如 qwen-agent-7b、qwen-agent-72b），以及部分通用大模型（如 qwen-max、qwen-plus）在启用 `enable_agent_context: true` 时的上下文增强模式。核心功能包括：
- RAG 检索结果自动注入（基于 [知识库](../../raw/application-user-guide/knowledge-base.md) 配置）；
- Memory 库中的对话历史与用户画像自动关联（详见 [memory-library-overview.md](../../raw/application-user-guide/agent-context/memory-library-overview.md)）；
- Connector 接入的第三方系统数据（如 CRM、数据库）按需加载；
- ParseX 解析后的结构化文档内容（PDF/Word/Excel 等）作为上下文片段嵌入（参见 [getting-started-overview.md](../../raw/application-user-guide/agent-context/getting-started-overview.md)）。

> **注意**：qwen-turbo 和 qwen-1.5 系列模型**不支持** `agent context`，调用时将静默忽略上下文字段；此行为与 [overview.md](../../raw/application-user-guide/agent-context/overview.md) 中“所有模型默认兼容”的旧描述矛盾，以本说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context_sources` | array | 否 | 指定启用的上下文类型，取值为 `["rag", "memory", "connector", "parsex"]`；未声明则默认启用全部（但受模型能力限制） |
| `context_max_tokens` | integer | 否 | 上下文总 token 上限，默认 4096；超出部分按 LRU 策略截断 |
| `memory_filter` | object | 否 | 用于过滤 memory 条目的条件对象，例如 `{ "user_id": "u123", "tag": "support" }` |

## 使用方式

1. 在 Agent 配置 YAML 或 API 请求体中显式声明 `context` 字段：
   ```yaml
   context:
     context_sources: ["rag", "memory"]
     context_max_tokens: 3072
   ```
2. 确保对应功能模块已启用并完成配置：RAG 需绑定知识库、Memory 需初始化库、Connector 需完成认证与 schema 映射、ParseX 需上传并解析文档；
3. 发起 `/v1/agents/{id}/run` 调用，平台自动合成上下文并注入模型 [prompt](prompt.md) 头部。

## 限制和注意事项

- 单次请求中 `context_sources` 最多指定 3 种类型，避免上下文膨胀导致推理延迟激增；
- RAG 与 ParseX 内容若存在语义重叠，系统**不自动去重**，需业务层预处理（[overview.md](../../raw/application-user-guide/agent-context/overview.md) 未说明此风险）；
- Memory 数据仅支持最近 100 条交互记录（按时间倒序），更早条目需通过 `memory_filter` 主动查询；
- 所有上下文内容在模型输入前经 Base64 编码与安全扫描，含敏感词或非法格式的片段将被整块丢弃且**不报错**。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


