# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用频次、并发量及总 token 消耗量。开发者需根据业务场景选择对应计划，并在请求中显式声明 `plan` 参数以生效配额策略。该机制与模型选型、请求参数强耦合，配置错误将导致 403 或 429 错误。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入通道。**不支持**自定义训练模型（Fine-tuning Job）或私有部署实例的 token 配额管理。具体兼容性请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中的“适用模型列表”章节。Coding Plan 作为独立子类，仅适用于 `/v1/coding/completions` 接口，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `plan`: 字符串，必填。取值包括 `personal`、`team`、`coding`；大小写敏感，非法值将被拒绝。
- `max_tokens`: 整数，可选。若指定，将覆盖 plan 默认的单次响应 token 上限（但不得超过 plan 允许的硬上限）。
- `temperature`、`top_p` 等采样参数不受 plan 影响，但高采样强度可能加速 token 消耗，间接触发配额限制。

> **注意**：原始文档 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中声明 `personal` plan 支持 5 QPS，而 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 示例代码中实际按 3 QPS 实现——请以控制台实时配额页或 `/v1/plans` API 返回值为准，文档存在滞后。

## 使用方式

1. 在 API 请求 Header 中添加 `X-Qwen-Plan: <plan_name>`（推荐），或  
2. 在请求 Body 的 JSON 中嵌入 `"plan": "<plan_name>"`（仅限 `/v1/chat/completions` 等标准接口）。  
示例（cURL）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Qwen-Plan: team" \
  -d '{"model":"qwen-max","messages":[{"role":"user","content":"hello"}]}'
```
详细参数组合与调试建议见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 限制和注意事项

- 同一请求**不可混用多个 plan**；若同时传 `X-Qwen-Plan` 和 body 内 `plan`，以 header 为准。
- plan 配额按自然日重置（UTC+8 00:00），不支持手动刷新或跨日累积。
- 免费额度仅对新注册用户首月有效，续订后需绑定支付方式；未绑定时调用将直接失败，而非降级至基础 plan。
- 团队版成员继承团队 plan，但无法单独升级个人 plan；如需差异化配额，请使用 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 的子账号隔离机制。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


