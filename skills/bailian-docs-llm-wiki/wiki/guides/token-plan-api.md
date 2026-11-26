# token plan api

[Token](../concepts/token.md) Plan API 是一套面向组织级 [Token](../concepts/token.md) 资源管理的 RESTful 接口集合，用于自动化管理账号、组织、成员、席位、邀请链接及 API Key 等核心资源。所有接口均基于阿里云 OpenAPI 规范，采用 ACS3-HMAC-SHA256 签名认证（除席位购买类接口调用 BssOpenApi 使用 HMAC-SHA1），不支持 `Bearer Token` 认证方式。开发者需通过阿里云 AccessKey 进行身份鉴权，并推荐使用阿里云 SDK 或 OpenAPI Explorer 降低签名复杂度。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源编排**，覆盖以下五大领域：

- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）；详见 [获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 和 [修改组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/update-organization.md)。
- **成员全生命周期管理**：支持批量添加、查询、修改角色、移除成员，以及统计成员与席位分布；其中 [查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md) 接口返回字段包含 `SeatId`、`SpecType` 和 `PackLimitInfo`，可用于实时判断席位分配状态与额度使用情况。
- **席位精细化运营**：分为「运行时席位分配」与「订阅层席位变配」两类：
  - *运行时分配*：通过 `BatchAssignSeats` / `BatchRevokeSeats` 实现成员层席位的即时绑定与回收；
  - *订阅层变配*：调用 BssOpenApi 的 `CreateCreditSeat`、`UpgradeCreditSeat` 等接口完成新购、升级、退订、续费等商业操作，需注意其 Endpoint 为 `business.aliyuncs.com` 且签名算法为 `HMAC-SHA1`。
- **邀请与权限配置**：创建/获取/撤销邀请链接，并设置默认角色与席位分配策略（如 `HIGH_TO_LOW`）；[获取邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md) 返回的 `SeatAssignStrategy` 字段直接影响新成员加入时的自动席位分配行为。
- **API Key 安全管控**：支持创建与重置 UAC API Key，`PlainApiKey` 仅在创建或重置时明文返回一次，后续均以 `MaskedApiKey` 形式展示，符合最小权限与密钥轮转安全要求。

> **注意**：文档中 `token-plan-api-seat-purchase` 系列接口（如 [创建席位（新购）](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)）明确声明其属于 BssOpenApi（`2023-09-30` 版本），Endpoint、签名算法、参数格式均与 ModelStudio 域下的其他 Token Plan API 不一致，开发者集成时需严格区分调用链路。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 示例值 |
|--------|------|----------|------|--------|
| `x-acs-action` | string | 是 | OpenAPI 动作标识，每个接口唯一 | `GetTokenPlanAccountDetail`, `BatchAssignSeats` |
| `x-acs-version` | string | 是 | API 版本号，当前统一为 `2026-02-10` | `2026-02-10` |
| `x-acs-date` | string | 是 | ISO8601 格式时间戳（UTC） | `2026-01-01T12:00:00Z` |
| `x-acs-signature-nonce` | string | 是 | 请求唯一随机字符串，防重放 | `e4a7b5c2-1d8f-4a0b-9e3c-1234567890ab` |
| `Authorization` | string | 是 | ACS3-HMAC-SHA256 签名结果 | `ACS3-HMAC-SHA256 Credential=xxx, SignedHeaders=..., Signature=xxx` |
| `SpecType` | string | 否（部分接口） | 席位规格类型，取值 `standard`/`pro`/`max` | `pro` |
| `AccountIds` | array | 否（部分接口） | 批量操作目标账号 ID 列表，使用 Flat 格式（如 `AccountIds.1=acc_xxx`） | `AccountIds.1=acc_123&AccountIds.2=acc_456` |
| `Items` | JSON string | 否（部分接口） | 复杂对象数组，需 URL 编码后作为 Query String 传递 | `%5B%7B%22AccountId%22%3A%22acc_123%22%7D%5D` |

## 使用方式

1. **认证准备**：  
   将阿里云 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免硬编码。

2. **构造请求**：  
   - 所有接口均为 HTTPS 请求，地域固定为 `华北2（北京）`，Endpoint 前缀为 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/`（BssOpenApi 接口除外）；  
   - 必须携带全部 `x-acs-*` 公共请求头，并按 [ACS3 签名规范](https://help.aliyun.com/document_detail/31961.html) 计算 `Authorization`；  
   - 查询类接口（GET）参数通过 Query String 传递；写入类接口（POST）参数也统一通过 Query String 传递（非 JSON Body），数组参数遵循 Flat 格式。

3. **SDK 推荐**：  
   直接使用阿里云官方 SDK（如 Python 的 `alibabacloud_tea_openapi`）可自动处理签名、重试、超时等细节，显著降低接入成本。

## 限制和注意事项

- **认证方式强制约束**：所有 Token Plan API **仅支持 AccessKey 签名认证**，明确不支持 `Authorization: Bearer {API_KEY}` 方式。任何尝试使用 API Key 的调用将被拒绝（参见 [获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 中的“认证方式”说明）。
- **席位回收前提**：调用 `RemoveOrganizationMember` 移除成员前，系统会校验该成员是否持有席位；若 `SeatId` 非空，则操作被拒绝。必须先调用 `BatchRevokeSeats` 回收席位，再执行移除。
- **幂等性保障**：BssOpenApi 类接口（如 `CreateCreditSeat`、`UpgradeCreditSeat`）要求传入 `ClientToken` 参数，服务端据此识别重复请求并保证结果幂等；ModelStudio 域接口暂未强制要求，但建议客户端自行实现请求去重。
- **参数编码规范**：当 Query String 中含中文或特殊字符时（如 `Name=新的组织名称`），必须按 RFC 3986 进行百分号编码，否则签名验证失败（`SignatureDoesNotMatch`）。使用 SDK 可规避此问题。
- **错误处理**：接口返回 `Success: false` 时，应优先检查 `Code` 和 `Message` 字段；对于 BssOpenApi 接口，外层 `Success` 表示请求受理成功，实际业务结果需解析 `Data.Success`（如 [退订席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md) 文档所示）。

## 来源文档

- [组织与账号](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member.md)
- [查询成员列表](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/list-organization-members.md)
- [添加成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/add-organization-member.md)
- [移除成员](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [查询订阅席位明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [席位购买与变配](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase.md)
- [创建席位（新购）](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
- [新增席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
- [升级席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
- [退订席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
- [续费席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
- [邀请管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite.md)
- [创建成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [批量回收席位](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [创建 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [重置 API Key](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [设置邀请配置](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [获取订阅席位与额度统计](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [API Key 管理](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-key.md)
- [订阅与用量](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription.md)
- [查询共享包明细](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [修改成员角色](../../raw/token-plan-user-guide/token-plan-api/token-plan-api-member/update-organization-member.md)


