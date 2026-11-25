# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调、压缩、导入、部署、[智能路由](../concepts/model-routing.md)与吞吐预留等关键环节。所有能力均通过统一 OpenAPI 接口（`/api/v1/...`）提供，支持自动化集成与规模化管理。开发者需根据模型类型、地域限制和业务 SLA 要求选择对应能力组合。

## 支持的模型/功能

- **微调训练**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务。其中文本生成支持 `sft`/`cpt`/`dpo_full`/`dpo_lora` 等多种训练方式；图像/视频/语音生成当前仅支持 `efficient_sft`（LoRA 高效微调）[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型压缩**：仅支持对自定义全参调优模型（非 LoRA）进行量化压缩，基础模型限定为 `qwen3.5-flash-2026-02-23` 或 `qwen3.6-plus-2026-04-02` [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。
- **模型导入**：支持将 OSS 中存储的调优模型文件（`full` 或 `lora` 类型）导入平台，当前仅在北京地域开放 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **部署方式**：
  - `lora`：LoRA 模型共享部署（按 [Token](../concepts/token.md) 计费）；
  - `mu`：模型单元（后付费，北京/新加坡支持）；
  - `dtu`：独占吞吐（预付费，仅北京，需业务空间专属域名）；
  - `mr`：[智能路由](../concepts/model-routing.md)（后付费，北京/新加坡支持，复用 `/deployments` 接口，`plan="mr"`）[智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。
- **吞吐预留**：通过容量实例实现确定性 QPS 保障，支持扩缩容、续订、自动续费及溢出策略配置。

> **注意**：文档 15（文本生成-部署模型）称 DTU “新购独占部署优先选择”，而文档 26 明确指出“DTU 部署仅支持预付费（`charge_type="pre_paid"`），不支持后付费创建”，二者无矛盾；但文档 15 中“DTU 为预付费（按月）计费”与文档 26 中“DTU 部署仅支持预付费”一致，而文档 1 的[智能路由](../concepts/model-routing.md)明确要求 `charge_type="post_paid"`，三者计费模式逻辑自洽。

## 关键参数

| 参数 | 作用 | 示例值 | 说明 |
|------|------|--------|------|
| `plan` | 核心部署策略标识 | `"lora"`, `"mu"`, `"dtu"`, `"mr"` | 必填，决定计费模式、资源隔离级别与接口行为。`dtu` 和 `mr` 均复用 `/deployments` 接口，靠此字段区分。 |
| `model_name` | 待部署模型唯一 ID | `"qwen3-14b-suffix-ft-202410291653-1c7f"` | 非基础模型名，须为微调产出的 `finetuned_output` 或导入任务生成的 `model_name`。 |
| `capacity` | 实例数量或资源单元数 | `1`, `8` | 对 `lora`/`mu` 表示实例数；对 `dtu` 则由 `sku_code` + `template_code` 决定容量范围，不直接传此参数。 |
| `route_model_version` | 智能路由版本标识 | `"model-router-20260908"` | 创建/编辑 `mr` 服务时必填，需先调用 `/model-routing/versions` 查询可用版本。 |
| `training_type` | 微调方法 | `"sft"`, `"efficient_sft"`, `"dpo_lora"` | 文本生成支持多类型；图像/视频/语音生成当前仅支持 `"efficient_sft"`。 |

## 使用方式

1. **准备阶段**：  
   - 获取对应地域的 API Key（北京：`dashscope.aliyuncs.com`；新加坡：`dashscope-intl.aliyuncs.com`；DTU/mr 需用业务空间专属域名 `{WorkspaceId}.{region}.maas.aliyuncs.com`）；  
   - 确认权限：子账号需授予模型调用、训练、部署权限；  
   - 准备数据：训练集/验证集上传至 OSS 或通过 API 上传获取 `file_id`。

2. **微调与处理**：  
   - 调用 `POST /api/v1/fine-tunes` 创建训练任务（各模态共用同一 endpoint）；  
   - 用 `GET /api/v1/fine-tunes/{job_id}` 轮询状态，待 `status="SUCCEEDED"` 后提取 `finetuned_output`；  
   - （可选）对全参模型调用 `/api/v1/fine-tunes/compress/jobs` 进行量化；  
   - （可选）通过 `/api/v1/custom_models/import` 导入 OSS 模型。

3. **部署与发布**：  
   - 调用 `POST /api/v1/deployments`，按 `plan` 提交对应参数（如 `lora` 需 `capacity`，`dtu` 需 `sku_code`+`template_code`）；  
   - 用 `GET /api/v1/deployments/{deployed_model}` 轮询，`status="RUNNING"` 即可调用；  
   - 智能路由需先查 `/model-routing/versions`，再以 `plan="mr"` 创建并配置策略；  
   - 吞吐预留通过 `POST /api/v1/deployments`（`plan="tpm"`）创建，再叠加 `capacity-instances`。

> **注意**：文档 2（吞吐预留 API 参考）强调“HTTP 请求成功不等于容量操作成功”，必须轮询 `GET /operations/{id}` 检查 `output.operation_status` 是否为 `SUCCEEDED`，否则可能因资源不足等导致后台失败。

## 限制和注意事项

- **地域限制严格**：  
  - 微调（文本/图像/视频/语音）、模型导入、模型压缩、Checkpoint 管理、部署（除 DTU/mr 外）**仅限华北2（北京）**；  
  - DTU 部署需使用业务空间专属域名（如 `ws-vxxx.cn-beijing.maas.aliyuncs.com`），且仅北京支持；  
  - 智能路由（`mr`）与部分 `mu` 部署支持北京+新加坡；  
  - 吞吐预留 API 在弗吉尼亚等地域亦可用（见文档 2 域名说明）。

- **模型与部署约束**：  
  - CosyVoice 语音合成模型**仅支持 `mu` 部署**，不支持 `lora`（文档 21 明确）；  
  - LoRA 模型不可用于模型压缩（文档 24 明确要求“LoRA 模型和已量化的模型不支持”）；  
  - `dtu` 部署不支持 `AssumedRoleUser` 角色身份（文档 26）；  
  - 智能路由不支持跨地域模型混合调度（文档 1 未提，但地域绑定 API Key 已隐含此限制）。

- **操作可靠性**：  
  - 所有异步操作（微调、压缩、吞吐预留容量变更）**必须轮询终态**，不可仅依赖 HTTP 200；  
  - 部署耗时约 5–10 分钟（文档 22），期间需持续轮询状态；  
  - 删除操作（如删除部署、删除导入任务）不可逆，执行前请确认。

## 来源文档

- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)


