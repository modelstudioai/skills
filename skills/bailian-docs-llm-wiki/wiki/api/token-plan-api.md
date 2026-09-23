# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的统一管控接口集合，用于实现 [Token](../concepts/token.md) 配额的精细化分配与生命周期管理。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer` 类型 API Key 认证。开发者需使用阿里云 AccessKey 进行调用，并通过 RAM 授权控制权限范围。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源配额编排**，包括：
- **组织与账号管理**：获取当前账号详情、查询/修改组织基本信息（如名称、描述）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，以及统计成员与席位关系（如已分配/未分配席位数）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)；
- **席位资源调度**：批量分配/回收标准（`standard`）、高级（`pro`）、尊享（`max`）三类席位，并支持分页查询席位明细与状态 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)；
- **邀请与配置管理**：创建/获取/撤销成员邀请链接，设置默认角色与席位分配策略（`HIGH_TO_LOW`/`LOW_TO_HIGH`/`NONE`）；
- **API Key 与订阅用量**：创建/重置 UAC API Key；查询订阅周期、各规格席位数量、已分配席位数及剩余 Credits 额度。

> **注意**：文档中多次出现 `ORG_OWNER` 角色定义不一致问题——在[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)返回示例中，`RoleCode` 字段值为 `"ORG_MEMBER"`，但 `RoleId` 为 `"SYSTEM_ROLE_ORG_OWNER"`；而[获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)中明确列出合法 `DefaultRoleId` 为 `SYSTEM_ROLE_ORG_ADMIN` 或 `SYSTEM_ROLE_ORG_MEMBER`，未包含 `ORG_OWNER`。建议以 `GetTokenPlanOrgInviteConfig` 文档定义的角色 ID 为准，`ORG_OWNER` 可能为内部系统角色，不应作为 `DefaultRoleId` 的输入值。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头；不接受 `Authorization: Bearer {API_KEY}`。
- **席位类型（`SeatType` / `SpecType`）**：统一取值为 `standard`、`pro`、`max`，各接口（如 `BatchAssignSeats`、`AddOrganizationMember`、`GetSubscriptionStats`）均保持一致。
- **批量操作参数格式**：数组类参数（如 `AccountIds`、`StatusList`）必须使用 Flat 格式（例如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`），而非 JSON 数组。
- **时间戳单位**：`CycleStartTime`、`CycleEndTime`、`ExpireTime` 等字段单位为**毫秒**（Unix timestamp），非秒。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量，避免硬编码；
2. **SDK 推荐**：优先使用阿里云官方 SDK（如 Python `alibabacloud_tea_openapi`）或 [OpenAPI Explorer](https://api.aliyun.com) 自动生成调用代码，免去手动签名；
3. **Endpoint**：所有接口当前仅支持华北2（北京）地域，固定 Endpoint 为 `https://modelstudio.cn-beijing.aliyuncs.com`；
4. **典型流程**：
   - 调用 `GetTokenPlanAccountDetail` 获取当前账号及所属组织 ID；
   - 调用 `CreateTokenPlanInviteLink` 生成邀请链接，或 `AddOrganizationMember` 直接添加成员；
   - 调用 `BatchAssignSeats` 为成员分配席位；
   - 调用 `GetSubscriptionStats` 实时监控 Credits 剩余量。

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名认证**，明确不支持 `Authorization: Bearer` 方式，尝试使用会导致 `400 Bad Request` 或 `403 Forbidden`；
- **席位回收约束**：`RemoveOrganizationMember` 接口会校验成员是否持有席位，若 `SeatId` 非空则拒绝移除，需先调用 `BatchRevokeSeats` 回收席位；
- **邀请链接唯一性**：`CreateTokenPlanInviteLink` 接口保证组织内仅存在一个有效链接；重复调用返回现有链接，如需更新过期时间，须先调用 `RevokeTokenPlanInviteLink`；
- **参数编码要求**：Query String 中含中文或特殊字符时（如 `Name=新组织名称`），必须按 RFC 3986 百分号编码，否则签名验证失败（`SignatureDoesNotMatch`）；
- **分页默认值**：`ListOrganizationMembers`、`GetSubscriptionSeatDetails` 等分页接口，`PageNum`/`PageNo` 默认为 `1`，`PageSize` 默认为 `20`（最大 `100`），`PageSize=0` 将导致错误。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
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
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


