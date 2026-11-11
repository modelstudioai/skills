# world model api reference

世界模型 API 提供面向叙事生成、场景调度与角色行为模拟的多模态建模能力，当前聚焦于 Adventure（冒险叙事）、Directing（场景编排）两类核心功能。API 以 RESTful 形式提供，支持 JSON 请求体与标准 HTTP 状态码响应。所有接口均需通过百炼平台申请对应模型权限后调用。

## 支持的模型/功能

目前开放以下三类子模型能力（均属 HappyOyster 系列）：
- **Adventure 模型**：用于生成连贯的交互式冒险故事流，支持多轮状态感知与分支决策；详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：用于动态调度场景元素（如镜头、光照、角色位置），输出结构化导演指令；详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**（邀测中）：用于驱动单个角色的细粒度行为与情绪表达，当前仅对白名单用户开放；详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中未明确说明 Acting 模型是否已支持 streaming 响应，但 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 的示例请求中使用了 `stream=false` 参数，而同期发布的 Adventure 接口文档默认启用流式响应。开发者应以实际调用返回的 `Content-Type` 和响应格式为准。

## 关键参数

所有请求共用以下必需头信息与参数：
- `Authorization: Bearer <api_key>`（平台颁发的 API Key）
- `Content-Type: application/json`
- `model`: 必填字符串，取值为 `"happyoyster-adventure"`、`"happyoyster-directing"` 或 `"happyoyster-acting"`
- `input`: 对象，结构依模型类型而异（详见各子文档）

通用可选参数：
- `temperature`: 控制生成随机性（0.0–1.0，默认 0.7）
- `max_tokens`: 输出最大 token 数（默认 512，上限 2048）
- `top_p`: 核采样阈值（默认 1.0）

## 使用方式

1. 向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model` 发起 POST 请求  
2. 在请求体中按目标模型要求组织 `input` 字段（例如 Adventure 需包含 `scene_state` 和 `user_action`）  
3. 解析响应中的 `output.text`（文本生成类）或 `output.directives`（结构化指令类）字段  

完整请求/响应示例见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 “请求示例” 小节。

## 限制和注意事项

- 单次请求 `input` 总长度（含上下文）不得超过 4096 tokens；超长输入将被截断并返回 `400 Bad Request`  
- Acting 模型暂不支持批量请求（`batch_size > 1`），且无重试保障机制  
- 所有模型均不支持跨会话状态持久化；若需长程一致性，须由客户端维护 `session_id` 并在 `input` 中显式传入  
- 错误码 `429 Too Many Requests` 表示超出当前配额，配额策略详见控制台「用量管理」页面（非本 API 文档范畴）

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


