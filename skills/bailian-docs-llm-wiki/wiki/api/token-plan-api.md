# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及 API Key 全生命周期管理接口集合，用于构建私有化或混合云场景下的 [Token](../concepts/token.md) 分配与治理能力。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer` [Token](../concepts/token.md) 方式。开发者需使用阿里云 AccessKey（推荐通过环境变量配置）调用，建议优先使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com) 降低签名复杂度。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源编排**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织信息（如名称、描述）；
- **成员全链路管理**：添加/移除成员、批量修改角色、查询成员列表及统计（含席位分配状态）；
- **席位精细化管控**：按规格（`standard`/`pro`/`max`）批量分配/回收席位，分页查询席位明细及状态；
- **邀请机制配置**：创建/撤销/获取邀请链接，设置默认角色与席位分配策略；
- **API Key 生命周期管理**：为成员创建、重置（rotate）UAC API Key；
- **订阅与用量洞察**：获取席位与 Credits 统计、查询共享包明细。

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)返回字段 `RoleCode: "ORG_OWNER"`），但实际权限体系中该角色未在 `update-organization-member.md` 或 `add-organization-member.md` 的 `OrgRoleCode` 可选值中定义，仅支持 `ORG_ADMIN` 和 `ORG_MEMBER`。请以接口参数约束为准，`ORG_OWNER` 为只读标识，不可通过 API 设置。

## 关键参数

- **认证参数**：所有接口必须携带 `x-acs-action`（如 `GetOrganization`）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法固定为 `ACS3-HMAC-SHA256`。
- **席位规格（`SpecType` / `SeatType`）**：统一取值为 `standard`、`pro`、`max`，见[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)与[获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)。
- **数组参数格式**：批量操作（如 `AccountIds`）必须使用 Flat 格式（`AccountIds.1=xxx&AccountIds.2=yyy`），而非 JSON 数组；`Items` 类参数（如 `batch-revoke-seats.md`）需对 JSON 字符串做 URL 编码。
- **分页参数**：`PageNo`/`PageNum`（从 1 开始）、`PageSize`（默认 10–20，最大 100），不同接口命名不一致，需按具体文档确认。

## 使用方式

1. **准备凭证**：确保已获取具备 `TokenPlanFullAccess` 或最小粒度 RAM 权限的 AccessKey，并配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`；
2. **选择入口**：所有接口 Endpoint 均位于华北2（北京）地域：`https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`；
3. **发起请求**：
   - GET 接口（如 `/tokenplan/account`）无请求体，参数通过 Query String 传递；
   - POST 接口（如 `/tokenplan/organization/member-additions`）参数也全部通过 Query String 传递（非 JSON Body）；
4. **构造签名**：使用阿里云 SDK（Python/Java/Go 等）自动处理签名最可靠；若手动构造，务必严格遵循 RFC 3986 对 Query String 进行百分号编码（如中文需编码），否则返回 `SignatureDoesNotMatch`；
5. **解析响应**：所有接口返回标准 `Success: boolean` 字段，业务数据位于 `Data` 字段内；错误信息通过 `Code`/`Message` 返回，详见[错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 限制和注意事项

- **认证方式强制约束**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`（见[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)、[获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)等多处强调）；
- **席位与成员强绑定**：移除成员前必须先回收其席位，否则调用 `RemoveOrganizationMember` 将被拒绝（见[移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接；重复调用 `CreateTokenPlanInviteLink` 将返回已有链接，需先调用 `RevokeTokenPlanInviteLink` 失效旧链接（见[创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)）；
- **API Key 安全**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 和 `RotateTokenPlanKey` 响应中**一次性返回**，后续无法再次获取，请务必安全存储；
- **地域硬编码**：当前所有接口仅开放华北2（北京）Endpoint，暂不支持多地域部署。

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
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


