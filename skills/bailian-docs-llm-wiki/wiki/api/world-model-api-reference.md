# world model api reference

世界模型 API 提供对多模态世界建模能力的程序化访问，支持场景理解、动态推演与行为生成等核心功能。当前以 HappyOyster 系列为主要实现，涵盖 Adventure（探索推演）、Directing（策略调度）和 Acting（具身动作生成）三类子模型。该接口面向需要构建智能体环境交互逻辑的开发者，需通过百炼平台统一鉴权调用。

## 支持的模型/功能

- **Adventure 模型**：用于开放世界状态推演与因果链预测，适用于游戏、仿真等长程决策场景。  
- **Directing 模型**：专注多智能体协作调度与目标分解，输出结构化指令序列。  
- **Acting 模型**：处于邀测阶段，提供细粒度动作生成与物理约束校验能力，详见 [Acting Open API参考（邀测中）](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference.md)。  

> **注意**：[Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 与 [Directing Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference.md) 中关于 `max_step` 参数的默认值描述不一致（前者为 5，后者为 10），实际调用时请以请求响应中的 `x-ratelimit-remaining` 头及错误码 `422` 的提示为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`happyoyster-adventure`、`happyoyster-directing` 或 `happyoyster-acting`（邀测白名单专用） |
| `input` | object | 是 | 包含 `scene`（场景快照）、`goal`（目标描述）、`history`（可选上下文）等字段，结构详见各子模型文档 |
| `temperature` | number | 否 | 控制输出随机性，范围 [0.0, 1.0]，默认 0.7 |
| `max_tokens` | integer | 否 | 响应最大 token 数，Adventure/Directing 默认 2048，Acting 默认 512 |

## 使用方式

1. 通过百炼控制台申请对应模型的 API Key；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`；  
3. 在 `Authorization` Header 中携带 `Bearer <API_KEY>`；  
4. 请求体为 JSON，`input` 字段需严格遵循各子模型定义的 schema —— 参考 [Adventure Open API参考](../../raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference.md) 中的 `InputSchema` 示例。

## 限制和注意事项

- 单次请求 `input.scene` 文本长度上限为 8192 字符，图像输入暂不支持；  
- Acting 模型仅对已获邀测权限的项目开放，未授权调用将返回 `403 Forbidden`；  
- 所有模型均不支持流式响应（`stream: true` 将被忽略），务必按完整响应解析；  
- 错误码 `429` 表示超出配额，配额详情请查阅平台控制台「用量管理」页。

## 来源文档

- [世界模型](../../raw/model-api-reference/world-model-api-reference.md)


