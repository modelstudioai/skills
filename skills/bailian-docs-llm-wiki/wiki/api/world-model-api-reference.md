# world model api reference

世界模型 API 提供对多模态动态环境建模与交互能力的程序化访问，支持场景生成、角色行为编排与实时响应控制。当前以 HappyOyster 系列为主要实现载体，涵盖 Adventure（叙事驱动）、Directing（导演式调控）和 Acting（角色级动作执行）三类核心能力。所有接口均基于 RESTful 设计，需通过 API Key 认证调用。

## 支持的模型/功能

- **Adventure 模型**：面向开放世界叙事，支持长周期状态演化、多角色关系推理与分支剧情生成。适用于游戏引擎集成与互动故事系统。  
- **Directing 模型**：提供高层语义指令解析与全局场景调度能力，如“让雨停、镜头拉远、主角进入警觉状态”。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。  
- **Acting 模型**：聚焦单角色实时动作决策与微表情/肢体语言合成（当前处于邀测阶段），需单独申请权限。其接口规范见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中描述的 `scene_control_level` 参数在 v2.3+ 版本已弃用，应改用 `directive_scope` 字段；旧文档未同步更新，以实际 OpenAPI Schema 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 取值为 `happyoyster/adventure`、`happyoyster/directing` 或 `happyoyster/acting` |
| `input` | object | 是 | 输入结构体，格式依模型类型而异（详见各子文档） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅 Adventure 和 Directing 支持 |
| `max_steps` | integer | 否 | 最大推理步数，范围 1–50；Acting 模型强制要求 ≤10 |

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`  
2. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`  
3. Body 示例（Adventure 调用）：
```json
{
  "model": "happyoyster/adventure",
  "input": {
    "world_state": {"time": "day", "weather": "sunny"},
    "user_input": "推开木门"
  },
  "parameters": {"max_steps": 8}
}
```
完整请求示例与错误码说明请参阅 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。

## 限制和注意事项

- 单次请求最大 `input` 长度为 4096 tokens（按 UTF-8 字符计）；超长输入将被截断并返回 `400 Bad Request`。  
- Acting 模型暂不支持流式响应与 `max_steps > 10`，违反将触发 `422 Unprocessable Entity`。  
- 所有模型均不支持跨会话状态持久化；如需连续交互，请在客户端维护 `session_id` 并显式传入 `input.session_id` 字段（若接口支持）。  
- 当前仅支持 `application/json` 内容类型，`multipart/form-data` 等格式暂未开放。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


