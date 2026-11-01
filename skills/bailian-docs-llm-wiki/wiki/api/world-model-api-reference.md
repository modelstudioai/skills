# world model api reference

世界模型 API 提供面向具身智能与交互式场景的建模能力，支持动态环境理解、行为规划与多角色协同推演。当前以 HappyOyster 系列模型为核心，覆盖冒险（Adventure）、导演（Directing）和表演（Acting）三类任务范式。API 设计遵循 OpenAPI 3.0 规范，所有端点均需通过百炼平台统一鉴权与路由。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界探索与状态演化建模，适用于游戏、仿真等长周期决策场景。  
- **Directing 模型**：聚焦多智能体协作调度与叙事结构生成，支持角色关系图谱与事件因果链推理。  
- **Acting 模型**（邀测中）：面向单角色实时行为生成，强调情感一致性与动作时序建模，当前仅对白名单用户开放。  
> **注意**：[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中描述的 `max_turns=12` 参数在最新 v2.3 SDK 中已调整为 `max_turns=8`，以匹配实际服务端限流策略，请以 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的参数说明为准。

## 关键参数

所有请求共用以下基础参数（`POST /v1/world-model/{task_type}`）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `scene_state` | object | 是 | 当前环境快照，格式见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中 `SceneStateSchema` 定义 |
| `history` | array | 否 | 过往交互轨迹，每项含 `role`, `content`, `timestamp` 字段 |
| `max_steps` | integer | 否 | 最大推理步数，默认 5，上限 20 |

## 使用方式

1. 构造 JSON 请求体，确保 `scene_state` 符合对应模型的 schema 要求；  
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/world-model/{task_type}`，其中 `{task_type}` 取值为 `adventure`、`directing` 或 `acting`；  
3. 设置请求头：`Authorization: Bearer <api_key>` 与 `Content-Type: application/json`；  
4. 解析响应中的 `output.steps[]` 获取逐帧演化结果，或 `output.narrative` 获取结构化叙事输出。

## 限制和注意事项

- 单次请求 `scene_state` 大小不得超过 2MB，嵌套深度不超过 10 层；  
- Acting 模型调用需提前申请邀测权限，未授权调用将返回 `403 Forbidden`；  
- 所有模型均不支持跨会话状态持久化，`history` 字段仅用于当前请求上下文建模；  
- 若发现 [HappyOyster Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中定义的 `agent_constraints` 字段在实际响应中缺失，请确认请求中已显式传入 `enable_constraints=true`。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


