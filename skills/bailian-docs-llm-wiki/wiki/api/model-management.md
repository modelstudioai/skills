# model management

模型管理是百炼平台的核心能力之一，为开发者提供统一的模型发现、权限控制、配额管理和使用监控能力。通过 RESTful API 和 SDK，开发者可程序化地查询可用模型、设置调用限额、授权模型访问权限，并获取模型元信息（如上下文长度、模态支持、定价等）。所有操作均基于业务空间（Workspace）隔离，支持多地域部署。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型统一管理，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商。推理服务亦由多家供应商提供，如 `aliyun-bailian`、`siliconflow`、`moonshot` 等，支持灵活的异构推理调度。详细模型列表及能力标签可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口获取。

## 关键参数

模型管理相关接口共用以下关键参数：

- **`model`（String）**：模型 ID，用于精确查询或限流/授权操作（如 `qwen3.8-max`），是调用推理 API 的必需字段；
- **`name`（String）**：模型名称模糊搜索，适用于快速定位系列模型（如 `qwen`）；
- **分页参数**：`page_no`（默认 1）和 `page_size`（默认 20，最大 200），用于遍历大规模模型集；
- **权限与限流专用参数**：
  - `authorization_scope`（`AUTHORIZABLE`/`AUTHORIZED`）控制查询范围，详见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)；
  - `request_limit` 与 `usage_limit`（含对应 `_period`）定义 QPM/TPM 阈值，单位为秒，`60` 表示每分钟；
  - `operation_type`（`OVERLAY`/`DELETE`）决定限流更新行为，见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

> **注意**：文档 1 中 `capabilities` 参数支持 `Realtime-Omni` 等实时能力标签，但文档 2、3、4、5 均未在限流或授权接口中提供对应筛选能力，实际使用时需先通过模型列表接口过滤出目标模型再逐个操作。

## 使用方式

### 查询与发现
- 使用 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 获取全量或筛选后的模型元数据（含 `context_window`、`features`、`prices` 等）；
- 使用 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 查看当前账号及业务空间下各模型的 QPM/TPM/并发队列等配额；
- 使用 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 确认模型是否已开通 `inference` 权限（必要前提）。

### 配置与管控
- 调用 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 设置或删除模型级 QPM/TPM 限制（POST `/api/v1/models/limits`）；
- 调用 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) 开通/关闭模型的 `inference`、`finetune` 或 `deploy` 权限（POST `/api/v1/models/permissions`），支持单模型粒度或 `access_all_entities=OPEN` 一键授权。

所有接口均需在 Header 中携带 `Authorization: Bearer YOUR_API_KEY`，并替换 `{WorkspaceId}` 为实际业务空间 ID。Python SDK 提供 `client.models.list()` 等便捷方法，但注意其参数支持有限（仅 `page_no`/`page_size`/`provider`），复杂筛选请直接调用 HTTP API。

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且未显式设置 `workspace_limit` 时默认继承 `model_limit`；
- **TPM 豁免约束**：若仅需设置 QPM 而不限制 TPM，必须分两步执行——先 `DELETE` 全部限流，再 `OVERLAY` 仅设 `request_limit`，中间存在短暂无限制窗口；
- **授权依赖关系**：调用模型前必须确保该模型在当前业务空间已获得 `inference: true` 权限，否则返回 `403 Forbidden`；微调（`finetune`）和部署（`deploy`）权限需单独申请；
- **SDK 功能差异**：DashScope Python SDK 2.0 的 `client.models.list()` 不支持 `capabilities`、`features` 等高级筛选参数，开发者需自行构造 HTTP 请求以实现精准过滤；
- **地域 Endpoint 差异**：美国区域模型列表接口为 `https://dashscope-us.aliyuncs.com/api/v1/models`（无 `{WorkspaceId}` 前缀），而其他地域均需拼接 `{WorkspaceId}`，调用时须严格区分。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


