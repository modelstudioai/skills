# agent legacy

`agent legacy` 指百炼平台早期推出的 Flow Agent（旧版）智能体能力体系，基于固定 Prompt 工程范式构建，不支持运行时动态规划与[工具调用](../concepts/tool-calling.md)链自动编排。其核心价值在于通过结构化样例驱动的 Prompt 反馈优化，提升大模型在垂直任务上的输出一致性与准确性。该体系已逐步被新一代 Agent 2.0（支持 LLM-based planning、function calling、stateful execution）所替代，但仍在部分存量应用和 Prompt 精调场景中使用。

## 支持的模型与功能

- **支持模型**：仅限百炼平台托管的指定推理模型，官方明确推荐使用 `qwen-max`（见[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)），其他模型（如 qwen-plus、qwen-turbo）未经过完整验证，效果不可保障。
- **核心功能**：
  - 单轮静态 Prompt 执行（无多步推理、无[工具调用](../concepts/tool-calling.md)）
  - Prompt 反馈优化（Feedback-based Prompt Optimization）：以用户提供的输入-输出样例为监督信号，自动生成更贴合业务场景的 Prompt
  - Prompt 模板管理与复用（通过[提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage)界面）

> **注意**：文档 1 中列出的链接 `[智能体应用（Agent 1.0）](../llm-application/single-agent-application.md)` 指向的是通用单智能体应用入口，但该入口实际已默认路由至新版 Agent 2.0 控制台；而 `agent legacy` 功能仅在 Flow Agent 旧版控制台路径（`/flow-agent/...`）下可用，二者模型底座与能力边界不兼容。请勿将 `agent legacy` 的 Prompt 模板直接用于新版智能体应用。

## 关键参数

在创建 Prompt 反馈优化任务时，以下参数必须显式配置：

| 参数 | 要求 | 说明 |
|------|------|------|
| **推理模型** | 必填 | 仅支持 `qwen-max`；其他模型可能导致优化失败或评估失真（见[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)） |
| **初始 Prompt** | 必填，≤ 6000 字符 | 仅需描述任务目标（如分类意图、输出格式约束），**不可包含样例**——样例由系统自动注入 |
| **样例数据** | 可选，但强烈建议提供 | 格式：`.xlsx`/`.xls`，≤ 20 MB，≤ 100 条；建议 5–10 条，覆盖全部类别（见[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)） |
| **评测数据** | 必填，≤ 100 条 | 用于自动化评估候选 Prompt 效果；建议 ≥ 20 条，越多越准 |

## 使用方式

1. 进入控制台：左侧导航栏 → **工具** → **提示词管理** → 切换至 **反馈优化** 标签页  
2. 点击 **新增优化包**，填写上述关键参数  
3. 提交后系统启动多轮优化流程（通常耗时 2–10 分钟，取决于评测数据量）  
4. 优化完成后，可：
   - 点击 **保存为 Prompt 模板**，供后续手动调用或调试  
   - 点击 **创建智能体应用**，生成基于该 Prompt 的 Flow Agent（旧版）应用实例  

> **注意**：Flow Agent（旧版）应用不支持 API 调用中的 `tools` 字段或 `messages` 中的 `tool_calls`，仅接受标准 `messages: [{role: "user", content: "..."}]` 输入。详见 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)。

## 限制和注意事项

- **无运行时[工具调用](../concepts/tool-calling.md)能力**：无法解析并执行[函数调用](../concepts/function-calling.md)请求，所有逻辑必须硬编码于 Prompt 中  
- **样例注入机制固定**：系统自动选取部分样例插入 Prompt，用户无法控制插入位置或方式；因此初始 Prompt 中**严禁重复包含样例内容**，否则导致 token 冗余与逻辑冲突  
- **评测强依赖模型稳定性**：因全程使用 `qwen-max` 推理，若该模型版本升级导致行为偏移，历史优化包效果可能退化，需重新训练  
- **数据安全边界**：上传的样例与评测数据仅用于本次优化任务，不会进入模型训练语料，但会临时缓存在百炼服务端（保留 ≤ 7 天）  
- **不兼容新版 Agent SDK**：`agent legacy` 应用的 `app_id` 无法被 `@alibaba/bailian-agent-sdk@v2+` 加载；如需迁移，须重写为 Agent 2.0 应用并重构 Prompt 为 system message + tool schema 形式

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


