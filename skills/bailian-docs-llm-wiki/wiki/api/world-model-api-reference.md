# world model api reference

世界模型 API 提供对多模态世界建模能力的程序化访问，支持场景理解、动态推演与角色行为生成等核心功能。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（探索推演）、Directing（叙事调度）和 Acting（角色动作生成）三类子模型。所有接口均基于 RESTful 设计，需通过 API Key 认证，并遵循统一的请求/响应结构。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态推理与多步因果推演，适用于游戏环境模拟、虚拟代理路径规划等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：专注叙事逻辑编排与事件触发调度，支持时间线管理、角色关系演化及冲突生成。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**：处于邀测阶段，提供细粒度角色动作序列生成（含肢体、语音、微表情），依赖 Adventure 与 Directing 的输出作为上下文输入。详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：Acting 模型的输入 schema 在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中定义为 `scene_state + narrative_context`，但最新 SDK v0.4.2 已将 `narrative_context` 替换为 `directing_output_id` 引用字段——请以 SDK 文档为准，API 参考文档尚未同步更新。

## 关键参数

所有请求共用以下必需参数：
- `model`: 字符串，取值为 `"happyoyster/adventure"`、`"happyoyster/directing"` 或 `"happyoyster/acting"`  
- `input`: 对象，结构依模型类型而异（参见对应 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `InputSchema` 定义）  
- `parameters.temperature`: 浮点数，范围 `[0.0, 1.5]`，控制输出随机性；Acting 模型建议 ≤ 0.7 以保障动作连贯性  

部分模型特有参数：
- `adventure` 支持 `max_reasoning_steps`（默认 5，上限 12）  
- `directing` 支持 `timeline_horizon_seconds`（整数，单位秒）  
- `acting` 当前不支持 `stream: true`

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/world-models/invoke`  
2. 设置 Header：`Authorization: Bearer <YOUR_API_KEY>`，`Content-Type: application/json`  
3. Body 示例（Adventure）：
```json
{
  "model": "happyoyster/adventure",
  "input": {
    "world_state": {"location": "forest", "entities": ["player", "wolf"]},
    "goal": "reach the cave safely"
  },
  "parameters": {"temperature": 0.4}
}
```
完整请求/响应示例见 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的 “Quick Start” 章节。

## 限制和注意事项

- 单次请求最大 `input` 大小为 8KB；`adventure` 模型单次推理最多返回 3 个并行推演分支  
- `acting` 模型调用必须显式传入由 `directing` 接口返回的 `output_id`，否则返回 `400 InvalidContext`  
- 所有模型均不支持跨会话状态保持，如需长周期世界演化，请自行维护 `world_state` 并在每次请求中完整传入  
- 错误码 `429 Too Many Requests` 表示超出配额，具体限流策略见 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 的 “Rate Limits” 小节

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


