# token plan api

Token Plan API 是百炼平台面向企业组织提供的账号、成员、席位与订阅管理的统一管控接口集合，用于自动化配置 TokenPlan 服务权限与资源配额。所有接口均基于阿里云 OpenAPI 规范，采用 `ACS3-HMAC-SHA256` 签名认证，不支持 `Bearer Token` 方式。开发者需使用阿里云 AccessKey（推荐通过环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 配置）调用，建议优先使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com) 进行调试。

## 支持的模型/功能

Token Plan API **不涉及大模型推理或生成能力**，其核心功能聚焦于企业级账号生命周期与资源治理，包括：
- **组织与账号管理**：获取当前账号详情、查询/更新组织基本信息（如名称、描述）  
- **成员全生命周期管理**：添加、移除、批量修改角色、查询成员列表及统计（含席位分配状态）  
- **席位资源调度**：批量分配/回收标准/高级/尊享三类席位，查询席位明细与订阅统计  
- **邀请与接入控制**：创建/获取/撤销邀请链接，配置默认角色与席位分配策略  
- **API Key 管理**：创建与重置 UAC API Key，用于下游服务集成  
- **订阅与用量监控**：获取席位数量、Credits 剩余量、共享包明细等运营数据  

> **注意**：文档中多次出现 `ORG_OWNER` 角色（如 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md) 返回字段 `RoleCode: "ORG_OWNER"`），但 [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md) 和 [邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md) 明确限定可选值为 `ORG_ADMIN` / `ORG_MEMBER`，且未提供 `ORG_OWNER` 的变更入口。实际调用中 `ORG_OWNER` 仅由系统自动赋予主账号，不可通过 API 修改。

## 关键参数

- **认证参数**：所有接口必须携带 `x-acs-action`（操作标识）、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 及 `Authorization` 头，签名算法为 `ACS3-HMAC-SHA256`。  
- **席位类型（`SpecType` / `SeatType`）**：统一取值为 `standard`（标准）、`pro`（高级）、`max`（尊享），见 [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md) 和 [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)。  
- **分页参数**：`PageNo`（页码，默认 1）、`PageSize`（每页条数，默认 10–20，最大 100），广泛用于成员列表、席位明细等接口。  
- **数组参数格式**：采用 Flat 格式，如 `AccountIds.1=acc_123`、`AccountIds.2=acc_456`（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；JSON 数组需 URL 编码（见 [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)）。  

## 使用方式

1. **环境准备**：配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 环境变量。  
2. **选择接口**：根据场景选择对应模块（如成员管理 → [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)）。  
3. **构造请求**：  
   - 方法：`GET`（查询类）或 `POST`（变更类）  
   - Endpoint：统一为华北2（北京）地域 `https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/...`  
   - Headers：按规范填充 `x-acs-*` 签名头（推荐使用阿里云 SDK 自动计算）  
   - 参数：Query String 传递（无 Body），注意数组和特殊字符编码规则。  
4. **处理响应**：检查 `Success: true` 及 `HttpStatusCode: 200`，解析 `Data` 字段；失败时参考 `Code`/`Message` 并查阅 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。  

## 限制和注意事项

- **认证强制性**：所有接口**仅支持 AccessKey 签名**，明确不支持 `Authorization: Bearer {API_KEY}`（见 [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)）。  
- **席位强约束**：移除成员前会校验其是否持有席位，若 `HasSeat=true` 则拒绝操作（见 [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)）；分配席位需确保组织订阅容量充足。  
- **邀请链接唯一性**：同一组织下仅允许存在一个有效邀请链接，重复调用 [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md) 将返回现有链接，需先调用 [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)。  
- **API Key 安全**：`PlainApiKey` 仅在创建（[创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)）或重置（[重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)）时返回一次，务必安全存储，后续无法再次获取。

## 来源文档

- [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)
- [获取账号详情](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-token-plan-account-detail.md)
- [获取组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/get-organization.md)
- [修改组织信息](../../raw/model-api-reference/token-plan-api/token-plan-api-organization/update-organization.md)
- [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)
- [添加成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/add-organization-member.md)
- [查询成员列表](../../raw/model-api-reference/token-plan-api/token-plan-api-member/list-organization-members.md)
- [移除成员](../../raw/model-api-reference/token-plan-api/token-plan-api-member/remove-organization-member.md)
- [修改成员角色](../../raw/model-api-reference/token-plan-api/token-plan-api-member/update-organization-member.md)
- [获取成员与席位统计](../../raw/model-api-reference/token-plan-api/token-plan-api-member/get-organization-member-seat-stats.md)
- [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)
- [批量分配席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-assign-seats.md)
- [批量回收席位](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/batch-revoke-seats.md)
- [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)
- [查询订阅席位明细](../../raw/model-api-reference/token-plan-api/token-plan-api-seat/get-subscription-seat-details.md)
- [创建成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/create-token-plan-invite-link.md)
- [获取成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-invite-link.md)
- [获取邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/get-token-plan-org-invite-config.md)
- [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)
- [撤销成员邀请链接](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/revoke-token-plan-invite-link.md)
- [重置 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/rotate-token-plan-key.md)
- [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)
- [获取订阅席位与额度统计](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/get-subscription-stats.md)
- [查询共享包明细](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription/list-subscription-shared-packages.md)
- [创建 API Key](../../raw/model-api-reference/token-plan-api/token-plan-api-key/create-token-plan-key.md)
- [设置邀请配置](../../raw/model-api-reference/token-plan-api/token-plan-api-invite/set-token-plan-org-invite-config.md)


