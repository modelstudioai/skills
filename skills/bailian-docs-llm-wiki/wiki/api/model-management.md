# model management

模型管理功能允许开发者通过 API 查询和配置百炼平台中已部署模型的访问权限、调用配额等运行时策略，适用于多租户场景下的细粒度管控。所有操作均基于模型 ID 进行，不涉及模型训练或部署生命周期管理。该能力面向企业级用户，需具备对应工作空间的管理员或模型管理员角色权限。

## 支持的模型与功能

当前支持对百炼平台中所有已上线的**推理模型（inference-only models）**进行管理，包括通义千问系列（如 `qwen-max`, `qwen-plus`）、语音/多模态模型（如 `paraformer-realtime-v1`）及客户私有微调模型（需已完成 [模型部署](raw/model-api-reference/deploy-model.md)）。核心功能包括：
- 查询模型列表：获取当前工作空间下可见模型元信息（含状态、创建时间等）  
- 查询/更新模型限流：按每秒请求数（RPS）或每分钟 [Token](../concepts/token.md) 数（TPM）设置速率限制  
- 查询/更新模型授权：控制指定用户组或身份主体（如 RAM Role）对该模型的调用权限  

> **注意**：文档 [模型管理](raw/model-api-reference/model-management.md) 中列出的 `list-model-permissions` 接口在 v2.3.0+ 版本中已废弃，实际应使用统一的 [权限中心 API](raw/iam/permission-center.md) 进行模型级授权管理；请以 [查询模型授权](raw/model-api-reference/model-management/list-model-permissions.md) 的最新响应字段说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识符，可通过 [查询模型列表](raw/model-api-reference/model-management/list-models.md) 获取 |
| `rate_limit.rps` | integer | 否 | 每秒最大请求数，设为 `0` 表示不限流；与 `tpm` 互斥 |
| `rate_limit.tpm` | integer | 否 | 每分钟最大 [Token](../concepts/token.md) 数；若同时设置 `rps` 和 `tpm`，系统以更严格的策略生效 |
| `permissions[].principal_type` | string | 是 | 取值为 `USER`, `GROUP`, `RAM_ROLE`，见 [查询模型授权](raw/model-api-reference/model-management/list-model-permissions.md) |

## 使用方式

所有接口均为 RESTful HTTP 请求，需携带 `Authorization: Bearer <access_token>` 头。典型流程如下：

1. 调用 [查询模型列表](raw/model-api-reference/model-management/list-models.md) 获取目标 `model_id`  
2. 根据需求构造请求体，例如更新限流：
   ```json
   PUT /v1/models/{model_id}/rate-limits
   { "rate_limit": { "rps": 5 } }
   ```
3. 对于授权变更，建议先调用 [查询模型授权](raw/model-api-reference/model-management/list-model-permissions.md) 获取当前策略快照，再提交增量更新

## 限制和注意事项

- 单次请求最多更新 10 个模型的限流策略；批量授权更新暂不支持  
- 限流策略变更后**5 秒内生效**，但可能因边缘缓存存在短暂延迟（详见 [查询模型限流](raw/model-api-reference/model-management/list-quotas.md) 文档）  
- 模型删除后，其关联的限流与授权策略将自动清除，不可恢复  
- 非管理员用户调用更新类接口将返回 `403 Forbidden`，错误码 `UnauthorizedOperation.ModelPermissionDenied`

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


