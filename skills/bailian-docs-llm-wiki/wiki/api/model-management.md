# model management

模型管理是百炼平台提供的核心能力之一，用于统一查询、配置和控制租户下可用模型的访问权限与调用配额。开发者可通过 REST API 对模型列表、限流策略及授权范围进行细粒度操作。所有接口均需使用 `Authorization: Bearer <token>` 认证，并遵循平台统一的错误响应格式。

## 支持的模型与功能

当前支持对平台内全部托管模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及第三方接入模型）执行以下管理操作：  
- 查询模型列表（含状态、版本、支持的输入/输出类型）  
- 查询与更新单个模型的调用限流（QPS、TPM、并发数）  
- 查询与更新模型级授权策略（如允许调用的用户组、应用 ID、IP 白名单）  

完整功能清单详见 [模型管理](../../raw/model-api-reference/model-management.md) 文档。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，例如 `qwen-max`；必须与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `id` 字段严格一致 |
| `quota_type` | string | 否 | 限流维度，可选 `qps` / `tpm` / `concurrency`；默认为 `qps` |
| `scope` | string | 是 | 授权作用域，支持 `tenant`（租户级）、`user_group`、`app_id`；注意 `ip_whitelist` 仅在 `update-model-permissions` 中生效 |

> **注意**：`scope=ip_whitelist` 的行为在 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 中未返回实际 IP 列表字段，该字段仅在 `update-model-permissions` 请求体中有效，属设计不一致，建议以更新接口文档为准。

## 使用方式

1. **获取模型列表**：`GET /v1/models` → 获取可用模型 ID 及基础元信息  
2. **查看某模型限流**：`GET /v1/models/{model_id}/quotas`  
3. **更新限流**：`PATCH /v1/models/{model_id}/quotas`，请求体示例：  
   ```json
   { "qps": 5, "tpm": 10000 }
   ```  
4. **更新授权**：`PATCH /v1/models/{model_id}/permissions`，支持按 `user_group_ids` 或 `app_ids` 批量授权  

所有接口均遵循 [模型管理](../../raw/model-api-reference/model-management.md) 定义的路径与认证规范。

## 限制和注意事项

- 单次 `update-model-permissions` 最多更新 100 个 `app_ids` 或 50 个 `user_group_ids`，超出需分批调用  
- 限流更新后通常在 30 秒内全网生效，但边缘节点可能存在最多 1 分钟延迟  
- 模型状态为 `disabled` 时，即使有授权也无法调用；状态变更需通过独立的模型生命周期接口（非本模块）完成  
- `list-quotas` 和 `list-model-permissions` 均不返回历史操作日志，审计需依赖平台操作中心  

请始终参考最新版 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) 和 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 文档确认字段兼容性。

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


