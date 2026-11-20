# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制与限流配置三大功能。开发者可通过统一 API 查询模型元信息（如能力、定价、上下文长度）、设置业务空间级模型调用权限（推理/微调/部署），以及精细化管控请求频率（QPS/QPM）与用量（TPM）。所有操作均基于业务空间（Workspace）隔离，支持多地域部署。

## 支持的模型与功能

- **模型发现**：通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口获取全量模型信息，支持按作者（`providers`）、能力（`capabilities`，如 `Reasoning`、`VU`）、模态（`request_modality`/`response_modality`）、特性（`features`，如 `function-calling`）等多维度筛选，并返回定价、上下文窗口（`context_window`）、发布时间等关键元数据。
- **权限控制**：通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 和 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 接口管理业务空间内模型的访问权限，支持逐模型授权（`models` 数组）与一键授权（`access_all_entities=OPEN`）两种模式，权限粒度包括 `inference`（必选）、`fine_tune`、`deploy`。
- **限流配置**：通过 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 和 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 接口管理账号级（`model_limit`）与业务空间级（`workspace_limit`）限流策略，支持 RPM/QPS、TPM 及异步任务并发与排队数（`async_user_concurrency_limit`/`async_user_queue_limit`）。

> **注意**：文档 5 中列出的 `deployment_methods=ptu` 和 `deployment_ptu_service_tiers` 参数在文档 1–4 的限流与权限接口中均未体现，当前限流配置不感知 PTU 部署模式，相关行为以实际 API 响应为准。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `model` / `name` | Query 或 Body | String | 模型 ID（精确）或名称（模糊） | `qwen3.8-max`, `qwen` |
| `page_no` / `page_size` | Query | Integer | 分页参数，`page_no` 从 1 开始 | `1`, `100` |
| `request_limit` / `request_limit_period` | Body (`models[].*`) | Number | 请求限流值及周期（秒），`60`=QPM，`1`=QPS | `60`, `1` |
| `usage_limit` / `usage_limit_period` | Body (`models[].*`) | Number | 用量限流值及周期（秒），单位为 Token | `100000`, `60` |
| `operation_type` | Body (`models[].operation_type`) | String | 限流操作类型：`OVERLAY`（覆盖）或 `DELETE`（清空） | `"OVERLAY"` |
| `authorization_scope` | Query | String | 权限查询范围：`AUTHORIZABLE`（可授）或 `AUTHORIZED`（已授） | `"AUTHORIZED"` |
| `access_all_entities` | Body | String | 一键授权开关：`OPEN`/`CLOSE`/`KEEP` | `"OPEN"` |

## 使用方式

1. **查询模型**：使用 `GET /api/v1/models`，推荐先按 `providers=qwen` 或 `capabilities=TG` 筛选，再用 `model=qwen3.8-max` 获取单模型详情。  
2. **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认目标模型是否已开通 `inference` 权限。  
3. **授权模型**：若未授权，调用 `POST /api/v1/models/permissions` 提交 `{"models":[{"model":"qwen3.8-max","inference":true}]}`。  
4. **配置限流**：调用 `GET /api/v1/models/limits?model=qwen3.8-max` 查看当前配额，再用 `POST /api/v1/models/limits` 设置 `request_limit=120`（QPM）和 `usage_limit=200000`（TPM）。  
5. **验证生效**：再次调用 `list-quotas` 接口确认 `workspace_limit` 字段已更新。

> **注意**：文档 2 明确要求“若需只限制 RPM、豁免 TPM”，必须分两步执行（先 `DELETE` 再 `OVERLAY` 设置 QPM），而文档 1 的示例中 `qwen3.8-max` 的 `usage_limit` 为 `500000`（非 null），表明该模型默认启用 TPM 限制。两者逻辑一致，但开发者需主动选择是否启用 TPM。

## 限制和注意事项

- **地域一致性**：所有模型管理 API 的 Endpoint 必须与业务空间所在地域匹配（如北京地域用 `cn-beijing.maas.aliyuncs.com`），跨地域调用将失败；美国弗吉尼亚地域使用独立域名 `dashscope-us.aliyuncs.com`，不带 `{WorkspaceId}` 前缀。
- **权限优先级**：模型必须先完成 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 中的 `AUTHORIZED` 状态，才能被调用；即使限流配额充足，无 `inference: true` 权限仍会返回 403 错误。
- **限流继承关系**：`workspace_limit` 不得超过 `model_limit`（账号级上限），且 `model_limit` 为 null 表示该模型无全局限制，此时 `workspace_limit` 可设为任意值（但受平台默认策略约束）。
- **异步任务限制**：仅部分模型（如 `wan2.6-i2v-flash`）支持 `async_user_queue_limit` 和 `async_user_concurrency_limit`，该字段在 `list-quotas` 响应中为 `null` 即表示不适用。
- **参数互斥性**：`update-model-rate-limits` 接口在 `operation_type=DELETE` 时，`request_limit` 和 `usage_limit` 必须为空；若仅传 `request_limit` 而未传 `request_limit_period`，将沿用当前值而非默认 `60`（文档 2 未明确定义默认值，以实际响应为准）。

## 来源文档

- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)


