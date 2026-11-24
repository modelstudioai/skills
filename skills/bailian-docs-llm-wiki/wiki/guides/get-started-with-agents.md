# get started with agents

Agent 是百炼平台提供的可编程智能体运行与编排服务，支持开发者快速构建具备知识、工具调用和上下文感知能力的 AI 应用。本文档面向开发者，梳理 Agent 的核心能力边界、关键配置项及接入路径，帮助你基于实际需求选择合适模式并规避常见陷阱。所有功能均需通过百炼控制台或 API 调用，不支持纯前端直连。

## 支持的模型与功能

Agent 本身不绑定特定大模型，而是通过 `model_id` 参数动态指定后端 LLM（如 `qwen-max`、`qwen-plus`），模型能力由 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中定义的执行环境决定。当前支持三类核心运行模式：  
- **Managed Agent**：托管会话生命周期、工具调用与状态管理，适合对话式应用；  
- **Flow Agent**：基于可视化节点编排多步骤工作流，支持条件分支与并行执行；  
- **Sandbox**：提供隔离沙箱环境，安全执行代码、浏览器操作或文件解析（如 PDF 表格提取）。  

上下文增强能力包括 RAG（知识库检索）、Memory（[长期记忆](../concepts/long-term-memory.md)存储）、Connector（企业系统对接）和 ParseX（文档结构化解析），详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 关键参数

调用 Agent 时必须显式指定以下参数：  
- `agent_id`：在控制台创建 Agent 后生成的唯一标识符；  
- `model_id`：所用大模型 ID，需与 Agent 配置的兼容模型列表一致（如 Flow Agent 不支持 `qwen-turbo`）；  
- `input`：用户输入文本，部分场景下需配合 `files`（上传文件）或 `context`（显式传入上下文片段）使用；  
- `stream`：布尔值，控制是否启用流式响应（仅 Managed Agent 和 Flow Agent 支持）；  
- `tools`：若启用 MCP 工具调用，需在此字段声明工具 ID 列表，且工具须已在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中注册并授权。

> **注意**：`memory_id` 参数在 Memory 功能中用于指定记忆库实例，但其值不能直接传入 Agent 调用请求 —— 必须通过控制台为 Agent 绑定 Memory 实例后，由平台自动注入上下文。该行为与旧版文档中“手动传 memory_id”的描述矛盾，以当前控制台逻辑为准。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，无需编码即可创建模板 Agent 并测试交互；  
2. **API 接入业务系统**：参考 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)，使用 `POST /v1/agents/{agent_id}/chat` 发起调用；  
3. **集成开发流程**：建议按“创建 Agent → 配置上下文（RAG/Memory）→ 绑定工具（MCP/Skill）→ 测试 → 部署”顺序推进，各环节操作指引见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 限制和注意事项

- 单次请求最大输入长度为 32,768 token（含 system prompt、history、input 及 context），超长内容需预处理截断或分块；  
- Sandbox 模式下，Python 执行超时默认为 30 秒，不可修改；浏览器操作（Puppeteer）仅支持 Chromium 内核，不兼容 IE 或旧版 Edge；  
- MCP 工具调用失败时，Agent 默认返回错误信息而非重试，需在业务层捕获 `tool_call_failed` 状态并处理；  
- 所有 Agent 实例默认开启内容安全检测（含敏感词过滤与图片鉴黄），无法关闭，但可通过 Security 模块配置自定义策略，详情见 [Security 文档](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


