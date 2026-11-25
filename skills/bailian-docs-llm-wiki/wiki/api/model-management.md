# model management

模型管理是百炼平台的核心能力之一，提供模型发现、权限控制、限流配置与使用监控等全生命周期管理功能。开发者可通过统一 API 接口查询可用模型、设置调用配额、授权模型访问权限，并获取模型能力、定价与上下文限制等关键元数据。所有操作均基于业务空间（Workspace）隔离，支持多地域部署与细粒度策略控制。

## 支持的模型与功能

百炼平台聚合了来自阿里巴巴（千问、万相、HappyHorse 等）、智谱AI、MiniMax、月之暗面、DeepSeek、Kling、Vidu、PixVerse、Tripo、小米等多家厂商的模型，覆盖文本生成（TG）、深度思考（Reasoning）、视觉理解（VU）、图片/视频/3D 生成（IG/VG/3D-generation）、语音识别与合成（ASR/TTS）、多模态向量（ME）、实时全模态（Realtime-Omni）等能力。模型按 `provider`（作者）和 `inference_provider`（推理服务供应商）双重标识，支持通过 `capabilities`、`features`（如 `function-calling`、`structured-outputs`、`web-search`）、`service_site`（部署区域）等参数精准筛选。详细模型列表及能力说明请参见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **通用筛选** | `model` / `name` | 模型 ID 精确匹配 / 名称模糊搜索 | `"qwen3.8-max"`, `"qwen"` |
| **能力过滤** | `capabilities` | 按模型能力筛选（需 HTTP API） | `["Reasoning", "VU"]` |
| **特性过滤** | `features` | 按功能特性筛选（如结构化输出） | `["function-calling", "cache"]` |
| **部署约束** | `service_site` | 指定部署区域（中国、欧盟、美国等） | `"asia-pacific-china"`, `"european-union"` |
| **权限控制** | `authorization_scope` | 查询可授权（`AUTHORIZABLE`）或已授权（`AUTHORIZED`）模型 | `"AUTHORIZED"` |
| **限流配置** | `request_limit` / `usage_limit` | QPM（每分钟请求数）/ TPM（每分钟 Token 用量）上限 | `60`, `100000` |

> **注意**：文档 3 中 `update-model-rate-limits.md` 的示例请求地址为 `https://dashscope.aliyuncs.com/api/v1/models/limits`，但其他文档（如 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)）明确要求将 `{WorkspaceId}` 替换为实际业务空间 ID 并拼接地域域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits`）。生产环境必须使用带 WorkspaceId 的完整 Endpoint，否则请求将失败。

## 使用方式

### 1. 查询模型元信息  
调用 `GET /api/v1/models` 获取模型列表，支持分页（`page_no`/`page_size`）与多维筛选。推荐优先使用 Python SDK：  
```python
from dashscope import Client
client = Client(api_key=os.getenv('DASHSCOPE_API_KEY'), 
                base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1")
resp = client.models.list(model="qwen3.8-max")  # 精确查单个模型
```

### 2. 管理模型权限  
- 查询已授权模型：`GET /api/v1/models/permissions?authorization_scope=AUTHORIZED`  
- 授权单个模型：`POST /api/v1/models/permissions` 传 `{"models": [{"model": "qwen-plus", "inference": true}]}`  
- 一键授权全部推理模型：`POST /api/v1/models/permissions` 传 `{"access_all_entities": "OPEN"}`  
详情见 [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)。

### 3. 配置调用限流  
- 查询当前限流：`GET /api/v1/models/limits?model=qwen3.8-max`  
- 更新限流（QPM+TPM）：`POST /api/v1/models/limits` 传 `{"models": [{"model": "qwen-plus", "request_limit": 60, "usage_limit": 100000, "request_limit_period": 60, "usage_limit_period": 60}]}`  
- **删除限流**：需显式指定 `"operation_type": "DELETE"`，且不可仅传空字段（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且未设置 `workspace_limit` 时默认继承 `model_limit`。  
- **TPM 豁免**：若仅需限制 QPM 而不限制 TPM，必须分两步操作——先 `DELETE` 全部限流，再 `OVERLAY` 仅设 QPM；中间存在短暂无限制窗口，需评估风险。  
- **授权生效延迟**：模型授权变更后，新请求通常在 10 秒内生效，但缓存可能导致短时延迟。  
- **模型下线通知**：响应中 `inference_offline_info.offline_time` 字段标明预计下线时间，建议定期轮询并监听该字段（见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 返回示例）。  
- **地域一致性**：所有模型管理 API（列表、限额、权限）必须与模型调用 API 使用**相同地域 Endpoint**，跨地域调用将返回 `404` 或权限错误。

## 来源文档

- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


