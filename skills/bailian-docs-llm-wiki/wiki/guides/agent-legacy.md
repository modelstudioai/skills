# agent legacy

`agent legacy` 指百炼平台早期推出的基于 Flow 架构的智能体能力体系（即 Agent 1.0），以零代码方式支持 RAG 知识库接入、插件调用和结构化 Prompt 管理，适用于需快速构建业务导向型对话应用但暂不依赖复杂工作流编排的场景。该体系当前仅在旧版控制台维护，新版控制台已转向更灵活的 Agent 2.0（Flow Agent）架构。

## 支持的模型与功能

- **模型支持**：仅限旧版控制台可用模型，包括 `千问-Plus`、`千问-Max` 等千问系列模型及用户自定义部署模型；不支持新版控制台中新增的长上下文或推理增强模型（如 Qwen2.5-72B-Instruct-1M）。  
- **核心能力**：
  - **知识库（RAG）**：支持连接私有知识库，检索结果直接注入模型上下文，适用于垂直领域问答；[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 明确指出“从知识库中检索到的文本会占用模型的上下文窗口”，需主动调优切片长度与检索策略。
  - **插件（Plugin）**：可调用平台预置 MCP（如代码执行、文生图）及自定义插件；所有插件调用超时限制为 **5 秒**（见[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 常见问题）。
  - **Prompt 工程支持**：提供预置模板（如营销文案生成）、自定义模板（含 ICIO/CRISPE/RASCEF 框架）及基于样例的自动优化（Prompt Feedback Optimization），全部通过 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 统一维护。

> **注意**：文档 3 和文档 4 均强调“本文档仅适用于华北2（北京）地域”，但文档 2 的快速开始流程未限定地域。实际使用中，若在非北京地域调用 `ListPromptTemplates` 或 `CreatePromptTemplate` 接口，将返回 `InvalidRegionId` 错误——此为地域强约束，非文档疏漏。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| **最长回复长度** | 模型生成内容的 token 上限（不含系统提示词与历史输入） | 因模型而异，如 `千问-Plus` 默认 8192 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **携带的上下文轮数** | 输入模型的最大历史对话轮数 | 整数，建议 ≤ 10 轮以避免上下文溢出 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **温度系数（temperature）** | 控制输出随机性 | `[0, 2)`，0 表示确定性输出 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **推理模式** | 是否启用模型内置推理能力（如思维链） | 仅支持明确标注“支持推理模式”的模型 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **Prompt 变量** | 模板中动态占位符（如 `${topic}`） | 最大支持 6144 字符总长；变量名需符合 `${key}` 格式 | [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) |

## 使用方式

1. **创建入口**：仅可通过旧版控制台访问——在新版控制台点击“旧版 Agent 创建入口”跳转，或直接访问 [旧版应用管理页](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)。  
2. **Prompt 集成**：
   - 控制台：在预置/自定义模板卡片点击 `··· → 创建应用`，模板内容自动填充至系统提示词框；变量（如 `${platform}`）需手动替换为实际值。  
   - API：调用 `GetPromptTemplate` 获取模板内容与 `variables` 列表，按需填充后作为 `system_prompt` 发送给智能体 API（见 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）。  
3. **反馈优化流程**：在 [提示词管理 → 反馈优化](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 中新建优化包，上传 **5–10 条样例数据**（覆盖所有目标类别）和 **≥20 条评测数据**，选择 `千问-Max` 作为推理模型启动优化（见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)）。  

## 限制和注意事项

- **地域限制**：所有 Prompt 模板相关功能（创建、调用、优化）仅在 **华北2（北京）地域** 可用，跨地域调用将失败。  
- **版本隔离**：Agent 1.0 应用与新版 Agent 2.0 应用完全隔离，无法迁移配置或共享知识库/插件实例。  
- **[长期记忆](../concepts/long-term-memory.md)计费**：记忆体内容虽不单独计费，但会合并入 Prompt 传递给模型，**增加模型输入 [Token](../concepts/token.md) 消耗**（见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 计费说明）。  
- **API 创建限制**：通过 Assistant API 创建的应用 **不支持控制台管理**，且无法使用 Agent 1.0 特有的 Prompt 模板、RAG 或插件能力（见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 常见问题）。  
- **插件超时**：自定义插件必须在 **5 秒内完成响应**，超时将导致智能体任务中断并返回错误。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


