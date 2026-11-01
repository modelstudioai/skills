# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与确定性性能的推理加速方案，涵盖模型级优化（如 Prime 模式）、容量保障机制（如吞吐预留/PTU/DTU）以及智能调度策略（如智能路由）。所有方案均基于标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK，无需修改核心调用逻辑，开发者可按业务 SLA 要求（TPS、首字延迟、缓存命中率、成本敏感度）选择最适配的组合。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，提供 1.5~2 倍于标准 API 的 TPS。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型完全一致，仅推理链路深度优化 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（TPM 预留）与 PTU 部署**：为指定模型锁定专属推理容量，保障高峰期不受公共限流影响。支持 Qwen、GLM、DeepSeek、Kimi 等主流系列，包括 `qwen3.8-max`、`glm-5.2`、`deepseek-v4-flash-0731` 等数十种模型 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **DTU 独占算力部署**：提供物理隔离的 GPU 资源，支持超长上下文（最高 1M token）与微调模型部署，适用于对数据隔离、低延迟和高并发有强要求的场景，支持 `qwen3.7-plus-2026-05-26`、`glm-5.2`、`deepseek-v4-flash` 等模型 [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **智能路由**：动态匹配请求内容至备选集中最优模型，支持效果优先与成本优先两种策略，当前版本 `model-router-20260908` 包含 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813` 等 10+ 模型 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  
- **批量推理**：异步处理大批量非实时请求，成本约为实时推理的 50%，支持 `qwen3.8-max`、`qwen3.7-plus`、`text-embedding-v3` 等文本生成与向量模型 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

> **注意**：文档 2（吞吐预留）与文档 4（专属部署概述）在“PTU”定义上存在表述差异：前者称 PTU 为“预置吞吐单元”，后者将其归类为“预置吞吐”部署方式；实际功能一致，均指通过预付费锁定 TPM 容量的专属服务。以[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)为准，其为当前统一管理入口。

## 关键参数

| 参数 | 说明 | 适用方案 | 备注 |
|------|------|----------|------|
| `model` | 指定模型标识符 | 所有方案 | Prime 模式使用 `glm-5.2-fast-preview`；吞吐预留/PTU 使用专属 `model code`；智能路由固定为 `auto-model-xxxx`；批量推理需在 JSONL `body.model` 中显式指定 |
| `input_tpm` / `output_tpm` | 预留输入/输出吞吐量（单位：kTPM） | 吞吐预留、PTU、DTU | DTU 与 PTU 均按此计量，但 DTU 基准值由模型规格决定，PTU 可自由配置 |
| `enable_thinking` | 控制是否启用思考模式 | Prime、批量推理、DTU/PTU | 设置为 `true` 时返回 `reasoning_content` 字段；批量推理结果中**不包含该字段**，即使设置为 `true` [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| `stream` | 是否启用流式响应 | Prime、标准 API | Prime 模式[流式输出](../concepts/streaming-output.md)时，`delta.reasoning_content` 与 `delta.content` 分别推送思考与回答内容 |
| `x-dashscope-resolved-model` | 响应头，标识实际执行模型 | 智能路由 | 用于验证路由生效及调试，计费依据此模型 |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime 模型 ID（如 `glm-5.2-fast-preview`），并使用兼容模式域名 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`。  
- **吞吐预留 / PTU**：在控制台创建后获取专属 `model code`，替换 API 请求中的 `model` 参数即可；支持自动溢出（超量转按量）或仅预留容量（超量返回 429）两种溢出策略 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **DTU**：部署成功后同样获得专属 `model code`，调用方式与 PTU 一致；支持自定义性能指标（如首字延迟、每 token 延迟）与 PD 分离计算模式。  
- **智能路由**：创建后获取 `auto-model-xxxx` code，直接用于 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用；**仅支持 `maas.aliyuncs.com` 域名与 `/compatible-mode/v1` 路径**，不支持 `dashscope.aliyuncs.com` [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  
- **批量推理**：上传 JSONL 文件提交[异步任务](../concepts/asynchronous-task.md)，文件内每行一个请求对象，`body` 结构与实时 API 完全一致；结果文件中 `choices[0].message` 仅含 `content` 和 `role` 字段，无 `reasoning_content` [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 限制和注意事项

- **计费刚性**：吞吐预留、PTU、DTU 均为预付费模式，**部署成功即开始计费，与是否调用无关**；未调用仍全额产生费用，退订时已使用部分按 1.2 倍系数结算 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **[Token](../concepts/token.md) 按量部署限制**：仅支持 LoRA 微调模型，不支持全参微调或基础模型；一个月不使用将自动释放；扩容需人工审核，不支持自助操作 [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)。  
- **智能路由限制**：仅支持文本 Chat Completions；不支持 `top_p`、`temperature`、`logprobs`、`stop` 等采样与控制参数；`max_tokens` 会自动转换为 `max_completion_tokens`，仅路由到支持该参数的模型 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  
- **模型导入约束**：从 OSS 导入 LoRA 模型时，`rank` 必须为 8/16/32/64 之一，且所有层必须一致；视觉模型必须冻结 VIT，否则校验失败 [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)。  
- **Prime 模式特殊行为**：调用量达限流值时，若平台仍有剩余资源，则**不会触发限流**，实际可用 TPS 不低于限流值；但此行为不改变计费逻辑，仍按实际输入/输出 token 计费 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)


