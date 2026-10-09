# Prompt 工程

Prompt 工程是系统化设计、验证与优化大语言模型输入指令（Prompt）的方法论与工程实践，其目标是通过结构化表达任务意图、约束上下文、引导推理路径与规范输出格式，显著提升模型响应的准确性、一致性、可控性与业务适配性。在百炼平台中，它不是一次性技巧，而是可复用、可管理、可迭代的核心基础设施能力。

## 在百炼平台的不同场景中，这个概念如何使用

Prompt 工程在百炼平台贯穿模型调用全链路，具体体现为以下四类工程化实践：

- **模板驱动开发**：通过控制台或 API 管理结构化 Prompt 模板（如 ICIO、CRISPE 框架），支持变量插值（`${topic}`）、角色设定、示例注入与跨环境复用。适用于标准化应用（如客服问答、报告生成），确保不同开发者、不同版本间 Prompt 行为一致。
- **知识增强型工程**：将 Prompt 与 RAG 表格库深度耦合——不再依赖已下线的 Prompt 样例库，而是通过 `has_thoughts: true` 启用召回溯源，并配置 `recall_count` 控制知识片段数量（默认 5，上限 10）。典型场景包括政策解读、产品文档问答等强事实性任务。
- **多模态 Prompt 编排**：在图像/视频生成类模型（如万相、Qwen-Image）中，Prompt 工程体现为正向提示词（`prompt`）与负向提示词（`negative_prompt`）的协同设计；万相 3.0 还支持分镜语法（`分镜1（0-3秒）：...`）、参考素材引用（`图1`）和导演风格关键词（`宫崎骏风格`），需按语义粒度精细组织。
- **翻译与多模态任务定制**：在 Qwen-MT 系列中，Prompt 工程转化为领域提示（`ext.domainHint`）、术语干预（`ext.terminologies`）和敏感词过滤（`ext.sensitives`）等参数化指令，实现对译文风格、专业术语与合规边界的精准控制。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 使用场景 |
|--------|------|------|----------|
| `promptTemplateId` | string | 模板唯一标识符，用于 API 获取模板内容 | 模板化调用（所有文本生成类模型） |
| `workspaceId` | string | 业务空间 ID，所有 Prompt 相关操作必需 | 所有 Prompt 功能的基础上下文 |
| `variables` | array<string> | 模板中声明的变量名列表（如 `["platform", "topic"]`），用于运行时填充 | 模板渲染前必校验的字段 |
| `has_thoughts` | boolean | 启用后返回 `thoughts` 字段，含 RAG 召回详情与推理依据 | 知识增强类应用调试与可解释性分析 |
| `recall_count` | integer | RAG 表格库召回片段数（默认 5，上限 10） | 平衡响应质量与 [Token](token.md) 成本的关键调优参数 |
| `prompt_extend` | boolean | （万相 V2 特有）开启后由大模型智能改写原始 Prompt，默认 `true` | 文生图场景中提升语义完整性 |
| `ext.domainHint` / `ext.terminologies` | string / object[] | 领域提示（英文）与术语表，直接嵌入 Prompt 逻辑层 | Qwen-MT 翻译类模型的 Prompt 定制核心 |

> ⚠️ 注意：Prompt 样例库功能已全面下线，所有依赖该能力的应用必须迁移至 RAG 表格库；`has_thoughts` 参数同时兼容旧样例库（仅限存量）与新 RAG 表格库，但新项目应仅绑定 RAG 表格库。

## 面向开发者，简洁实用

- **起步最快方式**：进入控制台 `应用开发 > 组件管理 > 提示词 > 自动优化`，粘贴原始自然语言指令，一键生成结构化模板并保存复用。
- **调试黄金组合**：调用时设置 `has_thoughts: true` + `recall_count: 3`，观察 `thoughts.retrieved_chunks` 内容是否匹配业务预期，再逐步调高 `recall_count` 或优化 RAG 表格库索引策略。
- **多模态 Prompt 必检项**：
  - 图像生成：检查 `negative_prompt` 是否明确排除模糊、畸变、水印等干扰项；
  - 视频生成：确认分镜语法格式正确（`分镜N（起-止秒）：...`），且参考素材 ID（`图1`/`音频2`）与 `input.files` 中顺序严格对应；
  - 翻译任务：`ext.domainHint` 必须为英文短语（≤200 单词），`ext.terminologies` 中 `source`/`target` 字段需完全匹配原文与译文。
- **避坑提醒**：
  - 所有 Prompt 功能仅支持华北2（北京）地域，跨地域 endpoint 调用必然失败；
  - 单个模板最大长度为 6144 字符，超长需拆分为多步骤 Prompt 链或启用 RAG 分片召回；
  - 使用三方模型（如 Kimi、DeepSeek）时，Prompt 工程仍有效，但需通过 `extra_body` 或顶层字段传入非标准参数（如 `enable_thinking`）。

## 关联主题页

- [prompt](../guides/prompt.md)
- [use cases](../guides/use-cases.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)


