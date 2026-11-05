# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖从模型微调、压缩、导入、部署到高性能推理服务管理的完整链路。所有能力均通过标准化 RESTful API 提供，支持开发者在 CI/CD 流程中自动化集成。核心能力围绕“可复现训练 → 可控成本部署 → 稳定服务交付”设计，不依赖控制台操作即可完成端到端模型上线。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成（[文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)）、图像生成（[图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)）、视频生成（[视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)）和语音合成（[语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)）四类模态。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入平台（[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)），导入后可直接部署。
- **模型压缩**：仅支持对 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，降低 MU 规格与推理成本（[模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)）。
- **部署方式**：
  - `lora`：LoRA 模型共享部署（按 [Token](../concepts/token.md) 计费），适用于轻量微调模型；
  - `mu`：模型单元部署（后付费），适用于 CosyVoice 等需专用资源的模型；
  - `dtu`：独占吞吐（预付费），需业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`）；
  - `ptu_v2`：预置吞吐（预付费/后付费），支持北京与新加坡地域；
  - `cu`：算力单元（已逐步归并至 DTU/MU）。

> **注意**：文档 14 与文档 23 均声明 DTU 部署必须使用 `maas.aliyuncs.com` 业务空间域名，但文档 14 的示例请求仍使用 `dashscope.aliyuncs.com`，该示例已过时；实际调用 DTU 接口时务必使用业务空间专属域名，否则返回鉴权失败。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源示例 |
|------|------|------|------|----------|
| `model_name` | string | 是 | 微调产出模型 ID（非基础模型名），取自 `create-fine-tuning-job` 响应中的 `output.finetuned_output` 字段 | [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md) |
| `plan` | string | 是 | 部署方案，值为 `lora`/`mu`/`dtu`/`ptu_v2`/`cu` | [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md) |
| `capacity` | integer | 是（除 `dtu`/`ptu_v2` 外） | 实例数量（`lora`/`mu`/`image`/`video`/`tts` 部署必需）；`dtu`/`ptu_v2` 使用 `dtu_capacity`/`ptu_capacity` 对象替代 | [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md) |
| `aigc_config` | object | 是（视频生成必需） | 视频生成专用配置，含 `use_input_prompt`、`prompt`、`lora_prompt_default` 字段 | [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md) |
| `deploy_spec` | string | 是（`mu` 部署 CosyVoice 必需） | 模型单元规格，如 `MU5`（容量须为 1 的整数倍）或 `MU2`（容量须为 8 的整数倍） | [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md) |

## 使用方式

1. **准备阶段**  
   - 获取 API Key 并配置环境变量（`DASHSCOPE_API_KEY`）；  
   - 确认地域限制：微调、模型导入、模型压缩、`mu`/`lora` 部署仅支持 **华北2（北京）**；`ptu_v2` 部署支持北京与新加坡；DTU 部署需提前在控制台开通额度。

2. **训练与准备模型**  
   - 创建微调任务（如 `POST /api/v1/fine-tunes`），轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`；  
   - （可选）对全参微调模型执行压缩：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建任务，成功后取 `quantized_output` 作为部署输入；  
   - （可选）导入 OSS 模型：`POST /api/v1/custom_models/import`，轮询至 `status=SUCCESSED` 后取 `output.model_name`。

3. **部署服务**  
   - 构造 `POST /api/v1/deployments` 请求体，根据 `plan` 填写对应参数（如 `lora` 仅需 `model_name`+`capacity`+`plan`；`dtu` 需 `sku_code`+`template_code`+`dtu_capacity`）；  
   - 使用正确域名：北京用 `dashscope.aliyuncs.com`（`mu`/`lora`）或 `ws-xxx.cn-beijing.maas.aliyuncs.com`（`dtu`）；新加坡用 `dashscope-intl.aliyuncs.com`（`ptu_v2`）；  
   - 轮询 `GET /api/v1/deployments/{deployed_model}` 直至 `status=RUNNING`（通常需 5–10 分钟）。

4. **调用与管理**  
   - 使用 `deployed_model`（即 `output.deployed_model`）作为模型标识调用推理 API；  
   - 扩缩容、修改限流、删除部署等操作均通过 `GET`/`PUT`/`DELETE /api/v1/deployments/{deployed_model}` 完成（[部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)）。

## 限制和注意事项

- **地域强约束**：所有微调类 API（文本/图像/视频/语音）及模型导入、模型压缩、`mu`/`lora` 部署仅在北京地域可用；跨地域调用将返回 403 错误。  
- **模型兼容性限制**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型，LoRA 模型、基础模型、第三方模型均不支持（[模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)）。  
- **DTU 部署特殊要求**：必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）和对应工作空间的 API Key；不支持 `AssumedRoleUser` 角色身份；续费与自动续费变更仅限控制台操作（[模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)）。  
- **HTTP 成功 ≠ 操作成功**：吞吐预留等异步操作接口即使返回 HTTP 200，也必须检查响应体中 `output.operation_status` 字段是否为 `SUCCEEDED`，否则视为失败（[吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)）。  
- **Checkpoint 导出限制**：语音合成（CosyVoice）模型的 Checkpoint `step` 为 LM epoch × 10000 + FM epoch 的复合值，排序与部署逻辑需据此解析（[Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)）。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)


