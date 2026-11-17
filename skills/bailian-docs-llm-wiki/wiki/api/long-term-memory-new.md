# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话保存和检索用户偏好、行为特征、历史交互等关键上下文。它通过分片（Fragment）机制实现细粒度控制，并支持基于语义与属性的混合检索。该功能需在应用配置中显式启用，且仅对兼容模型生效。

## 支持的模型/功能

当前仅以下模型支持[长期记忆](../concepts/long-term-memory.md)的完整读写能力：`qwen-max-20240919`、`qwen-plus-20240919` 及后续标注 `ltm_enabled: true` 的模型版本。基础模型（如 `qwen-turbo`）仅支持只读访问（即 `get_memory`），不支持自动更新或 `upsert_fragment`。所有支持模型均需配合 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中定义的接口调用，具体能力边界请参见 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档。

## 关键参数

- `memory_id`: 必填，全局唯一标识符，通常由用户 ID 或业务主键生成（建议使用 UUIDv4 或哈希值）  
- `fragments`: 可选数组，每个 fragment 包含 `type`（如 `"preference"`、`"order_history"`）、`content`（JSON 对象）、`ttl_seconds`（默认 30 天）  
- `enable_auto_update`: 布尔值，默认 `false`；设为 `true` 后，模型可在响应中隐式调用 `upsert_fragment`（仅限支持模型）  
- `retrieval_strategy`: 可选 `"semantic"`、`"attribute"` 或 `"hybrid"`，影响 `get_memory` 的召回逻辑  

> **注意**：`ttl_seconds` 在 [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 中声明最小值为 3600 秒，但实际 API 接收 0 表示“永不过期”，此行为与文档描述不一致，请以 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的 runtime 行为为准。

## 使用方式

1. 在应用配置页开启「[长期记忆](../concepts/long-term-memory.md)」开关，并选择目标模型  
2. 调用 `/v1/memory/upsert` 写入结构化片段（参考 [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)）  
3. 在对话请求 `messages` 中添加 `memory_id` 字段，平台将自动注入匹配 fragment 到系统提示词  
4. 如需主动查询，调用 `/v1/memory/get` 并指定 `memory_id` 和 `retrieval_strategy`  

## 限制和注意事项

- 单个 `memory_id` 下最多存储 100 个 fragment，总内容大小不超过 2MB  
- 自动更新（`enable_auto_update: true`）仅在模型输出中包含特定 `<ltm>` 标签时触发，格式详见 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)  
- 用户画像（Profile）功能独立于 fragment 存储，需通过 `/v1/profiles/*` 接口单独管理，其字段 schema 由 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 定义，不可混用  
- 所有写操作均为最终一致性，读取可能存在秒级延迟

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


