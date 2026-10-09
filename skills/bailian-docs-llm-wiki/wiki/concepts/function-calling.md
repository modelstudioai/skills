# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主规划并执行外部工具（如 API、插件、搜索服务等）的核心能力。它通过结构化工具定义与语义化参数解析，使模型能安全、可控地扩展其能力边界，完成实时信息检索、精确计算、代码执行、图像生成等模型原生不支持的任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个 API 层级的统一机制，具体体现为以下三类典型场景：

- **Omni Realtime API（实时多模态交互）**：在语音+文本流式对话中，模型可基于语音输入或文本上下文，动态触发 `type=function` 类型的工具调用。适用于需要低延迟响应的智能客服、会议助手等场景。此时工具定义需在 `tools` 参数中声明，且与 `enable_search` 互斥。

- **Application Call（应用调用）与 Plug-in（插件）体系**：在智能体（Agent）或工作流（Workflow）中，函数调用表现为插件的自动调度。官方插件（如计算器、夸克搜索）、三方插件及自定义插件均通过 `tools` 数组注册；模型根据 `tool_description` 和用户 query 自主选择工具并填充参数。`biz_params` 可用于透传业务侧参数（如用户 ID、会话上下文），但仅 `Authorization` Header 可被插件服务端接收。

- **Managed Agents API（托管智能体）**：作为声明式 Agent 的核心执行单元，函数调用由 `Skill` 资源封装，配合 `Vault` 管理凭证、`Environment` 控制执行沙箱。工具调用事件（`tool_executed`）可通过 Webhook 实时捕获，便于构建可观测、可审计的生产级智能体。

> ✅ 共同前提：所有场景均要求工具定义符合 OpenAI 兼容格式（含 `name`、`description`、`parameters`），且 `parameters` 中每个字段必须明确 `type` 与 `description`（含格式示例），否则模型无法准确提取参数。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `tools` | 请求体顶层 | `array` | 工具定义列表，每个元素为 `{ "type": "function", "function": { ... } }` | 必须提供；`qwen3.5-*` 系列仅支持 `function` 类型；`qwen3.8-*` 支持 `function` + `mcp` 混合 |
| `tool_choice` | 请求体顶层 | `string` 或 `object` | 控制调用策略：`"auto"`（默认，模型自主决策）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 不填即为 `auto`；强制指定时 `name` 必须与 `tools` 中某项完全匹配 |
| `biz_params` | 请求体顶层（Application Call / Managed Agents）或 `tools[].function.parameters`（自定义插件） | `object` | 业务透传参数容器，用于注入用户上下文、鉴权 [Token](token.md)、环境变量等 | 自定义插件中，`passing_method="业务透传"` 的参数必须从此处传入；不可写入用户 prompt |
| `enable_search` | Omni Realtime API 专用 | `boolean` | 启用内置联网搜索（非插件） | 与 `tools` 互斥，不可同时启用 |

> ⚠️ 重要限制：  
> - 单次对话最多触发 **10 次工具调用**（含重复调用同一工具）；  
> - 自定义插件的 `Object` 类型参数，子属性**不可为空**，否则发布失败（错误码 130022）；  
> - 所有工具调用返回结果将作为上下文输入模型，开发者需关注响应结构是否扁平、字段名是否清晰，避免解析失败。

## 面向开发者，简洁实用

- ✅ **快速验证**：在控制台「智能体调试」页开启「显示思考过程」，观察模型是否生成 `tool_calls` 字段及参数提取是否准确；  
- ✅ **调试技巧**：若调用失败，优先检查 `tool_description` 是否包含具体使用示例（如 `"获取北京今日天气：get_weather(city='北京')"`），这是模型理解意图的关键；  
- ✅ **安全实践**：敏感凭证（如 API Key）**必须**通过 `Vault`（Managed Agents）或插件鉴权配置注入，严禁硬编码或通过 `prompt`/`biz_params` 明文传递；  
- ✅ **性能提示**：函数调用会增加端到端延迟，对实时性要求极高的语音场景（如实时会议转录），建议预判高频需求并设计缓存策略或降级逻辑。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)


