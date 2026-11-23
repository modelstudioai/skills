# model production

`model production` 是百炼平台中模型从训练、压缩、导入到部署上线的全生命周期管理能力集合，涵盖微调（Fine-tuning）、模型导入、模型压缩、专属部署（含吞吐预留与智能路由）等核心环节。所有能力均通过统一 OpenAPI 接口提供，支持开发者在生产环境中自动化构建和运维定制化 AI 服务。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，对应不同基准模型与专用超参体系。例如文本生成支持 `qwen3` 系列，图像生成支持 `wan2.7-image-pro`，语音合成仅支持 `cosyvoice-v3-flash` [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **模型导入**：支持将 OSS 中的全参或 LoRA 调优模型文件导入平台，导入完成后可直接部署。当前仅在北京地域开放 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：通过量化技术降低全参调优模型的推理显存占用与延迟，当前仅支持 `qwen3.5-flash-2026-02-23` 和 `qwen3.6-plus-2026-04-02` 基础模型的衍生模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。
- **专属部署**：提供多种部署模式：
  - `lora`：LoRA 共享部署，按 Token 用量后付费；
  - `mu`：模型单元（Model Unit），资源隔离，支持弹性扩缩容；
  - `dtu`：独占吞吐（Dedicated Throughput Unit），预付费、独占 GPU 资源，需使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）；
  - `mr`：智能路由（Model Routing），基于效果或成本策略自动调度多个备选模型，仅支持后付费且当前仅限北京与新加坡地域 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。
- **吞吐预留（TPM Reservation）**：为 `dtu` 部署提供容量实例的购买、扩缩容、续订、释放及溢出策略管理能力，是保障高 SLA 场景的核心机制 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：文档 17（文本生成-部署模型）称 DTU “新购独占部署优先选择”，而文档 23（模型部署 API 参考）明确指出“DTU 部署仅支持预付费（`charge_type="pre_paid"`），不支持后付费创建”，但文档 21（语音合成-部署模型）示例中却出现 `"billing_method": "POST_PAY"` 与 `"plan": "mu"` 混用——这属于部署方式与计费方式的正确绑定，非矛盾；真正矛盾在于：文档 23 明确要求 DTU 必须用 `maas.aliyuncs.com` 域名和业务空间 API Key，而文档 17 的 DTU 示例请求地址仍写为 `dashscope.aliyuncs.com`，该地址**无法用于 DTU 创建**，属文档错误。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源示例 |
|------|------|------|------|----------|
| `model_name` | string | 是 | 待部署/压缩/导入的模型 ID（非基础模型名），如 `qwen3-14b-ft-20241029...` 或 `cosyvoice-v3-flash-ft-...` | [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |
| `plan` | string | 是 | 部署方案：`lora` / `mu` / `dtu` / `mr`；决定计费模型与资源模型 | [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md) |
| `capacity` / `dtu_capacity` | integer / object | 是（依 plan） | `lora`/`mu` 用 `capacity`（整数倍）；`dtu` 用 `dtu_capacity`（含 `input_tpm`/`output_tpm`） | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `charge_type` | string | 是（DTU） | `pre_paid`（DTU 强制），`post_paid`（其他 plan） | [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `aigc_config` | object | 是（视频生成） | 视频部署必需，控制提示词生成逻辑（`use_input_prompt`, `prompt`, `lora_prompt_default`） | [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md) |
| `weight_type` | string | 是（模型导入） | `full`（全参）或 `lora`（LoRA） | [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md) |

## 使用方式

1. **准备模型**  
   - 微调：调用 `/api/v1/fine-tunes` 创建任务（如 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)），轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，获取 `finetuned_output`。
   - 导入：调用 `/api/v1/custom_models/import` 提交 OSS 路径，轮询任务状态，成功后获得 `model_name`。
   - 压缩：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建，轮询至 `SUCCEEDED` 后取 `quantized_output`。

2. **部署服务**  
   - 统一入口：`POST /api/v1/deployments`  
   - 区分逻辑：通过 `plan` 参数路由至不同部署流程（`lora`/`mu`/`dtu`/`mr`）。  
   - 域名关键：`dtu` 和 `mr` 必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）；其余可用 `dashscope.aliyuncs.com` 或 `dashscope-intl.aliyuncs.com`（依地域）。  
   - 验证部署：`GET /api/v1/deployments/{deployed_model}` 轮询，`status=RUNNING` 表示就绪。

3. **管理运行时**  
   - 扩缩容：`PUT /api/v1/deployments/{deployed_model}/scale`（`mu`/`lora`）或 `PUT /api/v1/deployments/{deployed_model}/capacity-instances/{instance_id}/scale`（`dtu` 实例）  
   - 查询列表：`GET /api/v1/deployments`（所有部署）或 `GET /api/v1/deployments?plan=dtu`（仅 DTU）  
   - 删除：`DELETE /api/v1/deployments/{deployed_model}`  

## 限制和注意事项

- **地域限制严格**：微调、模型导入、模型压缩、绝大多数部署 API **仅在北京（华北2）地域可用**；新加坡仅支持部分 `mr` 和通用部署查询；其他地域必须使用控制台操作（见文档 5、7、8、10、12、14、21、22、25、26）。
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求已接收，**必须检查响应体中的 `output.operation_status` 字段**（如 `SUCCEEDED`/`FAILED`），并结合 `GET .../operations/{id}` 查询终态 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **DTU 特殊约束**：  
  - 不支持 `AssumedRoleUser` 角色；  
  - 续费与自动续费变更**仅支持控制台操作**，API 不提供接口；  
  - 创建必须使用业务空间专属域名与对应 API Key，`dashscope.aliyuncs.com` 域名调用将失败。
- **模型兼容性**：模型压缩**仅支持全参调优模型**，LoRA 模型、已量化模型、非指定基础模型（如 `qwen3.5-flash-2026-02-23`）均不可用 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。
- **命名与长度**：`display_name` ≤ 50 字符（`dtu`），`suffix` ≤ 24 字符，完整 `deployed_model` ≤ 100 字符；`output_model_suffix`（压缩）仅支持小写字母+数字，≤ 8 字符。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)


