# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化的推理加速方案，涵盖实时高速响应（Prime 模式）、专属容量保障（吞吐预留/PTU/DTU）、异步批量处理（Batch）及智能模型路由。各方案在性能、计费粒度、资源隔离性与接入方式上形成互补，开发者可根据业务流量特征、SLA 要求与成本敏感度进行选型。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，支持 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等模型，TPS 提升 1.5~2 倍，能力与原版模型一致 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（含 PTU）**：为指定模型锁定专属 TPM 容量，支持 `Qwen3.8-Max`、`GLM-5.3`、`DeepSeek-v4-Pro` 等数十种主流模型，性能模式可选“标准”或“高速”（即 PTU）[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **独占吞吐（DTU）与模型单元（MU）**：提供物理级资源隔离，DTU 按输入/输出 TPM 计费，MU 按模型单元数量×时长计费，均支持基础模型与 LoRA 微调模型部署 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **批量推理（Batch）**：适用于非实时场景，支持 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4` 等文本、多模态与向量模型，成本约为实时推理的 50% [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **智能路由**：通过 `auto-model-xxxxxx` 统一入口，动态匹配备选集内最优模型（如 `qwen3.8-flash`、`deepseek-v4-pro-0813`），支持效果优先与成本优先策略 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  

> **注意**：文档 9 明确指出“PTU 的创建与管理已迁移至[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面”，而文档 6 仍称“PTU 部署可在专属部署页面操作”。以文档 9 和文档 2 为准，PTU 已统一归入吞吐预留体系，专属部署控制台仅提供跳转入口。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `model` | 启用加速能力的核心标识符 | `"glm-5.2-fast-preview"`（Prime）、`"your-dedicated-model-code"`（吞吐预留）、`"auto-model-abcd1234"`（智能路由） | [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)、[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)、[智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) |
| `input_tpm` / `output_tpm` | 吞吐预留或 PTU 的容量配额（单位：kTPM） | `{"input_tpm": 10000, "output_tpm": 1000}` | [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md) |
| `enable_thinking` | 控制是否启用深度思考模式（影响 token 消耗与响应结构） | `true`（流式返回 `reasoning_content`）、`false`（仅 `content`） | [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)、[API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md) |
| `stream` | 是否启用流式响应（部分模式强制要求） | `true`（思考模式下必须设为 `true`） | [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) |

## 使用方式

- **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime 模型 ID（如 `glm-5.2-fast-preview`），并使用兼容模式域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留/PTU**：在控制台创建后获取专属 `model code`，替换 API 请求中的 `model` 字段；支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope SDK，调用方式与标准 API 完全一致 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **批量推理**：构造 UTF-8 编码的 JSONL 文件（每行一个请求，含 `custom_id`, `method`, `url`, `body`），通过控制台或 API 提交任务，结果异步生成 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **DTU/MU 部署**：通过控制台或 API 创建专属服务，获取 `deployed_model`（即 model code）后用于推理调用；DTU 需指定 `input_tpm`/`output_tpm`，MU 需指定 `deploy_spec` 与 `capacity` [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。  
- **智能路由**：将 `model` 设为 `auto-model-xxxxxx`，其余参数（`messages`, `stream` 等）与普通模型调用一致，响应中 `model` 字段返回实际执行模型 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  

## 限制和注意事项

- **容量预热与溢出**：吞吐预留实例在流量快速拉升时需短暂预热，期间可能出现延迟波动；溢出策略默认为“自动溢出至按量计费”，若选“仅使用预留容量”，超限请求将返回 HTTP 429 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **Batch 不返回思考内容**：即使 `enable_thinking=true`，批量推理结果文件中 `choices[0].message` 仅含 `content` 和 `role` 字段，不包含 `reasoning_content`；需实时 API 获取思考过程 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **计费刚性**：吞吐预留、DTU、MU 均为预付费模式，创建成功即开始计费，与实际调用量无关；提前退订已使用部分按 1.2 倍系数结算 [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)、[独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **模型兼容性**：[Token](../concepts/token.md) 按量部署仅支持 LoRA 微调模型，不支持全参微调或原始预置模型；批量推理对 `qwen3.5-omni-plus` 等模型有上下文长度（256K）与语音输出等特定限制 [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)、[批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)


