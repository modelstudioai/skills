# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及邀请等全生命周期管理能力的 OpenAPI 接口集合，基于阿里云统一认证体系（UAC）和 AccessKey 签名机制实现安全调用。所有接口均需通过 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer Token` 方式，适用于自动化运维、SaaS 集成与内部管理平台对接。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源配额管理**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基础信息（如名称、描述）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持按状态/席位分配情况过滤；
- **席位精细化运营**：支持批量分配/回收 `standard`/`pro`/`max` 三类席位，以及分页查询席位明细与绑定关系；
- **邀请与权限策略**：创建/撤销/获取邀请链接，配置默认角色与席位分配策略（如 `HIGH_TO_LOW`）；
- **API Key 安全管控**：为成员创建、重置独立 API Key，支持描述与密钥轮转；
- **订阅与用量洞察**：获取席位总数、已分配数、剩余 Credits 及共享包明细 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)。

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如文档2返回示例中 `RoleCode: "ORG_MEMBER"` 但 `RoleId: "SYSTEM_ROLE_ORG_OWNER"`），与文档10统计字段 `OwnerRoleUserCount` 的语义存在不一致；实际使用应以 `RoleCode` 字段为准，`ORG_OWNER` 并非标准可设角色，主账号权限由系统隐式赋予，不可通过 `UpdateOrganizationMember` 修改。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 和 `Authorization` 头，签名算法固定为 `ACS3-HMAC-SHA256`；
- **席位类型（`SeatType` / `SpecType`）**：取值严格限定为 `standard`、`pro`、`max`，大小写敏感，文档5、12、14、23均明确列出此枚举；
- **角色编码（`OrgRoleCode` / `RoleCode`）**：仅支持 `ORG_ADMIN` 和 `ORG_MEMBER`（文档5），`ORG_OWNER` 为系统保留，不可显式设置；
- **分页参数**：`PageNo`/`PageNum`（从1开始）、`PageSize`（默认20，最大100），不同接口命名不一致（文档6用 `PageNum`，文档14用 `PageNo`），需按各接口文档要求传入；
- **数组参数格式**：采用 Flat 格式，如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`（文档8、9、12），而非 JSON 数组。

## 使用方式

1. **前置准备**：确保已获取具备 `TokenPlanFullAccess` 或最小化自定义 RAM 权限的 AccessKey，并推荐配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID`/`ALIBABA_CLOUD_ACCESS_KEY_SECRET`；
2. **调用工具**：优先使用阿里云 SDK（Python/Java/Go 等）或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/) 自动生成签名代码，避免手动计算；
3. **典型流程**：
   - 调用 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 确认当前上下文；
   - 通过 `GetOrganization` 获取 `OrgId`，再调用 `ListOrganizationMembers` 查看成员现状；
   - 使用 `AddOrganizationMember` 创建新成员并指定 `SpecType`，或 `BatchAssignSeats` 分配席位；
   - 通过 `GetSubscriptionStats` 实时监控 Credits 余量，结合 `ListSubscriptionSharedPackages` 管理共享资源包。

## 限制和注意事项

- **地域限制**：所有接口当前仅支持华北2（北京）地域，Endpoint 固定为 `https://modelstudio.cn-beijing.aliyuncs.com`；
- **席位强约束**：移除成员前必须确保其未持有席位（文档9明确说明“持有席位时拒绝移除”），否则调用失败；
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接，重复调用 `CreateTokenPlanInviteLink` 将返回已有链接，需先调用 `RevokeTokenPlanInviteLink` 失效旧链接（文档16）；
- **API Key 安全**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 和 `RotateTokenPlanKey` 响应中**一次性返回**，服务端不存储明文，丢失后无法恢复，务必安全保存；
- **时间戳精度**：`x-acs-date` 必须为 ISO 8601 格式（如 `2026-01-01T12:00:00Z`），且与服务器时间偏差不得超过15分钟，否则返回 `InvalidDate` 错误。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)


