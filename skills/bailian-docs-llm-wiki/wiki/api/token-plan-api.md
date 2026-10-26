# token plan api

[Token](../concepts/token.md)Plan API 是百炼平台用于管理组织级 [Token](../concepts/token.md) 配额、席位生命周期及订阅用量的核心接口集合，覆盖从席位购买、变配到成员权限分配的全流程。该 API 分属两个底层服务：席位购买与变配由 BssOpenApi 提供，其余功能（如组织管理、成员/邀请/Key/用量等）由 ModelStudio 提供，版本与协议存在差异，调用时需注意服务路由和鉴权方式。详细接口定义与字段说明请参见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md)。

## 支持的模型/功能

[Token](../concepts/token.md)Plan API 不涉及模型推理能力，而是提供**组织级资源编排与配额治理能力**，具体包括：
- 组织与账号生命周期管理（创建、停用、查询）  
- 成员增删、角色分配与权限同步  
- 席位（Seat）的创建、释放、状态查询  
- 席位购买与规格变更（CPU/GPU/Token 配额调整）  
- 邀请链接生成与状态管理  
- API Key 的创建、轮换与作用域控制  
- 订阅计划查询、用量实时统计与阈值告警  

> **注意**：席位购买与变配功能归属 BssOpenApi（2023-09-30 版本），而组织、成员、邀请等管理功能归属 ModelStudio（2026-02-10 版本），二者 endpoint、鉴权 scheme（如 AK/SK vs. Bearer Token）及错误码体系不兼容，不可混用请求头或签名逻辑。详见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 中的服务划分说明。

## 关键参数

| 参数名 | 位置 | 必填 | 说明 |
|--------|------|------|------|
| `organization_id` | path / query | 是 | 组织唯一标识，需通过 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md) 接口获取 |
| `seat_id` | path | 否（部分接口必需） | 席位 ID，用于变配或释放操作；购买接口中由系统生成并返回 |
| `plan_type` | body | 是（购买/变配） | 取值为 `standard` / `pro` / `enterprise`，决定 Token 配额与并发上限 |
| `token_quota` | body | 否（变配时可选） | 显式指定 Token 总配额（单位：千），若未传则沿用当前 plan 的默认值 |
| `x-bce-date` + `authorization` | header | 是（BssOpenApi） | BSS 侧要求的 BCE 签名头，与 ModelStudio 的 `Authorization: Bearer <token>` 不互通 |

## 使用方式

1. **鉴权准备**：  
   - 调用 ModelStudio 接口（组织/成员/邀请/Key/用量）需使用平台颁发的 `Access Token`，通过 `Authorization: Bearer <token>` 传递；  
   - 调用 BssOpenApi 接口（席位购买/变配）需使用主账号 AK/SK 进行 BCE 签名，参考 [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md) 文档实现。  

2. **典型流程**：  
   ```bash
   # 1. 创建组织 → 获取 organization_id
   POST /v1/organizations
   
   # 2. 购买席位（BssOpenApi）
   POST https://bssopenapi.aliyuncs.com/?Action=CreateSeat&Version=2023-09-30
   
   # 3. 分配席位给成员（ModelStudio）
   POST /v2/organizations/{org_id}/seats/assign
   
   # 4. 查询用量（ModelStudio）
   GET /v2/organizations/{org_id}/subscriptions/usage
   ```

## 限制和注意事项

- 单组织最多支持 10,000 个活跃席位；单席位最大 `token_quota` 为 `50000`（5 千万）；  
- 席位变配操作（Upgrade/Downgrade）**不支持降级为更低配额的 plan_type**（例如 `pro` → `standard`），仅允许同级调整 `token_quota` 或升配；  
- API Key 仅对当前组织生效，无法跨组织复用；其 `scope` 字段必须显式声明（如 `"members:read,seats:write"`），空 scope 将被拒绝；  
- 所有用量统计延迟 ≤ 30 秒，不适用于毫秒级配额控制场景；实时限流请依赖模型调用侧的 `X-RateLimit-Remaining` 响应头。  

> **注意**：文档中提及的 ModelStudio 版本号 `2026-02-10` 为占位符，实际部署版本以 `/v2/openapi/version` 接口返回为准；若发现响应中 `api_version` 与 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 标注不一致，请优先以运行时返回值为准。

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


