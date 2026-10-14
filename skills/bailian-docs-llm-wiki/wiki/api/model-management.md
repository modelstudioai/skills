# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、限流配额与用量监控等全生命周期管理功能。开发者可通过统一 API 接口查询可用模型、配置调用权限、设置 QPM/TPM 限流，并实时查看当前配额使用情况。所有操作均基于业务空间（Workspace）维度进行隔离与管控。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型接入，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商；推理服务可由 `aliyun-bailian`（百炼）、`siliconflow`（硅基流动）、`mini-max` 等提供。具体支持的模型列表、能力标签（`capabilities`）、功能特性（`features`，如 `function-calling`、`structured-outputs`、`web-search`）及上下文窗口等元数据，均可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口获取。

## 关键参数

模型管理相关接口共用以下关键参数：

- **`model`**：模型 ID（如 `qwen3.8-max`），用于精确标识目标模型，是所有管理操作的必填标识符。
- **`workspace_id`**：业务空间 ID，所有限流与权限配置均作用于该空间，调用时需替换 Endpoint 中的 `{WorkspaceId}` 占位符。
- **`authorization_scope`**：在权限查询中用于区分 `AUTHORIZABLE`（可授权模型）与 `AUTHORIZED`（已授权模型），详见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)。
- **`operation_type`**：限流更新中指定 `OVERLAY`（合并覆盖）或 `DELETE`（删除限流），影响字段更新语义，见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **`access_all_entities`**：一键授权开关，取值 `OPEN`/`CLOSE`/`KEEP`，用于批量控制推理权限，避免逐模型重复配置。

> **注意**：文档 5 中 `/api/v1/models/limits` 的 GET 方法（查询限额）与文档 2 中同路径的 POST 方法（更新限流）共享同一 URL，但语义与参数结构完全不同（前者 Query 参数，后者 JSON Body）。开发者需严格区分 HTTP 方法，否则将触发 `405 Method Not Allowed` 或逻辑错误。

## 使用方式

### 1. 查询模型元信息  
调用 `GET /api/v1/models`，支持按 `providers`、`capabilities`、`features` 等多维条件筛选，返回模型 ID、描述、定价、上下文长度及输入/输出模态等完整信息。Python SDK 仅支持分页参数（`page`/`page_size`），复杂筛选请直接使用 HTTP API。

### 2. 管理模型权限  
- 查询：`GET /api/v1/models/permissions`，通过 `authorization_scope=AUTHORIZED` 获取当前已开通推理权限的模型列表。  
- 更新：`POST /api/v1/models/permissions`，支持两种模式：  
  - **逐模型授权**：在 `models[]` 中显式声明 `inference`/`finetune`/`deploy` 布尔值；  
  - **一键授权**：设置 `access_all_entities=OPEN` 自动授予当前空间全部推理模型权限（含后续新增）。

### 3. 配置与监控限流  
- 查询配额：`GET /api/v1/models/limits`，返回 `model_limit`（账号级上限）与 `workspace_limit`（空间级配置），其中 `request_limit_period=1` 表示 QPS，`=60` 表示 RPM。  
- 更新限流：`POST /api/v1/models/limits`，支持为单个或多个模型设置 `request_limit`（QPM/RPM）和 `usage_limit`（TPM）。若需“仅限 QPM、不限 TPM”，必须先 `DELETE` 再 `OVERLAY` 设置 QPM，因系统强制要求 QPM 存在后才允许设置 TPM（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 错误码说明）。

## 限制和注意事项

- **权限生效延迟**：模型授权变更通常在 30 秒内生效，但部分新模型可能需额外同步时间，建议授权后等待片刻再发起推理请求。  
- **限流继承关系**：`workspace_limit` 不得超过 `model_limit`；若未设置 `workspace_limit`，则直接继承 `model_limit`。  
- **API Key 作用域**：所有管理接口均校验 `DASHSCOPE_API_KEY` 所属主账号及其关联业务空间权限，子用户需具备对应 Workspace 的 `ManageModels` 权限。  
- **SDK 功能缺口**：DashScope Python SDK 的 `Models.list()` 方法不支持 `capabilities`、`providers` 等高级筛选参数，必须使用原始 HTTP API 实现精准模型发现 —— 此限制已在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中明确说明。  
- **模型下线提示**：返回结果中的 `inference_offline_info.offline_time` 字段标明预计下线时间，建议定期检查并提前迁移。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)


