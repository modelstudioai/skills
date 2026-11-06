# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与成本优化的推理加速能力，覆盖实时高速响应（Prime 模式、PTU/DTU 专属部署）、异步批量处理（Batch）、智能模型调度（智能路由）及自定义模型导入部署等场景。所有方案均兼容 OpenAI 接口，开发者可根据流量特征、SLA 要求、成本敏感度与模型可控性选择组合使用。

## 支持的模型/功能

百炼支持以下四类高并发/高性能推理能力，对应不同模型范围与适用场景：

- **Prime 模式**：专为输出速度敏感场景设计，TPS 较标准 API 提升 1.5~2 倍，适用于 AI 编程助手、Agent 多步推理、实时对话等。支持 `glm-5.2-fast-preview`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型，能力与原版模型一致，无需额外参数，仅需指定对应 model ID 即可启用 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
  
- **吞吐预留（PTU/DTU）**：通过预置输入/输出 TPM 容量锁定专属推理资源，保障高峰期不被公共限流影响。支持 Qwen、GLM、DeepSeek、Kimi 等主流模型，包括 `qwen3.8-max`、`glm-5.2`、`deepseek-v4-flash-0731` 等；其中 PTU 对应“高速模式”，DTU 为新一代独占吞吐单位 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **批量推理（Batch）**：适用于非实时、大批量离线任务（如模型评测、数据标注），成本约为实时推理的 50%。支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`text-embedding-v4` 等文本生成、多模态及向量模型，但结果文件不返回 `reasoning_content` 字段 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。

- **智能路由**：基于请求内容动态匹配最优模型，实现效果与成本的自动平衡。当前支持 `qwen3.8-flash`、`kimi-k3`、`glm-5.2`、`deepseek-v4-pro-0813` 等备选模型，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与文本 Chat Completions 场景 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 9 明确指出“PTU 的创建与管理现已支持在「吞吐预留」页面进行”，而文档 6 和文档 5 中仍存在指向旧入口（专属部署控制台）的描述，实际操作请以 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档为准。

## 关键参数

| 参数 | 说明 | 使用位置 | 注意事项 |
|--------|------|-----------|----------|
| `model` | 指定推理模型或服务标识 | 所有 API 请求体 | Prime 模式用 `glm-5.2-fast-preview`；吞吐预留用专属 `model-code`；智能路由固定为 `auto-model-xxxxxx`；Batch JSONL 中每行 `body.model` 必须一致 |
| `stream` | 控制是否流式响应 | `/chat/completions` 请求体 | Prime 模式下流式响应时需分别处理 `delta.reasoning_content` 与 `delta.content` 字段 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) |
| `enable_thinking` | 开启/关闭深度思考模式 | 请求体顶层（非 `extra_body`） | Batch 场景下该参数有效但结果文件不包含 `reasoning_content`；部分模型默认开启，建议显式设置 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| `input_tpm` / `output_tpm` | 吞吐预留容量额度（单位：kTPM） | 吞吐预留创建表单或 API `ptu_capacity` | 需结合 TPM 容量计算器估算；购买后立即计费，与实际调用量无关 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| `max_completion_tokens` | 限制最大输出 token 数 | 智能路由请求体 | 智能路由会将 `max_tokens` 自动转换为此参数，并仅路由至支持该参数的备选模型 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) |

## 使用方式

### 1. Prime 模式（开箱即用）
- 无需配置，直接调用标准 `/v1/chat/completions` 接口；
- 将 `model` 设为 `glm-5.2-fast-preview` 等 Prime 模型 ID；
- 接入域名：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。

### 2. 吞吐预留（PTU/DTU）
- 在[吞吐预留控制台](https://bailian.console.aliyun.com/cn-beijing/model/tpm-reservation)创建实例；
- 选择“高速模式”即为 PTU，获得 1.5~2 倍 TPS 提升；
- 创建成功后获取专属 `model-code`，替换 API 请求中的 `model` 参数；
- 支持按天/8 小时预付费，溢出策略可选「自动溢出」或「仅预留容量」。

### 3. 批量推理（异步离线）
- 构造 UTF-8 编码 JSONL 文件，每行一个请求对象，含 `custom_id`、`method`、`url`、`body`；
- `body` 中必须包含 `model` 且全文件一致，`enable_thinking` 须与 `model` 同级；
- 通过控制台或 API 提交任务，异步下载结果/错误文件。

### 4. 智能路由（零代码适配）
- 创建后获取 `auto-model-xxxxxx` code；
- 直接替换现有请求的 `model` 参数，其余不变；
- 响应头 `x-dashscope-resolved-model` 返回实际执行模型，便于监控与计费核验。

## 限制和注意事项

- **计费刚性**：吞吐预留（PTU/DTU）与 [Token](../concepts/token.md) 按量部署均为预付费/后付费模式，**创建成功即开始计费，与是否发起调用无关**；未调用仍全额产生费用 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
  
- **模型能力约束**：
  - Batch 推理不返回 `reasoning_content`，即使 `enable_thinking=true`，如需思考过程请改用实时 API；
  - 智能路由不支持 `top_p`、`temperature`、`logprobs`、`thinking_budget` 等采样与调试参数，设置将导致报错 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)；
  - 模型导入仅支持 LoRA，不支持全参微调模型，且要求 `rank` 为 8/16/32/64，`chat_template` 与词汇表必须与基础模型完全一致 [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)。

- **地域与协议限制**：
  - 智能路由仅支持 `maas.aliyuncs.com` 域名（`{workspace_id}.{region}.maas.aliyuncs.com`），不支持 `dashscope.aliyuncs.com`；
  - 批量推理不支持 DashScope 协议，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)；
  - 所有高速推理能力（Prime、PTU、DTU）当前仅支持华北2（北京）与新加坡地域。

- **缓存行为差异**：Prime 模式与吞吐预留支持前缀缓存并享受折扣（如 `glm-5.1` 缓存命中部分按 20% 折算容量），但智能路由因模型动态切换，**不保障缓存命中率**，仅依赖各备选模型自身的隐式缓存机制 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

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
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)


