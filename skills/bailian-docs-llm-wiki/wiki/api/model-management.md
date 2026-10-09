# model management

模型管理是百炼平台为开发者提供的核心能力，用于统一查看、配置和控制所使用模型的访问权限与调用配额。所有操作均通过 RESTful API 完成，需使用平台颁发的 API Key 进行身份认证。该功能适用于多租户场景下的细粒度模型治理，不涉及模型训练或部署生命周期管理。

## 支持的模型与功能

当前支持对百炼平台已接入的全部托管模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo` 等）进行运行时管控，包括：  
- 查询模型列表（含模型状态、版本、支持的输入/输出格式）  
- 查询与更新模型限流策略（按用户/应用维度设置 QPS 和总调用量）  
- 查询与更新模型授权（控制指定 API Key 是否可调用某模型）  

具体接口说明详见 [模型管理](../../raw/model-api-reference/model-management.md) 文档中列出的子页面，例如 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen-max`；必须与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `id` 字段完全一致 |
| `quota_type` | string | 否 | 限流类型，取值 `qps` 或 `total`；默认为 `qps`，详见 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) |
| `permission_level` | string | 是（更新授权时） | 取值 `allowed` / `denied`；注意该字段在部分旧版 SDK 中被误命名为 `access_level`，以 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 定义为准 |

> **注意**：`permission_level` 字段名在早期文档草稿中曾写作 `access_level`，但自 v2.3.0 起已统一为 `permission_level`，请以 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 的最新定义为准。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <API_KEY>`  
2. **调用示例（更新限流）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/qwen-max/rate-limits" \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{"quota_type": "qps", "value": 5}'
   ```
3. 所有接口均遵循 `/api/v1/models/{model_id}/[subpath]` 路径规范，完整路径结构参考 [模型管理](../../raw/model-api-reference/model-management.md)。

## 限制和注意事项

- 单个 API Key 最多可配置 100 个模型的独立限流策略；超出后需先删除旧策略  
- 模型授权变更通常在 30 秒内生效，但存在最多 1 分钟的最终一致性延迟  
- 不支持对未在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中返回的模型执行任何管理操作（如自定义微调模型暂不可管）  
- 限流值设为 `0` 表示禁用该维度的调用（如 `qps: 0` 即禁止实时调用），但不会影响已存在的授权关系  

> **注意**：模型限流策略对异步任务（如 `batch-inference`）不生效，相关控制需通过任务队列配额单独配置——该行为与部分旧版文档描述存在差异，请以 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) 的“适用范围”章节为准。

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


