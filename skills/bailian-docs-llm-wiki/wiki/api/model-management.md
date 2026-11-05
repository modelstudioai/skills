# model management

模型管理是百炼平台提供的核心能力之一，用于统一查询、配置和控制平台所支持模型的访问权限与调用配额。开发者可通过 API 对模型进行细粒度的限流策略设置和授权范围调整，适用于多租户、多应用的生产环境。所有操作均需通过 `POST /v1/models/{model_id}/...` 或 `GET /v1/models/...` 等标准 REST 接口完成。

## 支持的模型与功能

当前支持管理的模型包括平台内置的全部大语言模型（如 qwen-max、qwen-plus、qwen-turbo）及用户已部署的自定义模型（需通过 [模型部署](../../raw/model-api-reference/model-deployment.md) 流程完成注册）。支持的核心功能有：  
- 查询模型列表（含状态、版本、支持的输入格式等元信息）  
- 查询与更新单模型的调用限流（QPS、TPM、并发数）  
- 查询与更新模型级访问授权（按 API Key、UID 或应用 ID 授予/撤销调用权限）  

> **注意**：文档中未明确说明是否支持对已下线模型执行授权更新；根据 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 的接口定义，仅允许对 `status=active` 的模型操作，实际调用时若传入 inactive 模型 ID 将返回 404。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen-max`；必须与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `id` 字段完全一致 |
| `quota_type` | string | 否 | 限流类型，可选 `qps`、`tpm`、`concurrency`；默认为 `qps`，详见 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) |
| `granted_to` | object | 是（更新授权时） | 授权目标对象，结构为 `{ "type": "api_key" \| "uid" \| "app_id", "value": "xxx" }` |

## 使用方式

1. **获取模型列表**：调用 `GET /v1/models` 获取可用模型及其基础属性；  
2. **查看某模型限流**：`GET /v1/models/{model_id}/quotas`；  
3. **更新限流**：`POST /v1/models/{model_id}/quotas`，请求体为 JSON 格式，例如 `{"qps": 5}`；  
4. **查询授权列表**：`GET /v1/models/{model_id}/permissions`；  
5. **添加授权**：`POST /v1/models/{model_id}/permissions`，请求体需包含 `granted_to` 字段。  

所有接口均需携带有效的 `Authorization: Bearer <access_token>` 头。完整示例与错误码说明见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

## 限制和注意事项

- 单模型 QPS 上限默认为 100，TPM 默认为 100000，超出需提交工单申请提升；  
- 授权更新操作为**覆盖写入**（非增量），每次调用将全量替换该模型的授权列表，请务必先调用查询接口获取当前授权集再做修改；  
- 模型限流策略变更通常在 30 秒内生效，但高并发场景下可能存在最多 2 分钟延迟；  
- 非管理员角色调用更新类接口时，需确保当前 API Key 已被授予对应模型的 `manage_permissions` 或 `manage_quotas` 权限 —— 具体权限映射规则参见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)。

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


