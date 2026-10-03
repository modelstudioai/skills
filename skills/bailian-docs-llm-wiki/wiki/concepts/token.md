# Token 管理

Token 管理是百炼平台对模型调用过程中输入/输出 token 消耗进行计量、配额控制、计费结算与资源调度的核心机制。它贯穿 API 调用、应用集成、组织治理和成本优化全链路，是实现细粒度用量隔离、确定性性能保障与精细化预算管控的技术基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型 API 调用（实时/异步/Batch）**：通过 `X-Plan-ID` Header 或请求体中的 `plan_id` 显式绑定 Token Plan，触发配额校验与计费；未指定时回退至账户级默认额度，不计入 Token Plan 计费体系。  
- **智能体与工作流应用调用**：Token 消耗由底层所选模型（如 `qwen-vl`）自动计量，若应用配置了 Token Plan，则调用自动继承该 Plan 的配额与限流策略；OpenAI 兼容模式下同样支持 `X-Plan-ID` 透传。  
- **组织级资源治理**：通过 Token Plan API 实现按组织、成员、席位三级分配与动态调整配额（如 `PATCH /member/{id}/quota`），支持 SSO 集成、自动化审计与席位生命周期管理。  
- **模型权限与限流配置**：在模型管理接口中，`usage_limit`（Token/周期）与 `request_limit`（请求/周期）共同构成模型级 token 使用边界，需协同设置以生效。  
- **成本与预算控制**：Token 是计费基本单位（输入/输出分开计价），免费额度、节省计划、吞吐预留（PTU）均以 token 消耗为计量依据；预算告警、用量监控（如 `/v1/plans/{plan_id}/usage`）均基于 token 统计。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 生效范围 |
|------|------|------|------|-----------|
| `plan_id` | Header (`X-Plan-ID`) 或 Body 字段 | string | Token Plan 唯一标识，必须与调用模型匹配 | 所有模型 API（同步/异步/Batch）、应用调用 |
| `max_tokens` | Body | integer | 单次请求最大生成 token 数，受 Plan 的 `per_request_limit` 约束 | 单次请求级配额控制 |
| `priority` | Body | integer (1–100) | 请求调度优先级，默认 50；影响队列排队顺序 | 团队版及个人版 v2.1+（SDK v3.4.0+ 推荐） |
| `usage_limit` / `usage_limit_period` | Model Limits API Body | integer / integer（秒） | 模型级 token 消耗上限（如 `1000000`/`3600` 表示每小时 100 万 token） | 账号级或业务空间级模型限流 |
| `initial_quota` | Token Plan API（席位创建） | integer | 席位创建时预分配的初始 token 配额 | 组织内席位维度资源分配 |

> ⚠️ 注意：  
> - `plan_id` 与模型 `model` 必须严格一致，跨模型 Plan 不互通；  
> - `usage_limit` 依赖 `request_limit` 存在，单独设置会报错；  
> - Plan 创建后 `plan_id` 不可修改，配额变更（如 `total_quota`）立即生效，但缓存同步延迟 ≤3 秒，紧急时可调用 `/v1/plans/{plan_id}/refresh` 强制刷新。

## 面向开发者，简洁实用

- ✅ **快速启用**：控制台「配额中心 → Token Plan」新建计划 → 复制 `plan_id` → 在请求 Header 加 `X-Plan-ID: pln-xxx` 即可生效。  
- ✅ **调试验证**：调用 `/v1/plans/{plan_id}/usage` 查看 `used_tokens`、`remaining_tokens`、`reset_time`，确认配额扣减是否符合预期。  
- ✅ **错误排查**：返回 `403 Forbidden` 且含 `"code":"QUOTA_EXCEEDED"` 表示 Plan 配额耗尽；含 `"code":"PLAN_MODEL_MISMATCH"` 表示 `model` 与 Plan 绑定模型不一致。  
- ✅ **生产建议**：  
  - 避免在生产环境启用「额度用完即停」，改用「高额消费预警 + 自动扩容」策略；  
  - 多环境（开发/测试/生产）建议为每个环境独立创建 Plan，避免用量混杂；  
  - SDK 用户请升级至 v3.4.0+，自动处理 Plan 透传与优先级调度，无需手动拼接 Header。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [application call](../api/application-call.md)
- [model management](../api/model-management.md)


