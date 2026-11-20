# agent legacy

`agent legacy` 指百炼平台早期推出的基于 Flow Agent 架构的智能体（Agent 1.0）能力体系，面向零代码/低代码场景提供知识库（RAG）、插件调用、系统提示词配置等核心功能。该体系已逐步被新版 Agent（如 MCP 驱动的 Assistant）替代，但仍在旧版控制台中完整支持，适用于需快速落地、无需深度编排的业务集成场景。其能力边界、参数配置与使用路径均与当前主流 Agent 架构存在显著差异。

## 支持的模型与功能

- **模型支持**：仅限旧版控制台可用模型，包括 `千问-Plus`、`千问-Max` 等千问系列模型及用户自定义部署模型；不支持新版控制台中新增的推理优化型或长上下文专用模型。  
- **核心功能**：
  - **知识库（RAG）**：支持连接私有知识库，检索结果直接注入模型上下文，用于垂直领域问答；[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 明确指出“从知识库中检索到的文本会占用模型的上下文窗口”，需主动协调检索粒度与模型输入长度。
  - **插件（Plugin）**：调用平台预置工具（如代码执行、天气查询）或自定义插件；所有插件调用超时限制为 **5 秒**，且不支持流式响应或异步回调。
  - **[长期记忆](../concepts/long-term-memory.md)**：支持存储用户级对话历史，但内容仅在单次请求中合并入 Prompt，**不额外计费**（Token 消耗计入模型调用）；该能力未在新版 Agent 中复现，属 legacy 特有设计。

> **注意**：文档 2 中称“Agent 1.0 应用仅旧版控制台支持”，而文档 4 的 Prompt 模板管理页面 URL（`https://bailian.console.aliyun.com/flow-agent/prompt-manage`）仍指向旧版控制台路径，表明整个 `agent legacy` 生态未迁移至新版控制台，开发者必须切换入口使用。

## 关键参数

在模型配置环节可调整以下运行时参数（通过模型下拉框右侧设置图标进入）：

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| **最长回复长度** | 模型生成内容的 token 上限（不含系统提示词与历史输入） | 因模型而异，如 `千问-Plus` 默认 2048，上限通常 ≤ 8192 |
| **携带的上下文轮数** | 输入模型的最大历史对话轮数（非 token 数） | 建议 ≤ 10 轮，过多易触发上下文截断 |
| **温度系数（temperature）** | 控制输出随机性 | `[0, 2)`，0 表示确定性输出，推荐生产环境设为 `0.3–0.7` |
| **推理模式** | 是否启用结构化推理（如思维链） | 仅部分模型支持；不支持的模型该选项不可见 |

> **注意**：文档 5 在“Prompt反馈优化”中明确推荐使用 `千问-Max` 作为推理模型，但文档 2 未将 `千问-Max` 列入基础模型选择示例（仅列 `千问-Plus`），实际可用性需以旧版控制台下拉菜单为准，存在文档滞后风险。

## 使用方式

1. **创建入口**：  
   - 必须通过[旧版百炼控制台](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center) → **应用管理** → **智能体应用** → **立即创建**；  
   - 或在新版控制台点击“旧版 Agent 创建入口”跳转（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。

2. **Prompt 管理**：  
   - 支持两种模板体系：**预置模板**（开箱即用，不可修改）和**自定义模板**（可编辑、可基于 Prompt 工程框架如 ICIO/CRISPE/RASCEF 创建）；  
   - 模板变量格式为 `${variable}`，最大字符长度 **6144**（[Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）；  
   - 自定义 Prompt 可通过控制台“提示词管理”页面创建，或调用 `CreatePromptTemplate` API。

3. **优化与调试**：  
   - 提供 **Prompt 反馈优化** 功能：基于用户提供的输入-输出样例（`.xlsx` 文件）自动迭代生成更优 Prompt，需指定评测数据集（建议 ≥20 条）；  
   - 调试时可在模型界面右侧输入测试问题，实时查看 token 统计（输入/输出 token 数）及响应内容。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板相关功能（自定义模板、反馈优化）**仅支持华北2（北京）地域**，其他地域控制台不可见（[自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)、[Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）。
- **版本与发布**：  
  - 每个应用最多保存 **10 个历史版本**，超出后新版本自动覆盖最早版本；  
  - 发布是 API 调用前提，未发布应用无法通过 SDK/API 访问（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
- **计费关联**：  
  - 知识库检索内容、[长期记忆](../concepts/long-term-memory.md)内容均计入模型输入 token，**增加模型调用费用**；  
  - 插件调用按所选 MCP 类型计费（如文生图按次收费），第三方 API 费用由服务商单独收取。
- **兼容性警告**：  
  - 使用 Assistant API 创建的应用**不支持控制台管理**，且功能不等价于 `agent legacy`（如无 RAG 集成入口）；  
  - 旧版 Agent 应用无法迁移到新版控制台，升级需重建。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


