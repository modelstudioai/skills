# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控可用模型。通过统一的 RESTful API，开发者可程序化地查询模型元信息、设置调用配额、控制访问权限，并适配不同业务场景（如推理、微调、部署）。所有操作均基于 API Key 认证，支持多地域、多工作空间隔离。

## 支持的模型与功能

百炼平台聚合了来自阿里巴巴及第三方厂商的多种模型，涵盖文本、图像、视频、语音、3D 等多模态能力。模型按 `providers`（如 `qwen`、`zhipu-ai`、`kling`）和 `inference_providers`（如 `aliyun-bailian`、`moonshot`）分类，并通过 `capabilities`（如 `TG`、`IG`、`VG`、`ASR`）标识核心能力类型。同时支持按 `features`（如 `function-calling`、`structured-outputs`、`web-search`）筛选具备特定高级能力的模型。完整支持的模型列表可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口动态获取。

模型权限体系分为三级：**推理（`inference`）**、**微调（`fine_tune`）** 和 **部署（`deploy`）**，默认仅开放部分模型的推理权限。开发者需显式调用授权接口启用其他能力。例如，`qwen3-max` 默认支持推理与微调，但不支持部署；而 `qwen-turbo` 仅支持推理。具体权限状态需以 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回结果为准。

> **注意**：文档 5 中 `models[].finetune` 参数名与文档 4 返回字段 `fine_tune` 拼写不一致（`finetune` vs `fine_tune`），实际请求 Body 中必须使用 `finetune`（无下划线），否则将被忽略。该不一致已在最新 SDK 中统一为 `fine_tune`，但 HTTP API 仍保留旧字段名。

## 关键参数

| 参数类别 | 参数名 | 类型 | 说明 |
|----------|--------|------|------|
| **通用筛选** | `model` / `name` | `String` | 精确匹配模型 ID 或模糊搜索名称，适用于所有模型管理接口 |
| **能力过滤** | `capabilities`, `features`, `providers` | `Array[String]` | 多值筛选，如 `capabilities=TG&capabilities=Reasoning` 表示“文本生成或深度思考”（OR 逻辑） |
| **权限控制** | `inference`, `finetune`, `deploy` | `Boolean` | 更新授权时指定各动作是否开启；`null` 表示保持现状（见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)） |
| **限流配置** | `request_limit`, `request_limit_period`, `usage_limit`, `usage_limit_period` | `Number` | 分别控制 QPS/RPM 与 TPM；`request_limit_period=1` 表示每秒，`=60` 表示每分钟 |

## 使用方式

### 1. 查询模型元信息  
调用 `GET /api/v1/models` 获取模型列表、上下文长度（`model_info.context_window`）、定价（`prices`）及输入/输出模态（`inference_metadata`）。Python SDK 的 `Models.list()` 仅支持分页，**复杂筛选必须使用 HTTP API**（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。

### 2. 查询与设置限流  
- 查询当前配额：`GET /api/v1/models/limits`，返回 `model_limit`（账号级）与 `workspace_limit`（业务空间级）双层限流策略。  
- 更新限流：`POST /api/v1/models/limits`，支持 `OVERLAY`（合并覆盖）与 `DELETE`（清空）两种操作。**TPM 豁免需两步操作**：先 `DELETE` 再仅设 `request_limit`（详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。

### 3. 管理模型权限  
- 查询授权状态：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取已开通推理权限的模型列表。  
- 授权操作：`POST /api/v1/models/permissions` 支持两种模式：  
  - **逐模型**：在 `models` 数组中指定 `model` 及布尔权限字段；  
  - **一键授权**：设置 `access_all_entities=OPEN` 自动授权所有（含未来新增）推理模型。

## 限制和注意事项

- **分页限制**：所有列表接口 `page_size` 最大为 200，`models.list()` SDK 不支持非分页参数筛选。  
- **限流继承性**：业务空间级限流（`workspace_limit`）不能超过账号级上限（`model_limit`），且未设置时默认继承账号级策略。  
- **授权生效延迟**：权限变更后，新请求通常在 10 秒内生效，但缓存可能导致短暂不一致。  
- **Endpoint 差异**：国际站与国内站 Endpoint 不同（如 `dashscope-intl.aliyuncs.com` vs `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），调用前需确认地域并替换 `{WorkspaceId}`。  
- **错误处理**：所有接口均返回标准 `request_id`，排查问题时务必提供该字段（见各文档末尾的 [错误信息](../../raw/model-api-reference/preparations/error-code.md) 链接）。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


