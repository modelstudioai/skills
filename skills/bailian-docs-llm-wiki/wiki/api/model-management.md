# model management

模型管理是百炼平台的核心能力之一，为开发者提供统一的模型发现、权限控制、限流配置与元信息查询接口。所有操作均基于业务空间（Workspace）隔离，支持按地域、作者、能力、部署模式等多维度筛选，并可通过 API 或 DashScope SDK 进行自动化集成。

## 支持的模型与功能

百炼平台支持多源模型，涵盖文本生成（TG）、深度思考（Reasoning）、视觉理解（VU）、图片/视频生成（IG/VG）、语音识别（ASR）、TTS、3D 生成、实时全模态（Realtime-Omni）等能力。模型来源包括 `qwen`、`zhipu-ai`、`moonshot-ai`、`deepseek`、`kling`、`vidu` 等十余家供应商，同时支持 `aliyun-bailian`、`siliconflow`、`moonshot` 等多种推理服务提供商。模型特性（`features`）如 `function-calling`、`structured-outputs`、`web-search`、`cache`、`batch` 和 `fine-tuning` 可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口的 `features` 查询参数精确筛选。

> **注意**：文档 1 中 `inference_providers` 列表包含 `moonshot`（对应 Kimi），而文档 5 的授权接口错误码示例中提及 `"Model qwen-xxx is not authorized for Inference"`，但未说明该模型是否在当前业务空间已授权——实际权限状态必须通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口确认，不可仅依赖模型存在性判断可调用性。

模型授权分为三级权限：`inference`（必选）、`fine_tune` 和 `deploy`，默认仅开放部分模型的推理权限。未授权模型调用将直接返回 403 错误，而非限流或配额不足错误。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **筛选类** | `model`, `name`, `providers`, `capabilities`, `features`, `service_site`, `supports` | `model` 用于精确匹配模型 ID（如 `qwen3.8-max`）；`capabilities` 和 `features` 为数组，需重复传参（如 `capabilities=TG&capabilities=Reasoning`）；`service_site` 控制地域部署范围（如 `cn-hongkong`）；`supports=deploy` 表示支持部署的模型。 |
| **分页类** | `page_no`, `page_size` | 所有列表接口通用，`page_no` 从 1 开始，`page_size` 最大 200（[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 明确限定）。 |
| **限流类** | `request_limit`, `request_limit_period`, `usage_limit`, `usage_limit_period` | 单位：`request_limit_period=60` → QPM；`=1` → QPS；`usage_limit_period=60` → TPM。TPM 豁免需先 `DELETE` 再 `OVERLAY` 设置 QPM（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。 |
| **权限类** | `authorization_scope`, `action` | `authorization_scope=AUTHORIZED` 时返回已开通权限的模型；`action=INFERENCE` 是当前唯一有效值。 |

## 使用方式

### 1. 发现模型  
调用 `GET /api/v1/models` 获取模型元数据（名称、描述、上下文长度、定价、输入/输出模态等）。推荐使用 `model=qwen3.8-max` 精确查询单个模型，或 `providers=qwen&capabilities=TG` 组合筛选。

### 2. 查询权限  
调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认当前业务空间已开通推理权限的模型列表。未在此列表中的模型，即使存在于模型列表中，也无法调用。

### 3. 授权模型  
调用 `POST /api/v1/models/permissions` 开通权限：  
- **逐模型**：`{"models": [{"model": "qwen-plus", "inference": true}]}`  
- **一键授权**：`{"access_all_entities": "OPEN"}`（覆盖后续新增模型）

### 4. 配置限流  
调用 `POST /api/v1/models/limits` 设置账号级配额：  
- 设置 QPM=60 & TPM=100000：`{"models": [{"model": "qwen-plus", "request_limit": 60, "request_limit_period": 60, "usage_limit": 100000, "usage_limit_period": 60}]}`  
- 删除全部限流：`{"models": [{"model": "qwen-plus", "operation_type": "DELETE"}]}`

### 5. 查询当前限流  
调用 `GET /api/v1/models/limits?model=qwen3.8-max` 查看生效的 `model_limit`（账号级）与 `workspace_limit`（业务空间级）配额，其中 `workspace_limit` 为空表示未单独设置。

## 限制和注意事项

- **地域一致性**：所有模型管理接口（列表、限额、权限）必须使用**同一地域 Endpoint**（如北京 `cn-beijing.maas.aliyuncs.com`），跨地域调用将返回 404 或权限错误。
- **权限优先于限流**：模型未授权（`inference=false`）时，即使配额充足也无法调用；反之，已授权模型若超出 `model_limit`，则触发限流（HTTP 429）。
- **SDK 兼容性**：DashScope Python SDK 2.x 的 `client.models.list()` 返回对象中 `total_count` 字段对应响应 `output.total`，但 `providers` 参数仅在客户端过滤当前页，`total_count` 仍为未筛选总数（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。
- **PTU 部署限制**：`deployment_methods=ptu` 模型需额外指定 `deployment_ptu_service_tiers`，且仅适用于支持 PTU 的模型（如部分 `qwen-domain-model`）。
- **[异步任务](../concepts/asynchronous-task.md)限制**：`async_user_queue_limit` 和 `async_user_concurrency_limit` 仅对异步 API（如 `/v1/async/tasks`）生效，同步调用不适用。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


