# 函数调用

函数调用（Function Calling）是百炼平台中让大模型具备**主动识别用户意图、自主选择并执行外部工具（如 API、知识库、数据库查询、业务系统接口等）** 的核心能力。它通过结构化 Schema 描述可用工具，由模型在推理过程中动态生成符合规范的函数调用请求，再由平台自动路由、执行并注入结果回对话上下文，从而实现“思考→决策→行动→反馈”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼三大应用范式中均作为关键能力深度集成，但接入方式与控制粒度不同：

- **应用组件 API（`/api/v1/services/aigc/text-generation/generation`）**  
  通过 `input.messages` 中的 `tool` 数组声明可用函数（含 `name`、`description`、`parameters` JSON Schema），并在 `parameters.tool_choice` 中指定调用策略（`"auto"` / `"none"` / `{"type": "function", "function": {"name": "xxx"}}`）。模型返回 `tool_calls` 字段后，需由调用方自行解析、执行工具，并将结果以 `tool_response` 角色消息重新提交给 API 继续推理。适用于需要完全掌控工具执行逻辑、自建工具链或与现有系统深度集成的开发者。

- **托管智能体（Managed Agents）**  
  工具以 `Skill` 形式在 Agent 创建时预注册（支持 MCP 协议、HTTP API、函数计算等多种接入方式），无需在每次请求中重复定义 Schema。调用由平台全自动完成：模型输出 `tool_calls` → 平台匹配 Skill → 安全执行（自动注入 Vault 凭据、隔离 Environment）→ 将结果注入 Memory Store 并续写对话。开发者只需关注 Skill 开发与 Agent 编排，无需处理调用编排与状态同步。

- **LLM 应用（工作流/智能体）**  
  在可视化界面中，函数调用体现为 **MCP 节点、API 节点、数据连接器节点、自定义函数节点** 等。用户通过拖拽配置参数、设置失败重试、定义输入映射与输出解析规则。Agent 2.0 更进一步，将知识库检索、RAG、外部服务统一抽象为“工具”，由模型自主规划调用顺序与组合逻辑，并完整记录调用链路供调试与审计。适合低代码快速构建业务闭环。

> ✅ 共同前提：所有场景均要求工具定义严格遵循 OpenAI-style Function Calling Schema（JSON Schema 格式），且模型需支持该能力（当前 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分私有微调模型已支持）。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 |
|------|----------|------|------|
| `tools` | 应用组件 API、LLM 应用（智能体/工作流节点配置） | array | 工具列表，每项含 `name`（必填，唯一标识）、`description`（必填，影响模型理解）、`parameters`（必填，JSON Schema 定义参数类型、约束、默认值） |
| `tool_choice` | 应用组件 API、托管智能体 | string \| object | 控制调用行为：<br>• `"auto"`（默认）：模型自主决定是否及调用哪个工具<br>• `"none"`：禁用函数调用<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具 |
| `enable_thinking` | LLM 应用（智能体/大模型节点） | boolean | 启用思考链（Chain-of-Thought），提升复杂工具调用的规划准确性；建议在多步骤、多工具协同场景开启 |
| `thinking_budget` | LLM 应用 | integer | 思考过程 token 上限，默认 4000；避免过度思考导致延迟或超限 |
| `tool_response` | 应用组件 API（二次请求） | object | 工具执行结果必须以该角色提交，格式为 `{ "role": "tool", "content": "...", "tool_call_id": "..." }`；`tool_call_id` 需与模型返回的 `id` 严格匹配 |

> ⚠️ 注意事项：  
> - 工具名（`name`）仅支持字母、数字、下划线，长度 ≤64 字符；  
> - `parameters` Schema 中避免使用 `anyOf`/`oneOf` 等复杂联合类型，推荐使用明确字段定义；  
> - 托管智能体中，Skill 的 `name` 必须与注册时一致，大小写敏感；  
> - 所有工具返回内容应为纯文本或 JSON 字符串，避免 HTML/二进制等非结构化数据（如需文件，返回 URL 或 ID，再通过其他节点处理）。

## 面向开发者，简洁实用

- **调试技巧**：开启 `stream=true` + `enable_thinking=true`，观察模型在 `thinking` 步骤中如何分析工具、生成参数、规划调用顺序；  
- **错误定位**：若模型未触发调用，优先检查 `description` 是否清晰描述用途与约束，以及 `parameters` Schema 是否存在歧义（如 `type: "string"` 未加 `enum` 或 `pattern`）；  
- **性能优化**：对高频调用工具，可在 Skill 或工作流中启用缓存（如 `cache_key` 配置）；对耗时工具，设置合理 `timeout` 并配置重试；  
- **安全实践**：生产环境务必通过 `Vault` 管理凭证，禁止在 `description` 或 `parameters` 中硬编码敏感信息；工具执行日志默认留存 7 天，可用于审计。

## 关联主题页

- [application component api reference](../api/application-component-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [llm application](../guides/llm-application.md)


