# prompt

Prompt 是大语言模型应用的核心指令，用于精确控制模型的输出风格、格式与推理逻辑。阿里云百炼平台提供了一套完整的 Prompt 工程化工具链，涵盖模板化管理、自动化重写与基于样本反馈的迭代优化机制。开发者可通过结构化配置、动态变量替换与 API 集成，高效维护指令版本并显著提升复杂业务场景下的模型响应质量。

## 支持的模型与功能
- **模型兼容性**：Prompt 配置与优化功能适用于平台接入的全量文本生成大模型（如 [[千问系列]]）及图像生成模型。
- **模板化管理**：支持[[预置Prompt模板]]与[[自定义Prompt模板]]。文本生成场景支持基于 ICIO、CRISPE、RASCEF 等标准 Prompt 工程框架的结构化设计；图像生成场景支持正向（包含元素）与负向（排除元素）提示词分离配置。详细说明参见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **自动化优化引擎**：
  - **自动优化**：利用基座大模型对原始指令进行结构重组、专家角色注入与边界约束强化，快速生成高可用性 Prompt。详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - **反馈优化**：基于开发者提供的 I/O 样例集与独立评测数据集，通过多轮自动化评估与反思迭代生成 Prompt。该机制特别适用于强格式输出（如 JSON）或高精度分类任务。详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数与配置
- **动态变量占位符**：自定义模板使用变量语法分离固定指令结构与运行时数据。部署时通过 [[业务空间]]（Workspace ID）进行上下文隔离与参数注入。
- **优化数据配比**：在反馈优化流程中，**样例数据**建议覆盖所有目标类别（5~10 条），**评测数据集**建议不少于 20 条。数据分布的均衡性与数量直接决定优化后 Prompt 的泛化边界与准确率。
- **推理基座配置**：执行 Prompt 优化任务时，底层评估引擎推荐指定为高逻辑推理能力的模型（如 `qwen-max`），以避免优化过程中的指令畸变。
- **图像生成约束**：正/负向 Prompt 需避免特征冲突。负向提示词应聚焦于明确排除的视觉元素或负面风格词，以提升画面生成稳定性。

## 使用方式
### 控制台工作流
1. **构建与保存**：在提示词控制台选择“自定义创建”或“基于 Prompt 工程创建”，完成结构化字段填充后保存，系统自动生成唯一 Template ID。
2. **应用集成**：在 [[智能体应用]] 的配置面板中直接关联或复制模板内容至系统提示词区。支持一键切换不同工程框架。
3. **迭代发布**：通过优化控制台提交指令或上传 Excel 样例，生成优化版本后可一键保存至模板库或直接发布至应用环境生效。

### API 与 SDK 集成
- **动态拉取**：调用 `GetPromptTemplate` 接口传入 `workspaceId` 与 `promptTemplateId` 获取最新 Prompt 内容。该模式实现业务代码与指令逻辑解耦，支持控制台热更新而无需重新部署应用。
- **调试与鉴权**：API 调用需注入有效的 `accessKeyId` 与 `accessKeySecret`。可在控制台生成多语言 SDK 示例直接集成。完整调用链路、参数说明及错误码处理参见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **推理追踪**：在应用级 API 调用时，建议开启 `has_thoughts` 或类似追踪参数，便于在响应中查看 Prompt 组装、变量替换及模型推理的完整中间态，快速定位上下文截断或格式漂移问题。

## 限制和注意事项
- **地域适用范围**：当前 Prompt 模板管理控制台及自动优化功能仅面向**中国大陆版（北京地域）**实例开放。其他地域需依赖纯 API 流程进行指令维护。
> **注意**：`Prompt样例库`（Few-shot 检索库）功能已正式停止维护。为保障检索性能与系统长期兼容性，请将存量样例数据迁移至 [[RAG表格库]]，利用结构化向量化检索与混合召回策略实现更稳定的少样本上下文注入。
- **Token 消耗与成本控制**：优化功能本身不计费，但启用样例库或大型模板会显著增加请求上下文的 Token 占用。实际输入开销计算为：`总输入 Token ≈ 用户查询 Token + 召回样例/模板变量 Token + 系统指令 Token`。建议在应用配置中严格限制最大召回片段数（默认 5，上限 10），防止上下文溢出。
- **数据安全策略**：所有提交至优化控制台与反馈评估的 Prompt 及样例数据严格遵循平台隐私规范，仅用于单次计算，**不会持久化存储且绝对不参与任何基础模型的训练或微调**。
- **框架选型建议**：简单指令优化可使用“自动优化”快速迭代；涉及多步骤业务流、角色权限控制或严格输出格式的任务，务必在创建模板时选用内置工程框架（如 RASCEF），否则模型极易忽略隐含的上下文依赖条件。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)

