# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与用量监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、设置调用配额、授权模型使用权限，并基于返回的 `model` ID 直接发起推理请求。所有操作均需通过 API Key 认证，且作用域默认为当前业务空间。

## 支持的模型与功能

百炼平台支持多供应商、多模态、多能力的模型集合，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）等 17+ 种 capabilities，以及 function calling、结构化输出、联网搜索等高级 features。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）等十余家供应商，部署模式覆盖 `global`、`asia-pacific-china`、`european-union` 等地域。完整模型列表及筛选能力详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

模型权限维度分为三类：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。并非所有模型均开放全部权限，例如 `qwen3-max` 支持微调但不支持部署，而多数基础模型仅开放推理权限。具体权限状态需通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 接口实时获取。

> **注意**：文档 5 中 `models[].finetune` 参数名与文档 4 返回字段 `fine_tune` 不一致（前者为 `finetune`，后者为 `fine_tune`），实际请求 Body 中应使用 `finetune`（无下划线），否则将被忽略。该不一致已在最新 SDK 中统一为 `finetune`。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **模型标识** | `model`（ID） | 唯一模型标识符，如 `qwen3-max`，用于所有模型相关 API 及推理调用；`name` 仅用于模糊搜索，非唯一。 |
| **能力筛选** | `capabilities`, `features`, `providers` | 查询时用于过滤模型集合，例如 `capabilities=TG&capabilities=Reasoning` 返回同时支持文本生成与深度思考的模型。 |
| **限流控制** | `request_limit` / `request_limit_period`（QPM/QPS）、`usage_limit` / `usage_limit_period`（TPM/TPS） | 限流单位需严格匹配周期：`request_limit_period=60` 表示每分钟请求数（QPM），`=1` 表示每秒（QPS）；`usage_limit_period=60` 表示每分钟 [Token](../concepts/token.md) 用量（TPM）。 |
| **权限开关** | `inference`, `finetune`, `deploy`（布尔值） | 更新授权时设为 `true` 授予、`false` 撤销；不传则保持现状。`access_all_entities=OPEN` 可一键授权当前空间全部推理模型。 |

## 使用方式

1. **发现模型**：调用 `GET /api/v1/models` 查询可用模型，推荐优先使用 `capabilities` 和 `providers` 组合筛选（如 `capabilities=TG&providers=qwen`），避免全量遍历。Python SDK 的 `Models.list()` 仅支持分页，**复杂筛选必须使用 HTTP API** —— 此限制在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中明确说明。
2. **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认目标模型是否已获 `inference` 权限，避免因权限缺失导致 403 错误。
3. **授权模型**：若未授权，调用 `POST /api/v1/models/permissions` 设置 `inference=true`；如需微调，同步设置 `finetune=true`（注意字段名为 `finetune`，非 `fine_tune`）。
4. **配置限流**：调用 `GET /api/v1/models/limits` 获取当前配额，再通过 `POST /api/v1/models/limits` 设置 `request_limit` 与 `usage_limit`。**TPM 豁免需两步操作**：先 `DELETE` 全部限流，再 `OVERLAY` 仅设 QPM —— 详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
5. **监控用量**：限额接口返回的 `model_limit.usage_limit` 与 `usage_limit_field`（如 `total_tokens`）共同定义用量上限，开发者需自行统计并遵守。

## 限制和注意事项

- **分页约束**：所有列表接口（模型、限额、权限）均强制分页，`page_size` 最大为 200，需循环请求 `page_no` 直至 `output.total` 耗尽。
- **地域 Endpoint 差异**：国际用户须使用 `dashscope-intl.aliyuncs.com` 或 `cn-hongkong.dashscope.aliyuncs.com` 等国际 Endpoint，北京 Endpoint（`cn-beijing.maas.aliyuncs.com`）仅限中国内地业务空间；文档 1 中列出的 WorkspaceId 形式 Endpoint **不适用于国际用户**，此差异在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 的 Endpoint 表格中有明确区分。
- **限流继承关系**：`workspace_limit` 是业务空间级配额，其值不能超过 `model_limit`（账号级上限）；若未设置 `workspace_limit`，则直接受 `model_limit` 约束。
- **授权生效延迟**：权限变更（尤其是 `access_all_entities=OPEN`）可能有数秒延迟，建议授权后等待 5 秒再发起推理请求。
- **模型下线风险**：返回结果中 `inference_offline_info.offline_time` 字段指示预计下线时间，生产环境应定期轮询并制定降级预案。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


