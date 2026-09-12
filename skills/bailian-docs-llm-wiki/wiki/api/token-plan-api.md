# token plan api

[Token](../concepts/token.md)Plan API 是百炼平台用于组织级资源配额管理的核心接口集合，主要面向企业客户实现席位（seat）分配、成员邀请、API Key 管理及订阅状态查询等能力。该 API 不直接参与模型推理调用，而是服务于 [Token](../concepts/token.md) 计量计划的生命周期管理。所有接口均需通过 `Bearer <token>` 认证，并遵循统一的 RESTful 设计规范。

## 支持的模型/功能

[Token](../concepts/token.md)Plan API **不支持任何大模型调用**，其功能完全聚焦于组织治理与配额运营，包括：  
- 成员全生命周期管理（添加、移除、角色更新、列表查询）  
- 席位批量分配与回收（含共享包明细分页查询）  
- [Token](../concepts/token.md)Plan 专属邀请链接的生成、获取与撤销  
- API Key 的创建、轮转与管理  
- 组织信息维护（创建、更新、详情获取）  
- 订阅统计与席位使用情况查询（如 [成员数量和席位数量情况展示](../../raw/model-api-reference/token-plan-api.md)）  

> **注意**：原始文档中重复列出了两次“成员数量和席位数量情况展示”（对应不同路径），实际应以 [get-organization-member-seat-stats](../../raw/model-api-reference/token-plan-api.md) 为准；另一处 [get-subscription-stats](../../raw/model-api-reference/token-plan-api.md) 侧重订阅维度统计，二者语义不同，非冗余。

## 关键参数

所有请求必须携带以下通用 Header：  
- `Authorization: Bearer <your_api_token>`（[Token](../concepts/token.md) 来自 [生成API Key](../../raw/model-api-reference/token-plan-api.md) 或 [重置API Key](../../raw/model-api-reference/token-plan-api.md)）  
- `Content-Type: application/json`（POST/PUT 请求）  

关键路径参数与请求体字段示例：  
- `org_id`：组织唯一标识，可通过 [获取账号下的组织信息](../../raw/model-api-reference/token-plan-api.md) 获取  
- `invite_code`：邀请链接中的唯一编码，用于 [获得TokenPlan成员邀请链接](../../raw/model-api-reference/token-plan-api.md) 后续操作  
- `seat_count`：分配/回收席位数，须为正整数且不超过剩余可用席位  

## 使用方式

1. **认证准备**：调用 [生成API Key](../../raw/model-api-reference/token-plan-api.md) 获取初始密钥，或使用已有密钥；密钥泄露时立即调用 [重置API Key](../../raw/model-api-reference/token-plan-api.md)  
2. **组织初始化**：若无组织，先调用 [创建成员](../../raw/model-api-reference/token-plan-api.md)（自动创建默认组织）或 [获取账号下的组织信息](../../raw/model-api-reference/token-plan-api.md) 确认上下文  
3. **席位分配**：调用 [分配席位](../../raw/model-api-reference/token-plan-api.md) 并指定目标成员 ID 与席位数  
4. **成员加入**：通过 [创建TokenPlan成员邀请链接](../../raw/model-api-reference/token-plan-api.md) 生成链接，新成员点击后自动绑定席位  

所有接口均返回标准 HTTP 状态码（200/400/401/403/404/500）及 JSON 格式响应体，错误详情见 `message` 字段。

## 限制和注意事项

- 单次分配/回收席位数上限为 100，超出需分批调用  
- 邀请链接有效期默认 7 天，不可修改，过期后需重新生成  
- 同一成员在单个组织内仅能拥有一个活跃席位，重复分配将覆盖原席位  
- [撤销TokenPlan成员邀请链接](../../raw/model-api-reference/token-plan-api.md) 仅对未使用的链接生效，已注册成员不受影响  
- 所有写操作（如分配、移除、更新）均不可逆，建议操作前通过 [获取成员列表](../../raw/model-api-reference/token-plan-api.md) 和 [订阅明细-座席列表](../../raw/model-api-reference/token-plan-api.md) 校验当前状态

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)



