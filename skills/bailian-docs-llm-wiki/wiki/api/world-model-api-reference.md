# world model api reference

世界模型 API 提供对多模态世界模拟能力的程序化调用，支持场景构建、角色行为编排与动态交互生成。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（叙事驱动）、Directing（镜头与节奏控制）和 Acting（角色动作与微表情生成）三类子能力。所有接口均基于 RESTful 设计，需通过百炼平台统一鉴权访问。

## 支持的模型/功能

- **Adventure 模型**：面向开放世界叙事生成，支持长程因果链建模与分支剧情推演，适用于游戏引擎集成与互动小说开发。  
- **Directing 模型**：提供镜头调度、节奏控制与视听语言建议，输出结构化导演指令（如 `shot_type: close_up`, `tempo: accelerando`），详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。  
- **Acting 模型**：处于邀测阶段，专注角色级动作序列与非语言行为建模（如姿态过渡、视线朝向、微表情时序），其接口规范见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。  

> **注意**：[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中描述的 `scene_composition` 字段在 v2.3+ 版本已重命名为 `visual_layout`，旧字段名将被弃用，请以最新 OpenAPI Schema 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 取值为 `happyoyster/adventure`、`happyoyster/directing` 或 `happyoyster/acting`（后者需申请邀测权限） |
| `input` | object | 是 | 输入上下文，结构依模型而异；Adventure 接受 `world_state` + `narrative_goal`，Directing 要求 `current_shot` + `intended_emotion` |
| `max_steps` | integer | 否 | 最大推理步数，默认 8，仅 Adventure 和 Directing 支持；Acting 模型不支持该参数 |

## 使用方式

1. 发送 `POST /v1/world-models/invoke` 请求  
2. 在 `Authorization` Header 中携带 Bearer Token（由百炼平台 `/v1/auth/token` 获取）  
3. Body 示例（Adventure 场景）：
```json
{
  "model": "happyoyster/adventure",
  "input": {
    "world_state": {"location": "abandoned_station", "time_of_day": "dusk"},
    "narrative_goal": "reveal the protagonist's hidden memory"
  },
  "max_steps": 6
}
```
完整请求示例与响应格式参见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 限制和注意事项

- 单次请求最大输入长度：Adventure ≤ 4096 tokens，Directing ≤ 2048 tokens，Acting ≤ 1024 tokens（含 prompt 与 context）  
- Acting 模型暂不支持流式响应，必须等待完整动作序列生成完毕后返回  
- 所有世界模型均**不支持跨会话状态持久化**；若需连续交互，请在客户端维护 `session_id` 并显式传入 `input.session_state` 字段（详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 的 `session_state` 定义）

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


