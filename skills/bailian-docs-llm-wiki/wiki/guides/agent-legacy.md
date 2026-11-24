# agent legacy

`agent legacy` 指百炼平台已归档的旧版智能体能力体系（即 Agent 1.0 / Flow Agent），基于提示词驱动、零代码编排，支持 RAG 知识库接入与插件调用。该体系在新版控制台中已标记为“旧版入口”，其核心能力仍稳定运行并被部分存量应用依赖，但新功能开发与长期维护建议迁移至新一代 Agent 架构。

## 支持的模型与功能

- **模型支持**：仅限旧版控制台可用模型，包括 `千问-Plus`、`千问-Max` 等千问系列模型及用户自定义部署模型；不支持新版 Agent 的多模型协同或动态路由能力。  
- **核心功能**：
  - **知识库（RAG）**：通过[检索增强生成](../concepts/rag.md)，将私有文档内容注入上下文，显著降低幻觉；检索结果占用模型上下文窗口，需主动控制切片长度与召回数量。  
  - **插件（MCP）**：调用平台预置工具（如代码执行、文生图）或自定义插件；所有插件调用超时限制为 **5 秒**，超时即中断且不重试。  
  > **注意**：文档 2 中称插件适用于“网络搜索”，但当前旧版 Flow Agent **不提供内置网络搜索插件**；该能力仅存在于新版 Agent 或需用户自行集成第三方 API —— 此处为过时描述，应以实际控制台可选插件列表为准。

## 关键参数

在模型配置区域可设置以下运行时参数（详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）：

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| 最长回复长度 | 模型生成内容的 token 上限（不含系统提示词与历史输入） | 因模型而异，`千问-Plus` 默认 4096 |
| 携带的上下文轮数 | 输入模型的最大历史对话轮数 | 建议 ≤ 10 轮，避免上下文溢出 |
| 温度系数（temperature） | 控制输出随机性 | `[0, 2)`，0 表示确定性输出 |
| 推理模式 | 启用后增强多步推理能力 | 仅部分模型支持，不可在不兼容模型上启用 |

> **注意**：`携带的上下文轮数` 实际生效值受模型最大上下文长度与知识库/记忆体注入内容共同制约；若总输入 token 超限，系统将自动截断最早轮次，**不会报错提示**。

## 使用方式

### 创建与配置
1. 通过新版控制台底部的 **“旧版 Agent 创建入口”** 跳转至旧版控制台，进入 [应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center) 页面；  
2. 选择 **智能体应用** → **立即创建**；  
3. 在配置页选择模型，并可直接复用 Prompt 模板：点击预置或自定义模板卡片的 `···` → **创建应用**，模板内容将自动填充至系统提示词框（参见 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）。

### Prompt 工程支持
- **模板化管理**：支持预置模板（开箱即用）与自定义模板（含 ICIO/CRISPE/RASCEF 框架），全部在 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 页面统一维护；  
- **自动优化**：通过 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)，上传输入-输出样例对（query/answer），系统基于评测数据集自动迭代生成高匹配度 Prompt。

### 发布与调用
- 应用必须 **发布后** 才能通过 API 调用；发布版本最多保留 10 个，超出则自动覆盖最旧版本；  
- API 调用需使用独立的 `API KEY`（非百炼通用 AccessKey），密钥在 **发布渠道 → API** 页签获取；  
- 不支持通过 Assistant API 创建的智能体应用在旧版控制台管理（参见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。

## 限制和注意事项

- **地域限制**：Prompt 模板功能（含自定义模板、反馈优化）**仅支持华北2（北京）地域**，其他地域调用将返回错误（见 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 和 [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)）；  
- **知识库计费**：检索返回的文本计入模型输入 token，**增加模型调用费用**；[长期记忆](../concepts/long-term-memory.md)体内容虽不单独计费，但同样占用输入 token；  
- **插件超时**：所有插件调用硬性超时为 5 秒，无重试机制，超时响应为空或默认 fallback；  
- **控制台隔离**：旧版 Agent 应用无法在新版控制台编辑或监控；反之，新版 Agent 创建的应用无法在旧版控制台查看；  
- **模型兼容性**：`千问-Max` 是唯一明确推荐用于 Prompt 反馈优化的推理模型（见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)），其他模型可能因输出格式不稳定导致优化失败。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


