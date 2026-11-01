# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、配额设置与限流配置等全生命周期管理功能。开发者可通过统一 API 接口查询可用模型列表、查看/更新模型授权状态、查询/调整模型调用限额，从而实现精细化的模型资源治理与服务编排。

## 支持的模型与功能

百炼平台支持多厂商、多模态、多能力的模型接入，涵盖文本生成（`TG`）、深度思考（`Reasoning`）、视觉理解（`VU`）、图片/视频生成（`IG`/`VG`）、语音识别与合成（`ASR`/`TTS`）、3D 生成（`3D-generation`）等能力。模型来源包括 `qwen`（通义千问）、`zhipu-ai`（智谱AI）、`moonshot-ai`（月之暗面）、`deepseek`、`kling`、`vidu` 等十余家供应商；推理服务由 `aliyun-bailian`（百炼原生）、`siliconflow`（硅基流动）、`mini-max` 等提供。所有模型均通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口统一暴露，并支持按 `capabilities`、`features`（如 `function-calling`、`structured-outputs`）、`providers` 等多维条件筛选。

> **注意**：Python SDK 的 `client.models.list()` 方法**仅支持 `page_no`、`page_size` 与 `provider` 参数**，不支持 `capabilities`、`features` 等高级筛选条件；如需精确过滤，必须使用 HTTP API 直接调用 —— 此限制在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中明确说明。

除基础调用外，部分模型还支持微调（`fine-tuning`）、部署（`deploy`）、批量推理（`batch`）、缓存（`cache`）等高级功能，具体能力见返回字段 `features` 和 `permissions.inference/fine_tune/deploy`。

## 关键参数

模型管理相关接口共用以下核心参数：

- **`model`（String）**：模型唯一 ID（如 `qwen3.8-max`），用于精确查询或授权操作，是所有写操作（授权、限流）的必填标识。
- **`page_no` / `page_size`（Integer）**：分页参数，适用于所有 GET 列表接口（`/models`、`/models/limits`、`/models/permissions`），默认 `page_no=1`、`page_size=20`。
- **`authorization_scope`（String）**：仅用于 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)，取值 `AUTHORIZABLE`（可授权列表）或 `AUTHORIZED`（已授权列表），默认为前者。
- **`operation_type`（String）**：仅用于 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)，取值 `OVERLAY`（合并覆盖）或 `DELETE`（删除限流），默认 `OVERLAY`。
- **`access_all_entities`（String）**：仅用于 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)，支持 `OPEN`（一键授权全部推理模型）、`CLOSE`（清空授权）或 `KEEP`（保持逐模型配置）。

## 使用方式

### 1. 发现模型  
调用 `GET /api/v1/models` 查询可用模型，推荐先按 `providers=qwen&capabilities=TG` 筛选主流文本模型，再结合 `features=function-calling` 等细化。示例：
```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models?providers=qwen&capabilities=TG&page_size=50" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 2. 管理授权  
- 查询已授权模型：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`  
- 授权单个模型：`POST /api/v1/models/permissions`，Body 中指定 `"models": [{"model":"qwen-plus","inference":true}]`  
- 一键授权全部推理模型：`POST /api/v1/models/permissions`，Body 中设 `"access_all_entities":"OPEN"`  

### 3. 配置限流  
- 查询当前限额：`GET /api/v1/models/limits?model=qwen3.8-max`  
- 设置 QPM=60 & TPM=100000：`POST /api/v1/models/limits`，Body 中传 `{"models":[{"model":"qwen3.8-max","request_limit":60,"request_limit_period":60,"usage_limit":100000,"usage_limit_period":60}]}`  
- 删除限流（豁免 TPM）：先 `DELETE` 再 `OVERLAY` 仅设 QPM —— 具体步骤见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。

## 限制和注意事项

- **权限隔离**：模型授权（`/models/permissions`）与限流配置（`/models/limits`）作用域均为**业务空间级别**，不同 Workspace 间互不影响。
- **限流依赖关系**：若需单独设置 TPM（用量限制），必须**先存在 QPM（请求限制）**，否则返回 `InvalidParameter` 错误；如需仅限 RPM 豁免 TPM，须采用两步法（先 DELETE 再 OVERLAY 设 QPM）—— 详见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)。
- **SDK 功能差异**：Python SDK 对模型管理的支持有限：`client.models.list()` 不支持高级筛选；`client.models.limits.list()` 和 `client.models.permissions.list()` 仅封装基础分页，复杂操作仍需 HTTP 调用。
- **地域 Endpoint 差异**：国际用户应使用 `dashscope-intl.aliyuncs.com` 或 `cn-hongkong.dashscope.aliyuncs.com` 等国际 Endpoint，而国内用户需替换 `{WorkspaceId}` 并使用 `maas.aliyuncs.com` 域名，不可混用。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


