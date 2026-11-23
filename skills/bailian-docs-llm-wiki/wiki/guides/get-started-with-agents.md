# get started with agents

百炼 Agent 服务提供一套完整的智能体开发与运行基础设施，支持从快速体验到生产级 API 集成的全链路流程。开发者可按需组合模型、工具、知识与安全能力，构建具备上下文感知、多步推理和自主执行能力的智能体应用。本文档聚焦入门路径，梳理核心能力、参数配置、调用方式及关键约束。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 `model_id` 参数动态指定底层 LLM（如 `qwen-max`、`qwen-plus` 等），模型能力由 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中“开发与运行”章节定义的托管模式决定。当前支持三类核心运行形态：  
- **Managed Agent**：全托管会话与工具执行，适合快速验证逻辑；  
- **Flow Agent**：基于可视化编排的工作流智能体，支持条件分支与多节点协同；  
- **Sandbox**：提供隔离[沙箱环境](../concepts/sandbox.md)，用于安全执行代码、浏览器操作或文件解析（详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)）。  
此外，上下文能力（RAG、Memory、Connector、ParseX）与工具能力（MCP、Skill）均以插件化方式接入，无需修改核心逻辑。

## 关键参数

调用 Agent 时需在请求体中明确以下必选/常用参数：  
- `agent_id`：Agent 实例唯一标识（创建后生成）；  
- `model_id`：指定底层推理模型 ID，必须与 Agent 所属工作空间支持的模型列表一致；  
- `input`：用户输入内容，类型为 `string` 或结构化 `object`（取决于 Agent 配置）；  
- `enable_memory`：布尔值，控制是否启用[长期记忆](../concepts/memory.md)（依赖 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中 Memory 模块配置）；  
- `tools`：显式声明本次调用允许使用的工具列表（如 `["mcp://calculator", "skill://web_search"]`），未声明的工具将被拦截。

> **注意**：部分旧版文档将 `tool_choice` 描述为自由字符串枚举（如 `"auto"`/`"required"`），但最新 API 实际仅接受 `tools` 数组 + `tool_choice: "auto"` 组合，强制指定工具需使用 `tool_choice: {"type": "function", "function": {"name": "xxx"}}` 格式，该差异已在 [raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中修正。

## 使用方式

1. **快速体验**：访问控制台 Playground，选择模板 Agent 直接对话调试（链接见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)）；  
2. **低代码构建**：在控制台使用 Flow Agent 可视化画布编排节点，配置 RAG 知识库、Memory 存储及 MCP 工具调用；  
3. **API 集成**：调用 `POST /v1/agents/{agent_id}/chat` 接口，传入标准 OpenAI 兼容格式请求体（参考 [raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；  
4. **Sandbox 扩展**：对需执行 Python 代码或网页抓取的任务，必须显式启用 Sandbox 并在 `tools` 中声明 `sandbox://python` 或 `sandbox://browser`。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32768 tokens（含上下文拼接后），超长文本需前置截断或启用 RAG 分块检索；  
- Managed Agent 默认会话有效期为 24 小时，超时后 `session_id` 失效，需重新初始化；  
- MCP 工具调用受配额与并发数限制，企业版用户需在控制台开通对应工具服务并授权；  
- Sandbox 环境禁止访问内网地址、执行系统级命令（如 `rm -rf`）、或加载未经签名的第三方包；  
- Memory 模块当前仅支持 key-value 结构化存储，不支持向量相似度检索（该能力由 RAG 独立提供）。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


