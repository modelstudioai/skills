# model management

模型管理功能为开发者提供对百炼平台托管模型的元信息查询、访问控制与配额配置能力，支持通过 REST API 对模型列表、限流策略和授权策略进行细粒度操作。所有接口均需使用 `Authorization: Bearer <token>` 认证，且仅对拥有对应项目（project）管理员或模型管理员角色的用户开放。该能力不涉及模型训练或部署生命周期管理，仅聚焦于运行时访问治理。

## 支持的模型与功能

- **支持的模型类型**：当前仅支持百炼平台预置的 SaaS 模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo` 等），不支持用户自定义部署的私有模型实例。  
- **核心功能**：包括查询模型列表、查询/更新模型限流配额、查询/更新模型授权范围（即哪些 project 或 user group 可调用该模型）。完整功能清单见 [模型管理](../../raw/model-api-reference/model-management.md)。  
- 所有操作均基于模型 ID（如 `qwen-max`）而非模型别名或版本号；模型 ID 须严格匹配 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `model_id` 字段。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，区分大小写，例如 `qwen-max` |
| `project_id` | string | 否（部分接口必需） | 目标项目 ID；若为空，则操作作用于全局模型策略（需平台级权限） |
| `rate_limit` | object | 否（`update-model-rate-limits` 必需） | 包含 `requests_per_minute` 和 `tokens_per_minute` 两个整数字段，单位为每分钟请求数/[Token](../concepts/token.md) 数 |
| `permissions` | array of object | 否（`update-model-permissions` 必需） | 每项含 `type`（`project` 或 `user_group`）和 `id`（对应 ID） |

> **注意**：`list-quotas` 接口返回的 `rate_limit` 结构在 [查询模型限流](../../raw/model-api-reference/model-management/list-quotas.md) 中定义为扁平对象（如 `{ "requests_per_minute": 60 }`），但 `update-model-rate-limits` 要求嵌套在 `rate_limit` key 下；二者结构不一致，实际请求体必须遵循 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 的 schema，否则返回 400。

## 使用方式

1. **查询模型列表**：`GET /v1/models`，返回全部可用模型及其基础元数据（名称、描述、输入/输出 token 限制等）；适用于初始化客户端或构建模型选择器。  
2. **配置限流**：先调用 `GET /v1/models/{model_id}/quotas` 获取当前策略，再用 `PATCH /v1/models/{model_id}/quotas` 提交更新；支持按 `project_id` 细化到项目级配额。  
3. **管理授权**：通过 `GET /v1/models/{model_id}/permissions` 查看当前授权范围，使用 `PATCH /v1/models/{model_id}/permissions` 增删 `project` 或 `user_group` 条目。详细行为参见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)。

## 限制和注意事项

- 单次 `update-model-permissions` 请求最多修改 50 条授权规则；超出将返回 `400 Bad Request`。  
- 限流策略中 `tokens_per_minute` 不可设为 `0`（禁用模型需通过权限移除实现）；设为 `-1` 表示不限流（仅限平台管理员）。  
- 所有更新操作均为全量覆盖（非增量 patch）：提交的 `permissions` 数组将完全替换现有授权列表，务必在 `GET` 后合并新增项再提交。  
- 模型 ID 不可变更，且不支持删除模型条目——“禁用”模型应通过移除所有 `permissions` 并设置极低 `rate_limit` 实现。  
- 部分旧版文档提及 `model_version` 参数，但当前所有接口均忽略该字段；实际模型版本由平台统一维护，开发者无需指定——详见 [模型管理](../../raw/model-api-reference/model-management.md)。

## 来源文档

- [模型管理](../../raw/model-api-reference/model-management.md)


