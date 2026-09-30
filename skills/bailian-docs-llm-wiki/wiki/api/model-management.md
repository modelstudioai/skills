# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控可用模型。通过统一的 RESTful API，开发者可程序化地查询模型元信息、设置调用配额、控制模型访问权限，并适配不同业务场景（如推理、微调、部署）。所有操作均基于 API Key 认证，支持多地域、多工作空间隔离。

## 支持的模型与功能

百炼平台聚合了来自阿里巴巴及第三方厂商的多种模型，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）等模态能力。模型按 `providers`（如 `qwen`、`zhipu-ai`、`moonshot-ai`）和 `inference_providers`（如 `aliyun-bailian`、`siliconflow`）分类，支持按 `capabilities`、`features`（如 `function-calling`、`web-search`）、`service_site`（如 `asia-pacific-china`、`united-states`）等多维条件筛选。完整模型列表及能力详情请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 4 中 `update-model-permissions.md` 的请求示例字段名 `fine_tune` 与文档 5 `list-model-permissions.md` 返回结构中实际字段 `finetune` 不一致；实际 API 接受并返回 `finetune`（无下划线），示例中的 `fine_tune` 为笔误，应以 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 的返回结构为准。

## 关键参数

| 参数类别 | 示例字段 | 说明 |
|----------|----------|------|
| **筛选维度** | `providers`, `capabilities`, `features`, `service_site` | 用于 `list-models` 和 `list-quotas` 等接口，支持数组传参（如 `capabilities=TG&capabilities=Reasoning`） |
| **分页控制** | `page_no`, `page_size` | 所有列表类接口通用，`page_no` 从 1 开始，`page_size` 最大 200 |
| **限流配置** | `request_limit`, `request_limit_period`, `usage_limit`, `usage_limit_period` | 单位：`request_limit_period=60` 表示 QPM，`=1` 表示 QPS；`usage_limit_field` 固定为 `total_tokens`（见 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)） |
| **权限控制** | `inference`, `finetune`, `deploy` | 布尔值，控制对应操作是否启用；`access_all_entities=OPEN` 可一键授权全部推理模型 |

## 使用方式

- **发现模型**：调用 `GET /api/v1/models` 查询可用模型，推荐使用 HTTP API（而非 SDK）以充分利用 `capabilities`、`features` 等高级筛选能力；Python SDK 的 `Models.list()` 仅支持分页，不支持条件过滤。
- **查看配额**：调用 `GET /api/v1/models/limits` 获取当前 API Key 下各模型的请求频率（QPS/QPM）和用量（TPM）限制。
- **调整限流**：调用 `POST /api/v1/models/limits` 更新限流策略，支持 `OVERLAY`（合并覆盖）和 `DELETE`（清空）两种操作类型；若需“仅限 RPM、豁免 TPM”，须分两步执行（先 DELETE 再 OVERLAY）。
- **管理权限**：调用 `GET /api/v1/models/permissions` 查看已授权或可授权模型；调用 `POST /api/v1/models/permissions` 授权单个模型或启用 `access_all_entities=OPEN` 一键授权。

## 限制和注意事项

- 所有 API 均需在 Header 中携带 `Authorization: Bearer {API_KEY}`，且 `DASHSCOPE_API_KEY` 必须已配置为环境变量。
- `list-models` 接口的 `context_window` 参数含义为“返回上下文长度**严格小于**该值的模型”，非“大于等于”或“等于”。
- 限流更新接口（`update-model-rate-limits`）存在强约束：**不可单独设置 TPM 而不设置 QPM**，否则返回 `InvalidParameter` 错误；必须先设置 QPM，再叠加 TPM。
- 模型授权状态变更后，通常在 1 分钟内生效；但 `access_all_entities=OPEN` 授权范围包含“后续新增模型”，其生效时间可能延长至 5 分钟。
- 各接口 Endpoint 中 `{WorkspaceId}` 需显式替换为实际业务空间 ID；国际站用户应使用 `dashscope-intl.aliyuncs.com` 等对应国际域名（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)


