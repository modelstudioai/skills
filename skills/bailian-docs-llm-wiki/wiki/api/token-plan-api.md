# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及邀请全生命周期管理接口集合，用于自动化配置 TokenPlan 服务资源。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer` 类型 API Key 认证。开发者需使用阿里云 AccessKey（而非 TokenPlan 自身的 API Key）调用，适用于组织级权限管控与批量运维场景。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源编排**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织元信息（如名称、描述、状态）  
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持席位绑定状态检查（[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 中明确要求“已获取阿里云账号或 RAM 用户的 AccessKey”）  
- **席位精细化运营**：批量分配/回收席位、分页查询席位明细、统计已分配/未分配席位数（[获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md) 提供 `SeatedMemberCount`/`UnseatedMemberCount` 等关键指标）  
- **邀请流程自动化**：创建/获取/撤销邀请链接，配置默认角色与席位分配策略  
- **订阅与用量监控**：获取席位与 Credits 统计、查询共享包明细  
- **API Key 管理**：为成员创建及重置 UAC API Key（注意：此 Key 用于调用百炼模型 API，与 Token Plan 自身管理 API 的认证方式不同）

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回字段 `RoleCode: "ORG_OWNER"`），但 [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md) 接口的 `NewRoleCode` 参数说明仅列出 `ORG_ADMIN` 和 `ORG_MEMBER`，未提及 `ORG_OWNER`。实际调用时 `ORG_OWNER` 角色不可通过该接口变更，需通过组织 Owner 账号直接操作。

## 关键参数

- **认证参数**：所有接口必须携带标准阿里云 OpenAPI 公共请求头：`x-acs-action`（接口动作名）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization`。  
- **地域 Endpoint**：当前仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com`。  
- **席位规格（SpecType/SeatType）**：统一取值为 `standard` / `pro` / `max`，在 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 等多处文档中保持一致。  
- **数组参数格式**：`AccountIds`、`StatusList` 等数组类型参数必须使用 Flat 格式（如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`），而非 JSON 数组字符串；例外是 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md) 的 `Items` 参数需传入 URL 编码后的 JSON 字符串。

## 使用方式

1. **前置准备**：确保使用具备 `AliyunTokenPlanFullAccess` 或最小化自定义策略的阿里云 RAM 用户 AccessKey，并推荐配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET`。  
2. **签名调用**：  
   - 手动计算：严格遵循 `ACS3-HMAC-SHA256` 签名算法，对 CanonicalRequest 进行 RFC 3986 百分号编码（尤其 Query String 中中文需编码）。  
   - 推荐方案：使用阿里云官方 SDK（Python/Java/Go 等）或 [OpenAPI Explorer](https://api.aliyun.com) 自动生成调用代码，避免签名错误。  
3. **典型流程示例**：  
   - 创建组织 → 调用 `UpdateOrganization` 设置基本信息  
   - 配置邀请：`SetTokenPlanOrgInviteConfig` 设定默认角色与席位策略 → `CreateTokenPlanInviteLink` 生成链接  
   - 批量纳管：`AddOrganizationMember` 添加成员 → `BatchAssignSeats` 分配席位 → `ListOrganizationMembers` 验证结果  

## 限制和注意事项

- **认证隔离**：Token Plan 管理 API **仅接受阿里云 AccessKey 签名**，明确不支持 `Authorization: Bearer {TokenPlan_API_Key}`（所有文档均强调此限制，如 [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)）。TokenPlan 自身的 API Key（通过 `CreateTokenPlanKey` 创建）仅用于调用百炼模型服务。  
- **席位强约束**：移除成员前会校验其是否持有席位（[移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md) 文档明确说明“持有席位时拒绝移除”），需先调用 `BatchRevokeSeats` 回收席位。  
- **幂等性与覆盖逻辑**：`CreateTokenPlanInviteLink` 接口规定“用户只允许拥有一个有效的邀请链接”，重复调用将返回现有链接而非创建新链接；若需刷新，必须先调用 `RevokeTokenPlanInviteLink`。  
- **分页参数**：`PageNo`/`PageNum` 与 `PageSize` 在多个接口（如 `ListOrganizationMembers`, `GetSubscriptionSeatDetails`）中存在命名不一致（`PageNo` vs `PageNum`），但语义相同，均从 1 开始计数。  
- **数据一致性**：`GetOrganizationMemberSeatStats` 返回的 `SeatedMemberCount` 与 `GetSubscriptionStats` 中 `AssignedSeats` 应逻辑一致，但因统计口径（实时 vs 缓存）可能存在短暂延迟，生产环境建议以 `GetSubscriptionStats` 的 `AssignedSeats` 为准。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)


