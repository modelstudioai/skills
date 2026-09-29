# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位与订阅管理的后端控制面接口集合，用于自动化配置 TokenPlan 服务权限与资源配额。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 Bearer Token 方式。开发者需使用阿里云 AccessKey 进行调用，并通过 RAM 授权获得对应操作权限。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源编排**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)；
- **成员全生命周期管理**：添加、移除、角色变更、批量查询及统计（含席位分配状态）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)；
- **席位精细化运营**：批量分配/回收席位、查询席位明细与订阅统计，支持 `standard`/`pro`/`max` 三档规格 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)；
- **邀请与 API Key 管理**：创建/获取/撤销邀请链接、设置默认邀请策略、生成及重置 UAC API Key；
- **订阅与用量洞察**：获取席位与 Credits 额度统计、查询共享包明细。

> **注意**：文档中多次出现 `ORG_OWNER` 角色定义不一致问题——在[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)返回示例中，`RoleCode` 字段值为 `"ORG_MEMBER"`，但角色描述明确为 `"ORG_OWNER"`；而[获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)中 `DefaultRoleId` 的合法枚举仅列出 `SYSTEM_ROLE_ORG_ADMIN` 和 `SYSTEM_ROLE_ORG_MEMBER`，未包含 `ORG_OWNER`。实际调用应以 `GetOrganizationMemberSeatStats` 接口返回的 `OwnerRoleUserCount` 字段为准，该角色由系统自动赋予组织创建者，不可通过 `UpdateOrganizationMember` 修改。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`（固定版本）、`x-acs-date`（ISO8601 UTC 时间）、`x-acs-signature-nonce`（唯一随机字符串）、`Authorization`（含签名）等标准 OpenAPI 头。
- **席位规格（SpecType/SeatType）**：统一取值为 `standard`、`pro`、`max`，各接口（如 `AddOrganizationMember`、`BatchAssignSeats`、`GetSubscriptionStats`）均严格遵循此枚举，无大小写变体。
- **分页参数**：`PageNo`/`PageNum`（从 1 开始）与 `PageSize`（默认 10 或 20，最大 100），不同接口命名不一致（如 `list-organization-members` 用 `PageNum`，`get-subscription-seat-details` 用 `PageNo`），需按具体接口文档使用。
- **数组参数格式**：`AccountIds`、`StatusList` 等数组类型均采用 Flat 格式（如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`），非 JSON 数组或逗号分隔。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量，避免硬编码密钥；
2. **权限授予**：为 RAM 用户授予 `AliyunModelStudioFullAccess` 或最小化自定义策略（需包含 `modelstudio:TokenPlan*` 资源操作权限）；
3. **调用方式**：
   - **推荐**：使用阿里云 SDK（Python/Java/Go 等），自动处理签名与请求构造；
   - **调试**：通过 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/) 生成代码或发起在线请求；
   - **手动**：按 RFC 3986 对 Query String 进行百分号编码（尤其含中文时），再计算 `ACS3-HMAC-SHA256` 签名；
4. **Endpoint**：当前仅支持华北2（北京）地域，固定域名 `https://modelstudio.cn-beijing.aliyuncs.com`。

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`（见各文档“认证方式”章节），尝试使用将返回 `400 Bad Request`；
- **席位强约束**：`RemoveOrganizationMember` 接口会校验成员是否持有席位，若 `SeatAssigned=true` 则拒绝移除，须先调用 `BatchRevokeSeats` 回收席位；
- **邀请链接唯一性**：`CreateTokenPlanInviteLink` 接口保证组织内仅存在一个有效链接；重复调用返回现有链接，而非新建——如需刷新，必须先调用 `RevokeTokenPlanInviteLink` [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)；
- **API Key 安全**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 和 `RotateTokenPlanKey` 响应中**一次性返回**，服务端不存储明文，丢失后无法恢复，务必安全保存；
- **时间戳精度**：`x-acs-date` 必须为 ISO8601 格式（如 `2026-01-01T12:00:00Z`），且与服务器时间偏差不得超过 15 分钟，否则返回 `SignatureDoesNotMatch` 错误。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


