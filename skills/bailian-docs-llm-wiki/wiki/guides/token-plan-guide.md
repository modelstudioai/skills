# token plan guide

Token Plan 是百炼平台为开发者提供的按量计费的模型调用资源包方案，适用于需要灵活控制成本、避免预付费或长期承诺的场景。它通过预购 Token 额度并按实际调用消耗扣减，支持多种大模型 API 调用。本文档汇总关键使用要点，帮助开发者快速接入并合理规划用量。

## 支持的模型与功能

Token Plan 当前支持以下模型调用：
- 通义千问系列：`qwen-max`、`qwen-plus`、`qwen-turbo`（含 `qwen-turbo-20240919` 等迭代版本）
- 其他已接入百炼模型服务的 LLM（如 `qwen-vl-plus`、`qwen-audio`），但**不支持训练、微调、向量检索等非推理类功能**  
- 仅限同步 API 调用（`/v1/chat/completions`、`/v1/embeddings` 等标准 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）

> **注意**：部分旧版文档中提及支持 `qwen-7b-chat` 的 Token Plan 调用，但该模型已于 2024 年 8 月起下线公共 API 接入，实际不可用。请以 [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md) 中最新支持模型列表为准。

## 关键参数

调用时需在请求头或参数中显式声明 Token Plan 上下文：
- `x-bailian-token-plan-id`: 必填，购买后获得的唯一 Plan ID（格式如 `tp-abc123`）
- `x-bailian-token-plan-type`: 可选，值为 `prepaid`（默认）或 `postpaid`；后者需单独开通权限  
- 请求体中 `model` 字段必须与所购 Plan 绑定的模型严格一致（大小写敏感）

Token 扣减规则详见 [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)，其中明确说明：输入/输出 Token 均按 UTF-8 字节级编码统计，系统自动四舍五入到整数 Token。

## 使用方式

1. 在百炼控制台「费用中心 → Token Plan」完成购买（支持按 10k / 100k / 1M Token 档位选购）  
2. 获取 `token_plan_id`，并在 API 请求头中添加：  
   ```http
   x-bailian-token-plan-id: tp-abc123
   ```
3. 正常发起模型请求（无需修改 payload 结构），系统自动校验 Plan 有效性并扣减余额  
4. 余额不足时返回 `402 Payment Required`，错误码 `TOKEN_PLAN_INSUFFICIENT_BALANCE`

详细操作步骤和调试技巧见 [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。

## 限制和注意事项

- 单个 Token Plan 仅绑定一个模型，不可跨模型混用（例如 `qwen-turbo` Plan 不能用于 `qwen-plus`）  
- 不支持并发共享：同一 `token_plan_id` 在高并发下可能因余额检查竞争导致偶发 `429 Too Many Requests`，建议按业务粒度拆分 Plan  
- 过期策略：购买后 365 天内有效，过期未用完自动作废，不支持延期或退款  
- 用量查询：可通过 `/api/v1/token-plan/usage` 接口实时获取剩余 Token 数，响应字段 `remaining_tokens` 为最终可信值  

> **注意**：[Token Plan 常见问题](../../raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md) 中关于“可叠加使用多个 Plan”的描述已过时；自 v2.3.0 API 版本起，单次请求仅允许指定一个 `x-bailian-token-plan-id`，多 Plan 场景需由客户端自行路由。

## 来源文档

- [开始使用](../../raw/token-plan-user-guide/token-plan-guide.md)


