# memory library overview

记忆库是百炼平台提供的长期[记忆管理](../concepts/memory.md)能力，用于在多轮对话中持久化存储和检索用户或应用相关的上下文信息。它支持结构化与非结构化数据的混合存储，并通过向量检索与关键词匹配双路召回提升检索精度。该能力已集成至百炼 SDK、API 及低代码工作流中，适用于客服助手、个性化推荐等需状态保持的场景。

## 支持的模型/功能

- 当前仅支持接入 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大模型（详见 [记忆库](../../raw/application-user-guide/memory-library-overview.md)）；其他模型调用 memory library 将返回 `400 UnsupportedModel` 错误。  
- 提供两类核心功能：**长期记忆写入（upsert）** 与 **语义检索（search）**，不支持原地更新或批量删除（删除需按 ID 逐条调用）。  
- 支持自动摘要生成（`enable_auto_summary: true`），但仅对单次写入文本长度 ≥ 512 字符生效，且摘要结果不可编辑——该行为与 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview.md) 中描述一致。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_id` | string | 否 | 用户自定义唯一标识，若为空则由系统生成 UUIDv4 |
| `content` | string | 是 | 原始文本内容，最大长度 8192 字符 |
| `metadata` | object | 否 | 键值对形式的结构化标签（如 `{"user_id": "u123", "session_id": "s456"}`），用于过滤检索 |
| `embedding_model` | string | 否 | 指定嵌入模型，默认 `text-embedding-v2`；注意该参数在 [长期记忆 API](../../raw/application-user-guide/memory-library-overview.md) 文档中已被标记为 deprecated，后续版本将强制使用平台统一向量模型 |

> **注意**：`embedding_model` 参数虽仍可传入，但实际 embedding 计算已忽略该字段，统一使用 `text-embedding-v3`。请勿依赖旧文档中关于该参数的说明逻辑。

## 使用方式

1. **SDK 调用（推荐）**：使用 `@alibaba/bailian-sdk@latest`，通过 `memory.upsert()` / `memory.search()` 方法操作；  
2. **HTTP API**：向 `POST /v1/memories` 或 `POST /v1/memories/search` 发送 JSON 请求，需携带 `Authorization: Bearer <token>`；  
3. **低代码集成**：在「记忆节点」中配置写入/检索动作，支持拖拽绑定变量（参见 [记忆库](../../raw/application-user-guide/memory-library-overview.md) 的可视化配置章节）。

## 限制和注意事项

- 单账户默认配额：10 万条记忆条目，单条 `content` ≤ 8192 字符，`metadata` 总键值对数 ≤ 10；  
- 检索结果默认最多返回 10 条，`top_k` 参数上限为 50；  
- 写入后数据约 2–5 秒内可被检索到（最终一致性），高并发写入时可能出现短暂延迟；  
- 不支持跨 workspace 共享记忆库，每个 workspace 独立隔离。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview.md)


