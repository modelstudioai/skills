# agent legacy

`agent legacy` 指百炼平台早期推出的 Flow Agent（旧版）智能体能力，属于 Agent 1.0 架构，以可视化流程编排和 Prompt 驱动为核心，不依赖运行时 Agent 框架（如 ReAct、Plan-and-Execute）。其核心价值在于通过结构化 [Prompt 工程](../concepts/prompt-engineering.md)与数据反馈机制提升任务确定性，适用于分类、抽取、格式化等边界清晰的 LLM 应用场景。该能力已逐步被新版 Agent（基于大模型自主推理与工具调用）替代，但仍在部分存量应用中维护。

## 支持的模型与功能

- **支持模型**：仅限百炼平台托管的指定大模型，文档明确推荐使用 `qwen-max`（即千问-Max）作为推理模型，用于 Prompt 反馈优化中的多轮评测与生成 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。
- **核心功能**：
  - 可视化 Flow 编排（节点式 Prompt 组合与条件分支）
  - Prompt 模板管理与版本控制
  - **Prompt 反馈优化**：基于用户提供的输入-输出样例（SFT 数据），自动迭代生成更贴合业务预期的 Prompt，属数据驱动型 [Prompt 工程](../concepts/prompt-engineering.md)方案 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。
  > **注意**：文档 1 中提及的“[智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md)”链接路径未加 `../../raw/` 前缀，且该页面实际归属新版单智能体应用体系，与 `agent legacy` 的 Flow Agent 架构无技术继承关系；此处引用仅作上下文定位，不可视为功能兼容依据。

## 关键参数

在 Prompt 反馈优化任务中，以下参数直接影响优化效果：

| 参数 | 说明 | 约束 |
|------|------|------|
| **推理模型** | 用于执行候选 Prompt 推理并生成评测结果的模型 | 必填；仅支持平台预置模型，官方强推 `qwen-max` [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md) |
| **初始 Prompt** | 描述任务目标的原始提示词 | 必填；≤6000 字符；应聚焦任务定义，避免冗余约束 |
| **样例数据** | 用户标注的 query-answer 对，用于注入 Prompt 并对齐行为 | 可选上传；建议 5–10 条，覆盖全部类别/场景；格式为 `.xlsx/.xls`，≤20 MB，≤100 条 |
| **评测数据** | 用于自动化评估各候选 Prompt 效果的测试集 | 必填；≥20 条为佳，上限 100 条；质量直接影响最终 Prompt 选择准确性 |

## 使用方式

1. 进入控制台：**工具 > 提示词管理** → 切换至 **反馈优化** 标签页；
2. 点击 **新增优化包**，按表单填写上述关键参数；
3. 提交后系统启动多轮优化流程：将样例数据注入 Prompt → 在评测数据上批量推理 → 自动评估 → 反思迭代 → 输出最优 Prompt；
4. 优化完成后，可：
   - 将结果 **保存为 Prompt 模板**，供 Flow Agent 应用直接调用；
   - 或点击 **创建智能体应用**，一键生成基于该 Prompt 的旧版单 Agent 应用。

## 限制和注意事项

- **模型锁定**：`agent legacy` 不支持用户自定义模型或 BYOM（Bring Your Own Model），所有推理均强制走百炼托管模型通道；
- **数据规模硬限**：样例与评测数据均严格限制为 ≤100 条，超出部分将被截断，无法分批提交；
- **无运行时工具调用**：Flow Agent（旧版）不支持[函数调用](../concepts/function-calling.md)（Function Calling）、外部 API 集成或动态工具检索，纯 Prompt 驱动；
- **Prompt 注入逻辑固定**：系统自动选取样例子集注入 Prompt，开发者无法控制注入位置、顺序或模板语法，存在黑盒性；
- **弃用状态明确**：该能力已归类为 Legacy，新项目应优先选用新版 Agent 框架；存量应用迁移需重写 Flow 逻辑为 Tool-Calling + LLM Orchestration 形式。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


