# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、用量配额与限流配置等全生命周期管理功能。开发者可通过统一 API 接口查询可用模型列表、查看/更新模型授权状态、获取/调整模型调用限额，从而实现精细化的模型资源治理与业务适配。

## 支持的模型与功能

百炼平台支持多供应商、多模态、多能力的模型体系，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力类型。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，并支持按 `capabilities`、`providers`、`features`（如 `function-calling`、`structured-outputs`、`web-search`）等维度精准筛选。详细模型能力与供应商映射关系请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 5 中 `update-model-permissions.md` 的 `models[].finetune` 字段名与文档 4 中 `list-model-permissions.md` 返回字段 `fine_tune` 不一致（前者为 `finetune`，后者为 `fine_tune`），实际请求 Body 应使用 `finetune`（驼峰无下划线），返回字段为 `fine_tune`（带下划线）。该命名差异已在 SDK 与服务端兼容处理，但手动构造请求时需注意。

模型授权支持三种粒度：`inference`（推理调用）、`fine_tune`（微调训练）、`deploy`（私有化部署）。其中 `inference` 权限为默认启用前提，未授权则无法调用；`fine_tune` 与 `deploy` 需显式开通。授权状态可通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口实时获取。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **模型标识** | `model`（ID）、`name`（模糊匹配） | `model` 用于精确查询与调用（如 `qwen3.8-max`），`name` 仅用于列表检索 |
| **能力筛选** | `capabilities`、`features`、`providers` | 多值筛选需重复传参（如 `capabilities=TG&capabilities=Reasoning`）；`features` 包含 `function-calling` 等关键能力标识 |
| **配额控制** | `request_limit` / `request_limit_period`（QPM/QPS）、`usage_limit` / `usage_limit_period`（TPM/TPS） | `request_limit_period=60` 表示每分钟限制，`=1` 表示每秒限制；[查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 返回当前生效值 |
| **授权操作** | `inference` / `finetune` / `deploy`（布尔值）、`access_all_entities`（`OPEN`/`CLOSE`/`KEEP`） | `access_all_entities=OPEN` 可一键授权当前空间全部推理模型（含未来新增） |

## 使用方式

- **发现模型**：调用 `GET /api/v1/models` 查询模型列表，推荐优先使用 `capabilities` + `providers` 组合筛选（如 `capabilities=TG&providers=qwen`），避免全量拉取。Python SDK 的 `Models.list()` 仅支持分页，复杂筛选需直接调用 HTTP API。
- **管控权限**：通过 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 查看已授权模型；使用 `POST /api/v1/models/permissions` 更新权限——单模型授权填 `models` 数组，全空间授权设 `access_all_entities=OPEN`。
- **配置限流**：先调用 `GET /api/v1/models/limits` 获取当前限额，再用 `POST /api/v1/models/limits` 更新。若需“仅限 QPM、不限 TPM”，必须分两步：先 `DELETE` 全部限流，再 `OVERLAY` 仅设 `request_limit`（详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。
- **鉴权与地域**：所有接口均需在 Header 中携带 `Authorization: Bearer {API_KEY}`；Endpoint 地域需与业务空间所在 Region 严格匹配（如北京空间必须使用 `cn-beijing.maas.aliyuncs.com` 域名），不可混用国际站域名。

## 限制和注意事项

- 模型列表接口 `page_size` 最大为 100，`list-quotas.md` 和 `list-model-permissions.md` 中 `page_size` 最大为 200，超出将被截断。
- 限流更新接口 `POST /api/v1/models/limits` 要求 `models` 数组长度为 1~200，且 `operation_type=DELETE` 时所有限流字段（`request_limit`、`usage_limit` 等）必须为空。
- 授权更新接口中，`access_all_entities=OPEN` 会覆盖历史逐模型授权，且自动包含后续上架的推理模型；`CLOSE` 将清空所有推理授权，需谨慎操作。
- 所有模型 ID（`model` 字段）区分大小写且严格匹配，例如 `qwen3.8-max` 与 `Qwen3.8-Max` 视为不同模型。
- 模型上下文长度（`context_window`）与 Token 限制（`max_input_tokens`/`max_output_tokens`）以 `model_info` 字段返回，部分图像/视频模型该值为 `null`，表示不适用 Token 计量。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


