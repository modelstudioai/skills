# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的后端服务接口集合，基于阿里云 OpenAPI 规范实现。所有接口均采用 `ACS3-HMAC-SHA256` 签名认证（除席位购买类接口调用 BssOpenApi 使用 `HMAC-SHA1`），不支持 `Bearer Token` 认证方式。开发者需通过阿里云 AccessKey 进行身份鉴权，并推荐使用阿里云 SDK 或 OpenAPI Explorer 发起调用。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于 **组织治理与资源配额管理**，主要包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，支持批量操作与席位状态校验（例如 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md) 接口会拒绝移除已分配席位的成员）；
- **席位精细化管控**：分配/回收席位、查询席位明细与统计、管理席位订阅周期与额度（如 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md) 返回 `SeatRemainingCredits`）；
- **邀请与配置管理**：创建/撤销邀请链接、设置默认角色与席位分配策略（如 `HIGH_TO_LOW`）；
- **API Key 安全管理**：创建与重置 UAC API Key，明文 Key 仅在创建或重置时返回一次；
- **订阅与用量洞察**：查询共享包明细、席位规格分布及周期性 Credits 剩余量。

> **注意**：席位购买、新增、升级、退订、续费等商业化操作属于 BssOpenApi（`business.aliyuncs.com`），版本为 `2023-09-30`，签名算法为 `HMAC-SHA1`，与主 Token Plan API（`modelstudio.cn-beijing.aliyuncs.com`，`ACS3-HMAC-SHA256`）的认证体系和 Endpoint 均不同，不可混用。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（如 `GetTokenPlanAccountDetail`）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头；BssOpenApi 接口则需 `Action`、`Version`、`SignatureMethod=HMAC-SHA1` 等 RPC 参数。
- **席位类型（`SpecType` / `SeatType`）**：统一取值为 `standard`（标准）、`pro`（高级）、`max`（尊享），在 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 等多处接口中作为关键筛选或配置项。
- **分页参数**：`PageNo`/`PageNum`（页码，从 1 开始）与 `PageSize`（每页条数，默认 10–20，最大 100），见 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 和 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)。
- **幂等性令牌**：BssOpenApi 类接口（如 `CreateCreditSeat`）强制要求 `ClientToken`，用于保障重复请求的幂等性。

## 使用方式

1. **环境准备**：配置环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免硬编码密钥。
2. **Endpoint 选择**：
   - 主服务（组织、成员、席位分配、邀请等）：`https://modelstudio.cn-beijing.aliyuncs.com`（华北2北京）；
   - 席位购买与变配（BssOpenApi）：`https://business.aliyuncs.com`（中国站）。
3. **签名调用**：
   - 主服务接口：使用 `ACS3-HMAC-SHA256` 算法，推荐调用阿里云 SDK 的 `CommonRequest` 或直接使用 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetTokenPlanAccountDetail) 生成调试代码；
   - BssOpenApi 接口：使用 `HMAC-SHA1` RPC 签名，SDK 同样支持。
4. **典型流程示例**：
   - 先调用 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 确认当前组织上下文；
   - 再调用 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 获取待操作成员 ID；
   - 调用 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 分配 `pro` 席位；
   - 最后调用 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md) 验证额度生效。

## 限制和注意事项

- **认证方式严格限定**：所有 Token Plan 主服务接口**不支持 `Authorization: Bearer {API_KEY}`**，仅接受 AccessKey 签名；若误用 Bearer 方式将返回 `403 Forbidden`。
- **席位状态强约束**：`RemoveOrganizationMember` 接口会主动检查成员是否持有有效席位（`SeatId` 非空且 `Status` 为 `NORMAL`），若存在则拒绝移除，需先调用 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)。
- **URL 编码要求**：Query String 中含中文或特殊字符时（如 `Name=新组织`），必须按 RFC 3986 进行百分号编码，否则签名验证失败（`SignatureDoesNotMatch`），详见 [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md) 文档说明。
- **幂等性与重试**：BssOpenApi 接口（如 `CreateCreditSeat`）依赖 `ClientToken` 实现幂等；主服务接口无内置幂等机制，客户端需自行处理重试逻辑。
- **权限最小化原则**：RAM 策略应精确授予 `tokenplan:*` 相关 Action，避免过度授权。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [升级席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [退订席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [续费席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)


