# token plan guide

Token Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设定使用上限并支持按需升级。开发者可通过 Token Plan 精细管理不同环境（如开发、测试、生产）的调用量，避免意外超限或费用激增。该机制适用于所有通过百炼 API 接入的模型服务。

## 支持的模型/功能

Token Plan 适用于百炼平台全部公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及自定义微调模型，但**不适用于离线批量推理任务**（需单独申请配额）。实时流式响应、Function Calling、多轮对话上下文累计计费均纳入 Token Plan 统一计量。Coding Plan 作为子集，专用于代码生成类模型（如 Qwen2.5-Coder），其 token 计费规则与主 Plan 独立，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `max_tokens`：单次请求允许的最大输出 token 数（默认 2048，可调至 8192）  
- `total_quota`：账户/工作空间级月度总 token 配额（单位：千 token）  
- `burst_ratio`：突发流量倍率（默认 1.5×，最高 3×，仅限团队版）  
- `model_specific_quota`：可为指定模型（如 `qwen-max`）单独设置配额，优先级高于 `total_quota`  

> **注意**：原始文档中 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 将 `burst_ratio` 描述为“按小时重置”，但最新行为已改为“按自然日重置”，请以控制台实时配额水位为准。

## 使用方式

1. 登录百炼控制台 → 进入「配额管理」→ 选择目标工作空间  
2. 点击「创建 Token Plan」，选择版本（个人版/团队版）并配置 `total_quota`  
3. 调用 API 时，在请求头中显式声明 `X-Model-Quota-ID: <plan_id>` 即可绑定计费策略  
4. 如需动态切换 Plan，可在 SDK 初始化时传入 `quota_id` 参数（Python SDK v3.2+ 支持）  

详细配置示例见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)，常见场景模板参考 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md)。

## 限制和注意事项

- 个人版仅支持单工作空间、无 burst 能力、不可跨模型拆分配额  
- 团队版支持配额继承（子工作空间自动继承父级 80% 配额），但需手动开启「配额下放」开关  
- 所有 Plan 均**不覆盖模型本身的输入长度限制**（如 `qwen-turbo` 最大 context 为 8K tokens）  
- 当 `total_quota` 耗尽时，API 返回 HTTP 429 及错误码 `QUOTA_EXCEEDED`，此时需等待下月重置或手动扩容  

> **注意**：[个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档未说明配额重置时间，实际为每月 1 日 UTC+0 00:00 自动重置；该信息已在 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 中明确，建议以团队版文档为准。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


