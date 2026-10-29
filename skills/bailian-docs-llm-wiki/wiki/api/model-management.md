# model management

模型管理功能允许开发者通过 API 查询和配置百炼平台中已部署模型的访问权限、调用配额等运行时策略。该能力不涉及模型训练或部署，仅作用于已上线模型的治理层。所有操作均需具备对应模型的 `model.admin` 或 `tenant.admin` 权限。

## 支持的模型与功能

- **支持模型范围**：仅对已在百炼控制台「模型中心」完成部署并处于 `active` 状态的模型生效（包括系统预置模型如 `qwen-max`、`qwen-plus` 及用户自部署的 `custom-*` 模型）。
- **核心功能**：
  - 查询模型列表：获取当前租户下所有可管理模型的元信息 [模型管理](../../raw/model-api-reference/model-management.md)
  - 查询/更新模型限流：按模型粒度设置 QPS 和总调用量配额 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md)
  - 查询/更新模型授权：控制指定用户组或应用 ID 对特定模型的调用权限 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，格式如 `qwen-max` 或 `custom-abc123`；必须与 [模型管理](../../raw/model-api-reference/model-management.md) 中返回的 `id` 字段严格一致 |
| `quota_type` | string | 否 | 限流类型，取值 `qps` 或 `total`；默认为 `qps`，详见 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) |
| `principal_type` | string | 是（授权接口） | 授权主体类型，`user` / `group` / `app`；注意 `app` 类型需使用应用的 `client_id` 而非名称 |

> **注意**：`update-model-rate-limits` 接口的 `reset_time` 参数在 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 文档中定义为 UNIX timestamp（秒级），但实测要求毫秒级时间戳，否则返回 `400 Bad Request`。请以实际 API 响应为准。

## 使用方式

1. **认证**：使用 `Bearer <access_token>` 请求头，`access_token` 需含 `model:manage` scope；
2. **请求示例（更新限流）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/qwen-max/rate-limits" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"qps": 5, "total": 10000}'
   ```
3. 所有端点均遵循 RESTful 设计，路径为 `/api/v1/models/{model_id}/[quotas\|permissions]`，具体细节参见 [模型管理](../../raw/model-api-reference/model-management.md)。

## 限制和注意事项

- 单租户最多可为同一模型配置 100 条独立授权规则（`principal_type=app` 时按 `client_id` 去重计数）；
- 限流策略变更后 **最长 30 秒内生效**，无热更新保障；
- 自部署模型（`custom-*`）的授权策略仅影响百炼 API 调用，不影响其后端服务自身的鉴权逻辑；
- `list-models` 接口默认仅返回 `active` 状态模型；若需包含 `inactive` 模型，须显式传参 `status=all` —— 此行为与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 文档描述一致，但部分旧版 SDK 默认忽略该参数，建议显式声明。

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


