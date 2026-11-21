# agent legacy

`agent legacy` 指百炼平台早期推出的基于 Prompt 驱动、零代码配置的智能体能力体系（即 Agent 1.0），核心是通过系统提示词协调知识库（RAG）与插件调用，实现模型能力的外延扩展。该体系已逐步被新版 Agent（如 Flow Agent 2.0 / MCP 架构）替代，但仍在旧版控制台中维护，适用于对低代码快速交付有明确需求、且无需复杂工作流编排的场景。

## 支持的模型与功能

- **模型支持**：仅限旧版控制台可用模型，包括 `千问-Plus`、`千问-Max` 等千问系列模型及用户自定义部署模型（需兼容旧版 API 协议）。不支持新版控制台中新增的 `Qwen2.5` 及更高版本模型。
- **核心能力**：
  - **知识库（RAG）**：支持连接私有知识库，检索结果自动注入上下文；检索文本占用模型输入 token，需注意上下文窗口限制（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
  - **插件（MCP）**：提供预置插件（如代码执行、天气查询、文生图）及自定义插件接入能力；所有插件调用超时限制为 **5 秒**（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
  - **[长期记忆](../concepts/long-term-memory.md)（实验性）**：支持存储用户级记忆体，内容在对话中自动拼入 Prompt，但**记忆体 token 不计费**（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。

> **注意**：文档 3 和文档 4 均声明“本文档仅适用于华北2（北京）地域”，但文档 2 的快速开始流程未限定地域。实际使用中，`agent legacy` 全链路（含 Prompt 模板、知识库、插件）仅在北京地域稳定可用，其他地域调用可能失败或返回空响应。

## 关键参数

在智能体配置界面中，模型参数通过下拉框右侧设置图标展开配置：

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| **最长回复长度** | 模型生成内容的 token 上限（不含系统提示词与历史对话） | 因模型而异，`千问-Plus` 默认 4096，上限通常 ≤ 8192 |
| **携带的上下文轮数** | 输入模型的最大历史对话轮数（每轮含 user/assistant） | 推荐 3–10 轮；轮数过多易触发上下文截断 |
| **温度系数（temperature）** | 控制输出随机性 | `[0, 2)`，0 表示确定性输出，1.0 为默认值 |
| **推理模式** | 是否启用结构化推理（如思维链） | 仅部分模型支持；不支持的模型该选项不可见 |

此外，Prompt 模板机制提供另一层关键参数化能力：通过 `${variable}` 占位符实现动态内容注入，模板变量在调用时由业务数据填充（[Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）。

## 使用方式

1. **创建入口**：仅可通过旧版百炼控制台创建 —— 在新版控制台点击“创建智能体”弹窗底部的 **旧版 Agent 创建入口**，跳转至 `https://bailian-legacy.console.aliyun.com/...`（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
2. **Prompt 配置**：
   - 直接编辑系统提示词（推荐使用 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 中的预置/自定义模板，通过“创建应用”一键填充）；
   - 或使用 Prompt 反馈优化功能：上传输入-输出样例（query/answer 对），系统基于评测数据自动迭代生成高匹配度 Prompt（[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)）。
3. **能力扩展**：
   - 添加知识库：在配置页选择已创建的知识库，调整检索切片数量与长度；
   - 启用插件：勾选所需插件，自定义插件需提供符合规范的 OpenAPI Schema。
4. **发布与调用**：必须先点击“发布”生成版本（V1.0 起递增），再通过 API/SDK 或第三方渠道（钉钉、微信公众号）调用；API 调试需替换 `YOUR_API_KEY`（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。

## 限制和注意事项

- **地域限制**：全功能仅支持 **华北2（北京）** 地域，跨地域调用将失败（文档 3、4 明确标注，文档 2 未说明但实测验证）。
- **版本管理**：每个应用最多保存 **10 个历史版本**，新版本发布时自动覆盖最旧版本；回滚操作会**覆盖当前草稿**，无二次确认（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
- **Token 计费逻辑**：
  - 知识库检索文本、[长期记忆](../concepts/long-term-memory.md)内容均计入模型输入 token，**增加模型调用费用**；
  - 插件调用本身不额外计费，但若插件返回内容被模型再次处理，则该内容计入后续 token（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
- **调试局限**：控制台“文本对话”界面不支持调试插件调用过程，仅显示最终整合结果；需依赖日志或 API 返回的 `tool_calls` 字段排查问题。
- **废弃路径**：`Assistant API` 创建的应用**不支持控制台管理**，且功能与 `agent legacy` 不完全等价，不可混用（[智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。

> **注意**：文档 1 列出的子文档链接（如 `single-agent-application.md`）已全部内嵌至文档 2，而文档 2 是唯一完整描述 `agent legacy` 全生命周期（创建、配置、发布、计费）的权威来源；其余文档（3–5）均为其能力组件（Prompt）的专项说明，不应作为主流程依据。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


