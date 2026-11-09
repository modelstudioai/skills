# agent legacy

`agent legacy` 指百炼平台早期推出的 Flow Agent（旧版）智能体能力，属于 Agent 1.0 架构，以可视化流程编排和 Prompt 驱动为核心，不依赖运行时 Agent 框架（如 ReAct、Plan-and-Execute）。其核心价值在于通过结构化 [Prompt 工程](../concepts/prompt.md)与数据反馈机制提升任务确定性，适用于分类、抽取、格式化等边界清晰的 LLM 应用场景。该能力已逐步被新版 Agent（Agent 2.0+）替代，但仍在部分存量应用和 Prompt 优化链路中使用。

## 支持的模型与功能

- **支持模型**：仅限百炼平台托管的指定大模型，文档明确推荐使用 `qwen-max`（即千问-Max）作为推理模型，用于多轮 Prompt 评测与生成 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)；其他模型未被验证或不保证效果。
- **核心功能**：
  - 可视化 Flow 编排（节点式 Prompt 组合与条件分支）
  - Prompt 模板管理（含系统 Prompt、用户 Prompt 分离）
  - Prompt 反馈优化（Feedback Optimization）：基于用户提供的输入-输出样例（I/O pairs），自动迭代生成更贴合业务预期的 Prompt
  - 样例驱动的评测机制：将样例数据注入 Prompt 上下文，并在独立评测集上评估生成质量，择优输出最终 Prompt

> **注意**：文档 1 中提及的 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md) 属于同一技术代际，但其描述侧重应用部署形态；而文档 2 聚焦 Prompt 层优化能力。二者功能耦合紧密，但文档 1 未说明 Feedback Optimization 的具体参数约束，需以文档 2 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `任务名称` | 字符串 | 是 | 最多 20 个字符，仅用于控制台标识 |
| `推理模型` | 模型 ID | 是 | 当前仅支持 `qwen-max`；其他模型（如 `qwen-plus`）未在任何文档中声明兼容性 |
| `初始 Prompt` | 字符串 | 是 | 最多 6000 字符；应聚焦“任务目标描述”，避免冗余指令或示例（见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md) 中“只需要描述任务目标”的说明） |
| `样例数据` | Excel 文件（.xlsx/.xls）或样例库引用 | 否（但强烈建议提供） | ≤ 20 MB，≤ 100 条；推荐 5–10 条，覆盖全部业务场景类别 |
| `评测数据` | Excel 文件（.xlsx/.xls） | 是 | ≤ 100 条；推荐 ≥ 20 条，数据越多优化效果越稳定 |

## 使用方式

1. 进入控制台：**工具 > 提示词管理** → 切换至 **反馈优化** 标签页  
2. 点击 **新增优化包**，填写上述关键参数  
3. 上传样例数据（可选）与评测数据（必填）  
4. 点击 **开始优化**，系统启动多轮自反思优化流程  
5. 优化完成后，可：  
   - 将生成 Prompt **保存为 Prompt 模板**，供 Flow Agent 或其他应用复用  
   - 直接基于该 Prompt **创建智能体应用**（即 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 所述的单 Agent 应用）

## 限制和注意事项

- **模型锁定**：推理模型强制限定为 `qwen-max`，不支持切换或自定义模型——此为硬性限制，非配置项缺失。  
- **数据规模硬上限**：样例与评测数据均严格限制为最多 100 条，超量文件将被拒绝上传。  
- **Prompt 注入逻辑不可控**：系统自动选取部分样例数据拼接到 Prompt 中，开发者无法指定哪些样例生效或控制插入位置。  
- **无运行时 Agent 行为**：Flow Agent（旧版）不支持 Tool Calling、Memory、Loop 等动态决策能力，纯属静态 Prompt 执行器。  
- **弃用状态提示**：官方文档未明确声明 EOL，但所有新功能（如多步骤 Agent、[函数调用](../concepts/function-calling.md)）均归属新版 Agent 体系；[Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 文档本身未更新维护，最新实践应优先参考新版 Agent 文档。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


