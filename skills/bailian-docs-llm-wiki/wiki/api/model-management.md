# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与用量监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、设置调用配额、授权模型使用权限，并基于返回的 `model` ID 直接发起推理请求。所有操作均需通过 API Key 认证，且作用域默认为当前业务空间（Workspace）。

## 支持的模型与功能

百炼平台支持多供应商、多模态、多能力的模型集合，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成、实时全模态等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，同时支持 `aliyun-bailian`（百炼自研推理服务）及 `siliconflow`、`mini-max` 等第三方推理提供商。详细模型列表、能力标签（`capabilities`）、功能特性（`features`，如 `function-calling`、`structured-outputs`、`web-search`）及部署模式（`service_site`、`deployment_methods`）均可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口获取。

> **注意**：文档 1 中 `inference_providers` 列表包含 `moonshot`（Kimi），但文档 5 的 `providers` 示例中未列出该值；实际使用时请以 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回的 `inference_provider` 字段为准，避免硬编码过时枚举。

## 关键参数

模型管理相关接口共用以下核心参数：

- **`model`（String）**：模型唯一 ID（如 `qwen3-max`），用于精确查询、限额设置与权限更新，是调用推理 API 的必需字段。
- **`page_no` / `page_size`（Integer）**：分页参数，适用于所有列表类接口（`/models`、`/models/limits`、`/models/permissions`），默认 `page_no=1`、`page_size=20`。
- **限流参数**：`request_limit`（QPM/QPS）、`request_limit_period`（秒）、`usage_limit`（TPM）、`usage_limit_period`（秒），见 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 与 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **权限参数**：`inference`、`finetune`、`deploy`（Boolean），控制对应操作的授权状态，详见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)。

## 使用方式

### 1. 查询可用模型  
调用 `GET /api/v1/models`，支持按 `capabilities=TG`、`providers=qwen`、`features=function-calling` 等多维度筛选。Python SDK 仅支持分页参数，复杂筛选需直接调用 HTTP API：  
```bash
curl --get "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --data-urlencode "capabilities=TG" \
  --data-urlencode "providers=qwen"
```

### 2. 查询与设置限流  
- 查询配额：`GET /api/v1/models/limits?model=qwen3-max`  
- 更新配额：`POST /api/v1/models/limits`，传入 `models` 数组，支持 `OVERLAY`（覆盖）或 `DELETE`（清空）。注意：TPM 设置需先存在 QPM 配置，否则报错 `InvalidParameter`。

### 3. 管理模型权限  
- 查询已授权模型：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`  
- 授权单个模型：`POST /api/v1/models/permissions`，传 `{"models": [{"model":"qwen-plus","inference":true,"finetune":true}]}`  
- 一键授权全部推理模型：`{"access_all_entities": "OPEN"}`  

## 限制和注意事项

- **权限优先级**：模型必须先在 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 中返回 `"inference": true`，才可调用推理接口；未授权模型会返回 `403 Forbidden`。
- **限流继承关系**：`model_limit` 是账号级上限，`workspace_limit` 是业务空间级上限（可为空），后者不能超过前者。异步任务有独立限流字段（`async_user_queue_limit`、`async_user_concurrency_limit`）。
- **SDK 功能限制**：DashScope Python SDK 的 `Models.list()` 方法**不支持**按 `capabilities`、`features` 等条件筛选，仅支持分页，详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **Endpoint 差异**：国际站与国内站 Endpoint 不同（如 `dashscope-intl.aliyuncs.com` vs `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），务必根据地域选择正确地址，且 `{WorkspaceId}` 仅在国内站 URL 中出现。
- **模型下线提示**：返回结果中的 `inference_offline_info.offline_time` 字段标识模型预计下线时间，建议定期检查并迁移至替代模型。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


