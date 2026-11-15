# get started with agents

Agent 是百炼平台提供的可编程智能体运行与编排能力，支持开发者快速构建具备知识、工具调用、记忆与安全治理能力的 AI 应用。本文档梳理核心能力边界、关键配置项及接入路径，适用于希望以最小成本启动 Agent 开发的工程师。所有功能均需通过百炼控制台或 API 调用，不支持本地离线部署。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 `model_id` 参数动态指定底层 LLM（如 `qwen-max`、`qwen-plus` 等），模型选择直接影响推理质量与响应延迟。功能维度上分为三类核心组件：  
- **运行时类型**：`Managed Agent`（托管会话与工具执行）、`Flow Agent`（可视化工作流编排）、`Sandbox`（隔离式代码/浏览器/文件执行环境）；  
- **上下文增强**：`RAG`（知识库检索）、`Memory`（[长期记忆](../concepts/long-term-memory.md)存储与召回）、`Connector`（企业系统对接）、`ParseX`（多格式文档结构化解析）；  
- **能力扩展**：`MCP`（Model Context Protocol 工具协议接入）与 `Skill`（预封装能力包，如天气查询、数据库操作等）。  
详细能力对比与适用场景见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 关键参数

调用 Agent 时需显式指定以下参数（部分为必填）：  
- `agent_id`：Agent 实例唯一标识（控制台创建后生成，或通过 API 创建返回）；  
- `model_id`：底层大模型 ID，必须与当前 Agent 所属项目支持的模型列表一致；  
- `input`：用户输入文本，类型为 `string`；  
- `stream`：布尔值，启用流式响应（默认 `false`）；  
- `tools`：工具调用白名单数组，仅当 Agent 配置了 MCP 或 Skill 且显式声明时生效；  
- `memory_id`（可选）：指定关联的 Memory 实例 ID，用于跨会话状态保持。  
参数约束与默认行为详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的“开发与运行”章节。

## 使用方式

### 方式一：控制台快速体验  
访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8)，无需编码即可基于模板创建并对话测试 Agent。该入口默认使用 `Managed Agent` 运行时，适合验证基础逻辑与工具集成效果。

### 方式二：API 接入生产系统  
通过 `POST /api/v1/agents/{agent_id}/chat` 接口调用（参考 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。需在请求 Header 中携带 `Authorization: Bearer <access_token>`，Body 中传入标准参数。注意：Flow Agent 和 Sandbox 当前暂不支持直连该统一 chat 接口，需分别调用其专属 API（参见对应 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的链接）。

> **注意**：原始文档中 `Sandbox` 的 Quick Start 链接指向 `sandbox-quick-start.md`，但该路径实际已重定向至新版 `sandbox-getting-started.md`；建议以控制台最新文档导航为准，避免使用过期路径。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32768 字符，超长内容需前置截断或分块处理；  
- `Managed Agent` 默认会话有效期为 24 小时，超时后 `memory_id` 关联的状态不可恢复；  
- `Flow Agent` 不支持嵌套调用其他 Flow Agent，仅允许调用 Managed Agent 或外部 HTTP 工具；  
- 所有工具调用（MCP/Skill）均受沙箱资源配额限制（CPU/内存/执行时长），超限将直接中断并返回 `500 ToolExecutionTimeout`；  
- 安全策略（如内容过滤、代码执行禁用）需在 Agent 创建时显式开启，运行时无法动态修改——相关配置说明见 [Security](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md) 文档。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


