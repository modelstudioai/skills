# Prompt 工程

Prompt 工程是指通过系统化地设计、优化和管理提示词（Prompt），引导大语言模型产出更准确、更符合预期结果的技术实践。在阿里云百炼平台中，Prompt 工程覆盖了从模板管理、自动优化到少样本召回的完整工具链。

## 核心能力

百炼平台围绕 Prompt 工程提供五项核心能力：

| 能力 | 用途 | 适用阶段 |
|------|------|---------|
| 预置 Prompt 模板 | 开箱即用的场景化模板（营销、办公、文案润色等） | 快速启动 |
| 自定义 Prompt 模板 | 业务定制 + 集中管理 + API 拉取 | 生产集成 |
| Prompt 自动优化 | 单条 Prompt 一键结构重组与指令具体化 | 迭代改进 |
| Prompt 样例库（Few-shot） | 检索高质量问答对注入上下文 | 输出对齐 |
| Prompt 反馈优化 | 基于样例 + 评测集多轮迭代 | 持续调优 |

## 不同模态的 Prompt 设计

### 文生文

核心原则为清晰、具体、无歧义。推荐使用 Prompt 框架组织内容，包含背景、目的、风格、语气、受众和输出格式六个要素。百炼控制台提供 Prompt 一键优化工具可自动扩写和细化。

### 文生图

万相系列模型支持 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）两个参数。编写公式分两级：

- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

### 文生视频 / 图生视频

视频模型的 Prompt 在图文基础上增加运动描述维度，并支持多镜头分镜、声音描述、参考素材指代等高级用法。

## Prompt 模板管理

百炼提供基于 Prompt 框架的结构化模板创建方式，内置三种框架：

- **ICIO**（Instruction / Context / Input Data / Output Indicator）：适合数据分析、内容生成、摘要等明确任务。
- **CRISPE**（Capacity & Role / Insight / Statement / Personality / Experiment）：适合需要 AI 扮演特定角色的交互场景。
- **RASCEF**（Role / Action / Script / Content / Example / Format）：适合多步骤的复杂业务流程。

模板通过 `GetPromptTemplate` API 获取，支持变量占位（`${name}` 格式），实现 Prompt 与业务逻辑解耦。推荐通过 API 拉取模板而非在代码中硬编码，以便在控制台修改 Prompt 而无需重新部署应用。

## 关键参数与配置

| 参数 | 说明 |
|------|------|
| `workspaceId` | [业务空间](workspace.md) ID，所有 Prompt 相关 API 调用的必传参数 |
| `promptTemplateId` | 模板 ID，从模板卡片获取 |
| `prompt` / `negative_prompt` | 文生图场景的正向和反向提示词 |
| `prompt_extend` | 文生图 V2 的大模型智能改写开关 |
| `enable_thinking` | 思考模式开关，影响模型推理深度 |

模板提示词输入框上限为 6144 字符。

## 与其他能力的关系

- **模型调优（Fine-Tuning）**：当 Prompt 工程无法满足需求时，可通过 SFT/DPO 等方式微调模型。Prompt 工程是模型调优前的优先尝试手段。
- **智能体应用**：智能体的系统提示词本质上是 Prompt 工程的应用，定义了智能体的角色和行为边界。
- **RAG**：Prompt 样例库（Few-shot 召回）与 RAG 知识库检索互补，官方推荐将样例库数据迁移至 RAG 表格库以获得更好效果。
- **应用组件 API**：通过 `CreatePromptTemplate`、`GetPromptTemplate` 等接口实现 Prompt 模板的编程化管理。

## 最佳实践

1. 优先使用预置模板验证效果，再根据业务需求创建自定义模板。
2. 利用自动优化功能对初版 Prompt 进行结构重组和指令具体化。
3. 通过 API 管理模板，实现 Prompt 与代码的分离部署。
4. 对输出格式有严格要求的场景（如 JSON、列表），在 Prompt 中明确指定格式约束。
5. 当 Prompt 优化到达瓶颈时，考虑结合样例库或转向模型调优。

## 关联主题页

- [prompt](../guides/prompt.md)
- [use cases](../guides/use-cases.md)
- [application component api reference](../api/application-component-api-reference.md)
- [fine tuning](../guides/fine-tuning.md)
- [llm application](../guides/llm-application.md)


