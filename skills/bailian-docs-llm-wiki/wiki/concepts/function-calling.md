# 函数调用与工具集成

函数调用（Function Calling）是大模型与外部系统交互的核心机制，允许模型在推理过程中识别用户意图并自动调用预定义的函数或工具，从而突破纯文本生成的局限，实现实时信息获取、精确计算、数据查询等能力。在百炼平台中，函数调用与工具集成贯穿模型推理、应用构建和协议对接的全链路。

## 基本原理

函数调用的工作流程分为三步：

1. **声明工具**：开发者在请求中通过 `tools` 参数描述可用函数的名称、功能和参数结构
2. **模型决策**：模型根据用户输入和工具描述，判断是否需要调用函数，并生成结构化的调用参数
3. **执行与回传**：开发者在本地执行函数，将结果以 `tool` 角色消息回传模型，模型据此生成最终回复

模型本身不执行函数，而是输出调用意图和参数，实际执行由开发者控制。

## 在百炼平台的使用场景

### 模型推理层：Function Calling 参数

百炼的文本生成模型（Qwen3.7 系列、DeepSeek 等）原生支持 Function Calling。通过 OpenAI 兼容的 Chat Completions 接口或 DashScope 原生接口，在请求中传入 `tools` 数组即可启用。支持的模型包括 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash` 等。

关键参数：

- `tools`：工具定义数组，每个工具包含 `type`（固定为 `function`）和 `function`（含 `name`、`description`、`parameters`）
- `tool_choice`：控制模型调用策略——`auto`（模型自主决定）、`none`（禁止调用）、或指定具体函数名

### 应用层：插件与 MCP 工具

在百炼的应用体系中，函数调用以两种形态呈现：

- **插件（Plugin）**：百炼预置的官方插件（如代码解释器 `code_interpreter`、夸克搜索 `quark_search`）和自定义插件。在智能体应用中，模型根据用户输入自动判断是否调用；通过 Assistant API 则用 `tools` 参数显式指定工具 ID。单次任务最多组合调用 10 个工具。
- **MCP 服务**：通过模型上下文协议（MCP）标准化接入外部工具。智能体应用最多同时添加 5 个 MCP 服务，模型根据对话自动判断调用时机。MCP 服务也可通过 SDK 在外部项目中直接调用。

### 内置工具

百炼还提供不需要开发者自行实现的内置工具，通过 Responses API 直接使用：

- **联网搜索**：实时搜索互联网信息
- **代码解释器**：执行 Python 代码
- **网页内容提取**：抓取指定 URL 的页面内容

## 关键配置与开发要点

### 自定义插件配置

创建自定义插件时需配置：

| 配置项 | 说明 |
|--------|------|
| 插件 URL | API 的访问域名，同一插件下的工具共享 |
| 工具路径 | 相对于插件 URL 的 API 路径 |
| 鉴权方式 | 支持服务级/用户级鉴权，Token 位于 Header 或 Query |
| 输入参数 | "大模型识别"（从对话提取）或"业务透传"（外部传入） |
| 输出参数 | 定义返回数据结构，模型据此组织回复 |

### 接口选择

| 接口 | Function Calling 支持 | 适用场景 |
|------|----------------------|---------|
| OpenAI Chat Completions | 原生支持 `tools` 参数 | 迁移现有 OpenAI 应用 |
| OpenAI Responses API | 内置工具 + 自定义工具 | 需要联网搜索等内置能力 |
| DashScope 原生接口 | 最完整的参数支持 | 需要全部百炼功能 |
| Anthropic Messages 兼容 | 支持工具调用 | 使用 Anthropic 生态 |

### 注意事项

- **工具描述质量直接影响调用效果**：需在描述中明确工具名称和能力边界，效果不佳时可换用更强的推理模型（如千问 3 系列）
- **Token 消耗**：工具定义和调用结果都会占用上下文 Token，工具越多、返回内容越丰富，消耗越大
- **结构化输出配合**：需要模型返回严格 JSON 格式时，可结合结构化输出功能使用
- **超时限制**：自定义插件的调用超时限制为 5 秒
- **思考模式兼容**：开启 `enable_thinking` 后仍可使用 Function Calling，适合需要复杂推理后再调用工具的场景

## 关联主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [model inference](../guides/model-inference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [qwen api reference](../api/qwen-api-reference.md)


