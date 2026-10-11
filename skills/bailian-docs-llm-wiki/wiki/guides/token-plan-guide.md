# token plan guide

Token Plan 是百炼平台为开发者提供的模型调用配额管理机制，用于控制 API 调用量、保障服务稳定性并支持按需弹性伸缩。它适用于不同规模的应用场景，从个人实验到企业级生产部署均可配置对应策略。所有 Token Plan 均基于实际消耗的输入+输出 token 数进行计量，计费与配额均与此强相关。

## 支持的模型/功能

当前 Token Plan 适用于百炼平台全部公开模型（含 Qwen 系列、Qwen2 系列、Qwen3 系列及部分第三方模型），但不支持离线批量推理、模型微调训练任务或私有化部署实例的 token 计量。语音、图像等多模态模型暂未纳入统一 Token Plan 体系，其调用需参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中的例外说明。

## 关键参数

- `max_tokens`：单次请求允许生成的最大 token 数（默认值因模型而异，Qwen3-8B 默认为 8192）  
- `temperature` / `top_p`：不影响 token 消耗量，但影响实际输出长度分布，间接影响配额使用效率  
- `stream`：流式响应不改变总 token 消耗，但会触发多次小粒度配额扣减（每次 chunk 按实际 tokens 扣减）  
- `input_tokens` 与 `output_tokens`：在响应头中以 `x-bailian-input-tokens` 和 `x-bailian-output-tokens` 返回，是配额核算唯一依据，详见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)

> **注意**：文档 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中标注“免费额度每月重置时间为 UTC+0 00:00”，但控制台实际执行为北京时间（UTC+8）00:00，该差异已在 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 的“配额生效时间”章节中修正，请以后者为准。

## 使用方式

1. 登录百炼控制台 → 进入「API 密钥与配额」页面 → 选择目标 API Key → 绑定 Token Plan  
2. 调用时在请求 Header 中携带 `Authorization: Bearer <api_key>` 即可自动启用绑定的 Plan  
3. 如需动态切换 Plan，可通过 `/v1/token-plans/assign` 接口重新分配（需具备 `token_plan:assign` 权限）  
4. 配额余量与实时消耗可通过 `/v1/token-plans/usage` 查询，响应结构与 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中示例一致

## 限制和注意事项

- 单个 API Key 最多绑定 1 个 Token Plan；如需多环境隔离（如 dev/staging/prod），须创建多个 API Key 分别绑定  
- 超出配额后请求将返回 HTTP 429 状态码及 `{"error": {"code": "rate_limit_exceeded", ...}}`，**不会降级为低优先级队列**  
- Coding Plan 作为独立子类，仅适用于 `/v1/coding/*` 路径接口，其 token 计量规则与通用 Plan 不同（例如对代码补全上下文做特殊截断），详情见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)  
- 所有 token 计量均四舍五入到整数，小数部分不累计（例如 1.6 tokens 计为 2 tokens）

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


