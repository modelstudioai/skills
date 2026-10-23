# token plan guide

Token Plan 是百炼平台为模型调用设计的配额管理机制，用于控制 API 调用频次、并发量及总 Token 消耗量。它适用于不同规模的应用场景，支持按模型、调用方式和用户身份进行精细化配额分配。开发者需结合自身业务需求选择合适的 Plan 类型，并在调用时显式声明 `plan` 参数（如适用）。

## 支持的模型/功能

Token Plan 当前覆盖全部百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于自定义训练模型（Fine-tuned Model）或 BYOM（Bring Your Own Model）接入场景**。基础推理、流式响应、Function Calling 均受 Plan 约束；而模型部署、微调任务、向量检索等后台作业不受 Token Plan 限制。详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

- `plan`: 字符串，必填（部分接口默认 fallback 到 `personal`），取值包括 `personal`、`team`、`coding` 等，对应不同配额策略；
- `max_tokens`: 请求级硬上限，不可超过当前 Plan 允许的单次最大输出 Token 数（例如 `personal` 默认为 4096，`coding` 为 8192）；
- `temperature` / `top_p` 等采样参数不影响配额计算，但高 `max_tokens` 值可能触发 Plan 的实时 Token 消耗校验。

> **注意**：原始文档中 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 与 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 对 `concurrency_limit` 的默认值描述不一致（前者写为 5，后者写为 10），实际以控制台「配额中心」实时显示为准，API 返回的 `X-RateLimit-Remaining` 头部为权威依据。

## 使用方式

1. 在 API 请求 Header 中添加 `X-Plan: <plan_name>`（推荐），或在请求 Body 的顶层传入 `"plan": "<plan_name>"`（部分 SDK 支持）；  
2. 若未指定，系统按调用者身份自动 fallback：个人账号默认 `personal`，团队成员默认 `team`（除非被显式赋予更高权限）；  
3. 配额消耗实时统计，可通过 `/v1/usage/token-plan` 接口查询当前周期内剩余 Token 与并发余量。更多最佳实践请参考 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 限制和注意事项

- 同一请求不可跨 Plan 拆分配额（例如不能对 input 和 output 分别指定不同 plan）；  
- Token 计费粒度为整数 Token，按 `input_tokens + output_tokens` 精确累加，空格、标点、特殊字符均计入；  
- Plan 配额按自然日重置（UTC+8），不支持自定义周期；  
- 若请求触发 `429 Too Many Requests`，应检查 `X-RateLimit-Reset` 响应头并实现指数退避，而非重试原请求。详细规则见 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md)。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


