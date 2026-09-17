# token plan api

`token plan api` 是百炼平台面向企业组织提供的 [Token](../concepts/token.md) 配额与席位管理服务接口，用于统一管理账号、组织、成员、席位分配、API Key 及订阅用量等核心资源。该 API 基于阿里云 OpenAPI 规范设计，需通过 AccessKey 签名认证（ACS3-HMAC-SHA256），不支持 `Bearer {API_KEY}` 方式调用。所有接口当前仅在华北2（北京）地域提供，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`。

## 支持的模型/功能

`token plan api` 并非模型推理接口，而是**组织级资源治理 API**，覆盖以下五大功能域：

- **组织与账号管理**：创建/查询/更新组织信息，获取当前账号详情（含组织成员关系树）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)  
- **成员全生命周期管理**：添加、移除、批量修改角色、查询列表及统计（如已分配/未分配席位成员数）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)  
- **席位（Seat）管理**：按规格（`standard`/`pro`/`max`）批量分配/回收席位，查询席位明细与订阅统计 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)  
- **邀请与配置管理**：生成/撤销 SSO 邀请链接（SAML/DingTalk）、获取/设置默认角色与席位分配策略 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)  
- **API Key 与订阅用量**：创建/重置 UAC API Key；查询订阅周期、各规格席位数量、已分配席位数及剩余 Credits [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)

> **注意**：文档中多次出现 `ORG_OWNER` 角色描述不一致问题——`get-token-plan-account-detail.md` 返回字段 `RoleCode` 示例值为 `"ORG_MEMBER"`（实际应为 `"ORG_OWNER"`），而 `get-organization-member-seat-stats.md` 明确列出 `OwnerRoleUserCount` 字段。以 `get-organization-member-seat-stats.md` 的 `OwnerRoleUserCount` 定义为准，`ORG_OWNER` 是独立角色，不可与 `ORG_MEMBER` 混用。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作名）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 和 `Authorization` 头，签名算法为 `ACS3-HMAC-SHA256`。  
- **通用查询参数**：分页类（`PageNo`/`PageSize`）、状态过滤（`Status`/`StatusList.*`）、名称模糊匹配（`Name`）、席位类型（`SeatType`/`SpecType`，取值 `standard`/`pro`/`max`）。  
- **数组参数格式**：采用 Flat 格式，如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy` 或 `StatusList.1=NORMAL&StatusList.2=LIMIT`。  
- **席位策略参数**：`SeatAssignStrategy`（`HIGH_TO_LOW`/`LOW_TO_HIGH`/`NONE`）和 `DefaultRoleId`（`SYSTEM_ROLE_ORG_ADMIN`/`SYSTEM_ROLE_ORG_MEMBER`）仅在邀请配置接口中生效。

## 使用方式

1. **前置准备**：确保已获取阿里云主账号或具备 `AliyunModelStudioFullAccess` 权限的 RAM 用户 AccessKey，并推荐配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`。  
2. **调用方式**：  
   - 优先使用 [阿里云 SDK](https://help.aliyun.com/zh/sdk) 或 [OpenAPI Explorer](https://api.aliyun.com) 自动生成签名代码，避免手动计算错误；  
   - 若手动构造请求，务必对 Query String 中的键和值按 RFC 3986 百分号编码（如中文需转为 `%E4%B8%AD%E6%96%87`），否则返回 `SignatureDoesNotMatch`；  
   - 所有接口均需指定 `x-acs-action`（如 `GetOrganizationMemberSeatStats`）和 `x-acs-version: 2026-02-10`。  
3. **典型流程示例**：  
   - 获取组织 ID → 调用 `GET /tokenplan/organization`；  
   - 添加成员并分配标准席位 → `POST /tokenplan/organization/member-additions?AccountName=test&OrgRoleCode=ORG_MEMBER&SpecType=standard`；  
   - 查询已分配席位成员 → `GET /tokenplan/organization/members?HasSeat=true`；  
   - 查看当前订阅额度 → `GET /tokenplan/subscription/stats`。

## 限制和注意事项

- **地域限制**：全部接口仅支持华北2（北京）地域，Endpoint 固定为 `https://modelstudio.cn-beijing.aliyuncs.com`，不支持跨地域调用。  
- **席位强约束**：移除成员前会校验其是否持有席位（`remove-organization-member.md`），若存在则拒绝操作；分配席位时需确保组织订阅中存在对应规格的可用席位（参考 `get-subscription-stats.md` 的 `TotalSeats` 与 `AssignedSeats`）。  
- **API Key 安全**：`PlainApiKey` 仅在 `create-token-plan-key.md` 和 `rotate-token-plan-key.md` 的响应中**一次性返回**，后续无法再次获取，需妥善保存；`MaskedApiKey` 用于日志脱敏展示。  
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接（`create-token-plan-invite-link.md`），重复调用将返回已有链接，需先调用 `revoke-token-plan-invite-link.md` 失效旧链接。  
- **时间戳精度**：`x-acs-date` 必须为 ISO 8601 格式（如 `2026-01-01T12:00:00Z`），且与服务器时间偏差不得超过 15 分钟，否则返回 `InvalidDate` 错误。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


