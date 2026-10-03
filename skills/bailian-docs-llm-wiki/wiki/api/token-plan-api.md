# token plan api

Token Plan API 是百炼平台用于管理组织级 Token 配额、订阅计划及用量监控的核心接口集合，支持按组织/成员/席位维度精细化控制模型调用资源。该 API 与百炼的计费体系深度集成，适用于需要自动化配额分配、用量审计或 SSO 集成的开发者场景。详细设计与权限模型请参考 [TokenPlan](../../raw/model-api-reference/token-plan-api.md)。

## 支持的模型/功能

Token Plan API **不直接调用大模型**，而是提供以下组织级资源管理能力：
- 组织层级的 Token 配额设置与重置（如月度总 quota）
- 成员级 Token 分配与回收（支持按角色自动绑定配额）
- 席位（Seat）生命周期管理（创建、停用、迁移配额）
- 邀请链接生成与状态查询（带配额预分配能力）
- API Key 的配额绑定与用量隔离
- 订阅计划变更、用量实时查询（精确到小时粒度）

> **注意**：部分文档中提及的“模型级 Token 绑定”（如 `model_id` 字段）已在 v2.3 版本移除，当前仅支持组织/成员/席位三级配额模型，详见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md) 中的版本说明章节。

## 关键参数

所有 Token Plan API 请求需携带 `X-DashScope-Organization` Header 指定目标组织 ID。核心参数包括：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plan_id` | string | 否 | 订阅计划唯一标识，从 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md) 接口获取 |
| `seat_id` | string | 否（创建席位时必填） | 席位 ID，格式为 `seat_abc123`，见 [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md) |
| `member_id` | string | 否（成员操作时必填） | 成员在组织内的唯一 ID，非百炼全局用户 ID |

## 使用方式

1. **认证**：使用组织管理员的 AccessKey（需 `token_plan:manage` 权限），通过 `Authorization: Bearer <AK>` 传递  
2. **基础路径**：`https://dashscope.aliyuncs.com/api/v1/token-plan`  
3. **典型流程**：  
   - 调用 `GET /subscription` 获取当前组织可用 plan 列表  
   - 调用 `POST /seat` 创建席位并指定初始配额（`initial_quota` 字段）  
   - 调用 `PATCH /member/{member_id}/quota` 动态调整成员 Token 余额  

示例（调整成员配额）：
```bash
curl -X PATCH \
  "https://dashscope.aliyuncs.com/api/v1/token-plan/member/u-m456/quota" \
  -H "Authorization: Bearer ak-xxx" \
  -H "X-DashScope-Organization: org-abc" \
  -d '{"quota": 10000}'
```

## 限制和注意事项

- 单次配额调整上限为 100 万 Token，超出需提交工单申请  
- 成员配额变更后 **5 秒内生效**，但用量统计延迟不超过 30 秒  
- 席位删除后，其未消耗 Token **不可回收至组织池**，仅可转移至其他席位（见 [席位管理](../../raw/model-api-reference/token-plan-api/token-plan-api-seat.md)）  
- API Key 若已绑定席位，则无法再修改其配额来源，必须先解绑（参考 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)）  
- 所有写操作均记录审计日志，可通过 `/audit-log` 接口查询（需 `token_plan:read_audit` 权限）

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


