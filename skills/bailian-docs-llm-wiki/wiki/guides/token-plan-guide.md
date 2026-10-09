# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设定使用上限并支持多层级权限隔离。开发者可通过 [Token](../concepts/token.md) Plan 实现精细化的用量管控、成本预估和团队协作治理。该机制适用于所有通过百炼 API 接入的模型服务，且与身份认证、配额策略深度集成。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 适用于百炼平台全部公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及客户私有微调模型，但**不适用于直接调用 Model Studio 后台训练任务或离线批量推理作业**。实时流式响应、Function Calling、多轮对话上下文累计计费均纳入 Token Plan 统一计量。具体模型兼容性详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

- `max_tokens`：单次请求允许的最大输出 token 数（硬限制，超限将截断并返回 `400 Bad Request`）  
- `total_quota`：账户/工作空间级月度总 token 配额（单位：千 token），超出后请求将被拒绝  
- `burst_quota`：突发配额（单位：千 token），用于应对瞬时高峰，按小时重置，详情见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)  
- `quota_scope`：配额作用域，支持 `user`、`workspace`、`app` 三级，影响配额继承与共享逻辑  

> **注意**：文档中 `burst_quota` 的默认值在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中标注为 `50k`，但在 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 中明确要求由管理员显式配置，未配置时实际为 `0`。请以团队版文档为准。

## 使用方式

1. 在控制台「API 密钥管理」页为每个 API Key 绑定 Token Plan（支持创建/切换/解绑）  
2. 调用 API 时，无需额外传参，系统自动按绑定 Plan 执行配额校验与扣减  
3. 通过 `/v1/usage/quota` 接口可实时查询当前周期剩余配额（需 `read:quota` 权限）  
4. 配额告警与用量分析需结合 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中的监控模板配置  

## 限制和注意事项

- 单个 API Key 最多绑定 1 个 Token Plan；同一 Plan 可被多个 Key 共享（适用于灰度发布场景）  
- 配额重置时间为每月 1 日 UTC+0 00:00，不支持自定义周期  
- 输入 token 计算包含 system prompt、user message、history messages 全部内容（含 JSON 字符、空格、换行符），具体分词逻辑与模型原生 tokenizer 一致  
- 若请求因配额不足被拒绝，响应头中会携带 `X-RateLimit-Remaining: 0` 和 `X-RateLimit-Reset` 时间戳，建议客户端据此实现退避重试  

> **注意**：[Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 是 Token Plan 的子集特化方案，仅对代码生成类模型（如 Qwen-Coder）生效，其配额独立于通用 Token Plan，不可混用或叠加。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


