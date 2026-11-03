# world model api reference

世界模型 API 提供对[多模态](../concepts/multi-modal.md)世界建模能力的程序化访问，支持场景理解、动态推演与角色行为生成等核心功能。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（探索推演）、Directing（叙事调度）和 Acting（角色动作生成）三类子模型。所有接口均基于 RESTful 设计，需通过 API Key 认证，并遵循统一的请求/响应结构。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态推理与多步因果推演，适用于游戏环境模拟、虚拟代理路径规划等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：专注叙事逻辑编排与事件触发调度，支持时间线管理、角色关系演化及冲突生成。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**：处于邀测阶段，提供细粒度角色动作序列生成（含肢体、语音、微表情），依赖 Adventure 与 Directing 的输出作为上下文输入。详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：Acting 模型的输入 schema 在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中定义为 `scene_state + narrative_context`，但最新 SDK v0.4.2 已将 `narrative_context` 替换为 `directing_output_id` 引用字段——请以 SDK 文档为准，原始文档尚未同步更新。

## 关键参数

所有请求共用以下必需参数：
- `model`: 字符串，取值为 `"happyoyster/adventure"`、`"happyoyster/directing"` 或 `"happyoyster/acting"`  
- `input`: 对象，结构依模型类型而异（参见各子模型文档）  
- `parameters.max_steps`: 整数，推演最大步数（Adventure 默认 5，Directing 默认 3，Acting 不支持该参数）  
- `parameters.temperature`: 浮点数，控制随机性（0.0–1.0），默认 0.7  

部分高级参数（如 `parameters.world_seed`）仅在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中完整定义，其他模型暂不支持。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`  
2. 设置 Header：`Authorization: Bearer YOUR_API_KEY`，`Content-Type: application/json`  
3. Body 示例（Adventure）：
```json
{
  "model": "happyoyster/adventure",
  "input": {
    "world_state": {"location": "forest", "entities": ["player", "wolf"]},
    "goal": "reach the cave without alerting the wolf"
  },
  "parameters": {"max_steps": 8, "temperature": 0.5}
}
```
4. 解析响应中的 `output.steps[]`（Adventure/Directing）或 `output.actions[]`（Acting）

## 限制和注意事项

- 单次请求最大 `input` 长度为 8192 tokens；超过时返回 `400 Bad Request`  
- Acting 模型仅对白名单用户开放，未获邀测权限的调用将返回 `403 Forbidden`  
- 所有模型均不支持流式响应（`stream: true` 将被忽略）  
- 时间戳字段（如 `output.timestamp`）采用 ISO 8601 格式，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中示例误写为 Unix timestamp，实际响应以 ISO 格式为准。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


