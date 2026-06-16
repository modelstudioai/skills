# Prompt 工程

Prompt 工程是指通过系统化地设计、优化和管理输入给大语言模型的提示词（Prompt），以引导模型产出高质量、符合预期的输出的技术实践。在百炼平台中，Prompt 工程贯穿应用构建、模型调优和内容生成的全流程，是提升 AI 应用效果的首选低成本手段。

## 在百炼平台中的应用场景

### 智能体与应用构建

在构建智能体应用时，System Prompt 用于定义 AI 的角色和行为边界。无论是零代码的智能体应用还是工作流应用，Prompt 设计都直接决定了模型的回答质量和任务执行效果。新版智能体（Agent 2.0）支持在系统提示词中嵌入自定义变量，实现动态化的 Prompt 管理。

### 模型调优前的基线优化

在考虑模型微调（SFT/DPO）之前，建议优先通过 Prompt 工程优化模型表现。只有当 Prompt 工程无法满足特定行业或业务场景的需求时，才建议进入模型调优阶段。这一策略可以显著降低开发成本和迭代周期。

### 多模态内容生成

百炼平台为不同模态提供了专门的 Prompt 编写指南：

- **文生文**：关注任务描述的完整性、上下文信息的充分性以及输出格式的明确性。
- **文生图**：通过 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）控制图像生成，遵循"主体 + 场景 + 风格"的基础公式或更进阶的多维度公式。
- **视频生成**：遵循"主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介"的结构，部分模型支持通过关键词触发运镜控制和动态控制。

## Prompt 模板管理

百炼提供完整的 Prompt 模板管理体系：

- **预置模板**：覆盖营销、办公、文案润色等通用场景，开箱即用。
- **自定义模板**：通过控制台或 `CreatePromptTemplate` API 创建，支持变量占位（`${name}` 格式），适合对输出格式有严格要求的业务场景。
- **模板调用**：推荐通过 `GetPromptTemplate` 接口获取模板内容，而非在代码中硬编码 Prompt，便于在控制台侧修改而无需重新部署应用。

## Prompt 优化工具

百炼平台提供多层次的 Prompt 优化能力：

| 工具 | 机制 | 适用场景 |
|------|------|----------|
| 自动优化 | 大模型对输入 Prompt 做结构重组和指令具体化 | 单条 Prompt 快速改进 |
| 样例库（Few-shot） | 检索高质量问答对注入上下文 | 智能客服、格式化输出 |
| 反馈优化 | 基于样例和评测集多轮迭代 | 持续提升 Prompt 效果 |

> 官方推荐将样例库数据迁移到 RAG 表格库，新项目优先考虑反馈优化或 RAG 方案。

## Prompt 设计框架

百炼平台内置三种结构化的 Prompt 编写框架，可在创建自定义模板时选用：

- **ICIO**（Instruction / Context / Input Data / Output Indicator）：适合数据分析、内容生成、摘要等明确任务。
- **CRISPE**（Capacity & Role / Insight / Statement / Personality / Experiment）：适合需要角色扮演的交互场景，如智能客服、面试模拟。
- **RASCEF**（Role / Action / Script / Content / Example / Format）：适合多步骤的复杂业务流程。

## 关键参数

| 参数 | 说明 |
|------|------|
| `workspaceId` | [业务空间](workspace.md) ID，调用模板接口时必传 |
| `promptTemplateId` | 模板 ID，从控制台模板卡片获取 |
| `temperature` | 控制输出的随机性，值越低输出越确定 |
| `enable_thinking` | 开启思考模式，适用于需要逐步推理的场景 |
| `prompt_extend` | 文生图场景下启用大模型智能改写（默认启用） |

## 最佳实践

1. **先优化 Prompt，后考虑微调**：Prompt 工程是成本最低、迭代最快的优化手段。
2. **使用模板管理而非硬编码**：通过 API 拉取模板，实现 Prompt 与代码解耦。
3. **选择合适的设计框架**：根据任务复杂度选用 ICIO、CRISPE 或 RASCEF 框架。
4. **善用自动优化**：对初始 Prompt 进行结构重组和指令具体化。
5. **结合 RAG 增强**：对于需要领域知识的场景，将 Prompt 与知识库检索结合使用。

## 关联主题页

- [prompt](../guides/prompt.md)
- [fine tuning](../guides/fine-tuning.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)
- [model inference](../guides/model-inference.md)
- [start using](../guides/start-using.md)



