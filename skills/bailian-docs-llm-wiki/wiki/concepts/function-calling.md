# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图并结构化生成工具执行指令的能力，表现为模型输出符合预定义 Schema 的 JSON 格式函数调用请求（如 `{"name": "web_search", "arguments": "{\"query\": \"北京天气\"}"}`），而非自由文本。该能力是构建可靠智能体（Agent）的核心基础，使大模型能安全、可控地与外部系统（搜索、数据库、API 等）交互。

## 在百炼平台的不同场景中，这个概念如何使用

- **意图理解模型（`tongyi-intent-detect-v3`）**：专为毫秒级意图识别设计，通过在 system message 中声明 `Response in INTENT_MODE.` 指令，触发结构化函数调用输出。适用于对话路由、服务跳转等轻量决策场景，无需实际执行工具，仅需解析 `<function>` 标签提取调用意图。
  
- **Agent API（Managed / Flow Agents）**：作为 Agent 运行时的核心机制，模型（仅限 `qwen-max`/`qwen-plus`/`qwen-turbo`）基于用户输入和提供的 `tools` 列表，自主选择并填充函数参数。Agent 运行时自动执行调用、注入结果、继续推理，支持多轮工具链（如“查天气 → 换算温度 → 发送通知”）。

- **深度研究模型（`qwen-deep-research`）**：不支持函数调用。该模型采用自研规划协议（非 OpenAI 兼容格式），通过反问澄清、分阶段报告生成实现复杂任务，开发者需手动解析其自然语言输出并调用对应服务。

- **OCR/GUI 模型（如 `qwen3.5-ocr`、`gui-plus`）**：不支持函数调用。其输入为图像+文本指令，输出为结构化字段（OCR）或操作指令（GUI），属于单步感知-生成任务，无工具调度需求。

> ✅ **关键结论**：函数调用能力与模型强绑定——仅 `tongyi-intent-detect-v3`（意图识别）、`qwen-max`/`qwen-plus`/`qwen-turbo`（Agent 场景）原生支持；其他专用模型（OCR、GUI、Deep Research）均不提供该能力。

## 关键参数和配置

- `tools`（必需，Agent 场景）：工具列表，每个工具必须包含 `name`（字符串）、`description`（功能说明）和 `parameters`（JSON Schema v7 定义的参数结构）。Schema 用于约束模型输出，确保 `arguments` 字段可被 `json.loads()` 安全解析。

- `tool_choice`（可选）：控制调用策略：
  - `"auto"`（默认）：模型自主决定是否调用及调用哪个工具；
  - `"none"`：禁止任何函数调用，强制模型返回自然语言；
  - `"required"` 或具体 `tool.name`：强制调用指定工具（常用于确定性流程）。

- `system` 消息（意图模型必需）：必须包含 `Response in INTENT_MODE.` 字样以启用函数调用模式；若含 `choose one tag from the tag list` 则退化为纯标签分类，**禁用函数调用**。

- `enable_thinking`（可选，Managed Agents）：设为 `true` 时，响应中返回 `reasoning_content` 字段，展示模型选择该函数的中间推理过程，便于调试。

- **无额外参数**：函数调用本身不引入新参数（如 `function_timeout`），超时、重试、错误处理均由 Agent 运行时或 SDK 统一管理。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen-plus` + 1 个简单工具（如 `{"name":"calculator","parameters":{"type":"object","properties":{"expression":{"type":"string"}}}}`）发起一次请求，检查响应中是否存在 `tool_calls` 字段。
- ✅ **解析安全**：始终使用 `json.loads(tool_call['arguments'])` 解析参数，**切勿用 `eval()` 或正则提取**；百炼保证 `arguments` 是合法 JSON 字符串。
- ✅ **错误处理**：当模型返回无效 JSON 或参数不满足 Schema 时，Agent 会自动重试（最多 3 次）；开发者需监听 `event: error` 流式事件或检查 HTTP 400 响应体中的 `validation_error` 字段。
- ⚠️ **避坑提示**：`qwen-deep-research` 和所有 OCR/GUI 模型**不支持** `tools` 参数，传入将被忽略；`temperature=0` 可提升函数调用稳定性，但非必需。

## 关联主题页

- [more models](../api/more-models.md)
- [agent api start using](../api/agent-api-start-using.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [managed agents api](../api/managed-agents-api.md)


