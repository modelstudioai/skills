# token plan api

Token Plan API 是百炼平台用于管理组织级 Token 配额、席位分配与订阅用量的核心接口集合，支持企业客户按需购买、调整和监控模型调用资源。该 API 分属两个服务：席位购买与变配由 BssOpenApi 提供，其余功能（如组织管理、成员/席位/邀请/Key/用量等）由 ModelStudio 提供。所有接口均需使用组织管理员权限的 API Key 调用。

## 支持的模型/功能

Token Plan API 不直接关联具体大模型（如 Qwen 系列），而是提供**资源编排层能力**，包括：
- 组织层级的 Token 配额计划配置（[组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)）
- 成员 Token 席位分配与回收（[成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)）  
- 席位生命周期操作（创建、升级、降配、续费）（[席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)）
- 订阅状态与实时用量查询（[订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)）

> **注意**：原始文档中明确指出“席位购买与变配接口属于 BssOpenApi（版本 2023-09-30），其余接口属于 ModelStudio（版本 2026-02-10）”，但当前 ModelStudio 最新稳定版实际为 2025-04-15；请以 [API 版本兼容性说明](../../raw/model-api-reference/token-plan-api.md) 中声明的运行时版本为准，避免硬编码版本号。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `org_id` | string | 是 | 组织唯一标识，从百炼控制台或 `/v1/orgs` 接口获取 |
| `seat_type` | string | 是（席位类接口） | 取值：`standard` / `pro` / `enterprise`，对应不同 Token 配额包 |
| `quantity` | integer | 否（默认 1） | 购买/变配席位数量，仅在 [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md) 中生效 |
| `effective_time` | string (ISO8601) | 否 | 生效时间，不填则立即生效；仅对变配类请求有效 |

## 使用方式

1. **鉴权**：所有请求需在 `Authorization` Header 中携带 `Bearer <api_key>`，该 Key 必须具备 `token_plan:admin` 权限（参见 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)）  
2. **Endpoint 示例**：  
   - ModelStudio 接口：`POST https://dashscope.aliyuncs.com/api/v1/token-plan/seats`  
   - BssOpenApi 接口：`POST https://business.aliyuncs.com/api/bssopenapi/2023-09-30/ModifySeatQuantity`  
3. **响应格式**：统一返回 JSON，含 `request_id` 和 `data` 字段；错误时返回标准 `code` 与 `message`（详见 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md) 的错误码附录）

## 限制和注意事项

- 单次席位购买最大数量为 100，超过需分批调用（[席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)）  
- Token 席位变更（如升级）后，旧席位配额立即失效，新配额即时生效，**不支持回滚**  
- 成员被移出组织后，其已分配席位自动释放，但历史用量数据仍保留在 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md) 中可查  
- 所有接口均受百炼平台通用速率限制（100 QPS / org_id），突发流量需自行实现重试退避逻辑

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


