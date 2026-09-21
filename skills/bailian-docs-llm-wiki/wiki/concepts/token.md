# Token 管理

Token 管理是百炼平台对模型调用中 **输入与输出 token 消耗量** 进行计量、配额控制、计费结算与监控分析的统一机制。它贯穿 API 调用全生命周期，是保障服务稳定性、优化成本、实现精细化资源治理的核心横切能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **配额控制（Token Plan）**：通过 Token Plan 为 App 或 API Key 设置 `token_quota`（日/月总 token 配额）、`rate_limit`（RPS）、`burst_capacity`（突发缓冲）等硬性限制，超限即返回 `429 Too Many Requests`。适用于生产环境流量治理与多租户隔离。
- **计费计量**：所有模型调用（同步 `/v1/chat/completions`、异步 `/v1/async-tasks`、批量 `/v1/batch`、Embedding、Rerank、TTS 等）均按 **实际消耗的输入 token + 输出 token 总和** 计费，含 system prompt、function call schema 等隐式内容；流式响应按实际返回 token 实时扣减。
- **成本管理（[test 1](../guides/test-1.md)）**：免费额度、资源包、节省计划、吞吐预留（PTU）等付费模式均以 token 为基本计量单位进行抵扣与结算；PTU 容量也需按 token 消耗速率（TPM）换算使用。
- **监控与诊断（[model monitoring](../guides/model-monitoring.md)）**：监控系统按小时/天粒度聚合 token 消耗（分输入/输出），支持按 `api_key_id`、`app_id` 等维度下钻分析，辅助定位高消耗请求、验证配额策略有效性。
- **认证与初始化（[preparations](../api/preparations.md)）**：API Key 是触发 token 计量的前提——未配置有效 `api_key` 的请求无法通过鉴权，自然不进入 token 计量流水线；单个 API Key 默认受 10 QPS 限流保护，本质是轻量级 token 管理前置守门员。

## 关键参数和配置

| 参数 | 所属模块 | 说明 | 开发者须知 |
|------|----------|------|------------|
| `token_quota` | Token Plan | 每日/每月总 token 配额（单位：千 token），滚动窗口计费 | 建议设为业务峰值日消耗量的 1.5–2 倍；个人版默认值 `5000`（5M tokens/day）已过时，以控制台为准 |
| `burst_capacity` | Token Plan | 突发流量缓冲容量（token 单位） | 推荐设为 `token_quota` 的 5%–10%，用于平滑瞬时高峰，避免误拒合法请求 |
| `max_tokens` | Token Plan / 模型 API | 单次请求最大输出 token 数（硬限制） | 超出将被模型截断并返回 `context_length_exceeded` 错误；不影响输入 token 计费 |
| `input_tokens` / `output_tokens` | 监控 & 账单 | 实际消耗的输入/输出 token 数（由服务端精确解析） | **不等于客户端估算值**；流式响应中 `output_tokens` 在 `done` 事件后才最终确定；账单以此为准 |
| `X-Token-Quota-Used` / `X-RateLimit-Remaining` | 响应 Header | 当前周期已用 token 量、剩余 RPS 配额 | 开发者应在关键路径中记录该头信息，用于自助诊断配额异常 |

> ⚠️ 注意：  
> - 免费额度、节省计划、PTU 均**严格按地域隔离**，华北2（北京）的 token 配额/额度不可用于新加坡地域调用；  
> - Batch 调用产生的 token **不享受新人免费额度抵扣**；  
> - 异步任务重试不重复计费，但其状态轮询（`GET /v1/async-tasks/{task_id}`）单独计入 RPS 限额；  
> - 所有 token 计量以模型服务层解析结果为准，客户端应避免自行估算用于配额判断。

## 面向开发者，简洁实用

- ✅ **快速验证配额生效**：发起一次测试请求，检查响应头 `X-Token-Quota-Used` 是否递增、`X-RateLimit-Remaining` 是否减少。  
- ✅ **精准排查超限**：若遇 `429`，优先检查 `X-RateLimit-Remaining: 0`（RPS 超限）还是 `X-Token-Quota-Used` 接近 `token_quota`（总量超限）。  
- ✅ **成本优化建议**：高频小请求 → 优先调优 `max_tokens` 并启用 PTU；长上下文场景 → 关注缓存折算系数与长输入阶梯系数（见 [test 1](../guides/test-1.md) 文档），合理使用 `cache_prompt`。  
- ✅ **安全实践**：API Key 必须通过环境变量注入（如 `DASHSCOPE_API_KEY`），禁止硬编码；Token Plan 绑定应遵循最小权限原则（一个 App 仅绑定必需的 Plan）。  
- ❌ **避免踩坑**：不要依赖客户端 token 估算做限流；不要在前端暴露 API Key；不要开启“安心模式”（免费额度用完即停）于生产环境。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)


