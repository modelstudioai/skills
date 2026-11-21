# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与使用监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、设置业务空间级访问权限、调整调用配额，并基于返回的上下文长度、模态支持、定价等字段进行选型与集成。所有操作均需通过 API Key 认证，并按地域 Endpoint 调用。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型生态，涵盖文本生成（TG）、深度思考（Reasoning）、视觉理解（VU）、图片/视频生成（IG/VG）、语音识别（ASR）、TTS、3D 生成及实时全模态（Realtime-Omni）等能力。模型作者包括 `qwen`、`zhipu-ai`、`moonshot-ai`、`deepseek`、`kling`、`vidu` 等十余家供应商；推理服务由 `aliyun-bailian`、`siliconflow`、`moonshot` 等多家服务商提供。模型特性（如 `function-calling`、`structured-outputs`、`cache`、`web-search`）和部署模式（如 `ptu`）均可在查询时筛选。详细能力列表与可选值请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 1 中 `inference_providers` 列表包含 `moonshot`（对应 Kimi），但文档 5 的 `update-model-permissions.md` 中未提及该 provider 的授权兼容性；实际授权行为以 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 接口为准，不支持对非 `aliyun-bailian` 提供的模型执行 `deploy` 操作。

## 关键参数

模型管理相关接口共用以下核心参数：

- `model`（String）：模型 ID，用于精确查询或配置，如 `qwen3.8-max`；
- `name`（String）：模型名称模糊搜索，适用于列表类接口；
- `page_no` / `page_size`（Integer）：分页参数，`page_no` 从 1 开始，`page_size` 最大支持 200（[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 明确限定为 1–200）；
- `authorization_scope`（String）：仅用于权限接口，取值 `AUTHORIZABLE`（默认）或 `AUTHORIZED`；
- `access_all_entities`（String）：仅用于授权更新，支持 `OPEN`/`CLOSE`/`KEEP`，决定是否启用一键授权。

此外，限流接口特有 `request_limit`（QPM/RPS）、`usage_limit`（TPM）、`request_limit_period` 和 `usage_limit_period`；模型列表接口支持 `capabilities`、`features`、`context_window`、`service_site` 等高阶筛选参数。

## 使用方式

### 查询类操作
- **查模型列表**：调用 `GET /api/v1/models`，支持按作者（`providers`）、能力（`capabilities`）、特性（`features`）等多维过滤，返回含定价、上下文长度、模态支持的完整元数据；
- **查模型限额**：调用 `GET /api/v1/models/limits`，获取账号级（`model_limit`）与业务空间级（`workspace_limit`）的 QPM/TPM/异步并发等配额；
- **查模型授权**：调用 `GET /api/v1/models/permissions`，确认当前业务空间对各模型的 `inference`/`fine_tune`/`deploy` 权限状态。

### 配置类操作
- **更新限流**：调用 `POST /api/v1/models/limits`，支持 `OVERLAY`（合并覆盖）与 `DELETE`（清空限流）两种 `operation_type`。注意：TPM 设置依赖 QPM 已存在，否则报错 `Cannot set TPM without QPM`；
- **更新授权**：调用 `POST /api/v1/models/permissions`，支持逐模型设置布尔权限，或通过 `access_all_entities=OPEN` 一键授权全部推理模型（含未来新增）。

所有接口均需在请求头中携带 `Authorization: Bearer <API_KEY>`，并替换 `{WorkspaceId}` 为实际业务空间 ID。Python SDK 调用示例详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且未显式设置时默认继承账号级配额；
- **限流删除风险**：使用 `DELETE` 操作清空限流时，存在短暂无保护窗口期，生产环境建议采用两步法并评估风险；
- **授权范围隔离**：`access_all_entities=OPEN` 仅授予 `INFERENCE` 权限，`fine_tune` 与 `deploy` 仍需显式逐模型配置，且 `deploy` 仅对百炼托管模型生效；
- **地域一致性**：所有模型管理接口必须与模型调用所选地域保持一致（如北京地域模型需调用 `cn-beijing` Endpoint），跨地域查询可能返回空或过期数据；
- **分页总数差异**：DashScope Python SDK 2.x 在 `list()` 响应中将总数字段命名为 `total_count`，而原始 HTTP 响应为 `output.total`，注意适配；
- **模型下线提示**：部分模型响应中含 `inference_offline_info.offline_time` 字段，表示预计下线时间，建议定期轮询或监听变更。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


