# model production

`model production` 是百炼平台中模型从训练、压缩、部署到高可用推理服务的全生命周期管理能力集合，涵盖微调（Fine-tuning）、导入（Import）、压缩（Compression）、部署（Deployment）及吞吐预留（Throughput Reservation）等核心环节。所有操作均通过统一的 RESTful API 接口暴露，支持开发者在生产环境中自动化构建和管理专属模型服务。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类模态的 LoRA/全参微调，各模态对应独立的创建与管理接口，如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)、[图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md) 等。
- **模型导入**：支持将 OSS 中存储的自定义模型（全参或 LoRA）导入平台，仅在北京地域开放，详见 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，不支持 LoRA 模型或已量化模型，详见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **智能路由**：提供基于效果或成本策略的多模型动态路由服务，仅支持华北2（北京）与新加坡地域，且**强制后付费**（`charge_type="post_paid"`），详见 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。
- **吞吐预留（PTU）与独占吞吐（DTU）**：PTU 支持预付费/后付费及标速（`ptu_default`）/高速（`ptu_fast`）档位；DTU 为预付费独占算力方案，仅支持北京地域，且必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）调用。

> **注意**：文档 15（文本生成-部署模型）称 PTU 等部署方式支持“北京与新加坡”，而文档 27（模型部署 API 参考）明确指出“PTU 等部署方式支持北京与新加坡地域”，但文档 1（吞吐预留 API参考）示例中仅列出北京与弗吉尼亚（`us-east-1`）的 Endpoint，未提新加坡。实际支持地域应以控制台或 `/api/v1/deployments/models?plan=ptu` 接口返回为准，API 文档存在地域描述不一致，建议优先通过可部署模型列表接口确认。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源示例 |
|------|------|------|------|----------|
| `model_name` | string | 是 | 待部署/微调的模型标识（非基础模型名），如微调产出的 `qwen3-14b-suffix-ft-...` 或导入模型名 | [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md) |
| `plan` | string | 是 | 部署方案：`dtu`（独占）、`mu`（模型单元）、`ptu`（预置吞吐）、`lora`（LoRA共享）、`mr`（智能路由） | [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md) |
| `service_tier` | string | 否 | 吞吐预留性能档位：`ptu_fast`（默认）、`ptu_default` | [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `charge_type` | string | 是 | 付费类型：`pre_paid`（预付费）、`post_paid`（后付费）。**DTU 强制 `pre_paid`；智能路由强制 `post_paid`** | [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `aigc_config` | object | 是（视频/图像部署） | 提示词配置对象，含 `use_input_prompt`、`prompt` 等字段，用于控制生成逻辑 | [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md) |

## 使用方式

1. **准备环境**：获取并配置对应地域的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)），确认工作空间与地域权限。
2. **选择路径**：
   - *微调*：调用 `/api/v1/fine-tunes` 创建任务 → 轮询 `/api/v1/fine-tunes/{job_id}` 确认 `status=SUCCEEDED` → 获取 `output.finetuned_output`。
   - *导入*：调用 `/api/v1/custom_models/import` → 轮询 `/api/v1/custom_models/{job_id}` 直至 `status=SUCCESSED`。
   - *压缩*：先调用 `/api/v1/fine-tunes/compress/templates` 获取模板 → 再调用 `/api/v1/fine-tunes/compress/jobs` 创建 → 轮询至 `SUCCEEDED` → 获取 `quantized_output`。
3. **部署服务**：使用上一步得到的 `model_name`，向 `/api/v1/deployments` 发送 POST 请求，按 `plan` 填写对应参数（如 DTU 需 `sku_code`/`template_code`；LoRA 需 `capacity`；智能路由需 `route_model_version` 和 `candidate_models`）。
4. **验证状态**：调用 `/api/v1/deployments/{deployed_model}` 轮询，当 `output.status == "RUNNING"` 时即可调用。

> **注意**：文档 1（吞吐预留 API参考）强调“HTTP 请求成功不等于容量操作成功”，响应体中的 `output.operation_status` 必须为 `SUCCEEDED` 才代表预留生效；同理，部署接口返回 HTTP 200 后仍需轮询状态，不可直接假设部署完成。

## 限制和注意事项

- **地域限制严格**：微调、导入、压缩、视频/图像/语音部署等绝大多数功能**仅在北京（cn-beijing）地域可用**；新加坡仅部分部署方式（如 PTU）和智能路由支持；弗吉尼亚仅吞吐预留 API 明确提及。
- **鉴权与域名强绑定**：DTU 部署必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）和该空间的 API Key；智能路由在新加坡需用 `dashscope-intl.aliyuncs.com`；跨地域使用 API Key 将失败。
- **参数依赖查询接口**：`sku_code`、`template_code`、`route_model_version`、`supported_candidate_model_ids` 等关键参数**不可硬编码**，必须通过对应 `GET /api/v1/deployments/models` 或 `GET /api/v1/deployments/model-routing/versions` 等接口动态获取。
- **模型兼容性约束**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型；CosyVoice 部署仅支持 `mu` 方案；智能路由不校验备选模型调用权限，无权限模型将在运行时被过滤。
- **计费敏感参数**：`n_epochs`（文本/语音）、`max_steps`（图像）、`batch_size` 等直接影响训练费用，文档 4、8、10、13 均明确标注其计费影响，需谨慎设置。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)


