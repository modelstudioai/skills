# token plan api

`token plan api` 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的统一 API 接口集合，用于实现 [Token](../concepts/token.md)Plan 服务的自动化配置与治理。该 API 基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，**不支持 `Authorization: Bearer {API_KEY}` 方式**，所有调用均需通过 AccessKey 进行签名鉴权。接口覆盖组织生命周期管理、成员角色与席位分配、邀请链接控制、API Key 管理及用量统计等核心能力。

## 支持的模型/功能

`token plan api` 并非模型推理类 API，而是面向 **[Token](../concepts/token.md)Plan 企业级账号治理体系** 的管理型 API，主要功能模块包括：

- **组织管理**：获取/修改组织基本信息（如名称、描述、状态）  
- **成员管理**：添加、查询、修改、移除组织成员，并支持批量操作（见 [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)）  
- **席位管理**：分配、回收、查询席位明细，支持 `standard`/`pro`/`max` 三种规格（见 [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)）  
- **邀请管理**：创建、获取、撤销邀请链接，配置默认角色与席位分配策略（见 [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)）  
- **API Key 管理**：为成员创建或重置 UAC API Key，用于后续调用百炼模型服务  
- **订阅与用量**：获取席位总数、已分配数、剩余 Credits 及共享包明细  

> **注意**：文档中未提及任何模型推理能力（如 `chat/completions`），所有接口均聚焦于 [Token](../concepts/token.md)Plan 账号体系的资源编排与权限治理，与模型调用层完全解耦。

## 关键参数

- **认证参数（必需）**：`x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce`、`Authorization`（含 `Credential` 和 `Signature`）。必须使用阿里云 SDK 或 OpenAPI Explorer 生成，不可手算。
- **通用查询参数**：`PageNum`/`PageNo`（默认 1）、`PageSize`（默认 10–20，最大 100）、`Name`（模糊匹配）、`Status`（如 `ACTIVE`/`FROZEN`）、`HasSeat`（布尔值）。
- **席位相关参数**：`SeatType`（`standard`/`pro`/`max`）、`SpecType`（同义，见 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)）、`QueryAssigned`（`true`/`false`）。
- **数组参数格式**：统一采用 Flat 格式，如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`；JSON 类型参数（如 `Items`）需 URL 编码。

## 使用方式

1. **前置准备**：确保已获取具备 `TokenPlanFullAccess` 或最小必要 RAM 权限的阿里云 AccessKey，并推荐配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`。
2. **Endpoint**：当前仅支持华北2（北京）地域，固定域名 `https://modelstudio.cn-beijing.aliyuncs.com`，路径以 `/tokenplan/` 开头（如 `/tokenplan/organization`）。
3. **调用方式**：
   - 推荐使用 [阿里云 SDK](https://help.aliyun.com/zh/sdk)（Python/Java/Go 等）自动处理签名；
   - 或使用 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10) 在线调试；
   - 手动调用需严格遵循 [ACS3-HMAC-SHA256](https://help.aliyun.com/zh/aliyun-openapi/introduction-to-aliyun-openapi) 签名规范，注意 Query String 百分号编码（RFC 3986）。
4. **典型流程示例**：
   - 调用 `GetTokenPlanAccountDetail` 获取当前账号及所属组织列表；
   - 调用 `ListOrganizationMembers` 查询待操作成员；
   - 调用 `BatchAssignSeats` 为成员分配 `pro` 席位；
   - 调用 `GetSubscriptionStats` 验证席位与 Credits 分配结果。

## 限制和注意事项

- **认证强制约束**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Bearer Token` 认证方式（见 [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md) 和 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 文档说明）。
- **席位强校验**：移除成员前会检查其是否持有席位，若 `HasSeat=true` 则拒绝移除（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；分配席位时需确保组织订阅中存在对应规格的可用席位。
- **邀请链接唯一性**：一个组织同一时间仅允许存在一个有效邀请链接；重复调用 `CreateTokenPlanInviteLink` 将返回已有链接，而非新建（见 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)）。
- **API Key 敏感性**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 和 `RotateTokenPlanKey` 成功响应中**一次性返回**，服务端不存储明文，务必安全保存；后续调用需使用 `MaskedApiKey` 进行审计追踪。
- **地域与版本锁定**：API 版本固定为 `2026-02-10`，Endpoint 仅限华北2，暂不支持多地域部署。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


