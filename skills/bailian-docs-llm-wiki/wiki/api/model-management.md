# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控模型的全生命周期操作。通过统一的 REST API 接口，开发者可程序化地查询可用模型列表、获取模型配额与权限状态、动态调整限流策略及开通/关闭模型调用权限。所有操作均基于业务空间（Workspace）粒度，支持多地域部署与细粒度权限控制。

## 支持的模型/功能

百炼平台支持多源模型接入，涵盖文本生成（TG）、深度思考（Reasoning）、视觉理解（VU）、图片/视频生成（IG/VG）、语音识别（ASR）、TTS、3D 生成等能力。模型来源包括 `qwen`（阿里巴巴-千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商；推理服务由 `aliyun-bailian`、`siliconflow`、`moonshot` 等多家服务商提供。模型特性（`features`）支持 `function-calling`、`structured-outputs`、`web-search`、`cache`、`batch`、`fine-tuning` 等，具体能力需以 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口返回的 `capabilities` 和 `features` 字段为准。

> **注意**：文档 1 中列出的 `inference_providers` 包含 `alibaba-cloud-modelstudio`，但该值在实际 API 响应中未被观测到，且 Model Studio 已于 2024 年底完成服务迁移，建议以 `aliyun-bailian` 作为默认推理供应商，详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `model` | String | 模型 ID（如 `qwen3.8-max`），用于精确查询、限流、授权等操作 | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `providers` / `inference_providers` | Array[String] | 按作者或推理服务商筛选模型，客户端 SDK 仅对当前页生效 | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `capabilities` / `features` | Array[String] | 模型能力与特性标识，必须通过 HTTP API 查询，SDK 不透传 | [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) |
| `request_limit` / `usage_limit` | Number | QPM（每分钟请求数）与 TPM（每分钟 Token 用量），单位秒级周期需显式指定 `*_period` | [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md) |
| `authorization_scope` | String | `AUTHORIZABLE`（可授权）或 `AUTHORIZED`（已授权），控制 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 返回范围 | [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) |

## 使用方式

### 1. 发现模型  
调用 `GET /api/v1/models` 获取模型列表，支持按名称模糊搜索（`name=qwen`）、ID 精确查询（`model=qwen3.8-max`）、能力筛选（`capabilities=TG&capabilities=Reasoning`）等。推荐使用 Python SDK 的 `client.models.list()` 方法，自动处理分页与字段映射。

### 2. 查询权限与限额  
- 权限：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 查看当前业务空间已开通推理权限的模型；  
- 限额：`GET /api/v1/models/limits?model=qwen3.8-max` 获取账号级与业务空间级 QPM/TPM 配置。  

### 3. 授权与限流变更  
- **授权**：`POST /api/v1/models/permissions` 支持逐模型设置 `inference`/`finetune`/`deploy` 权限，或通过 `access_all_entities=OPEN` 一键授权全部推理模型；  
- **限流**：`POST /api/v1/models/limits` 支持 `OVERLAY`（合并覆盖）与 `DELETE`（清空）两种操作类型。若需“仅限 QPM、不限 TPM”，须先 `DELETE` 再 `OVERLAY` 设置 `request_limit`，详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

> **注意**：文档 3 中示例请求地址误写为 `https://dashscope.aliyuncs.com/...`，实际应替换 `{WorkspaceId}` 并匹配地域 Endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`），否则将返回 404 或鉴权失败，详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且未设置时默认继承账号级配置；  
- **权限生效延迟**：模型授权变更后，通常在 30 秒内全局生效，但缓存可能导致首次调用短暂失败；  
- **批量操作限制**：`update-model-rate-limits` 接口 `models` 数组最多 200 项，`update-model-permissions` 最多 20 项；  
- **异步任务限制**：部分模型（如 `wan2.6-i2v-flash`）额外限制 `async_user_queue_limit` 与 `async_user_concurrency_limit`，需在 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 响应中检查；  
- **模型下线预警**：响应中 `inference_offline_info.offline_time` 字段标明预计下线时间，建议定期轮询并制定降级预案。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


