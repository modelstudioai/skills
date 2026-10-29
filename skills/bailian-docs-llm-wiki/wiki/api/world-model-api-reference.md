# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的鉴权与错误码规范。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、角色关系图谱与剧情分支逻辑，适用于游戏叙事或互动小说初始化；参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing**：用于多角色协同调度、镜头语言编排与节奏控制，适用于影视化叙事或虚拟演出编导；参考 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting**（邀测中）：用于单角色实时情绪建模、台词演绎与微表情驱动，需单独申请权限；参考 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：文档中“Acting”模块标注为“邀测中”，但部分内部 SDK 示例代码已默认启用该 endpoint，实际调用前请务必确认账号权限状态，避免 403 错误。

## 关键参数

所有请求需包含以下通用头部参数：
- `Authorization: Bearer <access_token>`（OAuth2.0 访问令牌）
- `Content-Type: application/json`
- `x-world-model-version: v1`（必需，当前仅支持 v1）

各功能模块共用以下请求体字段（JSON）：
- `scene_id`（string, 必填）：场景唯一标识，长度 ≤ 64 字符，仅支持字母、数字、下划线
- `context`（object, 可选）：上下文快照，结构见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `ContextSchema`
- `timeout_ms`（integer, 默认 15000）：单次推理超时毫秒数，范围 5000–30000

## 使用方式

1. 获取 access_token：通过 `/v1/auth/token` 接口使用 client_id/client_secret 交换令牌  
2. 构造请求：向对应 endpoint 发送 POST 请求，例如 Adventure 模块 endpoint 为 `/v1/adventure/generate`  
3. 解析响应：成功返回 `200 OK`，含 `result` 字段（结构化输出）与 `trace_id`（用于问题排查）  
4. 错误处理：关注 `error.code`（如 `INVALID_SCENE_ID`, `CONTEXT_TOO_LARGE`），详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 的错误码附录  

## 限制和注意事项

- 单账号 QPS 限流：5 次/秒（所有模块共享），突发流量将触发 `429 Too Many Requests`  
- `context` 字段总字符数上限为 8192；超出将被截断并返回警告字段 `warnings: ["context_truncated"]`  
- Acting 模块暂不支持流式响应（`stream=false` 强制生效），且不兼容 `response_format=delta` 参数  
- 所有模型输入禁止包含可执行代码、系统指令或越权操作描述，违者触发 `400 Bad Request` 并记录审计日志

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


