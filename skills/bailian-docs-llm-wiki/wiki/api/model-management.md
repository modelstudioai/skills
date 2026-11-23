# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与配额监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息（如能力、模态、上下文长度、定价）、设置业务空间级访问权限、配置请求/用量限流，并实时查看当前配额使用情况。所有操作均基于业务空间（Workspace）隔离，需通过 API Key 认证。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）、结构化输出（`structured-outputs`）、function calling 等能力。模型作者包括 `qwen`、`zhipu-ai`、`moonshot-ai`、`deepseek`、`kling`、`vidu` 等十余家供应商；推理服务由 `aliyun-bailian`、`siliconflow`、`moonshot` 等提供。完整可选值详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中的 `providers`、`inference_providers`、`capabilities` 和 `features` 参数说明。

> **注意**：文档 1 中列出的 `inference_providers` 包含 `moonshot`（对应 Kimi），而文档 5 的授权接口返回示例中 `permissions` 字段仅包含 `inference`/`fine_tune`/`deploy` 三类布尔权限，未体现推理服务供应商绑定关系——实际授权粒度为模型 ID 级，不区分底层推理 provider，此为设计一致，非矛盾。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **模型标识** | `model`（ID）、`name`（名称） | `model` 用于精确查询与调用（如 `qwen3.8-max`）；`name` 仅用于模糊搜索。 |
| **筛选维度** | `providers`, `capabilities`, `features`, `service_site`, `supports` | 支持按作者、能力（如 `["Reasoning", "VU"]`）、特性（如 `["function-calling"]`）、部署地域（如 `cn-hongkong`）、用途（`inference` 或 `deploy`）组合过滤。 |
| **权限控制** | `inference`, `finetune`, `deploy` | 布尔值，分别控制模型调用、微调、部署权限，见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。 |
| **限流配置** | `request_limit` / `request_limit_period`, `usage_limit` / `usage_limit_period` | 分别表示 QPM/RPM（如 `60` 次/分钟）和 TPM（如 `100000` tokens/分钟），周期单位为秒（`60`=1分钟）。 |

## 使用方式

### 1. 查询模型列表  
调用 `GET /api/v1/models`，支持分页（`page_no`/`page_size`）与多维筛选。推荐优先用 `model` 精确查询单个模型详情，或用 `providers=qwen&capabilities=TG` 获取千问文本生成模型全集。[查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 提供了各地域 Endpoint 及 Python SDK 示例。

### 2. 查询/更新模型授权  
- **查询**：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取当前已开通推理权限的模型列表；  
- **更新**：`POST /api/v1/models/permissions` 支持逐模型授权（如 `{"model":"qwen-plus","inference":true}`）或一键授权（`access_all_entities=OPEN`）。详细字段与约束见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。

### 3. 查询/更新模型限流  
- **查询**：`GET /api/v1/models/limits?model=qwen3.8-max` 返回账号级（`model_limit`）与业务空间级（`workspace_limit`）配额；  
- **更新**：`POST /api/v1/models/limits` 通过 `operation_type=OVERLAY` 覆盖或 `DELETE` 清除限流。注意：TPM 设置需先存在 QPM 配置，否则报错（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 错误码说明）。

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且未显式设置时默认继承账号级配额。
- **限流生效延迟**：限流策略变更后通常在 10 秒内生效，但高并发场景下可能存在短暂窗口期。
- **权限与限流解耦**：模型授权（`permissions`）控制“能否调用”，限流（`limits`）控制“调用频次/用量”，二者独立配置，需同步管理。
- **地域一致性**：所有管理 API（列表、权限、限流）必须使用与业务空间所在地域匹配的 Endpoint（如北京空间需调用 `cn-beijing.maas.aliyuncs.com`），跨地域调用将返回 403。
- **模型状态**：部分模型可能返回 `inference_offline_info` 字段，标明预计下线时间，调用前应检查该字段避免生产中断。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


