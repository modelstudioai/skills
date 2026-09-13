# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为开发者提供的资源配额管理机制，用于控制模型调用的 token 消耗量与频次。它适用于不同规模的应用场景，支持按需配置、实时监控和灵活升降级。合理规划 [Token](../concepts/token.md) Plan 可有效平衡成本、性能与稳定性。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖百炼平台全部公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及部分专属模型，但**不适用于通过 `model_type=custom` 部署的私有模型**。推理 API（`/v1/chat/completions`）、批量异步任务（`/v1/batch/invoke`）和流式响应均受其约束；而模型微调（Fine-tuning）任务、向量检索（`/v1/embeddings`）和知识库索引构建则独立计费，不受 Token Plan 限制。详见 [Token Plan 概述](https://help.aliyun.com/zh/model-studio/token-plan-overview) —— 该文档明确指出“Token Plan 仅作用于 inference 类请求”。

## 关键参数

- `max_tokens_per_request`：单次请求最大输出 token 数，硬性截断阈值（默认 2048，最高可设 8192）  
- `tokens_per_minute`：每分钟总 token 配额（含 input + output），超限后请求将返回 `429 Too Many Requests`  
- `concurrent_requests`：最大并发请求数（影响吞吐，与 token 配额正交）  
- `burst_ratio`：突发流量系数（1.0–3.0），允许短时超额消耗（需在 [进阶配置](https://help.aliyun.com/zh/model-studio/token-plan-best-practice) 中启用并配置窗口期）

> **注意**：原始文档 [Token Plan 概述](https://help.aliyun.com/zh/model-studio/token-plan-overview) 将 `burst_ratio` 描述为“基于滑动窗口的弹性扩容”，但 [进阶配置](https://help.aliyun.com/zh/model-studio/token-plan-best-practice) 明确要求必须配合 `burst_window_seconds` 使用，否则 burst 不生效。实际配置时请以 [进阶配置](https://help.aliyun.com/zh/model-studio/token-plan-best-practice) 为准。

## 使用方式

1. 在控制台「配额管理」→「Token Plan」中创建计划，选择版本（个人版/团队版）  
2. 调用 API 时，在请求 Header 中显式声明 `X-DashScope-Token-Plan: <plan_id>`（未声明则走默认 plan）  
3. 通过 `/v1/usage/token-plan` 接口实时查询剩余配额与历史消耗（支持按小时粒度聚合）  
4. 如需动态切换 plan，可在 SDK 初始化时传入 `token_plan_id` 参数（Python SDK v3.12+ 支持），参考 [玩法攻略](https://help.aliyun.com/zh/model-studio/token-plan-playbooks) 中的 A/B 测试示例。

## 限制和注意事项

- 个人版 Token Plan 不支持跨账号共享，团队版需主账号授权子账号使用  
- 所有配额统计以服务端解析后的 token 数为准（例如：`"Hello, world!"` 的 input tokens 为 3，非字符数）  
- 若同时配置了 Coding Plan，其配额与 Token Plan **完全隔离、互不影响**（见 [Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan-guide) 文档说明）  
- 修改 plan 配置后，新规则**立即生效**，但已发起的长连接流式响应仍按旧配额执行至结束  

> **注意**：[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal) 文档称“升级团队版后历史用量自动清零”，但 [团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-edition) 明确说明“用量数据按 plan 实例持久化，升级不重置”。实际行为以 [团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-edition) 为准，建议通过 `/v1/usage/token-plan?plan_id=xxx` 主动校验。

请始终以 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 中的链接文档为最新依据，平台策略更新可能未同步至本 Wiki。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


