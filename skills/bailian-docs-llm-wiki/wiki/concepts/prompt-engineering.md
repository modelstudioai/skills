# Prompt 工程

Prompt 工程是指通过系统化地设计、优化和管理输入给大语言模型的提示词（Prompt），以获得更准确、更符合预期输出的实践方法。在百炼平台中，Prompt 工程贯穿模型推理、应用构建、模型调优和应用评测等多个环节，是开发者高效利用大模型能力的核心技能。

## 在百炼平台中的应用场景

### 文本生成场景

设计有效的 Prompt 是发挥文本生成模型能力的关键。百炼推荐的核心原则包括：

- **清晰具体**：任务描述越明确、无歧义，模型表现越好
- **使用 Prompt 框架**：按"背景 - 目的 - 风格 - 语气 - 受众 - 输出"六要素结构化组织
- **少样本示例（Few-shot）**：在 Prompt 中提供输入-输出示例，引导模型理解任务格式
- **思维链（Chain-of-Thought）**：对复杂推理任务，引导模型逐步思考再给出结论
- **限制输出格式**：明确指定 JSON、列表、表格等输出形式

### 图像与视频生成场景

文生图和文生视频场景中，Prompt 工程同样至关重要：

- **文生图基础公式**：主体 + 场景 + 风格；进阶可加入镜头语言、氛围词、细节修饰
- **文生视频基础公式**：主体 + 场景 + 运动；图生视频则侧重运动 + 运镜描述
- 通过 `negative_prompt`（反向提示词）排除不希望出现的内容
- 通过 `prompt_extend` 参数开启大模型智能改写，自动优化提示词质量

### 智能体与工作流应用

在智能体应用中，系统提示词（System Prompt）定义了智能体的角色和行为边界，支持嵌入自定义变量。工作流应用中的大模型节点同样依赖精心设计的 Prompt 来驱动每个处理步骤。

### 模型调优的前置手段

百炼推荐在考虑模型微调之前，先尝试通过 Prompt 工程解决问题。当 Prompt 工程和插件调用仍无法满足特定业务需求时，再考虑 SFT、DPO 等调优方式。

### 应用评测中的优化方向

在应用评测的归因分析中，"模型理解有误"类问题的首选优化方向即为优化 Prompt，然后才考虑切换更强模型。

## 百炼 Prompt 工具链

百炼围绕 Prompt 提供了一整套工具链：

| 工具 | 用途 | 适用场景 |
| --- | --- | --- |
| 预置 Prompt 模板 | 开箱即用的场景化模板 | 营销、办公、文案润色等通用场景 |
| 自定义 Prompt 模板 | 业务定制 + 集中管理 + API 拉取 | 金融、医疗等对格式有严格要求的场景 |
| Prompt 自动优化 | 单条 Prompt 一键重写 | 快速改进已有 Prompt |
| Prompt 反馈优化 | 基于样例 + 评测集多轮迭代 | 持续优化复杂业务 Prompt |

## 关键参数与配置

### Prompt 模板调用

通过 `GetPromptTemplate` API 获取模板内容，核心参数：

- `workspaceId`：[业务空间](workspace.md) ID
- `promptTemplateId`：模板 ID

模板中的变量以 `${name}` 占位，调用方将业务数据填入变量后下发模型。推荐通过 API 拉取模板而非在代码中硬编码，便于在控制台修改 Prompt 而不重新部署应用。

### Prompt 框架选型

百炼内置三种 Prompt 工程框架，适用于不同场景：

- **ICIO**（Instruction / Context / Input Data / Output Indicator）：适合数据分析、内容生成、摘要等明确任务
- **CRISPE**（Capacity & Role / Insight / Statement / Personality / Experiment）：适合需要 AI 扮演特定角色的交互，如智能客服、面试模拟
- **RASCEF**（Role / Action / Script / Content / Example / Format）：适合多步骤的复杂业务，如项目规划

### 模型推理相关参数

- `enable_thinking`：开启思考模式，让模型逐步推理后给出结论
- `temperature`：控制输出随机性，值越低越确定
- 结构化输出：通过 Prompt 指定 JSON Schema 获取有效 JSON 返回

## 最佳实践

1. **从模板起步**：优先使用百炼预置模板或基于 Prompt 框架创建，避免从零开始
2. **善用自动优化**：利用控制台的"自动优化"功能对初版 Prompt 进行结构重组和指令具体化
3. **迭代验证**：结合应用评测功能，通过评测集量化 Prompt 修改的效果
4. **版本管理**：通过 Prompt 模板 API 集中管理，实现多人协作和版本控制
5. **先优化 Prompt，后微调模型**：Prompt 工程成本远低于模型微调，应作为首选优化手段

## 关联主题页

- [prompt](../guides/prompt.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)
- [model inference](../guides/model-inference.md)
- [fine tuning](../guides/fine-tuning.md)
- [application evaluation](../guides/application-evaluation.md)


