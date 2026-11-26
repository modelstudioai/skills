# model management

模型管理功能允许开发者通过 API 查询、配置和控制百炼平台中可用模型的访问权限与调用配额。它面向企业级用户和平台管理员，支持细粒度的模型级治理，包括限流策略与授权范围调整。所有操作均需具备对应模型的 `model:admin` 或 `tenant:admin` 权限。

## 支持的模型与功能

当前支持对百炼平台全部公开模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）及客户私有部署模型进行管理。核心功能包括：  
- 查询模型列表（含状态、版本、支持的输入/输出格式）  
- 查询与更新单个模型的调用限流（QPS、TPM、并发数）  
- 查询与更新模型在指定项目（project）或用户组（user group）下的访问授权  

详细接口定义与响应字段请参见 [模型管理](../../raw/model-api-reference/model-management.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen-max`；私有模型需使用完整命名空间（如 `myorg/my-model:v1`） |
| `project_id` | string | 否 | 限定作用域的项目 ID；若为空，则操作作用于租户全局 |
| `rate_limit.qps` | integer | 否 | 每秒请求数上限，取值范围 1–10000；设为 `0` 表示禁用该维度限流 |
| `permissions.granted` | boolean | 是 | 授权开关；`true` 表示允许访问，`false` 表示显式拒绝（注意：未显式授权即默认拒绝） |

> **注意**：`rate_limit.tpm`（每分钟 token 数）在 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) 中返回单位为 `tokens/minute`，但 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 的请求体要求单位为 `tokens/second` —— 实际提交时需自行换算，否则将导致配置错误。

## 使用方式

1. **获取模型列表**：`GET /v1/models`  
2. **查询某模型限流**：`GET /v1/models/{model_id}/quotas?project_id=xxx`  
3. **更新限流**：`PATCH /v1/models/{model_id}/quotas`，请求体示例：
   ```json
   { "project_id": "proj-abc123", "rate_limit": { "qps": 50, "tpm": 60000 } }
   ```
4. **更新授权**：`PATCH /v1/models/{model_id}/permissions`，请求体示例：
   ```json
   { "project_id": "proj-abc123", "granted": true }
   ```

所有接口均需携带 `Authorization: Bearer <access_token>`，且 token 需具备目标模型或项目的管理权限。完整请求示例与错误码说明见 [模型管理](../../raw/model-api-reference/model-management.md)。

## 限制和注意事项

- 单租户下最多可为同一模型配置 100 个不同 `project_id` 的独立限流与授权策略；超出后 `update` 请求将返回 `400 Bad Request`  
- 私有模型的 `model_id` 必须与模型注册时一致，大小写敏感，不支持别名映射  
- 修改限流或权限后，策略通常在 30 秒内全网生效；但客户端 SDK 缓存可能延迟 1–2 分钟，建议避免高频轮询变更结果  
- 若同时调用 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 和 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)，应分两次独立请求，不可合并 —— 合并请求将被服务端拒绝

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


