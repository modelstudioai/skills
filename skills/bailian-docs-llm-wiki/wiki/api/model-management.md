# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控模型使用。通过统一的 REST API，开发者可程序化地查询可用模型列表、检查当前业务空间的模型权限与配额、动态调整限流策略，并批量管理模型调用权限。所有操作均基于 API Key 认证，适用于生产环境自动化运维。

## 支持的模型与功能

百炼平台支持多模态、多供应商的模型生态，包括通义千问（Qwen）、万相（Wan）、智谱AI、MiniMax、Kling、Vidu 等主流模型。可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口按 `providers`（如 `qwen`）、`capabilities`（如 `TG` 文本生成、`VG` 视频生成）、`features`（如 `function-calling`、`structured-outputs`）等维度筛选模型，并获取其上下文长度（`context_window`）、输入/输出模态（`request_modality`/`response_modality`）、定价（`prices`）及发布时间等元信息。同时，[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口可区分“可授权模型”与“已授权模型”，返回每个模型在当前业务空间下的 `inference`、`fine_tune`、`deploy` 三类权限状态。

> **注意**：Python SDK 的 `client.models.list()` 方法仅支持 `page_no`、`page_size` 和 `provider` 参数，不支持 `capabilities`、`features` 等高级筛选条件；如需精确过滤，必须直接调用 HTTP API —— 详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 关键参数

模型管理相关接口共用以下关键参数模式：

- **通用分页**：`page_no`（从 1 开始）、`page_size`（默认 20，最大 200），用于遍历结果集。
- **模型标识**：`model`（String，精确匹配模型 ID，如 `qwen3.8-max`）与 `name`（String，模糊搜索模型名称）。
- **限流控制**（见 `/models/limits`）：
  - `request_limit` + `request_limit_period`：请求频率限制（如 `60` 次/60 秒 = QPM）；
  - `usage_limit` + `usage_limit_period`：用量限制（如 `100000` tokens/60 秒 = TPM）；
  - `async_user_queue_limit` / `async_user_concurrency_limit`：异步任务专属限制（仅部分模型支持）。
- **权限控制**（见 `/models/permissions`）：
  - `authorization_scope`：`AUTHORIZABLE`（默认）或 `AUTHORIZED`；
  - `access_all_entities`：`OPEN`（一键授权全部推理模型）、`CLOSE`（清空）、`KEEP`（默认，维持逐模型配置）。

## 使用方式

1. **发现模型**：调用 `GET /api/v1/models`，按需传入 `capabilities=TG&providers=qwen` 等参数获取目标模型列表及元数据。
2. **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认当前业务空间已启用哪些模型的推理权限。
3. **设置限流**：调用 `POST /api/v1/models/limits`，以 `OVERLAY` 模式更新单个或多个模型的 `request_limit` 和 `usage_limit`；若需豁免 TPM 仅限 RPM，须先 `DELETE` 再 `OVERLAY` 设置（两步非原子）—— 具体流程参见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
4. **授权模型**：调用 `POST /api/v1/models/permissions`，可选择逐模型设置（如 `{"model":"qwen-plus","inference":true}`）或启用 `access_all_entities=OPEN` 一键授权全部推理模型。

所有接口均需在 Header 中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，Endpoint 需替换 `{WorkspaceId}` 并匹配地域（如华北2北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。

## 限制和注意事项

- 单次限流更新最多支持 200 个模型（`models` 数组长度 ≤ 200），单次权限更新最多支持 20 个模型（`models` 数组长度 ≤ 20）。
- 业务空间级别限流（`workspace_limit`）不能超过账号级别限流（`model_limit`）；若尝试设置超出上限的 `workspace_limit`，请求将失败。
- `update-model-rate-limits` 接口对 `operation_type=DELETE` 的请求要求 `models[].request_limit` 和 `models[].usage_limit` 均为空；若仅传一个字段为空，会返回 `InvalidParameter` 错误。
- `update-model-permissions` 接口在 `access_all_entities=OPEN` 时，`models` 字段可省略；但若同时传入 `models` 和 `OPEN`，行为未明确定义，建议避免混用。
- 所有模型管理接口均依赖业务空间（Workspace）上下文，未指定或错误 WorkspaceId 将导致 403 或 404 错误。WorkspaceId 必须与 API Key 所属主账号及地域一致。

## 来源文档

- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


