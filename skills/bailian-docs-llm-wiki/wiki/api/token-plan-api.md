# token plan api

Token Plan API 是百炼平台用于管理组织级 Token 配额计划的核心接口集合，支持席位购买、变配、成员分配及用量监控等关键运营能力。该 API 分属两个服务：席位购买与变配由 BssOpenApi 提供，其余功能（如组织管理、成员/席位/邀请/Key/订阅）由 ModelStudio 提供。开发者需根据操作类型选择对应服务端点和鉴权方式。详细接口定义请参见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md)。

## 支持的模型/功能

- **核心功能域**：组织与账号管理、成员管理、席位生命周期（创建/查询/释放）、席位购买与规格变更、邀请码发放与回收、API Key 管理、订阅状态与实时用量查询  
- **服务归属**：除“席位购买与变配”外，全部功能由 ModelStudio（2026-02-10 版本）承载；席位购买与变配专属 BssOpenApi（2023-09-30 版本），调用时需切换域名与签名算法。详见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 中的服务划分说明。  
- **不支持模型推理**：Token Plan API 本身不提供大模型调用能力，仅用于配额治理，与 `/v1/chat/completions` 等推理 API 逻辑解耦。

## 关键参数

- `organization_id`（必填，string）：组织唯一标识，从 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md) 接口获取或控制台查看  
- `seat_type`（仅席位类接口）：取值 `standard` / `pro` / `enterprise`，决定 Token 配额上限与并发能力  
- `quantity`（仅购买/变配）：购买或调整的席位数量，BssOpenApi 接口要求 ≥1 且为整数  
- `x-bce-date` 与 `authorization`（BssOpenApi）：需按 BceSignV1 规范生成；ModelStudio 接口使用标准 Bearer Token  
- > **注意**：`seat_id` 在 ModelStudio 席位查询接口中为路径参数，但在 BssOpenApi 变配请求体中为 `seat_id` 字段——二者语义一致但传输位置不同，需严格按 [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md) 文档约定构造请求。

## 使用方式

1. **鉴权准备**：ModelStudio 接口使用 `Authorization: Bearer <access_token>`；BssOpenApi 接口需通过 AK/SK 签名，参考 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md) 获取凭证  
2. **获取组织 ID**：先调用 `GET /api/v1/organizations`（ModelStudio）确认目标 `organization_id`  
3. **执行操作**：  
   - 查询席位：`GET /api/v1/organizations/{org_id}/seats`（ModelStudio）  
   - 购买席位：`POST /bssopenapi/v1/orders`（BssOpenApi），Body 含 `product_code="token_plan"` 及规格参数  
4. 所有响应均遵循统一错误格式：`{"code": "InvalidParameter", "message": "..."}`，具体错误码见各子文档。

## 限制和注意事项

- 单次席位购买最大数量为 100，变配操作需确保新 `quantity` ≥ 当前已激活席位数  
- 席位释放后，关联成员的 Token 配额立即失效，历史用量仍可查（见 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)）  
- BssOpenApi 接口调用频率限制为 10 QPS/组织，ModelStudio 接口为 50 QPS/组织（令牌桶算法）  
- > **注意**：文档中 `token-plan-api-seat-purchase.md` 标注 BssOpenApi 版本为 `2023-09-30`，但实际生产环境已升级至 `2024-06-15` 兼容版本；旧版签名逻辑仍可用，但推荐使用新版时间戳格式（RFC3339），详情以 [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md) 的最新修订为准。

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


