# 智能路由与模型选型

智能路由与模型选型（Auto-Model Routing）是百炼平台提供的动态模型调度能力，通过统一入口（`auto-model-xxxxxx`）自动匹配当前请求上下文、SLA要求与成本约束下的最优可用模型，实现效果、延迟、成本与资源可用性的实时平衡。

## 在百炼平台的不同场景中，这个概念如何使用

- **高吞吐低延迟业务**：在 `model-high-speed-inference` 场景中，智能路由作为轻量级替代方案，无需预购容量或绑定特定模型，即可按“效果优先”或“成本优先”策略，从十余款备选模型（如 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813`）中动态选择最适配的模型执行推理，兼顾性能与弹性。
- **多模型灰度与AB测试**：结合 `model-management` 的权限控制与限流配置，开发者可为同一 `auto-model-xxxxxx` 路由实例设置白名单模型集、地域约束（`service_site`）及能力过滤（`capabilities`），实现按流量比例、用户标签或输入特征的精细化分流。
- **统一应用接入层**：在 `model-experience` 和 `application-support` 中，智能路由完全兼容标准 OpenAI Chat Completions 协议（`/v1/chat/completions`），开发者只需将 `model` 字段设为 `auto-model-xxxxxx`，即可复用现有 SDK 与调用逻辑，无需修改请求结构、参数或错误处理流程。
- **异构模型混合部署**：支持跨厂商、跨模态类型（文本为主，逐步扩展至向量/重排等轻量任务）的模型池协同调度；路由决策会自动规避未授权、未部署、不满足 `features`（如 `cache`、`function-calling`）或超出地域限制的模型。
- **运维可观测性增强**：每次调用返回中，`model` 字段明确标识实际执行的模型 ID，`usage` 字段记录真实 token 消耗（含缓存命中数），便于归因分析、成本分摊与模型效果回溯。

## 关键参数和配置

- **核心标识符**：`model = "auto-model-xxxxxx"`（`xxxxxx` 为控制台生成的唯一路由 ID，长度固定 6 位字母数字）
- **策略配置（创建时设定，不可运行时覆盖）**：
  - `routing_policy`: `"effectiveness_first"`（默认，优先保障输出质量与响应稳定性）或 `"cost_first"`（优先选择单位 token 成本最低且满足基础 SLA 的模型）
  - `candidate_models`: 显式指定参与路由的模型列表（如 `["qwen3.8-flash", "glm-5.2", "deepseek-v4-pro-0813"]`），若为空则使用平台默认备选集
  - `service_site`: 限定候选模型部署区域（如 `"asia-pacific-china"`），确保低延迟与合规性
  - `capabilities` / `features`: 声明必需能力（如 `["Reasoning", "function-calling"]`），路由引擎将自动过滤不支持的模型
- **运行时透明字段（响应体中返回）**：
  - `model`: 实际执行的模型 ID（如 `"qwen3.8-flash"`）
  - `usage.prompt_tokens_details.cached_tokens`: 输入中命中前缀缓存的 token 数
  - `x-dashscope-routing-id`: 唯一路由执行 trace ID，用于日志关联与问题排查

> ⚠️ 注意：智能路由当前仅支持 `maas.aliyuncs.com` 域名下的标准协议（OpenAI Chat Compat），不支持 Anthropic 或 Responses 协议；也不支持实时全模态（Realtime-Omni）及长视频/3D 等异步任务类模型。

## 关联主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model management](../api/model-management.md)
- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)
- [more about models](../api/more-about-models.md)


