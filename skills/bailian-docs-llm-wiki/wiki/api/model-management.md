# model management

模型管理是百炼平台为开发者提供的核心能力，用于查询、授权、限流和配置模型的生命周期行为。通过统一的 REST API 接口，开发者可动态获取模型元信息、控制模型调用权限、设置业务级配额，并适配不同场景（如推理、微调、部署）的访问策略。所有操作均基于 Workspace 粒度进行隔离与管控。

## 支持的模型/功能

百炼平台支持多供应商、多模态、多能力的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）、3D 生成（`3D-generation`）等 [capabilities](../../raw/model-api-reference/model-management/list-models.md)。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，且支持按 `providers` 或 `inference_providers` 精确筛选。模型能力维度还包括 `function-calling`、`structured-outputs`、`web-search`、`cache`、`batch`、`fine-tuning` 等 [features](../../raw/model-api-reference/model-management/list-models.md)，便于开发者按需匹配业务需求。

> **注意**：文档 4 中 `update-model-permissions` 的请求参数字段名为 `finetune`（无下划线），但文档 5 的返回字段为 `fine_tune`（带下划线）；实际调用时应以请求体字段名 `finetune` 为准，SDK 或客户端需做兼容处理。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **模型标识** | `model`（ID）、`name`（模糊搜索） | 所有接口均支持按模型 ID 精确匹配或名称模糊检索 |
| **权限控制** | `inference` / `finetune` / `deploy`（布尔值） | 控制模型在当前 Workspace 的可用能力，详见 [update-model-permissions](../../raw/model-api-reference/model-management/update-model-permissions.md) |
| **限流配额** | `request_limit`（QPM/QPS）、`usage_limit`（TPM）、`request_limit_period`、`usage_limit_period` | 单位为秒，`60` 表示分钟级，`1` 表示秒级；`usage_limit_field` 固定为 `total_tokens` |
| **筛选维度** | `capabilities`、`features`、`providers`、`service_site`、`supports` | 仅 `list-models` 接口支持，用于发现符合业务要求的模型 |

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，支持分页（`page_no`/`page_size`）及多维筛选（如 `capabilities=TG&providers=qwen`）。Python SDK 的 `Models.list()` 仅支持分页，复杂筛选需直接调用 HTTP API [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **管理模型授权**：调用 `POST /api/v1/models/permissions` 设置单个或批量模型的 `inference`/`finetune`/`deploy` 权限；也可使用 `access_all_entities=OPEN` 一键授权全部推理模型。
- **配置模型限流**：调用 `POST /api/v1/models/limits` 设置 QPM 和 TPM 配额，支持 `OVERLAY`（合并覆盖）与 `DELETE`（清空）两种操作类型；若需“仅限 QPM、不限 TPM”，须先 `DELETE` 再 `OVERLAY` 设置 QPM。
- **查询当前配额与权限**：分别调用 `GET /api/v1/models/limits` 和 `GET /api/v1/models/permissions`，后者支持 `authorization_scope=AUTHORIZED` 获取已启用权限的模型清单。

## 限制和注意事项

- 模型限流接口（`/models/limits`）要求：若设置 `usage_limit`，必须同时设置 `request_limit`；否则会返回 `InvalidParameter` 错误（如文档 2 所述）。
- `list-models` 接口的 `context_window` 参数含义为“严格小于该值”，非“大于等于”或“等于”；且部分图像/视频模型（如 `qwen-image-3.0-pro`）的 `context_window` 字段为 `null`，不可用于筛选。
- 所有接口均需在 Header 中携带 `Authorization: Bearer {API_KEY}`，且 Endpoint 中的 `{WorkspaceId}` 必须替换为真实业务空间 ID；国际站与国内站 Endpoint 不同，不可混用。
- `update-model-permissions` 接口对 `finetune` 字段的描述存在不一致：文档 4 请求体字段名为 `finetune`，而文档 5 返回体中为 `fine_tune`；建议客户端以请求字段为准，并忽略返回字段命名差异。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)


