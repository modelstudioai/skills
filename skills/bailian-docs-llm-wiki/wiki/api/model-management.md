# model management

模型管理是百炼平台的核心能力之一，提供对可用模型的发现、权限控制、限流配置等全生命周期操作。开发者可通过标准 REST API 查询模型元信息、设置调用配额、授权推理/微调/部署权限，并支持按模态、能力、供应商等多维度筛选。所有操作均需使用业务空间 ID 和有效的 API Key 进行认证。

## 支持的模型与功能

百炼平台支持数百种多模态模型，涵盖文本生成（TG）、视觉理解（VU）、图片生成（IG）、视频生成（VG）、语音识别（ASR）、3D 生成等能力，由 Qwen、Zhipu-AI、Wan、MiniMax 等十余家供应商提供。模型可按 `providers`（如 `qwen`）、`capabilities`（如 `TG` 或 `IG`）、`features`（如 `function-calling`、`structured-outputs`）等参数精确筛选。例如，查询所有 Qwen 系列文本生成模型需组合 `providers=qwen&capabilities=TG` [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。模型详情包含上下文长度（`context_window`）、输入/输出模态（`inference_metadata.request_modality` / `response_modality`）、定价结构（`prices`）及发布时间等关键元数据。

> **注意**：Python SDK 的 `client.models.list()` 方法**仅支持 `page_no`、`page_size` 和 `provider` 参数**，不支持 `capabilities`、`features` 等高级筛选条件；如需完整过滤能力，必须直接调用 HTTP API [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 关键参数

模型管理涉及两类核心参数体系：

- **限流参数**（用于 `/api/v1/models/limits`）：
  - `request_limit` + `request_limit_period`：请求频率限制（如 `60` 次/分钟 → `request_limit=60, request_limit_period=60`）；
  - `usage_limit` + `usage_limit_period`：用量限制（如 `100000` tokens/分钟 → `usage_limit=100000, usage_limit_period=60`）；
  - `async_user_queue_limit` / `async_user_concurrency_limit`：[异步任务](../concepts/asynchronous-task.md)排队与并发上限（仅部分模型支持）。

- **权限参数**（用于 `/api/v1/models/permissions`）：
  - `inference`：是否允许调用该模型进行推理；
  - `finetune`：是否允许对该模型执行微调；
  - `deploy`：是否允许部署该模型至专属环境；
  - `access_all_entities`：一键开关（`OPEN`/`CLOSE`），用于批量管理推理授权。

所有限流与权限操作均以**业务空间（Workspace）为作用域**，且限流值不可超过账号级默认上限。

## 使用方式

### 1. 发现模型
调用 `GET /api/v1/models` 查询可用模型列表，支持分页与多维筛选：
```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models?providers=qwen&capabilities=TG&page_no=1&page_size=50" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 2. 查询当前权限与限额
- 查看已授权模型：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`  
- 查看模型限额（含账号级与业务空间级）：`GET /api/v1/models/limits?model=qwen3.8-max`  
  详见 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)。

### 3. 配置权限与限流
- **更新权限**（POST `/api/v1/models/permissions`）：支持逐模型设置或一键授权（`access_all_entities=OPEN`）；
- **更新限流**（POST `/api/v1/models/limits`）：支持 `OVERLAY`（合并覆盖）或 `DELETE`（清空限流）操作。  
  > **注意**：若需“仅设 RPM、不限 TPM”，必须分两步调用：先 `DELETE` 全部限流，再 `OVERLAY` 仅设 `request_limit`；中间存在短暂无限制窗口 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

## 限制和注意事项

- **地域 Endpoint 差异**：除美国（弗吉尼亚）使用 `dashscope-us.aliyuncs.com` 外，其余地域均需拼接 `{WorkspaceId}` 到域名前缀（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。美国区域不支持 Workspace ID 拼接。
- **限流依赖关系**：设置 `usage_limit`（TPM）时，必须同时设置 `request_limit`（QPM）；否则返回 `InvalidParameter` 错误 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **权限继承规则**：`access_all_entities=OPEN` 授权后，新上架的推理模型将自动获得授权；但 `finetune` 和 `deploy` 权限**不适用一键模式**，必须显式逐模型配置。
- **配额生效延迟**：限流与权限变更通常在 10 秒内全局生效，但高并发场景下可能存在秒级延迟。
- **[异步任务](../concepts/asynchronous-task.md)限制**：`async_user_queue_limit` 和 `async_user_concurrency_limit` 仅对明确标注支持异步能力的模型（如 `wan2.6-i2v-flash`）有效，普通文本模型返回 `null`。

## 来源文档

- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)


