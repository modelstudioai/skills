# token plan api

Token Plan API 是百炼平台面向企业组织提供的席位与成员管理服务接口，用于自动化完成组织创建、成员增删改查、席位分配/回收、邀请配置、API Key 管理及订阅用量查询等核心运营操作。所有接口均基于阿里云 OpenAPI 规范，采用 AccessKey 签名认证（`ACS3-HMAC-SHA256`），不支持 `Bearer Token` 认证方式。开发者需通过 RAM 授权获取必要权限，并推荐使用阿里云 SDK 或 OpenAPI Explorer 发起调用。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其功能聚焦于**组织治理与资源编排**，主要包括以下五大类：

- **组织管理**：获取/修改组织信息、获取账号详情（[获取组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-organization.md)）  
- **成员管理**：添加/查询/修改/移除成员，统计成员与席位分布（[查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md)）  
- **席位管理**：批量分配/回收席位、查询席位明细（[批量分配席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-assign-seats.md)）  
- **席位购买与变配**：新购、新增、升级、退订、续费席位（调用 BssOpenApi，非 ModelStudio 域名）  
- **邀请与 API Key 管理**：创建/获取/撤销邀请链接、设置邀请策略、创建/重置 API Key  

> **注意**：席位购买类接口（如 [创建席位（新购）](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)）属于 `business.aliyuncs.com` 域名下的 BssOpenApi（`HMAC-SHA1` 签名），而其余所有管理类接口均属 `modelstudio.cn-beijing.aliyuncs.com` 下的 ModelStudio OpenAPI（`ACS3-HMAC-SHA256` 签名）。二者认证机制、Endpoint、版本号均不兼容，不可混用。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `x-acs-action` | Header | string | 必填，接口动作标识符，值为文档中指定的 Action 名（如 `GetOrganization`） | `GetOrganization` |
| `x-acs-version` | Header | string | 必填，OpenAPI 版本号 | `2026-02-10` |
| `x-acs-date` | Header | string | 必填，ISO8601 格式时间戳（UTC） | `2026-01-01T12:00:00Z` |
| `Authorization` | Header | string | 必填，ACS3 签名字符串 | `ACS3-HMAC-SHA256 Credential=xxx, ...` |
| `AccountIds` | Query | array | 批量操作时使用 Flat 格式（如 `AccountIds.1=acc_1&AccountIds.2=acc_2`） | — |
| `SeatType` / `SpecType` | Query | string | 席位规格，统一取值：`standard` / `pro` / `max` | `pro` |
| `ClientToken` | Query | string | BssOpenApi 类接口必填幂等令牌（64 ASCII 字符内） | `abc123xyz789` |

## 使用方式

1. **认证准备**：配置环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，并授予对应 RAM 权限（参考各文档“前提条件”章节）；  
2. **选择 Endpoint**：区分两类域名——  
   - 组织/成员/席位/邀请/Key 管理 → `https://modelstudio.cn-beijing.aliyuncs.com`  
   - 席位购买/变配 → `https://business.aliyuncs.com`；  
3. **构造请求**：按文档要求设置 HTTP Method、Header（含 `x-acs-action`, `x-acs-version` 等）、Query 参数；  
4. **签名计算**：使用 `ACS3-HMAC-SHA256`（ModelStudio）或 `HMAC-SHA1`（BssOpenApi）算法生成签名；  
5. **调用建议**：**强烈推荐使用阿里云 SDK**（如 Python 的 `alibabacloud_tea_openapi`），可自动处理签名、重试、错误解析，避免手动构造 CanonicalRequest 出错（参见 [添加成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/add-organization-member.md) 文档中关于 URL 编码的警告）。

## 限制和注意事项

- **认证方式唯一性**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`（见全部文档“认证方式”小节）；  
- **席位回收前置检查**：调用 `RemoveOrganizationMember` 移除成员前，系统会校验该成员是否持有席位；若已分配席位，则拒绝移除（[移除成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/remove-organization-member.md)）；  
- **邀请链接唯一性**：每个组织同一时刻仅允许存在一个有效邀请链接；重复调用 `CreateTokenPlanInviteLink` 将返回已有链接，而非新建（[创建成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)）；  
- **API Key 安全**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 或 `RotateTokenPlanKey` 成功响应中**一次性返回**，务必安全保存；后续无法再次获取明文，仅能查看脱敏值（`MaskedApiKey`）；  
- **分页参数默认值**：`PageNo` 默认为 `1`，`PageSize` 默认为 `20`（最大 `100`），`ListOrganizationMembers` 和 `GetSubscriptionSeatDetails` 等接口均遵循此约定。

## 来源文档

- [组织与账号](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization.md)
- [获取组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-organization.md)
- [成员管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member.md)
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
- [撤销成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [获取成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [创建成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [创建 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [API Key 管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key.md)
- [订阅与用量](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription.md)
- [重置 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [查询共享包明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [获取订阅席位与额度统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [设置邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [修改组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/update-organization.md)


