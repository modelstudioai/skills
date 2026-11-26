# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的高速推理能力，核心包括 Prime 模式（轻量级加速）、吞吐预留（容量保障）、批量推理（异步降本）及机密推理（安全增强）。所有方案均兼容 OpenAI 等主流协议，无需修改业务代码即可接入。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景优化，TPS 提升至标准 API 的 1.5~2 倍。支持文本生成模型（如 `glm-5.2-fast-preview`、`glm-5.3-prime`）和视频生成模型（如 `wan3.0-video-prime`），能力与原版模型完全一致，仅推理链路加速 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（高速模式）**：为指定模型锁定专属推理容量，推理速度相比标准模式提升 1.5~2 倍，适用于高并发、低延迟场景。支持 `Qwen3.8-Max`、`Qwen3.7-Plus-2026-05-26`、`GLM-5.2`、`DeepSeek-v4-Pro` 等主流模型，但 `GLM-5.3` 和 `Qwen4-Max` 在华北2（北京）暂不支持高速模式 [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。
- **批量推理**：异步处理大批量请求，成本约为实时推理的 50%，适用于模型评测、数据标注等非实时场景。支持 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3.7-flash` 等系列模型，单次请求上下文最大支持 256K token [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **机密推理**：基于 TEE 硬件级可信执行环境，全程加密计算，保障提示词与输出隐私。当前支持 `cmaas-qwen3.8-flash`、`cmaas-glm-5.3`、`cmaas-deepseek-v4-flash-0731` 等模型，部署后通过专用 SDK 调用 [机密推理](../../raw/model-user-guide/model-high-speed-inference/confidential-inference.md)。

> **注意**：文档 2 中表格显示 `GLM-5.3` 在华北2（北京）“高速模式”列为 ×，但文档 1 的 Prime 模式价格表明确列出 `glm-5.3-prime` 模型。二者定位不同：Prime 是轻量 API 层加速，吞吐预留高速模式是底层资源独占加速。两者不冲突，但不可混用——调用 `glm-5.3-prime` 不消耗吞吐预留容量。

## 关键参数

- **Prime 模式**：无额外参数，仅需将 `model` 设为对应 Prime 模型 ID（如 `glm-5.2-fast-preview`），接入域名使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
- **吞吐预留**：创建时需指定 `推理模式`（标准/高速）、`付费周期`（预付费/按天 或 后付费/按小时）、`输入/输出容量`（单位 kTPM，起步 200/20，步长 10/1），以及 `溢出策略`（默认自动溢出，超出部分转按量计费）[创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。
- **批量推理**：JSONL 文件中每个请求必须包含 `custom_id`（唯一标识）、`method`（固定为 `POST`）、`url`（如 `/v1/chat/completions`）和 `body`（与实时 API body 结构一致），且同一文件内所有请求须使用相同模型及 `enable_thinking` 设置 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **机密推理**：调用必须使用专用 SDK（非 DashScope/OpenAI 官方 SDK），`model` 参数为部署生成的 `cmaas-*` 模型 Code，域名固定为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，不支持 `dashscope.aliyuncs.com`。

## 使用方式

- **Prime 模式**：直接替换 `model` 参数发起调用，示例：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model": "glm-5.2-fast-preview", "messages": [{"role": "user", "content": "你是谁"}]}'
  ```
- **吞吐预留**：创建成功后获取专属 `模型 code`，在任意兼容协议（OpenAI Chat、Anthropic Messages）中将其设为 `model` 值。关键验证字段为响应中的 `service_tier`（`ptu_fast` 表示命中高速预留）和 `provisioned_tokens`（折算后消耗量）[创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。
- **批量推理**：通过控制台或 API 提交 JSONL 文件，任务完成后下载结果文件（含成功响应）和错误文件（含失败详情）。不返回 `reasoning_content` 字段，如需思考过程请使用实时 API [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **机密推理**：部署后使用 [机密推理 SDK](https://github.com/dashscope/dashscope-)，调用方式与普通 SDK 类似，但需传入 `workspace` 和 `region`，且 `model` 必须为 `cmaas-*` 格式 Code。

## 限制和注意事项

- **Prime 模式**：不改变模型能力与限制，仅加速输出；`wan3.0-video-prime` 计费按输入/输出视频秒数，而非 token [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留**：长输入与前缀缓存会显著影响实际容量消耗——50K 输入可能因阶梯系数放大至 86 kTPM，而缓存命中可使其降至 27.5 kTPM。务必使用 [TPM 容量计算器](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) 并结合折算规则估算 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **批量推理**：不支持流式响应；`qwen3.8-max` 等模型默认开启思考模式，若无需思考内容，必须显式设置 `enable_thinking=false`，否则成本增加 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **通用限制**：所有高速方案均不支持 Responses 协议的容量保障（文档 10 明确指出 Responses 调用 `不消耗预留容量`）；智能路由（`auto-model-*`）虽能自动选模，但其本身不提供加速，仅优化效果与成本，不属于“高速推理”范畴。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [机密推理](../../raw/model-user-guide/model-high-speed-inference/confidential-inference.md)


