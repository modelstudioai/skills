# model production

`model production` 涵盖模型从训练、压缩、导入到部署上线的全生命周期管理能力，包括微调（Fine-tuning）、模型压缩（Quantization）、模型导入（Custom Model Import）及多种部署模式（DTU/MU/LoRA/智能路由）。所有能力均通过统一 OpenAPI 接口提供，面向开发者支持自动化集成与规模化运维。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务。各模态对应专属 API 文档，如[文本生成-创建调优任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)、[图像生成-创建调优任务](raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)等。  
- **模型压缩**：仅支持全参微调产出的自定义模型（如 `qwen3.5-flash-2026-02-23-ft-***`），不支持 LoRA 模型或已量化模型；当前仅开放量化一种压缩方式，详见[模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。  
- **模型导入**：支持从 OSS 导入全参或 LoRA 类型的调优模型，需提前完成 OSS 授权与文件上传，详见[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。  
- **部署模式**：  
  - `dtu`（独占吞吐）：预付费、按 TPM 购买容量，需使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）和对应 API Key；  
  - `mu`（模型单元）：后付费，适用于 CosyVoice 等对资源规格有强约束的模型；  
  - `lora`（LoRA 共享部署）：后付费、按 Token 计费，推荐用于 LoRA 微调模型；  
  - `mr`（智能路由）：后付费，仅支持华北2（北京）与新加坡地域，通过 `plan="mr"` 区分，其路由策略与备选模型版本需通过[智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)查询。

> **注意**：文档 16（文本生成-部署模型）称 DTU “是模型单元（MU）的继任方案”，但文档 24（模型部署 API 参考）明确说明 MU 与 DTU **并存且适用场景不同**，且 CosyVoice 部署强制要求 `plan="mu"`（见文档 23）。此处以文档 24 和 23 的实际约束为准，DTU 并非 MU 的替代，而是针对高 SLA 场景的补充方案。

## 关键参数

- **地域与域名**：所有 API 均严格绑定地域。华北2（北京）使用 `dashscope.aliyuncs.com`；新加坡使用 `dashscope-intl.aliyuncs.com`；DTU 和智能路由部署**必须**使用业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`），否则请求将失败。  
- **鉴权**：统一使用 `Authorization: Bearer <api-key>`，API Key 与地域强绑定，不可跨地域复用（见[吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)）。  
- **模型标识**：  
  - 微调产出模型取 `output.finetuned_output`（见文档 12）；  
  - 导入模型取 `output.model_name`（见文档 26）；  
  - 压缩产出模型取 `output.quantized_output`（见文档 25）。  
- **部署必填字段**：  
  - `model_name`（模型 ID）与 `plan`（部署类型）为所有部署接口共用必填项；  
  - DTU 部署额外必填 `sku_code`、`template_code`、`charge_type="pre_paid"` 及 `dtu_capacity` 对象；  
  - LoRA 部署需传 `capacity`（实例数，通常为 1）；  
  - CosyVoice 部署需传 `deploy_spec`（如 `MU5`）与 `capacity`（须为 `base_capacity` 整数倍）。

## 使用方式

1. **准备阶段**：确认地域、获取对应地域 API Key、开通必要权限（如 RAM 子账号需授予模型训练与部署权限）。  
2. **模型准备**：  
   - 微调：调用对应模态的 `POST /api/v1/fine-tunes`（如文档 5、7、9、11）；  
   - 压缩：先调用 `/api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs`（见文档 25）；  
   - 导入：`POST /api/v1/custom_models/import`（见文档 26）。  
3. **状态轮询**：所有异步任务（微调、压缩、导入、部署）均需轮询 `GET /api/v1/{resource}/{id}`（如 `/fine-tunes/{job_id}` 或 `/deployments/{deployed_model}`）直至 `status` 为 `SUCCEEDED` 或 `RUNNING`。  
4. **部署服务**：  
   - 使用上一步获得的模型 ID（`finetuned_output`/`model_name`/`quantized_output`）调用 `POST /api/v1/deployments`；  
   - 根据 `plan` 值填充对应参数（DTU 用 `sku_code`+`template_code`，LoRA 用 `capacity`，CosyVoice 用 `deploy_spec`）；  
   - 部署成功后，`output.deployed_model` 即为调用时使用的模型 code（见文档 22）。  

## 限制和注意事项

- **地域限制**：微调、压缩、导入、LoRA/MU 部署均**仅限华北2（北京）地域**；DTU 部署虽文档提及“支持华北2”，但其购买与扩缩容操作需在控制台完成（见文档 24），API 仅支持创建与状态查询；智能路由仅支持北京与新加坡（见文档 2）。  
- **HTTP 成功 ≠ 操作成功**：吞吐预留等容量操作返回 HTTP 200 仅代表请求被接收，**必须检查响应体中 `output.operation_status` 字段**（可能为 `PROCESSING`/`FAILED`），并主动轮询 `GET /.../operations/{id}` 确认终态（见[吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)）。  
- **模型兼容性**：  
  - 视频/图像生成微调任务中，`training_type` 固定为 `efficient_sft`（见文档 7、9），不支持 `sft`/`dpo`；  
  - CosyVoice 部署**不支持 `lora` plan**，必须使用 `mu`（见文档 23）；  
  - 智能路由服务创建时，`route_model_version` 必须来自 `/api/v1/deployments/model-routing/versions` 查询结果，且所选备选模型需已在当前工作空间开通调用权限（见文档 2）。  
- **计费提示**：`n_epochs`（文本/语音）、`max_steps`（图像）、`batch_size` 等超参数直接影响训练费用（见文档 5、7、9、11）；DTU 容量购买为预付费，续费与自动续费变更**仅支持控制台操作**（见文档 24）。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)


