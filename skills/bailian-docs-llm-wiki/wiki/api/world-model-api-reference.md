# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的身份认证机制。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、角色关系图谱与剧情分支逻辑，适用于游戏叙事或互动小说初始化；  
- **Directing**：支持多角色协同行为编排、镜头语言调度与节奏控制，常用于虚拟制片或AI导演场景；  
- **Acting**（邀测中）：提供角色实时情绪建模、台词微调与肢体动作生成，依赖高保真角色状态上下文。  
> **注意**：[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中标注的“邀测中”状态与 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的公开可用说明存在阶段差异，实际接入前请以控制台权限状态为准。

## 关键参数

所有请求需携带以下通用参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`world-model-happyoyster-v1`（暂不支持其他别名） |
| `input` | object | 是 | 包含 `scene`, `characters`, `constraints` 等子字段，结构依功能模块而异，详见各模块 OpenAPI 文档 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应（仅 Adventure 和 Directing 支持） |
| `max_tokens` | integer | 否 | 最大输出 token 数，范围 64–4096；Acting 模块强制限制 ≤1024 |

详细字段定义请参阅 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中的 `RequestBody` 描述。

## 使用方式

1. 通过百炼控制台开通「世界模型」服务并获取 API Key；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model`；  
3. 设置 Header：`Authorization: Bearer <YOUR_API_KEY>`，`Content-Type: application/json`；  
4. 在 `input` 中按所选功能填充结构化数据（例如 `input.scene.type = "fantasy"` 用于 Adventure）；  
5. 解析响应中的 `output.result` 字段，其格式为标准 JSON 对象，非 Markdown 或富文本。

## 限制和注意事项

- 单次请求 `input` 总长度（UTF-8 编码）不得超过 8192 字符；  
- Acting 模块暂不支持 `stream=true`，且响应延迟较其他模块高约 300–800ms；  
- 所有模块均不支持跨会话状态保持，如需连续交互，请自行维护 `session_id` 并在 `input` 中显式传递；  
- 若发现 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中示例 `input` 字段与实际返回结构不一致（如缺失 `timeline` 字段），请以最新响应体为准，文档更新可能存在滞后。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


