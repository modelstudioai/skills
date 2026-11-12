# model production

`model production` 是百炼平台面向模型全生命周期管理的核心能力集合，覆盖从模型微调（Fine-tuning）、压缩（Compression）、导入（Import）到部署（Deployment）及吞吐预留（Throughput Reservation）的完整生产链路。所有操作均通过标准化 RESTful API 提供，支持文本、图像、视频、语音等多模态模型，适用于开发者构建高性能、可扩展的 AI 服务。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务。各模态对应专属 API，如文本生成使用 `/api/v1/fine-tunes` [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)，图像生成使用同路径但不同 `model` 和 `hyper_parameters` 配置 [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入平台，仅限华北2（北京）地域 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，不支持 LoRA 或已量化模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **部署方式**：支持多种计费与资源模型：
  - `mu`（模型单元）、`dtu`（独占吞吐）、`ptu_v2`（预置吞吐）、`lora`（LoRA 共享部署）；
  - DTU 仅支持预付费且需业务空间专属域名；PTU 支持北京与新加坡双地域；MU/LORA 当前仅限北京 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。
- **吞吐预留**：即原 TPM 预留，通过 `plan=ptu` 创建，支持 `ptu_fast`（高速）与 `ptu_default`（标速）两档性能，后者支持 8 小时时段预付费 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：文档 15（文本生成-部署模型）称 PTU 等部署方式支持“北京与新加坡”，而文档 18（视频生成-部署模型）、22（图像生成-部署模型）、21（语音合成-部署模型）均明确限定“仅在华北2（北京）地域开放”。实际部署能力以具体模态的部署文档为准——**视频、图像、语音三类模型的部署 API 目前仅在北京可用，不支持新加坡地域**。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model_name` | string | 是 | 基础模型 ID（微调时）或微调/导入产出的模型 ID（部署时）；非显示名 | `"qwen3-14b"`, `"wan2.7-i2v-ft-202511111122-xxxx"` |
| `plan` | string | 是 | 部署方案：`mu`/`dtu`/`ptu_v2`/`lora`/`cu`；不同模态支持范围不同 | `"lora"`, `"dtu"` |
| `training_type` | string | 是（微调） | 微调方法：文本支持 `sft`/`dpo_lora` 等；图像/视频/语音当前仅支持 `efficient_sft` | `"sft"`, `"efficient_sft"` |
| `hyper_parameters` | object | 是（微调） | 模型/任务强相关：文本需 `n_epochs`/`batch_size`/`max_length`；图像需 `max_steps`/`generation_type`；语音需分 `lm_*`/`fm_*` 子网络参数 | 见各模态文档 |
| `ptu_capacity` / `dtu_capacity` / `capacity` | object / integer | 是（部署） | 吞吐/实例数量配置：`ptu_capacity={input_tpm: 10000, output_tpm: 1000}`；`dtu_capacity` 同结构；`capacity` 为整数（如 `1`） | `{ "input_tpm": 10000 }`, `1` |
| `service_tier` | string | 否（PTU） | PTU 性能档位：`ptu_fast`（默认）或 `ptu_default` | `"ptu_default"` |

## 使用方式

1. **准备环境**：  
   - 获取并配置 API Key（仅限目标地域），如北京地域必须使用北京 API Key [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
   - 确认账号权限（RAM 用户需授予 `AliyunBailianFullAccess` 或最小化策略）；  
   - OSS 导入需提前完成 Bucket 授权与文件上传。

2. **微调流程（以文本为例）**：  
   ```bash
   # 1. 创建任务（北京地域）
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen3-14b",
           "training_type": "sft",
           "hyper_parameters": {
             "n_epochs": 3,
             "batch_size": 32,
             "max_length": 8192
           }
         }'
   # 2. 轮询状态（使用 job_id）
   curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   # 3. 成功后取 output.finetuned_output 部署
   ```

3. **部署流程（通用）**：  
   - 调用 `/api/v1/deployments`，传入 `model_name`、`plan` 及对应容量参数；  
   - 轮询 `/api/v1/deployments/{deployed_model}` 直至 `status == "RUNNING"` [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)；  
   - 使用 `output.deployed_model` 作为模型调用标识。

4. **吞吐预留（PTU）**：  
   - 使用 `POST /api/v1/deployments` + `plan=ptu` 创建；  
   - `ptu_capacity` 单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟）；  
   - 注意 HTTP 200 不代表操作成功，必须检查响应中 `output.operation_status` 字段 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

## 限制和注意事项

- **地域限制严格**：  
  - 微调（所有模态）、模型导入、模型压缩、视频/图像/语音部署 API **仅限华北2（北京）**；  
  - 文本部署、PTU 吞吐预留支持北京与新加坡；DTU 部署仅限北京（需业务空间专属域名）。

- **认证与域名**：  
  - API Key 与地域强绑定，不可跨地域复用；  
  - DTU 部署必须使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），不可用 `dashscope.aliyuncs.com`；  
  - 新加坡地域部署需使用 `dashscope-intl.aliyuncs.com`。

- **关键校验逻辑**：  
  - 所有异步操作（微调、部署、吞吐预留）返回 HTTP 200 仅代表请求接收成功，**必须检查响应体中的 `output.status` 或 `output.operation_status` 字段**；  
  - 微调任务需确认 `status == "SUCCEEDED"` 后再部署；部署任务需确认 `status == "RUNNING"` 后再调用；  
  - 吞吐预留创建后，需通过 [查询容量操作](../../raw/model-api-reference/model-production/throughput-reservation-api.md#operation-query) 获取最终结果。

- **模型与参数约束**：  
  - CosyVoice 语音微调仅支持 `cosyvoice-v3-flash` 基准模型；  
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参调优模型；  
  - `ptu_default` 标速支持 8 小时时段预付费，`ptu_fast` 高速不支持；  
  - `max_length`（文本）、`max_steps`（图像）、`n_epochs`（视频/语音）等参数直接影响训练费用与效果，需按文档推荐值谨慎设置。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)


