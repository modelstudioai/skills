# world model api reference

世界模型 API 提供对多模态世界建模能力的程序化访问，支持场景理解、动态推演与交互式内容生成。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（叙事推演）、Directing（镜头调度）和 Acting（角色行为生成）三类核心功能。所有接口均基于 RESTful 设计，需通过 API Key 鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：面向开放世界叙事的因果链推演与状态演化，适用于游戏剧情分支、交互式小说等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：基于视觉语义理解进行镜头语言调度（如景别切换、运镜逻辑、构图建议），输出结构化导演指令。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**：生成符合角色设定、上下文状态及物理约束的细粒度动作序列（含时序、姿态、情绪强度），目前处于邀测阶段。详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中未明确说明 Acting 模型是否支持批量请求或流式响应，而 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确要求 `Content-Type: application/json` 且不支持 multipart；实际接入时请以最新 OpenAPI Schema 为准，避免假设通用行为。

## 关键参数

所有端点共用以下基础参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input` | object | 是 | 输入数据结构，格式依模型而异（见各子文档） |
| `stream` | boolean | 否 | 仅 Adventure 和 Directing 支持；Acting 暂不支持流式（参见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)） |
| `max_steps` | integer | 否 | 推演最大步数，默认 10，上限 50（Adventure 专用） |

## 使用方式

1. 获取 API Key（通过百炼控制台 → API 密钥管理）  
2. 构造 POST 请求至对应 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/adventure`）  
3. 设置 Header：`Authorization: Bearer <YOUR_API_KEY>`，`Content-Type: application/json`  
4. 在 request body 中按 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 等子文档定义组织 `input` 字段  

示例（Adventure 简单推演）：
```json
{
  "model": "happyoyster-adventure",
  "input": {
    "world_state": {"location": "forest", "time": "dusk", "characters": ["player", "wolf"]},
    "action": "player draws sword"
  }
}
```

## 限制和注意事项

- 单次请求 `input.world_state` 字段总 token 数不得超过 8192（Directing 模型为 4096）；超出将返回 `400 Bad Request`  
- Acting 模型暂不开放公网调用，需单独申请邀测权限，且仅支持同步阻塞响应（无 `stream=true` 选项）  
- 所有模型均不支持跨会话状态持久化；若需长程一致性，请在客户端维护 world state 并显式传入每次请求  
- > **注意**：[Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中示例使用 `scene_context` 字段，但最新 schema 已统一为 `world_state`；请以 `/v1/models` 接口返回的实时 schema 或 OpenAPI spec 为准，避免依赖旧示例字段名

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


