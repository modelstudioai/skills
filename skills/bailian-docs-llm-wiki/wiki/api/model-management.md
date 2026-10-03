# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、用量配额配置等全生命周期操作。开发者可通过统一 API 接口查询模型元信息、查看/更新当前业务空间的调用权限与限流策略，从而实现精细化的模型治理与资源规划。所有操作均基于 API Key 认证，需提前配置环境变量 `DASHSCOPE_API_KEY`。

## 支持的模型与功能

百炼平台支持多供应商、多模态、多能力的模型体系，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别（`ASR`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商，并支持按 `capabilities`、`providers`、`features`（如 `function-calling`、`structured-outputs`、`web-search`）等维度筛选。详细模型列表及能力说明请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

> **注意**：文档 1 中 `inference_providers` 列表包含 `moonshot`（Kimi），但文档 5 的 `providers` 列表中未列出该值；实际使用时应以 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中定义的 `providers` 和 `inference_providers` 取值为准，二者语义不同（前者为模型作者，后者为推理服务方），不可混用。

模型授权支持三级权限控制：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。并非所有模型默认开放全部权限，例如 `qwen3-max` 支持微调而 `qwen-turbo` 不支持（见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回示例）。授权状态可逐模型设置，也支持 `access_all_entities=OPEN` 一键开通当前空间全部推理模型权限。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **筛选参数** | `model`, `name`, `providers`, `capabilities`, `features`, `service_site` | 用于过滤模型列表，如 `capabilities=TG&providers=qwen` 查询通义千问文本生成模型；`service_site=asia-pacific-china` 限定中国区部署模型 |
| **分页参数** | `page_no`, `page_size` | 所有列表接口通用，`page_no` 从 1 开始，`page_size` 最大支持 200（[查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 明确限定） |
| **权限参数** | `inference`, `finetune`, `deploy`（布尔值） | 在更新授权时指定，`null` 表示保持现状；`false` 表示显式取消权限 |
| **限流参数** | `request_limit`, `request_limit_period`, `usage_limit`, `usage_limit_period` | 单位分别为“次/周期”和“Token/周期”，周期单位为秒（如 `60` = 每分钟）；`request_limit_period=1` 表示 QPS，`60` 表示 RPM |

## 使用方式

- **查询模型元信息**：调用 `GET /api/v1/models`，推荐使用 HTTP API（而非 SDK）以支持完整筛选条件；Python SDK 的 `Models.list()` 仅支持分页，不支持 `capabilities` 等高级筛选。
- **查询权限状态**：调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取已授权模型及其权限明细。
- **更新权限**：调用 `POST /api/v1/models/permissions`，支持两种模式：① `models` 数组逐模型设置（如授权 `qwen-plus` 微调）；② `access_all_entities=OPEN` 一键开通全部推理权限。
- **查询与更新限流**：  
  - 查询：`GET /api/v1/models/limits`，返回 `model_limit`（账号级上限）与 `workspace_limit`（业务空间级上限，可为空）；  
  - 更新：`POST /api/v1/models/limits`，通过 `operation_type=OVERLAY` 合并覆盖或 `DELETE` 彻底移除限流。注意：TPM（用量限制）依赖 QPM（请求限制）存在，删除时需两步操作（先删后设），详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

## 限制和注意事项

- **分页限制**：`page_size` 在权限查询接口中明确要求 ≤200（文档 3），模型列表接口虽未明说，但建议不超过 100 以保障响应性能；限额查询接口默认 `page_size=20`，需显式增大（如 `page_size=100`）以减少请求次数。
- **权限继承逻辑**：`access_all_entities=OPEN` 授权的是“当前及后续新增的推理模型”，但不会自动授予 `fine_tune` 或 `deploy` 权限；已有模型的权限变更仍需通过 `models` 数组显式操作。
- **限流强约束**：更新限流时若仅传 `usage_limit` 而未传 `request_limit`，将报错 `Cannot set TPM without QPM`（文档 4）。必须先设置 QPM，或采用两步法（先 `DELETE` 再 `OVERLAY`）。
- **Endpoint 差异**：国际站模型列表接口为 `https://dashscope-intl.aliyuncs.com/api/v1/models`（文档 1），而限流与权限接口在文档 2/3/4/5 中均使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 域名，**切勿混用**；国际站用户需确认对应地域的 WorkspaceId Endpoint。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


