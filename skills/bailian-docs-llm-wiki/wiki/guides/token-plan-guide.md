# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的配额管理机制，用于控制 API 调用的 token 消耗总量与速率。它适用于不同规模的应用场景，支持按模型、调用路径和用户角色进行精细化配额分配。开发者需结合自身业务流量特征选择合适 plan 类型，并在调用时显式声明 `plan` 参数以生效配额策略。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入通道。基础文本生成、流式响应、Function Calling 和多轮对话上下文管理均受 [Token](../concepts/token.md) Plan 控制；但模型微调训练任务、Embedding 批量计算、以及 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 所定义的代码补全专用通道需使用独立配额体系，不纳入通用 Token Plan 统计。

## 关键参数

- `plan`: 必填字符串，取值包括 `"personal"`、`"team"`、`"team-pro"`（详见 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 与 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档）  
- `max_tokens`: 可选整数，用于单次请求级硬限流（优先级高于 plan 总配额）  
- `timeout_ms`: 建议设置，避免因 plan 配额耗尽导致长等待（参考 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的超时建议）

> **注意**：文档中提及的 `"free"` plan 已于 v2.3 版本下线，所有新创建应用默认启用 `"personal"` 作为最小可用 plan，旧文档中关于 `"free"` 的说明已过时。

## 使用方式

在 API 请求 Header 中添加 `X-Qwen-Plan: <plan-name>`，例如：

```http
POST /v1/chat/completions HTTP/1.1
Host: dashscope.aliyuncs.com
X-Qwen-Plan: team-pro
Authorization: Bearer YOUR_API_KEY
```

SDK 调用时需通过 `params.plan` 显式传入（Python SDK v3.10+ 支持），未指定时将回退至应用默认 plan。配额消耗实时计入账户维度，可通过控制台「用量中心」或 `/v1/usage` 接口查询剩余 token 数。

## 限制和注意事项

- 单个 plan 实例每秒最大并发请求数为 50，超出将返回 `429 Too Many Requests`  
- plan 配额不可跨模型共享（例如 `qwen-max` 与 `qwen-plus` 的 token 消耗分别计费）  
- 流式响应中，`usage` 字段仅在 final chunk 返回完整 token 统计，中间 chunk 不触发配额扣减  
- 若同时配置了 `X-Qwen-Plan` 和 `X-Qwen-Rate-Limit`，后者将被忽略——Token Plan 已内置速率控制逻辑  

> **注意**：[玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中推荐的“动态 plan 切换”方案在 v3.0+ 版本中存在兼容性问题，当前仅支持请求级静态绑定，不支持运行时 runtime plan 变更。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


