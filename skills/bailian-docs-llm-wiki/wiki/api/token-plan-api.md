# token plan api

Token Plan API 是百炼平台用于管理组织级 Token 配额、订阅计划及用量监控的核心接口集合，支持按组织/成员/席位维度精细化控制模型调用资源。该 API 不直接调用大模型，而是为模型调用提供配额治理与计费基础能力。所有操作需通过 `Authorization: Bearer <api_key>` 认证，并遵循 RESTful 设计规范。

## 支持的模型/功能

Token Plan API 本身**不绑定具体大模型**（如 Qwen 系列），而是为所有接入百炼平台的模型服务提供统一的 Token 配额分配与用量追踪能力。其核心功能模块包括：组织层级配额配置、成员级 Token 分配、席位生命周期管理、邀请链接生成与绑定、API Key 权限与用量隔离、以及实时订阅状态与历史用量查询。各模块能力详见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 文档的子章节划分。

## 关键参数

- `org_id`（路径参数）：必填，目标组织唯一标识，从 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md) 接口获取  
- `seat_id` 或 `member_id`（路径/请求体）：用于席位或成员粒度操作，二者不可同时为空  
- `plan_type`（请求体）：枚举值 `pay_as_you_go` / `monthly_subscription` / `annual_subscription`，决定配额生效模式  
- `token_quota`（请求体）：整数，指定该实体可消耗的 Token 总量（非并发限制）  
- `effective_at`（可选）：ISO 8601 时间戳，支持未来时间点生效，详见 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)  

> **注意**：部分旧版文档示例中将 `token_quota` 解释为“每分钟限额”，该描述已过时；实际为**周期内累计配额上限**，以 `plan_type` 对应的计费周期（如月/年）为单位重置。

## 使用方式

1. 通过 `/v1/orgs/{org_id}/seats` 创建席位并绑定成员，自动继承组织默认配额  
2. 调用 `/v1/orgs/{org_id}/members/{member_id}/quota` 覆盖单成员配额  
3. 使用 `/v1/orgs/{org_id}/subscriptions/usage` 查询当前周期剩余 Token 量（含明细 breakdown）  
4. 所有写操作返回 `202 Accepted` 并附带异步任务 ID，最终状态需轮询 `/v1/tasks/{task_id}` 获取  

## 限制和注意事项

- 单组织最多创建 5000 个席位，单席位最大 `token_quota` 为 `2147483647`（2^31−1）  
- 配额变更**不实时生效**：通常在 30 秒内同步至模型网关，高并发场景下可能延迟至 2 分钟  
- 成员被移出组织后，其未用完的 Token 配额**立即作废**，不返还也不转移  
- 若需跨组织迁移用量，必须通过 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md) 的合并接口操作，直接修改 `org_id` 将导致 404 错误

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


