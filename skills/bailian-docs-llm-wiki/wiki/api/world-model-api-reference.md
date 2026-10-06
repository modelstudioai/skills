# world model api reference

世界模型 API 提供面向叙事生成、角色行为模拟与场景动态演化的结构化接口，当前聚焦于 Adventure（冒险叙事）、Directing（导演式编排）两类核心能力。API 采用标准 RESTful 设计，支持 JSON 请求/响应，需通过百炼平台统一鉴权。所有功能均处于邀测或灰度阶段，正式商用前请以 [原文标题](../../raw/model-api-reference/world-model-api-reference.md) 中的最新状态为准。

## 支持的模型/功能

- **Adventure 模块**：用于生成多分支剧情、环境反馈与玩家交互响应，适用于游戏叙事引擎与互动小说场景。  
- **Directing 模块**：支持对多个角色行为、镜头调度、节奏控制等导演级指令建模，常用于虚拟制片与AI导演原型。  
- **Acting 模块（邀测中）**：提供细粒度角色动作、微表情、语音韵律建模能力，当前仅限白名单用户调用，详情见 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中将 Acting 模块标注为“邀测中”，但部分内部测试文档（未纳入本次输入）提及该模块已开放小范围公测。请以 [原文标题](../../raw/model-api-reference/world-model-api-reference.md) 的当前描述为准，避免依赖未公开变更。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `scene_context` | object | 是 | 描述当前场景的结构化上下文，含时间、空间、角色状态等字段，格式详见各模块 OpenAPI 文档 |
| `narrative_intent` | string | 否 | 叙事意图标签（如 `"branch"`、`"resolve"`、`"escalate"`），影响生成策略 |
| `max_steps` | integer | 否 | 最大推理步数，默认 3，上限 10；超过可能触发截断并返回 `truncated: true` |

所有模块共用统一鉴权头 `Authorization: Bearer <api_key>`，且要求 `Content-Type: application/json`。

## 使用方式

1. 获取 API Endpoint：各模块独立部署，Endpoint 格式为 `https://dashscope.aliyuncs.com/api/v1/world-model/{module}`（`module` 取值为 `adventure` 或 `directing`）  
2. 构造请求体：严格遵循对应 OpenAPI Schema，例如 Adventure 请求需包含 `player_action` 字段，参考 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
3. 发送 POST 请求并解析响应：成功响应含 `output.steps[]`（每步为带 timestamp 的事件对象）和 `next_context`（用于链式调用）

## 限制和注意事项

- 单次请求最大 `scene_context` 大小为 8KB；超限将返回 `400 Bad Request`  
- Adventure 模块不支持跨世界状态持久化，每次请求视为独立会话；如需长程记忆，请自行维护 context 并显式传入  
- Directing 模块对镜头描述字段（`shot_description`）执行语义校验，非法值（如 `"zoom into void"`）将导致 `422 Unprocessable Entity`  
- 所有模块暂不支持流式响应（`stream=true` 参数无效）  

> **注意**：原始文档未明确说明 rate limit 配额，但实际调用中默认为 5 QPS / key；超出将返回 `429 Too Many Requests`。该限制未在 [原文标题](../../raw/model-api-reference/world-model-api-reference.md) 中体现，属平台运行时策略，建议客户端实现退避重试。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


