# agent legacy

`agent legacy` 指百炼平台早期推出的智能体（Agent 1.0）能力体系，基于 Flow Agent 架构实现零代码、提示词驱动的工具调用与知识增强。该体系已逐步被新版 Agent（如 MCP 驱动的 Agent 2.0）替代，但仍在华北2（北京）地域旧版控制台中持续维护，适用于需快速落地 RAG+插件组合场景的存量应用。开发者应优先评估迁移至新版架构的可行性，尤其在涉及长期维护或复杂工作流时。

## 支持的模型与功能

- **模型支持**：仅限旧版控制台可用模型，包括 `千问-Plus`、`千问-Max` 等千问系列模型及用户自定义部署模型；不支持新版控制台中新增的 MoE 或多模态专用模型。  
- **核心能力**：
  - **知识库（RAG）**：支持连接私有知识库，检索结果作为上下文注入 Prompt，显著降低幻觉；但检索文本占用模型上下文窗口，需主动控制切片长度 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
  - **插件（Plugin）**：可调用平台预置插件（如代码执行、天气查询）或自定义插件；所有插件调用超时限制为 **5 秒**，超时即失败，无重试机制 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
  - **[长期记忆](../concepts/long-term-memory.md)**：支持存储用户级记忆体，内容在问答时合并入 Prompt，**[Token](../concepts/token.md) 不计费**，但会增加实际输入 [Token](../concepts/token.md) 消耗。  

> **注意**：文档 3 和文档 4 均强调“本文档仅适用于华北2（北京）地域”，而文档 2 中的控制台链接（`bailian-legacy.console.aliyun.com`）明确指向旧版控制台，表明该能力不具备跨地域通用性，且新版控制台已移除对 Agent 1.0 的直接创建入口。

## 关键参数

在模型配置环节可调整以下运行时参数（通过模型下拉框右侧设置图标进入）：

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| 最长回复长度 | 模型生成内容的长度上限（不含 Prompt） | 因模型而异，如 `千问-Plus` 上限为 8192 tokens |
| 携带的上下文轮数 | 输入模型的最大历史对话轮数 | 轮数越多，上下文越长，[Token](../concepts/token.md) 消耗越高 |
| 温度系数（temperature） | 控制输出随机性 | `[0, 2)`，0 表示确定性输出，接近 2 时多样性高但稳定性下降 |
| 推理模式 | 是否启用推理增强（如思维链） | 仅部分模型支持；不支持的模型该选项不可见 |

系统提示词（System Prompt）是行为定义的核心，需明确角色、输出格式、约束条件及工具调用指引；其效果可通过[文本对话](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)界面实时验证。

## 使用方式

### 1. 创建与配置
- 仅能通过**旧版控制台**创建：访问 [应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)，选择「智能体应用」页签 → 「立即创建」；新版控制台需点击「旧版 Agent 创建入口」跳转 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
- 提示词可直接编写，或复用 Prompt 模板：在[提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage)页面，通过预置/自定义模板卡片的「··· → 创建应用」一键填充至提示词编辑框 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)。  

### 2. Prompt 工程支持
- **模板类型**：分预置模板（开箱即用，不可修改）和自定义模板（支持编辑、复制、删除）；预置模板需通过 API（`ListPromptTemplates` with `type=System`）获取完整变量列表 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)。  
- **自动优化**：使用「Prompt反馈优化」功能，基于输入-输出样例（`.xlsx`）和评测数据集，由 `千问-Max` 多轮迭代生成更贴合业务的 Prompt；样例建议 5–10 条（覆盖全类别），评测数据建议 ≥20 条 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。  

### 3. 发布与调用
- **发布前提**：必须先发布应用才能调用；每个应用最多保存 10 个版本，超出后新版本自动覆盖最早版本 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
- **API 调用**：在「发布渠道」页签 → 「API」卡片 → 「API 调试」或「API KEY」获取密钥；请求需携带 `YOUR_API_KEY`，且 `workspaceId` 必须与创建时一致 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  

## 限制和注意事项

- **地域与控制台锁定**：全部功能仅在华北2（北京）地域的旧版控制台可用；新版控制台不支持创建或管理 Agent 1.0 应用，且无平滑迁移路径。  
- **插件超时刚性**：自定义插件调用严格限制为 **5 秒**，超时即报错，无法通过参数延长；需确保插件逻辑轻量或具备异步回调能力。  
- **知识库 Token 隐性成本**：RAG 检索出的文本计入模型输入 Token，可能意外推高费用；若知识库命中率低，应优先优化检索策略而非增加切片长度 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。  
- **Prompt 模板字符上限**：控制台中模板填充后的提示词输入框最大支持 **6144 字符**，超出部分将被截断，需在模板设计阶段预留空间。  
- **[长期记忆](../concepts/long-term-memory.md) Token 计费例外**：记忆体内容虽不单独计费，但会增大实际输入 Token，影响模型调用费用；需权衡记忆深度与成本。  
- **API 创建的应用不可控台管理**：通过 Assistant API 创建的类 Agent 应用，**不支持在控制台编辑、发布或调试**，仅能通过 API 维护 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


