# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（专属容量保障）、独占吞吐（DTU）与智能路由（动态选模）。这些能力在不改变 API 调用方式的前提下，通过模型标识（model code）、专属域名或路由策略实现性能提升，适用于 AI 编程助手、Agent 多步推理、实时对话及批量评测等场景。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，TPS 提升至标准 API 的 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型一致，但计费单价更高（如华北2 北京地区 `glm-5.2-fast-preview` 输出单价 ¥56/百万 [Token](../concepts/token.md)）[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（TPM Reservation）**：为指定模型锁定专属推理容量，支持标准模式与高速模式两种推理路径。高速模式同样提供 1.5~2 倍 TPS 提升，且支持按小时后付费（如 `qwen3.8-max` 高速模式输入单价 ¥2.88/kTPM·小时）[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。  
- **独占吞吐（DTU）**：物理隔离的独占算力方案，按输入/输出 TPM 计费，提供最高等级性能保障与自定义规格（如 `qwen3.5-122b-a10b` Fast 规格基准输出 TPM 达 904,000），适用于对延迟和稳定性要求极高的生产环境 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **智能路由**：基于请求内容动态匹配最优备选模型（如 `qwen3.8-flash`、`deepseek-v4-pro-0813` 等），兼顾效果与成本，仅需使用固定前缀 `auto-model-xxxx` 的 model code 即可调用。  
- **批量推理**：异步处理大批量请求，成本约为实时推理的 50%，支持 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等主流文本与多模态模型，但结果文件不包含 `reasoning_content` 字段。  

> **注意**：文档 3（吞吐预留概述）中称 `GLM-5.3` 在华北2（北京）“高速模式”列显示为 ×，但文档 1（Prime 模式）明确列出 `glm-5.3-prime` 为可用模型。实际支持以控制台展示为准，`glm-5.3-prime` 是 Prime 模式的专用 model ID，其底层即对应 GLM-5.3 的高速推理能力，二者逻辑一致，非矛盾。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 启用高速能力的核心标识：Prime 模式用 `glm-5.2-fast-preview`；吞吐预留用专属 `model code`（如 `ptu-fast-xxx`）；智能路由用 `auto-model-xxxx` | `"glm-5.2-fast-preview"` |
| `service_tier` | 响应头字段，用于确认是否命中预留容量：`ptu_fast` 表示消耗高速模式预留容量，`ptu_default` 表示标准模式 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md) | `"ptu_fast"` |
| `provisioned_tokens` | 响应中实际消耗的折算后 token 数（已含长输入阶梯放大与缓存折算），位于 `usage.prompt_tokens_details.provisioned_tokens` 等路径 | `{"prompt_tokens_details": {"provisioned_tokens": 27500}}` |
| `cached_tokens` | 输入中命中前缀缓存的 token 数，直接影响容量消耗，位于 `usage.prompt_tokens_details.cached_tokens` | `{"prompt_tokens_details": {"cached_tokens": 30000}}` |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime model ID（如 `glm-5.2-fast-preview`），并使用专属域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。  
- **吞吐预留**：创建后获取专属 `model code`，在任意兼容协议（OpenAI Chat、Anthropic、DashScope）中替换 `model` 参数即可。必须使用 `maas.aliyuncs.com` 域名（如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），`dashscope.aliyuncs.com` 域名不支持预留容量 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。  
- **DTU / MU 部署**：通过控制台或 API 部署后，获得 `deployed_model`（即 model code），调用时 `model` 参数填此值，其余参数与标准 API 完全一致。  
- **智能路由**：调用时 `model` 设为 `auto-model-xxxx`，响应体 `model` 字段返回实际执行的模型名，便于效果追踪。  
- **批量推理**：上传 JSONL 文件（每行一个请求），`body` 中 `model` 字段填目标模型（如 `qwen-max`），不支持 `enable_thinking=true` 时返回 `reasoning_content`。  

## 限制和注意事项

- **Prime 模式无额外限流豁免**：虽有“特殊限流”描述，但本质仍是公共资源池内的优先调度，不提供容量独占保障；若需确定性容量，请选用吞吐预留或 DTU。  
- **吞吐预留容量消耗按折算计算**：长输入（如 >32K）按阶梯系数放大（如 `qwen3.7-flash` 超出部分 ×3），缓存命中部分按系数折扣（如 `glm-5.2` ×0.25），实际消耗可能显著偏离原始 token 数 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。  
- **协议兼容性限制**：  
  - 吞吐预留的 `model code` 经 `/v1/responses` 端点调用**不消耗预留容量，按量计费**；必须使用 `/v1/chat/completions` 或 `/apps/anthropic/v1/messages`。  
  - 智能路由**不支持 `dashscope.aliyuncs.com` 域名**，仅限 `maas.aliyuncs.com`。  
- **模型能力继承**：所有高速模式均完全继承基础模型的能力与限制（如上下文长度、多模态支持），Prime 模式与吞吐预留高速模式均不新增功能。  
- **计费叠加**：吞吐预留内调用不收 [Token](../concepts/token.md) 费，但超出部分按“自动溢出”策略转为按量计费；DTU/Prime 等模式费用与 [Token](../concepts/token.md) 费用相互独立，不可抵扣。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)


