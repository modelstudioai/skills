# model production

`model production` 是百炼平台中模型从训练、压缩、导入到部署上线的全生命周期管理能力集合，涵盖微调（Fine-tuning）、模型部署（Deployments）、吞吐预留（Throughput Reservation）、[智能路由](../concepts/model-routing.md)（Model Routing）及模型压缩（Quantization）等核心环节。所有能力均通过统一 OpenAPI 接口提供，支持开发者以编程方式完成模型工业化交付。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，对应不同基准模型与训练范式（如 `sft`、`dpo_lora`、`efficient_sft`）。各模态微调均需在华北2（北京）地域调用，且必须使用该地域的 API Key [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型部署（Deployments）**：支持将微调产出模型、OSS 导入模型或基础模型部署为在线服务，部署方式包括：
  - `lora`：LoRA 共享部署（按 Token 计费）
  - `mu`：模型单元（按资源单元计费，如 `MU5`、`MU2`）
  - `dtu`：独占吞吐（预付费，按输入/输出 TPM 购买容量）
  - `mr`：[智能路由](../concepts/model-routing.md)（后付费，仅支持北京与新加坡地域）[智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- **吞吐预留（Throughput Reservation）**：为专属模型 code 预留确定性推理容量，支持扩缩容、续订、自动续费与溢出策略配置 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型压缩（Quantization）**：仅支持对自定义全参调优模型（如 `qwen3.5-flash-2026-02-23-ft-*`）进行量化压缩，以降低显存占用、提升吞吐；LoRA 模型和已量化模型不支持 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。

> **注意**：文档 23 与文档 26 对 DTU 部署的域名要求存在表述差异——文档 23 明确要求 DTU 必须使用业务空间专属域名（如 `ws-vxxx.cn-beijing.maas.aliyuncs.com`），而文档 26 的示例中仍列出 `dashscope.aliyuncs.com` 作为北京地域可选域名。实际调用应以文档 23 为准：DTU 部署**必须**使用 `maas.aliyuncs.com` 域名及对应业务空间的 API Key。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model_name` | string | 是 | 待部署/压缩/调优的模型 ID（非基础模型名）。微调产出取 `output.finetuned_output`；导入模型取 `output.model_name`；DTU 部署需匹配 `sku_code` 与 `template_code` | `qwen3-14b-suffix-ft-202410291653-1c7f` |
| `plan` | string | 是 | 部署/预留类型标识符 | `lora`, `mu`, `dtu`, `mr`, `tpu`（吞吐预留） |
| `capacity` / `dtu_capacity` | integer / object | 条件必选 | `mu`/`lora` 部署需 `capacity`（整数）；`dtu` 部署需 `dtu_capacity`（含 `input_tpm` 和 `output_tpm`） | `capacity: 1`, `dtu_capacity: {"input_tpm": 100, "output_tpm": 200}` |
| `deploy_spec` | string | `mu` 部署必选 | 模型单元规格，如 `MU5`（capacity 为 1 的倍数）、`MU2`（capacity 为 8 的倍数） | `MU5` |
| `aigc_config` | object | 视频生成部署必选 | 提示词控制配置，含 `use_input_prompt`, `prompt`, `lora_prompt_default` | `{ "use_input_prompt": false, "prompt": "..." }` |

## 使用方式

1. **准备阶段**  
   - 获取并配置对应地域的 API Key（文档 1、2、5、7 等均强调地域绑定）；
   - 确认模型来源与状态：微调任务需 `status=SUCCEEDED`（文档 13、17、19、21），导入任务需 `status=SUCCESSED`（文档 7），压缩任务需 `status=SUCCEEDED` 并取 `quantized_output`（文档 24）。

2. **核心操作流程**  
   - **微调 → 部署**：调用 `/api/v1/fine-tunes` 创建任务 → 轮询 `/api/v1/fine-tunes/{job_id}` 确认成功 → 使用 `finetuned_output` 调用 `/api/v1/deployments` 部署；
   - **导入 → 部署**：调用 `/api/v1/custom_models/import` 提交导入 → 轮询确认 `status=SUCCESSED` → 使用 `output.model_name` 部署；
   - **吞吐预留**：调用 `/api/v1/deployments`（`plan=tpu`）创建预留 → 通过 `/capacity-instances` 管理实例 → 用 `update-overflowstrategy` 配置溢出行为；
   - **[智能路由](../concepts/model-routing.md)**：先调用 `/api/v1/deployments/model-routing/versions` 查询可用路由版本 → 再以 `plan=mr` 创建路由服务。

3. **调用规范**  
   - 所有 POST/PUT 请求体为 JSON，Header 必含 `Content-Type: application/json` 和 `Authorization: Bearer <api-key>`；
   - HTTP 200 不代表操作终态，必须检查响应 `output.operation_status` 或轮询 `/operations/{id}`（文档 1 强调）；
   - 同一 `deployed_model` 的变更操作串行执行，新请求可能被拒绝（文档 1）。

## 限制和注意事项

- **地域限制**：微调（文档 5、8、10、12）、模型导入（文档 7）、模型压缩（文档 24）、大部分部署接口（文档 17、19、21、22、26）**仅支持华北2（北京）地域**；智能路由（文档 2）额外支持新加坡；DTU 部署（文档 23、26）必须使用业务空间专属域名。
- **权限要求**：子账号需授予模型调用、训练、部署权限（文档 5、8、10、12、17、19、21、22）；DTU 部署不支持 `AssumedRoleUser`（文档 23）。
- **状态确认**：部署/预留/压缩等异步操作返回 `HTTP 200` 后，必须轮询查询终态（如 `status=RUNNING` 或 `operation_status=SUCCEEDED`），不可直接使用返回值（文档 1、22、24）。
- **参数约束**：`max_length`（文本微调）、`max_steps`（图像微调）、`n_epochs`（视频/语音微调）等关键超参直接影响费用与效果，需严格按文档推荐值设置（文档 5、8、10、12）；`capacity` 值必须满足部署方案的倍数约束（如 `MU2` 要求 capacity 为 8 的倍数，文档 21）。
- **错误处理**：所有接口统一返回 `request_id` 与 `code`/`message`，需记录 `request_id` 用于问题排查（文档 1、23、24）。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
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
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)


