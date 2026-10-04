# model management

模型管理是百炼平台为开发者提供的核心能力，用于查询、授权和限流控制可用模型。通过统一的 REST API，开发者可动态获取模型元信息、配置调用权限、设置 QPM/TPM 限流策略，并支持按业务空间粒度精细化管控。所有操作均需使用有效的 API Key 进行身份认证。

## 支持的模型与功能

百炼平台支持多模态、多供应商的模型生态，涵盖文本生成（`TG`）、视觉理解（`VU`）、图片生成（`IG`）、视频生成（`VG`）、语音识别（`ASR`）等能力类型。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`wan`（万相）、`kling`（可灵AI）、`vidu`、`pixverse` 等 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口提供完整模型目录，支持按 `providers`、`capabilities`、`features`（如 `function-calling`、`structured-outputs`）等维度筛选，并返回上下文长度、定价、输入/输出模态等关键元数据。

模型权限分为三类：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。默认仅开放推理权限，微调与部署需显式授权。[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口可区分 `AUTHORIZABLE`（可授权模型）与 `AUTHORIZED`（已授权模型），并返回各模型当前权限状态。

> **注意**：文档 5 中 `models[].finetune` 参数名与文档 4 返回字段 `fine_tune` 不一致（前者为 `finetune`，后者为 `fine_tune`），实际请求 Body 应使用 `finetune`（见文档 5 示例），响应体中为 `fine_tune`；SDK 或封装层需做兼容处理。

## 关键参数

| 功能 | 关键参数 | 说明 |
|------|----------|------|
| **模型发现** | `capabilities`, `providers`, `features`, `context_window` | 用于精准筛选模型，例如 `capabilities=TG&providers=qwen` 获取千问文本生成模型；`features=function-calling` 筛选支持[函数调用](../concepts/function-calling.md)的模型 |
| **权限控制** | `models[].inference` / `finetune` / `deploy`, `access_all_entities` | `access_all_entities=OPEN` 启用一键授权全部推理模型；逐模型授权时 `null` 表示保持现状 |
| **限流配置** | `request_limit` / `request_limit_period`, `usage_limit` / `usage_limit_period` | `request_limit_period=60` 表示 QPM（次/分钟），`=1` 表示 QPS（次/秒）；`usage_limit_field` 固定为 `total_tokens`，单位为 [Token](../concepts/token.md) 数 |

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，推荐使用分页（`page_no`/`page_size`）遍历全量模型；Python SDK 的 `Models.list()` 仅支持分页，复杂筛选请直接调用 HTTP API [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **管理模型权限**：先调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZABLE` 获取可授权模型列表，再通过 `POST /api/v1/models/permissions` 设置 `inference`/`finetune`/`deploy` 布尔值；启用一键授权时传 `"access_all_entities": "OPEN"` 即可。
- **配置模型限流**：调用 `GET /api/v1/models/limits` 查看当前配额，再通过 `POST /api/v1/models/limits` 更新。若需“仅限 RPM、不限 TPM”，必须分两步：先 `DELETE` 全部限流，再 `OVERLAY` 仅设 `request_limit` 和 `request_limit_period` —— 此为 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 明确要求的豁免方案。

## 限制和注意事项

- 所有 API 均需在 Header 中携带 `Authorization: Bearer {API_KEY}`，且 `DASHSCOPE_API_KEY` 必须已配置为环境变量或显式传入。
- 限流更新接口（`/models/limits`）对 `models` 数组长度限制为 1~200；权限更新接口（`/models/permissions`）对 `models` 长度限制为 1~20（逐模型模式）。
- 业务空间级别限流（`workspace_limit`）不能超过账号级别限流（`model_limit`），否则更新失败；删除限流时需确保 `operation_type=DELETE` 且所有限流字段为空。
- 模型授权与限流均为**业务空间（Workspace）级别**配置，不同 Workspace 间相互隔离；Workspace ID 需在请求 URL 中显式替换（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。
- > **注意**：文档 2 的请求示例中 Endpoint 使用了 `https://dashscope.aliyuncs.com/...`，而文档 1、3、4、5 均明确要求使用带 `{WorkspaceId}` 的地域化 Endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`）。生产环境**必须使用 Workspace ID 绑定的 Endpoint**，否则将返回鉴权失败或资源不存在错误。

## 来源文档

- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


