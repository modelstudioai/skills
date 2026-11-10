# 模型路由

模型路由是百炼平台提供的一种**智能、动态的请求分发机制**：在不改变客户端调用方式的前提下，平台根据请求内容特征（如输入长度、语义复杂度、参数约束等），自动从预配置的备选模型池中选择最适配的模型执行推理，实现效果、成本与延迟的实时最优平衡。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能路由（核心应用）**：这是模型路由最典型的落地形态。开发者只需在 [OpenAI 兼容接口](openai-compatible-interface.md)（`/v1/chat/completions`）中指定固定模型 ID（如 `auto-model-xxxxxx`），平台即对每个请求进行实时分析，从已纳管的多个文本生成模型（如 `qwen3.8-flash`、`glm-5.2`、`qwen3.7-plus` 等）中动态匹配最优者。适用于效果敏感但预算受限、流量波动大、或需快速验证多模型表现的场景。  
  ✅ 支持：标准 Chat Completions 请求、`response_format` 结构化输出、`max_tokens`（自动转为 `max_completion_tokens`）等过滤条件。  
  ❌ 不支持：流式响应（`stream=true`）、批量推理（Batch）、非生成类接口（如 Embedding、Decision）、多模态输入。

- **跨模型能力调度（隐式路由）**：在专用模型服务中，路由逻辑内嵌于协议层。例如：  
  - `qwen-mt-uni` 对不同输入格式（PDF/DOCX/图片/音频）自动触发对应模态处理链路，并在翻译引擎内部完成子模型选型；  
  - `tongyi-intent-detect-v3` 根据 `mode` 参数（`INTENT_MODE` 或分类模式）路由至不同推理后端；  
  - `gui-plus` 在理解截图后，结合系统消息中声明的工具签名，自动路由至 `computer_use` 等专用执行模块。  
  此类路由对开发者透明，由模型自身能力定义驱动，无需显式配置路由策略。

- **部署级路由（基础设施层）**：当用户为同一模型申请多种部署形态（如 DTU 独占实例 + 吞吐预留 + 标准共享 API）时，平台在负载均衡层按容量水位、SLA 要求和请求优先级，将流量分发至最优资源池。这属于运维侧自动路由，不暴露给 API 调用方。

## 关键参数和配置

- **必需参数**：  
  - `model`: 必须设为平台分配的智能路由专用模型 ID（格式为 `auto-model-xxxxxx`），不可使用具体模型名（如 `qwen3.8-max`）。该 ID 在控制台「模型路由」页面创建并获取。

- **影响路由决策的请求参数（作为过滤条件）**：  
  - `max_tokens`（或 `max_completion_tokens`）：仅路由至上下文窗口与输出长度能力满足要求的模型；  
  - `response_format`：仅路由至原生支持该结构化输出格式（如 `{"type": "json_object"}`）的模型；  
  - `input` 内容特征：平台自动分析 token 数量、文本领域、是否含代码/数学公式等，匹配模型专长（如 `qwen3.8-flash` 适合短文本快响应，`glm-5.2` 更擅逻辑推理）。

- **配置入口**：  
  - 在百炼控制台 → 「模型服务」→ 「模型路由」页面，可：  
    • 创建/删除路由策略；  
    • 添加或移除备选模型（需已获得该模型的推理权限）；  
    • 设置各备选模型的权重与启用状态（用于灰度或降级）；  
    • 查看路由日志与命中统计（需开通可观测性功能）。

## 面向开发者，简洁实用

- ✅ **快速接入**：替换 `model` 参数即可启用，无需修改 SDK、重写业务逻辑或管理多个 endpoint。  
- ✅ **免运维优化**：路由策略由平台持续迭代，新模型上线后可一键加入备选池，自动获得能力升级。  
- ⚠️ **注意限制**：  
  • 仅限 OpenAI 兼容的 `/v1/chat/completions` 接口；  
  • 不支持 `stream`、`tools`（[函数调用](function-calling.md)）、`parallel_tool_calls` 等高级特性；  
  • 若请求参数超出所有备选模型能力（如 `max_tokens=32768` 但无模型支持），将返回 `400 Bad Request` 并提示 `no_model_matched`。  
- 🔍 **调试建议**：开启请求头 `X-DashScope-Debug: true`，响应中将返回 `x-dashscope-routing-info` header，包含实际命中的模型 ID 与决策依据，便于问题定位。

## 关联主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model management](../api/model-management.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)
- [more models](../api/more-models.md)


