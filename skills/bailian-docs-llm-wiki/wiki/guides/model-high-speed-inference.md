# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化场景的推理加速能力，包括 Prime 模式（输出级加速）、吞吐预留（TPM 容量保障）、批量推理（异步离线处理）、专属部署（PTU/DTU/MU）及智能路由（动态模型选型）。所有方案均基于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，无需修改客户端核心逻辑即可接入，适用于 AI 编程助手、实时对话、内容审核、模型评测等典型高性能需求场景。

## 支持的模型/功能

| 方案 | 核心能力 | 典型适用模型（北京） | 文档依据 |
|------|----------|------------------------|----------|
| **Prime 模式** | 输出 TPS 提升 1.5~2 倍；按 token 计费；无额外参数，仅需指定专用 model ID（如 `glm-5.2-fast-preview`） | `glm-5.3-prime`, `glm-5.2-fast-preview`, `wan3.0-video-prime` | [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) |
| **吞吐预留（TPM 预留）** | 为指定模型锁定专属输入/输出 TPM 容量，支持「自动溢出」或「仅预留容量」策略；专属模型 code 调用 | `Qwen3.8-Max`, `GLM-5.3`, `DeepSeek-v4-Pro`, `Kimi-K2.6` 等 20+ 模型 | [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| **批量推理（Batch）** | 异步处理大批量请求，成本约为实时推理的 50%；支持 JSONL 文件提交；结果文件不返回 `reasoning_content` 字段 | `qwen3.8-max`, `qwen3.7-plus`, `qwen3-vl-plus`, `text-embedding-v4` 等 | [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| **专属部署（PTU/DTU/MU）** | PTU：预置吞吐保障，TPS 提升 1.5~2 倍；DTU：独占 TPM 吞吐；MU：独占模型单元，支持 PD 分离；三者均需替换 `model` 为专属 code | `qwen3.7-plus-2026-05-26`, `glm-5.2`, `deepseek-v4-flash-0731`, `qwen3.5-27b` 等 | [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md) |
| **智能路由** | 动态分析请求内容，在备选模型集中自动匹配最优模型（效果优先 / 成本优先）；调用 model-code 固定为 `auto-model-xxxxxx` | `qwen3.8-max`, `qwen3.7-flash`, `deepseek-v4-pro-0813`, `glm-5.2` 等（见路由版本 `model-router-2026-0908`） | [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) |

> **注意**：文档中关于 `GLM-5.2` 的 Prime 模式模型 ID（`glm-5.2-fast-preview`）与吞吐预留支持列表（`GLM-5.2`）存在命名差异，实际调用时需严格使用各方案文档明确列出的 model ID，不可混用。例如吞吐预留创建后生成的专属 code 与 Prime 模式 model ID 语义不同，不可互换。

## 关键参数

| 参数 | 说明 | 适用方案 | 注意事项 |
|------|------|----------|----------|
| `model` | 必填，指定推理模型或服务标识 | 全部 | Prime 模式用 `*-fast-preview`；吞吐预留/专属部署用控制台生成的专属 code；智能路由用 `auto-model-xxxxxx`；批量推理用标准 model ID（如 `qwen-max`） |
| `stream` | 是否启用流式响应 | Prime、专属部署、智能路由 | 流式下 `glm-5.2` 系列需通过 `delta.reasoning_content` 和 `delta.content` 分别获取思考与回答内容 |
| `enable_thinking` | 控制是否启用深度思考模式 | 批量推理、专属部署（MU）、部分 PTU | 批量推理中即使设为 `true`，结果文件也不含 `reasoning_content` 字段；[批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) 明确指出该字段在结果中被省略 |
| `input_tpm` / `output_tpm` | 预留或购买的吞吐额度（单位：kTPM） | 吞吐预留、PTU、DTU | DTU 要求购买基准 TPM 的整数倍；PTU 支持按天/8小时预付费；DTU 与 MU 不可混用同一模型实例 |
| `max_completion_tokens` | 限制最大输出 token 数 | 智能路由 | 智能路由会将 `max_tokens` 自动转换为此参数，并**仅路由到支持该参数的备选模型**；其他参数如 `temperature`、`top_p` 在智能路由下不支持 |

## 使用方式

### 1. Prime 模式
- **接入方式**：直接调用标准 `/v1/chat/completions` 接口，`model` 设为 `glm-5.2-fast-preview` 等专用 ID，域名使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
- **示例**：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```

### 2. 吞吐预留 & 专属部署（PTU/DTU/MU）
- **通用流程**：控制台创建 → 获取专属 `model code` → 替换 API 请求中的 `model` 参数。
- **关键区别**：
  - 吞吐预留：在 [TPM 预留页面](https://bailian.console.aliyun.com/cn-beijing/model/tpm-reservation) 创建，侧重容量保障；
  - PTU：在专属部署页选择「PTU 预置吞吐」，与吞吐预留底层能力一致，但管理入口不同；
  - DTU/MU：在专属部署页选择「独占算力」，支持更细粒度性能配置（如首字延迟、PD 分离）。

### 3. 批量推理
- **步骤**：准备 UTF-8 编码 JSONL 文件（每行一个请求，含 `custom_id`, `method`, `url`, `body`）→ 控制台上传 → 查询任务状态 → 下载结果/错误文件。
- **约束**：单文件 ≤ 50,000 请求且 ≤ 500 MB；所有请求必须使用相同模型与 `enable_thinking` 设置。

### 4. 智能路由
- **调用方式**：与普通模型完全一致，仅需将 `model` 替换为 `auto-model-xxxxxx`，使用 `maas.aliyuncs.com` 域名。
- **验证路由**：响应头 `x-dashscope-resolved-model` 返回实际执行的模型名；响应体 `model` 字段亦为实际模型。

## 限制和注意事项

- **协议与地域限制**：
  - 智能路由**仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**（`/v1/chat/completions`），不支持 DashScope 协议、Anthropic 协议、Batch、Embedding 等非生成接口；**仅限北京、新加坡地域**；**必须使用 `maas.aliyuncs.com` 域名**（`dashscope.aliyuncs.com` 不支持）。
  - 批量推理**不支持流式响应**，结果文件中无 `reasoning_content` 字段，如需思考过程请改用实时 API。

- **模型兼容性**：
  - [Token](../concepts/token.md) 按量部署**仅支持 LoRA 微调模型**，且需满足 rank=8/16/32/64、词汇表/对话模板未修改、视觉模型 VIT 冻结等约束，详见 [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)。
  - 智能路由对请求参数敏感：设置 `response_format` 或 `enable_search` 时，系统**仅路由到支持该参数的备选模型**；设置 `max_tokens` 会强制转换为 `max_completion_tokens` 并过滤不支持模型。

- **性能与计费**：
  - 吞吐预留/PTU/DTU 在额度内提供稳定 TPS（通常比标准 API 高 1.5~2 倍），但**超出额度后若选「自动溢出」，性能可能下降并受公共限流影响**，此时响应头含 `x-dashscope-ptu-overflow:true`。
  - 批量推理虽成本低，但**无实时性保障**，任务处理时间取决于后台队列负载，不适合对延迟敏感的场景。

- **运维与生命周期**：
  - 吞吐预留/PTU/DTU/智能路由均为预付费服务，**到期后有 2 小时宽限期**（可调用、可续费），超时 14 小时后资源释放不可恢复（8 小时时段预留无宽限）。
  - [Token](../concepts/token.md) 按量部署**一个月不使用将自动释放**，且扩容需人工审核，不支持自助扩缩容。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)


