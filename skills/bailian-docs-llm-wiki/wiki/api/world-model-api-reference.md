# world model api reference

世界模型 API 提供面向叙事与交互场景的多模态建模能力，支持剧情生成、角色行为决策、环境状态演化等核心功能。当前以 HappyOyster 系列模型为主力实现，覆盖 Adventure（冒险叙事）、Directing（导演式控制）和 Acting（角色实时动作）三类子任务。所有接口均基于 RESTful 设计，需通过 API Key 鉴权调用。

## 支持的模型/功能

- **HappyOyster Adventure**：用于长程剧情规划与分支逻辑生成，适用于游戏叙事引擎、互动小说等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **HappyOyster Directing**：提供高层意图到场景指令的映射，支持镜头调度、节奏控制、冲突强度调节等导演级干预能力。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **HappyOyster Acting（邀测中）**：面向单角色实时响应建模，输出符合性格、状态与上下文的动作/台词序列。该能力尚未全量开放，接口细节请参阅 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：文档中“Acting”标注为“邀测中”，但部分 SDK v2.3+ 已默认启用该 endpoint；实际调用前请确认所用 API Key 是否已获邀测白名单权限，否则将返回 `403 Forbidden`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `scene_state` | object | 是 | 当前世界状态快照，含角色位置、情绪、物品持有等字段，结构见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中 `SceneStateSchema` 定义 |
| `intent` | string | 否 | 高层目标描述（如 `"阻止反派启动装置"`），仅 Directing 和 Acting 接口有效 |
| `max_steps` | integer | 否 | 最大推理步数，默认 5，上限 20；超过将截断并返回 partial result |

## 使用方式

1. 构造 POST 请求，`Content-Type: application/json`  
2. 请求体包含 `scene_state` 及可选参数（如 `intent`, `max_steps`）  
3. 设置请求头 `Authorization: Bearer <your_api_key>`  
4. 调用对应 endpoint（例如 `/v1/world-model/adventure`）

示例（cURL）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/world-model/adventure \
  -H "Authorization: Bearer sk-xxx" \
  -H "Content-Type: application/json" \
  -d '{
        "scene_state": {"characters": [{"id": "hero", "mood": "anxious"}]},
        "max_steps": 8
      }'
```

## 限制和注意事项

- 单次请求 `scene_state` JSON 大小不得超过 256 KB；超限将返回 `413 Payload Too Large`  
- Adventure 接口响应延迟中位值约 1.2s（P95 < 3.5s），Directing 与 Acting 因计算复杂度更高，建议设置 5s+ 超时  
- 所有接口均不支持流式响应（`stream=false` 为唯一合法值）  
- > **注意**：原始文档未明确说明 rate limit，但生产环境实际限制为 10 QPS / key；该数值在 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 的 “Rate Limits” 小节中有补充说明，应以此为准。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


