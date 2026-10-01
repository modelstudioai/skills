# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及邀请等全生命周期管理的后端服务接口集合，基于阿里云 OpenAPI 规范实现。所有接口均需通过 AccessKey 签名认证（`ACS3-HMAC-SHA256`），不支持 `Bearer {API_KEY}` 方式。开发者可通过阿里云 SDK 或 OpenAPI Explorer 快速集成，无需手动构造签名。

## 支持的模型/功能

Token Plan API 不涉及模型调用，而是聚焦于**组织治理与资源配额管理**，核心能力包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织信息（如名称、描述）[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)；
- **成员全链路管理**：添加/查询/修改/移除成员，支持批量操作与角色变更（`ORG_OWNER`/`ORG_ADMIN`/`ORG_MEMBER`）；
- **席位精细化管控**：按 `standard`/`pro`/`max` 三档规格分配、回收席位，并支持分页查询席位明细与绑定状态 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)；
- **邀请与配置中心**：创建/获取/撤销邀请链接，设置默认角色与席位分配策略（如 `HIGH_TO_LOW`）；
- **API Key 安全体系**：为成员创建、重置 UAC API Key，明文 Key 仅在创建/重置时返回一次；
- **订阅与用量洞察**：获取席位总数、已分配数、剩余 Credits 及共享包明细 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)。

> **注意**：文档中多处提及 `OrgRoleCode` 允许值为 `ORG_OWNER`/`ORG_ADMIN`/`ORG_MEMBER`（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)），但 [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md) 的 `DefaultRoleId` 示例值为 `SYSTEM_ROLE_ORG_ADMIN`。实际调用应以接口文档中 `RoleCode` 字段定义为准（`ORG_ADMIN`），`SYSTEM_ROLE_*` 前缀为内部标识，外部调用请勿使用。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法固定为 `ACS3-HMAC-SHA256`。
- **席位规格**：`SpecType` / `SeatType` 参数统一取值为 `standard`、`pro`、`max`，大小写敏感，其他值将导致 `InvalidParameter` 错误。
- **数组参数格式**：批量操作（如 `AccountIds`、`StatusList`）必须使用 Flat 格式（`ParamName.1=value1&ParamName.2=value2`），不可传 JSON 数组字符串；`Items` 类参数（如 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)）需对 JSON 值做 URL 编码。
- **分页参数**：`PageNo`（从 1 开始）、`PageSize`（默认 20，最大 100），部分接口（如 `list-organization-members`）同时支持 `PageNum` 别名，但以文档明确标注的参数名为准。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量，避免硬编码；
2. **SDK 推荐**：优先使用阿里云官方 SDK（如 Python `alibabacloud_tea_openapi`），自动处理签名与重试；
3. **Endpoint**：华北2（北京）地域统一为 `https://modelstudio.cn-beijing.aliyuncs.com`，路径前缀为 `/tokenplan/`；
4. **典型流程**：
   - 调用 `GetTokenPlanAccountDetail` 获取当前账号及所属组织 ID；
   - 通过 `ListOrganizationMembers` 查询待操作成员，再调用 `BatchAssignSeats` 分配席位；
   - 新成员加入前，先 `CreateTokenPlanInviteLink` 生成链接，或 `AddOrganizationMember` 直接创建；
   - 用量监控使用 `GetSubscriptionStats` 获取周期内 Credits 剩余量。

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名**，`Authorization: Bearer {API_KEY}` 将被拒绝（见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 明确说明）；
- **席位约束**：移除成员前必须确保其未持有席位（`RemoveOrganizationMember` 接口会校验并拒绝），否则需先调用 `BatchRevokeSeats` 回收；
- **幂等性**：`CreateTokenPlanInviteLink` 在存在有效链接时直接返回原 Token，非幂等创建；如需新链接，必须先调用 `RevokeTokenPlanInviteLink`；
- **数据一致性**：`GetOrganizationMemberSeatStats` 返回的 `SeatedMemberCount` 与 `ListOrganizationMembers?HasSeat=true` 结果应一致，若偏差需检查缓存延迟（通常 < 5 秒）；
- **错误处理**：通用错误码参考 [错误信息](../../raw/model-api-reference/preparations/error-code.md)，重点关注 `SignatureDoesNotMatch`（签名计算错误）、`InvalidParameter`（参数非法）、`Forbidden`（RAM 权限不足）。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
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


