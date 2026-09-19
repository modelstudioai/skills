# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控可用模型。通过统一的 RESTful API，开发者可动态查询模型元信息（如能力、上下文长度、定价）、获取当前配额、设置业务空间级限流策略，并精细化控制模型调用权限（推理/微调/部署）。所有操作均基于 API Key 认证，适用于多地域、多供应商、[多模态](../concepts/multimodal.md)场景。

## 支持的模型与功能

百炼平台支持来自阿里巴巴（千问、万相、HappyHorse 等）、智谱AI、MiniMax、月之暗面、DeepSeek、小米等多家供应商的模型，覆盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成、实时全模态等能力。模型能力可通过 `capabilities` 参数筛选，例如 `capabilities=TG&capabilities=Reasoning`；支持的功能（如 function calling、structured-outputs、web-search）则通过 `features` 参数过滤。详细模型列表及能力映射请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

模型授权状态分为“可授权”与“已授权”两类：`AUTHORIZABLE` 表示当前业务空间具备授权资格但尚未启用；`AUTHORIZED` 表示已开通对应权限。权限粒度包括 `inference`（必选）、`fine_tune` 和 `deploy`，其中 `fine_tune` 和 `deploy` 需单独申请并显式授权。具体权限状态需调用 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口确认。

> **注意**：文档 5 中 `models[].finetune` 字段名与文档 4 返回字段 `fine_tune` 不一致（前者为 `finetune`，后者为 `fine_tune`），实际请求 Body 应使用 `finetune`，响应体中为 `fine_tune`，属命名不统一，以接口实际字段为准。

## 关键参数

| 参数类别 | 示例字段 | 说明 |
|----------|----------|------|
| **筛选类** | `providers=qwen`, `capabilities=TG`, `features=function-calling` | 用于 `list-models` 和 `list-quotas`，支持多值（重复参数名）；`providers` 指模型作者，`inference_providers` 指推理服务方（如 `aliyun-bailian`） |
| **分页类** | `page_no=1`, `page_size=20` | 所有列表接口通用，`page_size` 最大值为 200（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)） |
| **限流类** | `request_limit=60`, `request_limit_period=60`, `usage_limit=100000`, `usage_limit_period=60` | 单位：次/分钟（QPM）、[Token](../concepts/token.md)/分钟（TPM）；`request_limit_period=1` 表示 QPS，`60` 表示 RPM |
| **授权类** | `inference=true`, `finetune=false`, `deploy=false`, `access_all_entities=OPEN` | `access_all_entities=OPEN` 可一键授权全部推理模型（含未来新增），无需逐个指定 `models` |

## 使用方式

- **发现模型**：调用 `GET /api/v1/models` 查询模型列表，推荐使用 HTTP API（而非 SDK）以支持完整筛选条件（如 `capabilities`、`features`）；Python SDK 的 `Models.list()` 仅支持分页参数，详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **查看配额**：调用 `GET /api/v1/models/limits` 获取当前 API Key 下各模型的请求频率（QPM/QPS）与用量（TPM）限制，返回中 `model_limit` 为账号级上限，`workspace_limit` 为业务空间级配置（若为 `null` 则未设置）。
- **设置限流**：调用 `POST /api/v1/models/limits` 更新限流，支持 `OVERLAY`（合并覆盖）与 `DELETE`（清空）两种操作类型；若需“仅限 QPM、不限 TPM”，须先 `DELETE` 再 `OVERLAY` 设置 QPM（存在短暂无限制窗口）。
- **管理权限**：调用 `GET /api/v1/models/permissions` 查看已授权模型及其 `inference`/`fine_tune`/`deploy` 状态；调用 `POST /api/v1/models/permissions` 进行逐模型授权或 `access_all_entities=OPEN` 一键授权。

## 限制和注意事项

- 所有 API 均需在 Header 中携带 `Authorization: Bearer {API_KEY}`，且 `DASHSCOPE_API_KEY` 必须已配置为环境变量。
- `list-models` 接口的 `context_window` 参数含义为“返回上下文长度**严格小于**该值的模型”，非“大于等于”或“等于”。
- `list-quotas` 和 `update-model-rate-limits` 接口的 `usage_limit_field` 当前仅支持 `total_tokens`，其他值将被忽略。
- 业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），否则更新失败。
- `update-model-permissions` 接口对 `finetune` 字段的拼写为 `finetune`（无下划线），而响应中为 `fine_tune`，调用时务必使用 `finetune`。
- 模型 ID（如 `qwen3-max`）是调用推理 API 的必需参数，必须与 `list-models` 返回的 `model` 字段完全一致，大小写敏感。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


