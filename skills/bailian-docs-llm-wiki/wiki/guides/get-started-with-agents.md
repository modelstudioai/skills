# get started with agents

Agent 是百炼平台提供的可编程智能体运行与编排能力，支持开发者快速构建具备知识、工具调用、记忆与安全治理能力的 AI 应用。本文档梳理核心能力边界、关键配置项及接入路径，适用于希望以最小成本启动 Agent 开发的工程师。所有功能均需通过百炼控制台或 API 调用，不依赖本地部署。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 `model_id` 参数动态指定底层 LLM（如 `qwen-max`、`qwen-plus` 等），模型能力由 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的“开发与运行”模块统一承载。当前支持三类核心运行形态：  
- **Managed Agent**：托管会话生命周期、工具执行与环境隔离，适合对话式应用；  
- **Flow Agent**：基于可视化节点编排多步逻辑与条件分支，适用于复杂工作流；  
- **Sandbox**：提供代码解释器、浏览器自动化与文件解析沙箱，保障不可信代码安全执行。  
上下文增强能力（RAG、Memory、Connector、ParseX）和工具扩展能力（MCP、Skill）均为可插拔模块，按需启用。

## 关键参数

调用 Agent 时必须指定以下参数（以 Managed Agent API 为例）：  
- `agent_id`：平台生成的唯一 Agent 标识，创建后固定；  
- `model_id`：所用大模型 ID，需与 Agent 配置中声明的兼容模型一致；  
- `input`：用户输入文本，类型为 `string`；  
- `enable_memory`：布尔值，启用后自动读写[长期记忆](../concepts/long-term-memory.md)（依赖 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中 Memory 模块配置）；  
- `tools`：显式声明需调用的工具列表（如 `["mcp://calculator", "connector://crm"]`），未声明则不触发工具调用。  
> **注意**：`tools` 参数在 Flow Agent 中被 `nodes` 配置替代，详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 的“Flow Agent”链接指向文档，二者参数体系不兼容，不可混用。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，选择模板并直接对话，无需编码；  
2. **API 接入生产系统**：参考 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中“通过 API 接入”链接指向的 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)，使用 `POST /agents/{agent_id}/invoke` 发起调用；  
3. **自定义开发**：通过控制台创建 Agent 后，在“上下文”和“工具与能力包”中分别配置 RAG 知识库、Memory 实例、MCP 工具服务等，所有配置项均实时生效。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32,768 字符，超长内容需预处理截断或分片；  
- Sandbox 沙箱内 Python 执行超时默认为 30 秒，不可修改；浏览器操作（Puppeteer）仅支持 Chromium 内核，不支持插件或 localStorage 持久化；  
- MCP 工具注册后需手动授权调用权限，且仅支持 HTTP/HTTPS 协议的 OpenAPI 3.0 描述；  
- Memory 模块的[长期记忆](../concepts/long-term-memory.md)存储容量上限为 100 MB / Agent 实例，超出后写入失败（错误码 `MEMORY_QUOTA_EXCEEDED`）。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


