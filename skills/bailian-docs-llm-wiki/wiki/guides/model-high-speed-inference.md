# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与确定性性能的推理加速方案，涵盖 Prime 模式（轻量级提速）、吞吐预留（TPM 专属容量）、专属部署（PTU/DTU/MU）、批量推理（异步降本）及智能路由（动态选模）。各方案在性能保障强度、计费粒度、接入复杂度和适用场景上存在显著差异，开发者应根据业务流量特征（可预估性/峰谷比）、SLA 要求（延迟/TPS/稳定性）及成本敏感度进行选型。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景优化，提供 1.5~2 倍标准 API 的 TPS。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型完全一致，无需额外参数，仅需指定对应 model ID 即可启用 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM 预留）**：为指定模型锁定专属推理容量，保障高峰期不受公共限流影响。支持 Qwen、GLM、DeepSeek、Kimi 等主流系列的数十个模型，包括 `qwen3.8-max`、`glm-5.2`、`deepseek-v4-pro` 等 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **专属部署**：提供三种模式：
  - **PTU（预置吞吐）**：按输入/输出 TPM 预付费，保障额度内不限速，TPS 提升约 1.5~2.0 倍，适用于高负载生产环境；
  - **DTU（独占吞吐）**：按输入/输出 TPM 计费，提供物理隔离资源，支持微调模型与自定义性能指标；
  - **Token 按量部署**：仅支持 LoRA 微调模型，不使用不计费，适用于效果验证等低成本场景 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。
- **批量推理（Batch）**：异步处理大批量非实时请求，成本约为实时推理的 50%。支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`text-embedding-v1` 等文本、多模态及向量模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：通过 `auto-model-xxxxxx` model-code 接入，自动匹配备选集中最优模型（如 `qwen3.8-max`、`qwen3.7-flash`、`deepseek-v4-flash-0731`），支持效果优先与成本优先两种策略 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档中对 `glm-5.2` 在 PTU 模式下的 `thinking_budget` 参数描述存在矛盾。[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 明确指出“GLM-5.2 的 `thinking_budget` 参数（限制思考长度）在调用时不生效”，而 [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md) 未提及此限制，且其价格表中明确列出 `qwen-plus-2025-12-01` 等模型区分“非思考/思考”模式计价。因此，`glm-5.2` 在 PTU 场景下不支持 `thinking_budget`，开发者应避免设置该参数。

## 关键参数

| 参数 | 适用方案 | 说明 | 注意事项 |
|------|----------|------|----------|
| `model` | 全部 | 指定模型标识符 | Prime 模式用 `glm-5.2-fast-preview`；吞吐预留/专属部署用专属 model code；智能路由用 `auto-model-xxxxxx` |
| `input_tpm` / `output_tpm` | 吞吐预留、PTU、DTU | 预留或购买的每分钟 Token 吞吐量 | 必须为基准值整数倍；DTU 购买时需同时满足输入/输出最低基准 |
| `stream` | Prime、标准 API | 是否启用流式响应 | Prime 模式流式返回 `delta.reasoning_content` 和 `delta.content` 字段 |
| `enable_thinking` | Batch、专属部署 | 是否开启深度思考模式 | Batch 场景下即使设为 `true`，结果文件也不含 `reasoning_content` 字段 [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| `response_format` | 智能路由 | 指定响应格式（如 JSON Schema） | 智能路由会**仅路由到支持该参数的备选模型**，不支持则报错 |

## 使用方式

- **Prime 模式**：直接调用兼容 OpenAI 的 `/v1/chat/completions` 接口，`model` 参数设为 `glm-5.2-fast-preview` 等 Prime 模型 ID，接入域名格式为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`。
- **吞吐预留**：在控制台创建后获取专属 `model code`，替换 API 请求中的 `model` 参数即可，无需修改 endpoint 或其他 header。
- **专属部署（PTU/DTU/MU）**：部署成功后获得专属 `deployed_model` ID，调用时 `model` 参数即为此 ID；API 部署示例见 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。
- **批量推理**：上传符合规范的 JSONL 文件（每行一个请求对象），通过控制台或 API 提交任务；JSONL 中 `body` 字段需与 `/v1/chat/completions` 接口体结构一致。
- **智能路由**：将 `model` 参数设为生成的 `auto-model-xxxxxx` code，其余参数与普通 Chat Completions 完全一致；响应头 `x-dashscope-resolved-model` 返回实际执行的模型名。

## 限制和注意事项

- **Prime 模式**：无独立限流策略，但受业务空间整体配额约束；计费按实际输入/输出 token 计算，与标准 API 一致。
- **吞吐预留/PTU/DTU**：
  - 创建后立即开始计费，服务到期后有 2 小时宽限期（按天预留），超期 14 小时后释放；
  - 溢出策略为「自动溢出」时，超出部分转为按量计费，并在响应 Header 中返回 `x-dashscope-ptu-overflow:true`；
  - PTU 模式下，`glm-5.2` 的 `thinking_budget` 参数无效 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **批量推理**：
  - 不返回 `reasoning_content` 字段，即使请求中设置了 `enable_thinking=true`；
  - JSONL 文件单行 ≤ 1 MB，总文件 ≤ 500 MB，且同一文件内所有请求必须使用相同模型与 `enable_thinking` 设置；
  - 多模态请求的媒体 URL 必须为公网可访问地址，不支持本地路径或内网地址。
- **智能路由**：
  - 仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/v1/chat/completions`），**不支持 DashScope 协议、Anthropic 协议、Batch、Embedding 等其他接口**；
  - 不支持 `top_p`、`temperature`、`stop`、`logprobs` 等采样与控制类参数，设置将导致报错；
  - 缓存行为不可控：仅当请求被路由至同一模型且满足其缓存条件时才可能命中，不保障命中率。
- **通用限制**：所有高速推理方案均不支持通过 `dashscope.aliyuncs.com` 域名调用（智能路由明确要求 `maas.aliyuncs.com`），且 Token 按量部署仅支持 LoRA 微调模型，一个月不使用将自动释放。

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
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


