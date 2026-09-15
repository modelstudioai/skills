# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及邀请全生命周期管理的后端服务接口集合，基于阿里云 OpenAPI 规范实现。所有接口均需通过 AccessKey 签名认证（`ACS3-HMAC-SHA256`），不支持 `Bearer {API_KEY}` 方式。开发者可通过阿里云 SDK 或 OpenAPI Explorer 快速集成，无需手动构造签名。

## 支持的模型/功能

Token Plan API 不涉及模型调用本身，而是聚焦于**组织治理与资源配额管理**，核心能力包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）；
- **成员全链路管理**：添加/移除成员、批量修改角色、查询成员列表及统计（含席位分配状态）；
- **席位精细化运营**：批量分配/回收标准/高级/尊享三类席位，查询席位明细与订阅统计；
- **邀请体系控制**：创建/获取/撤销邀请链接，配置默认角色与席位分配策略；
- **API Key 安全管控**：为成员创建及重置专属 API Key；
- **订阅与用量洞察**：获取席位总数、已分配数、剩余 Credits 及共享包明细。

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如 [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md) 返回字段 `OwnerRoleUserCount`），但 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 接口明确限定 `OrgRoleCode` 仅允许 `ORG_ADMIN` 或 `ORG_MEMBER`，且未提供授予 `ORG_OWNER` 的途径——该角色应由系统自动赋予初始创建者，不可通过 API 分配。

## 关键参数

- **认证参数**：所有接口必须携带 `x-acs-action`（如 `GetTokenPlanAccountDetail`）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，采用 `ACS3-HMAC-SHA256` 签名算法。
- **席位规格（`SpecType` / `SeatType`）**：统一取值为 `standard`（标准）、`pro`（高级）、`max`（尊享），见 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 和 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)。
- **角色编码（`RoleCode`）**：组织层为 `ORG_OWNER`/`ORG_ADMIN`/`ORG_MEMBER`；工作空间层为 `WS_ADMIN`/`WS_MEMBER`（见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)）。
- **分页参数**：通用 `PageNo`（从 1 开始）与 `PageSize`（默认 10–20，最大 100），适用于成员列表、席位明细等接口。

## 使用方式

1. **前置准备**：确保 RAM 用户已授权 `AliyunModelStudioFullAccess` 或最小化自定义策略（含 `modelstudio:ListOrganizationMembers`, `modelstudio:BatchAssignSeats` 等动作）；
2. **认证配置**：将 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 设为环境变量，避免硬编码；
3. **发起请求**：
   - GET 接口（如 `/tokenplan/account`）直接附加 Query 参数；
   - POST 接口（如 `/tokenplan/organization/member-additions`）通过 URL Query String 传参，数组参数使用 Flat 格式（如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`）；
   - 注意 URL 编码：中文或特殊字符需按 RFC 3986 百分号编码，否则返回 `SignatureDoesNotMatch`；
4. **推荐工具**：优先使用 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetTokenPlanAccountDetail) 调试，或阿里云官方 SDK（Python/Java/Go 等）自动处理签名。

## 限制和注意事项

- **地域固定**：所有接口当前仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com`；
- **席位强约束**：移除成员前会校验其是否持有席位（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)），若已分配则拒绝操作，需先调用 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)；
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接；调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 时，若已有有效链接将直接返回，需先调用 [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)；
- **API Key 安全**：`PlainApiKey` 仅在创建（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)）或重置（[重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）时返回一次，务必安全存储，后续无法再次获取；
- **时间戳精度**：`ExpireTime`、`CycleStartTime` 等字段单位为毫秒（如 `1778379206000`），非秒级。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


