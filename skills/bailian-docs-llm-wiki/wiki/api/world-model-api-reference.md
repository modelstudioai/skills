# world model api reference

世界模型 API 提供面向具身智能与交互式场景的建模能力，支持环境感知、行为规划与多角色协同等核心功能。当前以 HappyOyster 系列模型为主力实现，涵盖 Adventure（探索建模）、Directing（指令编排）和 Acting（动作执行）三类子能力。所有接口均通过标准 HTTP POST 调用，需携带认证 token 与结构化 payload。

## 支持的模型/功能

- **Adventure 模型**：用于动态环境建模与状态推演，适用于游戏、仿真等开放世界场景。详见 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)。
- **Directing 模型**：专注多步任务分解与角色间协作调度，输出结构化指令序列。详见 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。
- **Acting 模型**：执行细粒度动作生成（如肢体控制、对话响应），目前处于邀测阶段，接口规范与权限策略以 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 为准。

> **注意**：原始文档中未明确说明 Acting 模型是否支持批量请求，但 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 的示例请求体含 `batch_size` 字段，而 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 明确声明“不支持 batch 请求”。请以各子模型独立文档为准，避免跨模型复用参数逻辑。

## 关键参数

所有请求共用以下必需参数：
- `model`: 字符串，取值为 `"happyoyster-adventure"` / `"happyoyster-directing"` / `"happyoyster-acting"`
- `input`: 对象，结构依模型类型而异（详见对应 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)）
- `temperature`: 浮点数，范围 `[0.0, 1.0]`，仅 Adventure 和 Directing 支持；Acting 模型固定为 `0.0`（确定性输出）
- `max_output_tokens`: 整数，最大输出长度，各模型默认值不同，建议显式指定

## 使用方式

1. 向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke` 发起 POST 请求  
2. Header 中设置 `Authorization: Bearer <your_api_key>` 和 `Content-Type: application/json`  
3. Body 示例（Adventure 场景）：
```json
{
  "model": "happyoyster-adventure",
  "input": {
    "world_state": {"player_pos": [3,5], "objects": ["key", "door"]},
    "goal": "reach the door"
  },
  "parameters": {
    "temperature": 0.7,
    "max_output_tokens": 512
  }
}
```
完整参数组合与错误码说明请参阅 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中的“请求格式”章节。

## 限制和注意事项

- 单次请求 `input` 总字符数上限为 8192；超过将返回 `400 Bad Request`  
- Acting 模型调用需提前申请邀测权限，未授权调用返回 `403 Forbidden`  
- 所有模型均不支持流式响应（`stream: true` 无效），响应为完整 JSON 对象  
- 时间敏感操作（如实时物理模拟）需自行在客户端处理时序对齐，服务端不保证低延迟——该约束在 [原文标题](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md) 的“性能说明”节中有明确强调

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


