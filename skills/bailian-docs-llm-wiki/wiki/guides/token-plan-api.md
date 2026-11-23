# token plan api

Token Plan API 是百炼平台用于管理组织级 Token 配额、席位分配与订阅用量的核心接口集合，支持企业客户精细化控制模型调用资源。该 API 分为两类服务：席位购买与变配由 BssOpenApi 承载，其余功能（如组织管理、成员/席位/邀请/Key/用量等）统一通过 ModelStudio API 提供。所有接口均需使用有效的 API Key 进行身份认证与权限校验。

## 支持的模型/功能

- **ModelStudio API（v2026-02-10）**：覆盖组织与账号管理、成员增删改查、席位分配与回收、邀请链接生成与状态查询、API Key 创建与轮换、订阅详情与实时用量统计等功能。  
- **BssOpenApi（v2023-09-30）**：仅提供席位购买、升级、降配等计费相关操作，不涉及运行时资源调度或权限控制。  
  > **注意**：[席位购买与变配](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md) 接口所属服务域与其他模块不一致，调用方需分别配置对应 OpenAPI endpoint 与鉴权凭证，详见 [原文标题](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md)。

## 关键参数

- `org_id`（路径参数）：必填，目标组织唯一标识，从 [组织与账号](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization.md) 接口获取。  
- `seat_id`（路径/请求体）：席位操作必需，用于绑定成员或触发变配，参见 [席位管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat.md) 文档。  
- `api_key`（Header: `Authorization: Bearer <key>`）：全局认证凭据，须具备对应组织 `token_plan_admin` 或 `token_plan_member` 权限，管理方式见 [API Key 管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key.md)。

## 使用方式

1. 调用 `GET /v1/organizations` 获取 `org_id`；  
2. 根据场景选择子资源路径：  
   - 成员管理 → `/v1/organizations/{org_id}/members`  
   - 席位分配 → `/v1/organizations/{org_id}/seats`  
   - 用量查询 → `/v1/organizations/{org_id}/subscriptions/usage`  
3. 席位购买/变配需切换至 BssOpenApi endpoint（如 `https://bssopenapi.aliyuncs.com`），使用 `Action=ModifySeatCapacity` 等专用 Action，具体参数格式以 [原文标题](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md) 为准。

## 限制和注意事项

- 单次请求最多返回 100 条记录，分页需传入 `page_number` 和 `page_size`；  
- ModelStudio 接口 QPS 限流为 50/秒/组织，BssOpenApi 限流为 10/秒/账号，超限返回 `429 Too Many Requests`；  
- 席位释放后，关联成员的 Token 调用权限将在 5 分钟内失效，但历史用量数据仍可查询，详见 [订阅与用量](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription.md)；  
- > **注意**：[原文标题](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat.md) 中描述的“席位可跨组织迁移”为过时信息，当前版本不支持跨 org seat 转移，实际行为以最新 OpenAPI Schema 为准。

## 来源文档

- [TokenPlan](../../raw/token-plan-user-guide/token-plan-api.md)


