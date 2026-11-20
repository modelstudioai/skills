# model management

模型管理是百炼平台为开发者提供的核心能力，用于统一查看、配置和控制所使用模型的访问权限、调用配额等运行时策略。所有操作均通过 RESTful API 完成，无需部署或维护模型实例。该能力适用于已接入百炼平台的全部托管模型及用户自定义模型。

## 支持的模型与功能

- **支持的模型类型**：所有在 [模型管理](../../raw/model-api-reference/model-management.md) 文档中列出的已上线模型（含 `qwen-*`、`baichuan-*`、`llama-*` 等系列），以及通过百炼控制台成功注册的私有模型。
- **核心功能**：
  - 查询模型列表（含版本、状态、支持的输入/输出格式）  
  - 查询与更新单模型的调用限流（QPS、TPM）  
  - 查询与更新模型级访问授权（按 AK/SK 或角色粒度）  
  > **注意**：[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口返回的权限结构与 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 所需的 `permission` 字段格式不一致（前者含 `granted_at` 时间戳，后者仅接受 `role` 或 `ak_id`），调用前请严格参照各接口文档字段定义。

## 关键参数

| 参数 | 说明 | 是否必需 | 示例 |
|------|------|----------|------|
| `model_id` | 模型唯一标识符（非模型名称），可在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 响应中获取 | 是 | `qwen-max-20240601` |
| `quota_type` | 限流类型，取值 `qps` 或 `tpm` | 是（限流相关接口） | `qps` |
| `value` | 限流阈值整数 | 是（限流相关接口） | `10` |
| `principal_type` | 授权主体类型，`ak` 或 `role` | 是（授权相关接口） | `ak` |

## 使用方式

1. **认证**：所有模型管理 API 均需携带 `Authorization: Bearer <access_token>` 请求头，`access_token` 通过 OAuth2 获取（参见 [认证与鉴权](../../raw/auth/oauth2.md)）；  
2. **调用示例（查询模型列表）**：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/models" \
     -H "Authorization: Bearer $ACCESS_TOKEN"
   ```
3. **批量操作**：暂不支持单次请求管理多个模型，需逐个调用；批量需求建议自行封装脚本，参考 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 的分页参数 `limit` 和 `next_token`。

## 限制和注意事项

- 单账号默认最多可为一个模型配置 50 条独立授权规则（AK/角色级）；超出需提交工单申请扩容；  
- 模型限流更新后**立即生效**，无缓存延迟，但部分旧客户端可能因连接复用导致短暂未生效（建议强制刷新连接）；  
- 自定义模型的限流与授权配置，仅在其“已启用”状态下生效；若模型状态为 `disabled`，相关策略将被忽略 —— 此行为与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中描述的状态机逻辑一致；  
- 所有模型管理接口均不支持跨地域调用（如华东1区账号不可调用华北2区模型管理接口），地域信息需与模型注册时指定的 `region_id` 严格匹配。

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


