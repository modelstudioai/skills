# world model api reference

世界模型 API 提供面向叙事与交互场景的多模态建模能力，支持剧情推演、角色行为生成与环境状态演化等核心任务。当前以 HappyOyster 系列模型为主力实现，覆盖 Adventure（冒险推演）、Directing（导演式编排）和 Acting（角色化动作生成）三类子能力。该接口遵循标准 RESTful 设计，需通过 `POST /v1/world-model` 调用。

## 支持的模型/功能

- **HappyOyster Adventure**：用于长程剧情逻辑推演与世界状态演化，适用于游戏叙事、互动小说等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **HappyOyster Directing**：支持多角色协同调度、镜头语言控制与节奏干预，常用于虚拟制片与AI导演流程。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **HappyOyster Acting（邀测中）**：提供细粒度角色动作、微表情与语音韵律生成能力，当前仅对白名单用户开放。详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中未明确说明 Acting 模型是否已支持 streaming 响应，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确要求 `response_format=stream` 时需启用 SSE；实际调用 Acting 接口时若设置 `stream=true` 将返回 400 错误——请以最新 SDK 文档为准，勿直接复用 Directing 的流式参数约定。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 取值为 `happyoyster-adventure`、`happyoyster-directing` 或 `happyoyster-acting` |
| `input` | object | 是 | 输入结构体，格式依模型类型而异（见各子文档） |
| `max_steps` | integer | 否 | 最大推理步数，默认 12，上限 64（Adventure/Directing），Acting 固定为 1 |
| `temperature` | number | 否 | 采样温度，范围 [0.0, 2.0]，默认 0.7 |

## 使用方式

1. 发送 `POST https://dashscope.aliyuncs.com/api/v1/world-model`
2. 设置请求头：`Authorization: Bearer <api_key>`，`Content-Type: application/json`
3. 请求体示例（Adventure）：
```json
{
  "model": "happyoyster-adventure",
  "input": {
    "world_state": {"location": "forest", "time": "dusk"},
    "action": "explore_north"
  },
  "max_steps": 8
}
```
完整输入结构定义请参阅对应子文档，例如 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `InputSchema` 小节。

## 限制和注意事项

- 单次请求最大 `input` 字符数：16384（所有模型统一）
- 每分钟调用配额按模型独立计算，`happyoyster-acting` 配额默认为 0，需单独申请
- `happyoyster-acting` 不支持 `max_steps > 1`，传入将被静默截断为 1
- 所有模型均不支持 `system` 字段，若传入将被忽略（与通用 LLM API 行为不一致）

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


