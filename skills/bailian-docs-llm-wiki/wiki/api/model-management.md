# model management

模型管理功能允许开发者通过 API 查询和配置百炼平台中已部署模型的访问权限、调用配额等运行时策略，适用于多租户场景下的细粒度管控。所有操作均基于模型 ID 进行，不涉及模型训练或部署生命周期管理。该能力面向企业级用户，需具备对应项目（project）的管理员或模型管理角色权限。

## 支持的模型与功能

当前支持对百炼平台中所有已上线的**推理模型**（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及第三方接入模型）进行以下管理操作：
- 查询模型列表：获取当前项目下可见的模型元信息（如名称、ID、状态）  
- 查询/更新模型限流：设置每秒请求数（QPS）和每分钟总调用量（TPM）阈值  
- 查询/更新模型授权：控制指定用户、用户组或服务身份（ServiceIdentity）对该模型的调用权限  

> **注意**：模型部署、下线、版本升级等生命周期操作不属于本模块范畴，详见 [模型部署](../../raw/model-api-reference/model-deployment.md) 文档；此处仅管理已部署模型的访问策略。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识符，可在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 响应中获取 |
| `qps_limit` | integer | 否 | 单用户 QPS 限制，默认为 `-1`（不限制）；设为 `0` 表示禁用该用户调用 |
| `tpm_limit` | integer | 否 | 单用户每分钟 [Token](../concepts/token.md) 总量限制，单位为千 token（ktoken），默认 `-1` |
| `principals` | array of string | 是（更新授权时） | 授权主体列表，格式为 `user:alice@company.com`、`group:dev-team` 或 `service:my-backend` |

## 使用方式

1. **查询模型列表**：调用 `GET /v1/models`，需在请求头携带 `X-DashScope-Project` 指定项目 ID  
2. **更新限流策略**：向 `PATCH /v1/models/{model_id}/rate-limits` 提交 JSON body（字段见上表）  
3. **更新授权关系**：向 `PUT /v1/models/{model_id}/permissions` 提交包含 `principals` 和 `action: "allow"` 或 `"deny"` 的 payload  

所有接口均遵循 RESTful 规范，返回标准 HTTP 状态码与错误结构。完整请求示例与响应体可参考 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 和 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 文档。

## 限制和注意事项

- 单模型最多支持 1000 个授权主体（principal），超出后 `PUT /permissions` 将返回 `400 Bad Request`  
- 限流策略变更通常在 10 秒内全网生效，但存在短暂窗口期可能未完全同步  
- `qps_limit` 和 `tpm_limit` 设置为 `0` 时，将**立即拒绝**该主体的所有新请求（含重试），此行为已在 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) 的“响应说明”中明确，旧版文档曾误述为“降级处理”，请以该文档为准  
- 非项目管理员调用更新类接口将返回 `403 Forbidden`，且不会触发审计日志记录（审计日志仅由管理员操作触发）

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


