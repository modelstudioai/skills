# world model api reference

世界模型 API 提供面向叙事生成、场景调度与角色行为模拟的专用接口，当前聚焦于 Adventure（冒险叙事）、Directing（场景编排）和 Acting（角色动作生成）三类核心能力。所有接口均通过 RESTful 方式调用，需使用平台颁发的 API Key 进行鉴权。该能力处于持续迭代中，部分功能仍处于邀测阶段。

## 支持的模型/功能

目前开放以下三类世界模型能力：
- **Adventure**：用于生成连贯的多步冒险叙事流，支持环境状态演化与用户意图响应；
- **Directing**：用于动态调度场景元素（如镜头切换、空间布局、时间节奏），适用于影视化叙事生成；
- **Acting**：用于生成符合角色设定的动作、微表情与交互行为序列（当前为邀测中，详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)）。

> **注意**：原始文档中将 Acting 标注为“邀测中”，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 均未注明邀测状态，开发者应以实际接口返回的 `403 Forbidden` 或平台控制台权限提示为准。

## 关键参数

所有请求共用以下基础参数：
- `model`: 必填，取值为 `"world-model/adventure"`、`"world-model/directing"` 或 `"world-model/acting"`；
- `input`: 必填，结构化 JSON 对象，具体 schema 因模型类型而异（详见各子文档）；
- `stream`: 可选，布尔值，默认 `false`；设为 `true` 时启用 SSE 流式响应；
- `max_tokens`: 可选，整数，控制输出长度上限，建议值范围：256–2048。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model`；
2. 在 Header 中设置 `Authorization: Bearer YOUR_API_KEY` 和 `Content-Type: application/json`；
3. Body 中按所选模型填写 `input` 字段（例如 Adventure 模型需包含 `scene_state` 和 `user_intent` 字段）；
4. 解析响应体中的 `output.text`（非流式）或逐帧解析 `data:` 行（流式）。

完整请求示例与字段定义请参阅 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 限制和注意事项

- 单次请求 `input` 总长度（含 JSON 序列化后）不得超过 8192 字符；
- Acting 模型暂不支持 `stream: true`，启用将返回 `400 Bad Request`；
- 所有模型均不支持跨会话状态保持，如需长程一致性，须由调用方自行维护上下文并显式传入；
- 接口响应延迟受输入复杂度影响显著，复杂 Directing 场景建议预估 1.5–3s P95 延迟。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


