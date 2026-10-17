# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设定使用上限并支持按需升级。开发者可通过 [Token](../concepts/token.md) Plan 精细管理不同环境（如开发、测试、生产）的调用量，避免意外超限或费用激增。该机制适用于所有通过百炼 API 接入的模型服务。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 适用于百炼平台全部公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及自定义微调模型，但**不适用于离线批量推理任务**（需单独申请配额）。实时流式响应、Function Calling、多轮对话上下文累计计费均纳入 Token Plan 统一计量。Coding Plan 作为子类，专用于代码生成类模型（如 Qwen2.5-Coder），其 token 计费规则与主 Plan 独立，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `max_tokens_per_request`：单次请求最大输出 token 数，硬性截断阈值（默认 2048，最高可设 8192）  
- `daily_quota`：账户级日 token 总配额（单位：千 token），影响所有 API 调用  
- `burst_limit`：每秒突发请求数（TPS），与 token 消耗解耦，仅限流量整形  
- `model_specific_quota`：可为指定模型（如 `qwen-max`）单独设置日配额，优先级高于 `daily_quota`  

参数配置生效后立即作用于新请求，历史请求不追溯调整。详细参数语义请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 使用方式

1. 登录百炼控制台 → 进入「配额管理」→ 选择目标项目  
2. 点击「创建 Token Plan」，选择版本（个人版/团队版）并填写配额值  
3. 在 API 请求 Header 中添加 `X-Request-ID`（可选）和 `X-Model-Plan-ID`（绑定计划 ID）  
4. 调用时若未显式指定 Plan，系统自动匹配项目默认 Plan；若无默认，则使用账户级 fallback Plan  

团队版支持成员粒度配额继承与覆盖，具体策略见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)。个人版用户无法设置 `model_specific_quota`，此限制已在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中明确说明。

## 限制和注意事项

- 单日 quota 超限后，后续请求将返回 HTTP 429 及 `{"error": {"code": "quota_exceeded"}}`  
- Token 计费以实际消耗为准（输入 + 输出 token），非请求次数；空格、标点、特殊字符均计入  
- **注意**：原始文档中 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 提到“配额重置时间为 UTC+0 凌晨”，但控制台实际采用北京时间（UTC+8）每日 00:00 重置，以控制台显示为准  
- **注意**：[玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中示例使用的旧版 Header 字段 `X-Plan-ID` 已废弃，当前必须使用 `X-Model-Plan-ID`  
- 配额不可跨项目共享，且不支持实时临时扩容（需提前申请审批）

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


