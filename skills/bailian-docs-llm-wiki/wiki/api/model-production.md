# model production

`model production` 是百炼平台中将训练/调优后的模型转化为可稳定、可扩展、可监控的在线推理服务的核心流程，涵盖模型微调（Fine-tuning）、模型压缩（Quantization）、模型导入（Custom Model Import）及模型部署（Deployment）四大环节。所有生产环节均通过统一的 RESTful API 管理，支持文本、图像、视频、语音等多模态模型，并强制要求在华北2（北京）地域调用。

## 支持的模型与功能

- **微调支持**：文本生成（Qwen 系列）、图像生成（Wan2.7 / Qwen-Image）、视频生成（Wan2.x-i2v/kf2v）、语音合成（CosyVoice-v3-flash），均需通过 `POST /api/v1/fine-tunes` 创建任务，详见[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **压缩支持**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，不支持 LoRA 模型或已量化模型，详见[模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)。
- **导入支持**：支持从 OSS 导入全参（`full`）或 LoRA（`lora`）调优模型，需提前完成百炼对 OSS Bucket 的授权，详见[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **部署支持**：所有模型类型均支持三种部署方案：按模型单元（`mu`）、LoRA 共享（`lora`）、预置吞吐量（`ptu`）。其中语音合成（CosyVoice）**仅支持 `mu` 方案**，而图像/视频生成推荐使用 `lora` 方案。

## 关键参数

| 参数 | 适用场景 | 必填性 | 说明 |
|--------|-----------|---------|------|
| `model_name` | 所有部署接口 | 是 | 必须为微调产出的 `finetuned_output` 或导入模型的 `model_name`，**不可直接使用基础模型名**（如 `qwen-plus`）；获取方式见各模型部署文档，例如[图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)。 |
| `plan` | 部署接口 | 是 | 取值为 `mu` / `lora` / `ptu`；`ptu` 方案下 `ptu_capacity` 为关键配置对象。 |
| `ptu_capacity` | `plan=ptu` 时 | 否（默认 `input_tpm=10000`, `output_tpm=1000`） | 单位为 kTPM（1000 Tokens/分钟），`input_tpm` 和 `output_tpm` 为绝对容量值，扩缩容时非增量变更，详见[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。 |
| `deploy_spec` & `capacity` | `plan=mu` 时 | 是 | `deploy_spec`（如 `MU1`/`MU5`）决定资源规格，`capacity` 必须为对应 `base_capacity` 的整数倍（如 `MU2` 要求 `capacity` 为 8 的倍数）。 |
| `aigc_config` | 视频生成部署 | 是（当 `plan=lora`） | 控制提示词行为：`use_input_prompt=false` 表示启用模板自动生成，此时 `prompt` 和 `lora_prompt_default` 为必填字段，详见[视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)。 |

> **注意**：文档 15（文本生成-部署模型）与文档 17（图像生成-部署模型）对 `capacity` 字段的必填性描述存在矛盾——前者未明确要求 `capacity`，后者明确标注“必选”。实际调用中，**所有 `plan=lora` 的部署（含图像、视频、语音）均需传 `capacity`，且推荐设为 `1`**；`plan=mu` 时 `capacity` 为必填。

## 使用方式

1. **准备模型**：  
   - 微调：调用 `/api/v1/fine-tunes` 创建任务，轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，提取 `output.finetuned_output`。  
   - 导入：调用 `/api/v1/custom_models/import` 提交 OSS 路径，轮询 `/api/v1/custom_models/{job_id}` 直至 `status=SUCCESSED`，提取 `output.model_name`。  
   - 压缩：先确保模型为 `qwen3.5-flash-2026-02-23` 全参调优结果，再调用 `/api/v1/fine-tunes/compress/jobs`，成功后取 `output.quantized_output`。

2. **部署服务**：  
   - 统一调用 `POST https://dashscope.aliyuncs.com/api/v1/deployments`，根据模型类型和业务需求选择 `plan`：  
     - 高并发、低延迟场景 → `ptu`（吞吐预留）或 `mu`（专属资源）；  
     - 成本敏感、中小规模调用 → `lora`（共享资源）；  
   - 部署后轮询 `GET /api/v1/deployments/{deployed_model}`，待 `status=RUNNING` 后即可调用。

3. **管理与扩缩容**：  
   - 查询状态、修改限流、扩缩容、删除部署均通过 [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md) 接口统一操作；  
   - 吞吐预留（PTU）的容量实例支持独立扩缩容、续订或释放，无需重建整个部署。

## 限制和注意事项

- **地域强约束**：所有微调、导入、部署、压缩 API **仅在华北2（北京）地域可用**，必须使用该地域的 API Key 和 Endpoint（`https://dashscope.aliyuncs.com`），跨地域调用将失败。  
- **模型兼容性**：`ptu` 方案仅支持部分基础模型（具体以控制台为准），且 `ptu_fast`（高速）不支持 8 小时时段付费周期，仅 `ptu_default`（标速）支持；`ptu_default` 的 `pricing_cycle=Hour` 且 `duration=8` 为唯一有效组合。  
- **状态校验关键性**：HTTP 200 不代表操作成功。例如吞吐预留创建接口返回 `output.operation_status=FAILED`，或部署接口返回 `status=FAILED`，均需检查 `error_code` 和 `message` 字段，严禁仅依赖 HTTP 状态码。  
- **计费起点**：模型部署成功（`status=RUNNING`）即开始计费，即使尚未发起任何推理请求；吞吐预留容量购买后立即计费，与是否调用无关。  
- **Checkpoint 管理**：调优任务产出的 Checkpoint 默认 15 天过期，需及时导出或部署；语音合成（CosyVoice）的 `step` 为 `LM_epoch × 10000 + FM_epoch`，排序按乘积降序，详见[Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


