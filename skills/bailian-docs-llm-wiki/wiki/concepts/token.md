# Token 与配额管理

Token 与配额管理是百炼平台对模型调用资源进行计量、限制与分配的核心机制，通过统一的 Token 计量单位（输入 + 输出 tokens）和可配置的配额策略（Token Plan），实现精细化的用量控制、成本约束与服务稳定性保障。

## 在百炼平台的不同场景中，这个概念如何使用

- **个人开发与快速验证**：系统自动发放 90 天有效期、100 万 Token 的免费额度（仅限华北2地域指定模型），无需配置即用；额度按自然日重置，输入与输出 Token 合并计算，直接抵扣实时推理调用费用。  
- **团队协作与多环境隔离**：通过 Token Plan 为不同工作区（Workspace）、子账号或团队（Team）独立分配配额，支持按模型 ID（如 `qwen-plus`）或通配符（企业版）绑定，严格区分同步调用（`/v1/chat/completions`）与异步批量任务（`/v1/batch`）的额度消耗。  
- **生产级资源治理**：结合 Token Plan API 实现组织级自动化配额调度，例如为新成员批量分配席位并绑定专属 Token Plan，或通过 OpenAPI 动态调整配额上限，支撑灰度发布、A/B 测试等场景。  
- **可观测与成本优化**：模型监控（Model Monitoring）提供分钟级 TotalToken 消耗统计与告警能力；应用观测（Application Monitoring）在 Span 级别精确拆解各节点（LLM、Retriever 等）的 Token 用量，辅助定位高消耗环节；所有用量数据均可用于驱动配额策略迭代。  
- **安全与权限分离**：Token Plan 配额校验与认证体系解耦——调用时通过 `X-Token-Plan-ID` Header 显式启用配额控制，而默认通道（无该 Header）受全局速率限制约束；Token Plan 专属 API Key 不消耗免费额度，确保计费路径清晰可控。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 约束 |
|------|------|------|------|------|
| `model` | string | 是 | 模型标识，如 `qwen-plus` 或 `qwen-max`；企业版支持 `*`（全部模型） | 单个 Plan 仅支持一个 model，不支持多模型聚合 |
| `limit` | integer | 是 | 配额上限，单位为 **千 tokens/日**（如 `500` = 50 万 tokens/日） | 最小值 `1`（1000 tokens/日） |
| `window` | string | 是 | 时间窗口类型 | **仅支持 `"day"`**（UTC+8 自然日），`"hour"` 已废弃，传入将返回 `400 Bad Request` |
| `scope` | string | 是 | 作用域 | 可选 `"user"`（当前账号）、`"workspace"`（当前工作区）、`"team"`（团队版专属） |
| `X-Token-Plan-ID` | header | 否（启用配额时必填） | 绑定 Plan 的唯一 ID | 缺失则走无配额通道，受全局限流约束 |

> ⚠️ 注意：  
> - 免费额度、Token Plan、AI 节省计划、资源包四者独立生效，抵扣优先级为：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**；  
> - Token Plan 配额按自然日（UTC+8）零点重置，不可跨日累计或借用；  
> - Coding Plan 是 Token Plan 的专用子集，仅适用于 `/v1/coding` 接口，其配额与通用模型 Plan **完全隔离、不可互通**。

## 面向开发者，简洁实用

- ✅ **快速上手**：控制台 → 运维管理 → Token 配额管理 → 创建 Plan，填入 `model`、`limit`、`scope` 即可生效；调用时加 Header `X-Token-Plan-ID: <plan_id>` 即启用校验。  
- ✅ **精准用量查询**：调用 `GET /v1/token-plans/{id}/usage?date=2024-06-01` 获取指定日期用量；控制台「模型用量」页也支持按 Plan、模型、API Key 多维下钻。  
- ✅ **避免踩坑**：  
  - 不要尝试 `window: "hour"` —— API 会拒绝；  
  - 不要混用免费额度与 Token Plan Key —— Token Plan Key 调用**不消耗免费额度**；  
  - 删除成员前请先回收其席位，否则操作失败（`HasSeat=true` 时拒绝移除）。  
- ✅ **推荐实践**：  
  - 团队初期用 `scope: "workspace"` 统一分配；  
  - 生产环境关键模型单独建 Plan 并开启 `TotalToken` 告警（阈值建议设为日配额的 80%）；  
  - 结合应用观测的 Span 级 Token 数据，持续优化 Prompt 长度与输出长度，降低实际消耗。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)


