# model management

模型管理是百炼平台的核心能力之一，提供统一的模型发现、权限控制、限流配置与使用监控功能。开发者可通过标准 REST API 或 Python SDK 查询可用模型列表、查看/更新模型授权状态、设置/查询调用配额，从而实现对模型资源的精细化治理。所有操作均基于业务空间（Workspace）维度进行隔离与管控。

## 支持的模型/功能

百炼平台支持多厂商、[多模态](../concepts/multi-modal.md)、多能力的模型统一纳管，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek` 等十余家供应商，并支持按 `providers`（模型作者）和 `inference_providers`（推理服务方）双维度筛选。详细能力枚举与语义说明见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

模型授权支持三类操作：推理（`inference`）、微调（`finetune`）、部署（`deploy`），既可逐模型精细配置，也支持 `access_all_entities=OPEN` 的一键授权模式，适用于快速开通全量推理能力的场景。相关接口设计与权限语义详见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。

> **注意**：文档 4 中 `models[].finetune` 字段在请求示例中误写为 `fine_tune`（下划线），而参数定义表中为 `finetune`（无下划线）。实际 API 以参数定义表为准，即应使用 `finetune`（如 `{"model": "qwen-plus", "finetune": true}`），否则将返回 `InvalidParameter` 错误。

## 关键参数

模型管理接口广泛复用以下核心参数：

- **分页控制**：`page_no`（从 1 开始）与 `page_size`（最大 200），适用于所有列表类接口（`list-models`、`list-quotas`、`list-model-permissions`）。
- **模型标识**：`model`（精确匹配模型 ID，如 `qwen3.8-max`）与 `name`（模糊搜索模型名称），两者在各接口中语义一致。
- **权限与限流粒度**：所有操作均作用于指定 `WorkspaceId`，且限流（`/models/limits`）与授权（`/models/permissions`）均支持按模型 ID 单独配置，不跨模型继承。
- **限流单位**：`request_limit_period` 默认单位为秒（如 `60` 表示每分钟），`usage_limit_field` 明确计量维度（如 `total_tokens`），避免歧义。

## 使用方式

### 查询与发现
- 获取模型列表：调用 `GET /api/v1/models`，推荐使用 `capabilities`（如 `TG`）或 `providers`（如 `qwen`）筛选，避免全量拉取。Python SDK 的 `client.models.list()` 仅支持 `page_no`/`page_size`/`provider`，复杂筛选需直调 HTTP API —— 参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- 查看当前授权：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 返回已开通推理权限的模型；`AUTHORIZABLE` 则返回当前空间可申请授权的全部模型。

### 配置与管控
- 设置限流：`POST /api/v1/models/limits` 支持 `OVERLAY`（覆盖）与 `DELETE`（清空）两种操作。若需“仅限 RPM、不限 TPM”，必须分两步：先 `DELETE` 再 `OVERLAY` 仅设 `request_limit` —— 具体流程见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- 授权模型：`POST /api/v1/models/permissions` 支持混合模式——`models` 数组用于单点授权，`access_all_entities=OPEN` 用于批量开通。注意 `access_all_entities` 为 `OPEN` 时 `models` 可省略，但 `CLOSE` 后需重新显式授权。

## 限制和注意事项

- **SDK 功能差异**：DashScope Python SDK 2.0 的 `client.models.list()` 方法**不支持**按 `capabilities`、`features`、`context_window` 等高级条件筛选模型，仅支持基础分页与 `provider` 过滤。生产环境需直接调用 HTTP API 实现精准发现。
- **限流依赖关系**：更新 TPM（用量限制）前，必须已存在 QPM（请求频率限制）。若当前无 QPM，直接设置 TPM 将报错 `"Cannot set TPM without QPM"` —— 此约束在 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 中明确说明。
- **授权状态同步延迟**：`/models/permissions` 接口返回的 `AUTHORIZED` 列表反映的是**最终生效状态**，但新授权可能有数秒延迟。建议在调用模型前，先通过该接口确认 `permissions.inference === true`。
- **Endpoint 地域绑定**：除国际站（`dashscope-intl.aliyuncs.com`）和中国香港站外，其余地域（北京、东京、法兰克福等）的 Endpoint 均需动态替换 `{WorkspaceId}`，不可硬编码。国内用户默认使用华北2（北京）地域。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)


