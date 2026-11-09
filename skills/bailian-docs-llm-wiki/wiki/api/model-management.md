# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、配额设置与限流配置等全生命周期管理功能。开发者可通过统一 API 接口查询可用模型、授权调用权限、设置业务空间级限流，并实时获取模型元信息（如上下文长度、模态支持、定价等）。所有操作均基于业务空间（Workspace）隔离，需使用有效的 API Key 进行身份认证。

## 支持的模型/功能

百炼平台支持多厂商、多模态、多能力的模型统一纳管，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商。同时支持按部署模式（如 `global`、`cn-hongkong`、`european-union`）和推理服务供应商（如 `aliyun-bailian`、`siliconflow`）筛选。详细模型列表及能力描述请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | String | 模型 ID（如 `qwen3.8-max`），用于精确查询、限流或授权操作，**所有接口均以此为模型标识主键**。 |
| `capabilities` | Array\[String\] | 模型能力标签（如 `TG`, `Reasoning`, `VU`），用于筛选符合业务场景的模型。注意：[查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 支持该参数，但 Python SDK 的 `client.models.list()` **不支持**。 |
| `request_limit` / `usage_limit` | Number | QPM（每分钟请求数）与 TPM（每分钟 [Token](../concepts/token.md) 用量）限流值，单位分别为“次/分钟”和“token/分钟”，在限流更新与限额查询中使用。 |
| `authorization_scope` | String | 权限查询范围，取值 `AUTHORIZABLE`（可授权模型）或 `AUTHORIZED`（已授权模型），详见 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)。 |

> **注意**：文档 2（更新模型限流）与文档 4（查询模型限额）中 endpoint 路径相同（`/api/v1/models/limits`），但 HTTP 方法不同（POST vs GET），且请求/响应结构完全独立——前者用于**写入**限流策略，后者用于**读取**当前配额状态。二者不可混淆使用。

## 使用方式

- **发现模型**：调用 `GET /api/v1/models` 查询全部或按条件筛选模型，推荐使用 HTTP API（非 SDK）以支持 `capabilities`、`features` 等高级筛选参数。  
- **授权模型**：先调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZABLE` 获取可授权列表，再通过 `POST /api/v1/models/permissions` 设置 `inference`/`finetune`/`deploy` 权限；支持逐模型授权或 `access_all_entities=OPEN` 一键授权。详情见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。  
- **配置限流**：使用 `POST /api/v1/models/limits` 设置业务空间内单个或多个模型的 QPM/TPM 配额；使用 `GET /api/v1/models/limits` 查看当前生效的账号级与业务空间级限额。  
- **检查权限与配额**：生产环境建议在调用模型前，先查询 `/models/permissions` 确认 `inference: true`，并调用 `/models/limits` 验证剩余配额，避免因权限缺失或超限导致 403/429 错误。

## 限制和注意事项

- 单次限流更新请求最多支持 200 个模型（文档 2），单次限额查询最多返回 200 条记录（文档 4），分页参数 `page_size` 最大值为 200。  
- Python SDK 的 `client.models.list()` 方法**仅支持 `page_no`、`page_size` 和 `provider` 参数**，不支持 `capabilities`、`features` 等筛选条件；如需精准过滤，请直接调用 HTTP API（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)）。  
- TPM（[Token](../concepts/token.md) 用量限流）与 RPM（请求频次限流）存在强依赖：若当前模型无 QPM 限制，则无法单独设置 TPM（错误码 `InvalidParameter`）。豁免 TPM 时，需先 `DELETE` 全部限流，再仅设置 `request_limit`（文档 2 中“TPM 豁免场景”说明）。  
- `access_all_entities=OPEN` 为全局推理授权，覆盖后续新增模型；但微调（`finetune`）与部署（`deploy`）权限**不支持一键开通**，必须显式逐模型设置。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


