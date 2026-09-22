# model management

模型管理是百炼平台为开发者提供的核心能力，用于统一发现、授权、限流和监控所用模型。通过 RESTful API，开发者可程序化地查询可用模型列表、设置模型调用权限、配置限流策略，并实时获取配额使用情况。所有操作均基于业务空间（Workspace）维度进行隔离与管控。

## 支持的模型/功能

百炼平台支持多模态、多供应商的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成、实时全模态等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，且支持按 `capabilities`、`providers`、`features`（如 `function-calling`、`structured-outputs`、`web-search`）等多维条件筛选。完整模型能力矩阵详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

模型管理功能覆盖三大核心场景：  
- **授权控制**：支持逐模型粒度的 `inference`（推理）、`finetune`（微调）、`deploy`（部署）权限开关，也支持 `access_all_entities=OPEN` 的一键授权模式；  
- **流量治理**：提供 QPM（请求次数）与 TPM（[Token](../concepts/token.md) 用量）双维度限流，支持 `OVERLAY`（合并覆盖）与 `DELETE`（清除）两种操作类型；  
- **配额洞察**：可实时查询各模型在账号级（`model_limit`）与业务空间级（`workspace_limit`）的限流配置及异步任务并发/排队限制。

> **注意**：文档中 `models[].finetune` 字段在 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 的请求示例中误写为 `fine_tune`（下划线），但实际 API 仅接受 `finetune`（驼峰无下划线）。请以接口定义为准，避免因字段名不一致导致 400 错误。

## 关键参数

| 参数类别 | 参数名 | 类型 | 说明 |
|----------|--------|------|------|
| **通用筛选** | `model` / `name` | `String` | 精确匹配模型 ID 或模糊搜索模型名称 |
| | `page_no` / `page_size` | `Integer` | 分页控制，默认 `page_no=1`, `page_size=20` |
| **能力筛选** | `capabilities` | `Array[String]` | 如 `TG`, `Reasoning`, `VU`；支持多值 `&capabilities=TG&capabilities=Reasoning` |
| | `features` | `Array[String]` | 如 `function-calling`, `web-search`, `cache` |
| | `providers` | `Array[String]` | 模型作者，如 `qwen`, `zhipu-ai`；注意与 `inference_providers`（推理服务方）区分 |
| **限流配置** | `request_limit` / `usage_limit` | `Number` | QPM 与 TPM 数值，`null` 表示不变更；`usage_limit` 为 `null` 即豁免 [Token](../concepts/token.md) 用量限制 |
| | `request_limit_period` / `usage_limit_period` | `Number` | 时间周期（秒），`60` = 每分钟，`1` = 每秒（即 QPS） |
| **授权控制** | `inference` / `finetune` / `deploy` | `Boolean` | 权限开关，`null` 表示保持现状；[更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 中明确要求此三字段为布尔值 |

## 使用方式

- **查询模型列表**：调用 `GET /api/v1/models`，推荐使用 HTTP 直接请求（而非 Python SDK 的 `Models.list()`），因其支持全部筛选参数（SDK 仅支持分页）；  
- **查询授权状态**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取当前已开通推理权限的模型；  
- **设置权限**：调用 `POST /api/v1/models/permissions`，传入 `models` 数组或 `access_all_entities=OPEN`；  
- **配置限流**：调用 `POST /api/v1/models/limits`，注意 `operation_type=DELETE` 时需清空所有限流字段；  
- **查询限额**：调用 `GET /api/v1/models/limits`，返回含 `model_limit`（账号级上限）与 `workspace_limit`（业务空间级配置）的嵌套结构。

所有接口均需在 Header 中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，Endpoint 需替换 `{WorkspaceId}` 并选择对应地域（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。

## 限制和注意事项

- 模型列表接口单页最多返回 200 条（`page_size` 最大值），需分页遍历获取全量；  
- 限流更新接口 `models` 数组长度限制为 1~200，批量操作建议分批提交；  
- TPM 豁免不可直接设为 0，须先 `DELETE` 再仅设 `request_limit`（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 中“TPM 豁免场景”说明）；  
- 一键授权 `access_all_entities=OPEN` 仅对**当前业务空间内已上架且支持推理的模型**生效，不包含后续新增模型（除非平台策略更新）；  
- `inference_metadata.request_modality` 和 `response_modality` 字段用于判断 I/O 模态兼容性（如 `["Text"]` → `["Image"]` 表示文生图），调用前务必校验，避免 `400 Bad Request`；  
- 所有模型的 `context_window`、`max_input_tokens` 等长度限制以 `model_info` 字段返回，部分图像/视频模型该值为 `null`，需参考其 `prices` 中的计费单元（如 `image_number`）而非 [Token](../concepts/token.md) 数。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)


