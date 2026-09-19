# world model api reference

世界模型 API 提供面向具身智能与交互式叙事场景的建模能力，支持环境模拟、角色行为编排与动态剧情生成。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（探索建模）、Directing（叙事调度）和 Acting（角色实时动作生成）三类核心能力。所有接口均通过标准 HTTP RESTful 方式调用，需携带有效 API Key 与模型标识。

## 支持的模型/功能

- **Adventure 模型**：用于构建可交互的三维/拓扑环境状态空间，支持动态障碍更新、路径可达性查询与事件触发条件注册。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：负责多角色叙事节奏控制、冲突生成与分支剧情决策，输出结构化导演指令（如 `{"scene_transition": "cut_to", "focus_actor": "A"}`）。该能力文档见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**（邀测中）：基于角色状态与导演指令生成细粒度动作序列（含时序、姿态、语音文本），当前仅对白名单用户开放。使用说明请参阅 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input` | object | 是 | 模型特定输入结构，详见各子文档中的 `request body` 示例 |
| `stream` | boolean | 否 | 仅 Directing 和 Acting 支持流式响应（`true` 时返回 SSE）；Adventure 不支持流式 |
| `max_tokens` | integer | 否 | 默认 1024；Acting 模型建议不超过 512，避免动作序列过长导致时序错乱 |

> **注意**：原始文档中 Adventure 接口描述曾提及 `stream=true` 可启用增量环境更新，但最新服务端已移除该支持——实际调用将忽略该参数并返回完整状态快照。请以 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 当前版本为准。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`  
2. 设置 Header：`Authorization: Bearer YOUR_API_KEY`，`Content-Type: application/json`  
3. Body 示例（Adventure）：
   ```json
   {
     "model": "happyoyster-adventure",
     "input": {
       "current_location": "room_203",
       "observed_objects": ["door_north", "chest_locked"]
     }
   }
   ```
4. 解析响应中的 `output.state`（Adventure）、`output.directives`（Directing）或 `output.actions`（Acting）

## 限制和注意事项

- 单次请求最大 `input` 大小为 8KB；超过将返回 `400 Bad Request`  
- Acting 模型调用需提前申请邀测权限，未授权调用返回 `403 Forbidden`  
- 所有模型均不支持跨会话状态持久化，需由客户端维护 world state 并在每次请求中显式传入必要上下文  
- > **注意**：[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中示例使用的 `session_id` 字段已于 v2.3 接口升级后废弃，新版本应使用 `context_hash` 进行会话关联，旧字段将被静默忽略

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


