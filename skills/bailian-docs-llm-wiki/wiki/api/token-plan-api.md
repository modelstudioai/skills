# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台面向企业组织提供的账号、成员、席位、订阅及邀请等核心资源的管理接口集合，用于实现 [Token](../concepts/token.md) 配额的集中化、自动化管控。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer {API_KEY}` 方式。开发者需使用阿里云 AccessKey 进行调用，并通过 RAM 授权控制权限粒度。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API 不涉及模型推理能力，其核心功能聚焦于**组织治理与资源配额管理**，包括：
- **组织生命周期管理**：创建、查询、更新组织基本信息（如名称、描述、状态）；
- **成员全周期管理**：添加/移除成员、批量修改角色、查询成员列表及统计（含席位分配状态）；
- **席位精细化运营**：批量分配/回收标准/高级/尊享三类席位，查询席位明细与订阅统计；
- **邀请与接入控制**：生成/撤销/获取邀请链接，配置默认角色与席位分配策略；
- **API Key 安全管理**：为成员创建或重置专属 UAC API Key；
- **订阅与用量洞察**：获取席位总数、已分配数、剩余 Credits 及共享包明细。

> **注意**：文档中多次出现“组织 Owner 的业务账号标识（ALIYUN 类型为 aliyunUid，SSO 类型为 userIdentifier）”的描述，但 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回字段实际为 `OwnerBizAccountId`（值如 `"1543686331379464"`），而未返回 `userIdentifier`；该不一致可能源于历史字段命名演进，建议以实际返回字段为准。

## 关键参数

- **认证参数**：必须携带 `x-acs-action`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法固定为 `ACS3-HMAC-SHA256`。
- **席位规格（SpecType/SeatType）**：统一取值为 `standard` / `pro` / `max`，在 [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)、[批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)、[查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md) 等多处接口中复用。
- **角色编码（RoleCode）**：组织角色严格限定为 `ORG_OWNER` / `ORG_ADMIN` / `ORG_MEMBER`；工作空间角色为 `WS_ADMIN` / `WS_MEMBER`，见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)。
- **分页参数**：`PageNo`（从 1 开始）与 `PageSize`（默认 10–20，最大 100）在成员列表、席位明细、共享包等接口中通用。

## 使用方式

1. **环境准备**：将 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 配置为环境变量，避免硬编码；
2. **SDK 优先**：强烈推荐使用阿里云官方 SDK（如 Python 的 `alibabacloud_tea_openapi`）发起调用，自动处理签名、重试与错误解析；
3. **调试验证**：可直接使用 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/) 构造请求并查看实时响应；
4. **URL 编码规范**：当 Query String 含中文或特殊字符时（如 `Name=新组织名称`），必须按 RFC 3986 进行百分号编码，否则返回 `SignatureDoesNotMatch` 错误（参见 [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md) 示例说明）。

## 限制和注意事项

- **认证方式强制约束**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`，此设计隔离了 Token Plan 管理面与模型调用面的凭证体系；
- **席位强校验逻辑**：移除成员前会检查其是否持有席位，若 `HasSeat=true` 则拒绝操作（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；
- **邀请链接唯一性**：一个组织在同一时刻仅允许存在一个有效邀请链接；重复调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 将返回现有链接，而非新建；
- **API Key 敏感性**：`PlainApiKey` 仅在创建（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)）或重置（[重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）时返回一次，务必安全存储，后续无法再次获取；
- **地域与 Endpoint 绑定**：当前所有文档示例均指向华北2（北京）地域 `cn-beijing`，Endpoint 为 `https://modelstudio.cn-beijing.aliyuncs.com`，暂未提及多地域支持。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)


