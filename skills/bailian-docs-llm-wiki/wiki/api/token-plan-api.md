# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位与订阅全生命周期管理接口集合，用于自动化配置 [Token](../concepts/token.md) Plan 团队版资源。所有接口均基于阿里云 OpenAPI 规范（部分席位购买类接口调用 BssOpenApi），需使用 AccessKey 签名认证，**不支持 `Authorization: Bearer {API_KEY}` 方式**。核心能力覆盖组织管理、成员邀请与角色控制、席位分配与回收、API Key 生命周期管理，以及订阅统计与用量查询。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API **不涉及模型调用本身**，而是提供配套的资源治理能力，主要包括以下功能域：

- **组织管理**：创建/查询/更新组织信息，获取组织与账号详情（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)）；
- **成员管理**：添加、查询、修改角色、移除成员，并支持批量操作与席位绑定状态统计（参见 [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)）；
- **邀请管理**：生成、获取、撤销邀请链接，并可配置默认角色与席位分配策略（如 [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)）；
- **席位管理**：包括运行时分配/回收（`/seat-assignments`, `/seat-revocations`）、订阅级购买/变配（`CreateCreditSeat`, `UpgradeCreditSeat` 等 BssOpenApi 接口）及明细查询；
- **API Key 管理**：为成员账号创建和重置 UAC API Key，用于后续调用百炼模型服务；
- **订阅与用量**：获取席位总数、已分配数、周期内 Credits 剩余量等关键运营指标。

> **注意**：文档中多次出现 `SeatType` 参数（如 `standard`/`pro`/`max`），但 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 的返回字段 `SpecType` 与 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md) 中的 `SeatType` 含义一致，而 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 接口的 `SpecType` 参数实际用于指定新成员初始席位规格——三者语义统一，均为席位档位标识，无矛盾。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 示例值 |
|------|------|------|------|--------|
| `x-acs-action` | string | 是 | OpenAPI 动作标识，每个接口唯一 | `GetTokenPlanAccountDetail` |
| `x-acs-version` | string | 是 | API 版本号 | `2026-02-10` |
| `x-acs-date` | string | 是 | ISO8601 格式时间戳（UTC） | `2026-01-01T12:00:00Z` |
| `x-acs-signature-nonce` | string | 是 | 防重放随机字符串 | `abc123def456` |
| `Authorization` | string | 是 | ACS3-HMAC-SHA256 签名头 | `ACS3-HMAC-SHA256 Credential=xxx,...` |
| `SeatType` / `SpecType` | string | 视接口而定 | 席位规格类型 | `standard`, `pro`, `max` |
| `AccountIds` | array | 视接口而定 | 批量操作目标账号 ID 列表（Flat 格式） | `AccountIds.1=acc_123&AccountIds.2=acc_456` |
| `ClientToken` | string | 是（BssOpenApi） | 幂等性令牌，用于购买/变配类接口 | `token-20260101-001` |

## 使用方式

1. **认证准备**：  
   获取阿里云主账号或具备 `AliyunModelStudioFullAccess` 或最小化自定义权限的 RAM 用户的 `AccessKeyId` 和 `AccessKeySecret`，推荐通过环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 配置。

2. **调用流程**：  
   - 组织级操作（如 `GET /tokenplan/organization`）需先确认组织上下文；  
   - 成员操作（如 `POST /tokenplan/organization/member-additions`）依赖组织已存在；  
   - 席位分配（`POST /tokenplan/subscription/seat-assignments`）要求目标成员已加入组织且未被冻结；  
   - **席位购买与变配类接口（如 `CreateCreditSeat`, `UpgradeCreditSeat`）调用 `business.aliyuncs.com`，使用 BssOpenApi RPC 签名（HMAC-SHA1），与 ModelStudio OpenAPI 签名算法不同，不可混用**。

3. **SDK 推荐**：  
   强烈建议使用阿里云官方 SDK（如 Python `aliyun-python-sdk-alimt` + `aliyun-python-sdk-bssopenapi`），自动处理签名、重试与错误解析，避免手动构造 CanonicalRequest。

## 限制和注意事项

- **地域限制**：所有 ModelStudio 域名接口（`modelstudio.cn-beijing.aliyuncs.com`）仅支持华北2（北京）地域；BssOpenApi 接口（`business.aliyuncs.com`）为中国站全局可用。
- **席位回收约束**：`RemoveOrganizationMember` 接口会拒绝移除已分配席位的成员；必须先调用 `BatchRevokeSeats` 回收席位，再执行移除。
- **API Key 安全**：`CreateTokenPlanKey` 返回的 `PlainApiKey` **仅在创建响应中出现一次**，后续无法再次获取，丢失需调用 `RotateTokenPlanKey` 重置。
- **幂等性要求**：BssOpenApi 购买/变配类接口（`CreateCreditSeat`, `RenewCreditSeat` 等）**必须传入 `ClientToken`**，否则请求可能重复提交导致超额订购。
- **分页规范**：列表类接口（如 `ListOrganizationMembers`, `GetSubscriptionSeatDetails`）默认 `PageSize=20` 或 `10`，最大 `100`，需显式传参控制。
- **签名兼容性**：`x-acs-content-sha256` 头值在 GET 请求中应为 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`（空字符串 SHA256），不可省略。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [升级席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [退订席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
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
- [续费席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)


