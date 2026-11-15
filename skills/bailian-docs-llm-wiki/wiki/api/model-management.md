# model management

模型管理是百炼平台的核心能力之一，为开发者提供统一的模型发现、权限控制、配额设置与限流管理接口。所有操作均基于业务空间（Workspace）隔离，支持按地域调用，并通过 API Key 进行身份认证。开发者可通过 HTTP API 或 DashScope Python SDK 2.x 完成全流程管理。

## 支持的模型与功能

百炼平台支持多源模型，涵盖文本生成（TG）、深度思考（Reasoning）、视觉理解（VU）、图片/视频生成（IG/VG）、语音识别（ASR）、TTS、3D 生成等能力。模型来源包括 `qwen`（阿里巴巴-千问）、`zhipu-ai`（智谱AI）、`kling`（可灵AI）、`vidu`（Vidu）、`tripo`（Tripo）等 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。除基础推理外，部分模型还支持 function calling、结构化输出、web search、cache 缓存、批量推理和 fine-tuning 等特性（见 `features` 字段）。模型部署模式支持全球（`global`）、中国（`asia-pacific-china`）、欧盟（`european-union`）、美国（`united-states`）等多地域服务站点。

> **注意**：文档 1 中 `inference_providers` 列表包含 `moonshot`（Kimi），但文档 2 和文档 5 的示例及错误码说明中未体现该 provider 的实际限流或授权行为；当前生产环境以 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 返回的实际 `model_limit` 字段为准，`moonshot` 暂未开放独立配额配置。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **模型标识** | `model`（ID）、`name`（模糊名） | `model` 用于精确查询（如 `qwen3.8-max`），`name` 仅用于前端展示名模糊匹配 |
| **权限控制** | `inference` / `finetune` / `deploy` | 布尔值，分别控制推理、微调、部署权限；`finetune` 和 `deploy` 在多数模型上默认为 `false`，需显式授权 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) |
| **限流配额** | `request_limit` + `request_limit_period`（QPS/QPM）、`usage_limit` + `usage_limit_period`（TPM） | `request_limit_period=1` 表示 QPS，`=60` 表示 QPM；TPM 豁免需先 `DELETE` 再 `OVERLAY` 设置仅 QPM |
| **模型能力筛选** | `capabilities`、`features`、`supports` | 仅在 HTTP API 查询时生效（如 `capabilities=TG&capabilities=Reasoning`），SDK 2.x 不支持服务端能力过滤 |

## 使用方式

- **发现模型**：调用 `GET /api/v1/models`，支持按 `providers`（作者）、`capabilities`（能力）、`context_window`（上下文长度）等筛选，返回含定价、模态、上下文窗口等元信息的完整模型列表。
- **管理权限**：  
  - 查询：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取已授权模型及其 `inference`/`fine_tune`/`deploy` 状态；  
  - 更新：`POST /api/v1/models/permissions` 支持逐模型授权（`models` 数组）或一键授权全部推理模型（`access_all_entities=OPEN`）。
- **配置限流**：  
  - 查询：`GET /api/v1/models/limits` 获取账号级（`model_limit`）与业务空间级（`workspace_limit`）配额；  
  - 更新：`POST /api/v1/models/limits` 使用 `operation_type=OVERLAY` 合并更新，或 `DELETE` 彻底移除限流。

所有接口均需在请求头中携带 `Authorization: Bearer <API Key>`，且 endpoint 中 `{WorkspaceId}` 需替换为实际业务空间 ID。Python SDK 示例见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 限制和注意事项

- 模型列表分页默认 `page_size=20`，最大支持 `200`（见文档 3 的 `page_size` 说明），但文档 1 未明确上限，以实际响应 `400 Bad Request` 错误为准。
- `providers` 参数在 DashScope Python SDK 2.x 中**仅客户端筛选当前页**，`output.total` 仍为未筛选总数（文档 1 明确提示），务必在业务逻辑中做二次过滤。
- 限流更新存在强约束：若模型无现有 QPM 限制，直接设置 TPM 会报错 `"Cannot set TPM without QPM"`（文档 5），必须先设 QPM 或采用两步法（`DELETE` → `OVERLAY`）。
- 授权范围 `authorization_scope=AUTHORIZABLE`（默认）仅返回“当前可申请授权”的模型列表，不包含已禁用或地域不可用模型；实际可用性需结合 `service_site` 和 `supports` 字段判断。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)


