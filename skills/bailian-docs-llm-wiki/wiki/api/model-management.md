# model management

模型管理是百炼平台为开发者提供的核心能力，用于查询、授权、限流等全生命周期操作。通过统一的 RESTful API 接口，开发者可动态获取可用模型列表、配置模型调用权限、设置 QPM/TPM 限流策略，并实时查询配额状态。所有操作均基于业务空间（Workspace）粒度，支持多模型批量处理。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）、3D 生成（`3D-generation`）等 [capabilities](../../raw/model-api-reference/model-management/list-models.md)。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，同时支持推理服务分离部署（如 `aliyun-bailian`、`siliconflow`、`moonshot` 等 [inference_providers](../../raw/model-api-reference/model-management/list-models.md)）。模型能力维度还包括 `function-calling`、`structured-outputs`、`web-search`、`fine-tuning` 等 [features](../../raw/model-api-reference/model-management/list-models.md)，可在查询时按需筛选。

> **注意**：文档 1 中列出的 `providers` 和 `inference_providers` 值存在部分重叠（如 `moonshot-ai` 与 `moonshot`），实际调用时应以 `providers` 表示模型作者、`inference_providers` 表示推理服务方为准；二者语义不同，不可混用。

## 关键参数

| 参数类别 | 示例字段 | 说明 |
|----------|----------|------|
| **模型标识** | `model`, `name` | `model`（如 `qwen3-max`）为精确 ID，用于 API 调用；`name` 为模糊搜索名称 |
| **能力筛选** | `capabilities`, `features`, `providers` | 多值筛选需重复传参（如 `capabilities=TG&capabilities=Reasoning`）；`features` 中 `fine-tuning` 对应微调权限，非所有模型默认开放 |
| **限流控制** | `request_limit`, `usage_limit`, `request_limit_period`, `usage_limit_period` | 单位：`request_limit_period=60` → RPM，`=1` → QPS；`usage_limit` 单位为 [Token](../concepts/token.md)，默认按 `total_tokens` 计量 |
| **授权控制** | `inference`, `finetune`, `deploy` | 布尔值，`null` 表示保持现状；`access_all_entities=OPEN` 可一键授权全部推理模型，覆盖逐模型设置 |

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，支持分页（`page_no`/`page_size`）及多维筛选（`capabilities`、`providers` 等）。Python SDK 的 `Models.list()` 仅支持分页，**复杂筛选必须使用 HTTP API** [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **查询/更新授权**：`GET /api/v1/models/permissions` 返回 `inference`/`finetune`/`deploy` 权限布尔值；`POST /api/v1/models/permissions` 支持逐模型设置或 `access_all_entities=OPEN` 一键授权 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。
- **查询/更新限流**：`GET /api/v1/models/limits` 返回 `model_limit`（账号级）与 `workspace_limit`（业务空间级）；`POST /api/v1/models/limits` 使用 `operation_type=OVERLAY` 合并更新或 `DELETE` 清除限流 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **权限与限流联动**：仅已授权模型（`inference=true`）才可被设置限流；若对未授权模型调用限流接口，将返回 `InvalidParameter` 错误。

## 限制和注意事项

- **QPM/TPM 强约束**：设置 `usage_limit`（TPM）前必须已存在 `request_limit`（QPM），否则报错 `"Cannot set TPM without QPM"`；如需仅限 QPM，须先 `DELETE` 再 `OVERLAY` 设置 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **授权范围隔离**：`authorization_scope=AUTHORIZED` 仅返回当前业务空间已显式授权的模型；`AUTHORIZABLE` 返回平台所有可授权模型（含未开通权限者），但调用前仍需确认是否在 `providers` 白名单内。
- **Endpoint 地域差异**：国际站（`dashscope-intl.aliyuncs.com`）与国内站（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）Endpoint 不同，且国际站不支持 Workspace ID 路径变量；调用前务必核对地域文档 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **模型上下文长度**：`model_info.context_window` 为总窗口长度，但实际可用输入受 `max_input_tokens` 限制，输出受 `max_output_tokens` 限制；部分图像/视频模型该字段为 `null`，需以 `inference_metadata` 中的模态信息为准。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


