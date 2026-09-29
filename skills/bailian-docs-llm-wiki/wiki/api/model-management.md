# model management

模型管理是百炼平台提供的核心能力之一，用于统一查询、配置和管控租户可访问的模型资源及其运行时策略（如限流与权限）。开发者可通过 REST API 对模型元信息、配额、访问控制等进行细粒度操作。所有接口均需通过 `Authorization: Bearer <token>` 认证，并遵循平台统一的错误响应格式。

## 支持的模型与功能

当前支持管理所有已接入百炼平台的模型，包括系统预置模型（如 `qwen-max`、`qwen-plus`）及用户自部署的私有模型（需完成[模型注册](raw/model-api-reference/model-management/register-model.md)）。主要功能涵盖：  
- 查询模型列表（含状态、版本、支持的输入/输出格式）  
- 查询与更新模型级速率限制（QPS/TPM）  
- 查询与更新模型级访问权限（按用户/角色/应用 ID 授权）  
- **注意**：模型注册功能在 [模型管理](raw/model-api-reference/model-management.md) 中被列为入口，但实际注册流程依赖独立的 `POST /v1/models` 接口，该细节在 [模型注册](raw/model-api-reference/model-management/register-model.md) 文档中有明确定义，而主文档未展开说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识符，全局唯一，由平台分配或用户指定（私有模型） |
| `quota_type` | string | 否 | 限流类型，取值 `qps` 或 `tpm`；默认为 `qps` |
| `limit_value` | integer | 是 | 限流阈值，正整数；`tpm` 场景下单位为 token/min |
| `principal_type` | string | 是 | 授权主体类型，`user` / `role` / `app` |
| `principal_id` | string | 是 | 主体 ID，如用户 UID、角色名或应用 client_id |

> **注意**：`limit_value` 在 [更新模型限流](raw/model-api-reference/model-management/update-model-rate-limits.md) 中要求严格大于 0，但部分旧版 SDK 示例中允许传 `0` 表示禁用，该行为已被废弃，以[更新模型限流](raw/model-api-reference/model-management/update-model-rate-limits.md)为准。

## 使用方式

所有模型管理接口均为 `POST` 或 `GET` 请求，基础路径为 `https://dashscope.aliyuncs.com/api/v1/models`。典型调用链如下：  
1. 调用 [查询模型列表](raw/model-api-reference/model-management/list-models.md) 获取目标 `model_id`  
2. 根据需要调用 [查询模型限流](raw/model-api-reference/model-management/list-quotas.md) 或 [查询模型授权](raw/model-api-reference/model-management/list-model-permissions.md) 获取当前配置  
3. 使用 [更新模型限流](raw/model-api-reference/model-management/update-model-rate-limits.md) 或 [更新模型授权](raw/model-api-reference/model-management/update-model-permissions.md) 提交变更  

请求头必须包含 `Content-Type: application/json` 和有效认证凭证。

## 限制和注意事项

- 单租户最多可注册 50 个私有模型；系统模型数量不受限，但不可修改其元数据  
- 模型限流策略生效延迟 ≤ 30 秒，不支持毫秒级实时生效  
- 权限更新后，新策略对后续请求立即生效，但已建立的长连接（如 SSE 流式响应）可能沿用旧策略至连接关闭  
- 所有写操作（更新限流/权限）均需 `model:manage` 系统权限，普通 `model:use` 权限仅允许读取  
- 删除模型操作暂不开放，需联系技术支持；临时停用请将限流设为 `0`（见 [更新模型限流](raw/model-api-reference/model-management/update-model-rate-limits.md)）

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


