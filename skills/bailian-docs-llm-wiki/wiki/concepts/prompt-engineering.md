# Prompt 工程

Prompt 工程是通过设计、优化和管理输入给大语言模型的提示词（Prompt），以引导模型产生更准确、更符合预期输出的系统化方法。在百炼平台中，Prompt 工程贯穿文本生成、图像生成、视频生成、智能体应用构建及模型评测等多个场景，是发挥模型能力的关键技术手段。

## 核心原则

设计有效的 Prompt 遵循以下原则：

- **清晰具体**：任务描述越明确、无歧义，模型表现越好
- **结构化组织**：按"背景 → 目的 → 风格 → 语气 → 受众 → 输出"六要素构建 Prompt
- **少样本示例（Few-shot）**：提供输入-输出示例，引导模型理解任务格式和输出风格
- **思维链（Chain-of-Thought）**：对复杂推理任务，引导模型逐步思考再给出结论
- **限制输出格式**：明确指定 JSON、列表、表格等输出形式，减少后处理成本

## 百炼平台的 Prompt 工具链

百炼围绕 Prompt 工程提供了从设计、复用到自动优化的完整工具链：

### Prompt 模板

平台提供预置模板和自定义模板两种形式：

- **预置模板**：覆盖营销、办公、文案润色等通用场景，效果经过调优，开箱即用
- **自定义模板**：通过控制台或 `CreatePromptTemplate` API 创建，支持变量占位（`${name}` 格式），适合对输出格式有严格要求的业务场景

推荐通过 `GetPromptTemplate` API 动态获取模板内容，而非在代码中硬编码 Prompt，以便在控制台侧修改 Prompt 而无需重新部署应用。

### Prompt 自动优化

控制台提供一键优化功能，利用大模型对输入 Prompt 进行结构重组、角色引导、指令具体化和格式注入。入口位于「组件管理 → 提示词 → 自动优化」。

### Prompt 框架

创建自定义模板时可选择内置框架辅助构建：

| 框架 | 全称 | 适用场景 |
|------|------|----------|
| ICIO | Instruction / Context / Input Data / Output Indicator | 数据分析、内容生成、摘要 |
| CRISPE | Capacity & Role / Insight / Statement / Personality / Experiment | 智能客服、角色扮演交互 |
| RASCEF | Role / Action / Script / Content / Example / Format | 多步骤复杂业务流程 |

### Prompt 样例库（Few-shot 召回）

通过预定义高质量问答对，在请求时检索 Top-K 注入上下文，引导模型按特定结构和风格回答。适用于智能客服、领域问答、格式化输出等场景。

> 官方已推荐将样例库数据迁移到 RAG 表格库，新项目优先考虑反馈优化或 RAG 方案。

### Prompt 反馈优化

基于样例和评测集进行多轮迭代，自动生成更优的 Prompt。适合需要持续改进 Prompt 质量的场景。

## 不同生成场景的 Prompt 策略

### 文生文

核心在于清晰的任务描述和结构化组织。可配合 Few-shot 示例和思维链提升复杂任务的输出质量。

### 文生图

关键参数包括 `prompt`（正向提示词）、`negative_prompt`（反向提示词）和 `prompt_extend`（智能改写开关）。

- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

### 文生视频 / 图生视频

- **文生视频公式**：主体 + 场景 + 运动
- **图生视频公式**：运动 + 运镜（图像已确定主体和风格，重点描述动态过程）

wan2.5 及以上版本还支持声音描述，可通过 `prompt_extend_with_audio` 参数开启音频提示词智能改写。

## 与模型调优的关系

Prompt 工程和模型调优是提升模型表现的两条互补路径。推荐优先尝试 Prompt 工程（成本低、迭代快），当 Prompt 优化无法满足业务需求时，再考虑通过 SFT、DPO 等方式进行模型调优。

## 在应用构建中的角色

在智能体应用中，Prompt 工程体现为系统提示词（System Prompt）的设计，用于定义智能体的角色和行为边界。在模型评测中，评分器 Prompt 则用于指导裁判模型如何评分——两者虽然都称为 Prompt，但作用对象和阶段不同：

- **System Prompt**：作用于被评测模型，在生成答案时生效
- **评分器 Prompt**：作用于裁判模型，在打分时生效

## 关键配置参数

| 参数 | 说明 |
|------|------|
| `workspaceId` | [业务空间](workspace.md) ID，调用 Prompt 模板 API 时必传 |
| `promptTemplateId` | 模板 ID，从控制台模板卡片获取 |
| `prompt` / `negative_prompt` | 图像和视频生成的正向/反向提示词 |
| `prompt_extend` | 文生图模型的智能改写开关（默认 true） |
| `prompt_extend_with_audio` | 视频生成的音频提示词智能改写开关 |

> Prompt 模板输入框上限为 6144 字符。

## 关联主题页

- [prompt](../guides/prompt.md)
- [use cases](../guides/use-cases.md)
- [fine tuning](../guides/fine-tuning.md)
- [llm application](../guides/llm-application.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


