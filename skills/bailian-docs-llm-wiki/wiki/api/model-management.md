# model management

模型管理是百炼平台为开发者提供的核心能力，用于统一查看、配置和控制所使用大模型的访问权限与调用配额。通过 RESTful API 可实现自动化运维，适用于多租户、多模型场景下的精细化治理。所有操作均需具备对应模型的 `model:manage` 权限。

## 支持的模型与功能

当前支持对平台已接入的全部托管模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通义系列模型及部分第三方合作模型）进行以下管理操作：  
- 查询模型列表（含状态、版本、支持的输入/输出格式）  
- 查询与更新模型级限流策略（按 QPS 或 TPS 限制）  
- 查询与更新模型级授权策略（指定用户/角色/应用 ID 的调用权限）  

详细接口定义请参阅 [模型管理](../../raw/model-api-reference/model-management.md) 文档。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen-max`；必须为 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的有效 ID |
| `quota_type` | string | 是 | 限流类型，仅支持 `qps`（每秒请求数）或 `tps`（每秒 token 数） |
| `scope` | string | 是 | 授权范围，取值为 `user`、`role` 或 `app`，对应 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 中定义的粒度 |

> **注意**：`update-model-rate-limits` 接口的 `reset_time` 字段在 v2.3+ 版本中已弃用，新策略将立即生效，旧文档中提及的“重置窗口”逻辑不再适用。

## 使用方式

1. **认证**：使用 `Bearer <access_token>` 请求头，[Token](../concepts/token.md) 需含目标模型的 `model:manage` 权限  
2. **调用示例（更新限流）**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/models/qwen-max/rate-limits \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"quota_type":"qps","limit":5}'
   ```
3. 所有管理接口均遵循 `/api/v1/models/{model_id}/[subpath]` 路径规范，完整路径结构见 [模型管理](../../raw/model-api-reference/model-management.md)。

## 限制和注意事项

- 单个模型最多配置 100 条独立授权规则（`user` + `role` + `app` 合计）  
- 限流策略变更后，全量生效延迟 ≤ 3 秒，不支持秒级灰度  
- `list-models` 接口默认仅返回启用状态（`status=enabled`）的模型；如需包含测试中或已下线模型，须显式传入 `status=all` 参数 —— 此行为与早期文档描述不一致，请以 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 最新版为准  
- 非阿里云主账号创建的应用无法调用 `update-model-permissions` 修改跨租户授权策略

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


