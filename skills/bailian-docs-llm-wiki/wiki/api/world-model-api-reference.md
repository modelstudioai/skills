# world model api reference

世界模型 API 提供对多模态场景理解与动态世界建模能力的程序化访问，支持基于视频、图像及文本输入构建可交互的环境表征。当前以 HappyOyster 系列模型为核心实现，覆盖冒险（Adventure）、导演（Directing）和表演（Acting）三类任务范式。该接口面向需要实时环境推理与行为规划的智能体系统设计者。

## 支持的模型/功能

- **Adventure 模型**：面向开放世界探索任务，支持从视频流中提取时空状态图、识别可交互对象及推断潜在行动路径。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：面向多智能体协同编排，提供镜头调度、角色动线规划与事件时序对齐能力。其输入需包含结构化场景描述与目标叙事约束。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**（邀测中）：面向单智能体具身行为生成，输出符合物理约束与社会规范的动作序列。当前仅对白名单用户开放，接口契约尚未稳定。详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：Acting 模型的输入 schema 在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中定义为 `ActionRequestV2`，但最新 SDK v0.4.1 已默认使用 `ActionRequestV3`（含关节力矩约束字段），实际调用请以 SDK 文档为准。

## 关键参数

所有端点共用以下基础参数：
- `model`: 必填，取值为 `"happyoyster/adventure"`、`"happyoyster/directing"` 或 `"happyoyster/acting"`；
- `input`: 必填，JSON 对象，结构依模型类型而异（见各子文档）；
- `stream`: 可选，布尔值，默认 `false`；仅 Adventure 和 Directing 支持流式响应，Acting 暂不支持；
- `max_steps`: 可选，整数，最大推理步数（仅 Adventure 有效），默认 `16`。

## 使用方式

1. 发送 `POST` 请求至 `https://dashscope.aliyuncs.com/api/v1/world-models/{model}/invoke`；
2. 设置请求头：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
3. 在请求体中按模型要求构造 `input` 字段（例如 Adventure 需传入 base64 编码的帧序列或视频 URL）；
4. 解析响应中的 `output` 字段，其结构与所选模型强绑定——务必参照对应子文档的响应示例与字段说明，例如 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 明确了 `state_graph` 的节点属性命名规则。

## 限制和注意事项

- 单次请求最大输入长度：Adventure ≤ 512 帧（或等效视频时长 ≤ 32 秒），Directing ≤ 8192 字符，Acting ≤ 2048 字符；
- 输出延迟敏感：Adventure 默认启用低延迟模式（`latency_optimized: true`），若需更高精度，需显式设置 `latency_optimized: false` 并接受约 +300ms 延迟；
- 所有模型均不支持跨会话状态持久化，每次请求必须携带完整上下文；
- > **注意**：原始文档中 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 将 `scene_context` 描述为“可选”，但 v2.3.0 服务端已强制校验该字段非空，缺失将返回 `400 Bad Request`。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


