# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、结构化提取参数，并按需触发外部工具或服务执行任务的核心能力。它不是简单的 API 转发，而是由大模型在推理过程中自主决策“何时调用、调用哪个、传入何参”，再将执行结果注入上下文继续思考，形成闭环的智能代理行为。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口，而是贯穿多个能力层的统一语义机制，具体体现为以下三类实践方式：

- **Managed Agents（托管智能体）**：作为默认执行范式。当智能体被赋予内置工具（如 `bash`、`web_search`、`read`）或挂载 MCP 服务/Skill 后，模型在会话中自动规划并发起函数调用；所有调用均在隔离沙箱中执行，结果以结构化事件（`tool_result`）形式返回并参与后续推理。开发者无需编写循环逻辑，只需声明可用工具及权限策略（`permission_policy`）。

- **Qwen API（模型直调）**：通过 `tools` 字段显式注册函数定义（支持 OpenAI 兼容格式或 DashScope 原生 `function` schema），模型根据 `function.description` 自主判断是否调用。适用于需要细粒度控制调用时机的场景，如构建自定义 Assistant 或集成到已有 Agent 框架中。注意：`qwen3.8+` 系列模型对多工具协同规划能力显著增强。

- **插件（Plug-in）与工作流**：官方/三方/自定义插件本质是已封装的函数服务。在智能体或工作流中启用插件后，其工具 ID（`tool_id`）即成为可被模型调用的函数标识；工作流节点亦可配置为“函数调用节点”，接收上游输出并透传参数（`biz_params`）至插件后端。

> ⚠️ 注意：OpenAI 兼容工具包（如 LangChain 集成、`openai==1.40.0+`）当前**不支持 `functions` / `tools` 参数**，无法触发函数调用——该能力仅在原生 DashScope 协议、Qwen API 及 Managed Agents 中完整可用。

## 关键参数和配置

| 参数 | 位置 | 说明 | 示例值 |
|------|------|------|--------|
| `tools` | 请求体（Agent 定义 / Qwen API / Application Call） | 工具列表，每个工具需含 `type`（`function`）、`function.name`、`function.description` 和 `function.parameters`（JSON Schema） | `[{"type": "function", "function": {"name": "web_search", "description": "实时网络搜索", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}}}]` |
| `tool_choice` | Qwen API 请求体（可选） | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | `"auto"` |
| `permission_policy` | Managed Agents 工具配置 | 内置工具的调用审批策略，取值 `"auto"`（自动放行）或 `"approval_required"`（需人工审核） | `"auto"` |
| `tool_id` | 插件调用 / `biz_params` | 插件工具唯一标识，用于在 `tools` 列表或业务透传中精准定位目标函数 | `"quark_search"` |
| `biz_params` | Application Call / DashScope SDK | 业务系统向函数传递的透传参数，常用于携带用户 [Token](token.md)、上下文变量或插件专用字段 | `{"user_id": "u123", "auth_token": "xxx"}` |

## 面向开发者，简洁实用

- ✅ **优先使用 Managed Agents**：若任务涉及多步工具链、文件操作或长时执行，直接定义 Agent 并挂载工具/MCP/Skill，平台自动处理调用编排、沙箱生命周期与错误重试。
- ✅ **Qwen API 直调适用轻量集成**：需快速验证函数逻辑或嵌入自研框架时，用 DashScope 协议调用 `qwen3.8-max` 等模型，`tools` 字段定义即生效。
- ✅ **插件 = 即插即用的函数服务**：自定义插件发布后，其工具 ID 可直接填入 `tools` 列表；调试阶段务必确认状态为“已发布”且“调试成功”。
- ❌ **避免在 [OpenAI 兼容接口](openai-compatible-api.md)中尝试函数调用**：`toolkits-and-frameworks` 明确不支持 `functions`，强行传参将被忽略。
- 🔍 **调试技巧**：开启 `enable_thinking=true` 查看模型调用决策依据；检查 `tool_result` 事件中的 `error` 字段定位执行失败原因（如鉴权失败、参数类型错误）。

## 关联主题页

- [managed agents](../guides/managed-agents.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


