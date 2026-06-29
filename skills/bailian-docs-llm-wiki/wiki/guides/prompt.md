# prompt

阿里云百炼平台围绕 Prompt 工程提供了一整套能力，覆盖从模板化管理、自动优化到基于样例的反馈优化全流程，帮助开发者把固定结构 Prompt 与动态变量分离、复用并持续提升模型输出质量。相关能力均位于控制台「应用开发 > 组件管理 > 提示词」页面下。

> **注意**：Prompt 模板相关功能（Prompt 模板概述、自定义 Prompt 模板）文档明确标注仅适用于华北2（北京）地域，使用前请确认目标[业务空间](../concepts/workspace.md)所在地域。

## 核心能力一览

| 能力 | 入口 | 是否[计费](../concepts/billing.md) | 关键用途 |
| --- | --- | --- | --- |
| Prompt 模板（预置 + 自定义） | 提示词页面 | 模板管理不额外[计费](../concepts/billing.md) | 把 Prompt 结构与变量分离，统一管理、复用 |
| Prompt 自动优化 | 提示词 > 自动优化 | 不[计费](../concepts/billing.md) | 用大模型重写原始 Prompt，结构更优、指令更清晰 |
| Prompt 样例库 | 样例库页面 | 不收存储费，但增加调用 [Token](../concepts/token.md) | Few-shot 检索样例注入上下文，提升特定领域输出一致性 |
| Prompt 反馈优化 | 提示词 > 反馈优化 | 涉及推理调用 | 基于输入输出样例 + 评测数据多轮自动评估、反思、优化 |

## Prompt 模板

Prompt 模板将 Prompt 的固定结构与动态变量分离，分为预置模板和自定义模板两类，工作流程统一为：创建模板 → 通过模板 ID 获取模板 → 用业务数据填充变量生成最终 Prompt → 发送给目标模型。详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

### 预置与自定义对比

- **预置模板**：阿里云百炼提供，覆盖创意文案、办公助理等通用场景，效果稳定、不支持修改，适合 Prompt 设计经验不足的场景。
- **自定义模板**：用户自行设计，支持修改和迭代，适合金融风控、医疗咨询等复杂或对输出格式有严格要求的场景。可基于预置模板复制（生成「名称_副本_时间戳」），也可从零创建。详见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

### 创建方式

控制台创建自定义模板支持两种输入模式：

- **自定义创建**：已有现成 Prompt，直接粘贴到文本框，可单击「优化 Prompt」做简单润色后保存。
- **基于 Prompt 工程创建**：选择 ICIO / CRISPE / RASCEF 等框架，按框架结构填写指令、背景、输出格式等字段，再单击「优化 Prompt」生成结构化 Prompt。

也可通过 API 创建：先获取 Workspace ID，再调用 `CreatePromptTemplate` 接口。

### Prompt 工程框架

平台内置框架为复杂任务提供结构化思维模型，选择建议如下：

| 框架 | 适用场景 |
| --- | --- |
| ICIO | 简单、明确的任务执行，如数据分析、内容生成、文本摘要 |
| CRISPE | 需要 AI 扮演特定角色的交互，如智能客服、创意写作、面试模拟 |
| RASCEF | 涉及多步骤的复杂业务流程，如项目规划、战略分析、流程设计 |

### 图片生成模板

图片生成模板支持分别定义正向 Prompt（应该包含的内容）和负向 Prompt（应排除的内容），用于控制画面内容与风格。

### 使用与调用

