# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，覆盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心场景。该接口当前以 OpenAPI 形式提供，支持结构化输入与事件流式响应。所有能力均需通过百炼平台申请权限后调用，其中 Acting 能力尚处邀测阶段。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作角色：

- **Adventure（冒险）**：用于生成多分支剧情、环境描述与玩家可交互状态，适用于游戏叙事或互动小说；  
- **Directing（导演）**：聚焦于镜头语言、节奏控制与多角色协同调度，输出含时间戳与动作指令的导演脚本；  
- **Acting（表演）**：支持单角色情绪化台词生成与微表情/肢体动作建议（[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)），目前仅对白名单用户开放。

> **注意**：原始文档中将 Acting 标注为“邀测中”，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 均未注明访问限制，实际调用前请确认控制台权限状态。

## 关键参数

所有世界模型 API 共享以下必需参数：

- `model`: 必填，取值为 `"happyoyster/adventure"`、`"happyoyster/directing"` 或 `"happyoyster/acting"`；  
- `input`: 必填，JSON 对象，结构依模型类型而异（详见各 OpenAPI 文档）；  
- `stream`: 可选，布尔值，默认 `false`；设为 `true` 时返回 SSE 流式响应；  
- `max_tokens`: 可选，整数，最大输出 token 数，上限为 4096（[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确指定此限制）。

## 使用方式

1. 在百炼控制台开通「世界模型」服务并获取 API Key；  
2. 根据目标场景选择对应 `model` 值，并按 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 等文档构造 `input`；  
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`，携带 `Authorization: Bearer <api_key>`；  
4. 解析 JSON 响应体中的 `output` 字段（非流式）或逐块处理 `data:` 行（流式）。

## 限制和注意事项

- 单次请求 `input` 总长度（含文本与结构化字段）不得超过 8192 字符；  
- Acting 模块暂不支持 `stream: true`，启用后将返回 400 错误；  
- 所有模型均不支持系统级角色设定（如 `system prompt`），上下文需完全由 `input` 结构承载；  
- 若发现 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中定义的 `shot_type` 枚举值与实际响应不符，请以最新 SDK 版本返回的 `enum` 字段为准。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


