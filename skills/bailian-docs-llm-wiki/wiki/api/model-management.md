# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、限流配置等全生命周期管理接口。开发者可通过标准 REST API 查询可用模型列表、查看/设置模型调用配额、授权或取消模型使用权限。所有操作均基于业务空间（Workspace）维度进行隔离与管控。

## 支持的模型与功能

百炼平台支持多供应商、[多模态](../concepts/multi-modal.md)、多能力的模型统一纳管，涵盖文本生成（`TG`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成、实时全模态等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，同时支持 `aliyun-bailian`（百炼自研推理服务）及第三方推理服务（如 `siliconflow`、`vanchin`）。详细模型能力与供应商映射关系请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 文档中 `providers` 和 `capabilities` 参数说明。

> **注意**：文档 5 中 `update-model-permissions.md` 的 `models[].finetune` 字段名与文档 4 中 `list-model-permissions.md` 返回字段 `fine_tune` 不一致（前者为 `finetune`，后者为 `fine_tune`），实际请求体应使用 `finetune`（无下划线），返回体为 `fine_tune`（带下划线）。该命名差异已在 SDK v1.21.0+ 中统一为 `fine_tune`，但 HTTP 接口仍保持兼容。

模型权限分为三类：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。并非所有模型均支持全部权限，例如 `qwen-turbo` 默认仅开放推理权限，而 `qwen3-max` 同时支持推理与微调。具体权限状态需通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口实时获取。

## 关键参数

| 参数类别 | 关键参数 | 说明 |
|----------|----------|------|
| **模型筛选** | `model`, `name`, `providers`, `capabilities`, `features`, `service_site` | `model` 用于精确匹配模型 ID（如 `qwen3-max`）；`capabilities=TG` 可筛选文本生成模型；`features=function-calling` 表示支持[函数调用](../concepts/function-calling.md)。详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。 |
| **分页控制** | `page_no`, `page_size` | 所有列表接口通用，`page_no` 从 1 开始，`page_size` 最大支持 200（`list-quotas.md` 和 `list-model-permissions.md` 明确限定最大值为 200）。 |
| **限流配置** | `request_limit`, `request_limit_period`, `usage_limit`, `usage_limit_period` | 单位：`request_limit_period=60` 表示 QPM，`=1` 表示 QPS；`usage_limit_field` 固定为 `total_tokens`（当前仅支持 [Token](../concepts/token.md) 用量限制）。 |
| **权限控制** | `inference`, `finetune`, `deploy`, `access_all_entities` | `access_all_entities=OPEN` 可一键授权当前空间所有可推理模型（含未来新增），无需逐个指定 `models`。 |

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，推荐使用 HTTP 直接请求以支持完整筛选条件；Python SDK 的 `Models.list()` 仅支持分页，不支持 `capabilities` 等高级筛选。
- **查询/设置限流**：  
  - 查看配额：`GET /api/v1/models/limits?model=qwen3-max`  
  - 更新配额：`POST /api/v1/models/limits`，传入 `models` 数组，`operation_type=OVERLAY`（默认）或 `DELETE`。  
  - 注意：若需“仅限 RPM、不限 TPM”，必须分两步执行（先 `DELETE` 再 `OVERLAY` 设置 QPM），详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **管理模型权限**：  
  - 查看授权状态：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`  
  - 授权单个模型：`POST /api/v1/models/permissions`，在 `models` 中指定 `model` 和布尔值（如 `"inference": true`）  
  - 一键授权：`POST /api/v1/models/permissions`，传 `{"access_all_entities": "OPEN"}` 即可开通当前空间全部推理模型权限。

## 限制和注意事项

- **分页上限**：`list-quotas.md` 和 `list-model-permissions.md` 明确要求 `page_size ≤ 200`，超出将返回 400 错误；`list-models.md` 未明确上限，但建议不超过 100 以保障响应性能。
- **权限变更延迟**：模型授权变更（尤其是 `access_all_entities=OPEN`）通常在 30 秒内生效，但[异步任务](../concepts/asynchronous-task.md)可能短暂沿用旧权限缓存。
- **限流继承关系**：`workspace_limit` 是业务空间级限制，其总和不能超过 `model_limit`（账号级上限）；若未设置 `workspace_limit`，则直接继承 `model_limit`。
- **Endpoint 差异**：国际站模型列表接口使用 `https://dashscope-intl.aliyuncs.com/api/v1/models`（无 `{WorkspaceId}`），而国内站及部分地域（如北京、东京）需替换 `{WorkspaceId}`。务必根据实际部署地域选择对应 Endpoint，否则返回 404 或权限错误。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


