# model production

`model production` 指在百炼平台上完成模型的微调、压缩、部署与容量管理的端到端生产流程，覆盖从定制化训练到高可用推理服务上线的全生命周期。该流程以 API 驱动为主，支持文本、图像、视频、语音等多模态模型，核心能力包括细粒度微调（SFT/DPO/LoRA）、量化压缩、多种部署模式（MU/DTU/PTU/Lora）及吞吐预留管理。

## 支持的模型与功能

- **微调支持**：文本生成（Qwen 系列）、图像生成（Wan2.7/Qwen-Image）、视频生成（Wan2.x-i2v/kf2v）、语音合成（CosyVoice-v3-flash），均需在**华北2（北京）地域**调用 API [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。  
- **部署支持**：文本、图像、视频、语音四类模型均可部署；其中文本与语音支持 MU/DTU/PTU/Lora 多种 `plan`，图像与视频当前仅支持 `lora` 部署方式（见[图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)）；DTU 部署需使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），不可使用 `dashscope.aliyuncs.com` [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。  
- **模型压缩**：仅支持华北2（北京）地域，且**仅限全参微调产出的自定义模型**（如 `qwen3.5-flash-2026-02-23-ft-***`），不支持 LoRA 模型或基础模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。  
- **吞吐预留（PTU）**：支持预置吞吐量（PTU）和高速吞吐（PTU Fast）两种性能档位，适用于文本生成类模型的稳定推理场景 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：文档 14（文本生成-部署模型）称 PTU 支持“北京与新加坡”，但文档 22（模型部署 API 参考）明确指出“PTU 等部署方式支持北京与新加坡”，而文档 16/18/20（图像/视频/语音部署）均限定为“仅华北2（北京）”。经交叉验证，**PTU 部署能力确已扩展至新加坡地域，但图像/视频/语音类模型的部署 API 尚未开放该地域支持**，开发者需按模型类型分别确认地域兼容性。

## 关键参数

| 参数 | 所属环节 | 说明 | 示例值 |
|------|----------|------|--------|
| `training_type` | 微调 | 必填，指定微调方法。文本支持 `sft`/`dpo_full`/`efficient_sft`；图像/视频/语音当前仅支持 `efficient_sft` | `"sft"` |
| `n_epochs` / `max_steps` | 微调 | 文本用 `n_epochs`（循环次数），图像/视频用 `max_steps`（总步数）；直接影响训练时长与费用 | 文本：`3`；图像：`800` |
| `model_name` | 部署 | 必填，**非基础模型名，而是微调产出的 `finetuned_output` 或导入/压缩后的 `model_name`** | `"qwen3-14b-suffix-ft-202410291653-1c7f"` |
| `plan` | 部署 | 必填，部署计费模式：`mu`（模型单元）、`dtu`（独占吞吐）、`ptu_v2`（预置吞吐）、`lora`（LoRA 共享） | `"lora"` |
| `ptu_capacity` / `dtu_capacity` | 吞吐预留 / DTU | 容量配置对象，含 `input_tpm` 和 `output_tpm` 字段，单位均为每分钟 [Token](../concepts/token.md) 数 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `aigc_config` | 视频部署 | 视频生成专属必填对象，控制提示词来源与模板，`use_input_prompt=false` 时启用自动填充 | `{"use_input_prompt": false, "prompt": "根据图像内容..."}` |

## 使用方式

1. **微调**：调用 `POST /api/v1/fine-tunes`（北京地域），传入 `model`、`training_type`、`hyper_parameters` 及数据源（`training_file_ids` 或 `training_datasets`）。任务状态通过 `GET /api/v1/fine-tunes/{job_id}` 轮询，成功后获取 `output.finetuned_output`。  
2. **压缩（可选）**：对全参微调模型，先调用 `GET /api/v1/fine-tunes/compress/templates` 获取 `template_id`，再 `POST /api/v1/fine-tunes/compress/jobs` 创建任务，轮询 `GET /api/v1/fine-tunes/compress/jobs/{job_id}` 直至 `SUCCEEDED`，取 `output.quantized_output` 作为新模型 ID。  
3. **部署**：调用 `POST /api/v1/deployments`（北京或新加坡，依 `plan` 而定），传入 `model_name`、`plan` 及对应参数（如 `lora` 需 `capacity`；`dtu` 需 `sku_code`/`template_code`；`ptu_v2` 需 `ptu_capacity`）。部署状态通过 `GET /api/v1/deployments/{deployed_model}` 查询，`status=RUNNING` 表示就绪。  
4. **吞吐预留（PTU）**：调用 `POST /api/v1/deployments`（路径同部署，但语义为预留），传入 `model_name`、`plan="ptu"`、`service_tier`（`ptu_fast`/`ptu_default`）、`ptu_capacity` 及 `pre_paid_info`（预付费必填）。  

## 限制和注意事项

- **地域强约束**：所有微调 API（文本/图像/视频/语音）及模型压缩 API **仅限华北2（北京）**；部署 API 中，DTU/MU 仅支持北京，PTU 支持北京与新加坡，但图像/视频/语音部署目前**仅支持北京**。  
- **模型来源限制**：模型压缩仅接受百炼平台内全参微调产出的自定义模型，不支持 LoRA、基础模型或 OSS 导入模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)。  
- **HTTP 200 ≠ 操作成功**：吞吐预留、部署、微调等异步接口返回 HTTP 200 仅表示请求接收成功，**必须检查响应体中 `output.operation_status` 或 `output.status` 字段**（如 `SUCCEEDED`/`FAILED`），否则可能误用未就绪资源 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。  
- **DTU 域名与鉴权特殊性**：DTU 部署必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）和对应工作空间的 API Key，**不可使用 `dashscope.aliyuncs.com`**；且仅支持 `pre_paid`，续费操作需在控制台完成 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。  
- **部署标识唯一性**：`deployed_model`（部署标识）由系统生成，用于后续调用、扩缩容及查询，**不可自行构造或复用**；其格式与 `model_name` 无关，需严格以接口返回值为准。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)


