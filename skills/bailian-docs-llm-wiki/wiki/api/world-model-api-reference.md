# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的身份认证机制。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、角色关系图谱与剧情分支逻辑，适用于游戏叙事或互动小说初始化；  
- **Directing**：支持多角色协同行为编排、镜头语言映射与节奏控制，常用于虚拟制片流程；  
- **Acting**（邀测中）：提供角色实时情绪建模、台词风格迁移与微表情驱动能力，依赖 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 文档说明。

> **注意**：原始文档中将 Acting 标注为“邀测中”，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 均未注明访问限制，实际调用前请确认控制台权限状态。

## 关键参数

所有请求需包含以下通用参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `happyoyster-adventure-v1`、`happyoyster-directing-v1`；不支持 `happyoyster-acting-v1` 在公开环境调用 |
| `input` | object | 是 | 输入结构体，具体字段依模型类型而异（详见各子文档） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅 Adventure 与 Directing 支持 `true` |

其他模型特有参数（如 `scene_context`、`emotion_bias`）请参阅对应子文档，例如 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中定义的 `shot_sequence` 字段为必填项。

## 使用方式

1. 获取 API Key 并配置 `Authorization: Bearer <key>` 请求头；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`；  
3. 在 `input` 中按目标模型要求组织数据（如 Adventure 需提供 `world_seed` 和 `narrative_constraints`）；  
4. 解析响应中的 `output.result` 字段获取结构化输出。

示例请求体（Adventure）：
```json
{
  "model": "happyoyster-adventure-v1",
  "input": {
    "world_seed": "cyberpunk_2077",
    "narrative_constraints": ["no magic", "single protagonist"]
  }
}
```

## 限制和注意事项

- 单次请求最大输入长度为 8192 tokens，超出将返回 `400 Bad Request`；  
- Acting 模块暂不支持批量调用与长上下文维持，相关约束详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)；  
- 所有模型默认超时时间为 30 秒，Directing 在复杂镜头链场景下建议主动设置 `timeout=60`；  
- 输出字段命名存在版本差异：v1 接口返回 `output.result`，而部分测试环境文档误写为 `response.data` —— 请以 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中定义的实际响应结构为准。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


