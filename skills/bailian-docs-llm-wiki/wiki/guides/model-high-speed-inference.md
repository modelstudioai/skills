# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**Prime 模式**（轻量级性能增强）和**吞吐预留**（专属容量保障）。二者均通过模型标识符（`model` 参数）启用，无需修改 API 协议或请求结构，适用于对输出速度（TPS）、稳定性或确定性 SLA 有明确要求的生产环境。

## 支持的模型与功能

- **Prime 模式**：面向通用高速响应场景，提供 1.5~2 倍于标准 API 的 TPS，适用于 AI 编程助手、Agent 多步推理、实时对话等。其本质是平台侧优化的共享资源调度策略，不独占算力。支持模型包括 `glm-5.2-fast-preview`、`qwen3.8-max-prime`、`wan3.0-video-prime` 等，具体列表见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- **吞吐预留**：为指定模型锁定专属推理容量（以 kTPM 为单位），确保业务高峰期不受公共资源限流影响。支持模型范围更广，覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列的多个版本（如 `Qwen3.8-Max`、`GLM-5.2`、`DeepSeek-v4-Pro`），详见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：`glm-5.2-fast-preview` 在 Prime 模式文档中被列为独立模型 ID，而在吞吐预留文档中仅支持 `GLM-5.2`（无 `-fast-preview` 后缀）。实际调用时，若需同时获得 Prime 性能与专属容量保障，应优先使用吞吐预留创建 `GLM-5.2` 的专属模型 code；`glm-5.2-fast-preview` 仅适用于纯 Prime 模式（共享资源池），二者不可混用。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **启用方式** | 直接在 `model` 字段填入专用模型 ID（如 `"glm-5.2-fast-preview"`） | 创建后获取专属 `model` code（如 `"tpm-xxx"`），替换请求中的 `model` 字段 |
| **性能档位** | 固定高速模式（1.5~2× TPS） | 可选「标准模式」或「高速模式」（后者等效于 PTU 部署，同样提供 1.5~2× TPS） |
| **容量保障** | 无专属容量，依赖平台剩余资源；限流值为软上限，实际可用 TPS 不低于该值 | 严格保障预留的输入/输出 kTPM，容量内调用完全隔离、零干扰 |
| **溢出策略** | 不适用（无预留概念） | 可配置：「自动溢出至按量计费」（默认，服务不中断）或「仅使用预留容量」（超限返回 429） |
| **计费单位** | 按实际输入/输出 token 计费，与标准 API 一致 | 预付费购买 kTPM 容量（按天），预留容量内调用不额外计费；溢出部分按 token 计费 |

## 使用方式

- **Prime 模式**：  
  仅需将 `model` 设为对应模型 ID，并使用兼容模式域名（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。示例见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

- **吞吐预留**：  
  1. 在控制台创建预留实例，选择模型、性能模式、输入/输出 kTPM 及溢出策略；  
  2. 在详情页复制生成的专属 `model` code；  
  3. 将 API 请求中的 `model` 替换为该 code（其他参数不变）；  
  4. 注意：首次调用存在短暂预热期，建议客户端实现排队或重试机制。完整接入流程见 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 限制和注意事项

- **模型能力一致性**：Prime 模式下，模型的功能、上下文长度、输出格式等与原版模型完全一致，仅推理性能提升；吞吐预留亦不改变基础模型能力。
- **缓存行为**：两者均支持缓存命中折扣（如 `cached_tokens` 计入 `prompt_tokens_details`），但 Prime 模式文档中明确列出缓存单价（如 `glm-5.2-fast-preview` 为 4 元/百万 token），而吞吐预留文档未提供缓存单价细节，实际计费请以控制台为准。
- **地域与模型绑定**：Prime 模式与吞吐预留的模型支持列表、价格均按地域（如华北2、新加坡）分别定义，跨地域不可复用模型 ID 或 code。
- **调试与监控**：吞吐预留提供完整的监控页签（利用率、配额内外调用次数、缓存命中量），推荐用于生产环境容量治理；Prime 模式暂无专属监控视图，需复用标准 API 监控能力。
- **退订与失效**：吞吐预留退订后专属 `model` code 立即失效，请求自动回退至公共资源；而 Prime 模式无生命周期管理，只要模型 ID 有效即可持续调用。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


