# 模型路由与选型

模型路由与选型是百炼平台实现“效果、性能、成本”三者动态平衡的核心横切能力，指系统根据请求上下文、参数约束及运行时策略，自动从预设模型池中选择最适配的模型执行推理，或显式引导开发者选用特定优化路径（如 Prime、PTU、智能路由等）。

## 在百炼平台的不同场景中，这个概念如何使用

- **实时交互场景（如 AI 编程助手、Agent 多步推理）**：通过指定 `Prime` 专用 model ID（如 `glm-5.2-fast-preview`）实现零改造提速，本质是**静态路由**——开发者主动选型，平台保障该模型在轻量级加速通道中执行。  
- **高确定性业务（如 SaaS 核心服务、金融问答）**：通过「吞吐预留」创建专属 `model code`（如 `ptu-qwen3.8-max-xxxx`），将流量**固定路由**至独占资源池，规避公共队列抖动，同时支持溢出降级策略。  
- **异构模型混合调用（如多供应商 RAG、A/B 测试）**：利用模型管理 API 查询带标签（`capabilities: Realtime-Omni`, `features: thinking`）的可用模型，再按业务逻辑**程序化选型**，例如优先选支持 `enable_thinking` 的模型处理复杂推理请求。  
- **泛化请求场景（如开放平台 API、低代码 Agent）**：启用 `auto-model-xxxx` 类型智能路由，平台基于 `response_format`、`max_tokens`、输入长度、任务类型（text/vision/audio）等参数**实时过滤+打分匹配**，自动路由至满足约束且性价比最优的模型（如 `qwen3.8-flash` 或 `glm-5.2`），响应头 `x-dashscope-resolved-model` 明确告知实际执行模型，便于监控与归因。  
- **Agent 开发场景**：`model_id` 字段即路由锚点——Managed/Flow Agent 中直接绑定模型 ID 实现声明式选型；Sandbox Agent 中则需在 `run()` 函数内调用 `llm.invoke(model_id=...)` 主动触发路由，支持运行时条件判断（如“长文本走 batch，短文本走 real-time”）。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 注意事项 |
|------|----------|------|----------|
| `model` | 全场景必填 | 模型标识符，决定路由入口：<br>• `qwen3.8-max`：标准模型<br>• `glm-5.2-fast-preview`：Prime 模式<br>• `ptu-xxx` / `dtu-xxx`：吞吐预留专属模型<br>• `auto-model-xxxx`：智能路由入口 | 必须与接入域名匹配（如 Prime 需用 `compatible-mode/v1` 域名）；混用会导致 404 或降级 |
| `response_format` | 智能路由、部分原生模型 | 触发模型能力过滤，仅路由至原生支持该格式的模型（如 `{"type": "json_object"}` 会排除不支持 JSON Schema 的模型） | 不支持的模型将被自动剔除，不报错但可能无候选模型导致失败 |
| `max_tokens`（自动转为 `max_completion_tokens`） | 智能路由、所有文本生成 | 参与路由决策：系统优先匹配上下文窗口充足、且推理成本更优的模型（如 2K 请求不会路由至 256K 上下文的高价模型） | 建议设置合理上限，避免因过度宽松导致选型偏差 |
| `enable_thinking` / `thinking` | 三方模型（DeepSeek/Kimi/GLM 等） | 影响模型能力筛选：智能路由会识别该参数并仅匹配支持深度思考的模型；若未提供，则默认跳过思考模式 | 非 OpenAI 标准参数，必须透传至顶层（非 `extra_body` 内）才参与路由 |
| `custom_id` | 批量推理 | 用于异步任务标识，不参与路由，但影响结果归因 | 批量任务中每个请求必须唯一，否则覆盖写入 |

> ✅ **最佳实践**：对稳定性要求高的服务，优先用吞吐预留 + 固定 model ID；对成本敏感且请求差异大的开放接口，用 `auto-model-xxxx` + 合理 `max_tokens`/`response_format` 约束；调试阶段务必检查响应头 `x-dashscope-resolved-model`，确认实际执行模型是否符合预期。

## 面向开发者，简洁实用

- **不要硬编码模型名**：用模型管理 API 动态查询 `status=active` 且带所需 `features` 的模型列表，再选型，避免因模型下线导致故障。  
- **智能路由不是万能**：若请求含强领域约束（如必须用 `qwen-audio-*` 处理语音），请直接指定 model ID，而非依赖路由——路由只保证“可用”，不保证“唯一”。  
- **监控先行**：在日志/可观测性系统中提取 `x-dashscope-resolved-model` 和 `usage.model`，对比分析路由分布与业务目标是否一致（例如：90% 请求应走 `flash` 模型，却大量命中 `max`，需检查 `max_tokens` 是否设得过大）。  
- **快速验证路由行为**：用 `curl` 发送最小化请求（仅 `model` + `messages`），观察响应头和 `usage.model`，无需等待完整业务逻辑。  
- **Agent 中慎用动态选型**：Sandbox Agent 内多次 `llm.invoke()` 调用不同 model ID 会显著增加延迟，建议在 `run()` 开头统一决策一次，复用结果。

## 关联主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model management](../api/model-management.md)
- [use cases](../guides/use-cases.md)
- [agent development](../guides/agent-development.md)


