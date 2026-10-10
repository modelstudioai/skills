# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的身份认证机制。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、角色关系图谱与剧情分支逻辑，适用于游戏叙事设计与互动小说构建；  
- **Directing**：支持多角色对话调度、镜头语言编排与节奏控制，常用于虚拟制片与AI导演场景；  
- **Acting**（邀测中）：提供角色人格建模、情绪状态迁移与实时台词演绎能力，详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中将 Acting 标注为“邀测中”，但 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 均未注明邀测状态，实际接入时请以控制台权限开通情况为准。

## 关键参数

所有请求需携带以下通用参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"happyoyster/adventure-v1"`、`"happyoyster/directing-v1"` |
| `input` | object | 是 | 输入结构体，具体字段依模型类型而异（见各子文档） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false` |
| `temperature` | number | 否 | 采样温度，范围 `[0.0, 2.0]`，仅部分模型支持 |

模型特有参数请参考对应子文档，例如 `Directing` 模块需额外指定 `scene_context` 字段，详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。

## 使用方式

1. 通过百炼控制台申请世界模型调用权限（尤其注意 Acting 模块需单独申请）；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`；  
3. 在 `Authorization` Header 中传入 Bearer [Token](../concepts/token.md)；  
4. 请求体示例（Adventure）：
```json
{
  "model": "happyoyster/adventure-v1",
  "input": {
    "world_seed": "cyberpunk_2077",
    "narrative_goal": "建立主角与反派的初次对峙"
  }
}
```

完整请求规范与错误码定义参见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。

## 限制和注意事项

- 单次请求 `input` 总长度上限为 8192 字符；  
- Acting 模块暂不支持 `stream: true`；  
- 所有模型均不支持跨会话状态保持，如需连续交互，请自行维护上下文并显式传入 `history` 字段（若模型支持）；  
- 接口调用频率限制为 5 QPS / 账号，突发流量需提前报备。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


