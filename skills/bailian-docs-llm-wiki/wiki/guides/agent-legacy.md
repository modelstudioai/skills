# agent legacy

`agent legacy` 指百炼平台早期推出的智能体（Agent 1.0）能力体系，基于 Flow Agent 架构实现零代码、提示词驱动的工具调用与知识增强。该体系已逐步被新版 Agent（如 MCP、Assistant API 等）替代，但仍在旧版控制台中维护，适用于需快速落地 RAG+插件组合场景的存量应用。开发者应优先评估新版能力，仅在兼容性或特定功能需求下使用本模块。

## 支持的模型与功能

- **模型支持**：仅限旧版控制台可用模型，包括 `千问-Plus`、`千问-Max` 等千问系列模型及用户自定义部署模型；不支持新版控制台中新增的 Qwen2.5、Qwen3 等模型。
- **核心能力**：
  - **知识库（RAG）**：通过[检索增强生成](../concepts/rag.md)接入私有知识，检索结果直接注入上下文，但占用模型输入 token；详情见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
  - **插件（Plugin）**：调用平台预置工具（如代码执行、天气查询）或自定义 MCP；超时限制为 5 秒，详见[插件概述](raw/application-user-guide/agent-development/llm-application/plug-in/plug-in-overview.md)（注：该文档属新版路径，旧版 Agent 插件能力受限，仅支持部分同步型 MCP）。
  - **[长期记忆](../concepts/long-term-memory.md)**：支持存储用户级对话历史，内容合并入 Prompt 后参与推理，**[Token](../concepts/token.md) 不计费**，但影响上下文长度。

> **注意**：文档 2 中称“Agent 1.0 应用仅旧版控制台支持”，而文档 3 和 4 多次强调“仅适用于华北2（北京）地域”，但未在文档 2 的快速开始或模型配置章节明确地域限制。实际使用中，若在非北京地域调用旧版 Agent API 或创建应用，可能返回地域不可用错误。建议以控制台实际可选区域为准。

## 关键参数

在智能体配置界面中，模型参数通过下拉框右侧设置图标展开配置：

- **最长回复长度**：模型生成内容上限（不含系统提示词），具体上限依模型而定（如 `千问-Plus` 默认 8192）。
- **携带的上下文轮数**：最大历史对话轮数，影响多轮连贯性；值过高易触发上下文截断。
- **温度系数（temperature）**：取值范围 `[0, 2)`，控制输出随机性；`0` 表示确定性输出，推荐问答类任务设为 `0.1–0.5`。
- **推理模式**：仅部分模型支持，启用后可提升复杂逻辑推理稳定性；不支持的模型该选项置灰。

此外，Prompt 相关参数通过独立模块管理：
- **系统提示词**：定义角色、约束、工具调用指引等，直接影响决策质量。
- **Prompt 模板**：支持预置模板（如营销文案生成）和自定义模板（含 ICIO/CRISPE/RASCEF 框架），模板变量格式为 `${variable}`，最大字符数 6144；参见 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)。

## 使用方式

### 创建与配置
1. 进入[旧版百炼控制台应用管理页](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)，选择 **智能体应用 > 立即创建**（新版控制台需点击“旧版 Agent 创建入口”跳转）。
2. 选择模型（如 `千问-Plus`），配置上述关键参数。
3. 设置系统提示词，或从 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 页面选择预置/自定义模板填充。
4. 绑定知识库（RAG）或启用插件（需提前在插件中心授权）。

### 调试与发布
- 在线调试：于文本对话界面输入测试问题（支持文件上传），实时查看 token 统计与响应。
- 发布应用：必须发布后方可 API 调用；每个应用最多保存 10 个版本，新版本自动覆盖最旧版本。
- API 调用：在“发布渠道 > API”中获取密钥与调试入口，请求体需包含 `prompt`、`model` 及 `parameters` 字段。

### Prompt 优化进阶
- **模板化复用**：通过控制台“提示词管理”创建自定义模板，支持基于 Prompt 工程框架（ICIO/CRISPE/RASCEF）结构化构建；详见 [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)。
- **样例驱动优化**：使用“Prompt反馈优化”功能，上传输入-输出样例（`.xlsx`，≤100 条）与评测数据（≥20 条），由 `千问-Max` 自动迭代生成高匹配度 Prompt；操作入口位于 [提示词管理 > 反馈优化](https://bailian.console.aliyun.com/flow-agent/prompt-manage)。

## 限制和注意事项

- **地域限制**：所有旧版 Agent 功能（含 Prompt 模板、反馈优化）**仅华北2（北京）地域可用**，其他地域控制台可能无法加载相关页面或返回 `RegionNotSupported` 错误。
- **模型与插件兼容性**：旧版 Agent 不支持异步插件（如长耗时文生视频）、流式响应插件；自定义插件须满足 5 秒超时约束。
- **知识库 [Token](../concepts/token.md) 占用**：RAG 检索文本计入模型输入上下文，若未合理配置切片长度或 top-k，易导致 `context_length_exceeded` 错误。
- **[长期记忆](../concepts/long-term-memory.md)副作用**：记忆体内容虽不计费，但会挤占 prompt 空间，降低知识库/插件调用所需上下文余量。
- **弃用风险**：该体系无新功能迭代，官方文档已标注“旧版”，后续将逐步下线；新建项目请优先采用 [Assistant API](https://help.aliyun.com/zh/model-studio/assistant-api) 或 MCP 架构。
- **API 创建限制**：可通过 Assistant API 创建类似应用，但**不支持控制台管理**（如版本回滚、Prompt 编辑），详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


