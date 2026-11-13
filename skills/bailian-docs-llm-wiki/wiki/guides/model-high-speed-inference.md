# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化的推理加速方案，涵盖实时高速响应（Prime 模式、吞吐预留/PTU）、异步批量处理（Batch Inference）及智能资源调度（智能路由）。各方案在模型支持、计费粒度、容量保障强度和接入方式上存在明确分工，开发者应根据业务流量特征（可预测性/突发性）、SLA 要求（TPS/首字延迟）及成本敏感度进行选型。

## 支持的模型/功能

百炼为不同场景提供分层加速能力：

- **Prime 模式**：专为输出速度敏感场景设计，通过底层优化将 TPS 提升至标准 API 的 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等模型，能力与原版模型完全一致，无需额外参数，仅需指定对应 model ID 即可启用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（含 PTU）**：为指定模型锁定专属推理容量，保障高峰期不受公共限流影响。支持 Qwen、GLM、DeepSeek、Kimi 等数十款主流模型，包括 `qwen3.8-max`、`glm-5.2`、`deepseek-v4-pro` 等；其中选择“高速模式”即为 PTU 部署，同样提供 1.5~2 倍 TPS 提升 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **批量推理（Batch Inference）**：适用于非实时场景，成本约为实时推理的 50%。支持千问全系列（Max/Plus/Flash/Long）、多模态模型（`qwen3-vl-plus`）、向量模型（`text-embedding-v4`）等，单次请求上下文最大支持 256K token [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：动态分析请求内容，在预设备选集中自动匹配最优模型，兼顾效果与成本。当前支持 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813` 等十余款模型，按实际路由模型计费 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 7（PTU）与文档 2（吞吐预留）存在表述重叠。文档 7 明确指出：“在控制台中，PTU 的创建与管理已迁移至[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面操作”，因此 PTU 已不再作为独立部署模式存在，而是吞吐预留的一种性能模式（“高速模式”），开发者应统一通过吞吐预留页面配置。

## 关键参数

| 方案 | 核心参数 | 说明 |
|------|----------|------|
| **Prime 模式** | `model` | 必须使用专用 model ID（如 `glm-5.2-fast-preview`），不可混用标准模型名；接入域名需为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| **吞吐预留/PTU** | `input_tpm`, `output_tpm`, `performance_mode` | 输入/输出 TPM（单位：kTPM）决定容量上限；`performance_mode` 为 `"standard"` 或 `"high_speed"`；溢出策略（`auto_overflow` 或 `only_reserved`）决定超量行为 |
| **批量推理** | `custom_id`, `enable_thinking`, `url` | JSONL 文件中每行必须含唯一 `custom_id`；`enable_thinking` 为顶层字段，不能置于 `extra_body`；`url` 必须为 `/v1/chat/completions` 或 `/v1/embeddings` |
| **智能路由** | `model`（固定前缀）, `routing_strategy` | `model` 必须为 `auto-model-xxxxxxx` 格式；`routing_strategy` 在创建时选定（`EFFECT_FIRST` 或 `COST_FIRST`），不可运行时修改 |

## 使用方式

- **Prime 模式**：直接调用兼容 OpenAI 的 `/chat/completions` 接口，仅需将 `model` 替换为 Prime 专用 ID，其余参数（`stream`、`messages` 等）与标准 API 完全一致。流式响应中思考内容通过 `delta.reasoning_content` 字段返回 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：创建成功后获取专属 `model code`，在 API 请求中替换 `model` 参数即可。首次调用存在短暂预热期，建议客户端实现请求排队或重试机制 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **批量推理**：通过控制台或 API 提交 JSONL 文件（UTF-8 编码，≤50,000 行，≤500 MB），系统异步处理并生成结果文件与错误文件；不返回 `reasoning_content` 字段，如需思考过程请使用实时 API [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：调用方式与普通模型完全一致，仅需将 `model` 设为 `auto-model-xxxxxxx`，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 Anthropic 协议；响应体中 `model` 字段标识实际执行模型，便于验证路由效果 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

## 限制和注意事项

- **容量与计费刚性**：吞吐预留、PTU、DTU 均为预付费模式，创建成功即开始计费，与是否发起调用无关；即使零调用，费用也全额产生。务必使用 TPM 容量计算器预估需求，避免资源浪费 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **模型能力约束**：批量推理不支持返回 `reasoning_content`，即使设置 `enable_thinking=true`；同时，`qwen3.5-omni-plus` 等部分模型在 Batch 场景下不支持语音输出 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **地域与协议限制**：智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`）地域，且**仅支持 `maas.aliyuncs.com` 域名**，不支持 `dashscope.aliyuncs.com`；调用协议仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat Completions/Responses）与 Anthropic 协议 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **部署模式不可变**：服务创建后无法更改计费方式（如从 Token 按量切换至 PTU），必须先下线原服务，再以新计费方式重新部署 [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)


