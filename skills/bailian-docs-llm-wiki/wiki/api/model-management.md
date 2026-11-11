# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与使用监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、设置调用配额、授权模型访问权限，并基于返回的 `model` ID 直接发起推理请求。所有管理接口均需通过业务空间 ID 和 API Key 认证，支持多地域部署与细粒度筛选。

## 支持的模型与功能

百炼平台支持多供应商、多模态、多能力的模型体系，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）等十余家供应商，同时支持 `aliyun-bailian`、`siliconflow` 等多种推理服务后端。模型能力可通过 `capabilities` 和 `features` 参数组合筛选，例如 `capabilities=TG&features=function-calling` 可定位支持[函数调用](../concepts/function-calling.md)的文本生成模型。完整可选值详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 文档。

平台还提供模型授权管理，区分三种权限维度：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。默认仅开放部分模型的推理权限，其他权限需显式申请；未授权模型调用将返回 403 错误。授权状态可通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口实时获取。

> **注意**：文档 5 中 `models[].finetune` 字段名与文档 4 返回字段 `fine_tune` 不一致（前者为 `finetune`，后者为 `fine_tune`），实际请求 Body 应使用 `finetune`（无下划线），响应体中为 `fine_tune`（带下划线）。该命名差异已在 SDK 2.0 中统一为 `fine_tune`，HTTP 接口仍保持兼容。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `model` | 模型唯一 ID，用于推理调用及所有管理接口精确查询 | `"qwen3.8-max"` | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `capabilities` | 按能力类型筛选（数组，支持多值） | `["TG", "Reasoning"]` | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `request_limit` / `request_limit_period` | 请求频率限制（QPM/QPS），如 `60` 次/分钟 | `60`, `60` | [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) |
| `usage_limit` / `usage_limit_period` | 用量限制（TPM/TPS），如 `100000` tokens/分钟 | `100000`, `60` | [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) |
| `access_all_entities` | 一键授权开关，`OPEN` 表示授权当前空间全部推理模型 | `"OPEN"` | [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) |

## 使用方式

- **查询模型列表**：使用 `GET /api/v1/models`，推荐通过 `capabilities` + `providers` 组合筛选目标模型集。Python SDK 的 `client.models.list()` 仅支持 `page_no`/`page_size`/`provider` 三个参数，复杂筛选请直接调用 HTTP API。
- **查询限额与权限**：分别调用 `GET /api/v1/models/limits` 和 `GET /api/v1/models/permissions`，均支持 `model` 精确查询和分页。权限查询时需指定 `authorization_scope=AUTHORIZED` 获取已开通模型。
- **配置限流**：使用 `POST /api/v1/models/limits` 设置 QPM/TPM。若需“仅限 RPM、不限 TPM”，必须分两步：先 `DELETE` 全部限流，再 `OVERLAY` 仅设 `request_limit`。
- **管理授权**：使用 `POST /api/v1/models/permissions` 授权单个或多个模型；对新业务空间快速启用全部推理模型，可传 `{"access_all_entities": "OPEN"}`。

所有接口均需在 Header 中携带 `Authorization: Bearer YOUR_API_KEY`，并替换 `{WorkspaceId}` 为实际业务空间 ID。Endpoint 地域需与业务空间所在 Region 一致（如北京空间用 `cn-beijing.maas.aliyuncs.com`）。

## 限制和注意事项

- 模型列表接口默认每页 20 条，`total_count` 可能达数百，需循环 `page_no` 直至取完；Python SDK 不支持 `capabilities` 等高级筛选，务必使用 HTTP API 实现精准过滤。
- 限流配置中，`usage_limit`（TPM）依赖 `request_limit`（QPM）存在：若当前无 QPM 限制，直接设置 TPM 将报错 `Cannot set TPM without QPM`。该约束在 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 文档中有明确说明。
- 授权操作不可逆撤回 `access_all_entities=OPEN` 后新增的模型自动继承权限，但取消授权需手动逐个调用或使用 `CLOSE` 清空。
- 所有管理接口返回的 `model` 字段值（如 `qwen3.8-max`）是后续调用 `/v1/chat/completions` 等推理接口时 `model` 参数的唯一合法值，大小写与连字符必须完全一致。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


