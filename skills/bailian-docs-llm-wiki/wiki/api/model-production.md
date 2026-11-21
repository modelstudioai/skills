# model production

`model production` 是百炼平台面向模型全生命周期管理的核心能力集合，覆盖从模型微调、压缩、部署到高性能推理服务（含吞吐预留与智能路由）的完整链路。所有能力均通过标准化 OpenAPI 提供，支持开发者在生产环境中自动化构建、验证和交付定制化模型服务。

## 支持的模型/功能

- **微调训练**：支持文本生成（SFT/CPT/DPO）、图像生成（LoRA）、视频生成（图生视频/首尾帧）、语音合成（CosyVoice）四类任务，全部仅限华北2（北京）地域调用 [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)。
- **模型压缩**：仅支持对自定义全参调优模型（如 `qwen3.5-flash-2026-02-23-ft-*`）进行量化压缩，不支持 LoRA 模型或已量化模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。
- **模型部署**：提供多种部署模式：
  - `lora`：LoRA 共享部署（后付费，按 Token 计费），适用于图像/视频生成等轻量微调模型；
  - `mu`：模型单元部署（后付费），适用于 CosyVoice 等需独立资源的语音模型；
  - `dtu`：独占吞吐（预付费，按 TPM 购买容量），适用于高 SLA 场景，需使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）[模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)；
  - `mr`：智能路由（后付费），支持效果优先（`EFFECT_FIRST`）或成本优先（`COST_FIRST`）策略，仅限华北2（北京）与新加坡地域 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。
- **吞吐预留（TPM Reservation）**：为专属部署模型预购输入/输出 TPM 容量，保障稳定低延迟推理，支持扩缩容、续订、自动续费及溢出策略配置。

> **注意**：文档 17（文本生成-部署模型）称 DTU “新购独占部署优先选择”，而文档 25（模型部署 API 参考）明确指出“DTU 部署仅支持预付费（`charge_type="pre_paid"`），不支持后付费创建”；但文档 19（图像生成-部署模型）示例中却使用 `plan="lora"` 且未提 `charge_type`。实际部署时，`plan` 与 `charge_type` 必须严格匹配：`dtu` → `pre_paid`，`lora`/`mu` → `post_paid`，否则请求将被拒绝。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源 |
|------|------|------|------|------|
| `model_name` | string | 是 | 微调产出模型 ID（如 `qwen3-14b-suffix-ft-202410291653-1c7f`），非基础模型名；从调优任务响应 `output.finetuned_output` 获取 | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `plan` | string | 是 | 部署方案：`lora`、`mu`、`dtu` 或 `mr`；决定计费方式与资源隔离级别 | [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md) |
| `capacity` | integer | 是（除 `dtu` 外） | 实例数量（`lora`/`mu`）或 DTU 容量对象（`dtu_capacity` 含 `input_tpm`/`output_tpm`） | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `deploy_spec` | string | 是（`mu` 语音模型） | 模型单元规格（如 `MU5`、`MU2`），决定 `capacity` 的倍数约束 | [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |
| `aigc_config` | object | 是（视频生成） | 视频生成专用提示词配置，含 `use_input_prompt`、`prompt`、`lora_prompt_default` | [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md) |

## 使用方式

1. **准备阶段**：  
   - 在华北2（北京）地域获取并配置 API Key；  
   - 确认账号已开通对应权限（如 RAM 子账号需授予模型调用、训练、部署权限）；  
   - 微调任务需先完成并确认 `status=SUCCEEDED`，再提取 `finetuned_output` 作为 `model_name`。

2. **部署调用**：  
   - 构造 `POST /api/v1/deployments` 请求；  
   - 根据 `plan` 选择正确域名：`dashscope.aliyuncs.com`（`lora`/`mu`/`mr`），或业务空间专属域名（`{ws-id}.{region}.maas.aliyuncs.com`）用于 `dtu`；  
   - 设置请求头：`Authorization: Bearer <api-key>` 和 `Content-Type: application/json`；  
   - 按 `plan` 填写对应必填字段（见上表）。

3. **状态轮询**：  
   - 部署后立即调用 `GET /api/v1/deployments/{deployed_model}` 查询状态；  
   - 持续轮询直至 `output.status=RUNNING`（通常需 5–10 分钟）；  
   - **重要**：HTTP 200 不代表部署成功，必须检查 `output.status` 字段 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

4. **后续管理**：  
   - 扩缩容、修改限流、删除部署均通过 `/api/v1/deployments/{deployed_model}` 系列接口操作；  
   - DTU 容量实例的续订、自动续费开关需通过 `/capacity-instances/{instance_id}/renew` 或 `/auto-renew` 接口，**不可在控制台操作**（文档 23 明确说明“续费与自动续费变更请在控制台操作”，但文档 1 显示其为 API 可控，以 API 文档为准）。

## 限制和注意事项

- **地域限制**：所有微调（文本/图像/视频/语音）、模型导入、模型压缩、`lora`/`mu` 部署均**仅限华北2（北京）地域**；智能路由额外支持新加坡；DTU 部署需使用业务空间专属域名，且资源申请需提前在控制台完成。
- **模型兼容性**：  
  - 模型压缩仅支持特定基础模型（如 `qwen3.5-flash-2026-02-23`）的**全参调优模型**，LoRA 模型直接部署即可，无需压缩；  
  - CosyVoice 语音模型**仅支持 `mu` 部署**，不支持 `lora`（文档 24 明确限定 `plan="mu"`）。
- **异步操作可靠性**：  
  - 吞吐预留、微调、压缩、部署均为异步任务，返回 HTTP 200 仅表示请求已接收，**必须轮询查询终态**；  
  - 操作失败时，错误码（如 `CAPACITY_INSTANCE_REQUIRED`）和消息在响应体 `output.error_code`/`output.error_message` 中返回，而非 HTTP 状态码 [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **命名与标识**：  
  - `deployed_model`（部署标识）与 `model_service_id`（容量实例中使用的模型服务 ID）为同一概念，用于后续所有管理接口；  
  - `instance_id`（容量实例 ID）和 `operation_id`（操作 ID）必须使用接口返回值，**不可自行构造或解析字符串格式**。

## 来源文档

- [吞吐预留 API 参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
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
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)


