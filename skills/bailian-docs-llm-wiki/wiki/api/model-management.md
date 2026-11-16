# model management

模型管理是百炼平台的核心能力之一，为开发者提供统一的模型发现、权限控制、限流配置与元信息查询接口。所有操作均基于业务空间（Workspace）隔离，支持按地域调用，并通过 API Key 进行身份认证。开发者可通过 HTTP API 或 DashScope Python SDK（2.x）完成全流程管理。

## 支持的模型/功能

百炼平台支持多源模型接入，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）等 16+ 种能力，以及 function calling、结构化输出、缓存（`cache`）、批量推理（`batch`）等高级特性。模型来源包括 `qwen`（阿里巴巴-千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）等十余家供应商，部署模式覆盖 `global`、`asia-pacific-china`、`european-union` 等区域。完整模型列表及能力详情请参考 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 |
|----------|--------|------|
| **通用筛选** | `model` / `name` | `model` 用于精确匹配模型 ID（如 `qwen3.8-max`），`name` 用于模糊搜索模型名称；二者不可同时为空。 |
| **权限控制** | `authorization_scope` | 取值 `AUTHORIZABLE`（可授权模型，默认）或 `AUTHORIZED`（已授权模型），见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)。 |
| **限流配置** | `request_limit` / `usage_limit` | 分别表示请求频率上限（QPM/RPS）和用量上限（TPM），单位周期由 `request_limit_period` / `usage_limit_period`（秒）指定；`operation_type=DELETE` 时需清空所有限流字段。 |
| **模型元信息** | `capabilities` / `features` / `context_window` | 用于筛选模型能力（如 `["TG", "Reasoning"]`）、特性（如 `["function-calling"]`）或上下文长度（严格小于给定值）。 |

> **注意**：文档 1 中 `providers` 参数在 DashScope Python SDK 2.x 中仅对当前页做客户端筛选，但 `output.total` 仍返回未筛选前的总数；而文档 2 和文档 5 的限流接口中，`request_limit_period=1` 表示 QPS，`=60` 表示 RPM——该语义一致性已在各文档中明确，无矛盾。

## 使用方式

1. **发现模型**：调用 `GET /api/v1/models` 查询可用模型，支持按 `providers`、`capabilities`、`context_window` 等多维筛选；推荐使用 `model=qwen3.8-max` 精确获取单个模型详情。  
2. **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认当前业务空间已开通哪些模型的 `inference` 权限。  
3. **授权模型**：调用 `POST /api/v1/models/permissions` 授予或取消 `inference`/`finetune`/`deploy` 权限；支持逐模型设置（`models` 数组）或一键授权全部（`access_all_entities=OPEN`），详见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。  
4. **配置限流**：调用 `POST /api/v1/models/limits` 设置或删除模型级限流；若需“仅限 QPM、不限 TPM”，须先 `DELETE` 再 `OVERLAY` 设置，避免触发 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 中的校验错误（如 `Cannot set TPM without QPM`）。  
5. **监控配额**：调用 `GET /api/v1/models/limits` 实时查看账号级（`model_limit`）与业务空间级（`workspace_limit`）限流生效状态。

## 限制和注意事项

- 所有 API 均需在请求头携带 `Authorization: Bearer <API Key>`，API Key 需在对应地域的 [百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 获取。  
- 模型列表接口 `page_size` 最大为 200，限额与授权接口同为 200；超出需分页处理。  
- `update-model-permissions` 接口对 `finetune` 和 `deploy` 权限的授予受模型本身能力约束（例如非微调型模型无法开启 `finetune:true`），失败时返回 `InvalidParameter` 错误。  
- 限流更新为“合并覆盖”语义（`OVERLAY` 默认），未传字段将保留原值；`DELETE` 操作不可逆，且要求 `models[].operation_type="DELETE"` 时所有限流字段必须显式设为 `null` 或省略。  
- 模型下线信息（`inference_offline_info`）仅在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 响应中返回，开发者应定期轮询以规避服务中断。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)


