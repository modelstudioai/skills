# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及邀请等全生命周期管理的后端服务接口集合，基于阿里云 OpenAPI 规范实现。所有接口均需通过 AccessKey 签名认证（`ACS3-HMAC-SHA256`），不支持 `Bearer {API_KEY}` 方式。开发者可通过阿里云 SDK 或 OpenAPI Explorer 快速集成，无需手动构造签名。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源配额管理**，包括：
- **组织与账号管理**：获取当前账号详情、查询/修改组织信息（如名称、描述）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)；
- **成员全链路管理**：添加、查询、修改角色、移除成员，并支持按状态/席位分配情况分页过滤 [原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)；
- **席位精细化运营**：批量分配/回收席位、查询席位明细及统计（含 `standard`/`pro`/`max` 三类规格）[原文标题](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)；
- **邀请与配置控制**：创建/获取/撤销邀请链接，设置默认角色与席位分配策略（`HIGH_TO_LOW`/`LOW_TO_HIGH`/`NONE`）；
- **API Key 安全管控**：为成员创建或重置独立的 UAC API Key，支持描述与权限隔离；
- **订阅与用量洞察**：获取席位与 Credits 额度统计、查询共享包明细。

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如文档 2 返回参数 `RoleCode: "ORG_OWNER"`），但文档 5（添加成员）明确限定 `OrgRoleCode` 只允许 `ORG_ADMIN` 或 `ORG_MEMBER`；且文档 8 统计字段名为 `OwnerRoleUserCount`，但描述为“主账号数（ORG_OWNER 角色）”，而文档 4 和文档 2 的 `RoleCode` 枚举值中均未定义 `ORG_OWNER`。该角色实际不可通过 API 分配，应以 `ORG_ADMIN` 作为最高管理权限角色。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法固定为 `ACS3-HMAC-SHA256`；
- **席位规格（`SpecType`/`SeatType`）**：统一取值为 `standard`（标准）、`pro`（高级）、`max`（尊享），各接口（如文档 5、13、14、24）保持一致；
- **数组参数格式**：Query String 中数组需使用 Flat 格式，例如 `AccountIds.1=acc_a&AccountIds.2=acc_b`（文档 9、10、13）或 `StatusList.1=NORMAL&StatusList.2=LIMIT`（文档 14、26）；
- **分页参数**：`PageNo`/`PageNum`（从 1 开始）与 `PageSize`（默认 10–20，最大 100），不同接口命名略有差异（文档 6 用 `PageNum`/`PageSize`，文档 14/26 用 `PageNo`/`PageSize`）。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量，避免硬编码；
2. **调用流程**：
   - 先调用 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 确认当前账号 ID 与组织关系；
   - 通过 [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md) 获取 `OrgId`；
   - 使用 `OrgId` 调用成员/席位/邀请等子资源接口；
3. **推荐工具**：优先使用阿里云官方 SDK（Python/Java/Go 等）或 [OpenAPI Explorer](https://api.aliyun.com) 自动生成代码，规避手动签名错误；
4. **Endpoint 统一性**：所有接口当前仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/{path}`。

## 限制和注意事项

- **认证方式强制约束**：所有接口**不支持** `Authorization: Bearer {API_KEY}`，仅接受 AccessKey 签名，违反将返回 `403 Forbidden`；
- **席位强校验**：移除成员前会检查是否持有席位（文档 10），若存在则拒绝操作；回收席位需显式调用 `/subscription/seat-revocations`（文档 11）；
- **邀请链接唯一性**：同一组织下仅允许一个有效邀请链接，重复调用 `CreateTokenPlanInviteLink` 将返回已有链接（文档 16），需先 `Revoke` 再新建；
- **API Key 敏感性**：`PlainApiKey` 仅在创建（文档 22）或重置（文档 23）时返回一次，务必安全存储，后续无法再次获取；
- **时间戳精度**：`CycleStartTime`/`CycleEndTime`/`ExpireTime` 等字段单位均为毫秒（Unix Timestamp），非秒级；
- **错误处理**：通用错误码参考 [错误信息](../../raw/model-api-reference/preparations/error-code.md)，需关注 `SignatureDoesNotMatch`（签名计算错误）、`InvalidParameter`（参数未 URL 编码）等高频错误。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


