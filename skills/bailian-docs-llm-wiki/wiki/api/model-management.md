# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、配额管理与限流配置等全生命周期操作。开发者可通过统一 API 接口查询可用模型列表、查看/更新模型授权状态、获取/调整模型调用限额，从而实现精细化的模型资源治理。所有操作均基于业务空间（Workspace）粒度进行隔离与管控。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型接入，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，同时支持 `aliyun-bailian`（百炼自研推理服务）与 `siliconflow`（硅基流动）等推理服务商。详细模型能力与模态支持可参考 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中的 `capabilities` 和 `inference_metadata` 字段说明。

> **注意**：文档 5 中 `update-model-permissions.md` 的请求参数字段名为 `finetune`，但文档 4 中对应返回字段为 `fine_tune`（含下划线），且文档 4 的示例中明确使用 `"fine_tune":false`；实际调用时应以返回字段命名（`fine_tune`）为准，SDK 或客户端需保持一致，避免因字段名不匹配导致授权失败。

## 关键参数

模型管理相关接口共用以下核心参数：

- **`model`（String）**：模型唯一 ID（如 `qwen3.8-max`），用于精确查询或操作目标模型，是多数接口的推荐筛选维度。
- **`page_no` / `page_size`（Integer）**：分页参数，所有列表类接口（`list-models`、`list-quotas`、`list-model-permissions`）均支持，`page_size` 最大值为 200（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)）。
- **`providers` / `inference_providers`（Array[String]）**：分别用于按模型作者和推理服务供应商筛选，二者语义不同，不可混用（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。
- **`authorization_scope`（String）**：仅用于权限查询，取值 `AUTHORIZABLE`（默认，可授权模型）或 `AUTHORIZED`（已授权模型），影响返回结果集范围。

## 使用方式

| 功能 | 接口路径 | 方法 | 说明 |
|--------|-----------|------|------|
| 查询模型列表 | `/api/v1/models` | GET | 支持按 `capabilities`、`features`、`context_window` 等多维条件筛选；Python SDK 当前仅支持 `page_no`/`page_size`/`provider`，复杂筛选需直接调用 HTTP API（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。 |
| 查询模型限额 | `/api/v1/models/limits` | GET | 返回各模型的账号级限流（`model_limit`）与业务空间级限流（`workspace_limit`），含 QPS/RPM、TPM 及异步任务并发限制。 |
| 更新模型限额 | `/api/v1/models/limits` | POST | 通过 `operation_type=OVERLAY` 合并覆盖或 `DELETE` 清除限流；注意 TPM 设置依赖 QPM 已存在（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 错误码说明）。 |
| 查询模型授权 | `/api/v1/models/permissions` | GET | 指定 `authorization_scope` 获取可授权或已授权模型列表，`permissions` 字段明确标识 `inference`/`fine_tune`/`deploy` 权限状态。 |
| 更新模型授权 | `/api/v1/models/permissions` | POST | 支持逐模型设置（`models` 数组）或一键授权（`access_all_entities=OPEN/CLOSE`）；`finetune` 参数名在文档中存在拼写不一致，实际应使用 `fine_tune`。 |

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且未显式设置 `workspace_limit` 时默认继承 `model_limit`。
- **限流更新约束**：调用 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 设置用量限制（`usage_limit`）前，必须已存在请求频率限制（`request_limit`），否则返回 `InvalidParameter` 错误。
- **授权生效延迟**：模型授权变更（尤其是 `access_all_entities=OPEN`）通常秒级生效，但部分新上架模型可能需数分钟同步至权限系统，建议操作后通过 `list-model-permissions?authorization_scope=AUTHORIZED` 验证。
- **地域 Endpoint 差异**：国际站（`dashscope-intl.aliyuncs.com`）与国内站（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）Endpoint 不同，且国际站不支持 WorkspaceId 路径变量；跨地域调用需严格匹配文档中列出的 Endpoint（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 地域章节）。
- **Python SDK 能力边界**：`dashscope.Client.models.list()` 仅支持基础分页与 `provider` 过滤，所有高级筛选（如 `capabilities=TG&features=function-calling`）必须使用原生 HTTP 请求。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


