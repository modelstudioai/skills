# prompt

阿里云百炼围绕 Prompt 提供了一整套从设计、复用到自动优化的工具链，覆盖预置模板、自定义模板、单轮自动优化、基于样例库的少样本召回以及基于评测数据的反馈式优化。本页汇总各能力的适用场景、关键操作与限制，帮助开发者快速选型并集成到智能体应用中。

> **注意**：本系列功能目前仅适用于中国大陆版（北京地域）。

## 能力矩阵

| 能力 | 用途 | 入口 | 是否计费 |
| --- | --- | --- | --- |
| 预置 Prompt 模板 | 开箱即用的场景化模板（营销、办公、文案润色等） | 控制台「提示词」插件市场 | 不额外计费 |
| 自定义 Prompt 模板 | 业务定制 + 集中管理 + API 拉取 | 控制台「组件管理 → 提示词」/ CreatePromptTemplate API | 不额外计费 |
| Prompt 自动优化 | 单条 Prompt 一键重写 | 「提示词 → 自动优化」 | 不计费 |
| Prompt 样例库（少样本召回） | 在线检索高质量样例注入上下文 | 「组件管理 → 样例库」 | 不收存储费，但增加模型调用 Token |
| Prompt 反馈优化 | 基于样例 + 评测集多轮迭代生成 Prompt | 「提示词 → 反馈优化」 | 不计费 |

