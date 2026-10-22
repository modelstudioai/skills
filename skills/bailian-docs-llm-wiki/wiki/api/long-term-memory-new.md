# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理能力，支持在多轮对话中持久化存储和检索用户事实性信息与画像特征。该能力通过独立的 API 接口与推理请求解耦，允许开发者显式控制记忆的写入、查询与更新。其设计目标是提升对话一致性与个性化水平，同时保障数据隔离与可控性。

## 支持的模型/功能

- 当前仅对 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类模型开放[长期记忆](../concepts/long-term-memory.md)调用权限；其他模型调用将被静默忽略（参见 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- 支持两类核心记忆类型：**事实记忆**（如“用户住在杭州”“上月订购了咖啡机”）和**用户画像**（如“偏好技术类内容”“常用语言为中文”），二者在存储结构、检索策略与 TTL 策略上相互独立。
- 所有记忆操作均需通过 `/v1/memory` 系列接口完成，不支持在 `/v1/chat/completions` 请求体中直接嵌入记忆字段（详见 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md)）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_type` | string | 是 | 取值为 `"fact"` 或 `"profile"`，不可混用 |
| `ttl_seconds` | integer | 否 | 有效期（秒），`fact` 默认 2592000（30 天），`profile` 默认 31536000（1 年）；设为 `0` 表示永不过期（但受平台总容量配额约束） |
| `metadata` | object | 否 | 键值对，仅支持字符串值，最大 10 对；用于辅助过滤，不参与语义检索 |

> **注意**：原始文档 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 中提到 `ttl_seconds` 可设为 `-1` 表示永不过期，但该值已在 v2.3.0 版本后废弃，实际行为等同于 `0`；请以 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 中定义为准。

## 使用方式

1. **写入记忆**：调用 `POST /v1/memory/write`，指定 `memory_type`、`content`（纯文本，≤2048 字符）、`user_id`（必填，用于隔离）及可选 `ttl_seconds` 和 `metadata`；
2. **查询记忆**：调用 `POST /v1/memory/query`，传入 `user_id` 与 `query_text`（自然语言问题，如“用户最近一次订单是什么？”），系统返回相关度排序的 top-5 记忆片段；
3. **删除记忆**：调用 `DELETE /v1/memory/clear`，支持按 `user_id` + `memory_type` 组合批量清除，不支持按单条 ID 删除。

所有接口均需携带 `Authorization: Bearer <api_key>`，且 `user_id` 必须与调用方应用绑定的租户 ID 具备归属关系。

## 限制和注意事项

- 单 `user_id` 下，`fact` 类型记忆总量上限为 1000 条，`profile` 类型上限为 100 条；超出后写入失败并返回 `400 Bad Request`；
- 记忆内容不参与模型训练，且不会出现在任何日志或审计导出中（符合 GDPR/PIPL 要求），但需开发者自行确保写入内容已脱敏；
- 查询时若 `query_text` 语义模糊（如仅含“你好”），系统将返回空结果集而非默认 fallback —— 此行为与 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 文档描述一致，但与旧版文档存在差异，请勿依赖隐式兜底逻辑。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


