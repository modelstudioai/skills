# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控可用模型。通过统一的 REST API 接口，开发者可程序化地查询模型元信息（如能力、上下文长度、定价）、获取当前配额、配置模型访问权限及调整调用限流策略。所有操作均基于业务空间（Workspace）粒度，需使用有效的 API Key 进行认证。

## 支持的模型/功能

百炼平台支持多模态、多供应商的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商；推理服务由 `aliyun-bailian`（百炼）、`siliconflow`（硅基流动）、`mini-max` 等提供。完整支持的能力列表详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中 `capabilities` 和 `features` 参数说明。

模型授权维度包括 `inference`（推理调用）、`fine_tune`（微调）和 `deploy`（部署），不同模型默认开通权限不同，例如 `qwen3-max` 默认支持 `inference` 和 `fine_tune`，而 `qwen-turbo` 仅支持 `inference`（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回示例）。授权状态直接影响是否能发起 API 请求。

> **注意**：文档 5 中 `update-model-permissions.md` 的请求参数字段名为 `finetune`（无下划线），但文档 3 中 `list-model-permissions.md` 的返回字段为 `fine_tune`（带下划线）。实际接口以返回字段 `fine_tune` 为准，SDK 或客户端应兼容两种命名风格或严格按响应字段解析。

## 关键参数

| 类别 | 参数名 | 类型 | 说明 |
|--------|---------|------|------|
| **通用筛选** | `model` / `name` | `String` | `model` 用于精确匹配模型 ID（如 `qwen3-max`）；`name` 用于模糊搜索模型名称（如 `qwen`） |
| **能力过滤** | `capabilities`, `features`, `providers` | `Array[String]` | 多值筛选，需重复传参（如 `capabilities=TG&capabilities=Reasoning`）；`features` 包含 `function-calling`、`structured-outputs` 等关键能力标识 |
| **限流控制** | `request_limit`, `request_limit_period`, `usage_limit`, `usage_limit_period` | `Number` | `request_limit_period=60` 表示 QPM（每分钟请求数），`=1` 表示 QPS（每秒请求数）；`usage_limit_field` 固定为 `total_tokens`（见 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)） |
| **权限控制** | `inference`, `fine_tune`, `deploy` | `Boolean` | 更新授权时设为 `true`/`false` 表示授/取消权；`null` 表示保持现状 |

## 使用方式

- **发现模型**：调用 `GET /api/v1/models` 查询可用模型列表，支持按 `capabilities`、`providers`、`context_window` 等条件组合筛选。Python SDK 的 `Models.list()` 仅支持分页参数，复杂筛选需直接调用 HTTP API（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。
- **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取当前业务空间已授权的模型及其 `inference`/`fine_tune`/`deploy` 状态。
- **配置权限**：调用 `POST /api/v1/models/permissions` 授权单个或多个模型，或使用 `access_all_entities=OPEN` 一键授权全部推理模型。
- **管理限流**：先调用 `GET /api/v1/models/limits` 查看当前配额，再通过 `POST /api/v1/models/limits` 设置或删除 `request_limit`（QPM/QPS）和 `usage_limit`（TPM）。若需“仅限 QPM、不限 TPM”，必须分两步：先 `DELETE` 再 `OVERLAY`（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。

## 限制和注意事项

- 所有模型管理 API 均需在请求 Header 中携带 `Authorization: Bearer {API_KEY}`，且 `DASHSCOPE_API_KEY` 必须具有对应业务空间的管理员或模型管理权限。
- 分页参数 `page_no` 从 1 开始，`page_size` 最大为 200（[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 明确限定）；`list-models.md` 未声明上限，但建议不超过 100 以保障响应性能。
- 模型限流设置存在依赖约束：若模型当前无 QPM 限制，直接设置 TPM 会失败（错误码 `InvalidParameter`），必须先设置 QPM（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 错误示例）。
- `deployment_methods=ptu` 和 `deployment_ptu_service_tiers` 等部署相关参数仅对支持 PTU 的模型生效，普通推理调用无需关注；其行为与 `supports=deploy` 的模型授权无关。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


