# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的后端控制面接口集合，基于阿里云 OpenAPI 规范实现。所有接口均需使用阿里云 AccessKey 进行 ACS3-HMAC-SHA256 签名认证，不支持 Bearer [Token](../concepts/token.md) 方式。该 API 主要服务于组织管理员对 [Token](../concepts/token.md)Plan 资源配额（如 Credits、席位规格）和成员生命周期的集中管控。

## 支持的模型/功能

Token Plan API **不涉及模型调用**，而是提供完整的组织治理能力，覆盖以下核心功能域：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)、[获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持批量操作（[添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)）；
- **席位精细化分配**：按 `standard`/`pro`/`max` 三类规格批量分配或回收席位，并可分页查询明细（[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）；
- **邀请与配置管理**：创建/获取/撤销邀请链接，设置默认角色与席位分配策略（[创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)、[设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)）；
- **API Key 与订阅用量**：为成员创建/重置 UAC API Key；查询席位统计、Credits 剩余量及共享包明细（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)、[获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)）。

> **注意**：文档中多处将 `ORG_OWNER` 角色列为合法值（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 的 `RoleCode` 枚举），但 [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md) 明确限定 `DefaultRoleId` 仅支持 `SYSTEM_ROLE_ORG_ADMIN` 和 `SYSTEM_ROLE_ORG_MEMBER`。实际调用时请以 `SetTokenPlanOrgInviteConfig` 接口文档为准，`ORG_OWNER` 不可用于邀请默认角色设置。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法为 `ACS3-HMAC-SHA256`；
- **席位规格（`SpecType` / `SeatType`）**：统一取值为 `standard`、`pro`、`max`，各接口（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)）语义一致；
- **数组参数格式**：`AccountIds`、`StatusList` 等数组类型均采用 Flat 格式（如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`），非 JSON 编码；
- **时间戳单位**：`CycleStartTime`、`CycleEndTime`、`ExpireTime` 等字段单位为**毫秒**（Unix Epoch），非秒；
- **地域 Endpoint**：当前仅支持华北2（北京）地域，Endpoint 固定为 `https://modelstudio.cn-beijing.aliyuncs.com`。

## 使用方式

1. **认证准备**：配置环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，确保 RAM 用户已授予 `AliyunModelStudioFullAccess` 或最小化自定义权限策略；
2. **SDK 推荐**：优先使用阿里云官方 SDK（如 Python 的 `alibabacloud_tea_openapi`），自动处理签名与请求构造，避免手动计算错误；
3. **调试工具**：通过 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/) 在线调试，实时生成签名并查看响应；
4. **关键流程示例**：
   - 新建组织成员 → 调用 `AddOrganizationMember`；
   - 分配席位 → 调用 `BatchAssignSeats`（传入 `SeatType` 和 `AccountIds`）；
   - 查询用量 → 调用 `GetSubscriptionStats` 获取 `SeatRemainingCredits`；
   - 安全轮转凭证 → 调用 `RotateTokenPlanKey`（`ApiKeyId` 不变，`PlainApiKey` 重置）。

## 限制和注意事项

- **认证方式强制约束**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`（见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)、[获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md) 等多处声明）；
- **席位回收前置检查**：调用 `RemoveOrganizationMember` 时，若成员已分配席位，接口将直接拒绝（返回错误），需先调用 `BatchRevokeSeats` 回收席位；
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接；重复调用 `CreateTokenPlanInviteLink` 将返回已有链接的 Token，而非新建（见 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)）；
- **分页参数默认值**：`PageNo` 默认为 `1`，`PageSize` 默认为 `20`（成员列表）或 `10`（席位/共享包明细），最大值均为 `100`；
- **敏感信息脱敏**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 和 `RotateTokenPlanKey` 的**首次响应中返回一次**，后续无法再次获取，需自行安全存储。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)


