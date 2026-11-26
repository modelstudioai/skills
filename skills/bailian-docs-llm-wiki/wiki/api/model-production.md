# model production

`model production` 指在百炼平台上将训练/调优后的模型转化为可稳定、可扩展、可管理的在线推理服务的完整流程，涵盖模型导入、微调、压缩、部署、吞吐预留与智能路由等核心能力。该流程面向开发者提供标准化 API 接口，支持文本、图像、视频、语音等多模态模型的全生命周期生产化。

## 支持的模型/功能

- **模型类型**：支持文本生成（如 `qwen3.8-flash`）、图像生成（如 `wan2.7-image-pro`）、视频生成（如 `wan2.7-i2v`）、语音合成（如 `cosyvoice-v3-flash`）四大类模型的微调、部署与管理。
- **核心功能链路**：
  - **模型调优**：通过 `POST /api/v1/fine-tunes` 创建 SFT/CPT/DPO/LoRA 等类型训练任务，支持文本、图像、视频、语音四类任务 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)；
  - **模型导入**：将 OSS 中的全参或 LoRA 调优模型文件导入平台，仅限北京地域 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)；
  - **模型压缩**：对自定义全参调优模型执行量化压缩，降低显存与推理成本，当前仅支持 `qwen3.5-flash-2026-02-23` 和 `qwen3.6-plus-2026-04-02` 基础模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)；
  - **模型部署**：统一使用 `/api/v1/deployments` 接口，通过 `plan` 参数区分部署模式（`mu`/`lora`/`dtu`/`mr`），支持文本、图像、视频、语音全类型；
  - **吞吐预留（DTU）**：为关键模型预购独占 GPU 容量，保障低延迟与高稳定性，通过专属 `deployed_model` code 管理容量实例 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)；
  - **智能路由（MR）**：基于策略（如 `EFFECT_FIRST`）动态调度请求至多个备选模型，仅支持北京与新加坡地域，且仅后付费 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。

> **注意**：文档 17（文本生成-部署模型）称 DTU 部署“支持华北2（北京）”，而文档 23（模型部署 API 参考）明确指出“DTU 部署需使用业务空间专属域名（如 `ws-vxxx.cn-beijing.maas.aliyuncs.com`）和该业务空间的 API Key”，二者不矛盾；但文档 19（图像生成-部署模型）和文档 22（视频生成-部署模型）均声明“当前模型部署 API 仅在华北2（北京）地域开放”，而文档 23 同时说明“新加坡地域使用 `dashscope-intl.aliyuncs.com`”，表明部署 API 在新加坡亦可用——此处存在地域支持范围表述不一致，以文档 23 的接口概览为准。

## 关键参数

| 参数 | 位置 | 类型 | 必选 | 说明 |
|------|------|------|------|------|
| `plan` | 请求体 | string | 是 | 部署模式标识：`mu`（模型单元）、`lora`（LoRA 共享）、`dtu`（独占吞吐）、`mr`（智能路由）；不同 plan 对应不同计费方式与参数集 |
| `model_name` | 请求体 | string | 是 | 待部署模型 ID，非基础模型名；来自调优任务响应的 `output.finetuned_output` 或导入任务的 `output.model_name` |
| `capacity` | 请求体 | integer | 是（除 `dtu` 外） | 实例数量（`mu`/`lora`/`cu`）；`dtu` 模式下由 `sku_code` + `template_code` + `quantity` 组合定义容量 |
| `deploy_spec` | 请求体 | string | 是（语音合成） | CosyVoice 部署必需，如 `MU5` 或 `MU2`，决定 `capacity` 的倍数约束 |
| `aigc_config` | 请求体 | object | 是（视频生成） | 包含 `use_input_prompt`、`prompt` 等提示词模板控制字段，影响调用时 prompt 行为 |
| `route_model_version` | 请求体 | string | 是（智能路由） | 从 `/api/v1/deployments/model-routing/versions` 获取的路由版本标识，如 `model-router-20260908` |

## 使用方式

1. **准备阶段**：  
   - 获取对应地域的 API Key（北京用 `dashscope.aliyuncs.com`，新加坡用 `dashscope-intl.aliyuncs.com`，DTU/MR 须用 `maas.aliyuncs.com` 业务空间域名）；  
   - 确认模型来源（`base` 或 `custom`），通过 `GET /api/v1/deployments/models?model_source=custom` 查询可部署模型列表 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。

2. **部署服务**：  
   - 文本/图像/视频：`POST /api/v1/deployments`，传 `plan=lora` + `model_name` + `capacity=1`；  
   - 语音合成（CosyVoice）：`POST /api/v1/deployments`，传 `plan=mu` + `deploy_spec=MU5` + `capacity=1`；  
   - DTU：使用业务空间域名，`plan=dtu`，并指定 `sku_code` 与 `template_code`（需先查 `/models?plan=dtu`）；  
   - 智能路由：`plan=mr`，且必须在请求体中包含 `route_model_version` 与 `candidate_models`。

3. **状态确认与调用**：  
   - 轮询 `GET /api/v1/deployments/{deployed_model}`，直到 `output.status == "RUNNING"`；  
   - 部署成功后，`output.deployed_model` 即为模型调用的 `model` 参数值。

## 限制和注意事项

- **地域限制**：  
  - 模型导入、模型压缩、所有微调任务（文本/图像/视频/语音）**仅在北京地域（`cn-beijing`）可用**；  
  - 智能路由 API **仅支持北京与新加坡地域**；  
  - DTU 部署必须使用业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`），不可使用 `dashscope.aliyuncs.com`。

- **权限与配置**：  
  - 子账号（RAM 用户）需显式授予 `AliyunBailianFullAccess` 或最小化权限策略；  
  - 所有 POST 请求必须携带 `Content-Type: application/json` 与 `Authorization: Bearer <api-key>`；  
  - HTTP 200 不代表操作成功：吞吐预留等异步操作需检查 `output.operation_status` 字段，否则可能误用未生效容量 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

- **模型兼容性**：  
  - 模型压缩**仅支持全参调优模型**，且基础模型严格限定为 `qwen3.5-flash-2026-02-23` 或 `qwen3.6-plus-2026-04-02`，LoRA 模型不支持；  
  - CosyVoice 语音合成模型**仅支持 `mu` 部署**，不支持 `lora` 或 `dtu`；  
  - 视频生成部署必需提供 `aigc_config`，且 `use_input_prompt=false` 时 `prompt` 为必填项。

- **计费差异**：  
  - DTU 为预付费（`charge_type="pre_paid"`），续费与自动续费变更**仅支持控制台操作**，API 不支持；  
  - 智能路由与 `mu`/`lora` 部署均为后付费（`charge_type="post_paid"`）。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)


