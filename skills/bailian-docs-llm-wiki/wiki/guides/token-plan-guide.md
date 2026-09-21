# token plan guide

Token Plan 是百炼平台为模型调用设计的配额管理机制，用于控制 API 调用频次、并发量及总 token 消耗量。它适用于不同规模的应用场景，支持按模型、调用方式（同步/异步）、请求来源（API Key / App ID）进行精细化配额分配。开发者需结合业务负载合理配置，避免因超限导致请求被拒绝。

## 支持的模型/功能

Token Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型），并支持以下功能维度：
- 同步推理（`/v1/chat/completions`）、异步任务（`/v1/async-tasks`）、批量推理（`/v1/batch`）
- 流式响应（`stream=true`）按实际返回 token 计费
- Embedding、Rerank、Text-to-Speech 等非生成类能力也纳入统一 token 配额体系  
详细支持列表请参见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `max_tokens` | 单次请求允许的最大输出 token 数（硬限制） | `2048` |
| `rate_limit` | 每秒请求数（RPS），按 App ID 或 API Key 维度生效 | `10` |
| `token_quota` | 每日/每月总 token 配额（单位：千 token），支持滚动窗口计费 | `5000`（即 5M tokens/day） |
| `burst_capacity` | 突发流量缓冲容量（以 token 为单位），用于应对瞬时高峰 | `10000` |

> **注意**：`burst_capacity` 在 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中建议设为 `token_quota` 的 5%–10%，但 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档中仍沿用固定值 `5000`，该值已过时，请以控制台实时配置为准。

## 使用方式

1. **创建 Plan**：在百炼控制台「配额管理」→「新建 Token Plan」，选择适用模型与计费周期（日/月）  
2. **绑定资源**：将 Plan 关联至具体 App 或 API Key（一个资源仅可绑定一个 Plan）  
3. **生效验证**：发起测试请求，检查响应头 `X-RateLimit-Remaining` 和 `X-Token-Quota-Used` 字段确认配额扣减逻辑  

所有配置均可通过 OpenAPI v3 接口 `PUT /v1/plans/{plan_id}` 动态更新，无需重启服务。完整操作流程见 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md)。

## 限制和注意事项

- Token 计费以模型实际消耗为准：输入 + 输出 token 总和（含 system prompt、function call schema 等隐式内容）  
- 异步任务失败重试不重复计费，但状态轮询请求（`GET /v1/async-tasks/{task_id}`）单独计入 RPS 限额  
- 免费额度与付费 Plan 独立计算，不可叠加；跨模型调用（如先调用 Qwen2-7B 再调用 Qwen2-72B）共享同一 Plan 配额  
- 若同时配置了 `rate_limit` 和 `token_quota`，任一维度超限均会触发 `429 Too Many Requests` 响应  

如遇配额异常扣减，请优先核查是否误启了调试模式下的冗余日志上报，该行为已在 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 中明确列为高风险操作。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


