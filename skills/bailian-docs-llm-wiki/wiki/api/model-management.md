# model management

模型管理是百炼平台为开发者提供的核心能力，用于查询、授权、限流和配额监控模型资源。通过统一的 REST API 接口，开发者可动态获取模型元信息、控制业务空间内模型的访问权限、设置调用频次与用量上限，并实时查看当前配额使用情况。所有操作均基于 API Key 认证，需提前配置 `DASHSCOPE_API_KEY` 环境变量。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成、实时全模态等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu`、`pixverse`、`tripo`、`xiaomi` 等 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。  
推理服务由 `aliyun-bailian`（百炼）、`siliconflow`（硅基流动）、`moonshot`（Kimi）等供应商提供；部署方式支持 `ptu`（预置吞吐量）。模型能力特征（`features`）包括 `function-calling`、`structured-outputs`、`web-search`、`cache`、`batch`、`fine-tuning` 等，可在查询时按需筛选。

> **注意**：文档 1 中 `inference_providers` 列表包含 `mini-max` 和 `kling`，但文档 4 的 `update-model-permissions.md` 中未提及对 `mini-max` 模型的授权支持，且实际调用 `POST /api/v1/models/permissions` 对非百炼原生模型（如 `mini-max`）可能返回 `InvalidParameter` 错误。建议优先使用 `providers=qwen` 或 `inference_provider=aliyun-bailian` 的模型以确保全功能兼容。

## 关键参数

| 参数类别 | 示例字段 | 说明 |
|----------|----------|------|
| **模型标识** | `model=qwen3.8-max`, `name=qwen` | `model` 用于精确匹配模型 ID；`name` 用于模糊搜索模型名称或 ID |
| **能力筛选** | `capabilities=TG&capabilities=Reasoning`, `features=function-calling` | 多值需重复参数名；`capabilities` 定义基础模态类型，`features` 描述高级能力 |
| **权限控制** | `inference=true`, `finetune=false`, `deploy=false` | 在授权接口中控制具体动作权限；`access_all_entities=OPEN` 可一键开通全部推理模型权限 |
| **限流配额** | `request_limit=60`, `request_limit_period=60`, `usage_limit=100000` | `request_limit_period=60` 表示 RPM，`=1` 表示 QPS；TPM 需与 QPM 同时存在（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)） |
| **分页与地域** | `page_no=1`, `page_size=100`, `service_site=cn-hongkong` | `page_size` 最大支持 200；`service_site` 控制模型部署区域可见性 |

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，支持按 `providers`、`capabilities`、`features` 等多维筛选。Python SDK 的 `Models.list()` 仅支持分页参数，复杂筛选需直接调用 HTTP API [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。  
- **管理模型授权**：先用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZABLE` 获取可授权模型列表；再用 `POST /api/v1/models/permissions` 设置 `inference`/`finetune`/`deploy` 权限，或启用 `access_all_entities=OPEN` 实现一键授权。  
- **配置模型限流**：使用 `POST /api/v1/models/limits` 设置 `request_limit`（QPM）与 `usage_limit`（TPM）。若仅需 RPM 限制，须先 `DELETE` 再 `OVERLAY` 单独设 QPM（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。  
- **查询当前限额**：调用 `GET /api/v1/models/limits` 查看各模型的 `model_limit`（账号级）与 `workspace_limit`（业务空间级）配额，其中 `request_limit_period=1` 表示 QPS，`=60` 表示 RPM [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)。

## 限制和注意事项

- 所有 API 均需在 Header 中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，且 `DASHSCOPE_API_KEY` 必须已配置为环境变量。
- 分页参数 `page_size` 最大为 200；`models` 批量操作（授权/限流）单次最多 200 个模型（授权）或 20 个模型（限流）。
- TPM（用量限制）依赖 QPM（请求限制）存在：若当前无 QPM 配置，直接设置 TPM 将报错 `"Cannot set TPM without QPM"`。必须先设置 QPM，或采用两步法（先 `DELETE` 再 `OVERLAY`）[更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- `access_all_entities=OPEN` 会自动覆盖历史逐模型授权，且对后续新增模型持续生效；`CLOSE` 将清空全部推理授权，不可逆。
- 模型上下文长度（`context_window`）、[Token](../concepts/token.md) 限制（`max_input_tokens` 等）在模型列表返回中为只读信息，不可修改；实际调用时超出限制将触发 `400 Bad Request`。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)


