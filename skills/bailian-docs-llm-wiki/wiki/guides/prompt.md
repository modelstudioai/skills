# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，支持通过模板化、样例增强、自动优化等多种机制实现结构化设计、集中管理和效果迭代。开发者可基于业务场景选择预置模板快速启动，或通过自定义模板、反馈优化、RAG 表格库等能力构建高精度、强可控的提示工程体系。所有功能均面向华北2（北京）地域提供服务。

## 支持的模型/功能

- **Prompt 模板**：支持预置与自定义两类模板，覆盖文本生成、图片生成等场景。预置模板由百炼官方提供并已优化，适用于通用场景；自定义模板支持通过控制台或 API 创建，可基于 [ICIO/CRISPE/RASCEF 等 Prompt 工程框架](raw/application-user-guide/prompt/prompt-custom-template.md) 结构化构建，适用于金融、医疗等专业领域 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **Prompt 样例库**：通过少样本学习注入高质量问答对，引导模型输出风格与格式一致性。但该功能**已停止维护**，官方明确要求迁移至 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与边界注入，无需样例数据即可提升清晰度与稳定性 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：需用户提供输入输出样例（建议 5–10 条）及评测数据集（建议 ≥20 条），通过多轮评估与反思生成带 few-shot 示例和内容提示的优化版 Prompt，效果更贴合实际业务需求。

> **注意**：文档 3 明确声明“Prompt样例库功能已不再维护”，而文档 4 提供完整迁移路径；二者存在明确的弃用与替代关系，开发者应以 RAG 表格库为当前标准方案，不得新建样例库。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspaceId` | 业务空间 ID，调用 Prompt 相关 API 的必需参数 | 从 [获取APP ID 和 Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等接口 | 控制台模板卡片上直接复制，长度固定 |
| `variables` | 模板中声明的动态变量名列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可在调用时自行增删 |
| `has_thoughts` | 应用 API 调用参数，启用后响应含 `thoughts` 字段（含样例检索或 RAG 召回详情） | `true` / `false`，仅调试阶段建议开启 |
| 召回片段数 | RAG 表格库配置项，控制注入上下文的样例数量 | 默认 5，最大 10（见 [RAG 表格库配置](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)） |

## 使用方式

- **模板创建与调用**：  
  - 控制台路径：`提示词 > 创建提示词` → 选择“文本生成”或“图片生成”，指定输入模式（自定义创建 / 基于 Prompt 工程创建）→ 保存后获取 `promptTemplateId`。  
  - API 调用：先调用 `CreatePromptTemplate` 创建，再用 `GetPromptTemplate` 拉取模板内容并填充变量，最后将生成的 Prompt 发送给目标模型。完整流程详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

- **RAG 表格库替代样例库**：  
  1. 从旧样例库导出 Excel 数据；  
  2. 在 `知识库 > 创建数据查询类型库` 中上传该文件，**关闭 `answer` 字段的“参与检索”开关**以复现原样例库仅匹配问题的行为；  
  3. 在智能体应用配置中关闭样例库开关，添加新表格库，并按需调整相似度阈值与拼装策略。

- **反馈优化任务**：  
  进入 `提示词 > 反馈优化` 页面 → 选择推理模型（推荐 `qwen-max`）→ 输入初始 Prompt → 上传样例数据（5–10 条）与评测数据（≥20 条）→ 启动优化 → 保存结果为模板或直接创建应用。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库/RAG）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板字符上限**：控制台编辑 Prompt 模板时，输入框右下角显示字符计数，**最大支持 6144 个字符**（非 Token 数），超长需精简或拆分逻辑。
- **样例库已弃用**：文档 3 与文档 4 共同确认 Prompt 样例库功能终止，新项目严禁使用；存量应用须按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档完成迁移。
- **Token 成本影响**：启用 RAG 表格库或样例库会显著增加输入 Token（用户 query + 召回样例内容），直接影响调用费用，需在 `召回片段数` 与 `最大拼装长度` 间权衡效果与成本。
- **安全与隐私**：Prompt 自动优化过程不存储用户输入，亦不用于模型训练，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


