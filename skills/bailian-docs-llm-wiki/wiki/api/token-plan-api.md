# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、邀请及订阅管理的后端服务接口集合，基于阿里云 OpenAPI 规范设计，所有接口均需使用 AccessKey 签名认证（`ACS3-HMAC-SHA256`），不支持 `Bearer Token` 认证方式。该 API 服务于 [Token](../concepts/token.md) Plan 团队版的全生命周期管理，覆盖组织治理、成员协作、席位分配与变配、用量统计等核心场景。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 并非模型推理类接口，而是**组织级管控型 API**，其核心能力分为五大功能域：

- **组织管理**：包括获取当前账号详情、查询/修改组织基本信息，详见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 和 [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)；
- **成员管理**：支持添加、查询、角色变更、移除成员，并提供成员与席位统计，如 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md) 和 [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)；
- **席位管理**：涵盖席位分配（批量）、回收、明细查询，以及订阅层级的统计与共享包管理，例如 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 和 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)；
- **邀请管理**：提供邀请链接创建、获取、撤销及配置管理能力，用于 SSO 成员自助加入，参见 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)；
- **API Key 与订阅管理**：支持为成员创建/重置 UAC API Key，以及查询订阅状态与用量，如 [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)。

> **注意**：席位购买、新增、升级、退订、续费等商业化操作属于 BssOpenApi（`business.aliyuncs.com`）范畴，使用 `HMAC-SHA1` 签名和 `2023-09-30` 版本，与主 TokenPlan OpenAPI（`modelstudio.cn-beijing.aliyuncs.com`，`ACS3-HMAC-SHA256`，`2026-02-10` 版本）在域名、签名算法、版本号上存在明确分离，开发者需严格区分调用上下文。

## 关键参数

- **认证参数**：所有 OpenAPI 接口必须携带以下公共请求头：
  - `x-acs-action`: 接口动作标识（如 `GetTokenPlanAccountDetail`）
  - `x-acs-version`: 固定为 `2026-02-10`
  - `x-acs-date`: ISO8601 格式时间戳（UTC）
  - `x-acs-content-sha256`: 请求体 SHA256 值（空请求体为 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`）
  - `x-acs-signature-nonce`: 唯一随机字符串
  - `Authorization`: `ACS3-HMAC-SHA256` 签名串  
  （BssOpenApi 接口则使用 `HMAC-SHA1` + `SignatureMethod` 等 RPC 风格参数）

- **席位规格参数**：`SpecType` 或 `SeatType` 字段统一取值为 `standard` / `pro` / `max`，各接口中含义一致，但需注意 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 返回字段为 `SpecType`，而 [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 中为 `SeatType`，属同一语义。

- **分页参数**：通用为 `PageNo`（从 1 开始）与 `PageSize`（默认 10–20，最大 100），但命名不完全统一（如 `PageNum` 出现在 [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md) 中），建议以各接口文档定义为准。

- **幂等性参数**：BssOpenApi 类接口（如席位购买）强制要求 `ClientToken`，而 OpenAPI 类接口无此要求。

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量，避免硬编码密钥；
2. **SDK 推荐**：优先使用阿里云官方 SDK（如 Python 的 `alibabacloud_tea_openapi` 或 Java 的 `aliyun-java-sdk-core`），自动处理签名、重试与错误解析；
3. **调试工具**：通过 [OpenAPI Explorer](https://api.aliyun.com) 快速生成调用示例并验证参数；
4. **典型流程**：
   - 调用 `GET /tokenplan/account` 获取当前账号及所属组织 ID；
   - 调用 `GET /tokenplan/organization` 确认组织状态；
   - 使用 `POST /tokenplan/invite/link/create` 生成邀请链接供成员加入；
   - 调用 `GET /tokenplan/organization/members` 查看新成员，再通过 `POST /tokenplan/subscription/seat-assignments` 分配席位；
   - 定期调用 `GET /tokenplan/subscription/stats` 监控 Credits 消耗。

## 限制和注意事项

- **认证方式唯一性**：所有 Token Plan OpenAPI 接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`，此限制在全部文档中一致强调，开发者不可尝试 bearer 方式；
- **地域固定**：当前所有 OpenAPI 接口 Endpoint 均限定于华北2（北京）地域，即 `https://modelstudio.cn-beijing.aliyuncs.com`，暂不支持多地域部署；
- **席位回收约束**：`POST /tokenplan/organization/member-removals` 在移除成员前会校验其是否持有席位，若已分配则拒绝操作；如需移除，须先调用 `POST /tokenplan/subscription/seat-revocations` 回收席位；
- **邀请链接唯一性**：一个组织在同一时刻仅允许存在一个有效邀请链接，重复调用 `CreateTokenPlanInviteLink` 将返回已有链接的 Token，而非新建——如需更新，必须先调用 `RevokeTokenPlanInviteLink` 失效旧链接；
- **BssOpenApi 权限隔离**：席位购买类接口（如 `CreateCreditSeat`）依赖 BssOpenApi 权限，需额外授予 `AliyunBSSFullAccess` 或最小化自定义策略，与 ModelStudio OpenAPI 权限（如 `AliyunModelStudioFullAccess`）相互独立。

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
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [升级席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [退订席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [续费席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)


