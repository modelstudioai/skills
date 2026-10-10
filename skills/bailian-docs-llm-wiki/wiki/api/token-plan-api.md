# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的统一账号、席位与资源配额管理接口集合，用于自动化完成组织创建、成员生命周期管理、席位分配回收、邀请配置及 API Key 管理等核心运营操作。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer Token` 方式调用。开发者需使用阿里云 AccessKey 进行身份鉴权，并推荐通过阿里云 SDK 或 OpenAPI Explorer 发起请求以简化签名流程。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源编排**，主要包括：
- **组织与账号管理**：获取/修改组织信息、查询当前账号详情（含组织成员关系树）  
- **成员全生命周期管理**：添加、移除、批量更新角色、查询列表、统计席位分配状态（见 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 和 [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)）  
- **席位精细化管控**：支持 `standard`/`pro`/`max` 三档规格的批量分配与回收、订阅明细与额度统计  
- **邀请体系配置**：创建/获取/撤销邀请链接，设置默认角色与席位分配策略（如 `HIGH_TO_LOW`）  
- **API Key 安全管理**：为成员创建及重置 UAC API Key，明文 Key 仅在创建或重置时返回一次  

> **注意**：文档中多处提及“工作空间（Workspace）”概念（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回字段 `Workspaces`），但当前 [Token](../concepts/token.md) Plan API 未提供独立的工作空间管理接口，相关能力需通过 Model Studio 其他服务实现。

## 关键参数

- **认证参数**：所有接口必须携带标准 OpenAPI 请求头：`x-acs-action`（接口动作名）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 签名串。  
- **席位规格（SpecType/SeatType）**：统一取值为 `standard`（标准）、`pro`（高级）、`max`（尊享），该字段在 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 等接口中高频出现。  
- **数组参数编码规则**：  
  - Flat 格式：`AccountIds.1=acc_xxx&AccountIds.2=acc_yyy`（用于 `ListOrganizationMembers`, `UpdateOrganizationMember` 等）  
  - JSON 字符串 URL 编码：`Items=%5B%7B%22AccountId%22%3A%22acc_xxx%22%7D%5D`（用于 `BatchRevokeSeats`）  
- **分页参数**：`PageNo`（页码，从 1 开始）与 `PageSize`（每页条数，默认 20，最大 100），适用于成员列表、席位明细、共享包等查询接口。

## 使用方式

1. **环境准备**：将阿里云 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免硬编码。  
2. **Endpoint**：所有接口当前仅支持华北2（北京）地域，固定 Endpoint 前缀为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/`。  
3. **签名调用**：  
   - 手动计算：严格遵循 `ACS3-HMAC-SHA256` 算法，注意 Query String 必须按 RFC 3986 百分号编码（如中文需编码）；  
   - 推荐方式：使用 [阿里云 Python SDK](https://help.aliyun.com/zh/sdk) 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10) 自动生成可运行代码。  
4. **典型流程示例**：  
   - 创建组织 → 添加成员（自动分配席位）→ 查询成员列表验证 → 批量回收闲置席位 → 为关键成员创建专属 API Key → 设置邀请链接供新成员自助加入。

## 限制和注意事项

- **认证方式强制约束**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`（见 [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md) 和 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 的“认证方式”章节）。  
- **席位强依赖检查**：移除成员前会校验其是否持有席位，若 `SeatAssigned=true` 则拒绝移除（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）。  
- **API Key 安全边界**：`PlainApiKey` 仅在 `CreateTokenPlanKey` 和 `RotateTokenPlanKey` 接口响应中返回一次，后续无法再次获取，需妥善保管；`MaskedApiKey`（如 `sk_***6`）用于日志脱敏展示。  
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接，重复调用 `CreateTokenPlanInviteLink` 将返回已有链接的 Token，需先调用 `RevokeTokenPlanInviteLink` 失效旧链接。  
- **错误处理**：通用错误码参考 [错误信息](raw/model-api-reference/preparations/error-code.md)，开发者应解析 `Code` 和 `Message` 字段进行容错。

## 来源文档

- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


