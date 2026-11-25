# token plan personal

个人版 Token Plan 是面向独立开发者和小型项目的按量计费方案，提供基础模型调用额度与轻量级管理能力。该计划不包含企业级 SLA、专属支持或私有化部署选项，适用于原型验证、学习实验及低频生产场景。详细权益说明请参见 [个人版](../../raw/token-plan-user-guide/token-plan-personal.md)。

## 支持的模型/功能

- 支持调用百炼平台全部公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio），但**不支持**自定义微调模型部署或私有模型托管；
- 支持标准 API 调用（`/v1/chat/completions`）、批量推理（`/v1/batch`）及基础流式响应；
- 不支持模型热更新、版本灰度、多租户隔离等企业功能；  
- 详细模型兼容性列表见 [个人版](../../raw/token-plan-user-guide/token-plan-personal.md) 中的“Harness 权益”子文档。

## 关键参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `quota_monthly` | 每月总 Token 配额（输入 + 输出） | 100 万 tokens |
| `rate_limit_rpm` | 每分钟请求次数上限 | 60 RPM |
| `rate_limit_tpm` | 每分钟 Token 处理上限 | 10,000 TPM |
| `max_context_length` | 单次请求最大上下文长度（依模型而定） | 与所选模型原生限制一致 |

> **注意**：部分旧版文档中将 `max_context_length` 错标为固定 4096，实际以 [个人版](../../raw/token-plan-user-guide/token-plan-personal.md) 所引用的 `token-plan-harness-benefits.md` 中最新模型规格为准。

## 使用方式

1. 登录百炼控制台 → 进入「计费与配额」→ 选择「个人版」并完成开通；
2. 在 API 请求头中携带有效 `Authorization: Bearer <your_api_key>`（该 Key 绑定至个人版配额池）；
3. 调用时无需额外指定 plan 参数，系统自动按账户所属 plan 扣减配额；
4. 配额使用情况可通过 `/v1/usage` 接口实时查询，或在控制台「用量明细」页查看。

## 限制和注意事项

- 配额按自然月重置，不累计、不可转让、不可退款；
- 同一阿里云主账号下仅允许一个活跃的个人版实例；
- 超出配额后 API 返回 `429 Too Many Requests`，错误体中含 `{"code":"QUOTA_EXCEEDED"}`；
- 若需更高配额或稳定性保障，应升级至专业版或企业版 —— 具体迁移路径详见 [个人版](../../raw/token-plan-user-guide/token-plan-personal.md) 的「订阅与权益」章节。

## 来源文档

- [个人版](../../raw/token-plan-user-guide/token-plan-personal.md)


