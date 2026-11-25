# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与使用监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、设置调用配额、授权业务空间访问权限，并基于返回的 `model` ID 直接发起推理请求。所有操作均需通过 API Key 认证，并按地域 Endpoint 调用。

## 支持的模型与功能

百炼平台聚合了来自阿里巴巴（`qwen`, `wan`, `qwen-domain-model`, `happyhorse`）、智谱AI（`zhipu-ai`）、MiniMax（`mini-max`）、月之暗面（`moonshot-ai`）、DeepSeek、Kling、Vidu、PixVerse、Tripo、小米（`xiaomi`）等多家供应商的模型，覆盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）、语音合成（`TTS`）、3D 生成、实时全模态（`Realtime-Omni`）等多种能力。模型支持的特性（如 `function-calling`、`structured-outputs`、`web-search`、`cache`）和部署方式（如 `ptu`）均可在查询结果中明确识别。完整可选值详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 文档。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 模型唯一标识符（ID），用于所有后续调用（如推理、限流、授权） | `"qwen3.8-max"` |
| `capabilities` | 模型能力标签数组，用于筛选具备特定能力的模型 | `["Reasoning", "VU"]` |
| `features` | 模型特性标签数组，如是否支持结构化输出或缓存 | `["function-calling", "cache"]` |
| `context_window` / `max_input_tokens` / `max_output_tokens` | 上下文长度相关字段，单位为 token，用于评估模型容量 | `1000000`, `991808`, `131072` |
| `request_limit` + `request_limit_period` | 限流参数：QPS/RPM 阈值及周期（秒） | `60`, `60`（即 60 QPM） |
| `usage_limit` + `usage_limit_period` | 用量限流参数：TPM 阈值及周期（秒） | `100000`, `60`（即 100k TPM） |

> **注意**：文档 3 中 `update-model-rate-limits.md` 明确要求“若需只限制 RPM、豁免 TPM”，必须采用两步法（先 `DELETE` 再 `OVERLAY` 设置 QPM），而文档 2 的 `list-quotas.md` 返回示例中 `qwen3.8-max` 的 `usage_limit_period` 为 `6` 秒——该周期值在实际限流策略中非常规（通常为 `60` 或 `3600`），且未在文档 3 的参数说明中列为合法值，建议以文档 3 的 `usage_limit_period` 定义为准。

## 使用方式

### 1. 查询模型列表  
使用 `GET /api/v1/models` 获取全部或筛选后的模型列表，支持按 `name`、`model`、`providers`、`capabilities`、`features`、`context_window` 等多维度过滤。推荐优先通过 `model` 精确查询单个模型以获取完整元数据（如定价、模态、上下文长度）。[查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 提供了各区域 Endpoint 和 SDK 调用示例。

### 2. 查询与更新限流配额  
- **查询**：调用 `GET /api/v1/models/limits` 获取账号级（`model_limit`）和业务空间级（`workspace_limit`）限流配置，含 `request_limit`、`usage_limit`、`async_user_queue_limit` 等字段。  
- **更新**：调用 `POST /api/v1/models/limits` 修改限流，支持 `OVERLAY`（合并覆盖）和 `DELETE`（清空）两种操作类型。注意：TPM 设置依赖 QPM 已存在，否则报错 `Cannot set TPM without QPM`。

### 3. 查询与更新模型授权  
- **查询**：调用 `GET /api/v1/models/permissions`，通过 `authorization_scope=AUTHORIZED` 获取当前已开通推理权限的模型列表；通过 `AUTHORIZABLE` 查看可授权模型池。  
- **更新**：调用 `POST /api/v1/models/permissions` 授权单个或多个模型的 `inference`、`finetune`、`deploy` 权限；也可启用 `access_all_entities=OPEN` 实现一键授权全部推理模型。详细权限字段定义见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)。

## 限制和注意事项

- **地域隔离**：所有模型管理 API 均按地域独立部署，Endpoint 必须与业务空间所在地域严格匹配（如华北2北京空间不可调用新加坡 Endpoint），否则返回 404 或鉴权失败。
- **权限前置**：调用 `models/permissions` 和 `models/limits` 前，业务空间必须已获得对应模型的 `inference` 授权；未授权模型无法设置限流或查看配额。
- **限流继承关系**：`workspace_limit` 不得超过 `model_limit`；若未设置 `workspace_limit`，则默认继承 `model_limit`。
- **配额生效延迟**：限流与授权变更通常在 10 秒内生效，但异步任务队列限制（`async_user_queue_limit`）可能有最高 30 秒延迟。
- **模型下线通知**：部分模型返回 `inference_offline_info.offline_time` 字段，表示预计下线时间，建议定期轮询并关注 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中的该字段。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


