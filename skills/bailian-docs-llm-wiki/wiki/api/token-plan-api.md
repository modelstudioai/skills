# token plan api

[Token](../concepts/token.md)Plan API 是百炼平台用于组织级资源配额管理的核心接口集合，主要面向企业客户实现成员管理、席位分配、邀请配置及订阅明细查询等能力。该 API 不直接参与模型推理调用，而是服务于 [Token](../concepts/token.md) 配额的生命周期管控与组织治理。所有接口均需通过 `Bearer <API Key>` 认证，且仅对拥有 `TokenPlanAdmin` 或 `TokenPlanManager` 权限的角色开放。

## 支持的模型/功能

[Token](../concepts/token.md)Plan API **不涉及任何大模型（如 Qwen 系列）的推理能力**，其功能完全聚焦于组织级 Token 配额治理，包括：  
- 成员全生命周期管理（添加、移除、角色更新、列表查询）  
- 席位批量分配与回收（[原文标题](../../raw/model-api-reference/token-plan-api.md)）  
- TokenPlan 专属邀请链接的生成、获取与撤销  
- API Key 的生成与轮换（[原文标题](../../raw/model-api-reference/token-plan-api.md)）  
- 组织信息、成员统计、订阅明细等只读数据查询  

> **注意**：原始文档中将“创建成员”“分配席位”等操作归类为 TokenPlan 功能，但实际这些能力在百炼控制台中与 `Organization API` 存在功能重叠；建议优先使用 [原文标题](../../raw/model-api-reference/token-plan-api.md) 中明确标注为 `token-plan-*` 前缀的接口，避免混用通用组织接口导致权限或配额同步异常。

## 关键参数

所有 TokenPlan API 请求必须携带以下认证与上下文参数：  
- `Authorization: Bearer <token_plan_api_key>`：须使用通过 `/v1/token-plan/key` 接口生成的专用 API Key（非通用 AccessKey）  
- `x-token-plan-org-id`（Header）：目标组织 ID，不可省略；可通过 `/v1/token-plan/account-detail` 获取  
- `page_size` / `page_number`（Query）：分页参数，仅部分列表接口支持，`page_size` 默认为 20，最大值为 100  
- `invite_code`（Path/Query）：邀请链接相关接口必需，由 `/v1/token-plan/invite-link` 返回  

## 使用方式

1. **获取 API Key**：调用 `POST /v1/token-plan/key` 生成首个密钥（参考 [原文标题](../../raw/model-api-reference/token-plan-api.md)）  
2. **确认组织上下文**：调用 `GET /v1/token-plan/account-detail` 获取当前账号下所有 TokenPlan 组织及其 `org_id`  
3. **执行核心操作**：例如分配席位 → `POST /v1/token-plan/seats/assign`，传入 `member_ids` 和 `seat_count`；查询席位明细 → `GET /v1/token-plan/subscription/seats`  
4. **权限变更后需重新鉴权**：修改成员角色或组织配置后，新权限在下次请求时生效，无缓存延迟  

## 限制和注意事项

- 单次席位分配上限为 500 个，超出需分批调用  
- 邀请链接有效期默认 7 天，不可修改；撤销后无法恢复（[原文标题](../../raw/model-api-reference/token-plan-api.md)）  
- `/v1/token-plan/invite-link` 与 `/v1/token-plan/invite-config` 接口返回的 `invite_code` 格式不同：前者为短码（如 `abc123`），后者为完整 URL 参数，不可混用  
- 所有写操作（如 `assign`、`revoke`、`remove`）均为同步执行，成功响应即表示状态已持久化  
- 不支持跨组织迁移席位；席位仅绑定至创建时指定的 `org_id`

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


