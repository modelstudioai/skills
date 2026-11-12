# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的鉴权与错误码规范。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、任务流与环境响应逻辑，适用于游戏叙事或互动小说场景；  
- **Directing**：用于控制多角色行为节奏、镜头调度与剧情分支决策，强调时序协调性；  
- **Acting**（邀测中）：用于驱动单角色的细粒度动作、情绪表达与对话演绎，依赖角色状态上下文。  

各模块的具体接口定义与示例详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)、[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 和 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

## 关键参数

所有请求必须包含以下通用参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`world-model-adventure` / `world-model-directing` / `world-model-acting`（仅邀测用户可用） |
| `input` | object | 是 | 包含 `scene_state`、`character_states` 等上下文字段，结构依模块而异 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应（仅 Adventure 和 Directing 支持） |

> **注意**：`world-model-acting` 模型暂不支持 `stream=true`，该限制未在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中明确说明，但实测返回 `400 Unsupported parameter` 错误。

## 使用方式

1. 通过百炼控制台申请世界模型 API 权限（需注明使用场景）；  
2. 获取 `API-Key` 并在请求头中携带：`Authorization: Bearer <your_api_key>`；  
3. 向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model` 发送 POST 请求；  
4. 解析响应中的 `output.result` 字段获取结构化输出（如 `narrative_step`、`camera_action` 或 `dialogue_line`）。

完整调用示例与 SDK 集成说明见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 限制和注意事项

- 单次请求 `input` 总字符数上限为 8192；  
- 每分钟调用配额默认为 60 次（可提工单申请提升）；  
- Acting 模块仅对已签署 NDA 的合作方开放，普通邀测用户调用将返回 `403 Forbidden`；  
- 所有模块均不支持跨会话状态持久化，需由调用方自行维护 `scene_state` 版本一致性。  

> **注意**：原始文档中 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 将最大 `input` 长度标为 10000，但服务端实际校验阈值为 8192，以运行时行为为准。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


