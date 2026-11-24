# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与配额监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息（如能力、模态、上下文长度、定价）、设置业务空间级访问权限、配置请求/用量限流，并实时查看当前配额使用情况。所有操作均基于业务空间（Workspace）隔离，需通过 API Key 认证。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）、结构化输出（`structured-outputs`）、function calling 等能力。模型来源包括 `qwen`（阿里巴巴-千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，部署模式覆盖 `global`、`asia-pacific-china`、`european-union`、`united-states` 等地域。完整模型列表及筛选能力详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

模型权限分为三类：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。并非所有模型默认开放全部权限；例如，多数第三方模型仅授权推理，而部分领域模型（如 `qwen-domain-model`）可能限制微调入口。具体可授权模型范围及当前状态需通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口确认。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `model` | 模型唯一 ID，用于 API 调用和限流/权限配置 | `"qwen3.8-max"` | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `providers` / `inference_providers` | 分别标识模型作者与推理服务方，影响计费归属与 SLA | `["qwen"]`, `["aliyun-bailian"]` | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `capabilities` | 模型核心能力标签，用于能力导向筛选 | `["Reasoning", "VU"]` | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `request_limit` & `request_limit_period` | QPS/RPM 限流阈值（秒/分钟粒度） | `60`, `60`（即 60 RPM） | [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) |
| `usage_limit` & `usage_limit_period` | TPM 用量限流（如 `total_tokens`） | `100000`, `60`（即 100K TPM） | [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) |
| `authorization_scope` | 控制 `list-model-permissions` 返回范围：`AUTHORIZABLE`（可授）或 `AUTHORIZED`（已授） | `"AUTHORIZED"` | [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) |

> **注意**：文档 3 中 `update-model-rate-limits` 的示例请求地址为 `https://dashscope.aliyuncs.com/api/v1/models/limits`，但文档 2 和文档 3 均明确要求将 `{WorkspaceId}` 替换为实际业务空间 ID，且文档 2 的 endpoint 明确包含 WorkspaceId（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits`）。因此，**生产环境必须使用带 WorkspaceId 的域名，不可直接使用 `dashscope.aliyuncs.com`**，否则将返回鉴权失败。

## 使用方式

### 1. 发现模型
使用 `GET /api/v1/models` 查询模型列表，支持按 `name`（模糊）、`model`（精确）、`providers`（作者）、`capabilities`（能力）、`context_window`（上下文长度）等多维筛选。推荐首次调用时省略参数获取全量概览，再结合业务需求细化过滤。

### 2. 管理权限
- 查询当前空间已授权模型：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`  
- 授权单个模型：`POST /api/v1/models/permissions` + `{"models": [{"model": "qwen-plus", "inference": true}]}`  
- 一键授权全部推理模型：`POST /api/v1/models/permissions` + `{"access_all_entities": "OPEN"}`  
详情见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。

### 3. 配置限流
- 查询当前限流：`GET /api/v1/models/limits?model=qwen3.8-max`  
- 设置 QPM+TPM：`POST /api/v1/models/limits` + `{"models": [{"model": "qwen3.8-max", "request_limit": 100, "request_limit_period": 60, "usage_limit": 500000, "usage_limit_period": 60}]}`  
- 删除限流（恢复默认）：`POST /api/v1/models/limits` + `{"models": [{"model": "qwen3.8-max", "operation_type": "DELETE"}]}`  

### 4. 监控配额
调用 `GET /api/v1/models/limits` 可实时获取 `model_limit`（账号级上限）与 `workspace_limit`（业务空间级设置），其中 `async_user_queue_limit` 和 `async_user_concurrency_limit` 专用于异步任务场景。

## 限制和注意事项

- **分页强制约束**：所有 `list-*` 接口（模型、限额、权限）均强制分页，`page_size` 最大为 200，`page_no` 从 1 开始；未传 `page_no` 默认为 1，但 `total` 字段返回的是**筛选后总数**，需据此判断是否需翻页。
- **权限与限流解耦**：模型授权（`permissions`）控制“能否调用”，限流（`limits`）控制“调用频次/用量”，二者独立配置。即使模型已授权，若超出限流仍会返回 `429 Too Many Requests`。
- **PTU 部署特殊性**：`deployment_methods=ptu` 的模型不参与常规限流，其吞吐由预置 PTU 单位保障，相关配置需在控制台完成，API 不暴露 PTU 管理接口。
- **SDK 兼容性提示**：DashScope Python SDK 2.x 的 `client.models.list()` 返回对象中，总数量字段名为 `total_count`（非响应体中的 `output.total`），且 `providers` 参数仅在客户端过滤当前页，`total_count` 仍为原始总数 —— 此行为与 HTTP API 语义不一致，[查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 文档已明确警示。
- **地域一致性要求**：查询模型、查询限额、更新权限等操作，Endpoint 的地域（如 `cn-beijing`）必须与业务空间所在地域严格一致，跨地域调用将失败。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


