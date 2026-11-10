# world model api reference

世界模型 API 提供对多模态世界模拟能力的程序化调用，支持场景构建、角色行为编排与动态交互生成。当前以 HappyOyster 系列为主要实现，覆盖 Adventure（探索）、Directing（导演）和 Acting（表演）三类核心能力。所有接口均基于 OpenAPI 规范设计，需通过百炼平台统一鉴权与路由。

## 支持的模型/功能

- **Adventure 模型**：用于生成开放世界中的环境演化、事件触发与空间状态推演，适用于游戏引擎集成与仿真系统。  
- **Directing 模型**：支持多角色叙事调度、镜头语言生成与剧情分支控制，常用于互动影视与教育模拟。  
- **Acting 模型**（邀测中）：提供细粒度角色动作、微表情与对话节奏建模，当前仅限白名单用户访问。该能力在 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中有详细接口定义。

> **注意**：[原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中标注的 `scene_version` 参数默认值为 `"v2"`，但实际服务端已强制升级至 `"v3"`（自 2024-09-15 起），旧值将被静默覆盖。请勿在请求中显式传入 `"v2"`。

## 关键参数

所有世界模型 API 共享以下必需参数：
- `model`: 必填，取值为 `"happyoyster-adventure"`, `"happyoyster-directing"` 或 `"happyoyster-acting"`  
- `input`: 必填，结构化 JSON，格式依模型类型而异（详见各子文档）  
- `stream`: 可选，布尔值，仅 `happyoyster-directing` 支持流式响应  
- `max_steps`: 可选，整数，限制单次推理的最大世界演化步数（默认 10，上限 50）  

完整参数约束与示例见 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 使用方式

1. 在百炼控制台开通「世界模型」服务并获取 API Key；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/world-models/{model}`；  
3. 设置 `Authorization: Bearer <API_KEY>` 与 `Content-Type: application/json`；  
4. 按对应模型文档组织 `input` 字段（如 Adventure 需包含 `world_state` 和 `trigger_event`）。  

SDK 支持 Python（`dashscope==1.20.0+`）、Node.js（`@dashscope/world-model@0.8.3+`），版本兼容性以各 OpenAPI 文档为准。

## 限制和注意事项

- 单次请求 `input` 总大小不得超过 2MB；  
- Acting 模型暂不支持 `stream=true`，且响应延迟较其他两类高约 300–800ms；  
- 所有模型均不支持跨会话状态持久化，若需长周期世界演化，请自行维护 `world_state` 并在每次请求中显式传入；  
- 当前仅支持 UTF-8 编码，非 ASCII 字符（如中文角色名、地名）必须正确转义。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


