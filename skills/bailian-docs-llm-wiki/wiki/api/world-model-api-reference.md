# world model api reference

世界模型 API 提供面向交互式叙事与智能体行为编排的底层能力，支持冒险生成、导演调度、角色执行等多阶段建模。当前以 HappyOyster 系列模型为核心实现，各模块通过标准化 OpenAPI 接口暴露。该接口集处于持续迭代中，部分功能仍处于邀测阶段。

## 支持的模型/功能

- **Adventure（冒险生成）**：基于场景上下文生成连贯的叙事路径与环境状态演化，适用于游戏关卡、教育模拟等场景。  
- **Directing（导演调度）**：协调多智能体行为时序、资源分配与冲突消解，输出可执行的调度指令序列。  
- **Acting（角色执行）**：驱动单智能体完成具体动作（如对话响应、物理交互），目前为[Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)，需申请权限后使用。

> **注意**：原始文档中将 Acting 标注为“邀测中”，但[Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md)与[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)未注明邀测状态，建议以实际 API 文档返回的 `403` 或 `feature_not_enabled` 错误码为准。

## 关键参数

所有端点共用以下基础参数（详见各子文档）：
- `model`: 必填，取值为 `happyoyster-adventure-v1`、`happyoyster-directing-v1` 或 `happyoyster-acting-v1`；  
- `input`: JSON 对象，结构依模型类型而异（如 Adventure 要求 `world_state` 和 `goal` 字段）；  
- `stream`: 布尔值，仅 Acting 支持流式响应，其余模型暂不支持；  
- `max_steps`: 仅 Directing 支持，限制调度步数上限，默认 50。

## 使用方式

1. 通过百炼平台获取 API Key 并配置 `Authorization: Bearer <api_key>` 请求头；  
2. 向对应端点发送 POST 请求（如 `/v1/models/happyoyster-adventure-v1:generate`）；  
3. 解析响应中的 `output` 字段（结构化 JSON）或 `error` 字段（含 `code` 与 `message`）。  
完整请求示例与错误码说明请参阅[Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md)。

## 限制和注意事项

- 单次请求 `input` 总长度不得超过 8192 字符（UTF-8 编码）；  
- Adventure 与 Directing 模型最大响应延迟为 15 秒，超时将返回 `504 Gateway Timeout`；  
- Acting 模型对输入 `action_context` 的语义一致性要求严格，无效上下文可能导致 `422 Unprocessable Entity`；  
- 所有模型均不支持跨会话状态保持，需由调用方自行维护 `world_state` 或 `session_id`。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


