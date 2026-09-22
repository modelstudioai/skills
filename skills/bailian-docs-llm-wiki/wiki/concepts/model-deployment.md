# 模型部署

模型部署是百炼平台将训练完成或导入的模型实例化为稳定、可调用的在线推理服务的核心能力。它通过资源隔离、容量保障与标准化 API 接入，使模型从开发态进入生产态，支撑高并发、低延迟、可计量的业务调用。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准推理服务**：用户选择预置模型（如 `qwen3-14b`）或自定义模型，通过控制台或 OpenAPI 创建部署，获得专属 `endpoint` 和 `api_key`，即可按标准 [OpenAI 兼容接口](openai-compatible-api.md)发起调用。
- **生产级稳定性保障**：对 SLA 敏感的业务，选用 `ptu`（预置吞吐）或 `dtu`（独占算力）部署，锁定确定性 TPM 容量与 GPU 显存资源，避免共享环境抖动；其中 `dtu` 支持 CUDA 内核级隔离，适用于金融、医疗等强合规场景。
- **弹性与成本敏感型场景**：采用 `token`（按量）部署，无需预付费，按实际输入/输出 [Token](token.md) 计费，适合测试、POC 或流量波动大的应用；但不支持流式响应与自定义 stop 字符串。
- **微调模型上线**：完成微调任务后，提取 `finetuned_output` 作为 `model_id`，以 `mu`（专属资源）或 `lora`（LoRA 共享）方式部署，实现定制能力快速投产。
- **高性能推理加速**：结合吞吐预留（TPM Reservation）创建专属 model code（如 `tpm-reserved-xxx`），或直接调用 Prime 模式模型（如 `glm-5.2-fast-preview`），在不改变业务代码的前提下提升 TPS 1.5–2 倍。

> ⚠️ 注意：所有部署操作**仅支持华北2（北京）地域**；跨地域调用需单独部署；专属 model code 与 Prime model ID 不可混用，且均不跨地域通用。

## 关键参数和配置

| 参数 | 必填 | 取值范围/说明 | 使用场景 |
|------|------|----------------|----------|
| `deployment_type` 或 `plan` | 是 | `dedicated` / `ptu` / `dtu` / `token`（控制台）；`mu` / `lora` / `ptu`（API） | 决定资源模式、计费方式与功能边界 |
| `model_id` | 是 | 平台预置模型 ID（如 `qwen3-8b`）或微调/导入产出的唯一标识（如 `qwen3-14b-ft-20241029`） | 指定被部署的模型实体 |
| `instance_type` | 仅 DTU/PTU | 如 `ecs.gn7i-c16g1.2xlarge`；专属部署由系统自动匹配 | 显式指定 GPU 实例规格（DTU 必填，PTU 可选） |
| `deploy_spec` & `capacity` | 仅 `mu` 部署 | `deploy_spec`: `MU1`/`MU2`/`MU5`；`capacity`: 对应规格的整数倍（如 `MU2` → `capacity` 为 8 的倍数） | 控制专属资源规模与并发能力 |
| `ptu_capacity` | 仅 `ptu` | JSON 对象：`{"input_tpm": 10000, "output_tpm": 1000}`（单位：kTPM） | 预留输入/输出吞吐量，默认值生效时为 `10000/1000` |
| `max_tokens` / `temperature` 等 | 否 | API 调用时传入，**不在部署阶段配置** | 属于推理时动态参数，不影响部署本身 |

> ✅ 提示：部署成功后状态为 `active`（控制台）或 `RUNNING`（API），通常耗时 2–10 分钟；部署期间不可热更新模型权重，变更需重新创建部署。

## 面向开发者，简洁实用

- **快速上手**：控制台「模型部署」页 → 选类型 → 填 `model_id` + `deployment_type` → 提交 → 复制 `endpoint` + `api_key` → 直接调用。
- **自动化集成**：使用 OpenAPI `POST /api/v1/deployments`，参数结构与控制台一致；务必轮询 `/api/v1/deployments/{id}` 直至 `status == "RUNNING"` 再发起业务请求。
- **调试建议**：
  - 首次部署后，先用简单请求（如 `{"messages":[{"role":"user","content":"你好"}]}`）验证连通性；
  - 若遇 429 错误，检查是否超出 PTU 预留容量或触发全局限流（可通过 `/api/v1/models/limits` 查询）；
  - 流式响应失败？确认未使用 `token` 部署（该类型不支持 `stream=true`）。
- **避坑清单**：
  - 同一 `model_id` 在同一地域下，`dedicated`/`ptu`/`dtu` 类型互斥，仅 `token` 可并存；
  - 自定义模型必须先通过「模型导入」完成校验并标记为“可用”，否则无法部署；
  - 所有部署均绑定地域，北京部署的 endpoint 不可在新加坡调用；
  - Prime 模式是独立 model ID，**不是部署产物**，无需创建部署，直接调用即可。

## 关联主题页

- [model deployment index](../guides/model-deployment-index.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [test 1](../guides/test-1.md)
- [model management](../api/model-management.md)


