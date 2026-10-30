# world model api reference

世界模型 API 提供面向交互式叙事与动态环境建模的推理能力，支持冒险生成、导演调度、角色行为决策等场景。当前以邀测形式开放部分功能，所有接口均基于标准 OpenAPI 规范实现。开发者需通过百炼平台申请对应模型权限后方可调用。

## 支持的模型/功能

目前世界模型 API 由 HappyOyster 团队提供，包含三类核心能力：
- **Adventure（冒险生成）**：根据用户输入构建连贯、可扩展的叙事世界与事件流；
- **Directing（导演调度）**：协调多角色状态、时间线与环境响应，维持世界一致性；
- **Acting（角色行为）**：驱动单个角色在给定情境下的细粒度动作与对话决策（当前处于邀测中，详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)）。

> **注意**：[Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中对 `world_state` 字段的版本兼容性说明存在不一致——前者要求 v2.1+，后者未明确版本约束。建议以最新版 SDK 的 schema 校验为准。

## 关键参数

所有请求需携带以下通用参数（除 `model` 外均为必填）：
- `model`: 模型标识符，如 `"happyoyster/adventure-v1"`、`"happyoyster/directing-v1"`；
- `input.world_state`: JSON 对象，描述当前世界快照（结构见各子文档）；
- `input.user_intent`: 用户本轮指令或提问文本；
- `parameters.max_steps`: 最大推理步数（默认 5，上限 20），影响响应深度与延迟；
- `parameters.return_full_trace`: 布尔值，启用时返回中间世界状态变更轨迹（仅 Directing 和 Acting 支持）。

## 使用方式

1. 向 `POST /v1/world-models/{model}/invoke` 发送请求（`{model}` 为实际模型 ID）；  
2. 请求体为 JSON，格式严格遵循对应 OpenAPI 文档定义；  
3. 鉴权使用平台标准 Bearer [Token](../concepts/token.md)（`Authorization: Bearer <token>`）；  
4. 成功响应返回 `200 OK`，含 `output` 字段（结构化结果）与可选 `trace` 字段。

完整请求示例与错误码说明请参阅 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 限制和注意事项

- 单次请求 `input.world_state` 大小不得超过 256 KB；  
- Acting 功能暂不支持批量调用，且仅限已签署邀测协议的项目使用；  
- 所有世界状态字段名区分大小写，空字符串与 `null` 在语义上不等价；  
- 若连续 3 次请求触发 `429 Too Many Requests`，需等待 60 秒后重试；  
- 当前不支持跨模型状态迁移（例如将 Acting 输出直接作为 Directing 输入），需经客户端显式转换。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


