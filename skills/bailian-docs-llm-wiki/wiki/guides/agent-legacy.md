# agent legacy

`agent legacy` 指百炼平台早期推出的智能体能力体系（即 Agent 1.0 / Flow Agent），以零代码方式支持模型调用知识库（RAG）和插件，通过提示词驱动任务规划与执行。该体系面向快速构建业务型智能体应用，适用于客服助手、营销文案生成、垂直领域问答等场景，其核心能力在旧版控制台中完整支持，新版控制台仅提供跳转入口。当前已逐步被更灵活的 `agent v2`（基于 MCP 协议与结构化工具调用）所演进，但大量存量应用仍在稳定运行。

## 支持的模型与功能

- **模型支持**：主要支持千问系列模型（如 `千问-Plus`、`千问-Max`），也支持用户自定义部署的模型。模型作为推理与决策核心，需在旧版控制台[应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)中显式选择。
- **核心扩展能力**：
  - **知识库（RAG）**：连接私有文档，检索结果注入 Prompt，显著降低幻觉，提升垂直领域回答准确率。详情见 [创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
  - **插件（Plugin）**：调用预置工具（如代码执行、天气查询、图像生成）或自定义插件，完成模型无法原生执行的操作。自定义插件超时限制为 5 秒。
  - **Prompt 模板**：支持预置模板（如营销文案、摘要抽取）与自定义模板（含 ICIO/CRISPE/RASCEF 工程框架），实现提示词结构化、可复用、易迭代。该能力统一在 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 页面管理。

> **注意**：文档 3 和文档 4 均强调“本文档仅适用于华北2（北京）地域”，但文档 1 的快速开始流程未限定地域。实际使用中，若在非北京地域调用 Flow Agent 相关 API（如 `ListPromptTemplates`），可能返回空列表或报错，需确认 workspace 所属地域一致性。

## 关键参数

在模型配置区域可调整以下运行时参数（单击模型下拉框右侧设置图标进入）：

- **最长回复长度**：模型生成内容的 token 上限（不含系统提示词与历史上下文），具体上限依模型而定。
- **携带的上下文轮数**：输入模型的最大历史对话轮数，影响多轮对话连贯性；轮数越多，Token 消耗越高。
- **温度系数（temperature）**：取值范围 `[0, 2)`，控制输出随机性；`0` 表示确定性输出，`1.0` 为默认平衡点。
- **推理模式**：仅对明确支持该模式的模型生效，启用后可增强复杂逻辑推理能力。

此外，Prompt 模板相关参数（如变量填充、评测数据量）见 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 与 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。

## 使用方式

1. **创建应用**：  
   访问旧版控制台 [应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)，选择 **智能体应用** → **立即创建**；或在新版控制台点击 **旧版 Agent 创建入口** 跳转。  
   > **注意**：文档 1 明确指出 Agent 1.0 仅旧版控制台支持，且新版控制台顶部提供“前往新版”入口——说明该能力已进入维护状态，新项目应优先评估 `agent v2`。

2. **配置能力**：  
   - 在应用配置页选择模型并设置上述关键参数；  
   - 编写或导入系统提示词（支持直接粘贴、使用预置模板、或基于 Prompt 工程框架创建）；  
   - 添加知识库（需提前创建并关联）或启用插件（官方插件开箱即用，自定义插件需配置 endpoint 与认证）。

3. **调试与发布**：  
   - 在文本对话界面输入测试语句（支持文件上传），观察响应及 Token 统计；  
   - 点击右上角 **发布** 完成版本上线，版本 ID 从 `V1.0` 开始递增，最多保留 10 个历史版本；  
   - 发布后可通过 API/SDK 调用，或集成至钉钉、微信公众号等渠道。

4. **Prompt 工程实践**：  
   - 使用 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 管理模板生命周期（创建、复制、删除）；  
   - 对高精度需求场景，采用 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)，通过上传样例与评测数据集驱动自动化优化。

## 限制和注意事项

- **地域限制**：Prompt 模板与反馈优化功能（文档 3、4、5）明确限定于 **华北2（北京）地域**，跨地域 workspace 调用将失败。
- **控制台依赖**：Agent 1.0 应用 **仅支持旧版控制台管理**；通过 Assistant API 创建的应用虽功能相似，但不支持控制台配置与版本管理（见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
- **Token 消耗透明性**：知识库检索内容、[长期记忆](../concepts/long-term-memory.md)体内容均计入模型输入 Token，但后者暂不计费；开发者需主动监控上下文长度，避免因超限导致截断或报错。
- **插件超时**：所有自定义插件调用硬性超时为 **5 秒**，超时后智能体将终止调用并可能触发 fallback 逻辑。
- **模板字符上限**：控制台中 Prompt 模板内容最大支持 **6144 字符**，超出需精简或拆分逻辑。
- **演进状态**：该体系已标记为 `legacy`，新项目建议评估 `agent v2`（基于标准 MCP 协议），其在工具发现、错误恢复、流式响应等方面具备更强工程能力。

## 来源文档

- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


