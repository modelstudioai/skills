# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置与使用监控等全生命周期操作。开发者可通过统一 API 接口查询模型元信息（如能力、模态、上下文长度、定价）、获取当前业务空间的授权状态与配额限制，并按需调整推理权限和流量策略。所有操作均基于业务空间（Workspace）粒度进行隔离与管控。

## 支持的模型/功能

百炼平台支持多源模型接入，涵盖阿里巴巴-千问（`qwen`）、智谱AI（`zhipu-ai`）、月之暗面（`moonshot-ai`）、MiniMax（`mini-max`）、Kling（`kling`）、Vidu（`vidu`）、PixVerse（`pixverse`）、Tripo（`tripo`）、小米MiMo（`xiaomi`）等十余家供应商的模型。模型能力覆盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D生成（`3D-generation`）、实时全模态（`Realtime-Omni`）等；特性支持包括 function calling、结构化输出、联网搜索、cache 缓存、批量推理与微调等。具体能力与特性列表可参考 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中的 `capabilities` 与 `features` 字段定义。

> **注意**：文档 1 中列出的 `inference_providers` 包含 `moonshot`（对应 Kimi），但文档 1 的 `providers` 列表中为 `moonshot-ai`；而文档 5 的权限接口仅支持 `INFERENCE` 动作，未提及 `fine_tune` 或 `deploy` 在实际授权中的生效条件——该细节需以 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回的 `permissions` 字段为准，其明确声明 `fine_tune` 和 `deploy` 字段存在但当前值恒为 `false`，表明微调与部署权限暂未开放。

## 关键参数

模型管理相关接口共用以下关键参数：

- `model`（String）：模型 ID，用于精确查询或操作，如 `qwen3.8-max`，是所有写操作（授权、限流更新）的必填标识。
- `page_no` / `page_size`：分页参数，`page_no` 从 1 开始，`page_size` 最大支持 200（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)）。
- `authorization_scope`（仅授权接口）：取值 `AUTHORIZABLE`（默认，可授权模型）或 `AUTHORIZED`（已授权模型）。
- `operation_type`（仅限流更新）：`OVERLAY`（合并覆盖）或 `DELETE`（删除限流），详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

## 使用方式

### 查询模型元信息
调用 `GET /api/v1/models` 获取模型列表，支持按 `name`（模糊）、`model`（精确）、`providers`（作者）、`capabilities`（能力）、`context_window`（上下文长度）等多维筛选。推荐优先使用 `model` 参数直查单个模型，避免分页遍历。

### 查询与设置授权
- 查询：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取当前空间已启用推理权限的模型列表。
- 设置：`POST /api/v1/models/permissions` 提交 `models` 数组（逐模型）或 `access_all_entities=OPEN`（一键授权全部推理模型）。注意：`finetune` 和 `deploy` 字段目前仅作占位，设为 `true` 不产生实际授权效果。

### 查询与更新限流
- 查询：`GET /api/v1/models/limits?model=qwen3.8-max` 获取指定模型的账号级（`model_limit`）与业务空间级（`workspace_limit`）配额。
- 更新：`POST /api/v1/models/limits` 提交 `models` 数组，支持独立设置 `request_limit`（QPM/RPS）与 `usage_limit`（TPM/TPS）。若需“仅限 QPM、不限 TPM”，必须先 `DELETE` 再 `OVERLAY` 设置（参见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) 的 TPM 豁免说明）。

## 限制和注意事项

- **地域 Endpoint 差异**：所有接口均需根据业务空间所在地域选择对应域名（如北京为 `cn-beijing.maas.aliyuncs.com`），美国弗吉尼亚地区使用独立域名 `dashscope-us.aliyuncs.com`，不可混用。
- **权限与限流继承关系**：模型必须先被授权（`inference: true`）才可被调用；限流配额中 `workspace_limit` 不得超过 `model_limit`，否则更新失败。
- **配额生效延迟**：限流策略变更后，通常在 10 秒内生效，但高并发场景下可能存在短暂窗口期。
- **模型下线提示**：响应中 `inference_offline_info.offline_time` 字段标明预计下线时间，调用方应主动监听并迁移。
- **错误处理**：所有接口返回 `code`/`message` 字段，常见错误如 `InvalidParameter`（参数冲突）、`Forbidden`（无权限）需结合 [错误信息](../../raw/model-api-reference/preparations/error-code.md) 文档排查。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


