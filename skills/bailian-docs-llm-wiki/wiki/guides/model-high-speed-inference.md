# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（专属容量保障）、独占吞吐（DTU）与智能路由（动态选模）。这些能力在不改变 API 接口的前提下，通过模型标识（model code）、域名或协议切换即可启用，适用于 AI 编程助手、Agent 多步推理、实时对话、批量评测等对输出速度或稳定性敏感的生产场景。

## 支持的模型/功能

- **Prime 模式**：专为输出速度优化的轻量级加速方案，TPS 提升至标准 API 的 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)明确指出其“按 token 计费，计费逻辑与标准 API 一致”，且“模型支持的能力、使用限制与原版模型相同”。
- **吞吐预留（TPM Reservation）**：为指定模型锁定专属推理容量，支持标准模式与高速模式两种推理模式。高速模式同样提供 1.5~2 倍 TPS 提升，但需预购 kTPM（千 Token/分钟）额度。支持模型范围更广，如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.2`、`deepseek-v4-flash-0731` 等，详见 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md) 中的地域与模式兼容性表格。
- **独占吞吐（DTU）**：物理隔离的独占算力部署，按输入/输出 TPM 额度×时长计费，性能保障最强。支持 `qwen3.8-flash`、`glm-5.3-flash`、`deepseek-v4-pro-0813` 等新发布模型，其基准 TPM 和性能指标（如首字延迟、每 token 延迟）在 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md) 中有详细表格。
- **智能路由**：动态分析请求内容，在预设备选模型集中自动匹配最优模型（如 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813`），兼顾效果与成本。仅支持文本输入，调用 model-code 固定为 `auto-model-xxxxxxxx` 格式，详见 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 3（吞吐预留概述）中列出 `GLM-5.3` 在华北2（北京）支持“高速模式 ×”，但文档 1（Prime 模式）明确列出 `glm-5.3-prime` 为可用模型。这表明 `glm-5.3-prime` 是 Prime 模式下的专用 model ID，而吞吐预留的“高速模式”是另一套独立容量体系，二者不可混用。开发者应根据实际需求选择：追求极致简单提速用 Prime；需容量保障与精细控制用吞吐预留。

## 关键参数

- **`model`**：核心参数，决定所用加速路径：
  - Prime 模式：使用 `glm-5.2-fast-preview` 等专用 model ID；
  - 吞吐预留：使用控制台生成的专属 model code（如 `tpu-xxxxx`）；
  - DTU：使用部署后生成的 deployed_model code（如 `qwen3-8b-ft-xxx`）；
  - 智能路由：使用 `auto-model-xxxxxxxx`。
- **`service_tier`**（响应字段）：用于验证是否命中预留容量。值为 `ptu_fast` 表示消耗高速模式预留容量，`ptu_default` 表示标准模式，`null` 或缺失表示未命中，走按量计费。该字段在 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) 的 API 查看部分有明确定义。
- **`provisioned_tokens`**（响应字段）：本次请求消耗的**折算后**预留容量（单位：token），已包含长输入阶梯放大与前缀缓存折扣，是判断容量是否充足的唯一准确依据。
- **`cached_tokens`**（响应字段）：本次请求中命中前缀缓存的输入 token 数，用于评估缓存收益。

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime model ID，并使用专属接入域名 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`。流式调用时需注意 `delta.reasoning_content` 与 `delta.content` 分离推送。
- **吞吐预留**：创建后获取专属 model code，在 OpenAI Chat 兼容或 Anthropic 协议中替换 `model` 参数即可。**必须使用 `compatible-mode/v1` 或 `/apps/anthropic/v1/messages` 路径**；`/v1/responses` 协议不消耗预留容量，[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md) 明确说明“专属模型 code 经 Responses 协议调用，当前不消耗预留容量、按量计费”。
- **DTU / 专属部署**：通过控制台或 API 创建部署服务，获取 deployed_model code 后，以标准 OpenAI SDK 或 DashScope SDK 调用，`model` 参数即为该 code。
- **智能路由**：创建后获得 `auto-model-xxxxxxxx` code，调用方式与普通模型完全一致，仅需替换 `model` 参数，支持 OpenAI Chat Completions、Responses 及 Anthropic Messages 协议。

## 限制和注意事项

- **模型能力一致性**：Prime 模式与原版模型能力完全一致，[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) 强调“模型支持的能力、使用限制与原版模型相同”。但吞吐预留、DTU 等部署模式可能因规格不同导致实际性能（如首字延迟）存在差异，需参考各文档中的性能基准表。
- **容量折算复杂性**：吞吐预留的 kTPM 消耗非线性。长输入超出阶梯边界（如 `qwen3.7-flash` >32K 部分）会按系数放大（3x），而缓存命中部分则按系数折扣（如 `glm-5.2` 为 0.25）。购买前务必使用 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) 提供的 TPM 容量计算器并手动上浮估算值。
- **协议与域名约束**：智能路由**仅支持 `maas.aliyuncs.com` 域名**，不支持 `dashscope.aliyuncs.com`；吞吐预留的 Responses 协议不生效；所有高速模式均要求使用业务空间专属域名（`{workspace_id}.{region}.maas.aliyuncs.com`），而非通用 `dashscope.aliyuncs.com`。
- **计费与退订**：吞吐预留与 DTU 均为预付费，创建即扣全款，“即使从未调用，费用也全额产生、不按实际用量退减”；首月内退订按日单价 1.2 倍结算。Token 按量部署虽“不使用不计费”，但一个月无调用将被自动释放。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


