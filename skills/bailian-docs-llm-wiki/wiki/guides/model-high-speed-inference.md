# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化的推理加速能力，覆盖实时高速响应（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型调度（智能路由）四大技术路径。所有方案均基于 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，无需修改客户端核心逻辑即可接入。

## 支持的模型/功能

百炼支持的高性能推理能力按场景分为四类：

- **Prime 模式**：专为输出速度敏感场景设计，TPS 较标准 API 提升 1.5~2 倍，适用于 AI 编程助手、Agent 多步推理与实时对话等。支持模型包括 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM 预留）与 PTU/DTU 部署**：通过预置专属推理容量保障业务高峰期稳定性。支持模型覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列，如 `qwen3.8-max`、`glm-5.2`、`deepseek-v4-flash` 等 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **批量推理（Batch）**：适用于非实时场景（如模型评测、数据标注），成本约为实时推理的 50%。支持文本生成、多模态理解（Qwen-VL）、向量嵌入（`text-embedding-v*`）等模型，但 `qwen3.8-max` 在新加坡地域**当前仅支持多模态输入，暂不支持纯文本输入** [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：动态匹配请求内容至最优备选模型，支持效果优先或成本优先策略。当前仅限文本 Chat Completions，且必须使用 `maas.aliyuncs.com` 域名与 OpenAI 兼容协议 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 3 明确指出 `qwen3.8-max` 在新加坡地域“当前仅支持多模态输入，暂不支持纯文本输入”，而文档 7 的 PTU 价格表中该模型在新加坡地域未标注此限制。实际调用时应以 Batch 文档的明确约束为准，避免因地域差异导致请求失败。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `model` | 全场景 | Prime 模式需指定专用 model ID（如 `glm-5.2-fast-preview`）；吞吐预留/PTU/DTU 需替换为专属 model code；智能路由固定为 `auto-model-xxxxxx`；Batch 中各请求须使用相同 model。 |
| `stream` | Prime / 实时部署 | 流式响应时，`glm-5.2` 系列会分别推送 `delta.reasoning_content` 与 `delta.content` 字段。 |
| `enable_thinking` | Batch / 实时部署 | 控制是否开启思考模式。Batch 场景下即使设为 `true`，结果文件**不包含 `reasoning_content` 字段**，需改用实时 API 获取 [原文标题](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。 |
| `input_tpm` / `output_tpm` | 吞吐预留 / PTU / DTU | 预留或购买的吞吐容量单位（kTPM 或 TPM），决定服务上限。PTU 与 DTU 均按输入/输出 TPM 分别计费。 |
| `response_format` / `max_tokens` | 智能路由 | 路由时将实时过滤不支持该参数的备选模型；`max_tokens` 会被自动转换为 `max_completion_tokens` 并用于筛选。 |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime 模型 ID，并使用 `maas.aliyuncs.com` 域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。  
- **吞吐预留 / PTU / DTU**：创建后获取专属 `model code`，在 API 请求中替换 `model` 参数。PTU 已整合至吞吐预留控制台管理；DTU 与 MU 部署需通过专属部署控制台或 API 创建 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。  
- **批量推理**：上传 JSONL 文件（每行一个请求，含 `custom_id`, `method`, `url`, `body`），通过控制台或 API 提交任务；结果通过下载文件获取，不支持流式响应。  
- **智能路由**：调用方式与普通模型完全一致，仅需将 `model` 替换为 `auto-model-xxxxxx`，并确保使用 `maas.aliyuncs.com` 域名与 OpenAI SDK。响应头 `x-dashscope-resolved-model` 返回实际执行模型。  

## 限制和注意事项

- **计费刚性**：吞吐预留、PTU、DTU、MU 均为预付费模式，**部署成功即开始计费，与是否调用无关**；未调用仍全额产生费用 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **缓存行为差异**：Prime 模式支持缓存（见 `usage.prompt_tokens_details.cached_tokens`）；智能路由**不支持显式缓存参数**，仅依赖底层模型的隐式缓存，命中率不可控；Batch 推理不返回缓存相关字段。  
- **模型能力继承**：所有加速模式均继承原模型的能力与限制（如上下文长度、输入类型支持），例如 `qwen3.8-max` 在 Batch 中支持 256K token 上下文，但新加坡地域不支持纯文本输入。  
- **协议与域名约束**：智能路由**仅支持 `maas.aliyuncs.com` 域名与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，不支持 `dashscope.aliyuncs.com` 或 DashScope 协议；Batch 也仅支持 OpenAI 兼容格式。  
- **错误处理**：智能路由故障自动切换默认启用，但对 429（限流）、400/403/500 等确定性错误**不触发切换**，错误直接透出；PTU/DTU 溢出策略可选「自动溢出至按量」或「仅预留容量返回 429」。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [PTU 预置吞吐部署](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


