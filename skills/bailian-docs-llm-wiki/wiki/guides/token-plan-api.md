# token plan api

TokenPlan API 是百炼平台用于管理组织级 Token 配额、席位生命周期及用量订阅的核心接口集合，支持开发者通过程序化方式完成席位购买、变配、成员绑定、API Key 分配等关键操作。该 API 由两个后端服务协同提供：席位购买与变配功能由 BssOpenApi 承载，其余管理能力（如组织、成员、席位状态、邀请、API Key、订阅用量）统一由 ModelStudio 提供。所有接口均需使用有效的 `AccessKeyId` 和 `AccessKeySecret` 进行签名认证。

## 支持的模型/功能

- **席位生命周期管理**：创建、查询、升级、降配、释放席位（对应 [席位购买与变配](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md)）
- **组织与成员治理**：组织信息维护、成员增删改查、角色分配（见 [组织与账号](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization.md) 和 [成员管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member.md)）
- **API 密钥与权限控制**：为成员或服务生成独立 API Key，并设置作用域与有效期（参见 [API Key 管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key.md)）
- **用量与订阅监控**：实时查询 Token 消耗量、剩余配额、账单周期及订阅状态（依据 [订阅与用量](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription.md)）

> **注意**：文档中明确指出“席位购买与变配接口属于 BssOpenApi（版本 2023-09-30），其余接口属于 ModelStudio（版本 2026-02-10）”，但当前 ModelStudio 最新稳定版实际为 2025-10-15；请以 [原文标题](../../raw/token-plan-user-guide/token-plan-api/token-plan-api.md) 中声明的接口归属为准，避免混用 SDK 版本。

## 关键参数

- `OrganizationId`（必填，string）：组织唯一标识，从组织管理接口获取  
- `SeatId`（部分接口必填）：席位 ID，用于变配或释放操作  
- `ModelName`（仅变配时可选）：目标模型名称（如 `qwen-max`），影响 Token 配额计算逻辑  
- `Quantity`（变配接口必填）：新席位数量，支持整数增减  
- `EffectiveTime`（可选）：变配生效时间，支持立即生效（`immediately`）或下个计费周期（`next-cycle`）  

所有请求需携带标准阿里云签名头（`x-acs-signature-nonce`, `x-acs-signature-method`, `x-acs-signature-version`, `x-acs-signature`）及 `x-acs-accesskey-id`。

## 使用方式

1. 调用 [组织与账号](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization.md) 接口获取 `OrganizationId`  
2. 调用 [席位购买与变配](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md) 创建初始席位（BssOpenApi 域名：`https://bssopenapi.aliyuncs.com`）  
3. 调用 [成员管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member.md) 将成员加入组织并分配席位  
4. 调用 [API Key 管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key.md) 为成员生成具备 Token 调用权限的密钥  
5. 定期轮询 [订阅与用量](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription.md) 接口监控配额水位  

SDK 示例（Python）建议使用 `aliyun-python-sdk-bssopenapi`（v1.3.11+）和 `aliyun-python-sdk-modelstudio`（v2.0.8+），注意区分 endpoint。

## 限制和注意事项

- 单次变配请求 `Quantity` 变更幅度不可超过当前值的 ±50%，超出需分批提交  
- 席位释放后，关联成员的 API Key 将自动失效，且无法恢复历史用量记录  
- ModelStudio 接口调用频率限制为 100 QPS / OrganizationId，BssOpenApi 席位类接口为 20 QPS / Account  
- 所有接口均不支持跨地域调用：BssOpenApi 必须使用 `cn-shanghai` 区域 endpoint，ModelStudio 必须与组织所在 region 一致  
- > **注意**：[原文标题](../../raw/token-plan-user-guide/token-plan-api/token-plan-api.md) 明确要求“席位购买与变配”必须走 BssOpenApi，但部分旧版 SDK 文档误将其归入 ModelStudio；请严格按该原始文档的服务划分调用，否则将返回 `InvalidAction` 错误。

## 来源文档

- [TokenPlan](../../raw/token-plan-user-guide/token-plan-api.md)


