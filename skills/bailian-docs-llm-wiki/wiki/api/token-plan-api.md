# token plan api

[Token](../concepts/token.md) Plan API 是百炼平台用于管理组织级 [Token](../concepts/token.md) 配额、订阅计划及用量监控的核心接口集合，支持按组织/成员/席位维度精细化控制模型调用资源。该 API 不直接参与模型推理，而是为配额分配、权限隔离和计费结算提供基础设施能力。开发者需结合 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 主文档理解整体架构。

## 支持的模型/功能

[Token](../concepts/token.md) Plan API **不绑定具体大模型**，其功能与底层模型无关，适用于所有接入百炼平台计费体系的模型（如 Qwen 系列、Baichuan、GLM 等）。核心能力包括：
- 组织级 Token 预算设置与分层下发（见 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)）
- 成员 Token 配额分配与实时用量查询（见 [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)）
- 席位（Seat）生命周期管理，实现“一人一配额”策略（见 [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)）

> **注意**：部分旧版文档中提及的“模型专属 Token Plan”已下线，当前所有配额均统一通过组织/席位/成员三级结构管理，以 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 中定义的模型为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `org_id` | string | 是 | 组织唯一标识，从控制台或 `/v1/orgs` 获取 |
| `seat_id` | string | 否（创建席位时必填） | 席位 ID，用于绑定成员与配额 |
| `quota_type` | enum | 是 | 取值：`total`（总配额）、`monthly`（月度配额） |
| `token_limit` | integer | 是 | 非负整数，单位为 token；设为 `0` 表示无限制（需管理员权限） |

## 使用方式

1. **认证**：使用组织管理员或具备 `token_plan:manage` 权限的 API Key（参见 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)）  
2. **基础流程**：  
   - 创建组织 → 分配席位 → 绑定成员 → 设置配额 → 查询用量（见 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)）  
3. **典型调用**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/token-plans/seats \
     -H "Authorization: Bearer $API_KEY" \
     -d '{"org_id":"org-xxx","seat_id":"seat-yyy","token_limit":1000000,"quota_type":"monthly"}'
   ```

## 限制和注意事项

- 单组织最多支持 10,000 个活跃席位；单席位最大 `token_limit` 为 `2147483647`（int32 上限）  
- 配额变更**立即生效**，但历史用量不重置；修改 `quota_type` 会导致当期配额清零（详见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md)）  
- 成员被移出组织后，其关联席位自动释放，但未消耗的 Token 不可转移或退款  
- 调用频率限制：单组织每秒最多 10 次写操作（读操作不限），超限返回 `429 Too Many Requests`

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


