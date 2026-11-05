# world model api reference

世界模型 API 提供面向仿真、游戏和交互式叙事场景的多模态建模能力，支持动态环境建模、角色行为生成与剧情推演。当前以 HappyOyster 系列为主要实现，涵盖 Adventure、Directing 和 Acting 三类子模型。所有接口均通过标准 HTTP POST 调用，需携带认证 token 并遵循 JSON Schema 请求体规范。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态演化与事件触发，适用于沙盒式探索场景。参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing 模型**：负责全局叙事节奏控制、镜头调度与多角色协同编排。参考 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting 模型**（邀测中）：聚焦单角色实时动作生成与情绪响应，尚未全量开放。参考 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：Acting 模型的 `max_response_tokens` 参数在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中声明为必填，但实际调用时若未提供仍可成功返回（v0.3.1），该不一致将在下个版本修复。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input` | object | 是 | 包含 `world_state`（JSON）、`prompt`（string）及可选 `history`（array） |
| `temperature` | number | 否 | 默认 0.7，范围 [0.0, 1.5]；Acting 模型建议 ≤0.4 以保障行为稳定性 |
| `stream` | boolean | 否 | 仅 Adventure 和 Directing 支持 true；Acting 模型暂不支持流式响应 |

## 使用方式

1. 构造请求体（示例：Adventure 模型）：
```json
{
  "model": "happyoyster-adventure",
  "input": {
    "world_state": {"location": "forest", "time_of_day": "dawn", "entities": ["player", "wolf"]},
    "prompt": "玩家向狼投掷火把"
  },
  "temperature": 0.6
}
```
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model`  
3. 解析响应中的 `output.action_sequence`（Adventure/Directing）或 `output.animation_clip_id`（Acting）

## 限制和注意事项

- 单次请求 `input.world_state` JSON 大小上限为 128 KB；超限将返回 `400 Bad Request`  
- Acting 模型当前仅支持华东1（杭州）Region，其他地域调用将返回 `403 Forbidden`  
- 所有模型均不支持跨会话状态持久化，`input.history` 仅用于当前请求上下文建模，不会写入服务端状态  
- 若需长期世界状态管理，请自行实现外部存储，并在每次请求中显式传入最新 `world_state` —— 此设计已在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中明确说明

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


