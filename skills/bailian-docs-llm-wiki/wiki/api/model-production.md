# model production

`model production` 是百炼平台面向开发者提供的模型全生命周期管理能力集合，覆盖模型调优、压缩、部署、吞吐预留及智能路由等核心环节。所有能力均通过标准化 OpenAPI 提供，支持自动化集成与生产环境编排。开发者需根据模型类型、地域限制和计费模式选择对应 API 路径与参数组合。

## 支持的模型/功能

- **模型调优**：支持文本生成、图像生成、视频生成、语音合成（含 CosyVoice）四类任务，均通过统一 `/api/v1/fine-tunes` 接口提交训练任务，但各模态对模型 ID、超参结构与数据格式有严格约束。例如 CosyVoice 语音合成仅支持 `cosyvoice-v3-flash` 基准模型与 `efficient_sft` 微调类型 [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)。
- **模型部署**：支持文本、图像、视频、语音四类模型的在线服务化，但部署方式因模态而异：文本/图像/视频推荐 `lora` 共享部署；语音合成（CosyVoice）强制使用 `mu` 模型单元部署；吞吐预留（PTU/DTU）与智能路由（MR）则复用同一套 `/api/v1/deployments` 接口，通过 `plan` 参数区分 [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。
- **模型压缩**：当前仅支持华北2（北京）地域，且仅限基于 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型，不支持 LoRA 模型或基础模型 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)。
- **吞吐预留与智能路由**：吞吐预留（PTU）支持预付费与后付费，分 `ptu_fast`（高速）与 `ptu_default`（标速）两档；智能路由（MR）仅支持后付费，且仅在北京与新加坡地域可用 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。

> **注意**：文档 15（文本生成-部署模型）称 DTU 部署“新购独占部署优先选择”，而文档 26（模型部署 API 参考）明确指出“DTU 部署仅支持预付费（`charge_type="pre_paid"`），不支持后付费创建”。二者一致，但文档 15 未强调该硬性限制，易引发误操作。实际调用 DTU 接口时必须传 `charge_type=pre_paid`，否则返回 `INVALID_PARAMETER` 错误。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `plan` | string | 是 | 部署方案标识，决定计费与资源模型 | `lora`, `mu`, `dtu`, `ptu`, `mr` |
| `model_name` | string | 是 | 待部署模型 ID（非基础模型名），微调产出取 `output.finetuned_output`，导入模型取 `output.model_name` | `qwen3-14b-suffix-ft-202410291653-1c7f` |
| `service_tier` | string | 否 | 吞吐预留性能档位 | `ptu_fast`（默认）, `ptu_default` |
| `charge_type` | string | 是 | 计费类型 | `pre_paid`, `post_paid`（MR 强制 `post_paid`） |
| `aigc_config` | object | 条件必填 | 视频生成部署必需，控制提示词生成逻辑 | `{ "use_input_prompt": false, "prompt": "..." }` |
| `deploy_spec` | string | 条件必填 | CosyVoice 语音合成部署必需 | `MU5`, `MU2` |

## 使用方式

1. **调优**：在华北2（北京）地域调用 `POST /api/v1/fine-tunes`，指定 `model`、`training_type` 和 `hyper_parameters`。训练完成后轮询 `GET /api/v1/fine-tunes/{job_id}` 确认 `status=SUCCEEDED`，再从响应中提取 `output.finetuned_output` 作为部署输入。
2. **部署**：根据模型类型选择 `plan`：
   - 文本/图像/视频微调模型 → `plan=lora`，传 `model_name` 与 `capacity=1`
   - CosyVoice 语音合成 → `plan=mu`，传 `model_name`, `deploy_spec`, `capacity`, `billing_method=POST_PAY`
   - 吞吐预留（PTU）→ `plan=ptu`，传 `service_tier`, `ptu_capacity`, `pre_paid_info`（预付费）或省略（后付费）
   - 智能路由 → `plan=mr`，先查 `/api/v1/deployments/model-routing/versions` 获取 `route_model_version`，再创建时传入
3. **吞吐预留管理**：使用 `/api/v1/deployments` 创建、扩缩容、查询实例，注意 HTTP 200 不代表操作成功，必须检查响应体中 `output.operation_status` 字段 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
4. **模型压缩**：先调用 `GET /api/v1/fine-tunes/compress/templates` 获取 `template_id`，再 `POST /api/v1/fine-tunes/compress/jobs` 提交任务，轮询 `GET /api/v1/fine-tunes/compress/jobs/{job_id}` 直至 `status=SUCCEEDED`，最后用 `output.quantized_output` 部署。

## 限制和注意事项

- **地域强绑定**：所有调优 API（文档 4/8/9/10/17/18）、模型导入（文档 5）、模型压缩（文档 27/28）、图像/视频/语音部署（文档 19/20/23）均**仅支持华北2（北京）地域**；PTU 吞吐预留与智能路由支持北京+新加坡；DTU 仅支持北京。跨地域调用将返回 `REGION_NOT_SUPPORTED`。
- **HTTP 成功 ≠ 业务成功**：吞吐预留、部署、压缩等异步操作接口返回 HTTP 200 仅表示请求被接收，实际状态需解析 `output.operation_status` 或 `output.status` 字段。忽略此检查将导致后续调用失败 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性限制**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型；智能路由备选模型列表中出现的模型 ID 不代表当前工作空间已获调用权限，无权限模型会在运行时被自动过滤 [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)。
- **参数不可逆性**：模型压缩不可逆，压缩后模型不支持继续微调或二次压缩；DTU 部署的续费与自动续费变更仅支持控制台操作，API 不提供接口 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [智能路由 API 参考](../../raw/model-api-reference/model-production/model-routing-api-reference.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview.md)
- [模型部署 API 参考](../../raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)


