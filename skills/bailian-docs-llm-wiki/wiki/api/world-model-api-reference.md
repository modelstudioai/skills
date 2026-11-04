# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖冒险（Adventure）、导演（Directing）和表演（Acting）三类核心功能。该 API 当前以邀测形式开放，需申请权限后使用。所有接口均基于 RESTful 设计，支持 JSON 请求/响应格式，并遵循统一的身份认证机制。

## 支持的模型/功能

世界模型当前提供以下三类功能模块，分别对应不同创作阶段：

- **Adventure**：用于生成动态世界观、角色关系图谱与剧情分支逻辑，适用于游戏叙事或互动小说初始化；  
- **Directing**：支持多角色协同行为编排、镜头语言调度与节奏控制，常用于虚拟制片或AI导演场景；  
- **Acting**（邀测中）：提供角色实时情绪建模、台词微调与肢体动作生成，依赖高保真角色状态上下文。  
> **注意**：[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 中标注的 `v1.2` 接口路径与 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的通用认证头字段名不一致（前者要求 `X-World-Auth`，后者为 `X-Model-Auth`），实际调用应以 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 的 `v1.3` 规范为准。

## 关键参数

所有请求共用以下必需参数：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 必填，取值为 `happyoyster/adventure`、`happyoyster/directing` 或 `happyoyster/acting` |
| `input` | object | 必填，结构依模型类型而异，详见各子文档输入 schema |
| `stream` | boolean | 可选，默认 `false`；仅 `directing` 和 `acting` 支持流式响应 |

此外，`adventure` 模型支持 `max_world_depth`（整数，范围 1–5），`directing` 模型支持 `scene_duration_sec`（浮点数，≥0.5），具体约束见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。

## 使用方式

1. 向 `https://dashscope.aliyuncs.com/api/v1/world-model` 发起 POST 请求；  
2. 在 Header 中携带 `Authorization: Bearer <api_key>` 及 `Content-Type: application/json`；  
3. Body 示例（Adventure）：
```json
{
  "model": "happyoyster/adventure",
  "input": {
    "setting": "赛博朋克都市",
    "characters": ["义体医生", "失忆黑客"]
  },
  "parameters": {"max_world_depth": 3}
}
```
完整请求示例与错误码说明请参阅 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 的“调用示例”章节。

## 限制和注意事项

- 单次请求 `input` 总字符数上限为 8192；`acting` 模块额外限制上下文窗口 ≤ 2048 tokens；  
- `adventure` 输出结果不可直接用于实时渲染，需经后处理校验一致性；  
- 所有模型均不支持跨会话状态保持，如需长程叙事连贯性，须由客户端维护 `world_id` 并显式传入；  
- 邀测中的 `acting` 功能暂不支持批量生成，且响应延迟波动较大（P95 ≤ 3.2s），生产环境部署前务必压测。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


