# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调、导入、压缩、部署、吞吐预留与智能路由等核心环节。开发者可通过统一 OpenAPI 接口完成从定制化训练到高可用服务上线的完整链路，所有能力均按需付费、地域隔离、权限可控，适用于企业级 AI 应用规模化落地。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成（[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)）、图像生成（[图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)）、视频生成（[视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)）和语音合成（[语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)）四大模态。所有微调任务**仅在华北2（北京）地域开放**，且必须使用该地域的 API Key。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入百炼平台（[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)），导入成功后可直接部署。
- **模型压缩**：提供量化压缩能力，当前仅支持 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型（[模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)），不支持 LoRA 或已量化模型。
- **模型部署**：支持多种部署模式：`lora`（LoRA 共享部署，按 Token 计费）、`mu`（模型单元）、`dtu`（独占吞吐，预付费）、`ptu_v2`（预置吞吐量 V2）及 `mr`（智能路由）。其中 `dtu` 和 `mu` 仅支持北京地域；`ptu_v2` 和 `mr` 同时支持北京与新加坡地域。
- **吞吐预留**：通过 PTU（预置吞吐量）实现确定性推理性能保障，支持高速（`ptu_fast`）与标速（`ptu_default`）两种性能档位（[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)）。
- **智能路由**：基于效果或成本策略自动调度多个备选模型，仅支持后付费（`charge_type="post_paid"`），且**仅在北京与新加坡地域可用**（[智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)）。

> **注意**：文档 17（文本生成-部署模型）称“PTU 等部署方式支持北京与新加坡”，而文档 24（模型部署 API 参考）明确指出“预置吞吐（PTU）等部署方式支持北京与新加坡地域”，二者一致；但文档 20（图像生成-部署模型）和文档 21（语音合成-部署模型）均声明其部署 API “仅在华北2（北京）地域开放”。这表明 PTU 部署虽在两地可用，但图像/语音类模型的 PTU 部署能力尚未在新加坡开放，实际可用性以具体模型类型为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model_name` | string | 是 | 待部署/微调的模型 ID（非基础模型名），如微调产出的 `qwen3-14b-suffix-ft-202410291653-1c7f` 或导入模型名 | `"wan2.7-image-pro-ft-202507011122-xxxx"` |
| `plan` | string | 是 | 部署方案标识：`lora` / `mu` / `dtu` / `ptu_v2` / `mr` | `"lora"` |
| `charge_type` | string | 是 | 付费方式：`pre_paid`（预付费）或 `post_paid`（后付费）；`dtu` 固定为 `pre_paid`，`mr` 固定为 `post_paid` | `"post_paid"` |
| `capacity` | integer | 是（部分 plan） | 实例数量（`lora`/`mu`）或资源单元数（`mu`/`dtu`）；`lora` 推荐设为 `1` | `1` |
| `ptu_capacity` / `dtu_capacity` | object | 是（对应 plan） | 吞吐容量配置对象，含 `input_tpm` 和 `output_tpm` 字段 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `aigc_config` | object | 是（视频生成部署） | 视频生成专属提示词配置，含 `use_input_prompt`、`prompt`、`lora_prompt_default` | `{"use_input_prompt": false, "prompt": "根据图像内容..."}` |
| `training_type` | string | 是（微调） | 微调方法：`sft`/`dpo_full`/`efficient_sft` 等；各模态支持类型不同（如视频/语音仅支持 `efficient_sft`） | `"efficient_sft"` |

## 使用方式

1. **准备环境**：获取并配置华北2（北京）地域的 API Key（所有微调、导入、压缩、多数部署操作必需），确认工作空间已开通对应权限（如 `model:Deploy`、`model:Train`）。
2. **模型准备**：
   - 微调：调用 `/api/v1/fine-tunes` 创建任务（如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)），轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，提取 `finetuned_output`。
   - 导入：调用 `/api/v1/custom_models/import` 提交 OSS 模型路径（[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)），轮询状态至 `SUCCESSED`。
   - 压缩：先调用 `/api/v1/fine-tunes/compress/templates` 获取模板，再用 `/api/v1/fine-tunes/compress/jobs` 创建压缩任务（[模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)），成功后取 `quantized_output`。
3. **部署服务**：
   - 统一入口：`POST /api/v1/deployments`
   - 指定 `plan` 与对应必填参数（如 `lora` 需 `capacity`；`dtu` 需 `sku_code`、`template_code`、`dtu_capacity`；`mr` 需路由策略与备选模型列表）
   - 地域域名：北京用 `dashscope.aliyuncs.com`，新加坡用 `dashscope-intl.aliyuncs.com`；`dtu` 部署**必须使用业务空间专属域名**（如 `ws-vxxx.cn-beijing.maas.aliyuncs.com`）
4. **验证与调用**：调用 `/api/v1/deployments/{deployed_model}` 查询状态，待 `status=RUNNING` 后即可通过 `deployed_model` 标识调用推理 API。

## 限制和注意事项

- **地域强约束**：所有微调（文本/图像/视频/语音）、模型导入、模型压缩、`mu`/`lora` 部署**仅限华北2（北京）地域**；`ptu_v2` 和 `mr` 支持北京与新加坡，但具体模型支持情况需单独验证。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，**必须检查响应体中 `output.operation_status` 字段**（如 `FAILED`）及错误码（[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)）。
- **DTU 特殊要求**：`dtu` 部署需提前在控制台开通功能并申请资源额度；必须使用业务空间专属域名和对应 API Key；续费与自动续费变更**仅支持控制台操作**，API 不支持（[模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)）。
- **智能路由限制**：仅支持后付费；路由版本、策略与备选模型需通过 `/api/v1/deployments/model-routing/versions` 查询，且备选模型需已在当前工作空间获得调用授权，否则调用时被实时过滤。
- **Checkpoint 管理**：语音合成（CosyVoice）的 Checkpoint `step` 字段为 `LM_epoch × 10000 + FM_epoch` 复合编码，排序与导出需按此逻辑处理（[Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)）。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
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
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)


