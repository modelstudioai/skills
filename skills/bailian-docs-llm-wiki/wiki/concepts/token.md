# Token 计量与管理

Token 计量与管理是百炼平台对模型调用资源进行精准计费、配额控制与用量治理的核心机制，以输入/输出 Token 为统一计量单位，贯穿推理、训练、监控与成本优化全链路。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：所有同步（`/v1/chat/completions`）、异步（`/v1/batch`）和流式响应请求均按实际消耗的输入 Token 和输出 Token 分别计量；计费与限流均基于此结果，系统提示词（system [prompt](../guides/prompt.md)）不计入 Token 消耗。
- **Token Plan 配额管控**：通过 `X-Plan-ID` 绑定计划，实现按分钟（`per_minute`）与按日（`per_day`）双维度的累计 Token 配额控制，支持 API Key 级隔离、多环境分配及团队成员权限继承。
- **成本抵扣与账单溯源**：免费额度（100 万 Token/模型/90 天）、资源包、节省计划等均以 Token 为抵扣单位；账单中 `实例 ID` 字段明确标识 `ApiKeyID;业务空间ID;模型名称;输入/输出类型`，支撑精确费用归因。
- **模型训练与部署**：训练任务按训练 Token 总量计费；部署类服务（如 PTU、TPM Reservation）虽以吞吐单位（kTPM/TPU）呈现，但底层容量换算、溢出计费仍锚定于 Token 处理能力（含长输入阶梯系数与缓存折算）。
- **监控与可观测性**：`/v1/monitoring/metrics` 等接口返回的用量统计严格对齐计费逻辑，提供按模型、应用、时间粒度聚合的 Token 消耗数据，并支持导出用于成本分析与容量规划。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `X-Plan-ID`（Header） | 指定生效的 Token Plan，必需 | 未提供或无效时回退至账户默认 plan；单个 plan 最多绑定 100 个 API Key |
| `max_tokens`（Request Body） | 单次请求最大输出 token 数 | 受模型原生限制与 plan 配额双重约束；仅部分模型支持动态覆盖 |
| `token_quota`（Token Plan API） | 周期内累计 Token 配额上限（非并发限制） | 按 `plan_type`（月/年）重置；旧版“每分钟限额”描述已过时 |
| `effective_at`（Token Plan API） | 配额变更生效时间戳 | 支持未来时间点生效；变更通常 30 秒内同步，高并发下延迟 ≤2 分钟 |
| 免费额度标识（账单字段） | `实例 ID` 中的 `免费额度用完即停标识` | 是判断服务中断原因的关键依据；欠费状态下即使有剩余额度，服务亦暂停 |

> ⚠️ 提示：所有 Token 计量均以 UTF-8 编码下的实际 tokenization 结果为准（基于对应模型 tokenizer），不依赖客户端估算；流式响应中，`finish_reason="length"` 截断情形下的 completion tokens 仍全额计费。

## 面向开发者，简洁实用

- ✅ **必做**：在生产调用中始终传入 `X-Plan-ID`，并通过 `/v1/usage/plan/{plan_id}` 实时检查剩余配额，避免突发限流。
- ✅ **推荐**：启用「免费额度用完即停」开关，配合监控告警（如 `error_rate > 0.05` 或 `quota_usage_ratio > 0.9`）实现主动成本干预。
- ✅ **避坑**：模型版本带日期后缀（如 `qwen3.7-plus-2026-05-26`）视为独立模型，其 Token 额度、资源包、节省计划均不与无后缀版本互通。
- ✅ **调试技巧**：使用 `X-Trace-ID` 透传调用上下文，确保监控中的 Token 消耗、延迟、错误率能准确关联至具体请求链路。
- ✅ **成本优化**：长期稳定调用优先选 AI 通用型节省计划（最高 5.3 折）；高并发低延迟场景选用 TPM Reservation，避免按量溢出计费。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [model data overview](../guides/model-data-overview.md)


