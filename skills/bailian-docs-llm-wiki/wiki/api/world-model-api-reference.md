# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的鉴权与错误码规范。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、角色关系图谱与剧情分支逻辑，适用于游戏叙事或互动小说初始化；参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing**：支持多角色协同行为编排、镜头语言映射与节奏控制，常用于虚拟制片流程；参考 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting**（邀测中）：提供细粒度角色情绪建模、台词风格迁移与实时反应生成，目前仅对白名单用户开放；参考 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)

> **注意**：原始文档中未明确说明 Acting 模块是否已支持流式响应，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确标注 `stream: true` 为可选参数，而 Acting 文档未提及该字段——建议调用前显式传入 `stream=false` 以确保兼容性。

## 关键参数

所有接口共用以下必需参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure-v1`、`happyoyster-directing-v1` 或 `happyoyster-acting-v1` |
| `input` | object | 是 | 结构化输入，具体 schema 因模型而异（详见各子文档） |
| `temperature` | number | 否 | 控制生成随机性，范围 `[0.0, 1.0]`，默认 `0.7` |

此外，`max_tokens` 为全局可选参数（默认 `2048`），但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 特别指出：当 `input.world_size > 5000` 时，`max_tokens` 将被强制截断至 `1024` 以保障推理稳定性。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <your_api_key>`  
2. **请求示例（Adventure）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/adventure \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "happyoyster-adventure-v1",
           "input": {"world_seed": "cyberpunk_2077", "num_characters": 3},
           "temperature": 0.5
         }'
   ```
3. **响应结构**：统一返回 `{"output": {...}, "usage": {...}}`，其中 `output` 内容依模型类型而异（如 Adventure 返回 `world_graph` 对象，Directing 返回 `shot_sequence` 数组）

## 限制和注意事项

- 单次请求 `input` 总字符数上限为 `128KB`；超出将返回 `400 Bad Request`  
- Acting 接口每分钟限流 `5` 次，其余接口为 `60` 次/分钟  
- 所有模型均不支持跨会话状态保持，若需连续交互，请在 `input` 中显式传递上下文快照  
- > **注意**：[Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中列出的 `scene_depth` 参数，在最新 v1.2.3 SDK 中已被弃用，实际生效参数为 `narrative_complexity` ——请以 SDK 文档为准

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


