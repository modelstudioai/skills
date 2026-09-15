# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位与订阅管理的 OpenAPI 接口集合，用于自动化配置 [Token](../concepts/token.md)Plan 服务资源。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer Token` 方式调用。开发者需使用阿里云 AccessKey（推荐通过环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 配置）并授予对应 RAM 权限。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API **不涉及大模型推理或生成能力**，其核心功能聚焦于企业级资源治理，包括：
- **组织与账号管理**：获取账号详情、查询/更新组织信息（见 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)）；
- **成员全生命周期管理**：添加、移除、角色变更、批量统计（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)）；
- **席位调度**：分配、回收、明细查询（如 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）；
- **邀请与配置**：创建/撤销邀请链接、设置默认角色与席位分配策略（见 [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)）；
- **API Key 管理**：创建与重置 UAC API Key（见 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)）；
- **订阅与用量监控**：获取席位与 Credits 统计、查询共享包明细（见 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)）。

> **注意**：文档中多次出现 `OrgRoleCode` 参数值示例为 `ORG_ADMIN` 或 `ORG_MEMBER`（如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)），但 [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md) 的返回字段 `DefaultRoleId` 明确列出 `SYSTEM_ROLE_ORG_ADMIN` 和 `SYSTEM_ROLE_ORG_MEMBER`。实际调用时应以 `SYSTEM_ROLE_*` 前缀为准，避免因角色编码不匹配导致权限配置失败。

## 关键参数

- **认证参数**：所有接口必须携带标准 OpenAPI 公共请求头：`x-acs-action`（接口动作）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization`（`ACS3-HMAC-SHA256` 签名）。不支持 `Authorization: Bearer {API_KEY}`。
- **地域与 Endpoint**：当前仅支持华北2（北京）地域，Endpoint 固定为 `https://modelstudio.cn-beijing.aliyuncs.com`。
- **关键业务参数**：
  - `SeatType`：席位类型，取值 `standard` / `pro` / `max`（见 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 和 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)）；
  - `AccountIds`：成员 ID 列表，数组参数统一采用 Flat 格式（如 `AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`）；
  - `Items`：批量操作对象（如回收席位），需传入 URL 编码后的 JSON 字符串（见 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)）；
  - `SpecType`：在 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 中作为席位规格参数，语义与 `SeatType` 完全一致，属冗余命名，建议统一使用 `SeatType`。

## 使用方式

1. **准备凭证**：确保已获取具备 `TokenPlanFullAccess` 或最小化自定义权限的阿里云 AccessKey，并配置为环境变量；
2. **选择调用方式**：
   - **推荐**：使用阿里云官方 SDK（Python/Java/Go 等），自动处理签名与重试；
   - **调试**：通过 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10) 可视化生成请求；
   - **手动**：按 RFC 3986 对 Query String 进行百分号编码（尤其含中文或特殊字符时），否则返回 `SignatureDoesNotMatch`；
3. **构造请求**：根据接口文档确定 HTTP 方法、Endpoint、必需请求头及 Query/String 参数（注意数组参数格式）；
4. **处理响应**：检查 `Success` 字段及 `HttpStatusCode`，解析 `Data` 中的业务数据；错误码参考通用 [错误信息](../../raw/model-api-reference/preparations/error-code.md) 文档。

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名认证**，明确不支持 `Authorization: Bearer {API_KEY}`（见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)、[获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md) 等多处强调）；
- **席位强约束**：移除成员前会校验其是否持有席位，若 `SeatedMemberCount > 0` 则拒绝移除（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；
- **邀请链接唯一性**：同一组织下用户只允许存在一个有效邀请链接；重复调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 将返回已有链接，需先调用 [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)；
- **API Key 安全**：`PlainApiKey` 仅在创建或重置时返回一次，务必安全存储；后续调用需使用该密钥，平台不提供密钥恢复能力；
- **分页参数**：`PageNo` 和 `PageSize` 默认值均为 `1` 和 `10`，`PageNo` 必须为正整数（见 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 和 [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)）；
- **时间戳精度**：`CycleStartTime` / `CycleEndTime` / `ExpireTime` 等字段单位为**毫秒**（非秒），需注意客户端时间格式转换。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)


