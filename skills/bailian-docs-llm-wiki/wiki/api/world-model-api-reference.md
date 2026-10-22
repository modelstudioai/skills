# world model api reference

世界模型 API 提供面向叙事与交互场景的多模态建模能力，支持剧情生成、角色行为决策、环境状态演化等核心功能。当前以 HappyOyster 系列模型为主力实现，覆盖 Adventure（冒险叙事）、Directing（导演式控制）和 Acting（角色实时动作）三类子任务。所有接口均基于 RESTful 设计，需通过 API Key 鉴权调用。

## 支持的模型/功能

- **HappyOyster Adventure**：用于长程剧情规划与分支逻辑生成，适用于游戏叙事引擎、互动小说等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **HappyOyster Directing**：提供高层意图到场景指令的映射，支持镜头调度、节奏控制、冲突强度调节等导演级干预能力。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **HappyOyster Acting（邀测中）**：面向单角色实时响应建模，输出符合性格、状态与上下文的动作/台词序列。该能力尚未全量开放，接口细节请参阅 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中未明确说明 Acting 模型是否已支持流式响应，但 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 的示例请求体包含 `stream: true` 字段；而 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确声明“不支持流式”。开发者应以各子模型文档的 `stream` 参数说明为准，不可跨模型复用流式配置。

## 关键参数

通用必填参数：
- `model`: 字符串，取值为 `"happyoyster-adventure"`、`"happyoyster-directing"` 或 `"happyoyster-acting"`；
- `input`: 对象，结构依模型类型而异（如 Adventure 要求 `story_context` 和 `available_choices`）；
- `temperature`: 浮点数，范围 `[0.0, 2.0]`，控制输出随机性（默认 `0.7`）；
- `max_tokens`: 整数，最大生成 token 数（Adventure 默认 `1024`，Directing 默认 `512`，Acting 默认 `256`）。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`；
2. 设置 Header：`Authorization: Bearer <YOUR_API_KEY>`，`Content-Type: application/json`；
3. 在 Body 中传入符合对应模型 schema 的 JSON 对象；
4. 解析响应中的 `output.choices[0].message.content` 字段获取结果。

## 限制和注意事项

- 单次请求 `input` 总长度（含文本与结构化字段）不得超过 8192 tokens；
- Acting 模型处于邀测阶段，未获白名单权限的调用将返回 `403 Forbidden`；
- 所有模型均不支持跨会话状态持久化，如需连续交互，须由客户端维护 `session_id` 并在 `input` 中显式传递；
- 当前不支持图像或音频输入，仅接受纯文本及轻量结构化数据（如 JSON 描述的场景状态）。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