> **注意**：[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 已不再维护，官方推荐将样例库数据迁移到 RAG 表格库（参见控制台「Prompt 样例库迁移到 RAG 表格库」文档）。新接入项目优先考虑反馈优化或 RAG。

## Prompt 模板

### 模板分类与差异

详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

- **预置模板**：阿里云已调优，效果稳定，覆盖营销标题、营销文案、商品推广、摘要抽取、文案润色、风格改写、商品评论等通用场景；卡片支持「复制 prompt / 创建应用 / 调用 API / 复制模板」操作。不支持原地修改，但可一键复制为自定义模板再编辑。
- **自定义模板**：通过控制台或 API 创建，适合金融风控、医疗咨询等对格式（如 JSON、列表）有严格要求的场景；可随时编辑、删除、复制为副本。

### 工作流程

1. **创建模板** —— 控制台或 `CreatePromptTemplate` API。
2. **获取模板** —— 通过 `GetPromptTemplate` 接口拿到模板内容与变量列表（变量字段名以 `${name}` 占位）。
3. **生成 Prompt** —— 由调用方将业务数据填入变量。
4. **下发模型** —— 把渲染好的 Prompt 发给目标模型。

> 推荐用 `GetPromptTemplate` 接口而不是在代码里拼字符串：可以在控制台改 Prompt 而不重新部署应用、便于多人协作和版本管理、保证跨服务的一致性。

### 创建自定义模板

[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md) 介绍了两种文本生成模板的输入模式，以及单独的图片生成模板入口：

- **自定义创建**：粘贴已有 Prompt，可调用「优化 Prompt」二次润色，再保存。
- **基于 Prompt 工程创建**：按内置框架填字段后由平台自动优化。可选框架：
  - **ICIO**（Instruction / Context / Input Data / Output Indicator）：适合数据分析、内容生成、摘要等明确任务。
  - **CRISPE**（Capacity & Role / Insight / Statement / Personality / Experiment）：适合需要 AI 扮演特定角色的交互，如智能客服、面试模拟。
  - **RASCEF**（Role / Action / Script / Content / Example / Format）：适合多步骤的复杂业务，如项目规划、上市策略。
- **图片生成模板**：分别填写正向 Prompt（应包含元素）和负向 Prompt（应排除元素），保存即可。

### 调用关键参数

调用 `GetPromptTemplate` 必须传：

| 参数 | 含义 | 获取方式 |
| --- | --- | --- |
| `workspaceId` | [业务空间](../concepts/workspace.md) ID | 参考「获取 APP ID 和 Workspace ID」 |
| `promptTemplateId` | 模板 ID | 模板卡片上展示 |

响应体关键字段：`name`（模板名）、`content`（含变量占位）、`variables`（变量列表）、`promptTemplateId`、`requestId`。

> 模板提示词输入框上限 6144 字符。

## Prompt 自动优化（单条重写）

[Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 入口：控制台「应用开发 → 组件管理 → 提示词」右上角「自动优化」。

工作机制：用大模型对输入 Prompt 做结构重组、角色扮演引导、指令具体化、格式与边界注入。

操作流程：

1. 在「原始 prompt」输入框粘贴待优化文本。
2. 点击「优化」。
3. 在「优化后 prompt」处复制结果，或「保存为模板」进入 Prompt 模板库。

常见失败原因：输入超出 Token 限制、触发安全审核、网络/服务临时不可用。

> 阿里云声明：自动优化提交的数据不用于模型训练。

## Prompt 样例库（Few-shot 召回）

通过预定义高质量问答对，在请求时检索 Top-K 注入到大模型上下文，引导其按既定结构/风格回答。典型用途：智能客服、特定领域问答、格式化输出。

### 创建与接入

[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 流程：

1. 在「样例库」页面新建样例库，支持「手动输入」或「批量导入」（≤ 20MB 的 Excel，单次最多 100 条）。
2. 在「应用管理」→ 目标智能体应用 → 配置中打开「样例库」开关，添加样例库。
3. （可选）调整召回片段数，默认 5，最多 10。
4. 发布应用使配置生效。

### 限制

| 项 | 上限 |
| --- | --- |
| 单样例库样例数 | 300 条 |
| 单应用关联样例库数 | 5 个（多路召回） |
| 单次召回片段数 | 10 |
| 批量导入文件 | 20MB / 100 条 |

> **注意**：超过 300 条建议按主题拆分多库（如「产品功能库」「售后策略库」），单库过大会增加检索延迟。

### 验证与计费

- 控制台调试时点击「prompt 样例检索」可查看本次召回的输入输出。
- API 调用时设置 `has_thoughts=true`，响应的 `thoughts` 字段会返回检索过程，便于排查。
- 样例库本身不收存储/管理费，但召回内容会进入模型输入，按 Token 计费。预估公式：`总输入 Token ≈ 用户查询 Token + 所有召回样例 Token + 系统指令 Token`。

## Prompt 反馈优化（基于评测集多轮迭代）

[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 与单条「自动优化」相比，把用户提供的**评测数据集**作为评估标准，由推理模型多轮反思-改写-再评估，最终产出在该业务场景下表现更好的 Prompt。

### 数据要求

| 数据集 | 推荐量 | 说明 |
| --- | --- | --- |
| 样例数据 | 5 ~ 10 条 | 自动注入到优化后的 Prompt 里，每种场景至少 1 条 |
| 评测数据 | ≥ 20 条 | 用于评估 Prompt 表现，数据越多效果越好 |

> 推理模型推荐 **qwen-max**。

### 操作步骤

1. 「提示词 → 反馈优化」→「新增优化任务」。
2. 选择推理模型。
3. 输入初始 Prompt（仅描述任务目标即可）。
4. 上传样例数据（支持文件或从样例库选择）。
5. 上传评测数据。
6. 启动优化，结束后可「保存为 Prompt 模板」或直接「创建智能体应用」。

## 选型建议

| 诉求 | 推荐能力 |
| --- | --- |
| 通用场景，没有特殊定制 | 预置 Prompt 模板（直接复制或一键创建应用） |
| 自有业务、需 API 拉取并多版本管理 | 自定义 Prompt 模板 |
| 已有 Prompt，想一键润色 | Prompt 自动优化 |
| 需要严格遵循既有风格/格式 | Prompt 样例库（短期）→ 迁移到 RAG 表格库（长期） |
| 有标注好的样例 + 评测集，追求生产环境最优 | Prompt 反馈优化 |

## 错误与排查

- 模板/优化接口调用失败时，参考阿里云百炼「错误码」文档处理。
- Prompt 自动优化失败通常源于 Token 超限、内容审核或临时网络问题。
- 已被应用引用的样例库不能直接删除，需先在「应用管理」中解除引用。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)






