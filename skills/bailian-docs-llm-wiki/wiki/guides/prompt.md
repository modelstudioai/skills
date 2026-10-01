# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为静态文本直接调用模型，也可通过模板化、自动化优化、样例增强等方式进行工程化管理。当前平台提供 Prompt 模板、Prompt 自动优化、Prompt 反馈优化三类核心能力，并已将历史 Prompt 样例库功能迁移至更灵活的 RAG 表格库体系。所有能力均面向开发者设计，强调可复用性、可调试性与生产环境一致性。

## 支持的模型/功能

百炼平台支持以下 Prompt 相关功能，均基于通义系列大模型（如千问-max、千问-Plus-Latest）实现：

- **Prompt 模板**：支持预置模板与自定义模板，涵盖文本生成、图片生成两大类型；自定义模板提供 ICIO、CRISPE、RASCEF 等结构化 Prompt 工程框架，适用于从简单摘要到复杂流程规划的全场景 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 自动优化**：对单条原始 Prompt 进行结构重组、角色注入、指令增强等重写，不依赖用户数据，适合快速提升基础 Prompt 质量 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（few-shot data）和评测数据集，通过多轮模型评估与反思生成高适配性 Prompt，推荐使用千问-max 作为推理模型 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **Prompt 样例库（已下线）**：该功能已于近期停止维护，官方明确要求迁移到 RAG 表格库以获得更高容量、更细粒度的检索控制与策略配置能力 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

> **注意**：文档 1 中仍详述了 Prompt 样例库的创建、关联与限制，但其首段即声明“该功能已不再维护”，与文档 2 的迁移指引完全一致。开发者应以文档 2 为唯一权威依据，避免在新项目中启用样例库。

## 关键参数

| 参数 | 说明 | 可配置性 | 来源 |
|------|------|----------|------|
| `has_thoughts` | API 请求参数，设为 `true` 时返回 `thoughts` 字段，含样例检索或 RAG 召回的完整过程日志，用于调试验证 | ✅ 控制台/API 均支持 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)、[Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |
| 召回片段数（RAG 表格库） | 控制每次请求注入上下文的召回知识条目数量，默认 5，最大 10 | ✅ 应用配置中可调 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)（注：该参数现仅适用于 RAG 表格库） |
| 最大拼装长度（token） | RAG 表格库拼装策略中可设上限，防止上下文超长 | ✅ 调试界面可调 | [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |
| promptTemplateId / workspaceId | 调用 Prompt 模板 API 所需的必需参数，用于精准拉取模板内容 | ✅ 必填 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |

## 使用方式

### 控制台操作路径
- **模板管理**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 创建/编辑/使用模板。
- **自动优化**：在 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面右上角点击 **自动优化** → 输入原始 Prompt → 点击优化 → 复制或保存为模板。
- **反馈优化**：在 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面选择 **反馈优化** → 新增任务 → 配置推理模型、初始 Prompt、样例数据（5–10 条）、评测数据（≥20 条）→ 启动优化。
- **RAG 表格库替代样例库**：访问 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) → 创建「数据查询」型知识库 → 上传原样例库导出的 Excel 文件 → 在智能体应用配置中关闭样例库开关，添加该表格库并调试召回效果。

### API 集成要点
- 使用 `GetPromptTemplate` 接口获取模板内容，再填充变量生成最终 Prompt（推荐方式，保障逻辑与内容分离）[Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- 调用应用 API 时，务必设置 `has_thoughts=true` 以获取 `thoughts` 字段，用于验证 Prompt 注入与知识召回是否符合预期。
- 创建自定义模板可通过 `CreatePromptTemplate` 接口完成，需提前获取 `workspaceId` [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

## 限制和注意事项

- **地域限制**：Prompt 模板功能（含预置与自定义）**仅支持华北2（北京）地域**，跨地域调用将失败 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)、[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **容量与性能**：
  - 单个 Prompt 模板内容最大支持 6144 字符（控制台编辑器右下角实时计数）。
  - RAG 表格库无单库条目上限，但建议按业务主题分表（如“产品FAQ”“售后政策”），避免单表过大影响检索精度。
- **数据安全**：Prompt 自动优化功能**不存储、不训练、不共享**用户提交的 Prompt 数据，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **计费影响**：
  - Prompt 模板本身不产生费用；但通过模板生成的 Prompt 若包含大量样例或长背景信息，将显著增加输入 Token，从而推高模型调用成本。
  - RAG 表格库按小时计费（规格费 + 向量/排序模型调用费），而原 Prompt 样例库功能免费但已停用 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **版本兼容性**：预置 Prompt 模板不支持修改；如需定制，必须通过「复制模板」生成自定义副本后编辑。

## 来源文档

- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)


