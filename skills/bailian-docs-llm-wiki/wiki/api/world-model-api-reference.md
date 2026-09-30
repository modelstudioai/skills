# world model api reference

世界模型 API 提供面向游戏与交互式叙事场景的多模态建模能力，支持剧情生成、角色行为决策、环境状态演化等核心功能。当前以 HappyOyster 系列模型为主力实现，涵盖 Adventure（冒险叙事）、Directing（导演调度）和 Acting（角色表演）三大子系统。所有接口均通过标准 HTTP POST 调用，遵循 OpenAPI 3.0 规范。

## 支持的模型/功能

- **Adventure 模型**：用于生成动态剧情分支、世界状态演化及玩家意图推理，适用于开放世界 RPG 或文字冒险类应用。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。  
- **Directing 模型**：负责多角色协同调度、镜头语言生成与节奏控制，常用于交互式影视或虚拟制片流程。其能力说明见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。  
- **Acting 模型**（邀测中）：专注单角色实时行为建模，包括微表情、语音韵律与动作序列生成，当前仅对白名单用户开放。完整接口定义请参阅 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中未明确标注 Acting 模型是否支持流式响应，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确要求 `stream: false`；实际调用时若启用 `stream=true` 将返回 400 错误，建议以 Directing 文档为准统一禁用流式。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input.world_state` | object | 是 | 当前世界快照（JSON Schema 见各子模型文档） |
| `input.user_intent` | string | 否 | 用户最近输入或动作意图（仅 Adventure 和 Directing 推荐提供） |
| `parameters.temperature` | number | 否 | 默认 0.7；Acting 模型建议 ≤0.5 以保障行为一致性 |

## 使用方式

1. 向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model` 发起 POST 请求  
2. Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. Body 示例（Adventure 场景）：
```json
{
  "model": "happyoyster-adventure",
  "input": {
    "world_state": {"location": "forest", "characters": ["player", "elf"]},
    "user_intent": "ask elf about the ancient gate"
  },
  "parameters": {"temperature": 0.6}
}
```

## 限制和注意事项

- 单次请求 `world_state` 最大 JSON 大小为 128 KB；超限将返回 `413 Payload Too Large`  
- Acting 模型暂不支持 `system_prompt` 字段，该字段在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中虽有定义，但在 Acting 实现中被忽略  
- 所有模型均要求 `input.world_state` 包含 `location` 和 `characters` 两个顶层字段，缺失将触发校验失败（HTTP 400）  
- 调用频率限制：默认 5 QPS / key，如需提升请提交工单申请配额扩容

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


