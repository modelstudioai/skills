# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（专属容量保障）、批量推理（异步低成本）及独占算力部署（物理隔离高性能）。开发者可根据业务对实时性、稳定性、成本与资源隔离的要求，选择合适的技术路径。

## 支持的模型/功能

- **Prime 模式**：适用于对输出速度敏感的实时场景（如 AI 编程助手、Agent 多步推理），支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`kimi-k3.1-pro-prime`、`wan3.0-video-prime` 等模型，TPS 提升至标准 API 的 1.5~2 倍 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（TPU）**：为指定模型锁定专属推理容量，分**标准模式**（TPS 与标准 API 相同）和**高速模式**（TPS 提升 1.5~2 倍），支持 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.2`、`deepseek-v4-flash-0731`、`deepseek-v4-pro` 等主流模型，且两地域（北京/新加坡）支持情况存在差异 [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。  
- **批量推理（Batch）**：适用于非实时、高性价比场景（如模型评测、数据标注），支持 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-omni-flash` 等文本与多模态模型，成本约为实时推理的 50% [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **独占算力部署（DTU/MU）**：提供物理隔离的 GPU 资源，DTU 按输入/输出 TPM 计费（新模型首选），MU 按模型单元数量计费（旧模型沿用），均支持基础模型与 LoRA 微调模型，性能可定制 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **智能路由**：动态匹配请求内容与备选模型集（如 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813`），自动选择效果或成本最优模型，仅支持文本输入与 OpenAI/Anthropic 兼容协议 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 3（吞吐预留概述）中明确列出 `GLM-5.3` 在华北2（北京）**不支持高速模式**，但文档 14（DTU）价格表中却包含 `glm-5.3` 的 `Fast` 规格并标注“起售价格(元/月)”。该矛盾表明 DTU 的 `Fast` 规格并非等同于吞吐预留的“高速模式”，而是 DTU 自身的性能规格命名，二者属不同产品线，不可直接对标。实际使用时应以各产品控制台展示的支持状态为准。

## 关键参数

| 参数 | 含义 | 说明 |
|------|------|------|
| `model` | 模型标识符 | Prime 模式使用专用 model ID（如 `glm-5.2-fast-preview`）；吞吐预留使用专属 `model code`；智能路由固定为 `auto-model-xxxxxx`；DTU/MU 部署后生成唯一 `deployed_model` ID。 |
| `service_tier` | 计费层级标识 | 响应体顶层字段，`ptu_default` 表示命中吞吐预留标准模式，`ptu_fast` 表示命中高速模式，`null` 表示未命中而走按量计费 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。 |
| `provisioned_tokens` | 折算后消耗容量 | 单次请求实际消耗的预留容量（单位：token），已应用长输入阶梯系数与缓存折算系数，见 `usage.prompt_tokens_details.provisioned_tokens` 等路径 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。 |
| `cached_tokens` | 缓存命中 token 数 | 输入中复用前缀缓存的 token 数量，用于验证缓存收益，仅 OpenAI Chat/DashScope 原生协议返回 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。 |
| `enable_thinking` | 思考模式开关 | 批量推理中需在 JSONL `body` 顶层显式设置（不能放 `extra_body`），开启后产生额外 `reasoning_tokens` 并增加成本；但批量结果文件**不返回** `reasoning_content` 字段 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。 |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime 模型 ID（如 `glm-5.2-fast-preview`），调用域名与标准 API 一致（`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`）[Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留**：创建后获取专属 `model code`，调用时将其作为 `model` 参数值，协议支持 OpenAI Chat、Anthropic Messages、OpenAI Responses（但 Responses 不消耗预留容量）[创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。  
- **批量推理**：构造 UTF-8 编码 JSONL 文件（每行一个请求，含 `custom_id`、`method`、`url`、`body`），通过控制台或 API 提交任务；`body` 中模型与思考模式须全文件统一 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **DTU/MU 部署**：通过 API 或控制台部署后，使用返回的 `deployed_model`（非 `name`）作为 `model` 参数调用；DTU 需指定 `input_tpm`/`output_tpm`，MU 需指定 `deploy_spec` 与 `capacity` [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。  
- **智能路由**：将 `model` 设为 `auto-model-xxxxxx`，其余参数与普通模型完全一致，响应中 `model` 字段返回实际执行的模型名 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

## 限制和注意事项

- **容量折算复杂性**：吞吐预留的 kTPM 消耗非原始 token 数，受**长输入阶梯系数**（如 `qwen3.7-flash` >32K 输入部分 ×3）和**缓存折算系数**（如 `glm-5.2` 命中部分 ×0.25）双重影响，务必使用 [TPM 容量计算器](https://help.aliyun.com/zh/model-studio/tpm-reservation-long-input#tpm-long-input-calc-h2) 估算并监控 `provisioned_tokens` 字段 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。  
- **协议兼容性限制**：吞吐预留的 `Responses` 协议调用**不消耗预留容量**；智能路由**不支持 DashScope 原生协议**；批量推理**不返回 `reasoning_content`**，需实时 API 获取思考过程 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **模型与地域约束**：同一模型在不同地域支持的推理模式可能不同（如 `GLM-5.3` 在北京不支持吞吐预留高速模式，但在新加坡未明确说明）；视频模型 `wan3.0-video-prime` 计费按**秒数**而非 token [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **计费与生命周期**：吞吐预留预付费按天/8小时扣费，**创建即全额扣费，无论是否调用**；DTU/MU 预付费退订按 1.2 倍日单价结算；Token 按量部署若一个月不使用将**自动释放** [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)


