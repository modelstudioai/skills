# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及 API Key 全生命周期管理接口集合，用于自动化构建 Token Plan 团队版的治理能力。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名（除 BssOpenApi 席位购销类接口使用 `HMAC-SHA1`），不支持 `Bearer Token` 认证方式。开发者需通过 RAM 授权后使用 AccessKey 调用。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源编排**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)、[修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)）；
- **成员全链路管理**：添加/查询/修改/移除成员，支持角色分级（ORG_OWNER/ORG_ADMIN/ORG_MEMBER）与批量操作（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)）；
- **席位精细化运营**：分配/回收席位（[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)）、查询明细（[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）、统计用量（[获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)）；
- **邀请与接入控制**：创建/获取/撤销邀请链接，配置默认角色与席位分配策略（如 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)、[设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)）；
- **API Key 安全管理**：创建与重置 UAC API Key（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)、[重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）。

> **注意**：席位购买、新增、升级、退订、续费等商业化操作属于 BssOpenApi（`business.aliyuncs.com`），版本为 `2023-09-30`，签名算法为 `HMAC-SHA1`，与主站 OpenAPI 的 `ACS3-HMAC-SHA256` 不兼容，需单独处理认证逻辑。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头；BssOpenApi 接口则需 `Action`、`Version`、`SignatureMethod=HMAC-SHA1` 等 RPC 参数。
- **席位规格（SpecType/SeatType）**：统一取值为 `standard` / `pro` / `max`，在成员添加、席位分配、订阅统计等多处接口中作为关键筛选或配置字段。
- **ID 类参数**：`OrgId`（组织 ID）、`AccountId`（账号 ID）、`ApiKeyId`（API Key ID）、`InstanceId`（席位实例 ID）均为全局唯一字符串，不可重复使用或拼接。
- **分页参数**：`PageNo`/`PageNum` 与 `PageSize` 在列表类接口（如成员列表、席位明细）中通用，`PageSize` 最大值为 100。
- **幂等性参数**：BssOpenApi 接口（如 `CreateCreditSeat`）强制要求 `ClientToken`，用于防止重复下单。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量，避免硬编码密钥；
2. **权限授予**：为 RAM 用户授予 `AliyunModelStudioFullAccess` 或最小化自定义策略（含 `modelstudio:ListOrganizationMembers`, `modelstudio:BatchAssignSeats`, `bss:CreateCreditSeat` 等细粒度 Action）；
3. **调用路径**：
   - 主站管理类接口（组织、成员、席位分配、邀请、API Key）：Endpoint 为 `https://modelstudio.cn-beijing.aliyuncs.com`，地域固定为华北2（北京）；
   - 商业化席位操作（购销变配）：Endpoint 为 `https://business.aliyuncs.com`，属中国站 BssOpenApi；
4. **推荐实践**：优先使用阿里云 SDK（如 Python 的 `aliyun-python-sdk-modelstudio` + `aliyun-python-sdk-bssopenapi`），自动处理签名、重试与错误解析；调试阶段可借助 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetTokenPlanAccountDetail) 生成示例代码。

## 限制和注意事项

- **认证方式严格限定**：所有接口均**不支持 `Authorization: Bearer {API_KEY}`**，仅接受 AccessKey 签名，尝试使用 bearer token 将直接返回 `403 Forbidden`；
- **席位回收约束**：`RemoveOrganizationMember` 接口会校验成员是否持有席位，若 `SeatAssigned=true` 则拒绝移除，须先调用 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)；
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接，重复调用 `CreateTokenPlanInviteLink` 将返回已有链接的 token，需先调用 `RevokeTokenPlanInviteLink` 失效旧链接；
- **API Key 安全边界**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 和 `RotateTokenPlanKey` 响应中**一次性返回**，服务端不存储明文，丢失后无法再次获取，必须由客户端安全保存；
- **地域与 Endpoint 绑定**：文档中所有 `modelstudio.cn-beijing.aliyuncs.com` 接口**仅支持华北2（北京）地域**，跨地域调用将失败；BssOpenApi 接口无地域概念，但需确保 `HostId=cn`（中国站）。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [续费席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [升级席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [退订席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)


