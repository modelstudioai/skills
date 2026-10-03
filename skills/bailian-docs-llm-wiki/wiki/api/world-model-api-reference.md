# world model api reference

世界模型 API 提供面向具身智能与交互式场景的建模能力，支持动态环境理解、角色行为生成与多智能体协同推演。当前以 HappyOyster 系列模型为核心，覆盖冒险（Adventure）、导演（Directing）和表演（Acting）三类任务范式。所有接口均基于 OpenAPI 规范实现，需通过百炼平台统一鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态演化与因果推理，适用于游戏引擎集成、教育模拟等场景。  
- **Directing 模型**：聚焦多角色叙事调度与事件编排，支持长程剧情一致性控制。  
- **Acting 模型**（邀测中）：面向单角色实时行为生成，强调情感表达与物理动作合理性。  
> **注意**：[Adventure Open API参考](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中描述的 `max_step` 默认值为 50，但 [Directing Open API参考](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 同名参数默认为 200 —— 实际行为以各接口文档最新版为准，建议显式传参。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `scene_id` | string | 是 | 场景唯一标识，需提前在平台注册；未注册时返回 `404` |
| `context_window` | integer | 否 | 上下文窗口长度（token），范围 1024–8192，默认 4096 |
| `temperature` | number | 否 | 采样温度，0.0–2.0，默认 0.7（[Acting Open API参考（邀测中）](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中明确禁用该参数） |
| `enable_state_tracking` | boolean | 否 | 是否启用内部世界状态快照，默认 `true` |

## 使用方式

1. 调用前确保已开通世界模型权限，并获取 `API_KEY`；  
2. 构造 POST 请求至对应 endpoint（如 `/v1/world-model/adventure`），`Content-Type: application/json`；  
3. 在请求头中携带 `Authorization: Bearer <API_KEY>`；  
4. 响应体含 `state_id`（用于后续 step 追溯）与 `next_action` 字段，详见 [原文标题](../../raw/model-api-reference/world-model-api-reference.md)。

## 限制和注意事项

- 单次请求最大输入长度为 65536 字符，超限将返回 `400 Bad Request`；  
- Acting 模型处于邀测阶段，未获白名单的调用将返回 `403 Forbidden`；  
- 所有模型均不支持流式响应（`stream=false` 强制生效），此限制在 [原文标题](../../raw/model-api-reference/world-model-api-reference.md) 中明确声明；  
- 多次调用同一 `scene_id` 时，若间隔超过 30 分钟未续期，内部状态将被自动清理；  
- > **注意**：[原文标题](../../raw/model-api-reference/world-model-api-reference.md) 列出的子文档路径（如 `happyoyster-acting-openapi-reference.md`）尚未同步更新 v2.1 接口变更（如新增 `physics_constraints` 字段），请以 OpenAPI Schema 文件为准。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


