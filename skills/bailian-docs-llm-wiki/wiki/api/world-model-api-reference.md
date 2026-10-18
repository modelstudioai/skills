# world model api reference

世界模型 API 提供面向游戏与交互式叙事场景的[多模态](../concepts/multi-modal.md)建模能力，支持剧情生成、角色行为决策、环境状态演化等核心功能。当前以 HappyOyster 系列模型为主力实现，涵盖 Adventure（冒险叙事）、Directing（导演调度）和 Acting（角色表演）三大子系统。所有接口均通过标准 HTTP POST 调用，遵循 OpenAPI 3.0 规范。

## 支持的模型/功能

- **Adventure 模型**：用于生成动态剧情分支、世界状态演化及玩家意图推理，适用于开放世界 RPG 或文字冒险类应用。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：负责多角色协同调度、镜头语言编排与节奏控制，常用于实时互动影视或虚拟制片流程。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**（邀测中）：提供细粒度角色动作、微表情、语音韵律建模能力，需申请白名单接入。其接口定义与调用约束见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：Acting 模型当前仅支持 WebSocket 长连接流式调用，而 Adventure 和 Directing 均仅支持 RESTful 同步请求——该差异在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的“传输协议”章节中未明确说明，但已在 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 的 v1.2 版本更新日志中确认。

## 关键参数

所有模型共用以下顶层参数（`POST /v1/{model}`）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `scene_state` | object | 是 | 当前世界状态快照，结构依模型类型而异（详见各子文档） |
| `user_input` | string | 否 | 用户最新输入文本，可为空（如仅需状态推演） |
| `max_steps` | integer | 否 | 最大推演步数，默认为 1；Adventure 模型上限为 5，Directing 为 3 |
| `stream` | boolean | 否 | 仅 Acting 模型有效；设为 `true` 时启用流式响应 |

## 使用方式

1. 获取 API Key 并设置 `Authorization: Bearer <key>` 请求头；
2. 根据目标能力选择 endpoint：
   - Adventure：`POST https://dashscope.aliyuncs.com/api/v1/world-model/adventure`
   - Directing：`POST https://dashscope.aliyuncs.com/api/v1/world-model/directing`
   - Acting：`wss://dashscope.aliyuncs.com/api/v1/world-model/acting`（仅 WebSocket）
3. 构造 JSON body，确保 `scene_state` 符合对应模型的 schema（参见各 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `SceneState` 定义）；
4. 发起请求并处理响应（同步接口返回 `200 OK` + JSON；Acting 流式响应按 SSE 格式分块推送）。

## 限制和注意事项

- 单次请求 `scene_state` 总大小不得超过 256 KB（JSON 序列化后）；
- Adventure 与 Directing 模型不支持跨会话状态保持，需由客户端显式传递完整上下文；
- Acting 模型暂不支持 `max_steps > 1`，设置将被忽略；
- 所有模型对中文输入优化最佳，英文输入可能降低剧情连贯性与角色一致性；
- 接口调用频率限制为 10 QPS / key（Acting 模型按连接数计费，不计入 QPS 限额）。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


