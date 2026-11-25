# world model api reference

世界模型 API 提供面向游戏化、叙事交互场景的多模态推理与行为生成能力，支持剧情推演、角色调度、动作决策等核心功能。当前以 HappyOyster 系列为主要实现载体，涵盖 Adventure（剧情推演）、Directing（场景调度）和 Acting（角色动作生成）三类子服务。所有接口均基于 RESTful 设计，需通过 API Key 鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：用于长周期剧情状态建模与分支推演，支持基于用户输入与世界状态的因果链预测；详见 [Adventure Open API参考](../../raw/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing 模型**：负责多角色协同调度与镜头语言生成，输出场景切换指令、角色位置/朝向变更等结构化指令；详见 [Directing Open API参考](../../raw/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting 模型**（邀测中）：生成细粒度角色动作序列（含肢体、表情、语音节奏），当前仅对白名单用户开放；详见 [Acting Open API参考（邀测中）](../../raw/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)  

> **注意**：原始文档中未明确说明 Acting 模型是否支持流式响应，但 [Acting Open API参考（邀测中）](../../raw/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 的示例请求体中包含 `stream: true` 字段，而 [Directing Open API参考](../../raw/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确声明“不支持流式”。请以各子服务文档为准，勿跨模型复用流式参数。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `world_state` | object | 是 | 当前世界状态快照，格式为 JSON Schema 定义的 `WorldState`，字段含义见各子服务文档 |
| `user_input` | string | 否 | 用户本轮输入文本，部分模型（如 Adventure）可为空，触发自主演化 |
| `max_steps` | integer | 否 | 最大推演步数，默认 1，上限 10（Adventure）/5（Directing）/3（Acting） |
| `temperature` | number | 否 | 采样温度，范围 [0.1, 2.0]，默认 0.8；Acting 模型对此参数更敏感 |

## 使用方式

1. 获取 API Key（控制台 → API 密钥管理 → 创建世界模型专用密钥）  
2. 构造 POST 请求，目标 URL 格式为：`https://dashscope.aliyuncs.com/api/v1/world-model/{service}`，其中 `{service}` 取值为 `adventure` / `directing` / `acting`  
3. 设置 Header：`Authorization: Bearer <your_api_key>`，`Content-Type: application/json`  
4. 请求体按对应子服务文档要求组织，例如 Adventure 调用需包含完整 `world_state` 和可选 `user_input`  

## 限制和注意事项

- 单次请求 `world_state` JSON 大小不得超过 2MB；超过时将返回 `413 Payload Too Large`  
- 所有模型均不支持跨会话状态持久化，`world_state` 必须由客户端全量维护并每次传入  
- Acting 模型处于邀测阶段，未获授权调用将返回 `403 Forbidden`，错误码为 `InvalidAPIKey`（非密钥失效）  
- 若发现 [Adventure Open API参考](../../raw/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中定义的 `WorldState` 字段与实际响应不一致（如缺失 `time_elapsed_ms`），请以最新响应为准，该字段已在 v2.3.1 版本中移除

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


