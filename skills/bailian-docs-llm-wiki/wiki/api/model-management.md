# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、用量配额配置等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、查看/更新当前账号或业务空间下的调用限额与授权状态，从而实现精细化的资源治理与成本管控。

## 支持的模型与功能

百炼平台支持多供应商、多模态、多能力的模型体系，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，并支持按 `providers`、`capabilities`、`features`（如 `function-calling`、`structured-outputs`、`web-search`）等维度筛选。详细模型列表及能力说明请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 1 中 `inference_providers` 列表包含 `aliyun-bailian` 和 `alibaba-cloud-modelstudio`，但实际调用 `/api/v1/models` 返回的 `inference_provider` 字段值为 `aliyun-bailian`（如 `qwen3.8-max` 示例），而 `alibaba-cloud-modelstudio` 在返回示例中未出现；该字段语义应以实际 API 响应为准，建议以 `inference_provider` 返回值作为推理服务归属判断依据。

模型权限分为三类：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。并非所有模型均开放全部权限，需通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口确认当前业务空间的实际可授权范围。

## 关键参数

| 参数 | 作用 | 示例值 | 说明 |
|------|------|--------|------|
| `model` | 模型 ID（精确匹配） | `qwen3.8-max` | 所有管理接口均支持此参数用于定位目标模型 |
| `capabilities` | 按能力类型筛选 | `TG`, `Reasoning` | 多值需重复传参，如 `capabilities=TG&capabilities=Reasoning` |
| `features` | 按高级能力筛选 | `function-calling`, `web-search` | 决定模型是否支持结构化输出、联网等特性 |
| `request_limit` / `usage_limit` | 限流配额 | `60`, `100000` | 分别表示 QPM（每分钟请求数）和 TPM（每分钟 Token 数）上限 |
| `authorization_scope` | 授权状态筛选 | `AUTHORIZED`, `AUTHORIZABLE` | 用于区分“已授权”与“可授权但未授权”的模型 |

## 使用方式

- **查询模型元信息**：调用 `GET /api/v1/models`，支持分页与多维筛选（如 `providers=qwen&capabilities=TG`），返回模型 ID、上下文长度、定价、输入/输出模态等完整信息。Python SDK 的 `Models.list()` 仅支持分页，复杂筛选需直接调用 HTTP API —— 详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **查询/设置限流**：  
  - 查看配额：`GET /api/v1/models/limits`，返回 `model_limit`（账号级）与 `workspace_limit`（业务空间级）；  
  - 更新配额：`POST /api/v1/models/limits`，支持 `OVERLAY`（覆盖部分字段）与 `DELETE`（清空限流）两种操作模式。注意：TPM 设置依赖 QPM 已存在，否则报错 `Cannot set TPM without QPM` —— 参考 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **管理模型授权**：  
  - 查询当前授权：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`；  
  - 授权/取消授权：`POST /api/v1/models/permissions`，支持逐模型设置（`models` 数组）或一键授权（`access_all_entities=OPEN`）。`finetune` 字段在文档 5 中拼写为 `finetune`，但文档 3 返回字段名为 `fine_tune`，调用时请以请求体参数名 `finetune` 为准。

## 限制和注意事项

- **分页限制**：所有列表接口默认 `page_size=20`，最大支持 `200`（如 `list-model-permissions.md` 明确限定）；获取全部结果需循环请求并检查 `output.total`。
- **权限与限流隔离**：模型授权（`/permissions`）控制“能否调用”，限流（`/limits`）控制“调用频次/用量”，二者独立配置，缺一不可。
- **地域与 Endpoint 差异**：国际区域（如新加坡、德国）使用 `dashscope-intl.aliyuncs.com` 或 `eu-central-1.maas.aliyuncs.com` 等专属域名，而中国内地、香港、日本等地使用 `{WorkspaceId}.<region>.maas.aliyuncs.com` 格式 —— 具体地址请严格参照各接口文档中的 [Endpoint 表格](../../raw/model-api-reference/model-management/list-models.md)。
- **认证一致性**：所有接口均要求 `Authorization: Bearer {API_KEY}`，且 `DASHSCOPE_API_KEY` 必须已正确配置为环境变量，否则返回鉴权失败错误。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


