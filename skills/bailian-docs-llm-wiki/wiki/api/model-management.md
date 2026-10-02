# model management

模型管理是百炼平台为开发者提供的核心能力，用于查询、授权和限流控制业务空间内可用的模型。通过统一的 REST API，可实现模型发现、权限配置与配额调整，支撑多模型协同与资源精细化管控。所有操作均基于业务空间（Workspace）维度进行隔离。

## 支持的模型/功能

百炼平台支持多供应商、多模态、多能力的模型体系，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek` 等十余家厂商，并支持按 `providers`、`capabilities`、`features`（如 `function-calling`、`structured-outputs`）等维度筛选。完整模型列表及元数据（含上下文长度、定价、输入/输出模态）可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口获取。

模型权限分为三类：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。并非所有模型默认开放全部权限；例如 `qwen3-max` 在返回示例中显示 `"fine_tune": true`，而 `qwen-plus` 为 `false`。权限状态需通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 确认，且仅已授权模型才可被调用或限流配置。

> **注意**：文档 4 中 `supports` 参数默认值为 `inference`，但实际接口行为以 `authorization_scope=AUTHORIZED` 查询结果为准；若某模型未出现在 `AUTHORIZED` 列表中，则即使其在 `list-models` 中存在，也无法直接调用。

## 关键参数

| 参数名 | 作用 | 说明 |
|--------|------|------|
| `model`（String） | 模型唯一标识 | 所有管理接口均以此字段定位模型，如 `qwen-plus`、`qwen3-max`，必须与 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `model` 字段严格一致。 |
| `request_limit` / `usage_limit` | 限流配额 | 分别表示 QPM/RPM（请求次数）与 TPM（[Token](../concepts/token.md) 用量），单位周期由 `*_period` 决定（秒）。`request_limit_period=1` 表示 QPS，`=60` 表示 RPM。 |
| `operation_type`（`OVERLAY`/`DELETE`） | 限流更新语义 | 仅用于 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)，决定是覆盖现有配置还是彻底清除。 |
| `access_all_entities`（`OPEN`/`CLOSE`/`KEEP`） | 授权范围控制 | 用于 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)，`OPEN` 将自动授权当前及未来所有推理模型，适合快速开通环境。 |

## 使用方式

1. **发现模型**：调用 `GET /api/v1/models`，按 `providers=qwen&capabilities=TG` 等条件筛选，获取目标模型 ID 与能力详情。  
2. **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`，确认模型是否已获 `inference: true`。若未授权，需先执行下一步。  
3. **授权模型**：调用 `POST /api/v1/models/permissions`，传入 `{"models": [{"model": "qwen-plus", "inference": true}]}` 或 `{"access_all_entities": "OPEN"}`。  
4. **配置限流**：调用 `POST /api/v1/models/limits` 设置 `request_limit` 和 `usage_limit`；如需仅限 QPM、豁免 TPM，须分两步：先 `DELETE` 后 `OVERLAY` 仅设 `request_limit`（详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 的 TPM 豁免说明）。  
5. **验证配额**：调用 `GET /api/v1/models/limits` 查看生效的 `model_limit`（账号级）与 `workspace_limit`（业务空间级）。

所有接口均需在 Header 中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，且 Endpoint 需替换 `{WorkspaceId}`。Python SDK 仅对 `list-models` 提供基础分页封装（`Models.list()`），其余管理操作推荐直接使用 HTTP 请求。

## 限制和注意事项

- **限流依赖权限**：必须先完成模型授权（`inference: true`），才能为其设置限流；否则 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 将返回 `InvalidParameter` 错误：“Model X is not authorized for Inference”。  
- **TPM 依赖 QPM**：若当前无 QPM 限制，单独设置 TPM 会失败（错误信息明确提示“please set QPM first”），必须先设置 `request_limit`。  
- **批量上限**：`update-model-permissions` 接口 `models` 数组最多 20 项；`update-model-rate-limits` 最多 200 项。超出需分批调用。  
- **地域与 Endpoint 差异**：`list-models` 接口支持多地域（如新加坡、德国），但 `list-quotas`、`update-model-rate-limits` 等管理接口目前仅支持华北2（北京）Endpoint，其他地域调用将失败。  
- **异步任务限制**：部分模型（如 `wan2.6-i2v-flash`）在 `list-quotas` 返回中包含 `async_user_queue_limit` 和 `async_user_concurrency_limit`，该参数仅适用于异步推理任务，同步调用不生效。

## 来源文档

- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)


