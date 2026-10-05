# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的统一管控接口集合，基于阿里云 OpenAPI 规范实现。所有接口均需使用 AccessKey 签名认证（`ACS3-HMAC-SHA256`），不支持 `Bearer {API_KEY}` 方式。开发者可通过 SDK 或 OpenAPI Explorer 快速集成，适用于组织治理、自动化开通与资源配额调度等场景。

## 支持的模型/功能

Token Plan API 不涉及模型调用，而是提供完整的**组织级资源治理能力**，覆盖以下核心功能域：

- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）  
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持席位分配状态过滤与统计  
- **席位精细化运营**：批量分配/回收席位、查询席位明细与订阅统计、管理共享包  
- **邀请机制配置**：创建/获取/撤销邀请链接，设置默认角色与席位分配策略  
- **API Key 安全管控**：为成员创建及重置专属 API Key  
- **订阅与用量洞察**：获取席位总数、已分配数、剩余 Credits 等关键指标  

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回字段 `RoleCode: "ORG_OWNER"`），但实际权限体系中该角色未在 [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md) 的 `NewRoleCode` 可选值中列出（仅支持 `ORG_ADMIN`/`ORG_MEMBER`），表明 `ORG_OWNER` 为系统固定主账号角色，不可通过 API 修改。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头；推荐使用阿里云 SDK 自动签名。
- **席位规格（`SpecType` / `SeatType`）**：统一取值为 `standard`（标准）、`pro`（高级）、`max`（尊享），见 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 与 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)。
- **分页参数**：`PageNo`/`PageNum`（从 1 开始）、`PageSize`（默认 10–20，最大 100），不同接口命名不一致（如 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 用 `PageNum`，而 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 用 `PageNo`），需按各接口文档严格使用。
- **数组参数格式**：采用 Flat 格式（如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`），非 JSON 数组或逗号分隔。

## 使用方式

1. **前置准备**：确保 RAM 用户已授予 `AliyunModelStudioFullAccess` 或最小化自定义策略（含 `modelstudio:ListOrganizationMembers`, `modelstudio:BatchAssignSeats` 等 Action）。
2. **Endpoint**：全部接口仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`。
3. **典型流程**：
   - 调用 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 确认当前组织 ID（`OrgId`）
   - 调用 [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md) 查看默认策略
   - 创建邀请链接 → 新成员注册 → 调用 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 确认入账 → 批量分配席位
4. **调试建议**：优先使用 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/) 实时生成签名请求，避免手动计算错误。

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`（见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)、[添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 等多处强调）。
- **席位强约束**：移除成员前必须确保其无已分配席位（[移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md) 明确说明“持有席位时拒绝移除”）；回收席位后，成员将无法调用模型 API。
- **幂等性与 Token 安全**：邀请链接 Token 仅在创建/获取时返回一次（[创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)、[获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)），且用户同一时刻仅允许一个有效链接，需自行保管。
- **数据一致性**：`GetSubscriptionStats` 返回的 `SeatRemainingCredits` 为当前周期实时剩余额度，但 `ListOrganizationMembers` 中 `PackLimitInfo.CycleSurplusValue` 字段存在同名但结构嵌套更深的冗余字段，以 `GetSubscriptionStats` 为准。

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
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)


