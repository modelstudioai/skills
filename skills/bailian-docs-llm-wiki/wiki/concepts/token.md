# Token 计量与管理

Token 计量与管理是百炼平台对模型调用资源消耗进行统一量化、实时统计、配额控制与成本归因的核心机制。所有 API 请求的输入（[prompt](../guides/prompt.md)）与输出（completion）均按实际解析后的 token 数精确计量，该数值既是配额校验、限流熔断、计费结算和用量监控的唯一依据，也是开发者进行资源规划与成本优化的基础单位。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 配额管理**：Token Plan 以实际消耗的输入/输出 token 总数为计量基准，实时校验请求是否超出月度 quota；超限立即返回 `429 Too Many Requests`，并附带 `Retry-After` 头。多模态模型（Qwen-VL、Qwen-Audio）也纳入同一计量体系，其非文本输入（如图像、音频）按平台预设换算规则折算为等效 token。
  
- **计费与成本控制**：免费额度、按量付费、节省计划、吞吐预留（PTU）全部基于 token 消耗计价。输入与输出 token 共享免费额度；阶梯计费模型（如 `qwen3.7-plus`）按单次请求总 token 数归属最高档位计费；启用上下文缓存时，命中 token 按固定系数（如 0.125）折算 TPM 消耗。

- **模型监控与可观测性**：用量统计页中的 `TotalToken` 指标即平台侧计量的 token 总和，支持按模型、API Key、时间维度聚合分析；该数据延迟约 1 小时，用于成本复盘与趋势预警（如配置「Token 突增」告警），但**不作为计费依据**（账单为准）。

- **API 调用与调试**：每次成功响应的 `usage` 字段（含 `input_tokens`、`output_tokens`、`total_tokens`）是唯一可信的计量结果；客户端预估（如 tiktoken）可能存在 ±3% 偏差，严禁用于配额判断或计费审计。

- **环境与权限隔离**：Token 计量严格绑定于调用上下文——不同业务空间、API Key、Token Plan 实例、地域（如华北2 vs 新加坡）的用量完全隔离；免费额度仅对通用 API Key 有效，Token Plan 专属 Key 不可消耗免费额度。

## 关键参数和配置

- `max_tokens`：单次请求允许生成的最大 token 数（默认 2048，上限 8192）；影响输出长度上限及对应配额消耗，是 token 计量的硬边界。
- `X-Plan-ID`：HTTP 请求头中指定 Token Plan 的唯一标识；未传入时 fallback 至账户默认 plan，缺失则报 `403 Forbidden`。
- `usage`（响应体字段）：必读字段，包含 `input_tokens`、`output_tokens`、`total_tokens`，代表平台侧最终计量结果，是配额、计费、监控的唯一事实源。
- `Free Tier Stop` 开关：控制「免费额度用完即停」行为（开启后返回 `403 AllocationQuota.FreeTierOnly`）；仅在仍有未消耗额度时可开启，关闭需待额度完全耗尽。
- `TPM（Tokens Per Minute）`：吞吐预留（PTU）的容量单位，购买时以 kTPM 为粒度；输入/输出分别按万TPM/千TPM报价，实际消耗按请求频次与 token 数动态计算。

> ⚠️ 注意：`max_output_tokens` 已于 v2.3.0 统一替换为 `max_tokens`；`secret_key` 自 v3.15.0 起不再支持；所有计量以平台服务端解析为准，客户端不可绕过或覆盖。

## 面向开发者，简洁实用

- ✅ **必做**：每次调用后检查响应 `usage` 字段，将其作为真实消耗记录；在监控中配置 `TotalToken` 突增告警，防成本失控。
- ✅ **必配**：Token Plan 场景下，务必在请求 header 中显式携带 `X-Plan-ID`；免费额度调试请使用通用 API Key（非 Token Plan Key）。
- ✅ **必避**：勿依赖本地 tokenizer 预估 token 数做配额控制；勿在未确认地域匹配时混用 API Key；勿在生产环境开启「免费额度用完即停」（可能导致业务中断）。
- ✅ **推荐**：结合用量统计页的 TOP10 模型排行，识别高消耗模型并针对性优化 [prompt](../guides/prompt.md) 或启用缓存；对关键业务流，用 Token Plan + PTU 双重保障稳定性与成本确定性。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [preparations](../api/preparations.md)


