# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化场景的推理加速能力，涵盖 Prime 模式（轻量级提速）、吞吐预留（PTU/DTU 专属容量）、批量推理（异步离线处理）及智能路由（动态模型选型）。所有方案均兼容 OpenAI 接口，开发者可通过统一 API 调用，按需选择性能、确定性与成本的最优平衡点。

## 支持的模型/功能

百炼支持三类核心高速推理能力，覆盖实时、准实时与离线场景：

- **Prime 模式**：为标准 API 提供约 1.5~2 倍 TPS 提升，无需修改代码逻辑，仅需指定专用 model ID（如 `glm-5.2-fast-preview`）即可启用。该模式适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的实时交互场景 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（TPM 预留）**：通过预购输入/输出 TPM 容量锁定专属推理资源，保障业务高峰期不受公共限流影响。支持「标准模式」（与标准 API 同性能）和「高速模式」（即 PTU，TPS 提升 1.5~2 倍），并可选溢出策略（自动降级至按量计费或严格限流返回 429）[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **批量推理（Batch）**：异步处理大批量非实时请求，成本约为实时推理的 50%，适用于模型评测、数据标注等离线任务。支持千问、GLM、DeepSeek 等主流文本生成与多模态模型，且单次请求上下文最大支持 256K token [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。  
- **智能路由**：基于请求内容动态匹配备选模型集中的最优模型（如 `qwen3.8-flash` 或 `glm-5.2`），实现效果与成本的自动权衡，调用时仅需使用 `auto-model-xxxx` 类型 model-code [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 2 与文档 8 在 PTU 的归属描述上存在不一致——文档 2 明确指出“PTU 的创建与管理现已支持在「吞吐预留」页面进行”，而文档 8 开头仍称“已迁移至[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面操作；专属部署页面提供前往入口”。二者实质指向同一功能入口，但文档 8 的表述易引发路径混淆，应以文档 2 的权威说明为准。

## 关键参数

不同加速方案依赖的关键参数如下，开发者需根据场景准确配置：

| 方案 | 关键参数 | 说明 |
|------|----------|------|
| **Prime 模式** | `model` | 必须使用 Prime 专用 model ID（如 `glm-5.2-fast-preview`），不可混用标准模型名；接入域名需为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` |
| **吞吐预留 / PTU / DTU** | `input_tpm`, `output_tpm`, `performance_mode` | 创建时需明确指定输入/输出 TPM 数值及性能模式（`standard` 或 `high_speed`）；专属模型 code 由系统生成，必须用于 API 的 `model` 字段 |
| **批量推理** | `custom_id`, `enable_thinking`, `url` | JSONL 文件中每行必须含唯一 `custom_id`；`enable_thinking` 为 `body` 顶层字段（非 `extra_body` 内）；`url` 固定为 `/v1/chat/completions` 或 `/v1/embeddings` |
| **智能路由** | `model`, `response_format`, `max_tokens` | `model` 必须为 `auto-model-xxxx` 格式；`response_format` 和 `max_tokens`（自动转为 `max_completion_tokens`）会触发实时过滤，仅路由至支持该参数的备选模型 |

## 使用方式

### 1. Prime 模式（零改造接入）
直接替换 `model` 参数，保持原有请求结构：
```bash
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你好"}]}'
```

### 2. 吞吐预留（专属容量）
- 在控制台创建吞吐预留 → 获取专属 `model code` → 替换 API 中的 `model`；
- 流量超出预留时，按创建时选择的溢出策略处理（默认自动降级为按量计费）；
- 首次大流量突增需注意短暂预热期，建议客户端实现重试机制 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

### 3. 批量推理（异步提交）
- 构建 UTF-8 编码 JSONL 文件（≤50,000 行，≤500 MB），每行含 `custom_id`, `method`, `url`, `body`；
- 通过控制台或 API 提交任务；
- **注意**：批量结果文件不返回 `reasoning_content` 字段，如需思考过程请改用实时 API 调用 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

### 4. 智能路由（动态选型）
- 创建服务获取 `auto-model-xxxx` code；
- 调用时仅替换 `model`，其余参数透传；
- 响应头 `x-dashscope-resolved-model` 标明实际执行模型，便于监控与计费核验。

## 限制和注意事项

- **模型兼容性**：Prime 模式与吞吐预留支持的模型列表不同。例如，`kimi-k3.1-pro` 仅在吞吐预留中明确列出支持，而未出现在 Prime 模式文档的模型表中 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)；批量推理明确不支持 `qwen3.5-omni-plus` 的语音输出 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **计费刚性**：吞吐预留（PTU/DTU）为预付费模式，创建成功即开始计费，与是否调用无关；即使未发起任何请求，费用也全额产生 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **协议与域名约束**：智能路由**仅支持 `maas.aliyuncs.com` 域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），**不支持 `dashscope.aliyuncs.com`**；且仅兼容 OpenAI Chat Completions 协议，不支持 DashScope 原生协议、Anthropic 协议、Batch、Embedding 等 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **缓存行为差异**：Prime 模式和吞吐预留支持前缀缓存（见文档 8 的长输入阶梯系数），但智能路由**不保障缓存命中率**，因其请求可能被路由至不同模型，仅依赖各备选模型自身的隐式缓存机制 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **参数限制**：智能路由禁用 `top_p`, `temperature`, `stop`, `tool_choice`, `thinking_budget` 等 12 个参数，设置将导致运行报错；而 Prime 模式中 `glm-5.2` 的 `thinking_budget` 参数在调用时不生效 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


