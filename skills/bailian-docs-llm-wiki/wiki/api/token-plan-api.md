# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位与订阅管理的后端服务接口集合，用于实现组织级 [Token](../concepts/token.md) 配额分配、成员生命周期管理及资源用量监控。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，**不支持 `Bearer {API_KEY}` 认证方式**。开发者需使用阿里云 AccessKey（而非 [Token](../concepts/token.md) Plan 的 API Key）调用，适用于自动化运维、SaaS 集成等场景。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于 **组织治理与资源编排**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持按状态/席位分配情况过滤 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)；
- **席位精细化运营**：批量分配/回收席位、查询席位明细与统计（含 Credits 剩余量）、支持 `standard`/`pro`/`max` 三档规格 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)；
- **邀请与配置管理**：创建/撤销/获取邀请链接，设置默认角色与席位分配策略（如 `HIGH_TO_LOW`）；
- **订阅与用量洞察**：获取订阅周期、各类型席位总数/已分配数、剩余额度等关键指标。

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如文档9返回参数），但文档1、文档3、文档4中定义的合法 `RoleCode` 仅包含 `ORG_OWNER`、`ORG_ADMIN`、`ORG_MEMBER`；而文档6、文档8、文档19、文档22中示例值为 `ORG_MEMBER` 或 `ORG_ADMIN`，未见 `ORG_OWNER` 实际使用案例。建议以 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 中 `Roles` 字段的实际返回值为准，避免硬编码不存在的角色码。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法固定为 `ACS3-HMAC-SHA256`；
- **地域与 Endpoint**：当前仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`；
- **席位规格（SpecType）**：统一使用字符串枚举：`standard`、`pro`、`max`，见于添加成员（文档6）、批量分配席位（文档11）、查询席位明细（文档14）等接口；
- **数组参数格式**：Query String 中数组需用 Flat 格式，如 `AccountIds.1=acc_1&AccountIds.2=acc_2`（文档8、文档10）或 JSON URL 编码字符串 `Items=%5B%7B%22AccountId%22%3A%22acc_1%22%7D%5D`（文档15）；
- **分页参数**：`PageNo`（从1开始）与 `PageSize`（默认20，最大100），见于查询成员列表（文档7）、查询席位明细（文档14）等。

## 使用方式

1. **前置准备**：确保 RAM 用户已授予 `AliyunModelStudioFullAccess` 或最小化自定义权限策略；
2. **认证方式**：使用阿里云 SDK（推荐）或手动构造 ACS3 签名请求，**禁止将 AccessKey 明文写入代码**，应通过环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID`/`ALIBABA_CLOUD_ACCESS_KEY_SECRET` 注入；
3. **典型流程**：
   - 调用 `GetTokenPlanAccountDetail` 获取当前账号 ID 和组织关系；
   - 调用 `ListOrganizationMembers` 检查成员状态与席位分配；
   - 调用 `BatchAssignSeats` 为新成员分配 `pro` 席位；
   - 调用 `GetSubscriptionStats` 监控 `SeatRemainingCredits` 防止额度耗尽；
4. **调试工具**：优先使用 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/) 在线调试，可自动生成签名与 SDK 代码。

## 限制和注意事项

- **认证隔离**：Token Plan API 与百炼模型调用 API 使用**完全独立的认证体系**——前者必须用阿里云 AccessKey 签名，后者使用 `Authorization: Bearer {API_KEY}`，二者不可混用；
- **席位强约束**：移除成员前会校验其是否持有席位（文档10），若 `SeatedMemberCount > 0` 则拒绝操作，需先调用 `BatchRevokeSeats` 回收；
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接（文档16），重复调用 `CreateTokenPlanInviteLink` 将返回已有链接，需先 `RevokeTokenPlanInviteLink` 再新建；
- **API Key 生命周期**：`CreateTokenPlanKey` 与 `RotateTokenPlanKey` 返回的 `PlainApiKey` **仅在响应中出现一次**，务必安全存储，丢失后无法再次获取（文档21、文档23）；
- **错误处理**：所有接口均遵循阿里云标准错误结构，`Code` 字段为错误码，`Message` 为可读提示，详细错误码请查阅 [错误信息](raw/model-api-reference/preparations/error-code.md)。

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
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)


