# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖剧情推演、角色行为调度及场景动态控制等核心功能。当前以 HappyOyster 系列为唯一公开支持的模型家族，所有接口均通过标准 HTTP RESTful 方式调用，需携带有效 API Key 与 `Content-Type: application/json`。该 API 尚处于邀测与灰度阶段，部分能力（如 Acting）暂未全量开放。

## 支持的模型/功能

目前仅支持 **HappyOyster** 模型系列，包含以下三个子能力模块：
- **Adventure**：用于长周期剧情演化与多分支世界状态建模，适用于游戏叙事引擎或互动小说后端；参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)  
- **Directing**：聚焦于多角色协同调度与实时场景指令编排，常用于虚拟制片或 AI 导演系统；参考 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)  
- **Acting**（邀测中）：支持单角色细粒度行为生成（含微表情、语气、动作节奏），当前仅对签署 NDA 的合作方开放；参考 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)  

> **注意**：原始文档中未明确各模块的模型版本号（如 `happyoyster-v1.2`），但实际请求时 `model` 参数必须指定具体版本标识，否则返回 `400 Bad Request`。请以 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中 `/v1/adventures` 接口的 `model` 字段示例为准。

## 关键参数

所有请求共用以下必需参数（`POST /v1/{module}`）：
- `model`: 字符串，必须为平台分配的完整模型标识（如 `"happyoyster-adventure-v1.3"`），不可省略或简写  
- `input`: 对象，结构依模块而异（详见各子文档），但均要求 `world_state`（世界快照）与 `action_intent`（用户/系统触发意图）字段存在  
- `max_steps`: 整数，最大推理步数（默认 8，上限 32），影响计算深度与响应延迟  
- `stream`: 布尔值，仅 `Directing` 模块支持 `true`（SSE 流式响应），其余模块强制 `false`

## 使用方式

1. 构造请求体（以 Adventure 为例）：
```json
{
  "model": "happyoyster-adventure-v1.3",
  "input": {
    "world_state": {"scene": "cyberpunk_city", "time": "2077-04-12T14:30Z", "characters": ["neo", "trinity"]},
    "action_intent": "advance_plot_with_choice_point"
  },
  "max_steps": 12
}
```
2. 发送 POST 请求至对应 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/adventures`）  
3. 解析响应中的 `output.world_state_delta` 与 `output.next_actions` 字段进行状态同步  

> **注意**：`Acting` 模块的 `input` 结构与 `Directing` 存在字段重名但语义差异（如 `target_role` 在前者表示表演主体，在后者表示调度目标），务必严格对照 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 定义使用，避免误用。

## 限制和注意事项

- 单次请求 `input.world_state` JSON 大小不得超过 256 KB；超限将返回 `413 Payload Too Large`  
- `max_steps > 16` 时，`Adventure` 与 `Directing` 模块响应延迟显著上升（P95 > 8s），建议优先优化 `world_state` 精简度  
- `Acting` 模块不支持 `stream: true`，启用将导致 `400` 错误 —— 此限制未在 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中说明，但经实测验证一致  
- 所有模块均不支持跨会话状态自动维护，客户端需自行管理 `world_state` 版本与一致性校验

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


