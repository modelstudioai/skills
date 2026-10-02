# world model api reference

世界模型 API 提供面向叙事与交互式场景的多模态建模能力，支持剧情推演、角色行为生成与环境动态响应等核心功能。当前以 HappyOyster 系列模型为主力实现，覆盖 Adventure（冒险推演）、Directing（导演调度）和 Acting（角色表演，邀测中）三大子能力。该接口遵循标准 RESTful 设计，兼容 JSON Schema 请求/响应格式。

## 支持的模型/功能

- **HappyOyster-Adventure**：用于长周期剧情演化、状态空间建模与因果链推理，适用于游戏引擎集成与互动叙事系统。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **HappyOyster-Directing**：聚焦多角色协同调度、镜头语言生成与节奏控制，常用于虚拟制片与AI导演工作流。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **HappyOyster-Acting**（邀测中）：支持细粒度角色动作、微表情与语音韵律联合生成，当前仅对白名单用户开放。其接口规范见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：Acting 模型的 `emotion_intensity` 参数在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中定义为 0–100 的整数，但部分旧版 SDK 示例中误用为浮点范围 0.0–1.0，实际调用请以该文档为准。

## 关键参数

所有端点共用以下基础参数（`POST /v1/world-model/{task_type}`）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `scene_state` | object | 是 | 当前世界状态快照，需符合 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 定义的 `SceneState` schema |
| `task_type` | string | 是 | 取值为 `"adventure"`、`"directing"` 或 `"acting"`，决定路由至对应子模型 |
| `max_steps` | integer | 否 | 推演最大步数，默认 1；`adventure` 场景下建议 ≤ 5，避免状态爆炸 |

## 使用方式

1. 认证：使用 `Authorization: Bearer <api_key>` 头部；
2. 请求体示例（Adventure 推演）：
   ```json
   {
     "scene_state": {
       "entities": [{"id": "hero", "position": [3, 5], "health": 82}],
       "world_rules": ["gravity=9.8", "day_cycle=24h"]
     },
     "task_type": "adventure",
     "max_steps": 3
   }
   ```
3. 响应含 `next_state`（更新后的世界状态）与 `reasoning_trace`（可选，需显式启用 `enable_trace=true` 查询参数）。

## 限制和注意事项

- 单次请求 `scene_state` JSON 大小上限为 256 KB；
- `acting` 类型请求暂不支持流式响应，必须等待完整动作序列生成后返回；
- 所有模型均要求 `scene_state` 中的时间戳字段（如 `timestamp_ms`）为毫秒级 Unix 时间，且不得早于请求发起时间前 5 秒，否则将被拒绝——该约束在 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中明确强调，但未在 Adventure 文档中重复说明，请统一遵守。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


