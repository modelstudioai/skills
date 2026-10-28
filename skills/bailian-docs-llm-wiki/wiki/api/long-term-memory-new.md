# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理能力，用于在多轮对话中持久化存储和检索用户事实性信息、行为偏好与画像特征。它通过语义索引与向量检索实现低延迟、高相关性的记忆召回，支持开发者构建具备上下文连续性的智能应用。该能力需配合兼容模型调用，并依赖显式配置的 memory 参数启用。

## 支持的模型/功能

当前仅以下模型支持[长期记忆](../concepts/long-term-memory.md)功能：`qwen-max-20241017`、`qwen-plus-20241017` 及后续标注 `ltm_enabled: true` 的模型版本。不支持旧版 `qwen-turbo` 或 `qwen-plus-20240618` 等未启用 LTM 的模型。功能上分为三类：**事实记忆**（存储可验证的客观事实，如“用户生日是1992年5月3日”）、**用户画像**（聚合抽象标签与统计特征，如“偏好技术类内容”）、以及**通用记忆片段**（非结构化文本块，适用于临时上下文锚点）。详情见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 文档中的分类说明。

## 关键参数

调用时需在 `messages` 中的 system 或 user 消息内嵌 `memory` 字段（JSON 对象），结构如下：
```json
{
  "type": "fact" | "profile" | "generic",
  "id": "string", // 必填，全局唯一标识符
  "content": "string", // 必填，记忆内容正文
  "metadata": { ... } // 可选，支持自定义键值对（如 source: "user_input", timestamp: 1730000000）
}
```
`type` 决定存储策略与检索权重；`id` 重复提交将触发覆盖更新；`metadata` 中的 `ttl_seconds`（整数）可指定自动过期时间（最小 3600 秒），超时后记忆不可检索。参见 [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 中的字段约束说明。

## 使用方式

1. **写入记忆**：在任意请求的 `messages` 数组中插入一条含 `memory` 字段的 message（推荐放在首条 system message 或最新 user message 中）；  
2. **读取记忆**：无需显式查询，模型在生成响应前会自动检索匹配的[长期记忆](../concepts/long-term-memory.md)并注入上下文；  
3. **删除记忆**：发送 `memory` 类型为 `"delete"` 的消息，携带待删 `id` 即可（详见 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 文档的清理机制）。  
> **注意**：`memory` 字段**不可**置于 assistant 消息中，且单次请求最多携带 5 条记忆记录（含写入与删除），超出部分将被静默截断。

## 限制和注意事项

- 单个应用实例的长期记忆总容量上限为 100 万条记录，每条 `content` 长度不得超过 2048 字符；  
- 记忆检索基于向量相似度，对精确关键词匹配（如身份证号、手机号）效果有限，敏感信息须自行脱敏后再写入；  
- 同一 `id` 的多次写入以最后一次为准，但历史版本**不可回溯**；  
- 当前不支持跨应用共享记忆，各应用 memory 空间完全隔离。  
> **注意**：原始文档 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 中提及的“支持 profile 自动聚类”功能尚未上线，实际行为仍需显式传入 `type: "profile"` 并指定 `metadata` 标签，此为文档过时描述。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


