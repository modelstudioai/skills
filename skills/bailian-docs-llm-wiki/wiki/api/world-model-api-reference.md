# world model api reference

世界模型 API 提供面向叙事与交互式场景的建模能力，支持冒险生成、导演调度、角色行为模拟等核心功能。当前以邀测形式开放部分能力，所有接口均基于 RESTful 设计，需通过百炼平台鉴权调用。详细协议规范与字段定义请参考 [原文标题](../../raw/model-api-reference/world-model-api-reference.md)。

## 支持的模型/功能

- **Adventure（冒险生成）**：生成结构化世界观、任务链与环境动态响应  
- **Directing（导演调度）**：控制多角色交互节奏、事件触发时机与叙事分支权重  
- **Acting（角色行为模拟）**：模拟单角色在给定情境下的决策、对话与动作序列（当前处于邀测中）  

各功能模块对应独立 OpenAPI 文档，例如 Adventure 接口详情见 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)，Directing 接口见 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。

## 关键参数

所有请求需包含以下通用 Header：
- `Authorization: Bearer <access_token>`（由百炼平台颁发）
- `Content-Type: application/json`

必选请求体字段（以 Adventure 为例）：
- `world_seed`（string）：初始世界种子，用于可复现生成  
- `scene_context`（object）：描述当前场景的 JSON 结构，含时间、地点、参与角色等  
- `max_steps`（integer, default=10）：生成的最大推理步数（影响输出长度与计算开销）

> **注意**：`max_steps` 在 Acting 模块文档中被标记为 `max_actions`，语义一致但字段名不统一；实际调用时请以对应模块的 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 为准。

## 使用方式

1. 申请邀测权限（仅 Acting 模块需额外审批）  
2. 获取 access_token（通过 `/v1/auth/token`）  
3. 构造 POST 请求至对应 endpoint（如 `POST /v1/world/adventure`）  
4. 解析响应中的 `output` 字段（结构化 JSON）及 `trace_id`（用于问题排查）

## 限制和注意事项

- 单次请求最大 `scene_context` 大小为 8KB，超限将返回 `413 Payload Too Large`  
- Adventure 与 Directing 模块默认 QPS 限流为 5，Acting 模块为 1（邀测期严格限制）  
- 输出内容不保证强因果一致性，建议在业务层做状态校验与回滚机制  
- 所有模型暂不支持流式响应（`stream=false` 为唯一有效值）

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


