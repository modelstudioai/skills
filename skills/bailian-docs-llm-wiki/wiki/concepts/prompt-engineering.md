# 提示工程

提示工程（Prompt Engineering）是指通过系统性设计、结构化表达与迭代优化输入指令（Prompt），以精准引导大语言模型生成符合预期的高质量输出的技术实践。它既是连接业务需求与模型能力的关键桥梁，也是百炼平台中实现可控、可复用、可评测 AI 行为的核心方法论。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，“提示工程”并非仅指手动编写一段文本，而是一套覆盖**设计—管理—优化—验证**全生命周期的工程化能力，深度集成于多个核心模块：

- **Prompt 模板**：提供开箱即用的预置模板（如“会议纪要生成”“技术文档摘要”）和自定义模板能力，支持变量插值（`${topic}`）、版本控制与跨应用复用，是提示工程的标准化载体。
- **Prompt 自动优化**：无需人工经验，平台自动对原始 Prompt 进行角色设定增强、指令澄清、安全边界注入与结构重组，适用于快速启动或非专业开发者。
- **Prompt 反馈优化**：基于真实用户 query/answer 样例与评测数据集，驱动多轮自动化评估与迭代优化，显著提升特定任务（如金融问答、客服话术）的准确率与一致性。
- **Agenteval 优化闭环**：在可观测链路中捕获实际调用中的 Prompt 执行轨迹，支持多版本对比调试与人工反馈驱动的 Prompt 重写，实现“观测 → 评测 → 优化”闭环。
- **多模态生成场景**：在文生图（万相）、文生视频（Vidu/万相3.0）等场景中，提示工程体现为结构化正向/负向提示词（`prompt`/`negative_prompt`）、分镜语法、风格关键词等精细化控制手段。

> ⚠️ 注意：原 Prompt 样例库功能已下线，官方明确要求迁移至 RAG 表格库；当前所有提示工程实践均应围绕模板 + RAG + 自动/反馈优化 + Agenteval 四类能力构建。

## 关键参数和配置

| 参数 | 说明 | 使用位置 | 备注 |
|------|------|----------|------|
| `promptTemplateId` | 模板唯一标识符 | API 调用（`GetPromptTemplate`、`InvokeApplication`） | 必填；用于加载模板内容并执行变量替换 |
| `variables` | 模板中声明的变量名数组（如 `["query", "context"]`） | `GetPromptTemplate` 响应体 | 由平台返回，不可手动指定；运行时需按此列表填充值 |
| `has_thoughts=true` | 启用 RAG 检索过程日志输出（含 `thoughts` 字段） | `InvokeApplication` 请求参数 | 仅 DashScope API 支持，用于调试检索逻辑 |
| `recall_count` | RAG 表格库召回片段数量 | 应用配置页或 `rag_options` 中 | 默认 5，上限 10；影响 Prompt 上下文长度与 Token 成本 |
| `prompt_extend: true` | 启用大模型智能改写提示词（文生图 V2+） | 文生图 API 请求体 | 提升提示词表达力与生成质量，推荐开启 |

## 面向开发者，简洁实用

- ✅ **起步建议**：优先使用控制台「提示词」页面的预置模板创建应用，再通过「反馈优化」上传 10–20 条高质量样例快速收敛效果。
- ✅ **生产推荐**：将 Prompt 模板与 RAG 表格库绑定，在 `InvokeApplication` 中启用 `has_thoughts=true` 观察检索过程，结合 Agenteval 导出 Span 数据做根因分析。
- ✅ **避坑提醒**：
  - 所有 Prompt 功能**仅支持华北2（北京）地域**，跨地域调用将失败；
  - 单模板内容上限 6144 字符，超长 Prompt 建议拆分为 RAG 片段而非硬编码；
  - `stream=true` 与 `incremental_output=true` 需同时设置才生效；
  - Prompt 自动优化不存储用户数据，但 RAG 检索内容计入输入 Token，影响计费。

提示工程的本质是“用确定性约束不确定性”。在百炼平台，它已从手工技巧升级为可配置、可追踪、可度量的基础设施能力——善用模板、RAG、反馈优化与 Agenteval，即可让大模型真正成为你业务逻辑的可靠延伸。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application call](../api/application-call.md)
- [agenteval](../guides/agenteval.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


