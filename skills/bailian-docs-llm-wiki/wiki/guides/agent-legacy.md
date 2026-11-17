# agent legacy

`agent legacy` 指百炼平台中已归档的旧版 Flow Agent（Agent 1.0）技术栈，包含基于固定 [Prompt 工程](../concepts/prompt-engineering.md)流程构建智能体的能力，不支持运行时动态规划（如 Tool Calling、多跳推理等现代 Agent 范式）。其核心价值在于通过数据驱动的 Prompt 反馈优化提升确定性任务（如分类、结构化提取）的输出稳定性，适用于对可控性要求高、场景边界清晰的生产环境。该能力现已被 `Agent 2.0`（即新版 Flow Agent）替代，但历史应用与优化包仍可维护。

## 支持的模型与功能

- **支持模型**：仅限百炼平台已接入的**同步推理模型**，包括 `qwen-max`、`qwen-plus`、`qwen-turbo`；不支持异步模型或自定义模型接入。  
- **核心功能**：
  - Prompt 反馈优化（Prompt Feedback Optimization）：基于用户提供的样例数据（input-output pairs）和评测数据，自动迭代生成并筛选最优 Prompt；
  - Prompt 模板管理：支持将优化结果保存为可复用的 Prompt 模板；
  - 智能体应用创建：可基于优化后的 Prompt 直接发布为单轮调用型智能体应用（即 [智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md)）。

> **注意**：文档 2 中列出的 `[Prompt反馈优化](raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)` 是唯一权威入口，而文档 1 实际是该功能的完整操作指南——二者内容一致，但文档 1 提供了详细参数说明与案例，应以 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `推理模型` | 字符串 | 是 | 用于执行多轮评测的模型 ID，**仅支持 `qwen-max`（推荐）、`qwen-plus`、`qwen-turbo`**；其他模型将导致优化失败。 |
| `初始 Prompt` | 字符串 | 是 | 最多 6000 字符；仅需描述任务目标（如“请将以下汽车文章分类为六类之一，并严格按 JSON 格式输出”），**不可包含样例数据**（系统将自动注入）。 |
| `样例数据` | 文件（.xlsx/.xls）或样例库引用 | 是 | ≤ 100 条，≤ 20 MB；建议 5–10 条，覆盖全部类别；每条需含 `query`（输入）与 `answer`（期望输出）两列。 |
| `评测数据` | 文件（.xlsx/.xls） | 是 | ≤ 100 条；建议 ≥ 20 条；格式同上；用于自动化评估各候选 Prompt 的准确率，决定最终输出。 |

## 使用方式

1. 进入控制台 → 左侧导航栏选择 **工具 > 提示词管理**，打开 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 页面；
2. 切换至 **反馈优化** 分类，点击 **新增优化包**；
3. 按表单填写：选择推理模型 → 输入初始 Prompt → 上传/选择样例数据 → 上传评测数据；
4. 点击 **开始优化**，等待任务完成（通常 2–10 分钟，取决于数据量与模型负载）；
5. 优化完成后，可：
   - 点击 **保存为 Prompt 模板**，供后续应用复用；
   - 或直接点击 **创建智能体应用**，生成一个基于该 Prompt 的 API 可调用服务。

该流程完整说明见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)。

## 限制和注意事项

- **数据规模硬限制**：样例数据与评测数据均不得超过 100 条，单文件 ≤ 20 MB；超出将被前端拦截。
- **无运行时干预能力**：`agent legacy` 不支持[函数调用](../concepts/function-calling.md)、外部工具集成、状态记忆或多步决策链；所有逻辑必须编码在 Prompt 中。
- **模型绑定严格**：优化过程强制使用指定 `推理模型` 执行全部评测，**不可混用模型**；若在 `qwen-turbo` 上优化出的 Prompt，直接部署到 `qwen-max` 应用中可能因 token 行为差异导致效果下降。
- **模板复用风险**：保存的 Prompt 模板默认继承优化时所选模型的上下文长度与行为特征，跨模型复用前需人工验证输出格式一致性。
- **弃用状态**：该能力已标记为 Legacy，新项目应使用 [Flow Agent（新版）](raw/application-user-guide/agent/flow-agent.md)；存量应用仍可维护，但不再接收功能更新。相关背景与迁移路径详见 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)。

## 来源文档

- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)
- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)


