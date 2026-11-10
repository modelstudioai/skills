# agent legacy

`agent legacy` 指百炼平台早期推出的 Flow Agent（旧版）智能体能力，属于 Agent 1.0 架构，以可视化流程编排和 Prompt 驱动为核心，不依赖运行时 Agent 框架（如 ReAct、Plan-and-Execute）。其核心价值在于通过结构化 Prompt 工程与数据反馈机制提升大模型在垂直任务中的确定性输出，适用于规则明确、输出格式强约束的场景。该能力现已归入历史维护路径，新项目推荐使用 [智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md) 或新一代 Agent SDK。

## 支持的模型与功能

- **支持模型**：仅限百炼平台已接入的 LLM（如 Qwen-Max、Qwen-Plus），不支持用户自托管模型或外部 API 模型。
- **核心功能**：
  - 可视化流程节点编排（条件分支、循环、变量传递等）；
  - Prompt 模板管理与版本控制；
  - **Prompt 反馈优化**：基于输入-输出样例自动迭代生成更优 Prompt，详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)；
  - 支持将优化结果直接导出为 Prompt 模板或一键创建智能体应用。

> **注意**：文档 1 中列出的 [智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md) 实际为独立于 Flow Agent 的新架构，二者无继承关系；Flow Agent（旧版）并非 Agent 1.0 的实现，该链接存在误导性归类，应以 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 正文描述为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `推理模型` | string | 是 | 用于多轮评测与优化的模型 ID，**仅支持千问系列（如 `qwen-max`）**；其他模型可能触发失败或静默降级。 |
| `初始 Prompt` | string | 是 | 最多 6000 字符；只需描述任务目标（如“对汽车论坛文章分类为六类之一，并严格按 JSON 格式输出”），**不可包含样例数据**（系统将自动注入）。 |
| `样例数据` | file / list | 否（但强烈建议） | .xlsx/.xls，≤20 MB，≤100 条；需覆盖全部业务场景，**建议 5–10 条，每类至少 1 条**。详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。 |
| `评测数据` | file / list | 是 | .xlsx/.xls，≤100 条；用于自动化评估候选 Prompt 效果，**建议 ≥20 条，越多越准**。 |

## 使用方式

1. 进入控制台 → **工具** > **提示词管理** → 切换至 **反馈优化** 标签页；
2. 点击 **新增优化包**，填写表单（含任务名称、推理模型、初始 Prompt）；
3. （可选）上传样例数据（直接上传或从样例库选择）；
4. **必填**上传评测数据；
5. 点击 **开始优化**，等待任务完成（通常 2–10 分钟）；
6. 查看优化报告，可：
   - 下载最终 Prompt 文本；
   - 点击 **保存为 Prompt 模板**，供后续复用；
   - 点击 **创建智能体应用**，跳转至应用配置页（此时仍基于 Flow Agent 运行时）。

## 限制和注意事项

- **无运行时 Agent 能力**：不支持[工具调用](../concepts/tool-calling.md)（Tool Calling）、记忆（Memory）、多步规划（Planning）等动态行为，所有逻辑必须静态编码进 Prompt 或流程节点。
- **样例与评测数据隔离**：样例数据仅用于 Prompt 构建（few-shot 注入），**不参与评测**；评测数据仅用于打分排序，**不参与 Prompt 构建** —— 此设计避免过拟合，但要求两类数据语义分布一致。
- **最大并发与配额**：单账号最多同时运行 3 个优化任务；每个任务最多处理 100 条样例 + 100 条评测数据。
- **输出格式强依赖 Prompt 约束**：若初始 Prompt 未明确指定 JSON Schema 或分隔符，优化后仍可能产生非结构化输出。
- **弃用提示**：该能力已停止新增功能开发，[Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 文档中标注的关联链接（如 Prompt 模板概述）部分已迁移至新版 Prompt 管理体系，旧链接可能失效或内容陈旧。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


