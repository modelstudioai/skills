# world model api reference

世界模型 API 提供面向交互式叙事与动态环境建模的推理能力，支持冒险生成、导演调度、角色行为决策等场景。当前以邀测形式开放部分功能，所有接口均基于 OpenAPI 3.0 规范定义。开发者需通过百炼平台申请对应模型的调用权限后方可使用。

## 支持的模型/功能

目前世界模型 API 包含以下三个核心子系统，均由 HappyOyster 团队提供：

- **Adventure（冒险生成）**：用于构建多分支剧情、环境状态演化及玩家影响反馈，详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing（导演调度）**：负责全局节奏控制、事件触发时机管理与多角色协同编排，详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting（角色行为）**：实现单角色实时响应、情绪状态迁移与动作序列生成，当前处于邀测阶段，详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：原始文档中未明确各子系统是否共享统一 base URL 或鉴权方式；实际接入时请以 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `servers` 字段为准，其他子系统若存在不一致配置，以该文档为权威依据。

## 关键参数

所有请求必须携带以下通用 Header：
- `Authorization: Bearer <access_token>`（token 由百炼平台 OAuth2 流程颁发）
- `Content-Type: application/json`

各接口共用以下可选 Query 参数：
- `trace_id`（string）：用于链路追踪，建议客户端生成 UUIDv4
- `timeout_ms`（integer）：超时毫秒数，范围 500–30000，默认 5000

请求 Body 中，`scene_state`（JSON object）为必填字段，结构需符合 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 定义的 `SceneStateSchema`。

## 使用方式

1. 在百炼控制台开通「世界模型」服务并申请对应子模型权限；
2. 获取 access_token（参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的认证章节）；
3. 根据业务需求选择子系统 endpoint（如 `/v1/adventure/step`, `/v1/directing/trigger`），构造符合 OpenAPI Schema 的请求；
4. 发起 POST 请求，解析返回的 `next_state` 与 `actions` 字段驱动后续逻辑。

## 限制和注意事项

- 单次请求 `scene_state` 大小上限为 256 KB，嵌套深度不得超过 12 层；
- Acting 子系统仅对白名单用户开放，未获邀测权限的调用将返回 `403 Forbidden`；
- 所有子系统均不支持流式响应（`text/event-stream`），必须等待完整 JSON 响应；
- 若发现 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中描述的 `emotion_decay_rate` 参数在实际响应中缺失，请以运行时返回的 Schema 为准，该文档可能存在滞后更新。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


