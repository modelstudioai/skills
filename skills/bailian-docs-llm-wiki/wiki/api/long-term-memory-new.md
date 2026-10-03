# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理能力，支持在多轮对话中持久化存储和检索用户事实性信息、行为偏好与画像特征。该能力通过独立的 API 接口与推理请求解耦，允许开发者按需写入、查询和更新记忆片段。其设计目标是提升大模型应用在个性化、上下文连续性和状态一致性方面的工程可控性。

## 支持的模型与功能

- 当前仅对 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型开放[长期记忆](../concepts/memory.md)能力（需在请求中显式启用）；其他模型调用时将忽略 `memory` 相关参数。
- 支持两类核心记忆类型：**事实记忆**（facts，如“用户姓张”“常住北京”）和**用户画像**（profiles，如“偏好科技新闻”“阅读水平为高级”），二者语义分离、存储隔离、检索独立。
- 记忆写入与检索不依赖于模型内部 token 位置，因此不受上下文窗口限制，详见 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

- `memory.write`: 布尔值，设为 `true` 时触发本次请求结果自动提取并写入记忆（需配合 `memory.rules` 定义提取逻辑）。
- `memory.rules`: JSON 数组，每项指定字段名、来源路径（如 `response.content`）、类型（`fact` 或 `profile`）及可选的归一化规则（如 `"value": "lowercase"`）。
- `memory.query`: 对象，支持 `facts` 和 `profiles` 两个子字段，各为字符串数组（如 `["user_name", "location"]`），用于声明本轮请求需注入的记忆键；具体匹配策略参见 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md)。

> **注意**：`memory.rules` 中若指定 `type: "profile"`，但对应字段值为纯数字或空字符串，系统将静默跳过写入——此行为与 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 文档中描述的“空值强制转为 null 并保留条目”存在不一致，建议以实际 API 返回 `201 Created` 且 `memory_id` 非空为准。

## 使用方式

1. 在 `/v1/chat/completions` 请求体中添加 `memory` 对象；
2. 若需写入，设置 `memory.write: true` 并配置 `memory.rules`；
3. 若需读取，设置 `memory.query.facts` 或 `memory.query.profiles`；
4. 所有记忆操作均基于 `user_id`（必传 header `x-bailian-user-id`）进行隔离，跨用户不可见。

示例片段（精简）：
```json
{
  "model": "qwen-plus",
  "messages": [...],
  "memory": {
    "write": true,
    "rules": [{"field": "name", "source": "response.content.name", "type": "fact"}],
    "query": {"facts": ["location"]}
  }
}
```

## 限制和注意事项

- 单个 `user_id` 下，事实记忆总量上限为 500 条，用户画像上限为 100 条；超出后写入失败并返回 `400 Bad Request`。
- 记忆内容不参与模型训练，且默认 TTL 为 90 天（可配置），过期后自动清理。
- 写入时若 `memory.rules` 中 `source` 路径不存在于响应中，该条规则被忽略，**不会报错**——此静默行为已在 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 中明确说明，但与部分旧版 SDK 示例代码存在偏差，请以该文档为准。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


