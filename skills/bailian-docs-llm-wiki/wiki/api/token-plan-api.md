# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及邀请等全生命周期管理的 OpenAPI 接口集合，基于阿里云统一认证体系（AccessKey + ACS3-HMAC-SHA256 签名），不支持 Bearer [Token](../concepts/token.md) 认证。所有接口均部署于华北2（北京）地域，Endpoint 域名为 `https://modelstudio.cn-beijing.aliyuncs.com`，版本号固定为 `2026-02-10`。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源配额管理**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持批量操作；
- **席位资源调度**：批量分配/回收席位（standard/pro/max 三档规格），查询席位明细与统计；
- **邀请机制控制**：创建/获取/撤销邀请链接，配置默认角色与席位分配策略；
- **API Key 安全管控**：为成员创建、重置 UAC API Key；
- **订阅与用量洞察**：获取席位总数、已分配数、剩余 Credits 及共享包明细。

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回字段 `RoleCode: ORG_OWNER`），但 [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md) 明确限定 `NewRoleCode` 仅允许 `ORG_ADMIN` 或 `ORG_MEMBER`；且 [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md) 列出的 `DefaultRoleId` 枚举值也不含 `ORG_OWNER`。这表明 `ORG_OWNER` 为系统保留角色，不可通过 API 修改或分配，开发者应避免在角色变更逻辑中使用该值。

## 关键参数

- **认证参数**：必须通过阿里云 AccessKey（`ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET`）签名，Header 中强制包含 `x-acs-action`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 和 `Authorization`。不支持 `Authorization: Bearer {API_KEY}`。
- **通用查询参数**：分页类接口（如 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）统一使用 `PageNum`/`PageNo` 和 `PageSize`，默认值分别为 `1` 和 `20`（最大 `100`）。
- **席位规格参数**：`SeatType` / `SpecType` 统一取值为 `standard`、`pro`、`max`，用于席位分配、回收、统计等场景。
- **数组参数格式**：批量操作（如 `AccountIds`、`StatusList`）采用 Flat 格式，例如 `AccountIds.1=acc_1&AccountIds.2=acc_2`，而非 JSON 数组。

## 使用方式

1. **环境准备**：配置阿里云 AccessKey 环境变量，或使用阿里云 SDK（推荐）自动处理签名；
2. **选择接口**：根据功能目标定位对应 Endpoint（如成员管理 → `/tokenplan/organization/members`）；
3. **构造请求**：
   - GET 接口：参数拼接至 URL Query String；
   - POST 接口：参数全部置于 Query String（非 Body），注意对中文和特殊字符做 RFC 3986 百分号编码；
   - 所有请求需携带标准 OpenAPI Header；
4. **解析响应**：检查 `Success` 字段及 `HttpStatusCode`，业务数据位于 `Data` 字段（GET）或根对象（部分 POST）。

## 限制和注意事项

- **地域与版本锁定**：所有接口仅支持华北2（北京）地域，API 版本固定为 `2026-02-10`，不可覆盖；
- **席位强约束**：移除成员前会校验其是否持有席位（[移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)），若已分配则拒绝操作，需先调用 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)；
- **邀请链接唯一性**：每个组织同一时间仅允许存在一个有效邀请链接（[创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)），重复创建将返回现有链接，需先调用 [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)；
- **API Key 安全**：`PlainApiKey` 仅在创建（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)）和重置（[重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）时返回一次，务必安全存储，后续无法再次获取；
- **权限最小化**：调用方 RAM 用户需被授予精确的 `AliyunModelStudioFullAccess` 或自定义策略，避免过度授权。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)


