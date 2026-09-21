# world model api reference

世界模型 API 提供面向叙事与交互式内容生成的专用能力，涵盖剧情推演、角色行为调度、场景动态构建等核心功能。当前以 HappyOyster 系列为主要实现，分 Adventure（冒险推演）、Directing（导演调度）和 Acting（角色表演，邀测中）三类接口。所有接口均基于统一认证与配额体系，需通过百炼平台申请对应模型权限。

## 支持的模型/功能

- **Adventure 模型**：用于长周期剧情状态演化、多分支路径预测与世界状态一致性维护，适用于游戏叙事引擎、互动小说等场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：聚焦于多角色协同调度、镜头语言生成、节奏控制与冲突触发，常用于虚拟制片或实时演出系统。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**（邀测中）：支持单角色细粒度行为建模（含微表情、语气、动作时序），当前仅对白名单用户开放。其接口规范见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

> **注意**：原始文档中未明确说明 Acting 模型是否已支持流式响应，但 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确要求 `stream=false`；若在 Acting 接口中启用 `stream=true`，将返回 400 错误——该不一致行为已在内部工单 #WM-218 中记录，预计 v1.3 版本统一。

## 关键参数

所有世界模型接口共用以下必需参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input.world_state` | object | 是 | JSON 格式的世界初始状态快照，结构依模型类型而异（参见各子文档） |
| `input.prompt` | string | 否 | 补充指令，优先级高于 `world_state` 中的隐式约束 |
| `parameters.max_steps` | integer | 否 | 最大演化步数（Adventure 默认 5，Directing 默认 1，Acting 不支持） |

> **注意**：`max_steps` 在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中定义为“单次请求内最多执行的状态转移次数”，而非总 token 数；部分旧版 SDK 示例误将其等同于 `max_tokens`，请以该文档为准。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头；
2. **端点**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/<model_name>`；
3. **请求体**：JSON 格式，必须包含 `input` 字段（含 `world_state` 和可选 `prompt`），`parameters` 为顶层可选对象；
4. **响应**：成功时返回 `200 OK`，`output.steps[]` 包含每步演化结果；失败时返回标准错误码及 `error.message`。

## 限制和注意事项

- 单次请求 `world_state` 大小上限为 256 KB，超限将返回 `413 Payload Too Large`；
- Adventure 模型单次调用最多生成 20 步演化，超过 `max_steps` 将截断并标记 `"truncated": true`；
- Acting 模型暂不支持 `system_prompt` 或历史对话上下文，所有角色行为必须完全由 `world_state` 显式定义；
- 所有世界模型接口均**不支持重试幂等性标识（如 `idempotency_key`）**，重复请求可能产生不同演化路径——此设计已在 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 的“行为确定性”章节中明确说明。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


