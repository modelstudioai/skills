# model high speed inference

百炼平台提供多种高吞吐、低延迟的模型推理能力，核心包括 Prime 模式（轻量级加速）、吞吐预留（专属容量保障）、独占吞吐（DTU）与智能路由（动态选模）。这些能力面向对输出速度、稳定性或成本效率有明确要求的生产场景，开发者可根据业务负载特征（如 TPS 峰值、长输入比例、缓存命中率、成本敏感度）选择最适配方案。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，TPS 提升至标准 API 的 1.5~2 倍。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型一致，无需额外参数，仅需指定对应 model ID 即可启用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（PTU）**：为指定模型锁定专属推理容量，支持标准模式（TPS 与标准 API 相同）和高速模式（TPS 提升 1.5~2 倍）。华北2（北京）和新加坡地域均支持 Qwen3.8-Max、Qwen3.7-Plus、GLM-5.2、DeepSeek-v4-Flash 等主流模型；但部分模型（如 GLM-5.3、DeepSeek-v4.1-Flash）在高速模式下暂不支持 [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。
- **独占吞吐（DTU）**：提供物理隔离的 GPU 资源，按输入/输出 TPM 计费，适用于需极致性能与数据隔离的场景。支持 `qwen3.7-plus-2026-05-26`、`glm-5.2`、`deepseek-v4-flash-0731` 等新发布模型，其性能基准（如首字延迟、每 token 延迟）在缓存命中率为 0% 条件下已实测 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。
- **智能路由**：通过 `auto-model-xxxxxxx` model-code 动态匹配最优备选模型，支持效果优先与成本优先两种策略。当前版本 `model-router-20260908` 的备选集包含 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813` 等 10 余个模型，所有备选模型均支持思考模式 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **批量推理（Batch）**：适用于非实时场景，成本约为实时推理的 50%。支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash` 等系列模型，单次请求上下文最大支持 256K tokens，但结果文件不返回 `reasoning_content` 字段 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

> **注意**：文档 3（吞吐预留概述）中称 GLM-5.3 在高速模式下“不支持”，而文档 1（Prime 模式）明确列出 `glm-5.3-prime` 为可用模型。实际以控制台支持列表为准，`glm-5.3-prime` 是 Prime 模式下的独立 model ID，不属于吞吐预留高速模式范畴，二者属不同产品线。

## 关键参数

- **`model` 参数**：是启用高速能力的核心标识。Prime 模式使用专用 model ID（如 `glm-5.2-fast-preview`）；吞吐预留使用专属 model code（如 `ptu-default-xxxx`）；智能路由使用 `auto-model-xxxxxxx`；DTU 部署后生成的 model code 用于调用。
- **`service_tier` 响应字段**：用于验证是否命中预留容量。返回 `ptu_default` 表示命中标准模式预留，`ptu_fast` 表示命中高速模式预留；若该字段缺失或为 `null`，则请求走按量计费 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **`provisioned_tokens` 与 `cached_tokens`**：`provisioned_tokens` 表示本次请求消耗的**折算后**预留容量（单位 token），已计入长输入阶梯系数与缓存折算系数；`cached_tokens` 表示输入中命中前缀缓存的 token 数，用于评估缓存收益 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **容量单位 kTPM**：1 kTPM = 1,000 Tokens/分钟。吞吐预留与 DTU 均以此为计量单位，输入/输出容量需分别购买。输入起步 200 kTPM（步长 10），输出起步 20 kTPM（步长 1） [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。

## 使用方式

- **Prime 模式**：直接将 `model` 参数设为对应 model ID（如 `glm-5.2-fast-preview`），使用标准兼容域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），无需修改其他参数 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：在控制台创建预留后获取专属 model code，调用时将其填入 `model` 参数。必须使用 OpenAI Chat 兼容或 Anthropic 兼容协议；若使用 Responses 协议，当前**不消耗预留容量，按量计费** [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。
- **DTU / MU 部署**：通过控制台或 API 创建专属服务，部署成功后获得 model code。调用时 `model` 参数即为此 code，其余参数（如 `messages`、`stream`）与标准 API 完全一致 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。
- **智能路由**：创建后获取 `auto-model-xxxxxxx` code，调用方式与普通模型完全相同，仅替换 `model` 参数即可，客户端零代码改动 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **批量推理**：需构造 JSONL 文件，每行一个请求对象，`body` 中 `model` 字段指定目标模型（如 `qwen-max`），通过 `/v1/batch/jobs` 接口提交任务 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 限制和注意事项

- **模型能力一致性**：Prime 模式与吞吐预留高速模式下的模型能力、使用限制（如上下文长度、支持的参数）与原版模型完全相同，但计费逻辑独立 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **缓存与长输入折算**：吞吐预留的容量消耗非原始 token 数，而是经“长输入阶梯系数”放大与“缓存折算系数”折扣后的折算值。例如 `qwen3.7-flash` 输入 50K 且无缓存命中时，实际消耗约 86 kTPM；若前 30K 命中缓存（系数 0.2），则消耗降至约 62 kTPM [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **协议兼容性限制**：吞吐预留专属 model code 经 Responses 协议调用不消耗预留容量；Anthropic 兼容格式暂不返回 `cached_tokens` 字段；智能路由仅支持 `maas.aliyuncs.com` 域名，不支持 `dashscope.aliyuncs.com` [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)、[长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)、[智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **计费与生命周期**：吞吐预留预付费按天/8 小时一次性扣费，即使未调用也全额产生；按小时后付费在删除实例或容量归零时立即停止计费；Token 按量部署若一个月内不使用将自动释放 [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)、[Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)。

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
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


