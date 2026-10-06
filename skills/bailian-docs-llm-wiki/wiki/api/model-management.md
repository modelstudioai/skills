# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控可用模型。通过统一的 RESTful API，开发者可程序化地查询模型元信息、设置调用配额、控制权限范围，并适配不同业务场景的合规与成本要求。所有操作均基于 API Key 认证，支持多地域、多工作空间隔离。

## 支持的模型/功能

百炼平台聚合了来自阿里巴巴（千问、万相、HappyHorse 等）、智谱 AI、MiniMax、月之暗面、DeepSeek、Kling、Vidu、Tripo、PixVerse、小米等多家供应商的模型，覆盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成、实时全模态（`Realtime-Omni`）等多种能力。模型按部署模式（如 `global`、`asia-pacific-china`、`european-union`）和推理服务供应商（如 `aliyun-bailian`、`siliconflow`、`moonshot`）分类，支持细粒度筛选。详细模型列表及能力标签可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口获取。

模型权限维度包括：`inference`（调用）、`fine_tune`（微调）、`deploy`（私有部署）。并非所有模型默认开放全部权限；例如 `qwen3-max` 支持微调而 `qwen-turbo` 不支持，具体以 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回的 `permissions` 字段为准。> **注意**：文档 5 中 `models[].finetune` 参数名与文档 4 返回字段 `fine_tune` 拼写不一致（`finetune` vs `fine_tune`），实际请求 Body 中应使用 `finetune`（无下划线），返回体中为 `fine_tune`（带下划线），SDK 实现需注意该差异。

## 关键参数

| 参数类别 | 示例参数 | 说明 |
|----------|----------|------|
| **筛选参数** | `capabilities=TG&providers=qwen` | 用于 `list-models` 和 `list-quotas`，支持多值（重复 key）或数组形式，如 `features=function-calling&features=web-search` |
| **分页参数** | `page_no=1&page_size=20` | 所有列表接口通用，`page_size` 最大值为 200（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)） |
| **限流参数** | `request_limit=60&request_limit_period=60` | 单位：次/分钟（QPM）；`usage_limit` 单位为 [Token](../concepts/token.md)/周期，周期单位为秒（如 `60` = 分钟） |
| **权限参数** | `inference=true&finetune=false` | `update-model-permissions` 请求中使用，`null` 表示保持现状；`access_all_entities=OPEN` 可一键授权全部推理模型 |

## 使用方式

1. **发现模型**：调用 `GET /api/v1/models` 查询模型列表，推荐优先使用 `capabilities` 和 `providers` 筛选，避免全量拉取。Python SDK 的 `Models.list()` 仅支持分页，复杂筛选请直接调用 HTTP API。
2. **检查权限**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 确认当前业务空间已启用的模型及其 `inference`/`fine_tune`/`deploy` 状态。
3. **设置权限**：调用 `POST /api/v1/models/permissions` 授权模型。若需批量开通推理权限，使用 `access_all_entities=OPEN`；若需精确控制，传入 `models` 数组并指定各模型权限布尔值。
4. **配置限流**：先调用 `GET /api/v1/models/limits` 查看当前配额，再调用 `POST /api/v1/models/limits` 更新。注意：TPM（用量限制）依赖 QPM（请求限制）存在，删除限流需显式传 `operation_type=DELETE`；若仅需设 QPM 豁免 TPM，须分两步操作（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。

## 限制和注意事项

- **配额继承关系**：模型级限流（`model_limit`）为账号全局上限，业务空间级限流（`workspace_limit`）不可超过其值；未设置 `workspace_limit` 时，实际生效配额为 `model_limit`。
- **地域与 Endpoint 差异**：`list-models` 接口在国际地域（如新加坡、德国）使用独立域名（如 `dashscope-intl.aliyuncs.com`），而 `list-quotas`、`update-model-rate-limits`、`list-model-permissions` 等管理类接口目前仅支持工作空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），跨地域调用将失败。
- **权限变更延迟**：模型授权变更后，新权限通常在 30 秒内生效，但部分高并发场景下可能延迟至 2 分钟。
- **模型下线提示**：`list-models` 返回的 `inference_offline_info.offline_time` 字段标识模型预计下线时间，建议定期轮询并制定迁移计划。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


