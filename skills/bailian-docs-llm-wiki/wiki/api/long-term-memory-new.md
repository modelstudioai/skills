# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆存储与检索能力，支持在多轮对话中持久化保存和动态调用用户事实性信息、行为偏好及画像特征。该能力通过 API 显式控制，不依赖模型自身隐式记忆，确保可审计、可更新、可隔离。详细设计目标与架构说明见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)。

## 支持的模型/功能

- **模型兼容性**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生支持 LTM 上下文注入；其他模型调用时将忽略 `memory_id` 参数，不报错但无实际效果。  
- **核心功能模块**：  
  - **事实记忆（Fragments）**：以键值对形式存储短生命周期、高精度的事实（如“用户手机号为138****1234”），支持按 key 精确检索与批量更新；详见 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)。  
  - **用户画像（Profiles）**：结构化存储跨会话的长期属性（如“偏好语言=英语”“行业=金融”），支持字段级版本控制与条件查询；详见 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)。  

> **注意**：文档 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 中提及的 `llama-3-70b` 支持声明已过时，实测该模型无法解析 `memory_id` 字段，应以当前 SDK 文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_id` | string | 是 | 记忆实例唯一标识符，由应用侧生成并维护，长度 1–64 字符，仅支持字母、数字、`-`、`_` |
| `memory_type` | string | 否 | 取值 `fragment` 或 `profile`，未指定时默认为 `fragment`；类型决定后续读写行为 |
| `ttl_seconds` | integer | 否 | 仅对 `fragment` 有效，过期时间（秒），范围 300–2592000（5 分钟–30 天），默认 86400（24 小时） |

## 使用方式

1. **初始化记忆实例**：调用 `/v1/memories` 创建 `memory_id`（需携带 `app_id` 认证）；  
2. **写入数据**：向 `/v1/memories/{memory_id}/fragments` 或 `/v1/memories/{memory_id}/profiles` 发送 POST 请求，body 为 JSON 对象；  
3. **在推理中启用**：在 `/v1/chat/completions` 请求中，于 `messages` 外层传入 `"memory_id": "xxx"` 字段（非 message 内容中）；模型将自动注入关联的 fragment + profile 数据作为系统上下文。  
完整流程与示例代码参见 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项

- 单个 `memory_id` 下最多存储 1000 条 fragment 或 100 条 profile；超出后写入失败并返回 `400 Bad Request`；  
- `memory_id` 不具备租户隔离能力：不同 `app_id` 若使用相同 `memory_id`，将共享同一份记忆数据（此行为已在 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 中明确标注，但易被忽略）；  
- 所有 memory 数据默认加密落盘，但**不支持字段级权限控制**，敏感字段（如身份证号）需应用层脱敏后再写入；  
- 删除 `memory_id` 后，其关联的所有 fragment/profile 立即不可访问，且**不可恢复**——该强一致性语义与 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 中“软删除”的旧版描述存在冲突，以当前 API 行为为准。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


