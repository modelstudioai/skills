# agent legacy

`agent legacy` 指百炼平台早期推出的基于 Flow Agent 架构的智能体（Agent 1.0）能力体系，面向零代码/低代码场景，通过提示词驱动、RAG 知识库接入与插件调用实现模型能力扩展。该体系已逐步被新版 Agent（如 MCP 驱动的 Agent 2.0）替代，但仍在旧版控制台和部分存量应用中持续维护与使用。

## 支持的模型与功能

- **模型支持**：仅限旧版控制台可用模型，包括 `千问-Plus`、`千问-Max` 等千问系列模型及用户自定义部署模型；不支持新版控制台新增的 MoE 或多模态专用模型。  
- **核心能力**：
  - **知识库（RAG）**：支持连接私有知识库，检索结果自动注入模型上下文，适用于垂直领域问答；[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 明确指出“从知识库中检索到的文本会占用模型的上下文窗口”，需谨慎配置切片长度与检索数量。
  - **插件（Plugin）**：提供官方预置插件（如代码执行、天气查询、文生图）及自定义插件接入能力；自定义插件有严格超时限制（5 秒），详见[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
  - **[长期记忆](../concepts/long-term-memory.md)**：支持对话级记忆存储，内容在调用时合并入 Prompt，**占用 [Token](../concepts/token.md) 但暂不计费**（见[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 计费说明）。

> **注意**：文档 3 和文档 4 均强调 Prompt 模板功能“仅适用于华北2（北京）地域”，但文档 2 的快速开始流程未限定地域，且控制台链接为通用域名。实际使用中，若在非北京地域调用 Prompt 模板 API 可能失败，建议以文档 3 和 4 的地域约束为准。

## 关键参数

在创建智能体时可配置以下模型级参数（位于模型下拉框右侧设置图标中）：

- **最长回复长度**：模型生成内容的字符上限（不含系统提示词与历史输入），具体上限依模型而异；
- **携带的上下文轮数**：输入模型的最大历史对话轮数，影响多轮连贯性，建议根据任务复杂度设为 3–10 轮；
- **温度系数（Temperature）**：取值范围 `[0, 2)`，控制输出随机性；数值越低（如 0.1）越确定、一致；越高（如 1.5）越多样、发散；
- **推理模式**：仅对支持该能力的模型开放；启用后可提升复杂逻辑链路的稳定性，但可能增加延迟。

此外，Prompt 模板与反馈优化模块提供独立参数：
- Prompt 模板变量（如 `${topic}`）需在填充时确保类型与长度符合预期，模板内容总长上限为 **6144 字符**（见[Promp模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）；
- Prompt 反馈优化任务中，**样例数据建议 5–10 条**（覆盖全部类别），**评测数据建议 ≥20 条**，且必须为高质量输入-输出对（见[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)）。

## 使用方式

1. **控制台创建**：  
   - 访问旧版控制台 [应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)，选择**智能体应用**页签 → **立即创建**；  
   - 在配置界面选择模型、填写系统提示词（支持直接粘贴或从[Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)中“创建应用”快捷填充）；  
   - 可选添加知识库、插件，并完成发布（发布是 API 调用前提）。

2. **API/SDK 调用**：  
   - 发布后，在应用**发布渠道**页签获取 API Key 与 Endpoint；  
   - 请求体需包含 `prompt`（系统提示词）、`messages`（对话历史）等字段，格式与标准 LLM API 一致；  
   - 若使用 Prompt 模板，需先调用 `GetPromptTemplate` 接口（见[Promp模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）获取模板并填充变量，再传入智能体 API。

3. **Prompt 工程增强**：  
   - 通过[自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)页面，使用 ICIO/CRISPE/RASCEF 框架结构化构建提示词；  
   - 对已有 Prompt 效果不佳时，可使用[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)功能，上传样例与评测集进行自动化迭代。

## 限制和注意事项

- **控制台兼容性**：Agent 1.0 仅支持旧版控制台；新版控制台需点击“旧版 Agent 创建入口”跳转，且旧版控制台顶部提供“前往新版”单向链接（见[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）；  
- **版本管理**：每个应用最多保存 **10 个历史版本**，超出后新版本自动覆盖最早版本；回滚操作（“覆盖当前草稿”）不可逆；  
- **[Token](../concepts/token.md) 计费细节**：知识库检索文本、[长期记忆](../concepts/long-term-memory.md)内容均计入模型输入 [Token](../concepts/token.md) 并产生费用，但记忆体本身存储免费；插件调用若涉及第三方服务（如文生图），其费用由第三方收取，百炼不额外计费（见[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）；  
- **地域锁定**：Prompt 模板创建、管理与调用功能**仅限华北2（北京）地域**，跨地域调用将失败；  
- **API 创建限制**：虽支持通过 Assistant API 创建类智能体应用，但此类应用**不支持控制台管理**（如版本回滚、插件配置），仅限纯 API 场景（见[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) 常见问题）。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


