# model production

`model production` 指在百炼平台完成模型的训练、压缩、部署与容量管理的端到端生产流程，覆盖从微调（Fine-tuning）、导入（Import）、压缩（Compression）到在线服务化（Deployment）及吞吐预留（Throughput Reservation）的全生命周期。该流程面向开发者提供标准化 API 接口，支持文本、图像、视频、语音等多模态模型的定制化生产。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成（[文本生成-创建调优任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)）、图像生成（[图像生成-创建调优任务](raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)）、视频生成（[视频生成-创建调优任务](raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)）和语音合成（[语音合成（CosyVoice）-创建调优任务](raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)）四类任务，均**仅限华北2（北京）地域**调用。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入平台（[模型导入](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)），导入后可部署为服务。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩（[模型压缩](raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)），以降低显存占用、提升推理吞吐；LoRA 模型和已量化模型不支持。
- **模型部署**：支持多种部署方式，包括 LoRA 共享部署（`plan=lora`）、模型单元（`mu`）、DTU 独占算力（`dtu`）和预置吞吐（`ptu_v2`/`ptu`）。其中 DTU 部署需使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），而 PTU 及通用部署支持北京与新加坡双地域（[模型部署 API 参考](raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)）。
- **吞吐预留（TPM Reservation）**：即 PTU 预留，用于为模型预购确定性推理容量，支持高速（`ptu_fast`）与标速（`ptu_default`）两种性能档位（[吞吐预留 API参考](raw/model-api-reference/model-production/throughput-reservation-api.md)）。

> **注意**：文档 16（文本生成-部署模型）称 PTU 部署支持“北京与新加坡”，而文档 18（图像生成-部署模型）和文档 20（视频生成-部署模型）明确声明其部署 API “仅在华北2（北京）地域开放”。经交叉验证，**PTU 部署能力确已扩展至新加坡**，但图像/视频/语音类部署接口尚未同步开放该地域支持——开发者若需在新加坡部署图像/视频模型，须先通过北京地域完成微调与导出，再将产出模型 ID 传入新加坡地域的通用部署接口（`plan=ptu_v2` 或 `plan=lora`），前提是该模型已在新加坡地域完成注册（可通过 `GET /api/v1/deployments/models?model_source=custom&region=ap-southeast-1` 查询）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model_name` | string | 是 | 待部署/微调的模型标识。微调时为基准模型 ID（如 `qwen3-14b`）；部署时为微调产出 ID（如 `qwen3-14b-ft-xxx`）或导入模型名。 | `"qwen3-14b"` |
| `plan` | string | 是 | 部署方案。取值：`lora`（LoRA 共享）、`mu`（模型单元）、`dtu`（独占算力）、`ptu_v2`（预置吞吐 V2）、`ptu`（吞吐预留旧版别名）。语音合成模型强制为 `mu`（见 [语音合成-部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)）。 | `"lora"` |
| `training_type` | string | 是（微调） | 微调方法。文本支持 `sft`/`dpo_lora` 等；图像/视频/语音统一为 `efficient_sft`（LoRA）。 | `"efficient_sft"` |
| `hyper_parameters` | object | 是（微调） | 超参数对象。各模型必填字段不同：文本需 `n_epochs`/`batch_size`/`max_length`；图像需 `max_steps`/`learning_rate`；视频需 `n_epochs`/`learning_rate`；语音需 `lm_max_epoch`/`fm_max_epoch` 等双网络参数（见 [语音合成（CosyVoice）-创建调优任务](raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)）。 | `{"n_epochs": 3, "batch_size": 32}` |
| `ptu_capacity` / `dtu_capacity` / `capacity` | object / integer | 是（对应 plan） | 容量配置。`ptu_capacity` 含 `input_tpm`/`output_tpm`（单位 kTPM）；`dtu_capacity` 同样含二者；`capacity`（如 `lora`/`mu`）为整数实例数（推荐 1）。 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `aigc_config` | object | 是（视频部署） | 视频生成专用提示词配置，含 `use_input_prompt`、`prompt` 和 `lora_prompt_default`，控制生成时的 prompt 来源与模板（见 [视频生成-部署模型](raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)）。 | `{"use_input_prompt": false, "prompt": "根据图像内容..."}` |

## 使用方式

1. **微调训练**：  
   - 调用 `POST /api/v1/fine-tunes` 创建任务（如 [文本生成-创建调优任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)），传入 `model`、`training_type` 和 `hyper_parameters`。  
   - 轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，获取 `finetuned_output`（即模型 ID）。

2. **模型导入/压缩（可选）**：  
   - 导入：调用 `POST /api/v1/custom_models/import` 提交 OSS 模型路径（[模型导入](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)）。  
   - 压缩：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建量化任务（[模型压缩](raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)）。

3. **部署服务**：  
   - 调用 `POST /api/v1/deployments`，根据 `plan` 传入对应参数：  
     - `lora`/`mu`：传 `model_name`、`plan`、`capacity`；  
     - `dtu`：传 `model_name`、`plan="dtu"`、`sku_code`、`template_code`、`dtu_capacity`，**必须使用业务空间域名**；  
     - `ptu`：传 `model_name`、`plan="ptu"`、`service_tier`、`ptu_capacity` 等（见 [吞吐预留 API参考](raw/model-api-reference/model-production/throughput-reservation-api.md)）。  
   - 轮询 `GET /api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`（[部署模型管理](raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)）。

4. **调用服务**：  
   - 使用 `deployed_model`（即 `output.deployed_model`）作为 `model` 参数，向对应模型推理 API 发起请求（如 `/api/v1/services/aigc/text-generation`）。

## 限制和注意事项

- **地域限制严格**：所有微调（文本/图像/视频/语音）、模型导入、Checkpoint 管理、模型压缩接口**仅支持华北2（北京）地域**；部署接口中，`dtu` 和 `mu` 仅支持北京，`ptu_v2`/`ptu` 支持北京与新加坡，但图像/视频/语音的专用部署文档未开放新加坡，需按通用部署流程操作（见上文注意项）。
- **API Key 绑定地域**：API Key 与创建时的地域强绑定，不可跨地域复用（[吞吐预留 API参考](raw/model-api-reference/model-production/throughput-reservation-api.md)）。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，**必须检查响应体中的 `output.operation_status` 字段**（如 `SUCCEEDED`/`FAILED`），否则可能误用未生效的容量（[吞吐预留 API参考](raw/model-api-reference/model-production/throughput-reservation-api.md)）。
- **模型兼容性约束**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参调优模型，不支持 LoRA、其他基座或已量化模型（[模型压缩](raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)）；语音合成模型部署强制使用 `plan=mu`，且 `deploy_spec` 仅支持 `MU5` 或 `MU2`（[语音合成-部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)）。
- **部署等待时间**：模型部署通常需 **5～10 分钟** 才能进入 `RUNNING` 状态，期间需轮询状态接口（[部署模型管理](raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)）。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)


