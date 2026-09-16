# model production

`model production` 指在百炼平台完成模型从训练、压缩、导入到部署上线的全生命周期管理，覆盖文本、图像、视频、语音等多模态模型。核心能力包括微调训练（Fine-tuning）、自定义模型导入、量化压缩、专属/共享部署及 TPM 预留容量管理。所有生产环节均通过 OpenAPI 实现自动化集成，适用于开发者构建可扩展的 AI 服务。

## 支持的模型与功能

- **微调训练**：支持文本生成（[文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)）、图像生成（[图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)）、视频生成（[视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)）和语音合成（[语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)）四类模型。
- **模型导入与压缩**：支持将 OSS 中的全参或 LoRA 模型导入平台（[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)）；支持对特定全参调优模型进行量化压缩以降低推理成本（[模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)）。
- **部署方式**：提供三种部署方案：
  - `mu`（Model Unit）：专属资源、按单元时长计费，支持限流与上下文长度配置；
  - `lora`：LoRA 共享部署、按 Token 用量计费，适用于轻量级微调模型；
  - `ptu`：预置吞吐量（Pre-provisioned Throughput Unit），按输入/输出 TPM 预留容量计费（详见 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)）。

> **注意**：文档 17（文本生成部署）与文档 19（图像生成部署）对 `plan=lora` 的适用性描述存在不一致——前者未明确限制，后者强调“LoRA高效微调推荐为`lora`”；而文档 22（语音合成部署）则明确要求 CosyVoice 模型**仅支持 `mu`**。实际使用中，请以目标模型类型对应的专用部署文档为准，语音合成类必须使用 `mu`。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model_name` | string | 是 | 待部署/调优的模型标识（非基础模型名）。微调产出取 `output.finetuned_output`；导入模型取 `output.model_name`。 | `qwen3-14b-suffix-ft-202410291653-1c7f` |
| `plan` | string | 是 | 部署方案：`mu` / `lora` / `ptu` | `"lora"` |
| `deploy_spec` | string | 条件必填 | `plan=mu` 时必填，指定部署模板规格（如 `MU1`, `MU5`） | `"MU5"` |
| `capacity` | integer | 条件必填 | 资源单元数量（`mu`/`lora`）或实例数（`ptu`）；需满足 `base_capacity` 倍数约束 | `1`（`lora`）或 `4`（`MU1`） |
| `ptu_capacity` | object | 条件必填 | `plan=ptu` 时必填，含 `input_tpm` 和 `output_tpm`（单位：kTPM） | `{"input_tpm": 10, "output_tpm": 1}` |
| `aigc_config` | object | 条件必填 | 视频生成部署必需，控制提示词生成逻辑（`use_input_prompt`, `prompt`, `lora_prompt_default`） | — |

## 使用方式

1. **训练/准备模型**：  
   - 创建微调任务（如文本生成：`POST /api/v1/fine-tunes`），确认 `status=SUCCEEDED` 后获取 `finetuned_output`；  
   - 或通过 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md) 将 OSS 模型导入，待 `status=SUCCESSED`；  
   - 或对全参模型执行 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)，获取 `quantized_output`。

2. **部署模型**：  
   - 统一调用 `POST /api/v1/deployments`，根据模型类型选择 `plan` 并传入对应参数：  
     - 文本/图像/视频 LoRA 模型 → `plan=lora` + `capacity=1`；  
     - 语音合成模型 → `plan=mu` + `deploy_spec=MU5` + `capacity=1`；  
     - 高性能/低延迟场景 → `plan=mu` + `deploy_spec=MU2/MU5` + `capacity` 按需设置；  
     - 稳定吞吐保障 → `plan=ptu` + `ptu_capacity` 配置。

3. **验证与调用**：  
   - 轮询 `GET /api/v1/deployments/{deployed_model}`，等待 `status=RUNNING`；  
   - 使用返回的 `output.deployed_model` 作为模型 ID 进行在线推理调用。

## 限制和注意事项

- **地域限制**：所有微调、导入、压缩及部署 API **仅在华北2（北京）地域可用**（文档 4、5、6、8、10、12、13、14、17、19、21、22、23、24 均明确声明），跨地域调用将失败。TPM 预留接口虽支持多地域（如弗吉尼亚），但需使用对应地域的 Endpoint 和 API Key（[TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)）。
- **认证与域名**：必须使用与地域匹配的 API Key 及工作空间专属域名（如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），DashScope 公共域名 `https://dashscope.aliyuncs.com` 仅适用于北京地域（文档 2、4、5、6、8、10、12、13、17、19、22、23、24）。
- **状态检查关键点**：  
  - HTTP 200 不代表操作成功（如 TPM 预留创建），必须检查响应 `output.operation_status` 或 `output.status` 字段（文档 2 强调：“HTTP 请求成功不等于容量操作成功”）；  
  - 部署任务需轮询至 `status=RUNNING` 才可调用（文档 24 明确提示“模型部署过程预计需要 5～10 分钟”）；  
  - 微调任务需 `status=SUCCEEDED` 后方可部署（文档 19、22、23 均要求前置校验）。
- **模型兼容性**：模型压缩当前**仅支持 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型**，LoRA 模型和已量化模型不支持（文档 6）；语音合成部署**强制要求 `plan=mu`**，不支持 `lora` 或 `ptu`（文档 22）。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)


