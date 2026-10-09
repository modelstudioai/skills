# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的统一管控接口集合，用于实现 [Token](../concepts/token.md) 配额的精细化分配与生命周期管理。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，**不支持 `Authorization: Bearer {API_KEY}` 方式**。开发者需使用阿里云 AccessKey 进行调用，并建议通过阿里云 SDK 或 OpenAPI Explorer 简化签名流程。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于企业级资源治理，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持批量操作；
- **席位（Seat）精细化分配**：支持 `standard`/`pro`/`max` 三类规格的席位批量分配与回收，以及明细查询；
- **邀请体系控制**：创建、获取、撤销邀请链接，并可配置默认角色与席位分配策略；
- **API Key 安全管控**：创建与重置 UAC API Key，明文 Key 仅在创建/重置响应中返回一次；
- **订阅与用量统计**：获取席位总数、已分配数、剩余 Credits 及共享包明细。

> **注意**：文档中多次出现 `ORG_OWNER` 角色定义不一致问题——[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 的返回示例中 `RoleCode` 为 `"ORG_MEMBER"`，但实际应为 `"ORG_OWNER"`；而 [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md) 中明确列出合法值为 `SYSTEM_ROLE_ORG_ADMIN`/`SYSTEM_ROLE_ORG_MEMBER`。请以 [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md) 文档中定义的 `DefaultRoleId` 取值为准，避免硬编码 `ORG_OWNER`。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 和 `Authorization` 头，签名算法固定为 `ACS3-HMAC-SHA256`。
- **席位规格（SpecType/SeatType）**：统一取值为 `standard`、`pro`、`max`，各接口（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)）均保持一致。
- **数组参数格式**：批量操作（如 `AccountIds`、`StatusList`）必须使用 Flat 格式（如 `AccountIds.1=acc_123&AccountIds.2=acc_456`），而非 JSON 数组。
- **分页参数**：`PageNo`/`PageNum`（起始为 1）与 `PageSize`（默认 10–20，最大 100）在列表类接口中广泛使用。

## 使用方式

1. **准备凭证**：确保已获取具备 `TokenPlanFullAccess` 或最小权限策略的阿里云 AccessKey，并推荐配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`。
2. **选择地域 Endpoint**：当前仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`。
3. **发起请求**：
   - GET 接口（如 `/tokenplan/account`、`/tokenplan/subscription/stats`）直接拼接 Query 参数；
   - POST 接口（如 `/tokenplan/organization/members/update`、`/tokenplan/api-keys`）将参数置于 URL Query String（非 Request Body）；
   - 所有请求必须按 OpenAPI 规范计算签名，**严禁明文传输 AccessKey**。
4. **处理响应**：检查 `Success: true` 及 `HttpStatusCode: 200`，解析 `Data` 字段；失败时依据 `Code` 和 `Message` 排查（参考 [错误信息](../../raw/model-api-reference/preparations/error-code.md)）。

## 限制和注意事项

- **认证方式强制约束**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Bearer Token` 认证，此设计与百炼模型推理 API 的 `Authorization: Bearer` 方式形成隔离，需严格区分调用上下文。
- **席位强校验逻辑**：移除成员前会校验其是否持有席位（[移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)），若已分配则拒绝操作；同理，[添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 时 `SpecType` 为空则不分配席位。
- **邀请链接唯一性**：每个组织仅允许存在一个有效邀请链接，重复调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 将返回现有链接，需先调用 [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md) 再新建。
- **敏感信息保护**：API Key 明文（`PlainApiKey`）**仅在创建或重置响应中返回一次**，后续无法再次获取，务必安全存储；返回的 `MaskedApiKey` 用于日志脱敏展示。
- **时间戳精度**：`ExpireTime`（毫秒）、`CycleStartTime`（毫秒）等字段均为 Unix 时间戳（毫秒级），非秒级，解析时需注意单位。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


