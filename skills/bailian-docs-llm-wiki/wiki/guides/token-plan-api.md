# token plan api

[Token](../concepts/token.md) Plan API 是一套面向企业组织的账号、成员、席位与订阅管理接口，用于自动化 [Token](../concepts/token.md) Plan 团队版的组织治理、资源分配与用量监控。所有接口均基于阿里云 OpenAPI 规范（`ACS3-HMAC-SHA256` 签名），部分购买/变配类操作调用 BssOpenApi（`HMAC-SHA1`）。不支持 `Authorization: Bearer {API_KEY}` 认证方式，必须使用 AccessKey 签名。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理层**，包括：
- **组织与账号管理**：获取账号详情、查询/修改组织信息（[获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)、[获取组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-organization.md)）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，以及统计成员与席位关系（[添加成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/add-organization-member.md)、[查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md)、[获取成员与席位统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)）；
- **席位管理**：批量分配/回收席位、查询席位明细（[批量分配席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）；
- **订阅与用量**：获取席位与 Credits 统计、查询共享包明细（[获取订阅席位与额度统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)）；
- **邀请与 API Key**：创建/撤销邀请链接、配置邀请策略、生成/重置 API Key（[创建成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)、[创建 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/create-token-plan-key.md)）。

> **注意**：文档 13（[席位购买与变配](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md)）明确指出其 Endpoint 为 `business.aliyuncs.com` 且使用 BssOpenApi（`2023-09-30` 版本），而其余所有管理类接口（如文档 1–12、19–32）均使用 `modelstudio.cn-beijing.aliyuncs.com` 和 `2026-02-10` 版本。二者签名算法（`HMAC-SHA1` vs `ACS3-HMAC-SHA256`）、Endpoint、参数格式均不同，不可混用。

## 关键参数

- **认证参数**：必须通过 AccessKey 签名，需携带 `x-acs-action`（如 `GetTokenPlanAccountDetail`）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头。推荐使用阿里云 SDK 自动处理。
- **席位规格（SpecType）**：在成员添加、席位分配、订阅统计等多处出现，取值统一为 `standard` / `pro` / `max`（见 [添加成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/add-organization-member.md) 和 [查询订阅席位明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）。
- **角色编码（RoleCode）**：组织角色为 `ORG_OWNER` / `ORG_ADMIN` / `ORG_MEMBER`；工作空间角色为 `WS_ADMIN` / `WS_MEMBER`（见 [获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)）。
- **分页参数**：`PageNo`（从 1 开始）和 `PageSize`（默认 20，最大 100），广泛用于列表接口（如 [查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md)、[查询订阅席位明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）。

## 使用方式

1. **环境准备**：配置环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，并确保 RAM 用户已授予对应 API 的调用权限（如 `tokenplan:ListOrganizationMembers`）。
2. **调用流程**：
   - 对于组织/成员/席位管理类接口（`modelstudio.cn-beijing.aliyuncs.com`），使用 `ACS3-HMAC-SHA256` 签名，按文档指定 `x-acs-action` 和 `x-acs-version`；
   - 对于购买/续费/退订等计费操作（`business.aliyuncs.com`），使用 BssOpenApi 的 `HMAC-SHA1` RPC 签名，`Action` 参数（如 `CreateCreditSeat`）必须显式传递；
3. **参数传递**：
   - GET 接口参数全部通过 Query String 传递；
   - POST 接口参数根据文档要求，或通过 Query String（如 `UpdateOrganization`），或通过表单（如 `CreateCreditSeat`），数组参数统一采用 Flat 格式（如 `AccountIds.1=acc_1&AccountIds.2=acc_2`）；
4. **结果解析**：所有接口返回 `Success: boolean` 字段作为主状态标识，业务数据位于 `Data` 字段；BssOpenApi 接口外层 `Success` 表示请求受理成功，退款类操作需检查 `Data.Success`（见 [退订席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)）。

## 限制和注意事项

- **地域限制**：所有 `modelstudio.cn-beijing.aliyuncs.com` 接口仅支持华北2（北京）地域；BssOpenApi 接口为中国站（`business.aliyuncs.com`）。
- **席位约束**：移除成员前会校验其是否持有席位，若已分配则拒绝移除（见 [移除成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/remove-organization-member.md)）；退订席位仅支持“未使用 Credits”的席位（见 [退订席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)）。
- **幂等性**：BssOpenApi 类接口（如 `CreateCreditSeat`、`AddCreditSeats`）必须传入 `ClientToken` 以保证幂等；OpenAPI 类接口无内置幂等机制，需业务侧控制。
- **API Key 安全**：`PlainApiKey` 仅在创建（[创建 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/create-token-plan-key.md)）和重置（[重置 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）时返回一次，务必安全保存，后续无法再次获取。
- **邀请链接唯一性**：一个组织同一时间只允许存在一个有效邀请链接，重复调用创建接口将返回现有链接而非新建（见 [创建成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)）。

## 来源文档

- [获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [席位购买与变配](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [升级席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [退订席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [续费席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [邀请管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription.md)
- [组织与账号](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization.md)
- [获取订阅席位与额度统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [成员管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member.md)


