# world model api reference

世界模型 API 提供面向叙事与交互场景的多模态建模能力，支持剧情推演、角色行为生成与环境状态演化等核心任务。当前以 HappyOyster 系列模型为主力实现，覆盖 Adventure（冒险推演）、Directing（导演调度）和 Acting（角色表演）三类子能力。所有接口均通过标准 HTTP POST 调用，需携带认证 token 与结构化 payload。

## 支持的模型/功能

- **Adventure 模型**：用于长程剧情逻辑推演与分支决策，适用于游戏叙事引擎、互动小说等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：负责多角色协同调度、镜头语言生成与节奏控制，常用于虚拟制片与实时演出系统。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**（邀测中）：聚焦单角色细粒度行为建模（含微表情、语气、动作时序），当前仅对白名单用户开放。详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中未明确说明 Acting 模型是否支持流式响应，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确要求 `stream: false`；实际调用中若启用 `stream=true` 将返回 400 错误，建议统一按同步模式使用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input` | object | 是 | 包含 `scene_state`（当前世界快照）、`narrative_context`（上下文文本）、`available_actions`（可选动作列表）等字段，结构依模型类型而异 |
| `max_steps` | integer | 否 | 推演最大步数，默认 5，上限 20（Adventure/Directing）；Acting 模型不支持该参数 |
| `temperature` | number | 否 | 采样温度，范围 [0.1, 1.5]，默认 0.7 |

## 使用方式

1. 构造 JSON 请求体，确保 `input` 字段符合对应模型的 schema（参见各子文档的 `Request Body` 示例）；
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`；
3. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
4. 解析响应中的 `output.result` 字段，其为包含 `next_state`、`generated_action` 和 `confidence` 的对象。

## 限制和注意事项

- 单次请求 `input` 总字符数不得超过 8192（含 JSON 结构开销）；
- Adventure 与 Directing 模型支持批量推演（`batch_size=1..5`），但 Acting 模型暂不支持（见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)）；
- 所有模型均不支持跨会话状态持久化，`scene_state` 必须在每次请求中完整提供；
- 若输入中 `scene_state` 缺失关键字段（如 `characters[].position`），模型将返回 `422 Unprocessable Entity`，而非静默降级。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


