# world model api reference

世界模型 API 提供面向叙事与交互场景的多模态建模能力，支持剧情推演、角色行为生成与环境状态演化等核心任务。当前以 HappyOyster 系列为主要实现，涵盖 Adventure、Directing 和 Acting 三类子模型。所有接口均通过标准 HTTP POST 调用，返回结构化 JSON 响应。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态演化与剧情分支预测，适用于游戏引擎集成与互动叙事系统。  
- **Directing 模型**：聚焦镜头调度、节奏控制与多角色协同编排，常用于虚拟制片与AI导演工作流。  
- **Acting 模型**（邀测中）：支持细粒度角色动作、微表情与语音韵律生成，需申请白名单权限。  
详细能力边界与输入输出格式请参阅 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)、[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 和 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `scene_state` | object | 是 | 当前世界状态快照，含环境、角色、时间戳等字段；结构定义见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) |
| `intent` | string | 是 | 用户或系统意图描述（如 `"advance_plot"`、`"recenter_focus"`），影响模型决策倾向 |
| `max_steps` | integer | 否 | 最大推演步数，默认为 1；Acting 模型不支持该参数 |

> **注意**：`scene_state` 的 schema 在 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中定义了额外的 `camera_plan` 字段，但该字段在 Adventure 模型中被忽略——实际调用时请按目标模型文档严格构造请求体。

## 使用方式

1. 向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/{model_type}` 发起 POST 请求  
2. 设置 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`  
3. 请求体示例（Adventure）：
```json
{
  "scene_state": {"world_time": "2024-06-15T14:22:00Z", "characters": [{"id": "hero", "x": 12.3, "y": 4.7}]},
  "intent": "advance_plot",
  "max_steps": 1
}
```

## 限制和注意事项

- 单次请求最大 `scene_state` 大小为 256KB；超限将返回 `413 Payload Too Large`  
- Acting 模型暂不支持流式响应，且仅接受 `application/json` 格式输入（不兼容 `multipart/form-data`）  
- 所有模型均要求 `scene_state` 中的 `world_time` 为 ISO 8601 UTC 时间格式，否则触发校验失败 —— 此约束在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中明确，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 未强调，建议统一遵循。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


