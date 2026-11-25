# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（TPM 专属容量保障）、批量推理（异步低成本）及智能路由（动态模型选型）。所有方案均基于标准 API 协议兼容设计，开发者可按业务 SLA、成本敏感度与运维复杂度需求选择组合。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景优化，TPS 提升至标准 API 的 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型一致，但计费按 token 细粒度拆分（输入/输出/缓存命中）[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（TPM Reservation）**：为指定模型锁定专属推理容量，支持**标准模式**（TPS 与标准 API 相同）和**高速模式**（TPS 提升 1.5~2 倍），覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。  
- **批量推理（Batch Inference）**：异步处理大批量请求，成本约为实时推理的 50%，适用于模型评测、数据标注等非实时场景，支持 qwen3/4 系列、Qwen-VL、向量模型等 [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **智能路由（Auto-Model Routing）**：通过 `auto-model-xxxxxx` model-code 动态匹配最优备选模型，支持“效果优先”与“成本优先”策略，当前备选集含 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813` 等十余款模型。  

> **注意**：文档 2 中表格显示 `GLM-5.3` 在华北2（北京）**不支持高速模式**，但文档 1 明确列出 `glm-5.3-prime` 为 Prime 模式支持模型。二者逻辑一致（Prime 是吞吐预留高速模式的轻量实现），但术语需统一——实际使用中 `glm-5.3-prime` 即对应 GLM-5.3 的高速推理能力，无需额外创建吞吐预留实例。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 启用加速能力的核心标识符 | `"glm-5.2-fast-preview"`（Prime）、`"your-dedicated-model-code"`（吞吐预留）、`"auto-model-abcd1234"`（智能路由） |
| `service_tier`（响应字段） | 标识是否命中预留容量 | `"ptu_fast"`（高速模式预留）、`"ptu_default"`（标准模式预留）、`null`（未命中，走公共池） |
| `provisioned_tokens`（响应字段） | **折算后**消耗的预留容量（含长输入阶梯放大与缓存折扣） | `usage.prompt_tokens_details.provisioned_tokens`（输入侧） |
| `cached_tokens`（响应字段） | 输入中命中前缀缓存的 token 数 | `usage.prompt_tokens_details.cached_tokens` |

> **注意**：吞吐预留的容量消耗是**折算值**，非原始 token 数。例如 `qwen3.7-flash` 输入 50K 且无缓存时，因长输入阶梯系数（(32K,256K] 区间为 3x）实际消耗 86 kTPM；若前 30K 命中缓存（系数 0.2），则消耗降至 62 kTPM [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。

## 使用方式

1. **Prime 模式**：直接调用 `model` 为 Prime 专用 ID 的接口，无需修改 endpoint 或 header。接入域名格式为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`。  
2. **吞吐预留**：在控制台创建后获取专属 `model code`，将其替换至请求中的 `model` 字段即可。支持 OpenAI Chat 兼容、Anthropic、OpenAI Responses 三种协议，但 Responses 协议**不消耗预留容量**（按量计费）[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。  
3. **批量推理**：上传 JSONL 文件（每行一个 POST 请求对象），指定 `/v1/chat/completions` 或 `/v1/embeddings` endpoint，系统异步执行并返回结果文件。  
4. **智能路由**：使用 `auto-model-xxxxxx` model-code 发起标准 OpenAI Chat Completions 请求，响应体中 `model` 字段返回实际执行的模型名，`usage` 字段记录真实 token 消耗。

## 限制和注意事项

- **Prime 模式限流**：虽有特殊限流机制（资源充足时不触发），但**仍受账号级 RPM/TPM 配额约束**，超限将返回 429。  
- **吞吐预留容量折算**：购买的 kTPM 容量按长输入阶梯系数与缓存折算系数动态计算，务必使用控制台“以折算容量观测”开关查看真实利用率；超出部分按溢出策略处理（默认自动转按量计费）。  
- **模型兼容性**：  
  - Prime 模式与吞吐预留高速模式**不支持思考模式（reasoning_content）的流式分片推送**，但响应体仍包含完整 `reasoning_content` 字段（见文档 1 返回示例）。  
  - 批量推理结果文件**不包含 `reasoning_content` 字段**，如需思考过程必须使用实时 API 调用。  
- **地域与协议限制**：智能路由仅支持 `maas.aliyuncs.com` 域名，不支持 `dashscope.aliyuncs.com`；吞吐预留的 Anthropic 协议必须使用业务空间专属域名（`{workspaceId}.{region}.maas.aliyuncs.com`）。  
- **计费差异**：Prime 按 token 计费；吞吐预留预付费容量内不另收 token 费，溢出部分才按量计费；批量推理与智能路由均为纯按量计费。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


