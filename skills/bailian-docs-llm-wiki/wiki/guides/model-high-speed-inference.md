# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化场景的推理加速能力，涵盖实时高速输出（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型路由。各方案在性能、确定性、成本和接入复杂度上形成梯度，开发者应根据业务流量特征（可预测性/峰谷比）、SLA 要求（TPS/首字延迟/99% P99）及成本敏感度进行选型。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，提供 1.5~2 倍于标准 API 的 TPS。支持 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等模型，能力与原版模型一致，但需使用专用 model ID 和接入域名 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM 预留）与 PTU 部署**：通过预置输入/输出 TPM 容量锁定专属推理资源，保障高峰期不被限流。支持 Qwen、GLM、DeepSeek 等主流系列，如 `qwen3.8-max`、`glm-5.2`、`deepseek-v4-flash` 等 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **DTU 独占算力部署**：以物理 GPU 隔离为前提，提供最高性能确定性，支持超长上下文与自定义性能指标（如首字延迟）。适用于对数据隔离、微调模型部署或极致延迟有要求的场景 [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。
- **批量推理（Batch）**：异步处理大批量非实时请求，成本约为实时推理的 50%。支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen-vl-ocr` 等文本、多模态及向量模型，但结果文件不返回 `reasoning_content` 字段 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：基于请求内容动态匹配备选模型集（如 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813`），实现效果与成本的自动平衡，仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 `maas.aliyuncs.com` 域名 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 7（PTU 部署）中列出的 `qwen3.7-flash-2026-07-15` 模型标注“联系商务经理开通”，而文档 2（吞吐预留）明确将其列为华北2（北京）支持模型。该矛盾表明模型开通状态可能随地域或时间动态变化，实际使用前请以控制台实时列表为准。

## 关键参数

| 参数 | 说明 | 影响范围 |
|------|------|----------|
| `model` | 必填。指定推理模型或服务标识：<br>- Prime 模式：`glm-5.2-fast-preview`<br>- 吞吐预留/PTU/DTU：专属生成的 model code（如 `ptu-xxx`）<br>- Batch：JSONL 中 `body.model` 字段<br>- 智能路由：固定前缀 `auto-model-xxxx` | 全局生效，决定底层调度路径与计费模型 |
| `stream` | 控制响应格式。Prime 模式下[流式输出](../concepts/streaming-output.md)时需分别解析 `delta.reasoning_content` 与 `delta.content` 字段 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) | 影响客户端解析逻辑与首字延迟感知 |
| `enable_thinking` | 控制是否启用深度思考模式。Batch 场景下即使设为 `true`，结果文件也**不包含** `reasoning_content` 字段；实时 API 才返回完整思考过程 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) | 仅影响 token 计费与输出字段，不影响模型核心能力 |
| `input_tpm` / `output_tpm` | 吞吐预留与 PTU 部署的核心配置，单位 kTPM（千 Token/分钟）。容量计算器建议值需结合 RPM、平均输入/输出长度及缓存命中率估算 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) | 直接决定预留容量上限与费用 |
| `response_format` / `max_completion_tokens` | 智能路由的过滤参数：仅路由至支持该参数的备选模型。设置 `max_tokens` 会自动转换为 `max_completion_tokens` [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) | 触发实时过滤，缩小实际候选模型集 |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime model ID，并使用专属域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
- **吞吐预留/PTU/DTU**：在控制台创建后获取专属 `model code`，API 请求中直接替换 `model` 参数即可，接入零改造。PTU 实例支持叠加容量包，DTU 支持 PD 分离计算模式 [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。
- **批量推理**：构造符合规范的 JSONL 文件（UTF-8 编码、每行一个请求、含 `custom_id`），通过控制台或 API 提交任务，异步下载结果文件。
- **智能路由**：调用方式与普通模型完全一致，仅需将 `model` 设为 `auto-model-xxxx`，响应头 `x-dashscope-resolved-model` 标明实际执行模型。
- **Token 按量部署**：仅支持 LoRA 微调模型，API 部署时 `plan="lora"`，`capacity` 参数必须填写但无效；扩容需人工审核 [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)。

## 限制和注意事项

- **模型兼容性**：Batch 推理不支持 `qwen3.8-max` 的纯文本输入（仅支持多模态输入），且所有 Batch 结果均无 `reasoning_content` 字段，此为硬性限制 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **缓存行为**：Prime 模式与吞吐预留均支持前缀缓存，但智能路由**不保障缓存命中率**，因其请求可能被路由至不同模型，仅当连续请求命中同一模型且满足其缓存条件时才可能生效 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **协议与域名约束**：智能路由**仅支持** `maas.aliyuncs.com` 域名与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，不支持 `dashscope.aliyuncs.com` 或 DashScope 协议；同时禁用 `top_p`、`temperature`、`tool_choice` 等 12 个参数，设置即报错 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **部署与调用隔离**：在百炼调优后的模型，部署成功后**仅能使用其所在业务空间的 API Key 调用，且目前仅支持 DashScope SDK 方式，不支持 OpenAI 兼容方式** [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)。
- **预热与限流**：吞吐预留实例在请求量快速拉升时存在短暂预热期，期间可能出现延迟波动，建议客户端实现请求排队或重试机制 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)


