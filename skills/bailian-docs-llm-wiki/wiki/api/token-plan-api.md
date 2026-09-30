# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的后端控制面接口集合，用于实现 TokenPlan 服务的自动化配置与治理。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 Bearer Token 方式。开发者需使用阿里云 AccessKey 进行调用，并通过 RAM 授权获取对应权限。

## 支持的模型/功能

Token Plan API **不涉及模型推理能力**，其核心功能聚焦于企业级资源治理，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织信息（如名称、描述）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，以及统计成员与席位关系；
- **席位精细化分配**：批量分配/回收标准（`standard`）、高级（`pro`）、尊享（`max`）三类席位；
- **邀请链路控制**：创建/获取/撤销邀请链接，配置默认角色与席位分配策略；
- **API Key 安全管理**：为成员创建或重置专属 API Key；
- **订阅与用量洞察**：查询席位总数、已分配数、剩余 Credits 及共享包明细。

> **注意**：文档中多次出现 `ORG_OWNER` 角色定义，但 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 的返回示例中 `RoleCode` 字段值为 `"ORG_MEMBER"`，而 [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md) 明确列出 `OwnerRoleUserCount` 字段。二者语义不一致，实际角色映射应以 [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md) 中的字段命名（`OwnerRoleUserCount`）为准。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 和 `Authorization` 头；推荐使用阿里云 SDK 自动签名。
- **席位规格（`SpecType` / `SeatType`）**：统一取值为 `standard`、`pro`、`max`，各接口（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)）保持一致。
- **分页参数**：`PageNo`（从 1 开始）和 `PageSize`（默认 10–20，最大 100），见 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 与 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)。
- **数组参数格式**：使用 Flat 格式（如 `AccountIds.1=xxx&AccountIds.2=yyy`），非 JSON 数组，详见 [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md) 和 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量；
2. **权限授予**：为 RAM 用户授予 `AliyunModelStudioFullAccess` 或最小化自定义策略（含 `modelstudio:ListOrganizationMembers`, `modelstudio:BatchAssignSeats` 等动作）；
3. **调用方式**：
   - 直接构造带签名的 HTTP 请求（参考各文档 `curl` 示例）；
   - 使用阿里云 SDK（Python/Java/Go 等）调用 `ModelStudio` 服务，指定 `RegionId=cn-beijing` 和 `Version=2026-02-10`；
   - 通过 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10) 调试并生成代码；
4. **Endpoint 统一**：所有接口均位于华北2（北京）地域，基础域名 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/`。

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`，违反将返回 `400 Bad Request`；
- **席位约束**：移除成员前必须确保其未持有席位，否则调用 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md) 将被拒绝；
- **邀请链接唯一性**：一个组织同一时间仅允许存在一个有效邀请链接，重复调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 将返回已有链接，需先调用 [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)；
- **API Key 敏感性**：`PlainApiKey` 仅在创建（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)）或重置（[重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）时返回一次，务必安全存储，后续无法再次获取；
- **URL 编码要求**：Query String 中含中文或特殊字符时，必须按 RFC 3986 百分号编码，否则签名验证失败（`SignatureDoesNotMatch`），详见 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 文档说明。

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
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)


