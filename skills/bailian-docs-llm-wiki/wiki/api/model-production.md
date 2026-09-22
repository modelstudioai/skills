# model production

`model production` 指在百炼平台上将基础模型或自定义模型完成训练、压缩、导入、部署并投入生产调用的全生命周期管理能力，涵盖微调（fine-tuning）、模型导入（custom model import）、模型压缩（quantization）和专属部署（deployment）四大核心环节。所有操作均通过统一的 DashScope OpenAPI 接口实现，需使用华北2（北京）地域的 API Key 进行鉴权。

## 支持的模型/功能

- **微调支持多模态任务**：文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务均提供完整的微调 API，但**全部仅限华北2（北京）地域可用**，且必须使用该地域的 API Key [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)。
- **模型导入与压缩**：支持从 OSS 导入全参或 LoRA 微调模型，并通过量化压缩降低推理成本；当前模型压缩 API 也**仅在北京 Region 开放**，且仅支持 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)。
- **部署方式差异化适配**：
  - 文本生成支持 `mu`（模型单元）、`lora`（LoRA 共享）、`ptu`（预置吞吐量）三种部署方案；
  - 图像/视频生成推荐 `lora` 部署；
  - 语音合成（CosyVoice）**仅支持 `mu` 部署**，且必须指定 `MU5` 或 `MU2` 规格 [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)。

> **注意**：文档 17（图像生成-部署模型）与文档 20（图像生成）均指出部署 API 仅限华北2（北京），但文档 13（[模型部署](../concepts/model-deployment.md)）未限定地域，属信息缺失；以具体子任务文档为准，即所有部署接口实际仅支持北京地域。

## 关键参数

| 参数 | 所属场景 | 必填性 | 说明 |
|------|----------|--------|------|
| `model_name` | 微调、部署、导入 | 是 | 微调时为基准模型 ID（如 `qwen3-14b`）；部署时为微调产出的 `finetuned_output` 或导入模型的 `model_name`；导入时为基础模型名（如 `qwen3-32b`）。 |
| `training_type` | 微调 | 是 | 文本生成支持 `sft`/`dpo_lora` 等；图像/视频/语音生成当前**仅支持 `efficient_sft`**。 |
| `plan` | 部署 | 是 | 决定计费与资源模型：`mu`（专属资源）、`lora`（共享资源、按 token 计费）、`ptu`（预置吞吐量）。 |
| `ptu_capacity` | `ptu` 部署 | 否（默认值生效） | 包含 `input_tpm` 和 `output_tpm`（单位：kTPM），不填则默认 `10000` / `1000`。详见[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。 |
| `deploy_spec` & `capacity` | `mu` 部署 | 是（`mu` 场景） | `deploy_spec` 如 `MU1`/`MU5`；`capacity` 需为对应规格的 `base_capacity` 整数倍（如 `MU2` 要求为 8 的倍数）。 |

## 使用方式

1. **准备阶段**：  
   - 在华北2（北京）地域获取并配置 API Key；  
   - 确保 RAM 子账号已授予 `AliyunBailianFullAccess` 或最小化权限策略 [权限管理概述](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)；  
   - 微调需准备符合格式的数据集（OSS 挂载或 API 上传）；导入需完成 OSS Bucket 授权及文件上传。

2. **核心流程（典型路径）**：  
   ```mermaid
   graph LR
   A[创建微调任务] --> B[轮询查询任务状态]
   B -->|SUCCEEDED| C[获取 finetuned_output]
   C --> D[部署模型]
   D --> E[轮询部署状态至 RUNNING]
   E --> F[调用 deployed_model]
   ```
   - 微调任务创建后，必须轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status == "SUCCEEDED"`，再提取 `output.finetuned_output` 用于部署；  
   - 部署后需轮询 `/api/v1/deployments/{deployed_model}` 直至 `status == "RUNNING"`；  
   - 吞吐预留（PTU）部署需先调用 `/api/v1/deployments` 创建预留，再用返回的 `deployed_model` 调用模型。

3. **部署调用示例（文本生成，mu 方案）**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/deployments" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model_name": "qwen3-14b-ft-20241029",
           "plan": "mu",
           "deploy_spec": "MU1",
           "capacity": 2,
           "billing_method": "POST_PAY"
         }'
   ```

## 限制和注意事项

- **地域强约束**：微调、模型导入、模型压缩、所有类型模型的部署 API 均**仅支持华北2（北京）地域**，跨地域调用将失败。控制台操作不受此限，但 API 集成必须严格匹配地域。
- **HTTP 成功 ≠ 业务成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，**必须检查响应体中 `output.operation_status` 字段**（可能为 `FAILED`），否则可能导致容量未生效 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性限制**：  
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型，LoRA 模型和已量化模型不支持；  
  - CosyVoice 语音合成[模型部署](../concepts/model-deployment.md)**不支持 `lora` 或 `ptu` 方案**，必须使用 `mu` + `MU5`/`MU2`；  
  - `ptu_fast`（高速）不支持 8 小时时段预付费，仅 `ptu_default`（标速）支持。
- **资源与计费**：  
  - `mu` 部署在服务创建成功后立即开始计费，即使尚未调用；  
  - `n_epochs`、`max_steps`、`batch_size` 等超参数直接影响训练 [Token](../concepts/token.md) 消耗与费用，需按需设置 [训练计费说明](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


