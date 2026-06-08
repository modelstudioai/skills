# deploy dedicated services

阿里云百炼平台提供模型专属部署服务，允许开发者将平台预置模型或自定义微调模型部署为独立推理实例，获得专属算力资源与可控的吞吐、并发和延迟表现。该服务覆盖模型部署与模型导入两大 API 体系，支持多种计费模式和丰富的模型类型，适用于从原型验证到生产级推理的各类场景。

## 核心流程

专属部署涉及两个主要环节：

1. **模型导入**（可选）：将 OSS 上的自定义微调模型（LoRA 或全参）导入百炼平台，详见[模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)。
2. **模型部署**：对平台已有模型或导入后的模型创建部署实例，获取专属推理端点，详见[模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)。

所有接口均通过 HTTP 调用，基础地址为 `https://dashscope.aliyuncs.com/api/v1/`，需在请求头中携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`。

## 模型部署 API

### 查询可部署模型

```
GET /deployments/models?page_no=1&page_size=100
```

返回当前支持部署的模型列表，包含 `model_name`（模型名称）和 `base_capacity`（最小资源单元数）。分页参数 `page_size` 最大为 200。

### 创建部署任务

```
POST /deployments
```

根据所选计费模式设置不同的请求参数：

| 计费模式 | `plan` 值 | 适用场景 | 吞吐/并发可调 |
|---------|----------|---------|-------------|
| 按预置吞吐（PTU） | `ptu` | 稳定吞吐、高并发低延迟、流量可预估 | 否（平台预置） |
| 按模型单元计费 | `mu` | 大规模推理、资源专属、灵活调参 | 是（自定义） |
| 按 Token 用量计费 | `lora` | 高性价比、对并发延迟要求不高 | 否（平台预置） |
| 按算力单元计费 | 不设置 | 图片/视频生成模型 | 是（自定义） |

关键请求参数：

- `model_name`（必填）：待部署的模型 ID
- `capacity`（必填）：资源单元数量，须为 `base_capacity` 的整数倍
- `deploy_spec`：仅 `mu` 模式必填，如 `MU1`
- `enable_thinking`：部分模型可切换思考模式
- `max_context_length`：部分模型可配置最长上下文
- `rpm_limit` / `tpm_limit`：部分模型支持服务限流
- `suffix`：同一模型多次部署时需指定后缀以区分

> **注意**：部署任务创建成功即开始计费，即使尚未发送推理请求。按 Token 用量计费模式下 `capacity` 参数虽设置无效但必须填写。

### 部署状态

部署任务经历以下生命周期：`PENDING` → `RUNNING`（可服务）→ `STOPPED` / `DELETING` / `FAILED`。

## 模型导入 API

当需要部署自定义微调模型时，需先通过导入 API 将模型文件从 OSS 导入百炼平台。完整流程参见[模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)。

### 创建导入任务

```
POST /custom_models/import
```

关键参数：

- `model_name`：基础模型名称（如 `qwen3-32b`）
- `source`：当前仅支持 `oss`
- `weight_type`：`full`（全参微调）或 `lora`（LoRA 微调）
- `storage_info`：包含 `bucket_name` 和 `object_key`（须以 `/` 结尾）

### 导入任务管理

- **查询详情**：`GET /custom_models/import/{job_id}`
- **查询列表**：`GET /custom_models/import?page_no=1&page_size=10`，支持按 `status` 和 `model_name` 过滤
- **删除任务**：`DELETE /custom_models/import/{job_id}`，仅 `SUCCESSED` 或 `FAILED` 状态可删除

导入任务状态流转：`PENDING` → `RUNNING` → `SUCCESSED` / `FAILED`。

## 支持的模型

模型单元（MU）部署模式支持的模型覆盖多个类别，详细规格与定价见[模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)中的支持模型表：

- **文本生成**：千问系列（Qwen 3.6/3.5/3/2.5 等各尺寸）、GLM-5/4.7、DeepSeek-v4-Flash/v3.2、MiniMax-M2.5、Kimi-K2.5
- **多模态**：千问 VL 系列（视觉理解）、千问 Omni 系列（全模态）
- **语音合成**：CosyVoice-v3-Flash
- **Embedding/Rerank**：千问3-Embedding-0.6B、千问3-Rerank 系列

部分模型支持 PD 分离模式（Prefill-Decode 分离），可降低首 Token 延迟并提高吞吐。

## 注意事项

- 使用前需获取百炼 API-KEY 并熟悉模型部署基本流程
- 模型导入前须完成 OSS Bucket 创建和百炼平台的 OSS 授权
- 模型单元按小时或包月计费，不同 MU 规格（MU1-MU9）对应不同算力和价格
- 常见错误码包括 `InvalidParameter`（参数无效）、`NotFound`（资源不存在）、`OperationDenied`（操作被拒绝）、`InvalidApiKey`（密钥无效）

## 来源文档

- [模型部署API参考](../../raw/model-api-reference/deploy-dedicated-services/model-deployment-api.md)
- [模型导入API参考](../../raw/model-api-reference/deploy-dedicated-services/model-import-api-reference.md)



