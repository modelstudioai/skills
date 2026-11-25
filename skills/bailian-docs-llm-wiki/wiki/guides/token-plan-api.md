# token plan api

[Token](../concepts/token.md) Plan API 是一套面向企业组织的账号、成员、席位与订阅管理接口，用于自动化 [Token](../concepts/token.md) Plan 团队版的组织治理、成员邀请、席位分配与用量监控。所有接口均基于阿里云 OpenAPI 规范，采用 AccessKey 签名认证（`ACS3-HMAC-SHA256`），不支持 `Bearer` 类型 API Key 认证。核心能力覆盖组织生命周期管理、成员角色与席位绑定、邀请链路控制及订阅状态查询。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型调用本身，而是提供完整的**组织级资源管控能力**，主要包括：
- **组织管理**：创建/查询/更新组织信息，获取组织层级结构与归属关系（[获取组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-organization.md)）；
- **成员管理**：添加、移除、批量查询与角色变更成员，支持按席位分配状态过滤（[查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md)）；
- **席位管理**：分层操作——在组织层批量分配/回收席位（如 `BatchAssignSeats`），在订阅层执行购买、升级、退订等变配动作（如 `UpgradeCreditSeat`）；
- **邀请管理**：生成、获取、撤销邀请链接，并可配置默认角色与席位分配策略（[设置邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)）；
- **订阅与用量**：查询席位统计、Credits 剩余量、共享包明细及周期额度刷新状态（[获取订阅席位与额度统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)）。

> **注意**：文档中存在两类不同 Endpoint 与签名机制的接口：  
> - `modelstudio.cn-beijing.aliyuncs.com` 下的接口（如成员、席位分配、邀请）统一使用 `ACS3-HMAC-SHA256` 签名；  
> - `business.aliyuncs.com` 下的席位购买类接口（如 `CreateCreditSeat`, `UpgradeCreditSeat`）属于 BssOpenApi，使用 `HMAC-SHA1` RPC 签名。二者权限、Endpoint 和签名算法不可混用。

## 关键参数

- **认证参数**：必须通过环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 配置，并在请求头中携带 `x-acs-action`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 字段。
- **席位规格（`SpecType` / `SeatType`）**：取值为 `standard`、`pro` 或 `max`，贯穿席位分配（`BatchAssignSeats`）、回收（`BatchRevokeSeats`）、查询（`GetSubscriptionSeatDetails`）及变配（`UpgradeCreditSeat`）全流程。
- **成员标识**：主要使用 `AccountId`（如 `acc_123456789`），部分接口（如 `AddOrganizationMember`）支持通过 `AccountName` 创建新账号。
- **幂等性控制**：BssOpenApi 类接口（席位购买/变配）必须传入 `ClientToken`，确保重复请求不会产生重复订单。
- **分页参数**：`PageNo` / `PageSize`（默认 1/10 或 1/20，最大 100），适用于 `ListOrganizationMembers`、`GetSubscriptionSeatDetails` 等列表接口。

## 使用方式

1. **初始化认证**：配置阿里云 AccessKey，并优先使用阿里云 SDK（如 Python 的 `alibabacloud_tea_openapi`）自动处理签名，避免手动构造 CanonicalRequest；
2. **选择接口路径**：
   - 组织/成员/席位分配/邀请类操作 → 调用 `modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`；
   - 席位购买、升级、退订、续费等计费操作 → 调用 `business.aliyuncs.com/` 并指定 `Action=XXX`（如 `Action=UpgradeCreditSeat`）；
3. **构造请求**：
   - GET 接口（如 `GetOrganizationMemberSeatStats`）将参数拼入 Query String；
   - POST 接口（如 `BatchAssignSeats`）使用 Flat 格式传递数组（`AccountIds.1=...&AccountIds.2=...`），或对 JSON 字符串（如 `Items=[{...}]`）做 URL 编码；
4. **解析响应**：所有接口返回统一结构体，`Success: true` 表示业务成功，`Code` 和 `Message` 用于诊断错误；关键业务数据位于 `Data` 字段内。

## 限制和注意事项

- **认证方式严格限定**：所有接口均**不支持 `Authorization: Bearer {API_KEY}`**，仅接受 AccessKey 签名（[获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 明确强调此限制）；
- **席位回收前提**：`BatchRevokeSeats` 要求目标成员**未持有已分配席位**，否则调用失败；而 `RemoveOrganizationMember` 在移除前会主动校验席位占用，若存在席位则拒绝移除；
- **邀请链接唯一性**：`CreateTokenPlanInviteLink` 接口保证组织下**仅存在一个有效邀请链接**，重复调用返回已有链接，需先调用 `RevokeTokenPlanInviteLink` 失效后方可新建；
- **API Key 安全**：`CreateTokenPlanKey` 返回的 `PlainApiKey` **仅在创建时返回一次**，后续无法再次获取，务必安全存储；重置（`RotateTokenPlanKey`）后旧 Key 立即失效；
- **地域与 Endpoint 绑定**：当前所有 `modelstudio.cn-beijing.aliyuncs.com` 接口仅支持华北2（北京）地域，暂无多地域部署说明。

## 来源文档

- [组织与账号](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-organization.md)
- [成员管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/add-organization-member.md)
- [修改组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/update-organization.md)
- [移除成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat.md)
- [查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md)
- [批量回收席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [批量分配席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [席位购买与变配](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [升级席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [查询订阅席位明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [退订席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [续费席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [邀请管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [设置邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [修改成员角色](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/update-organization-member.md)


