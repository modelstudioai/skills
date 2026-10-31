# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、配额配置与限流管理等全生命周期操作。开发者可通过统一 API 接口查询可用模型、查看/更新授权状态、设置调用限额，并基于模型能力（如 `TG`、`VU`）和部署模式（如 `ptu`、`global`）进行精准筛选。所有操作均需使用有效的 API Key 进行认证。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型生态，涵盖文本生成（`TG`）、视觉理解（`VU`）、图片生成（`IG`）、视频生成（`VG`）、语音识别（`ASR`）、3D 生成（`3D-generation`）等 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 所定义的全部 capabilities。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek` 等十余家供应商；推理服务可由 `aliyun-bailian`、`siliconflow`、`kling` 等多家 provider 提供。模型能力（`features`）如 `function-calling`、`structured-outputs`、`web-search`、`cache`、`batch` 等均可在模型元数据中直接获取。

> **注意**：文档 3 中 `update-model-permissions.md` 的请求体字段名为 `finetune`，但文档 4 中 `list-model-permissions.md` 的返回字段为 `fine_tune`（含下划线），且文档 5 的错误示例中也使用 `fine_tune`。实际接口以 `fine_tune` 为准，`finetune` 为文档笔误。

## 关键参数

| 参数类别 | 示例参数 | 说明 |
|----------|----------|------|
| **筛选类** | `capabilities=TG&capabilities=Reasoning` | 多值需重复参数名；支持 `providers`、`inference_providers`、`features`、`service_site`、`supports` 等多维组合过滤 |
| **分页类** | `page_no=1&page_size=50` | `page_size` 最大支持 200（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)）；HTTP 接口返回 `output.total`，SDK 返回 `resp.total_count` |
| **权限类** | `{"model":"qwen-plus","inference":true,"fine_tune":false}` | `inference`/`fine_tune`/`deploy` 均为布尔值；未传表示“保持现状”；`access_all_entities=OPEN` 可一键授权全部推理模型 |
| **限流类** | `request_limit=60&request_limit_period=60` | QPM 单位为“次/分钟”；TPM 单位为“Token/分钟”；`operation_type=DELETE` 时所有限流字段必须为空 |

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，推荐使用 HTTP API（非 SDK）以支持完整筛选条件；Python SDK 的 `client.models.list()` 仅支持 `page_no`、`page_size` 和 `provider`（客户端过滤），不支持 `capabilities` 或 `features` 筛选 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。  
- **管理模型授权**：先用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZABLE` 获取可授权模型列表，再通过 `POST /api/v1/models/permissions` 设置 `inference`/`fine_tune`/`deploy` 权限或启用 `access_all_entities=OPEN`。  
- **配置调用限额**：用 `GET /api/v1/models/limits` 查看当前配额，再用 `POST /api/v1/models/limits` 更新。若需“仅限 RPM、不限 TPM”，须先 `DELETE` 再 `OVERLAY` 设置 QPM，因平台禁止单独设置 TPM（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 错误示例）。  

## 限制和注意事项

- 模型列表接口默认每页 20 条，最大 `page_size=200`（仅限 `/models/permissions`）；`/models` 接口无明确上限，但建议分页拉取避免超时。  
- 限流配置作用域为「业务空间」级别，`workspace_limit` 不能超过 `model_limit`；`async_user_queue_limit` 和 `async_user_concurrency_limit` 仅对[异步任务](../concepts/asynchronous-task.md)生效。  
- 模型授权变更后非实时生效，通常在 1–2 分钟内同步至推理网关。  
- `deployment_methods=ptu` 与 `deployment_ptu_service_tiers` 仅对支持 PTU 部署的模型有效，调用前需确认模型 `supports` 包含 `deploy` 且 `service_site` 匹配目标地域。  
- 所有模型 API 均需在 Header 中携带 `Authorization: Bearer {API_KEY}`，且 `DASHSCOPE_API_KEY` 必须已配置为环境变量或显式传入。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)


