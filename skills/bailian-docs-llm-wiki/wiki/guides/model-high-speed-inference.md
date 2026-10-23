# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，涵盖 API 层优化（如 Prime 模式）、资源层保障（如吞吐预留/PTU/DTU）和架构层智能调度（如智能路由）。所有方案均基于 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，无需修改客户端核心逻辑，开发者可根据业务对性能、成本、确定性与运维复杂度的要求进行选型。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，通过底层调度优化实现 TPS 提升 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型一致，但需使用特定 model ID 调用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM 预留）**：为指定模型锁定专属推理容量，保障高峰期服务稳定性。支持 Qwen3.x、GLM-5.x、DeepSeek-v4.x、Kimi-K2.6 等主流文本模型，以及部分视频生成模型 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **专属部署模式**：包括 PTU（预置吞吐）、DTU（独占吞吐）和 Token 按量三种计费方式。PTU 和 DTU 均提供物理或逻辑资源隔离，DTU 还支持自定义性能指标与 PD 分离计算；Token 按量仅支持 LoRA 微调模型，适用于效果验证阶段 [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。
- **智能路由**：动态分析请求内容，在预设备选模型集中自动匹配最优模型执行。当前支持 `qwen3.8-max`、`qwen3.7-flash`、`deepseek-v4-pro-0813`、`glm-5.2` 等模型，仅限北京与新加坡地域的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **批量推理（Batch）**：异步处理大批量非实时请求，成本约为实时推理的 50%。支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等模型，单次请求上下文最大支持 256K token [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

> **注意**：文档中关于 `glm-5.2` 的思考模式参数 `thinking_budget` 存在矛盾。[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 明确指出该参数“在调用时不生效”，而 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) 又说明其在思考模式下生效。实际使用时，请以具体部署模式的文档为准：PTU/DTU 部署不支持 `thinking_budget`，标准 API 或 Prime 模式下需结合 `enable_thinking=true` 使用。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `model` | 所有模式 | 必填。值为具体模型 ID（如 `glm-5.2-fast-preview`）、专属模型 code（如吞吐预留生成的 code）、或智能路由 code（如 `auto-model-abcd1234`）。 |
| `stream` | 实时推理 | 布尔值。流式响应需设为 `true`；Prime 模式流式返回时，思考内容通过 `delta.reasoning_content` 字段推送 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。 |
| `enable_thinking` | 思考模式 | 布尔值。开启后模型将生成思考过程，产生额外 `reasoning_tokens` 并按输出单价计费。部分模型（如 Qwen3.x 系列）默认开启，建议显式设置 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。 |
| `response_format` | 智能路由 | 仅当备选模型支持该参数时才参与路由；否则请求将被拒绝 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。 |
| `max_tokens` | 智能路由 | 自动转换为 `max_completion_tokens`，仅路由到支持该参数的备选模型 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。 |

## 使用方式

1. **API 调用通用流程**：
   - 使用正确的 Base URL：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（智能路由、Prime、吞吐预留等均需此域名）或 `https://dashscope.aliyuncs.com/api/v1`（专属部署 API 创建）。
   - 在请求头中携带 `Authorization: Bearer $API_KEY`。
   - 请求体中 `model` 字段填入对应模式的标识符（模型 ID、专属 code 或路由 code）。

2. **各模式接入要点**：
   - **Prime 模式**：无需额外参数，直接使用 `glm-5.2-fast-preview` 等专用 model ID 即可启用。
   - **吞吐预留**：创建成功后获取专属 `model code`，替换 API 请求中的 `model` 参数；注意首次调用量激增时存在短暂预热期 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
   - **PTU/DTU 专属部署**：部署成功后获取 `deployed_model`（即 model code），用于推理调用；部署时需指定 `plan`（`ptu`/`mu`/`lora`）及相应容量参数 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。
   - **智能路由**：创建后获得 `auto-model-xxxxxx` code，直接作为 `model` 参数传入；响应头 `x-dashscope-resolved-model` 返回实际执行模型 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
   - **批量推理**：通过控制台或 API 提交 JSONL 文件，文件内每行一个请求对象，`body` 中必须包含 `model` 字段且全文件统一 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 限制和注意事项

- **地域限制**：吞吐预留、PTU、DTU、智能路由均仅支持华北2（北京）和新加坡地域；批量推理在两地均支持，但模型列表略有差异。
- **协议限制**：智能路由**仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（`/v1/chat/completions`），不支持 DashScope 原生协议、Anthropic 协议及 `/v1/embeddings` 等非生成接口 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **缓存行为**：Prime 模式、吞吐预留、PTU 均支持前缀缓存并提供缓存折扣；智能路由因模型动态切换，**不保障缓存命中率**，仅依赖实际路由模型自身的隐式缓存机制 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **参数兼容性**：智能路由明确禁用 `top_logprobs`、`logit_bias`、`stop`、`tool_choice`、`temperature` 等 10 余个参数，设置将导致报错 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **模型导入约束**：LoRA 模型导入要求 `rank` 为 8/16/32/64，词汇表与对话模板不可修改，视觉模型必须冻结 VIT；全参微调模型导入需白名单 [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)。
- **计费叠加**：吞吐预留/PTU/DTU 的溢出策略若设为“自动溢出”，超出部分将按标准按量计费，费用叠加产生；智能路由本身不收费，仅按实际路由模型计费。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


