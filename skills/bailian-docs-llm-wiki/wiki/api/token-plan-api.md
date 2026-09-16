# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及 API Key 全生命周期管理接口集合，用于构建自动化组织治理与资源分配系统。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 Bearer Token 方式。开发者需使用阿里云 AccessKey 进行调用，并通过 RAM 授权控制权限粒度。

## 支持的模型/功能

Token Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源配额管理**，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）；
- **成员全生命周期管理**：添加、查询、修改角色、移除成员，并支持批量操作；
- **席位资源调度**：按 `standard`/`pro`/`max` 三类规格批量分配或回收席位，查询席位明细与统计；
- **邀请体系配置**：创建/获取/撤销邀请链接，设置默认角色与席位分配策略；
- **API Key 安全管控**：为成员创建、重置 UAC API Key，支持描述与审计追踪。

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回字段 `RoleCode: "ORG_OWNER"`），但 [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md) 明确限定 `NewRoleCode` 仅允许 `ORG_ADMIN` 或 `ORG_MEMBER`。这表明 `ORG_OWNER` 为不可变更的系统主账号角色，实际角色变更仅适用于普通管理员与成员。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`（接口动作标识）、`x-acs-version: 2026-02-10`（固定版本）、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头；推荐使用阿里云 SDK 自动签名。
- **席位规格（`SpecType` / `SeatType`）**：统一取值为 `standard`、`pro`、`max`，见 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 与 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)。
- **角色编码（`RoleCode`）**：组织层角色为 `ORG_OWNER`（只读）、`ORG_ADMIN`、`ORG_MEMBER`；工作空间层为 `WS_ADMIN`、`WS_MEMBER`。
- **分页参数**：`PageNo`（从 1 开始）、`PageSize`（默认 20，最大 100），见 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)。

## 使用方式

1. **环境准备**：将 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 配置为环境变量；
2. **选择地域 Endpoint**：当前仅支持华北2（北京）地域，Endpoint 均为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`；
3. **构造请求**：
   - GET 接口（如 `/tokenplan/account`）直接拼接 Query String；
   - POST 接口（如 `/tokenplan/organization/member-additions`）参数通过 Query String 传递（非 JSON Body）；
   - 数组参数（如 `AccountIds`）使用 Flat 格式：`AccountIds.1=acc_1&AccountIds.2=acc_2`；
4. **签名与调用**：使用阿里云 SDK（Python/Java/Go 等）或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10) 生成合法请求，避免手动计算签名出错。

## 限制和注意事项

- **认证强制要求**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`，此设计与百炼模型调用 API 分离，确保组织管理通道独立安全。
- **席位强约束**：移除成员前会校验其是否持有席位，若 `HasSeat=true` 则拒绝移除（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；分配席位时需确保组织订阅中存在对应规格的可用席位。
- **邀请链接唯一性**：一个组织同一时间仅允许存在一个有效邀请链接；重复调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 将返回已有链接，而非新建。
- **API Key 敏感性**：`PlainApiKey` 仅在创建（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)）或重置（[重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）时返回一次，务必安全存储，后续无法再次获取明文。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)


