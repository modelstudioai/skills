# get started with agents

Agent 是百炼平台提供的可编程智能体运行与编排能力，支持开发者快速构建具备知识、工具调用、记忆与安全治理能力的 AI 应用。本文档梳理核心能力边界、关键配置项及接入路径，适用于希望以最小成本启动 Agent 开发的工程师。所有功能均需通过百炼控制台或 API 调用，不依赖本地部署。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 `model_id` 参数动态指定底层 LLM（如 `qwen-max`、`qwen-plus` 等），模型能力由 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的“开发与运行”模块统一承载。当前支持三类核心运行形态：  
- **Managed Agent**：托管会话生命周期、工具执行与环境隔离，适合对话式应用；  
- **Flow Agent**：基于可视化节点编排多步逻辑与条件分支，适用于复杂工作流；  
- **Sandbox**：提供沙箱化代码执行、浏览器自动化与文件解析能力，需显式启用。  
上下文增强能力（RAG、Memory、Connector、ParseX）和工具扩展能力（MCP、Skill）均为可插拔模块，按需组合使用，详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 关键参数

调用 Agent 时必须指定以下参数（API 或控制台均适用）：  
- `agent_id`：Agent 的唯一标识符，创建后生成；  
- `model_id`：所用大模型 ID，必须为当前项目已开通的模型；  
- `input`：用户输入文本，类型为 `string`；  
- `enable_memory`：布尔值，启用[长期记忆](../concepts/long-term-memory.md)需设为 `true`，且对应 Memory 实例已配置；  
- `tools`：工具列表，格式为 `[{ "type": "mcp", "name": "xxx" }]` 或 `[{ "type": "skill", "id": "yyy" }]`。  
> **注意**：`tools` 参数中 `type` 字段在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中同时列出 `mcp` 和 `skill`，但实际 API 文档要求 `skill` 类型必须使用 `skill_id` 字段而非 `id`，该不一致已在 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中修正。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8)，选择模板并对话，无需编码；  
2. **API 接入业务系统**：调用 `/v1/agents/{agent_id}/chat` 接口，传入必要参数（参考 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；  
3. **集成上下文与工具**：在控制台 Agent 编辑页中，依次配置 Knowledge Base（RAG）、Memory 实例、Connector 或 MCP 工具，配置项实时生效，无需重启。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32768 字符，超长内容需预处理截断或分块；  
- Sandbox 沙箱默认禁用，需在 Agent 配置中显式开启 `enable_sandbox: true`，且仅支持 Python 3.9 运行时；  
- RAG 检索结果默认最多返回 5 个 chunk，不可通过参数调整，如需更多上下文需自行调用 Knowledge API 后拼接；  
- 所有工具调用（MCP/Skill）均受账户级 QPS 与并发数限制，具体配额见控制台「配额管理」，超出将返回 `429 Too Many Requests`。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


