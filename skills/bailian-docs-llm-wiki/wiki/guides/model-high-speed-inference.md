# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与确定性性能的推理加速能力，覆盖从 API 层优化（如 Prime 模式）、容量保障（吞吐预留/PTU/DTU）、异步批量处理到[智能模型路由](../concepts/model-routing.md)的完整技术栈。所有方案均基于标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，无需修改客户端核心逻辑即可接入，适用于 AI 编程助手、实时对话、内容审核、批量标注等对速度、稳定性或成本敏感的生产场景。

## 支持的模型/功能

百炼支持以下四类高速推理能力，适用模型与能力范围各异：

- **Prime 模式**：专为输出速度敏感场景设计，TPS 较标准 API 提升 1.5~2 倍，**仅限特定模型变体**，如 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等。其模型能力、限制与原版完全一致，但需使用专属 model ID 调用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（含 PTU）**：通过预付费锁定专属 TPM 容量，保障高峰期服务不被公共限流影响。支持“标准模式”（与标准 API 吞吐一致）和“高速模式”（即 PTU，TPS 提升 1.5~2 倍）。支持模型包括 `Qwen3.8-Max`、`GLM-5.3`、`DeepSeek-v4-Pro`、`Kimi-K2.6` 等数十个主流模型 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **独占部署（DTU/MU）**：物理隔离的 GPU 资源部署，提供最高性能确定性与最低延迟。DTU 按输入/输出 TPM 计费，MU 按模型单元（MU）数量计费，均支持基础模型与 LoRA 微调模型。典型支持模型有 `qwen3.7-plus-2026-05-26`、`glm-5.2`、`deepseek-v4-flash-0731` 等 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **智能路由**：动态分析请求内容，在预设备选模型集中自动匹配最优模型（效果优先或成本优先），实现效果与成本的帕累托最优。当前支持 `qwen3.8-flash`、`kimi-k3`、`qwen3.7-plus`、`glm-5.2` 等十余个文本模型，且支持忙闲时分时计费 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  

> **注意**：文档 12 明确指出“PTU 的创建与管理已迁移至[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面”，而文档 6 和文档 4 中仍存在指向旧“专属部署控制台”的入口描述，实际操作应以吞吐预留页面为准，避免路径混淆。

## 关键参数

不同高速方案的核心控制参数如下：

| 方案 | 关键参数 | 说明 | 示例值 |
|------|----------|------|--------|
| **Prime 模式** | `model` | 必须指定 Prime 专属 model ID，无额外参数 | `"glm-5.2-fast-preview"` |
| **吞吐预留 / PTU** | `input_tpm`, `output_tpm`, `performance_mode` | 预留输入/输出吞吐量（单位 kTPM），`performance_mode` 为 `"standard"` 或 `"high_speed"` | `"input_tpm": 10000, "output_tpm": 1000, "performance_mode": "high_speed"` |
| **DTU** | `input_tpm`, `output_tpm` | DTU 按基准 TPM 的整数倍购买，各模型有固定基准值 | `qwen3.5-27b`: 基准输入 2,432,000 TPM，至少购 1 倍 |
| **MU** | `deploy_spec`, `capacity` | `deploy_spec` 如 `"MU1"`，`capacity` 为副本数 | `"deploy_spec": "MU1", "capacity": 4` |
| **Token 按量部署** | `plan="lora"`, `capacity` | 仅支持 LoRA 模型，`capacity` 参数无效但必须填写 | `"plan": "lora", "capacity": 1` |
| **智能路由** | `model` | 固定前缀 `auto-model-` + 8 位随机字符 | `"auto-model-abcd1234"` |

所有方案均支持 `stream: true/false` 控制是否流式响应；部分模型（如 GLM-5.2）在流式下需额外处理 `delta.reasoning_content` 字段 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。

## 使用方式

### 1. Prime 模式
直接替换 `model` 参数，使用专属 model ID 发起标准 `/chat/completions` 请求：
```bash
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你好"}]}'
```

### 2. 吞吐预留 / PTU / DTU
- **控制台**：在[吞吐预留页面](https://bailian.console.aliyun.com/cn-beijing/model/tpm-reservation)创建实例，获取专属 `model code`，替换 API 中的 `model` 参数。
- **API**：调用 `/api/v1/deployments` 接口，`plan` 设为 `"ptu"` 或 `"mu"`，传入对应容量参数 [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)。

### 3. Token 按量部署
仅支持 LoRA 模型，API 部署时 `plan="lora"`：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/deployments \
  -d '{"model_name":"qwen3-8b-ft-202511132025-0260","plan":"lora","name":"my_qwen8b"}'
```

### 4. 智能路由
创建后获得 `auto-model-xxxxxx` code，调用方式与普通模型完全一致，仅需替换 `model` 字段 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

### 5. 批量推理（Batch）
适用于非实时场景，上传 JSONL 文件异步执行，成本降低 50%。需确保文件内所有请求使用**相同模型及 `enable_thinking` 设置**，且结果文件中**不包含 `reasoning_content` 字段** [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

## 限制和注意事项

- **容量费用刚性**：吞吐预留、PTU、DTU、MU 均为预付费模式，**创建成功即开始计费，与是否调用无关**。未调用也全额产生费用，退订时已使用部分按 1.2 倍系数结算 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **模型兼容性限制**：  
  - Prime 模式仅支持明确列出的模型变体（如 `glm-5.2-fast-preview`），不可对任意模型启用。  
  - Token 按量部署**仅支持 LoRA 微调模型**，全参微调模型不支持 [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)。  
  - 批量推理中，即使设置 `enable_thinking=true`，结果文件也**不返回 `reasoning_content`**，需用实时 API 获取思考过程 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **地域与协议约束**：  
  - 智能路由**仅支持 `maas.aliyuncs.com` 域名**，不支持 `dashscope.aliyuncs.com`；且仅开放北京与新加坡地域 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  
  - 吞吐预留的 8 小时时段预留**不支持续订与宽限期**，到期后立即失效 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **性能预热**：吞吐预留实例在流量快速拉升时需短暂预热，期间可能出现延迟波动，建议客户端实现请求排队或重试机制 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **缓存与长输入**：PTU/DTU 支持长输入阶梯系数与前缀缓存折扣，但具体系数因模型而异（如 `qwen3.7-flash-2026-07-15` 输入超 32K 后系数升至 3x），需结合计算器评估额度需求 [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)


