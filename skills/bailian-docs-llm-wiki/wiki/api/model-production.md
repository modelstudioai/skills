# model production

`model production` 指在百炼平台完成模型的微调（fine-tuning）、压缩、导入、部署及容量管理的全生命周期操作，覆盖文本、图像、视频、语音等多模态模型。核心流程为：训练（微调）→ 产出模型 → （可选）压缩或导入 → 部署为在线服务 → （可选）TPM 预留容量保障。所有生产环节均通过 OpenAPI 实现自动化集成，适用于开发者构建可扩展的 AI 应用服务。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成（[文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)）、图像生成（[图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)）、视频生成（[视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)）和语音合成（[语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)）四类任务。
- **模型压缩**：仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，以降低推理显存占用并提升吞吐，详见 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)。
- **模型导入**：支持将 OSS 中存储的全参（`full`）或 LoRA（`lora`）调优模型文件导入平台，导入成功后即可部署，详见 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型部署**：支持将微调产出、导入或压缩后的模型发布为在线 API 服务，覆盖文本、图像、视频、语音四类模型，统一使用 `/api/v1/deployments` 接口，但部署参数因模型类型而异。

> **注意**：文档中多次强调“仅在华北2（北京）地域可用”，包括全部微调任务创建（文档 2、7、10、12）、Checkpoint 管理（文档 15）、部署接口（文档 18、20、21、24）及部署管理（文档 23）。该地域限制是硬性要求，非配置项，跨地域调用将失败。

## 关键参数

| 功能 | 参数 | 说明 | 示例/约束 |
|------|------|------|-----------|
| **微调通用** | `model` | 基础模型 ID，必须为平台支持的基准模型 | `qwen3-14b`, `wan2.7-image-pro`, `cosyvoice-v3-flash` |
| | `training_type` | 微调方法 | 文本：`sft`, `dpo_lora`；图像/视频/语音：当前仅支持 `efficient_sft` |
| | `hyper_parameters` | 超参数对象，各模型支持字段不同 | 必填 `n_epochs`（文本）、`max_steps`（图像）、`n_epochs`（视频）、`lm_max_epoch`（语音）等 |
| **部署通用** | `model_name` | 待部署模型 ID，非基础模型名，而是微调产出的 `finetuned_output` 或导入生成的 `model_name` | `qwen3-14b-suffix-ft-202410291653-1c7f` |
| | `plan` | 部署方案 | `mu`（模型单元）、`lora`（LoRA 共享）、`ptu`（预置吞吐量）；语音合成仅支持 `mu`（见文档 24），图像/视频推荐 `lora`（见文档 20、21） |
| **部署（mu 方案）** | `deploy_spec` | 部署模板规格 | `MU1`, `MU2`, `MU5`；需通过 `/deployments/models` 接口获取有效值 |
| | `capacity` | 资源单元数量 | 必须为 `base_capacity` 的整数倍（如 `MU2` 要求 8 的倍数） |
| **部署（ptu 方案）** | `ptu_capacity.input_tpm` / `output_tpm` | 输入/输出吞吐量（单位：kTPM = 1000 [Token](../concepts/token.md)s/分钟） | 默认 `10000` / `1000`；扩缩容时传绝对值，非增量 |
| **部署（lora 方案）** | `capacity` | 实例数量 | 图像/视频部署中明确要求“推荐设置为1”（文档 20、21） |

## 使用方式

1. **微调训练**：  
   - 使用 `POST https://dashscope.aliyuncs.com/api/v1/fine-tunes` 提交任务（文档 2、7、10、12）。  
   - 通过 `GET /api/v1/fine-tunes/{job_id}` 轮询状态（文档 13），确认 `status=SUCCEEDED` 后获取 `finetuned_output`。  
   - 可选：调用 `/api/v1/fine-tunes/{job_id}/checkpoints` 获取中间 Checkpoint（文档 15）。

2. **模型导入/压缩**：  
   - 导入：`POST /api/v1/custom_models/import`（文档 5）；压缩：`POST /api/v1/fine-tunes/compress/jobs`（文档 6）。两者均需轮询任务状态至 `SUCCESSED` 或 `SUCCEEDED`。

3. **模型部署**：  
   - 统一调用 `POST https://dashscope.aliyuncs.com/api/v1/deployments`（文档 18、20、21、24）。  
   - 根据 `plan` 选择必填参数：`mu` 需 `deploy_spec` + `capacity`；`lora` 仅需 `capacity=1`；`ptu` 需 `ptu_capacity`。  
   - 部署后，用 `GET /api/v1/deployments/{deployed_model}` 查询状态，待 `status=RUNNING` 即可调用（文档 23）。

4. **TPM 预留（容量保障）**：  
   - 使用 `POST /api/v1/deployments`（同部署接口，但 `plan=ptu`）创建预留（文档 1）。  
   - 创建响应中的 `deployed_model` 即 ModelCode，用于后续调用；`instance_id` 和 `operation_id` 用于容量管理。

## 限制和注意事项

- **地域强绑定**：所有微调、部署、Checkpoint、导入、压缩 API **仅支持华北2（北京）地域**，且必须使用该地域的 API Key 和 Endpoint（`https://dashscope.aliyuncs.com`）。控制台操作亦需切换至北京地域（文档 2、7、10、12、13、15、18、20、21、23、24）。
- **HTTP 200 ≠ 操作成功**：TPM 预留等异步操作返回 HTTP 200 仅表示请求已接收，必须检查响应体中 `output.operation_status` 字段（如 `FAILED`）及错误码（文档 1）。
- **部署方案与模型强耦合**：  
  - CosyVoice 语音模型**仅支持 `mu` 部署**（文档 24），不支持 `lora` 或 `ptu`；  
  - 图像/视频模型**推荐 `lora` 部署**（文档 20、21），其 `capacity` 固定为 1；  
  - `ptu` 方案虽在部署接口中定义（文档 18），但实际用于 TPM 预留场景（文档 1），而非普通模型部署。
- **模型命名与后缀**：部署时若需多次部署同一模型，必须指定唯一 `suffix`（文档 18）；导入任务生成的 `model_name` 已含时间戳后缀（文档 5），避免冲突。
- **计费敏感参数**：`n_epochs`（文本/视频）、`max_steps`（图像）、`batch_size`、`max_length` 等超参数直接影响训练费用（文档 2、7、10、12），部署时 `capacity` 和 `ptu_capacity` 直接决定推理成本（文档 1、18）。

## 来源文档

- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)