- **控制台**：单击模板的「使用 prompt > 创建应用」，模板内容自动填充到[智能体应用](../concepts/agent-application.md)的提示词编辑框（最大 6144 字符），随后选择模型调试。
- **API / SDK**：通过 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId` 拉取模板内容（含 `variables`、`content` 等字段），在代码中填充变量后调用模型。相比字符串拼接，接口方式可实现逻辑与内容分离、集中管理与协作、版本一致性保障。

## Prompt 自动优化

当手动编写高质量 Prompt 耗时或缺乏经验时，可让大模型对原始 Prompt 进行结构重组、角色扮演引导、指令增强、安全与边界注入等重写，生成结构更优、效果更稳定的新版本。详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

操作步骤：进入「提示词 > 自动优化」页面 → 在「原始 prompt」框输入内容 → 单击「优化」查看「优化后 prompt」 → 复制使用或「保存为模板」。该功能不计费，提交的数据不会被存储或用于模型训练。优化失败常见原因包括输入超长超出 [Token](../concepts/token.md) 限制、触发内容审核、网络或服务临时不可用。

## Prompt 样例库（Few-shot 检索）

针对特定领域专业任务，通用大模型可能难以生成精准或符合预设格式的回答。样例库采用少样本学习思路：从预定义的高质量问答对中检索相关样例注入模型上下文，引导其生成更准确、风格更一致的回复，适用于智能客服、特定领域知识问答、格式化内容生成。详见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

> **注意**：Prompt 样例库功能已不再维护，官方推荐将样例库数据迁移到 RAG 表格库。

### 创建与关联

1. 在「样例库」页面新建样例库，支持手动输入或批量导入（小于 20MB 的 Excel，单次最多 100 条）。
2. 在同[业务空间](../concepts/workspace.md)的[智能体应用](../concepts/agent-application.md)配置中打开「样例库」开关，关联样例库（单应用最多 5 个，采用多路召回策略）。
3. 可选调整召回片段数（默认 5，最多 10），发布应用使配置生效。

### 使用限制

- 单样例库最多 300 条样例；超过建议按业务主题拆分多个库。
- 单应用最多关联 5 个样例库；单次请求最多召回 10 个片段注入上下文。
- 批量导入支持 20MB 以内 Excel，单次最多 100 条。

### 计费

样例库本身不收存储或管理费用，但召回样例会增加大模型调用 [Token](../concepts/token.md) 消耗。总输入 Token ≈ 用户查询 Token + 所有召回样例总 Token + 系统指令 Token。

## Prompt 反馈优化

相较于纯重写式的自动优化，反馈优化把用户提供的输入输出样例和评测数据作为评估标准，对 Prompt 在推理模型上的表现进行多轮自动化评估、反思和优化，最终生成包含原始指令、few-shot 样例和内容提示三部分的优化 Prompt，在用户实际场景中回复质量更高。详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

### 操作步骤

在「提示词 > 反馈优化」页面单击「新增优化任务」：

1. **选择推理模型**：在该模型上进行多轮 Prompt 评测，推荐选择千问-max。
2. **输入初始 Prompt**：只需描述任务目标。
3. **样例选择（可选）**：支持直接上传或从样例库选择；建议 5~10 条数据，且每种场景至少一条。样例会被添加到优化后的 Prompt 中。
4. **上传评测数据**：作为评估最优 Prompt 的标准，建议至少 20 条，数据越多效果越好。
5. **开始优化**：完成后可保存为 Prompt 模板或直接创建[智能体应用](../concepts/agent-application.md)。

### 典型场景

以汽车论坛文章分类为例，初始 Prompt 要求按 6 个类别输出 JSON，但模型分类不准确。用户提供手动分类的样例数据与评测数据后，反馈优化生成的 Prompt 在评测集上推理结果由错误转为正确（如质量投诉与销量关系的文本被正确分类为「销量表现」）。

## 限制与注意事项

- **地域限制**：Prompt 模板（预置/自定义）相关功能仅适用于华北2（北京）地域。
- **字符与 Token**：智能体应用提示词输入框最大支持 6144 字符；自动优化输入过长会因超出 Token 限制而失败。
- **数据安全**：自动优化提交的数据不会被存储或用于模型训练。
- **功能维护状态**：Prompt 样例库已不再维护，建议迁移至 RAG 表格库；反馈优化仍为推荐路径。
- **计费影响**：模板管理与自动优化不额外计费；样例库本身免费但增加调用 Token；反馈优化涉及推理模型多轮调用，会产生相应 Token 费用。
- **调用失败排查**：若 API 调用返回错误码，参见平台错误码文档定位。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)



