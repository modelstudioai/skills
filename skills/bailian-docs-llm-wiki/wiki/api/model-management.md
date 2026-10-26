# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、用量配额配置等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、查看/更新授权状态、设置限流策略，从而实现精细化的模型资源治理。所有操作均基于业务空间（Workspace）维度进行隔离与管控。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型接入，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，推理服务亦可由 `aliyun-bailian`、`siliconflow`、`moonshot` 等多家服务商提供。完整能力列表及筛选方式详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 4 中 `update-model-permissions.md` 的请求参数示例使用了字段名 `fine_tune`，但实际返回结构（文档 5）和接口定义中统一为 `finetune`（无下划线）。请以 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回的 `output.permissions[].permissions.finetune` 字段为准，避免因字段名不一致导致解析失败。

## 关键参数

模型管理相关接口共用以下核心参数：

- **`model`（String）**：模型唯一 ID（如 `qwen3.8-max`），用于精确查询或操作目标模型；
- **`page_no` / `page_size`（Integer）**：分页参数，适用于列表类接口（`list-models`、`list-quotas`、`list-model-permissions`），默认 `page_no=1`、`page_size=20`；
- **`authorization_scope`（String）**：仅用于权限查询，取值 `AUTHORIZABLE`（可授权模型，默认）或 `AUTHORIZED`（已授权模型）；
- **`operation_type`（String）**：仅用于限流更新，取值 `OVERLAY`（合并覆盖，默认）或 `DELETE`（删除限流）；
- **`access_all_entities`（String）**：仅用于权限更新，取值 `OPEN`（一键授权全部推理模型）、`CLOSE`（清空一键授权）或 `KEEP`（保持逐模型配置，默认）。

## 使用方式

| 功能 | 接口路径 | 方法 | 说明 |
|------|----------|------|------|
| 查询可用模型 | `/api/v1/models` | GET | 支持按 `capabilities`、`providers`、`features` 等多维条件筛选，返回模型 ID、上下文长度、定价等元信息；Python SDK 仅支持分页，[高级筛选需调用 HTTP API](../../raw/model-api-reference/model-management/list-models.md) |
| 查询模型限额 | `/api/v1/models/limits` | GET | 获取当前 API Key 下各模型的 QPS/RPM、TPM/TPM 及[异步任务](../concepts/asynchronous-task.md)并发限制；返回中 `request_limit_period=1` 表示 QPS，`=60` 表示 RPM |
| 更新模型限额 | `/api/v1/models/limits` | POST | 支持批量设置 `request_limit`（QPM）、`usage_limit`（TPM）；若需“仅限 QPM、豁免 TPM”，须先 `DELETE` 再 `OVERLAY` 设置（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)） |
| 查询模型授权 | `/api/v1/models/permissions` | GET | 按 `authorization_scope` 区分可授权/已授权模型，返回 `inference`/`finetune`/`deploy` 三类布尔权限状态 |
| 更新模型授权 | `/api/v1/models/permissions` | POST | 支持逐模型设置权限（`models` 数组）或一键授权（`access_all_entities=OPEN`）；注意 `finetune` 字段名无下划线 |

## 限制和注意事项

- 所有接口均需在 Header 中携带 `Authorization: Bearer {API_KEY}`，且 API Key 必须具备对应业务空间的操作权限；
- 模型列表接口（`/models`）的 `capabilities`、`features` 等筛选参数**不被 Python SDK `Models.list()` 支持**，必须使用原生 HTTP 调用；
- 限流更新接口（`/models/limits`）要求 `usage_limit` 和 `request_limit` 不可单独设置：若未设置 `request_limit`，则不能设置 `usage_limit`（否则报错 `Cannot set TPM without QPM`）；
- 一键授权（`access_all_entities=OPEN`）仅覆盖**推理权限**（`inference=true`），不影响微调与部署权限，后者仍需逐模型显式配置；
- 模型授权状态变更后，通常在 1 分钟内生效；限流配置变更生效时间约为 30 秒；
- 部分图像/视频生成模型（如 `qwen-image-3.0-pro`）的 `model_info.context_window` 为 `null`，因其不适用 [Token](../concepts/token.md) 上下文概念，应以 `prices` 中的 `image_number` 等计费单元为准。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)


