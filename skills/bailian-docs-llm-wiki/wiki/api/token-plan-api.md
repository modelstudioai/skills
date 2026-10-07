# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位与订阅管理的后端控制面接口集合，用于自动化配置 [Token](../concepts/token.md)Plan 企业版资源配额与访问权限。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，**不支持 `Authorization: Bearer {API_KEY}` 方式**。开发者需使用阿里云 AccessKey（主账号或具备 RAM 权限的子用户）调用，推荐通过阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com) 发起请求以简化签名流程。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于企业级资源治理，包括：
- **组织与账号管理**：获取/修改组织信息、查询当前账号详情（含组织成员关系树）  
- **成员全生命周期管理**：添加/移除/更新角色、批量查询成员列表、统计成员与席位分布（如 [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)）  
- **席位精细化分配**：支持 `standard`/`pro`/`max` 三类规格的席位批量分配与回收，以及按状态分页查询明细（见 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）  
- **邀请与配置管理**：生成/撤销邀请链接、设置默认角色与席位分配策略（如 [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)）  
- **API Key 与订阅管理**：为成员创建/重置 UAC API Key；查询订阅周期、席位用量及共享包明细  

> **注意**：文档中多次出现 `ORG_OWNER` 与 `SYSTEM_ROLE_ORG_OWNER` 的混用（如文档 3 返回示例中 `RoleCode: "ORG_MEMBER"` 但描述为 `ORG_OWNER` 角色），实际角色编码应以 [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md) 和 RAM 权限模型定义为准，`SYSTEM_ROLE_*` 前缀为内部系统角色标识，对外暴露的 `RoleCode` 应为 `ORG_OWNER`/`ORG_ADMIN`/`ORG_MEMBER`。

## 关键参数

- **认证参数**：所有接口必须携带 `x-acs-action`（接口动作名）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头。`x-acs-action` 值严格对应接口文档（如 `GetOrganization`, `BatchAssignSeats`）。  
- **地域与 Endpoint**：当前仅支持华北2（北京）地域，固定 Endpoint 为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`。  
- **Query String 参数**：  
  - 分页类：`PageNum`/`PageNo`（从 1 开始）、`PageSize`（默认 20，最大 100）  
  - 席位规格：`SpecType` 或 `SeatType`，取值为 `standard`/`pro`/`max`（见 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 与 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)）  
  - 数组传递：`AccountIds.1=xxx&AccountIds.2=yyy`（Flat 格式），`StatusList.1=NORMAL` 等  
- **必选字段**：`AddOrganizationMember` 要求 `AccountName` 和 `OrgRoleCode`；`CreateTokenPlanKey` 要求 `AccountId`；`SetTokenPlanOrgInviteConfig` 要求 `DefaultRoleId` 和 `SeatAssignStrategy`。

## 使用方式

1. **环境准备**：将 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 配置为环境变量，避免硬编码。  
2. **签名调用**：  
   - 手动计算：按 `ACS3-HMAC-SHA256` 算法生成签名（参考各文档“请求示例”中的 `curl` 命令结构）  
   - 推荐方式：使用阿里云官方 SDK（Python/Java/Go 等），自动处理签名、重试与错误解析  
3. **典型流程**：  
   - 先调用 `GetTokenPlanAccountDetail` 获取当前账号所属 `OrgId`  
   - 通过 `GetOrganization` 确认组织状态，再用 `UpdateOrganization` 修改基本信息  
   - 使用 `AddOrganizationMember` 添加成员并指定 `SpecType`，或先 `ListOrganizationMembers` 查询后 `BatchAssignSeats` 分配席位  
   - 为成员调用 `CreateTokenPlanKey` 生成专属 API Key，后续可 `RotateTokenPlanKey` 安全轮换  
4. **调试工具**：所有接口均在 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10) 提供在线调试，支持自动生成签名代码。

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Bearer Token` 认证（文档 2/3/5/6 等均强调此点）。  
- **席位约束**：`RemoveOrganizationMember` 会校验成员是否持有席位，**持有席位时拒绝移除**，需先调用 `BatchRevokeSeats` 回收（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）。  
- **邀请链接唯一性**：`CreateTokenPlanInviteLink` 接口保证单组织下仅存在一个有效链接；若需更新，必须先调用 `RevokeTokenPlanInviteLink`（文档 25 明确说明）。  
- **时间格式**：`GmtCreate`/`GmtModified` 等字段为 ISO 8601 字符串（如 `"2025-11-20T02:26:35Z"`），而 `CycleStartTime`/`ExpireTime` 等为毫秒级时间戳（如 `1778379206`）。  
- **错误处理**：统一返回 `Success: boolean` 字段，失败时 `Code` 和 `Message` 提供具体错误码（详见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)）。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
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
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)


