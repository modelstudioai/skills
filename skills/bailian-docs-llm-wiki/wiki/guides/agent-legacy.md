# agent legacy

`agent legacy` 指百炼平台已下线、仅在旧版控制台（华北2北京地域）支持的智能体应用架构，代号 Agent 1.0。它以零代码方式通过提示词驱动，协调知识库（RAG）与插件完成任务，不支持新版 Agent 的多节点编排、[长期记忆](../concepts/memory.md)持久化或 MCP 协议标准。该架构已停止功能迭代，新项目应使用新版 Agent，但存量应用仍可维护与调用。

## 支持的模型与功能

- **模型支持**：仅限千问系列公开模型（如 `qwen-plus`、`qwen-max`）及用户自定义部署模型；不支持新版 Agent 所兼容的第三方模型直连或混合推理路由。  
- **核心能力**：  
  - **知识库（RAG）**：支持连接私有知识库，检索结果作为上下文注入 Prompt；需手动控制切片长度，避免超出模型上下文窗口 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
  - **插件（Plugin）**：仅支持平台预置插件（如代码执行、天气查询）和自定义 HTTP 插件；超时限制为 5 秒，且不兼容 MCP v1.0+ 标准 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
  - **Prompt 管理**：支持预置模板与自定义模板，覆盖文本生成、图片生成等场景；所有模板功能仅限华北2（北京）地域 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)。  

> **注意**：文档 2 中称“Agent 1.0 应用仅旧版控制台支持”，而文档 3 和 4 多次强调“仅适用于华北2（北京）地域”，但未说明其他地域是否完全不可用。实际部署中，非北京地域调用会返回地域不支持错误，此为硬性限制，非控制台跳转问题。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| **最长回复长度** | 模型生成内容的 token 上限（不含 Prompt） | 因模型而异，`qwen-plus` 默认 4096 |
| **携带的上下文轮数** | 输入模型的最大历史对话轮数 | 建议 ≤5，过高易触发上下文截断 |
| **温度系数（temperature）** | 控制输出随机性 | `[0, 2)`，0 表示确定性输出 |
| **推理模式** | 是否启用推理增强（如思维链） | 仅部分模型支持，不支持时该参数灰显 |

- **Prompt 相关**：系统提示词最大长度 6144 字符；变量占位符格式为 `${variable}`；模板变量需在调用时显式传入，无默认值机制 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)。

## 使用方式

1. **创建应用**：  
   - 访问旧版控制台 [应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)，选择 **智能体应用** → **立即创建**；  
   - 或在新版控制台点击 **旧版 Agent 创建入口** 跳转（二者共用同一业务空间）。  

2. **配置 Prompt**：  
   - 直接编辑系统提示词；  
   - 或从 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 页面选择预置/自定义模板，点击 **创建应用** 自动填充 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)。  

3. **优化 Prompt（高级）**：  
   - 使用 **Prompt 反馈优化**：上传输入-输出样例（`.xlsx`，≤100 条），指定评测数据集（≥20 条），由 `qwen-max` 自动迭代生成候选 Prompt 并择优 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。  

4. **发布与调用**：  
   - 必须先点击 **发布** 生成版本（V1.0 起递增），最多保留 10 个版本；  
   - API 调用需使用 `YOUR_API_KEY`，Endpoint 为 `/v1/agents/{agent_id}/chat`（非新版 `/v1/agents/{id}/invoke`）。

## 限制和注意事项

- **地域锁定**：全部功能（含 Prompt 模板、反馈优化、API 调用）仅支持华北2（北京）地域，跨地域请求将失败。  
- **模型能力边界**：不支持[函数调用](../concepts/function-calling.md)（Function Calling）原生协议，插件调用依赖平台封装的 JSON Schema 解析，容错率低。  
- **知识库 Token 占用**：RAG 检索文本直接计入模型输入上下文，若未精简切片，易导致 `context_length_exceeded` 错误；需主动配置检索 Top-K 与 chunk size。  
- **[长期记忆](../concepts/memory.md)**：虽支持记忆体（Memory），但其内容仅在单次会话中合并至 Prompt，**不持久化存储**，且占用的 Token 不计费但影响上下文容量 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
- **API 创建限制**：可通过 Assistant API 创建兼容应用，但该应用**不支持控制台管理**（无法编辑、发布、查看版本），仅能通过 API 维护 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
- **弃用状态**：该架构已归档，不再接收新特性、安全补丁或模型升级支持；官方文档明确建议新项目使用新版 Agent。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


