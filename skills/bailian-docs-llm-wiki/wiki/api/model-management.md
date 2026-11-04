# model management

模型管理是百炼平台为开发者提供的核心能力，用于统一查看、配置和控制所使用模型的访问权限、调用配额等运行时策略。所有操作均通过 RESTful API 完成，无需部署或维护模型实例。该能力适用于已接入百炼平台的全部托管模型及用户自定义模型。

## 支持的模型与功能

- **支持的模型类型**：所有在 [模型管理](../../raw/model-api-reference/model-management.md) 文档中列出的已上线模型（含 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分第三方模型），不支持未完成接入审核的私有模型。
- **核心功能**：
  - 查询模型列表（含状态、版本、支持的输入/输出格式）  
  - 查询与更新单模型调用限流（QPS/TPM）  
  - 查询与更新模型级授权策略（如允许调用的 App ID 白名单）  

> **注意**：[查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) 和 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 接口当前仅对企业版租户开放；免费版用户调用将返回 `403 Forbidden`，此限制未在 [模型管理](../../raw/model-api-reference/model-management.md) 主文档中明确说明，需以子文档为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型唯一标识符（如 `qwen-max`），必须与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `id` 字段完全一致 |
| `app_id` | string | 否（授权类接口必填） | 应用 ID，用于白名单授权；若为空则表示全局策略 |
| `qps` / `tpm` | integer | 否（更新限流时至少填一项） | 每秒请求数 / 每分钟 Token 数，设为 `0` 表示禁用该维度限流 |

## 使用方式

1. **认证**：所有接口需携带 `Authorization: Bearer <access_token>`，Token 通过 [API Key 管理](../../raw/auth/api-key.md) 获取；
2. **查询模型列表**：`GET /v1/models` → 获取可用模型元信息；
3. **更新模型限流**：`POST /v1/models/{model}/rate-limits` → 提交 JSON body（见上表参数）；
4. **更新模型授权**：`POST /v1/models/{model}/permissions` → body 中 `allowed_app_ids` 为字符串数组，空数组表示禁止所有应用调用。

## 限制和注意事项

- 单次调用最多更新 10 个 `app_id` 的授权状态，超出需分批提交；
- 限流策略变更通常在 30 秒内生效，但高并发场景下可能延迟至 2 分钟；
- 模型删除或下线后，其关联的限流与授权配置自动失效，**不会**保留历史记录；
- 所有写操作（更新限流/授权）均需具备 `model:manage` 权限，该权限由主账号在 IAM 控制台分配；
- 若发现 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回的 `allowed_app_ids` 包含已删除的 App ID，请手动调用更新接口清理，否则可能引发鉴权异常。

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


