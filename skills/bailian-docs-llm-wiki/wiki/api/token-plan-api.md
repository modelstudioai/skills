# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅全生命周期管理接口集合，基于阿里云 OpenAPI 和 BssOpenApi 体系构建。所有管理类操作（如组织、成员、席位分配）均通过 `modelstudio.cn-beijing.aliyuncs.com` 域名调用，而席位购买、变配、退订等计费类操作则统一接入 `business.aliyuncs.com` 的 BssOpenApi。开发者需使用阿里云 AccessKey 进行 ACS3-HMAC-SHA256（OpenAPI）或 HMAC-SHA1（BssOpenApi）签名认证，**不支持 `Authorization: Bearer {API_KEY}` 方式**。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于企业级 [Token](../concepts/token.md) 配额治理与协作管控，主要包括以下四类：

- **组织与账号管理**：获取当前账号详情（含组织隶属关系）、查询/修改组织基本信息。例如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回 `OrgMemberships` 树形结构，清晰呈现账号所属组织及工作空间层级。
- **成员与席位管理**：覆盖成员全生命周期操作——添加、查询、角色变更、移除；以及席位分配策略（批量分配/回收）、统计（已分配/未分配成员数）。[获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md) 接口可实时获取 `SeatedMemberCount` 与 `UnseatedMemberCount`，是席位规划的关键依据。
- **邀请与配置管理**：支持创建、获取、撤销邀请链接，并可设置默认角色与席位分配策略（如 `HIGH_TO_LOW`）。[设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md) 允许管理员预设新成员加入时的初始权限和资源分配逻辑。
- **订阅与用量管理**：提供席位购买（新购/新增/升级/续费/退订）、额度统计（按 `specType` 分组的 `SeatRemainingCredits`）及共享包明细查询能力，全部通过 BssOpenApi 实现。

## 关键参数

- **认证参数**：所有 OpenAPI 接口必须携带 `x-acs-action`（如 `GetOrganizationMemberSeatStats`）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头；BssOpenApi 接口则需 `Action`、`Version=2023-09-30`、`SignatureMethod=HMAC-SHA1` 等 RPC 公共参数。
- **席位规格（SpecType）**：在成员添加（`add-organization-member.md`）、席位分配（`batch-assign-seats.md`）、统计（`get-subscription-stats.md`）等多处作为关键枚举值出现，取值为 `standard` / `pro` / `max`，需严格匹配。
- **幂等性令牌（ClientToken）**：所有 BssOpenApi 购买/变配类接口（如 `create-credit-seat.md`、`upgrade-credit-seat.md`）均强制要求，用于防止重复下单导致资损。
- **ID 类参数**：`OrgId`（组织）、`AccountId`（成员）、`ApiKeyId`（密钥）、`InstanceId`（席位实例）为各接口间串联数据的核心标识，其中 `InstanceId` 需从 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 的 `InstanceCode` 字段提取。

> **注意**：文档 15（`create-credit-seat.md`）与文档 31（`add-credit-seats.md`）对 `Configs` 参数的描述存在不一致：前者要求 `Configs.N.Code` 和 `Configs.N.Value` 成对填写（如 `plan_type=standard`），后者示例中 `Configs` 仅作为占位符未体现具体键值。实际调用应以商品控制台或 `DescribePricingModule` 返回的属性定义为准，避免因属性名错误导致下单失败。

## 使用方式

1. **环境准备**：配置环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免硬编码密钥。
2. **选择 SDK 或工具**：优先使用阿里云官方 SDK（如 Python 的 `aliyun-python-sdk-modelstudio` 和 `aliyun-python-sdk-bssopenapi`），自动处理签名与公共参数；调试阶段可借助 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetTokenPlanAccountDetail) 或 `curl` 示例。
3. **典型流程**：
   - 调用 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 获取 `OrgId`；
   - 调用 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 确认目标成员 `AccountId`；
   - 调用 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 将席位绑定至成员；
   - 如需扩容，调用 BssOpenApi 的 [新增席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md) 创建新实例，再通过 `batch-assign-seats` 分配。
4. **错误处理**：关注 HTTP 状态码（如 403 权限不足）、`Code` 字段（如 `InvalidParameter`）、以及 BssOpenApi 中嵌套的 `Data.Success`（退订接口需双重校验）。

## 限制和注意事项

- **地域与 Endpoint 绑定**：所有 OpenAPI 接口仅支持华北2（北京）地域，Endpoint 固定为 `https://modelstudio.cn-beijing.aliyuncs.com`；BssOpenApi 接口为中国站，Endpoint 为 `https://business.aliyuncs.com`。
- **席位操作约束**：移除成员前必须确保其无已分配席位（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)），否则返回拒绝；退订席位（`reduce-credit-seats.md`）仅允许针对“未使用 Credits”的席位。
- **邀请链接唯一性**：一个组织在同一时间仅能存在一个有效邀请链接，重复调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 将返回现有链接，需先调用 [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)。
- **API Key 安全**：`PlainApiKey` 仅在创建（`create-token-plan-key.md`）和重置（`rotate-token-plan-key.md`）时返回一次，务必安全存储；后续调用应使用脱敏后的 `MaskedApiKey` 进行日志审计。

## 来源文档

- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [创建席位（新购）](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)
- [升级席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [续费席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [退订席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [新增席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


