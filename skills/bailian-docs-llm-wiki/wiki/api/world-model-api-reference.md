# world model api reference

世界模型 API 提供面向具身智能与交互式场景的建模能力，支持动态环境理解、行为规划与多角色协同推演。当前以 HappyOyster 系列模型为核心，覆盖冒险（Adventure）、导演（Directing）和表演（Acting）三类任务范式。API 设计遵循 OpenAPI 3.0 规范，所有接口均需通过百炼平台鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态演化建模，支持基于自然语言指令的环境变迁预测与多步因果链推理。  
- **Directing 模型**：面向叙事结构控制，可生成角色调度方案、节奏编排与冲突触发逻辑，适用于游戏剧情引擎或虚拟制片流程。  
- **Acting 模型**（邀测中）：提供细粒度角色行为生成能力，包括微表情、动作时序与对话情绪耦合输出，当前仅对白名单用户开放。  
以上模型能力详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)、[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 和 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure` / `happyoyster-directing` / `happyoyster-acting` |
| `input` | object | 是 | 包含 `scene_state`（当前世界快照）、`intent`（用户指令或目标）等字段，结构依模型而异 |
| `max_steps` | integer | 否 | 推演最大步数，默认 5；Adventure 模型上限为 20，Directing 为 10 |
| `stream` | boolean | 否 | 是否启用流式响应（仅 Adventure 和 Directing 支持），默认 `false` |

> **注意**：原始文档中 `happyoyster-acting` 的 `max_steps` 描述为“无限制”，但实际服务端强制限制为 8 步，以避免长序列退化——该不一致已在 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 的 v1.2 补丁中修正。

## 使用方式

1. 在百炼控制台开通「世界模型」服务并获取 API Key；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/world-models`；  
3. 设置请求头：`Authorization: Bearer <YOUR_API_KEY>`，`Content-Type: application/json`；  
4. 按所选模型填充 `input` 字段（参考各子模型 OpenAPI 文档中的 `RequestBody` 示例）；  
5. 解析响应体中的 `output.steps[]`（Adventure/Directing）或 `output.behavior_sequence`（Acting）。

## 限制和注意事项

- 单次请求 `input.scene_state` 文本长度上限为 8192 字符，超长需预压缩或分块提交；  
- Acting 模型暂不支持 `stream=true`，启用将返回 HTTP 400 错误；  
- 所有模型均要求 `input` 中至少包含一个有效 `scene_state` 对象，空对象或缺失字段将触发 422 校验失败；  
- 实际调用前请务必查阅最新版 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)，其中包含字段级校验规则与错误码映射表。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


