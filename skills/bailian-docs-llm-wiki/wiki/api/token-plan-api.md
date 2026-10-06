# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台用于管理组织级 [Token](../concepts/token.md) 配额、成员席位、API Key 及用量订阅的核心管理接口集合，适用于企业客户进行细粒度的资源分配与成本控制。该 API 不直接参与模型推理调用，而是聚焦于账户体系下的资源规划与治理。所有操作均需使用组织管理员权限的 API Key 进行身份认证。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API **不涉及任何大模型推理能力**，也不支持模型调用；其功能完全围绕组织资源治理展开，包括：组织与账号生命周期管理、成员增删与角色分配、席位（seat）配额绑定与释放、邀请链接生成与状态查询、API Key 创建/轮换/禁用，以及订阅计划变更与实时用量统计。详细功能划分可参考 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 的模块索引。

## 关键参数

- `org_id`（路径参数）：必需，目标组织唯一标识，由百炼控制台或 `/v1/orgs` 接口获取  
- `Authorization: Bearer <api_key>`（Header）：必需，仅接受组织管理员级别的 API Key，普通成员 Key 无权调用  
- `plan_type`（Body 或 Query）：取值为 `pay_as_you_go` / `monthly_commit` / `annual_commit`，影响配额生效逻辑，具体约束见 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)  
- `seat_id`（部分接口路径）：用于席位级操作，如续期或解绑，不可复用或跨组织迁移  

> **注意**：原始文档中 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md) 提到 `key_scope=org` 为默认值，但实测 v2.3+ 版本已强制要求显式声明 `key_scope`，否则返回 `400 Bad Request` —— 请以最新 SDK 示例为准。

## 使用方式

1. 获取组织管理员 API Key（需在控制台「组织设置 → API Key」中创建，勾选「Token Plan Management」权限）  
2. 构造请求：所有接口根路径为 `https://dashscope.aliyuncs.com/api/v1/token-plan`，方法与路径遵循 RESTful 规范（如 `POST /orgs/{org_id}/seats` 创建席位）  
3. 解析响应：成功响应统一返回 `200 OK` + JSON body，含 `request_id` 便于问题追踪；错误码详见 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md) 中的错误码表  

## 限制和注意事项

- 单组织最多支持 10,000 个活跃席位，超出需提交工单扩容  
- API Key 调用频次限制为 100 QPS（按 `org_id + api_key` 组合限流），突发流量将触发 `429 Too Many Requests`  
- 席位分配后 5 分钟内生效，但用量数据延迟不超过 2 分钟（非实时计费）  
- 删除成员不自动释放其关联席位，须显式调用 `/seats/{seat_id}/release` 接口；该行为与 [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md) 文档描述一致，但部分旧版 SDK 示例遗漏此步骤，易导致配额泄漏

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


