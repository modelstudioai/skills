# long term memory new

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化记忆存储与检索能力，支持在多轮对话中持久化保存用户事实性信息、行为偏好和画像特征。该能力通过独立的 API 接口与推理服务解耦，可按需启用或关闭。其设计目标是提升对话一致性与个性化水平，同时保障数据隔离与可控性。

## 支持的模型/功能

- 当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款模型原生支持长期记忆上下文注入（需显式开启 `enable_long_term_memory: true`）；其他模型调用时将忽略该字段。
- 功能分为两类：**事实记忆**（Fact Memory）用于存储结构化实体关系（如“用户居住地为杭州”），支持语义检索与版本管理；**用户画像**（Profile）用于聚合非结构化偏好标签（如“偏好技术类内容”），支持动态更新与权重衰减。
- 所有功能均基于 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 定义的 REST 接口实现，不依赖模型内部参数微调。

## 关键参数

- `enable_long_term_memory`: 布尔值，必须设为 `true` 才启用记忆注入（默认 `false`）。
- `memory_source`: 字符串，指定来源类型，可选 `"fact"` 或 `"profile"`；混合使用需分两次请求。
- `max_memory_items`: 整数，单次请求最多注入 20 条记忆片段（超过部分被截断），详见 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档说明。
- `ttl_seconds`: 可选，记忆有效期（秒），`fact` 类型默认 30 天，`profile` 类型默认 7 天；设为 `0` 表示永不过期（不推荐生产环境使用）。

## 使用方式

1. 首先通过 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 或 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 对应的写入接口（如 `POST /v1/memory/facts`）存入数据；
2. 在调用 `/v1/chat/completions` 时，在 `messages` 上层传入 `long_term_memory` 对象，并设置上述关键参数；
3. 平台自动在 prompt 中注入匹配的记忆片段（按相关性 Top-K 截取），不改变原始模型输入格式。

> **注意**：文档中提及的 `memory_strategy: "auto"` 参数已在 v2.3.0 版本移除，当前仅支持显式指定 `memory_source`；旧版 SDK 示例代码若含此字段将导致 400 错误，请同步更新至最新 SDK。

## 限制和注意事项

- 单个应用（app_id）下所有用户的记忆数据物理隔离，但**不支持跨应用共享记忆**；
- 记忆检索基于向量相似度 + 规则过滤（如时间衰减、权限标签），不保证 100% 召回，高精度场景建议结合业务 ID 显式查询；
- 每个 `fact` 片段最大长度为 512 字符，超长内容会被截断——该限制在 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 中未明确说明，实际以 API 返回 `400` 错误为准；
- 用户删除自身账户后，关联记忆不会自动清除，需调用 `/v1/memory/clear` 主动清理。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


