# Token 管理

Token 管理是百炼平台对模型调用过程中输入/输出文本、图像、音频等内容所消耗的计算资源（以 token 为计量单位）进行统一配额控制、实时计量、用量监控与成本治理的核心机制。它贯穿 API 调用、资源分配、可观测性与计费全链路，是保障服务稳定性、实现精细化资源治理和合规成本管控的基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **配额控制（Token Plan）**：通过 `Token Plan` 机制为模型调用设置周期性配额（如日/月 quota）、突发弹性策略（burst_ratio）及模型白名单，实现按角色、场景、模型维度的资源隔离与分级管控。不指定 plan 的请求默认走共享池，易受全局限流影响。
- **调用执行（API 请求）**：每次模型请求的实际 token 消耗（含 [prompt](../guides/prompt.md) + completion）由平台自动统计，并实时扣减对应 Token Plan 的剩余配额；超限行为由 `enforce_mode`（strict/soft）决定是否拒绝或短时容忍。
- **可观测性（Monitoring）**：`应用观测` 和 `模型监控` 均将 token 用量作为核心指标——前者在 trace 中记录单次调用的 `input_tokens`/`output_tokens`，后者按模型、API Key、时间维度聚合统计，支撑用量分析、SLO 评估与账单对账。
- **安全与调试（Preparations）**：`max_tokens` 等参数直接约束 token 消耗上限；输入总长度超模型最大上下文时，平台主动拦截并返回明确错误，避免无效 token 浪费；流式响应中 token 分块生成也纳入实时计量。
- **组织治理（Token Plan API）**：企业级 Token 管理依赖组织账号体系——席位（Seat）分配隐式绑定 token 配额能力，成员角色（ORG_ADMIN/ORG_MEMBER）决定其可创建/修改 Token Plan 的权限范围，实现从组织到个人的配额继承与管控下沉。

## 关键参数和配置

| 参数 | 所属模块 | 类型/取值 | 说明 |
|------|----------|-----------|------|
| `quota` | Token Plan | 整数或科学计数法（如 `5e5`） | 周期总配额（单位：token），单 plan 最大 `1e9` |
| `burst_ratio` | Token Plan | float `[1.0, 3.0]`，默认 `1.5` | 突发流量倍率，修改后需 60 秒同步生效 |
| `enforce_mode` | Token Plan | `"strict"`（默认）或 `"soft"`（已弃用） | 严格模式下超限立即返回 `429`；`soft` 模式已不推荐使用 |
| `model_whitelist` | Token Plan | 字符串数组（如 `["qwen-plus"]`） | 空数组表示允许全部模型；同一账号下各 plan 白名单不可重叠 |
| `X-Plan-ID` / `X-Task-ID` | API 请求头 | string | 调用时显式指定 Token Plan，否则走默认配额池 |
| `input_tokens` / `output_tokens` | Monitoring | integer | 监控系统自动采集的单次调用实际消耗量，用于用量统计与告警 |
| `time_granularity` | 模型监控 | `"1m"` / `"1h"` / `"1d"` | 用量统计的时间精度，影响数据延迟与查询粒度 |

> ⚠️ 注意：`enforce_mode=soft` 已标记为弃用；`burst_ratio > 3.0` 或单次请求 `> 1e6` tokens 将被强制拦截；所有 token 计量均基于百炼平台标准 tokenizer（非开源社区 tokenizer），结果具有一致性与平台内可比性。

## 面向开发者，简洁实用

- ✅ **必做**：生产环境务必为每个关键业务路径创建专属 Token Plan，并在请求头中显式传入 `X-Plan-ID`，避免共享池争抢导致抖动。
- ✅ **必查**：调用失败时，优先检查响应 Header 中的 `X-RateLimit-Remaining` 和 `X-RateLimit-Reset`，结合 `request_id` 在监控中定位 token 消耗峰值与超限原因。
- ✅ **必配**：在模型监控中为高价值模型配置 `Token Usage Rate`（单位时间 token 消耗量）告警，及时发现异常刷量或 [prompt](../guides/prompt.md) 泄漏风险。
- ❌ **禁用**：不要依赖 `enforce_mode=soft` 实现“柔性降级”——该模式已失效，应改用 `burst_ratio` + 重试退避策略。
- 📊 **诊断工具**：使用 `dashscope` CLI 的 `/skill diagnose` 命令自动分析历史调用中的 token 分布、平均长度与截断比例，优化 [prompt](../guides/prompt.md) 设计。

Token 管理不是静态配额开关，而是动态、可观测、可审计的资源治理闭环。从 Plan 定义 → 请求执行 → 实时计量 → 监控告警 → 成本归因，每一步都应纳入你的 SRE 与 FinOps 实践。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)


