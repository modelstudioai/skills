# Prompt 工程

Prompt 工程是指系统性设计、测试、优化和管理大语言模型输入指令（Prompt）的方法论与实践体系，其目标是提升模型输出的准确性、一致性、可控性与任务完成率。它不是一次性编写文本，而是涵盖模板化、结构化、可评估、可迭代的全生命周期管理过程。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，Prompt 工程已深度融入三大核心应用形态与评测闭环，具体体现为：

- **智能体（Agent）与工作流（Workflow）中**：Prompt 是驱动模型行为的“系统提示词”（System Prompt），直接决定角色设定、任务边界、输出格式及工具调用逻辑。Agent 2.0 将 Prompt 与知识库、MCP 工具统一纳入规划链路，其质量直接影响“思考→执行→反思”的闭环效果；工作流中的大模型节点也依赖高质量 Prompt 实现意图分类、参数提取等确定性子任务。

- **Prompt 模板体系中**：支持基于 ICIO、CRISPE、RASCEF 等工程框架创建结构化模板（如 `Role-Action-Steps-Format-Examples`），预置模板覆盖营销文案、摘要抽取、风格改写等高频场景；所有模板均需在华北2（北京）地域部署，单模板内容上限 6144 字符。

- **[agenteval](../guides/agenteval.md) 评测优化闭环中**：Prompt 工程进入量化迭代阶段——通过观测 Trace 捕获真实 Prompt 执行路径，利用评测集（≥20 条样本）和人工反馈（5–10 条优质 I/O 对）驱动多轮自动优化；支持多版本对比调试，但优化结果仅更新草稿，需手动验证后发布。

- **RAG 增强场景中**：Prompt 不再孤立存在，而是与 RAG 表格库协同工作。系统提示词需明确指示模型“仅基于以下检索结果回答”，并通过 `has_thoughts=true` 参数启用调试模式，查看 `thoughts` 字段中 RAG 召回片段是否准确、相关。

> ⚠️ 注意：Prompt 样例库（few-shot 注入）功能已正式停用，所有新项目必须迁移至 RAG 表格库实现知识约束，不可再依赖历史样例库能力。

## 关键参数和配置

| 参数 | 说明 | 使用场景 |
|------|------|----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 相关 API（如 `GetPromptTemplate`）的必需参数 | 模板拉取、API 调用 |
| `promptTemplateId` | 模板唯一标识符，控制台模板卡片上直接获取 | 模板引用与变量填充 |
| `variables` | 模板中定义的占位符列表（如 `["topic", "platform"]`），由 `GetPromptTemplate` 接口返回 | 运行时动态注入上下文 |
| `has_thoughts=true` | API 请求参数，启用后响应含 `thoughts` 字段，用于调试 RAG 召回逻辑 | RAG 场景下必开，验证知识匹配质量 |
| `enable_thinking` / `reasoning_effort` | 控制模型是否输出推理过程（如 `max`/`high`/`low`），影响输出可控性与 [Token](token.md) 消耗 | Agent、工作流、三方模型通用 |

## 面向开发者，简洁实用

- ✅ **起步建议**：新项目优先使用预置模板 + `GetPromptTemplate` API 获取结构化内容，避免手写硬编码；变量替换务必校验 `variables` 字段，防止占位符残留。
- ✅ **调试必做**：调用含 RAG 的接口时，始终添加 `has_thoughts=true`，检查 `thoughts.retrieved_chunks` 是否召回预期知识片段。
- ✅ **优化路径**：  
  - 快速迭代 → 用「Prompt 自动优化」（免费、无数据留存）；  
  - 高精度需求 → 进入 `agenteval → 应用优化`，上传 5–10 条优质 I/O + ≥20 条评测样本，启动定向优化。
- ✅ **避坑提醒**：  
  - 所有 Prompt 模板功能仅支持 **华北2（北京）地域**，跨地域调用将失败；  
  - 图片/视频生成需谨慎设置 `negative_prompt`，避免触发内容安全策略；  
  - `incremental_output=True` 启用增量[流式输出](streaming-output.md)（推荐），但需确认 SDK 版本兼容性（部分旧版对应 `delta=True`）。

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


