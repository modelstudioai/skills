# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。开发者可通过订阅不同档位的 [Token](../concepts/token.md) Plan 获取稳定、可预期的调用额度，适用于批量推理、应用集成等生产场景。该机制与模型计费模型深度耦合，直接影响请求成功率与排队行为。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型），但**不适用于**以下场景：  
- 通过 `/v1/chat/completions` 等 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用的非百炼托管模型；  
- 实时音视频流式 infer 接口（如 `/v1/audio/transcribe-stream`）；  
- 模型微调训练任务（训练阶段 token 不计入 [Token](../concepts/token.md) Plan 配额）。  
详情请参阅 [Token Plan 概述](https://help.aliyun.com/zh/model-studio/token-plan-overview) —— 该文档明确指出“Plan 仅约束 inference 请求的输入+输出 token 总和”，与 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 中列出的链接体系一致。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `total_tokens_per_month` | 月度总配额（输入 + 输出 token） | `10000000` |
| `rate_limit_per_second` | 每秒最大并发 token 消耗量（硬限流阈值） | `5000` |
| `burst_capacity` | 短期突发容量（单位：token），允许瞬时超限后平滑回落 | `10000` |

> **注意**：`burst_capacity` 在 [进阶配置](https://help.aliyun.com/zh/model-studio/token-plan-best-practice) 中被定义为“基于令牌桶算法的补充额度”，但 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 所引的官方帮助页未明确定义其重置周期，实际行为以控制台实时配额仪表盘为准。

## 使用方式

1. 在控制台「配额管理」→「[Token](../concepts/token.md) Plan」中完成订阅（个人版/团队版）；  
2. 调用 API 时**无需额外 header 或参数**，系统自动按请求的 `prompt_tokens + completion_tokens` 扣减配额；  
3. 若触发限流，API 返回 `429 Too Many Requests`，响应头含 `X-RateLimit-Remaining` 和 `X-RateLimit-Reset`；  
4. 可通过 `/v1/usage/token-plan`（需 `token_plan:read` 权限）查询实时余量。  
该流程与 [玩法攻略](https://help.aliyun.com/zh/model-studio/token-plan-playbooks) 中的自动化监控示例一致，也与 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 所列入口路径完全对应。

## 限制和注意事项

- 配额按自然月清零，不可结转；  
- 团队版 Plan 的配额在成员间共享，但**不跨工作空间（workspace）**；  
- 同一账号下多个 Plan 订阅不叠加，系统优先使用到期时间最近的 Plan；  
- 若同时启用 Coding Plan，其 token 消耗**独立计费且不占用 [Token](../concepts/token.md) Plan 配额**（详见 [Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan-guide)）；  
- 输入含图片/音频 base64 的[多模态](../concepts/multi-modal.md)请求，其编码开销（如 base64 膨胀）**不计入 token 统计**，仅模型实际 consume 的语义 token 计入。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)



