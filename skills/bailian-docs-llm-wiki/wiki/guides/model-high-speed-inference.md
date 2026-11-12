# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化场景的推理加速能力，包括 Prime 模式（轻量级提速）、吞吐预留/PTU（专属容量保障）、批量推理（异步降本）、专属部署（DTU/MU）及智能路由（动态选模）。所有方案均兼容 OpenAI 接口，开发者可根据流量特征、SLA 要求与预算灵活组合使用。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，TPS 提升 1.5~2 倍，支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型一致，无需额外参数，仅需指定对应 model ID 即可启用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（含 PTU）**：通过预置输入/输出 TPM 容量锁定专属推理资源，保障高峰期不被限流；支持“高速模式”（即 PTU），提供 1.5~2 倍 TPS 提升；支持模型包括 `Qwen3.8-Max`、`GLM-5.3`、`DeepSeek-v4-Pro` 等数十种主流模型 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **批量推理（Batch）**：适用于非实时场景，成本约为实时推理的 50%，支持 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4` 等文本、多模态与向量模型，单次请求上下文最大支持 256K token [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **专属部署（DTU/MU）**：提供物理隔离的独占 GPU 资源，DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费；支持基础模型与 LoRA 微调模型，性能指标（如首字延迟、每 token 延迟）在文档中有明确基准数据 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **智能路由**：基于请求内容自动匹配备选模型集中的最优模型，支持 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813` 等多档位模型，按实际执行模型计费，调用时仅需传入 `auto-model-xxxxxx` code [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 9 明确指出“PTU 的创建与管理已迁移至[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面”，而文档 6 仍称“PTU 可在专属部署页面操作”。以文档 9 为准，PTU 已统一归入吞吐预留体系，专属部署页仅提供跳转入口。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `model` | 指定推理模型或服务标识 | `"glm-5.2-fast-preview"`（Prime）、`"your-dedicated-model-code"`（吞吐预留）、`"auto-model-abcd1234"`（智能路由） | 必须与所选方案匹配；吞吐预留和专属部署生成的 model code 具有唯一性，不可复用 |
| `input_tpm` / `output_tpm` | 吞吐预留/PTU/DTU 的容量配额（单位：kTPM） | `10000`, `1000` | DTU 购买需为基准 TPM 的整数倍；PTU 支持长输入阶梯系数与缓存折扣计算 [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md) |
| `enable_thinking` | 控制是否启用深度思考模式 | `true` / `false` | Batch 场景下即使设为 `true`，结果文件中也不返回 `reasoning_content` 字段；流式 API 中需通过 `delta.reasoning_content` 获取 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| `stream` | 是否启用流式响应 | `true` | Prime 模式下流式响应需分别处理 `delta.reasoning_content` 与 `delta.content` 字段 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) |
| `plan` | API 部署时指定计费方式 | `"ptu"`, `"mu"`, `"lora"` | `"lora"` 仅支持 LoRA 微调模型，且 `capacity` 参数无效但必须填写 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md) |

## 使用方式

- **Prime 模式**：直接调用标准 `/v1/chat/completions` 接口，将 `model` 设为 Prime 模型 ID（如 `glm-5.2-fast-preview`），接入域名使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。  
- **吞吐预留/PTU**：在控制台创建预留后获取专属 `model code`，替换 API 请求中的 `model` 参数即可；支持自动溢出（超量转按量）或仅限预留容量（超量返回 429）两种策略。  
- **批量推理**：上传 JSONL 文件（每行一个 POST 请求对象），通过 `/v1/batches` 接口提交任务；文件需符合格式规范（UTF-8、≤50,000 行、每行 ≤1 MB），媒体 URL 必须公网可访问。  
- **专属部署（DTU/MU）**：通过控制台或 API（`POST /api/v1/deployments`）部署，指定 `plan` 为 `"dtu"` 或 `"mu"`，并传入对应容量参数；部署成功后使用返回的 `deployed_model` code 调用。  
- **智能路由**：调用时 `model` 设为 `auto-model-xxxxxx`，必须使用 `maas.aliyuncs.com` 域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不支持 `dashscope.aliyuncs.com`。

## 限制和注意事项

- **容量与计费刚性**：吞吐预留、DTU、MU 均为预付费模式，创建成功即开始计费，与实际调用量无关；未调用也全额收费，且提前退订按 1.2 倍系数结算 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **模型兼容性限制**：[Token](../concepts/token.md) 按量部署仅支持 LoRA 微调模型，不支持全参微调或原始基础模型；批量推理不返回 `reasoning_content`，如需思考过程请改用实时 API [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **地域与协议约束**：智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`）地域，且仅限 `maas.aliyuncs.com` 域名；不支持 DashScope 原生协议，仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Anthropic 协议 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  
- **预热与稳定性**：吞吐预留实例在流量快速拉升时需短暂预热，期间可能出现延迟波动，建议客户端实现请求排队或重试机制 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **OSS 导入限制**：LoRA 模型导入要求 `adapter_model.safetensors` 中不含 `visual.*` 类参数（即 VIT 必须冻结），且 `rank` 必须为 8/16/32/64 之一；不支持归档类 OSS 存储类型 [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


