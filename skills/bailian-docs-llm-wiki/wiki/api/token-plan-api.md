# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位与订阅管理的后端服务接口集合，用于实现 [Token](../concepts/token.md)Plan 企业版的自动化治理。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer` 类型 API Key 认证。开发者需使用阿里云 AccessKey（推荐通过环境变量配置）并授予对应 RAM 权限方可调用。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于**企业级账号生命周期与资源配额治理**，主要包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织信息（如名称、描述）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，以及统计成员与席位分配状态；
- **席位精细化运营**：批量分配/回收席位、查询席位明细与订阅统计；
- **邀请与权限配置**：创建/获取/撤销邀请链接，设置默认角色与席位分配策略；
- **API Key 安全管控**：为成员创建及重置专属 UAC API Key；
- **订阅与用量洞察**：获取席位与 Credits 额度统计、查询共享包明细。

> **注意**：文档中多次出现“组织 Owner 的业务账号标识（ALIYUN 类型为 aliyunUid，SSO 类型为 userIdentifier）”的描述（见 [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md) 和 [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)），但实际返回字段名为 `OwnerBizAccountId`，且未在接口响应示例中体现 `userIdentifier` 字段，建议以实际返回值为准，避免硬编码解析逻辑。

## 关键参数

- **认证参数**：所有接口必须携带标准阿里云 OpenAPI 公共请求头，包括 `x-acs-action`（如 `GetTokenPlanAccountDetail`）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization`。不支持 `Authorization: Bearer {API_KEY}`。
- **地域与 Endpoint**：当前仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`。
- **席位规格（SpecType）**：统一使用字符串枚举：`standard` / `pro` / `max`，该值贯穿席位分配、查询、统计等所有相关接口（如 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）。
- **分页参数**：`PageNo`（从 1 开始）与 `PageSize`（默认 10 或 20，最大 100）广泛用于列表类接口（如 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)、[查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)）。

## 使用方式

1. **前置准备**：确保已获取具备 `TokenPlanFullAccess` 或最小化自定义 RAM 权限的阿里云 AccessKey，并配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`。
2. **签名调用**：推荐直接使用阿里云官方 SDK（Python/Java/Go 等），自动处理 `ACS3-HMAC-SHA256` 签名；若手动构造请求，务必严格遵循 RFC 3986 对 Query String 进行百分号编码（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 示例中强调）。
3. **典型流程示例**：
   - 调用 `GET /tokenplan/account` 获取当前账号 ID 与所属组织 ID；
   - 调用 `GET /tokenplan/organization/members` 查询待操作成员列表；
   - 调用 `POST /tokenplan/organization/members/update` 批量调整成员角色；
   - 调用 `POST /tokenplan/subscription/seat-assignments` 为新成员分配 `standard` 席位；
   - 调用 `GET /tokenplan/subscription/stats` 实时监控剩余 Credits。

## 限制和注意事项

- **认证方式强制约束**：所有接口明确不支持 `Authorization: Bearer {API_KEY}`，仅接受阿里云 AccessKey 签名，此设计与百炼模型推理 API 的认证方式不同，不可复用同一套鉴权逻辑。
- **席位强依赖检查**：移除成员前会校验其是否持有席位，若 `SeatAssigned: true` 则拒绝移除（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；需先调用 `batch-revoke-seats` 接口回收席位。
- **邀请链接唯一性**：一个组织在同一时间仅允许存在一个有效邀请链接；重复调用 `create-token-plan-invite-link` 将返回现有链接而非新建（见 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)）。
- **API Key 敏感性**：`PlainApiKey` 仅在 `create-token-plan-key` 和 `rotate-token-plan-key` 接口的响应中**一次性返回**，服务端不存储明文，丢失后无法再次获取，需客户端妥善保管。
- **数组参数格式差异**：不同接口对数组参数的序列化要求不一致——`AccountIds` 类参数多采用 Flat 格式（`AccountIds.1=xxx&AccountIds.2=yyy`），而 `Items` 类参数则要求 JSON 字符串并 URL 编码（如 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)），需严格按各接口文档要求构造。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
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
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)


