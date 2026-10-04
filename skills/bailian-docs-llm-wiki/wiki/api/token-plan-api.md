# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台用于管理组织级 [Token](../concepts/token.md) 配额、订阅计划及用量监控的核心接口集合，支持按组织/成员/席位维度精细化控制模型调用资源。该 API 不直接参与模型推理，而是为配额分配、权限隔离和计费结算提供基础设施能力。开发者需结合 [原文标题](../../raw/model-api-reference/token-plan-api.md) 中的模块划分理解其完整能力边界。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API **不涉及具体大模型（如 Qwen 系列）的推理能力**，其功能完全聚焦于资源治理层，包括：
- 组织级 Token 配额配置与继承策略  
- 成员 Token 用量实时查询与限额设置  
- 席位（Seat）生命周期管理（分配、回收、冻结）  
- 邀请链接生成与邀请状态跟踪  
- API Key 级别 Token 配额绑定与轮换  
- 订阅计划变更、用量汇总与账期快照  

所有子功能均在 [原文标题](../../raw/model-api-reference/token-plan-api.md) 的导航结构中明确定义，各子模块文档（如 `token-plan-api-seat.md`）描述了对应 REST 资源的 URI 和语义。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `org_id` | string | 是 | 组织唯一标识，从百炼控制台或 `/v1/orgs` 接口获取；所有操作均需显式指定 |
| `seat_id` / `member_id` | string | 条件必填 | 席位或成员 ID，用于粒度化配额操作；二者不可同时为空（见 [原文标题](../../raw/model-api-reference/token-plan-api.md) 中 `token-plan-api-seat.md` 与 `token-plan-api-member.md` 的约束说明） |
| `quota` | integer | 是 | Token 配额值，单位为千 token（k-tokens），最小值为 100（即 100k tokens） |
| `effective_at` | string (ISO8601) | 否 | 配额生效时间，默认为请求时刻；历史时间将被拒绝 |

> **注意**：部分旧版 SDK 示例中将 `quota` 单位误标为“个 token”，实际始终以千 token 为单位，以 [原文标题](../../raw/model-api-reference/token-plan-api.md) 中 `token-plan-api-subscription.md` 的用量统计口径为准。

## 使用方式

1. **认证**：使用组织管理员的 `API Key`（需具备 `token_plan:manage` 权限），通过 `Authorization: Bearer <api_key>` 传入  
2. **基础路径**：`https://dashscope.aliyuncs.com/api/v1/token-plan`  
3. **典型流程**：  
   - 创建席位 → 分配给成员 → 为该席位绑定 API Key → 查询该 Key 的实时用量  
   - 或：直接为成员设置全局配额（绕过席位），适用于轻量协作场景  

所有端点均遵循 RESTful 设计，支持 `GET`（查询）、`POST`（创建/触发）、`PATCH`（更新配额）操作，详见各子模块文档。

## 限制和注意事项

- 单次 `PATCH /seats/{seat_id}/quota` 请求最多修改 10 个席位配额（批量接口需另行调用 `/bulk` 端点）  
- 配额变更**不立即生效于正在执行的请求**，新配额仅对变更后发起的调用生效  
- 成员被移出组织后，其关联席位自动释放，但历史用量数据保留 90 天  
- 免费试用组织默认无 Token Plan 权限，需升级为付费组织后方可调用（参见 [原文标题](../../raw/model-api-reference/token-plan-api.md) 中 `token-plan-api-organization.md` 的权限矩阵）  
- 所有用量统计延迟 ≤ 30 秒，不适用于毫秒级配额熔断场景

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


