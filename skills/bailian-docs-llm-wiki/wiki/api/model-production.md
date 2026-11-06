# model production

`model production` 指在百炼平台上完成模型的定制化训练、压缩、部署与容量管理的端到端流程，覆盖从微调（Fine-tuning）到高可用推理服务上线的全生命周期。该能力支持文本、图像、视频、语音等多模态模型，并提供吞吐预留（PTU/DTU）、模型单元（MU）等多种部署模式，满足不同性能、成本与隔离性需求。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，均通过统一 `/api/v1/fine-tunes` 接口提交。各类型适用基准模型与超参结构差异显著，例如图像生成仅支持 `efficient_sft` 且需指定 `generation_type` 和 `max_pixels`，而语音合成需分别配置 LM/FM 双网络超参 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **模型导入**：支持将 OSS 中的全参或 LoRA 调优模型导入平台，仅限华北2（北京）地域 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，不支持 LoRA 或已量化模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **部署方式**：支持 `lora`（共享推理、按 token 计费）、`mu`（模型单元）、`dtu`（独占吞吐）、`ptu_v2`（预置吞吐）等多种 plan；其中 `dtu` 仅支持预付费且需使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），而 `lora` 在图像/视频生成中为推荐方案。

> **注意**：文档 16（文本生成部署）称 PTU 支持北京与新加坡，但文档 2（吞吐预留 API）明确指出 PTU 预留 API 的 Endpoint 为 `https://{workspaceId}.{region}.maas.aliyuncs.com`，且示例中仅列出北京与弗吉尼亚（`us-east-1`），未提新加坡。实际部署时请以控制台可选地域及 `GET /deployments/models?plan=ptu_v2` 接口返回结果为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model_name` | 请求体 | string | 是 | 微调任务中为基准模型 ID（如 `qwen3-14b`）；部署时为微调产出模型 ID（如 `qwen3-14b-ft-xxx`）或导入模型名。 |
| `training_type` | 请求体 | string | 是 | 微调方法：文本支持 `sft`/`dpo_full` 等；图像/视频/语音统一限定为 `efficient_sft`。 |
| `hyper_parameters` | 请求体 | object | 是（部分字段必填） | 含 `n_epochs`/`batch_size`/`max_length`（文本）、`max_steps`（图像）、`n_epochs`（视频）、`lm_max_epoch`+`fm_max_epoch`（语音）等，具体必填项依模型类型而异。 |
| `plan` | 请求体 | string | 是 | 部署方案：`lora`、`mu`、`dtu`、`ptu_v2` 等。语音合成部署强制要求 `plan="mu"` [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)。 |
| `ptu_capacity` / `dtu_capacity` | 请求体 | object | 是 | 吞吐容量配置对象，含 `input_tpm` 和 `output_tpm`（单位：kTPM），值需符合目标地域模型的最小值与步长限制。 |

## 使用方式

1. **微调训练**：  
   - 在华北2（北京）调用 `POST https://dashscope.aliyuncs.com/api/v1/fine-tunes` 提交任务；  
   - 通过 `GET /api/v1/fine-tunes/{job_id}` 查询状态，`status=SUCCEEDED` 后获取 `finetuned_output`；  
   - Checkpoint 可通过 `GET /api/v1/fine-tunes/{job_id}/checkpoints` 列举，`status=SUCCEEDED` 的 checkpoint 才可用于部署。

2. **模型部署**：  
   - 文本/图像/视频：使用 `POST /api/v1/deployments`，传入 `model_name`（来自微调输出）、`plan`（如 `lora`）、`capacity`（图像/视频推荐为 1）；  
   - 语音合成：必须用 `plan="mu"` + `deploy_spec`（如 `MU5`）+ `capacity`（需为 `base_capacity` 整数倍）；  
   - DTU 部署：需改用业务空间专属域名，传 `plan="dtu"`、`sku_code`、`template_code`，且 `charge_type` 固定为 `pre_paid`。

3. **吞吐预留（PTU）**：  
   - 调用 `POST /api/v1/deployments`（同部署接口路径，但语义为预留容量），指定 `model_name`、`plan="ptu"`、`service_tier`（`ptu_fast` 或 `ptu_default`）及 `ptu_capacity`；  
   - 创建成功后返回 `deployed_model`（即 ModelCode），后续调用模型时在请求头中传 `X-DashScope-Deployed-Model: {ModelCode}`。

4. **验证与调用**：  
   - 部署后轮询 `GET /api/v1/deployments/{deployed_model}`，待 `status=RUNNING` 即可调用；  
   - 吞吐预留服务调用时，Endpoint 与普通部署一致，但需显式携带 `X-DashScope-Deployed-Model` 头。

## 限制和注意事项

- **地域限制严格**：所有微调 API（文档 4/7/9/11）、模型导入（文档 6）、Checkpoint 管理（文档 14）、模型压缩（文档 26）均**仅限华北2（北京）**；部署 API 中，`mu`/`dtu` 仅支持北京，`ptu_v2` 支持北京与新加坡，但文档 18/20/22 明确图像/视频/语音部署仅开放北京——实际使用前务必确认控制台或 `GET /deployments/models` 返回的可用地域。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求被接收，必须检查响应体中 `output.operation_status` 字段是否为 `SUCCEEDED`，否则视为失败 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型与部署强绑定**：部署时 `model_name` 必须是微调/导入后生成的有效模型 ID（如 `qwen3-14b-ft-xxx`），不可直接使用基础模型名（如 `qwen3-14b`）；若部署失败，优先检查该 ID 是否存在于 `GET /deployments/models?model_source=custom` 响应中。
- **DTU 特殊要求**：DTU 部署必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）和对应 workspace 的 API Key，不可使用 `dashscope.aliyuncs.com`；续费与自动续费变更仅支持控制台操作，API 不支持 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
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
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)


