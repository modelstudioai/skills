# model management

模型管理是百炼平台的核心能力之一，提供统一的模型发现、权限控制、限流配置与用量监控能力。开发者可通过 RESTful API 查询可用模型列表、查看/更新模型授权状态、设置/调整模型调用配额，从而实现精细化的模型生命周期治理。所有操作均基于业务空间（Workspace）维度进行隔离与管控。

## 支持的模型/功能

百炼平台支持多模态、多供应商的模型生态，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek` 等十余家供应商，同时支持 `aliyun-bailian`、`siliconflow` 等多种推理服务后端。具体支持的模型列表、模态类型、能力标签（如 `function-calling`、`structured-outputs`）及上下文窗口等元信息，可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口实时获取。

模型授权体系分为三级权限：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。并非所有模型默认开放全部权限；例如 `qwen3-max` 支持微调但 `qwen-turbo` 不支持（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回示例）。授权状态可按模型粒度或通过 `access_all_entities=OPEN` 一键开通当前空间全部推理模型（含后续新增），详见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。

> **注意**：文档 5 中 `models[].finetune` 参数名与文档 4 中返回字段 `fine_tune` 拼写不一致（`finetune` vs `fine_tune`），实际请求 Body 中必须使用 `finetune`（无下划线），否则将被忽略。该不一致已在最新 SDK 中统一为 `fine_tune`，但 HTTP API 仍以文档 5 为准。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **筛选参数** | `capabilities`, `providers`, `features`, `service_site`, `supports` | 用于在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中精准定位目标模型，例如 `capabilities=TG&providers=qwen` 获取通义千问文本生成模型 |
| **权限参数** | `inference`, `finetune`, `deploy` | 在 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 中控制模型能力开关；`finetune` 字段名无下划线，需特别注意 |
| **限流参数** | `request_limit`, `request_limit_period`, `usage_limit`, `usage_limit_period` | 用于 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 和 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)，单位分别为“次/周期”和“Token/周期”，周期单位为秒（如 `60` 表示每分钟） |

## 使用方式

1. **发现模型**：调用 `GET /api/v1/models`，推荐先用 `capabilities` + `providers` 筛选缩小范围，再结合 `page_no`/`page_size` 分页获取完整列表；
2. **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认目标模型是否已获 `inference: true`；
3. **授予权限**：若未授权，调用 `POST /api/v1/models/permissions` 提交 `{"model": "xxx", "inference": true}`；
4. **配置限流**：调用 `GET /api/v1/models/limits` 查看当前配额，再用 `POST /api/v1/models/limits` 设置 `request_limit`（QPM/QPS）和 `usage_limit`（TPM/TPS）；
5. **SDK 提示**：DashScope Python SDK 的 `Models.list()` 仅支持分页参数，**不支持** `capabilities` 等高级筛选，复杂查询请直接使用 HTTP API（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且未显式设置 `workspace_limit` 时默认继承 `model_limit`；
- **TPM 豁免约束**：若需仅限制 RPM 而不限制 TPM，必须分两步操作——先 `DELETE` 全部限流，再 `OVERLAY` 仅设 `request_limit`（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 中的“TPM 豁免场景”）；
- **授权生效延迟**：`access_all_entities=OPEN` 开通后，新上架模型通常在 5 分钟内自动获得推理权限，但需确保模型本身处于 `AUTHORIZABLE` 状态；
- **Endpoint 差异**：国际站用户应使用 `dashscope-intl.aliyuncs.com` 域名，而中国站用户需替换 `{WorkspaceId}` 并选用对应地域 Endpoint（如 `cn-beijing.maas.aliyuncs.com`），详见各文档的 Endpoint 表格。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


