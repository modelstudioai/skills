# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控模型的使用。通过统一的 RESTful API，开发者可程序化地查询可用模型列表、配置模型访问权限、设置调用配额，并实时查看限额状态。所有操作均基于业务空间（Workspace）维度进行隔离与管控。

## 支持的模型/功能

百炼平台支持多模态、多供应商的模型生态，涵盖文本生成（`TG`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，同时支持 `aliyun-bailian`（百炼自研推理服务）及 `siliconflow`、`vanchin` 等第三方推理提供商。详细能力矩阵与供应商列表请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 1 中 `inference_providers` 列表包含 `moonshot`（Kimi），但文档 4 的 `update-model-permissions.md` 中未列出该值作为合法 `model` ID；实际调用时应以 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `model` 字段为准，避免硬编码供应商别名。

## 关键参数

模型管理涉及三类关键参数体系：

- **筛选参数**（GET `/models` 和 `/models/permissions`）：`name`（模糊匹配）、`model`（精确 ID）、`capabilities`（如 `TG`, `VU`）、`features`（如 `function-calling`, `web-search`）、`providers`（作者）、`service_site`（部署地域）等，支持组合过滤。
- **权限参数**（POST `/models/permissions`）：`inference`（推理）、`finetune`（微调）、`deploy`（部署），布尔值控制开关；另支持 `access_all_entities=OPEN` 实现一键全量授权。
- **限流参数**（POST `/models/limits` 和 GET `/models/limits`）：`request_limit`（QPM/QPS）、`request_limit_period`（秒，默认 `60` 为分钟级）、`usage_limit`（TPM）、`usage_limit_field`（如 `total_tokens`）。注意：设置 `usage_limit` 前必须已存在 `request_limit`（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 错误码说明）。

## 使用方式

- **发现模型**：调用 `GET /api/v1/models` 查询全量或筛选后的模型列表，推荐优先使用 HTTP API（而非 SDK）以支持完整参数过滤；Python SDK 的 `Models.list()` 仅支持分页，不支持 `capabilities` 或 `providers` 等条件筛选（详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。
- **授权模型**：先调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZABLE` 获取可授权模型列表，再通过 `POST /api/v1/models/permissions` 设置 `inference`/`finetune` 权限；对新业务空间，建议使用 `access_all_entities=OPEN` 快速启用全部推理模型。
- **配置限流**：使用 `GET /api/v1/models/limits` 查看当前配额，再通过 `POST /api/v1/models/limits` 更新。若需“仅限 QPM、不限 TPM”，须分两步：先 `DELETE` 全部限流，再 `OVERLAY` 仅设 `request_limit`（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 的 TPM 豁免说明）。
- **监控限额**：定期轮询 `GET /api/v1/models/limits`，解析 `output.quotas[].model_limit` 和 `workspace_limit` 字段，注意 `request_limit_period=1` 表示 QPS，`=60` 表示 RPM。

## 限制和注意事项

- 单次请求最多返回 200 条记录（`page_size` 上限），模型列表需分页遍历；权限与限额接口同理。
- 模型授权变更非实时生效，通常在 30 秒内同步至推理网关；限流配置变更亦有秒级延迟。
- `POST /models/permissions` 中 `finetune` 字段在文档 4 中拼写为 `finetune`，但文档 3 的返回字段名为 `fine_tune`（带下划线）；实际请求体应使用 `finetune`，响应体中为 `fine_tune`，二者语义一致。
- 所有 API 均需在 Header 中携带 `Authorization: Bearer {API_KEY}`，且 Endpoint 中 `{WorkspaceId}` 必须替换为真实业务空间 ID；国际站用户需使用 `dashscope-intl.aliyuncs.com` 等对应域名（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 地域说明）。
- 模型下线信息通过 `inference_offline_info.offline_time` 字段返回，调用方应主动检查并做好降级预案。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)


