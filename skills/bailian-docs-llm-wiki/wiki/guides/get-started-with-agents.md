# get started with agents

Agent 是百炼平台提供的可编程智能体运行与编排服务，支持开发者快速构建具备知识、工具调用和工作流能力的 AI 应用。本文档面向开发者，梳理 Agent 的核心能力边界、关键配置项及接入路径，帮助你基于实际需求选择合适类型并启动开发。所有功能均需通过控制台或 API 调用，不支持纯前端直连。

## 支持的模型与功能

Agent 本身不绑定特定大模型，而是通过 `model_id` 参数指定底层 LLM（如 `qwen-max`、`qwen-plus` 等），模型能力由 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中“开发与运行”章节定义的托管模式决定。当前支持三类核心运行形态：  
- **Managed Agent**：全托管会话生命周期与工具执行，适合对话式应用；  
- **Flow Agent**：可视化编排多步骤任务与条件分支，适用于复杂业务逻辑；  
- **Sandbox**：提供隔离沙箱环境，支持安全执行代码、浏览器操作与文件解析（如 PDF/Excel）。  

上下文增强能力（RAG、Memory、Connector、ParseX）和工具扩展能力（MCP、Skill）均为可插拔模块，按需启用。详细能力说明见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 关键参数

调用 Agent 时需在请求体中明确以下参数（以 Managed Agent API 为例）：  
- `agent_id`：必填，Agent 实例唯一标识（控制台创建后生成）；  
- `model_id`：必填，指定推理所用模型，须与 Agent 配置兼容；  
- `input`：必填，用户输入内容（字符串或结构化对象）；  
- `enable_memory` / `enable_rag`：布尔值，控制是否启用对应上下文模块；  
- `tools`：数组，显式声明允许调用的工具 ID 列表（MCP 或 Skill 类型）；  
- `sandbox_config`：仅 Sandbox Agent 需要，用于配置执行超时、资源限制等。  

> **注意**：`tools` 参数在 Flow Agent 中被 `nodes[].tool_id` 替代，且不支持运行时动态覆盖——该差异已在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 的 Flow Agent 链接文档中明确，但部分旧版 API 示例仍沿用全局 `tools` 字段，应以最新 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 为准。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，无需编码即可基于模板创建并调试 Agent；  
2. **API 集成**：调用 `/v1/agents/{agent_id}/chat`（Managed）、`/v1/flows/{flow_id}/run`（Flow）或 `/v1/sandbox/run`（Sandbox）端点，参考 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 获取完整请求示例与鉴权方式；  
3. **本地开发联调**：使用 SDK（Python/Java）封装调用逻辑，SDK 自动处理重试、流式响应解析与错误映射。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32768 token（含系统提示词与上下文），超出将触发截断，具体策略参见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)；  
- Sandbox 模式下，代码执行默认超时 30 秒，不可修改；浏览器操作仅支持 Chromium 内核，不支持 headless 模式外的 GUI 交互；  
- RAG 检索结果默认最多返回 5 个 chunk，`top_k` 参数仅在启用 `enable_rag: true` 时生效；  
- 所有 Agent 实例共享账户级 QPS 限额（默认 5 QPS），高并发场景需提工单申请提升。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


