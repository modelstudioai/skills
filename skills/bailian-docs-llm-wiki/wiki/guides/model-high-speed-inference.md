# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（专属容量保障）、独占吞吐（DTU）与智能路由（动态选模）。这些能力在不改变 API 接口的前提下，通过模型标识（model 参数）、专属域名或路由策略实现性能提升，适用于 AI 编程助手、实时对话、Agent 多步推理等对输出速度敏感的场景。

## 支持的模型/功能

- **Prime 模式**：为特定模型提供 1.5~2 倍 TPS 提升，无需额外参数，仅需将 `model` 设为对应 Prime 模型 ID（如 `glm-5.2-fast-preview`）。支持文本与视频生成模型，但视频模型（如 `wan3.0-video-prime`）按秒计费，价格与分辨率强相关 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM Reservation）**：为指定模型锁定专属推理容量，分标准模式（TPS 与普通 API 一致）和高速模式（TPS 提升 1.5~2 倍）。支持 Qwen3.8-Max、Qwen3.7-Plus、GLM-5.2、DeepSeek-v4-Pro 等主流模型，但部分模型（如 GLM-5.3）在高速模式下暂未开放支持 [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。
- **独占吞吐（DTU）**：面向新发布模型的独占算力方案，按输入/输出 TPM 计费，提供物理隔离资源与可预期性能。支持 qwen3.8-flash、glm-5.3-flash、deepseek-v4-flash-0731 等模型，并明确标注各规格下的基准 TPM 与首字延迟等性能参考值 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。
- **智能路由**：通过 `auto-model-xxxxxx` 模型码自动匹配备选集中最优模型，支持效果优先与成本优先两种策略。当前仅支持文本输入，且备选模型必须已开通调用权限并满足配额要求 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **批量推理（Batch）**：异步处理大批量请求，成本约为实时推理的 50%，适用于模型评测、数据标注等非实时场景，支持 qwen3.8-max、qwen3.7-plus、qwen-vl-ocr 等数十种文本与多模态模型 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

> **注意**：文档 3（吞吐预留概述）中称 GLM-5.3 在华北2（北京）“高速模式”列显示为 ×，但文档 11（DTU）中明确列出 `glm-5.3-fast` 规格及对应 TPM 基准与价格。这表明 GLM-5.3 的高速能力实际通过 DTU 方案提供，而非吞吐预留的高速模式。开发者应以 DTU 文档为准进行选型。

## 关键参数

- **`model`**：核心路由参数。使用 Prime 模式时填入 Prime 模型 ID（如 `glm-5.2-fast-preview`）；使用吞吐预留时填入专属 `model code`；使用智能路由时填入 `auto-model-xxxxxx`；使用 DTU 部署后则填入部署生成的 `deployed_model` ID。
- **`service_tier`**：响应头字段，用于确认是否命中预留容量。返回 `ptu_default` 表示消耗标准模式预留，`ptu_fast` 表示消耗高速模式预留，`null` 或缺失表示按量计费 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **`provisioned_tokens`**：响应 `usage` 中的字段，表示本次请求已折算（含长输入阶梯放大与缓存折减）后实际消耗的预留容量 token 数，是判断容量是否充足的直接依据 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **`cached_tokens`**：响应 `usage.prompt_tokens_details.cached_tokens` 字段，表示输入中命中前缀缓存的 token 数，用于评估缓存收益 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **`enable_thinking`**：控制是否开启深度思考模式。在批量推理中，即使设置为 `true`，结果文件也不包含 `reasoning_content` 字段；如需获取思考过程，必须使用实时 API 调用 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 使用方式

- **Prime 模式**：直接调用兼容模式 endpoint（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`），`model` 参数设为 Prime 模型 ID 即可，无需修改其他参数或协议。
- **吞吐预留**：创建预留后获取专属 `model code`，将其替换到任意 OpenAI 兼容（Chat Completions、Responses）、Anthropic 或 DashScope 原生接口的 `model` 参数中。**注意**：通过 Responses 端点调用专属 `model code` 当前不消耗预留容量，仅 Chat Completions 和 Anthropic 协议有效 [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。
- **DTU / MU 部署**：通过 API 或控制台部署后，使用返回的 `deployed_model` ID 作为 `model` 参数调用，endpoint 与标准模型一致（如 `/v1/chat/completions`），但底层为独占资源。
- **智能路由**：将 `model` 参数设为 `auto-model-xxxxxx`，使用 `maas.aliyuncs.com` 域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不支持 `dashscope.aliyuncs.com` 域名 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **批量推理**：需构造符合规范的 JSONL 文件（UTF-8 编码，每行一个请求对象，含 `custom_id`, `method`, `url`, `body`），通过 Batch API 提交任务，结果异步下载 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 限制和注意事项

- **模型兼容性**：Prime 模式与吞吐预留的高速模式均不支持所有模型。例如，Qwen4-Max、DeepSeek-v4.1-Flash 在吞吐预留高速模式中明确标记为不支持；而 GLM-5.3 的高速能力仅通过 DTU 提供，不在吞吐预留高速模式列表中。
- **协议与域名约束**：吞吐预留的专属 `model code` 在 Responses 协议下不生效；智能路由强制要求使用 `maas.aliyuncs.com` 域名，禁用 `dashscope.aliyuncs.com`；批量推理仅支持 OpenAI 兼容与 Anthropic 协议，不支持 DashScope 原生协议。
- **计费与容量消耗**：吞吐预留的容量消耗按折算后值计算（长输入阶梯放大 + 缓存折减），购买的 kTPM 并非原始 token 数。务必通过控制台“以折算容量观测”查看利用率，或检查响应中的 `provisioned_tokens` 字段，避免因误判导致容量不足 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **[流式输出](../concepts/streaming.md)差异**：Prime 模式下，`glm-5.2-fast-preview` 流式响应中 `reasoning_content` 与 `content` 分别通过 `delta.reasoning_content` 和 `delta.content` 推送，需分别处理 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **批量推理限制**：`qwen3.8-max` 等系列模型在 Batch 场景下单次请求上下文最大支持 256K token；`qwen3.5-omni-plus` 不支持语音输出；且结果文件中永远不包含 `reasoning_content` 字段，此为设计限制 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


