# model management

模型管理是百炼平台为开发者提供的核心能力，用于查询、授权和限流控制可用模型。通过统一的 REST API，开发者可动态获取模型元信息、配置调用权限、设置 QPM/TPM 配额，并支持按业务空间粒度精细化管控。所有操作均需使用有效的 API Key 进行认证。

## 支持的模型与功能

百炼平台支持多模态、多供应商的模型生态，涵盖文本生成（`TG`）、视觉理解（`VU`）、图像生成（`IG`）、视频生成（`VG`）、语音识别（`ASR`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`wan`（万相）、`kling`（可灵AI）、`vidu`（Vidu）等 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口支持按 `providers`、`capabilities`、`features` 等多维条件筛选，并返回上下文长度、定价、输入/输出模态等关键元数据。同时，[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口可区分“可授权”与“已授权”模型，明确各模型在当前业务空间下的 `inference`、`fine_tune`、`deploy` 三级权限状态。

## 关键参数

模型管理涉及两类核心参数体系：

- **模型标识参数**：`model`（模型 ID，精确匹配，如 `qwen3-max`）和 `name`（名称模糊搜索，如 `qwen`），在 `GET /models`、`GET /models/permissions`、`GET /models/limits` 中均作为可选 Query 参数；  
- **限流与权限参数**：  
  - 限流中 `request_limit`（QPM/QPS）、`request_limit_period`（秒级周期）、`usage_limit`（TPM）、`usage_limit_period`（秒级周期）用于定义请求频次与用量上限；  
  - 权限中 `inference`、`finetune`、`deploy` 均为布尔值，控制对应操作的开通/关闭；  
  - `access_all_entities`（`OPEN`/`CLOSE`/`KEEP`）支持一键授权全部推理模型，覆盖后续新增模型。

> **注意**：文档 2 中示例请求地址使用 `https://dashscope.aliyuncs.com/api/v1/models/limits`，但文档 1 和文档 4 明确要求将 `{WorkspaceId}` 替换为实际业务空间 ID 并拼接地域 Endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits`）。生产环境必须使用带 WorkspaceId 的地址，否则将返回鉴权失败或 404 错误。

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，推荐使用分页（`page_no`/`page_size`）遍历，避免遗漏；Python SDK 的 `Models.list()` 仅支持分页，复杂筛选需直接调用 HTTP API。  
- **查询/更新授权**：先用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取当前已授权模型清单；再用 `POST /api/v1/models/permissions` 批量更新权限，支持逐模型设置或 `access_all_entities=OPEN` 一键开通。  
- **查询/更新限流**：`GET /api/v1/models/limits` 返回 `model_limit`（账号级）与 `workspace_limit`（业务空间级）两级配额；`POST /api/v1/models/limits` 使用 `operation_type=OVERLAY` 合并更新，或 `DELETE` 清除限流。若需“仅设 RPM、豁免 TPM”，须两步执行：先 `DELETE` 再 `OVERLAY` 设置 `request_limit` [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

## 限制和注意事项

- 模型授权与限流均以**业务空间（Workspace）为作用域**，跨空间不共享；  
- `POST /models/permissions` 中 `models` 数组最多 20 项，`POST /models/limits` 最多 200 项；  
- 限流更新存在最终一致性，变更后约 30 秒内生效；  
- `usage_limit`（TPM）依赖 `request_limit`（QPM）存在：若当前无 QPM 限制，单独设置 TPM 将报错 `"Cannot set TPM without QPM"`；  
- 查询模型时 `service_site` 参数值 `global` 与 `international` 含义重叠，建议优先使用 `international`；`asia-pacific-china` 已被 `cn-hongkong` 等更细粒度值替代，旧值可能返回空结果 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 来源文档

- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


