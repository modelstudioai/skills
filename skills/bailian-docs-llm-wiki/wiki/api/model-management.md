# model management

模型管理功能为开发者提供对百炼平台所支持模型的元信息查询、访问控制与配额配置能力，包括模型列表、限流策略和权限设置等核心操作。所有接口均通过 RESTful API 提供，需使用有效的 API Key 进行身份认证。该能力适用于多租户场景下的精细化模型治理需求。

## 支持的模型与功能

当前支持的模型类型涵盖大语言模型（如 Qwen 系列）、嵌入模型（如 text-embedding-v1）及多模态模型（如 qwen-vl），具体可用模型列表以 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口实时返回为准。功能覆盖：
- 模型元信息查询（名称、版本、输入/输出格式、计费单位）
- 模型级速率限制配置（每秒请求数 QPS、每分钟总 Token 数等）
- 模型级访问权限控制（按用户 ID 或角色授予/撤销调用权限）

> **注意**：[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 文档中描述的 `role_based` 字段在 v2.3+ 版本已废弃，实际响应中不再返回；请以 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 的最新请求体结构为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen-max`、`text-embedding-v1`，须与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `id` 字段严格一致 |
| `quota_type` | string | 否 | 限流类型，可选 `qps` 或 `tpm`（Tokens Per Minute），默认为 `qps` |
| `permission_level` | string | 是 | 权限等级，取值为 `read`（仅查询）或 `invoke`（可调用），详见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) |

## 使用方式

1. **查询模型列表**：`GET /v1/models`，用于获取当前账号下可访问的全部模型及其状态  
2. **配置限流**：`PATCH /v1/models/{model_id}/quotas`，支持按 `quota_type` 设置独立限流阈值  
3. **管理权限**：`POST /v1/models/{model_id}/permissions` 配置白名单，`DELETE /v1/models/{model_id}/permissions/{user_id}` 撤销单个用户权限  

所有接口均要求 `Authorization: Bearer <API_KEY>` 请求头，且 `model_id` 必须已在目标项目中启用。

## 限制和注意事项

- 单个模型最多支持 100 个独立用户权限配置；超出后需先删除冗余条目  
- 限流策略变更通常在 30 秒内生效，但高并发场景下可能存在短暂延迟  
- 免费试用账号默认无模型调用权限，必须显式调用 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 授予 `invoke` 权限后方可使用  
- 模型 ID 区分大小写，`Qwen-Max` 与 `qwen-max` 视为不同模型

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


