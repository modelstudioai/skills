# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、配额管理与限流配置等全生命周期操作。开发者可通过统一 API 接口查询可用模型、检查授权状态、获取用量限额，并按需调整推理权限与流量策略。所有操作均基于业务空间（Workspace）隔离，支持细粒度控制。

## 支持的模型/功能

百炼平台支持多供应商、多模态、多能力的模型体系，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商；推理服务可由 `aliyun-bailian`（百炼）、`siliconflow`（硅基流动）、`moonshot`（Kimi）等提供。完整能力与供应商列表详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 3 中 `list-model-permissions.md` 的前提条件链接指向 `raw/model-api-reference/preparations/get-api-key.md`，而文档 1 和 2 均指向外部帮助中心 URL（`https://help.aliyun.com/...`）。实际生产环境应以 [配置API Key到环境变量](../../raw/model-api-reference/preparations/get-api-key.md) 为准，该路径为平台内统一凭证管理入口。

## 关键参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `model` | `String` | 模型唯一 ID，用于 API 调用和限流/授权操作 | `qwen3.8-max` |
| `capabilities` | `Array[String]` | 模型核心能力标签，用于筛选（如 `TG`, `Reasoning`, `IG`） | `["TG", "Reasoning"]` |
| `features` | `Array[String]` | 高级功能支持，如 `function-calling`、`structured-outputs`、`web-search` | `["function-calling"]` |
| `request_limit` / `request_limit_period` | `Number` | 请求频次限制（QPM/QPS），`period=60` 表示每分钟，`period=1` 表示每秒 | `60`, `60` |
| `usage_limit` / `usage_limit_period` | `Number` | 用量限制（TPM/TPS），单位为 Token 数 | `100000`, `60` |
| `inference` / `finetune` / `deploy` | `Boolean` | 授权开关，分别控制推理、微调、部署权限 | `true`, `false` |

## 使用方式

- **查询模型**：调用 `GET /api/v1/models`，支持按 `providers`、`capabilities`、`features`、`context_window` 等多维筛选。Python SDK 仅支持分页参数（`page`, `page_size`），复杂筛选需直接调用 HTTP API —— 参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **检查授权**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取当前业务空间已启用推理权限的模型列表；`AUTHORIZABLE` 则返回所有可申请授权的模型。
- **管理配额**：  
  - 查询限额：`GET /api/v1/models/limits` 返回各模型的 `request_limit`（QPM/QPS）与 `usage_limit`（TPM/TPS）；  
  - 更新限额：`POST /api/v1/models/limits` 支持 `OVERLAY`（合并覆盖）与 `DELETE`（清空限流）两种操作模式，详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **配置权限**：  
  - 逐模型授权：`POST /api/v1/models/permissions` 提交 `models` 数组，指定 `inference`/`finetune`/`deploy` 布尔值；  
  - 一键授权：设置 `access_all_entities=OPEN` 自动授予当前及后续新增的所有推理模型权限 —— 参见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。

## 限制和注意事项

- 所有 API 均需在请求 Header 中携带 `Authorization: Bearer {API_KEY}`，且 `DASHSCOPE_API_KEY` 必须已配置为环境变量。
- `list-models` 接口默认每页 20 条，需循环 `page_no` 直至 `output.total` 覆盖全部结果；`list-quotas` 与 `list-model-permissions` 同理。
- 限流更新（`update-model-rate-limits`）不支持原子性部分更新：若仅传 `request_limit` 而未传 `usage_limit`，后者将被重置为 `null`（即取消 TPM 限制），而非保持原值。如需“只设 QPM、豁免 TPM”，必须先 `DELETE` 再 `OVERLAY`（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 中的 TPM 豁免说明）。
- `update-model-permissions` 的 `access_all_entities=OPEN` 为长期生效策略，关闭需显式调用 `CLOSE`；`KEEP` 为默认行为，不改变现有逐模型授权状态。
- 模型上下文长度（`context_window`）、输入/输出 token 上限等元信息仅在 `list-models` 返回中提供，其他接口不返回该数据。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


