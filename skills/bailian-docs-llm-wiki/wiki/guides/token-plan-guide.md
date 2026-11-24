# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为开发者提供的按量计费的模型调用资源包方案，适用于需要灵活控制成本、避免预付费或长期合约约束的场景。它通过预购 [Token](../concepts/token.md) 额度并按实际调用消耗扣减，支持多种大模型 API 调用。本文档汇总关键使用要点，帮助开发者快速接入并合理规划用量。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 当前支持调用以下模型（含基础版与增强版）：  
- Qwen 系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）  
- 其他已接入百炼 Model Hub 的公开模型（需模型页标注“支持 Token Plan”）  

**不支持**：自定义微调模型（Fine-tuned models）、私有部署模型、流式响应中的 `stream_options.include_usage=true` 场景（该参数会额外触发一次用量上报，导致重复扣减）。详情见 [用量与额度](../../raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)。

## 关键参数

调用时需在请求头或参数中显式声明 `x-acs-trace-id`（用于用量归属）及 `x-acs-token-plan-id`（指定使用的 Token Plan ID）。若未传 `x-acs-token-plan-id`，请求将回退至主账号余额支付。  
> **注意**：部分旧版 SDK 示例中误将 `token_plan_id` 作为 query 参数传递，实际应统一置于 HTTP Header；最新行为以 [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md) 为准。

## 使用方式

1. 在百炼控制台「费用中心 → Token Plan」页面购买资源包（支持按 10k / 100k / 1M Token 档位）；  
2. 调用模型 API 时，在请求 Header 中添加：  
   ```http
   x-acs-token-plan-id: tp-xxxxxx
   x-acs-trace-id: trace-xxxxxx  # 建议使用唯一业务 ID，便于用量归因
   ```  
3. 查看实时用量：控制台「用量明细」页或调用 `/api/v1/usage/token-plan` 接口（需对应权限）。完整流程参见 [Token Plan 概览](../../raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。

## 限制和注意事项

- 单个 Token Plan 包仅限一个主账号及其子账号（需已授权）使用，不支持跨账号共享；  
- Token 不可退款、不可转让、有效期为自购买日起 12 个月；  
- 若同时存在多个有效 Token Plan，系统按 `created_time` 降序自动选择最先过期的包优先扣减；  
- 当前不支持在 `batch` 批量调用接口中混用不同 Token Plan ID（单次请求仅允许指定一个 ID）。  
更多合规要求请参考 [权限与使用规范](../../raw/token-plan-user-guide/token-plan-guide/token-plan-permissions-and-usage.md)。

## 来源文档

- [开始使用](../../raw/token-plan-user-guide/token-plan-guide.md)


