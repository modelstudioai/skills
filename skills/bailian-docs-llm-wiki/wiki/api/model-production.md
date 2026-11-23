# model production

`model production` 是百炼平台中将训练/调优完成的模型转化为可稳定、可扩展、可管理的在线推理服务的核心能力集合，涵盖模型部署、吞吐预留、智能路由、模型压缩及多模态模型（文本、图像、视频、语音）的全生命周期管理。所有生产级操作均通过统一的 `/api/v1/deployments` 和 `/api/v1/fine-tunes` 等 OpenAPI 接口实现，支持自动化集成与精细化资源控制。

## 支持的模型与功能

- **模型类型**：支持文本生成（如 `qwen3-*`）、图像生成（如 `wan2.7-image-pro`）、视频生成（如 `wan2.7-i2v`）、语音合成（如 `cosyvoice-v3-flash`）四类主流模态模型的部署与生产化。
- **核心功能**：
  - **模型部署**：提供多种计费与资源隔离模式，包括模型单元（MU）、独占吞吐（DTU）、LoRA 共享部署（`lora`）及算力单元（CU）；其中 DTU 为预付费独占 GPU 资源方案，是 MU 的继任者 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。
  - **吞吐预留（TPM Reservation）**：通过专属 `deployed_model` 标识创建容量实例，支持按需叠加、扩缩容、续订与自动续费，保障低延迟高并发场景下的确定性性能 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
  - **智能路由（Model Routing）**：基于效果或成本策略动态调度请求至多个备选模型，仅支持华北2（北京）与新加坡地域，且**强制后付费**（`charge_type="post_paid"`）[智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。
  - **模型压缩**：对全参微调模型执行量化压缩，降低显存占用并提升吞吐，当前仅支持 `qwen3.5-flash-2026-02-23` 和 `qwen3.6-plus-2026-04-02` 基础模型的衍生模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。

> **注意**：文档 15 与文档 23 均指出 DTU 部署必须使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）和对应工作空间的 API Key，而文档 17、19、21 却在示例中错误地使用了 `dashscope.aliyuncs.com` 域名进行 DTU 相关部署（实际 DTU 不在此域名下生效）。请以 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md) 中的说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `plan` | string | 是 | 部署方案标识：`mu`（模型单元）、`dtu`（独占吞吐）、`lora`（LoRA 共享）、`mr`（智能路由）、`cu`（算力单元） | `"dtu"`, `"lora"`, `"mr"` |
| `model_name` | string | 是 | 待部署模型 ID（非基础模型名），来自微调任务输出 `finetuned_output` 或导入任务 `model_name` | `"qwen3-14b-suffix-ft-202410291653-1c7f"` |
| `deployed_model` | string | — | 部署成功后返回的唯一服务标识，用于后续查询、调用及容量管理 | `"qwen3-14b-ft-sample-20241029"` |
| `dtu_capacity.input_tpm` / `output_tpm` | integer | 是（DTU） | DTU 模式下购买的输入/输出 TPM 容量，步长与上限依模型而异 | `{"input_tpm": 1000, "output_tpm": 2000}` |
| `aigc_config.use_input_prompt` | boolean | 是（视频生成） | 视频部署特有参数，控制提示词来源（自动生成 or 手动传入） | `false` |
| `routing_config` | object | 是（MR） | 智能路由配置对象，含 `route_model_version`、`strategy`、`candidate_models` 等字段 | `{"route_model_version": "model-router-20260908", "strategy": "EFFECT_FIRST", ...}` |

## 使用方式

1. **准备模型**：  
   - 文本/图像/视频/语音模型需先完成微调（见各模态 `create-fine-tuning-job-api.md`）或 OSS 导入（见 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)），并确认任务状态为 `SUCCEEDED`。

2. **选择部署方式并调用**：  
   - **通用部署**（MU/CU/LORA）：向 `https://dashscope.aliyuncs.com/api/v1/deployments` 发送 `POST`，携带 `model_name`、`plan`、`capacity`（MU/CU）或 `aigc_config`（视频）等参数。  
   - **DTU 部署**：必须使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），请求体需包含 `sku_code`、`template_code`、`charge_type: "pre_paid"` 及 `dtu_capacity`。  
   - **智能路由**：同样调用 `/api/v1/deployments`，但请求中必须指定 `plan="mr"`，且需先通过 `/api/v1/deployments/model-routing/versions` 查询可用路由版本。

3. **验证与管理**：  
   - 轮询 `GET /api/v1/deployments/{deployed_model}` 直至 `status == "RUNNING"`。  
   - 吞吐预留操作（如扩容）需通过 `/api/v1/deployments/{deployed_model}/capacity-instances` 系列接口完成，并**必须检查 `output.operation_status` 字段**，HTTP 200 不代表操作成功 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

## 限制和注意事项

- **地域限制**：  
  - 微调（`/api/v1/fine-tunes`）、模型导入、Checkpoint 管理、模型压缩、所有模态的部署 API **仅在华北2（北京）地域开放**（文档 5、6、8、10–14、17–21、24）。  
  - 智能路由 API 仅支持华北2（北京）与新加坡（文档 2）。  
  - DTU 部署虽支持北京，但其查询模板接口（`/api/v1/deployments/models?plan=dtu`）**必须使用业务空间专属域名**，不可用 `dashscope.aliyuncs.com`（文档 23）。

- **权限与鉴权**：  
  - 所有 API 均需 `Authorization: Bearer <api-key>`，且 API Key 与地域强绑定，跨地域调用将失败。  
  - 子账号（RAM 用户）需被授予 `AliyunBailianFullAccess` 或最小化自定义权限策略（含 `bailian:CreateDeployment`、`bailian:ListDeployments` 等动作）。

- **关键行为约束**：  
  - 同一 `deployed_model` 的容量变更操作（如扩缩容）按顺序串行处理；若存在进行中操作，新请求可能被拒绝。  
  - DTU 续费与自动续费开关**不支持 API 修改，仅限控制台操作**（文档 23）。  
  - 智能路由服务不支持预付费，`charge_type` 固定为 `"post_paid"`，且无法与 DTU 混用（文档 2）。  
  - 模型压缩仅支持全参微调模型，LoRA 模型、已量化模型及非指定基础模型（`qwen3.5-flash-2026-02-23` / `qwen3.6-plus-2026-04-02`）均不可压缩（文档 24）。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


