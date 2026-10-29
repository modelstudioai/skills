# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅全生命周期管理接口集合，用于自动化配置 [Token](../concepts/token.md) Plan 团队版资源。所有接口均基于阿里云 OpenAPI 体系（部分席位购买类接口调用 BssOpenApi），需使用 AccessKey 签名认证，不支持 `Bearer` 类型 API Key。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能覆盖四类管理域：

- **组织与账号管理**：包括获取当前账号详情、查询/修改组织信息等，例如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 和 [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)；
- **成员管理**：支持添加、查询、修改角色、移除成员及统计，如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 和 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)；
- **席位管理**：涵盖分配、回收、查询明细及用量统计，例如 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 和 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)；
- **邀请与 API Key 管理**：提供邀请链接创建/撤销、邀请策略配置，以及 API Key 的创建与重置能力。

> **注意**：文档中提及的 `ORG_OWNER` 角色在 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 的 `RoleCode` 字段定义为系统内置角色，但 [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md) 中仅允许 `SYSTEM_ROLE_ORG_ADMIN` / `SYSTEM_ROLE_ORG_MEMBER` 作为 `DefaultRoleId`，二者语义不一致，实际配置时请以 `ORG_ADMIN` 或 `ORG_MEMBER` 为准（参考 `RoleCode` 字段枚举值）。

## 关键参数

- **认证参数**：所有 OpenAPI 接口（除 BssOpenApi 外）强制要求 `x-acs-action`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法为 `ACS3-HMAC-SHA256`；BssOpenApi 接口（如席位购买）使用 `HMAC-SHA1` RPC 签名。
- **席位规格**：`SpecType` 或 `SeatType` 参数统一取值为 `standard` / `pro` / `max`，见 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 和 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)。
- **分页参数**：`PageNo`（从 1 开始）和 `PageSize`（默认 20，最大 100）广泛用于列表接口，如 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)。
- **幂等性**：BssOpenApi 类接口（如 `CreateCreditSeat`）必须传入 `ClientToken`，长度 ≤64 ASCII 字符，用于保障重复请求的幂等性。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量，避免硬编码；
2. **SDK 优先**：推荐使用阿里云官方 SDK（如 Python 的 `aliyun-python-sdk-modelstudio`）自动处理签名与公共参数，避免手动构造；
3. **Endpoint 区分**：
   - 组织、成员、席位分配、邀请、API Key 等管理接口：`https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`；
   - 席位购买、变配、续费等计费类操作：`https://business.aliyuncs.com/`（BssOpenApi）；
4. **典型流程示例**：
   - 创建组织 → 添加成员 → 分配席位 → 创建 API Key → 配置邀请链接；
   - 查询成员列表 → 批量分配席位 → 获取用量统计。

## 限制和注意事项

- **认证方式限制**：所有接口均**不支持** `Authorization: Bearer {API_KEY}`，仅接受 AccessKey 签名（[获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 明确强调此点）；
- **席位分配约束**：`移除成员` 接口会校验成员是否持有席位，若已分配则拒绝移除；`批量回收席位` 需先调用该接口释放席位，再执行移除；
- **邀请链接唯一性**：每个组织仅允许存在一个有效邀请链接，重复调用 `CreateTokenPlanInviteLink` 将返回已有链接，需先调用 `RevokeTokenPlanInviteLink` 失效旧链接；
- **BssOpenApi 权限隔离**：席位购买类接口（如 `CreateCreditSeat`）需额外授予 `bss:CreateCreditSeat` 等 BssOpenApi 权限，与 ModelStudio OpenAPI 权限分离；
- **地域固定**：当前所有 `modelstudio.cn-beijing.aliyuncs.com` 接口仅支持华北2（北京）地域，无跨地域 Endpoint。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [升级席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [退订席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [续费席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)


