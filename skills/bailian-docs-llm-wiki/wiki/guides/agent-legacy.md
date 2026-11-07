# agent legacy

`agent legacy` 指百炼平台早期推出的基于 Prompt 驱动、零代码配置的智能体应用能力（即 Agent 1.0），核心是通过系统提示词协调模型、知识库（RAG）和插件完成多步任务。该能力已迁移至旧版控制台，新版控制台默认提供更灵活的 Flow Agent（2.0+），但 Agent 1.0 仍被部分存量应用和特定工作流依赖。其设计强调易用性与快速上线，适用于对工具调用自主性要求高、但无需复杂流程编排的场景。

## 支持的模型与功能

- **模型支持**：以千问系列为主（如 `千问-Plus`、`千问-Max`），支持自定义部署模型；模型作为推理与决策核心，需在旧版控制台[应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)中选择。
- **核心扩展能力**：
  - **知识库（RAG）**：连接私有文档，检索结果注入上下文，显著提升垂直领域问答准确率，减少幻觉 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
  - **插件（MCP）**：调用预置工具（如代码执行、天气查询、文生图）或自定义插件，超时限制为 5 秒；不支持 MCP 的模型无法启用此能力。
  - **[长期记忆](../concepts/long-term-memory.md)**：存储用户对话历史，内容合并入 Prompt 传递给模型（Token 消耗计入输入，但**暂不计费**）。

> **注意**：文档 2 中明确说明“Agent 1.0 应用仅旧版控制台支持”，而文档 4 和 5 的操作路径（如 `https://bailian.console.aliyun.com/flow-agent/prompt-manage`）指向新版控制台的 Prompt 管理页。二者控制台入口与功能归属存在事实割裂——Prompt 模板能力虽可复用于 Agent 1.0 应用（见文档 4 “使用Prompt模板”节），但其本身属于独立模块，并非 Agent 1.0 原生组件。

## 关键参数

在模型配置中可调整以下运行时参数（通过模型下拉框右侧设置图标进入）：

- **最长回复长度**：生成内容的 token 上限（不含提示词），具体上限依模型而定。
- **携带的上下文轮数**：输入模型的最大历史对话轮数，影响多轮一致性。
- **温度系数（Temperature）**：取值范围 `[0, 2)`，控制输出随机性（高值→多样性高，低值→确定性强）。
- **推理模式**：仅对支持该能力的模型开放，用于增强逻辑链式推理。

## 使用方式

1. **创建应用**：访问旧版控制台 [应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)，选择 **智能体应用** → **立即创建**；或在新版控制台“创建智能体”弹窗底部点击 **旧版 Agent 创建入口** 跳转。
2. **配置能力**：
   - 在模型选择后，于 **系统提示词** 区域编写角色定义、约束条件及工具调用引导（例如：“你是一名客服，必须优先调用‘知识库查询’插件回答产品问题”）。
   - 添加知识库：关联已创建的知识库实例，注意检索文本占用上下文窗口。
   - 启用插件：从插件列表勾选所需工具，自定义插件需提前注册。
3. **Prompt 复用（可选）**：通过 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 页面创建或选用预置/自定义模板，点击模板卡片的 **··· → 创建应用**，自动填充提示词内容（含变量 `${var}`）。
4. **发布与调用**：应用需**先发布**（版本 ID 从 V1.0 开始递增，最多保留 10 个版本）；发布后可通过 API/SDK 调用，或集成至钉钉、微信公众号等渠道。

## 限制和注意事项

- **地域限制**：自定义 Prompt 模板与反馈优化功能**仅支持华北2（北京）地域**（见文档 3 和 4 开头说明）。
- **控制台隔离**：Agent 1.0 的生命周期管理（创建、发布、版本回滚）完全依赖旧版控制台；新版控制台的 Prompt 工具（如反馈优化）虽可产出 Prompt 供其使用，但无法直接管理 Agent 1.0 应用本身 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。
- **Token 计费细节**：
  - 知识库检索文本、[长期记忆](../concepts/long-term-memory.md)内容均计入模型输入 Token，增加模型调用费用；
  - 插件调用若涉及第三方 API，费用由第三方收取，百炼不额外计费。
- **调试与优化**：若知识库未生效，需先进行命中测试并调整检索配置；提示词效果不佳时，可结合 [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md) 中的 ICIO/CRISPE/RASCEF 框架重构，或使用反馈优化功能基于真实 I/O 样例迭代生成 Prompt。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


