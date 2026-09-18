# 提示工程

提示工程（Prompt Engineering）是系统性设计、优化和管理大语言模型输入指令（[prompt](../guides/prompt.md)）的技术实践，旨在通过结构化表达、角色设定、上下文注入与约束控制等手段，显著提升模型输出的准确性、一致性、安全性与业务适配性。它既是低代码应用构建的核心方法论，也是高代码集成中实现可控生成的关键能力层。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，提示工程不是单一功能，而是贯穿模型调用全链路的横切能力，按使用深度分为三层：

- **基础层（直接调用）**：在 `start using` 和 `application support` 场景中，开发者通过 `input.messages` 数组（含 `system`/`user` 角色）直接构造 [prompt](../guides/prompt.md)，例如设置 `system` 消息定义角色与规则，`user` 消息提供任务指令与输入变量。此时提示工程体现为人工编写高质量指令的能力，适用于快速验证或轻量级集成。

- **工程层（模板化管理）**：在 `llm application`（尤其是 Agent 2.0 和工作流应用）中，[prompt](../guides/prompt.md) 以**Prompt 模板**形式统一管理。支持 `${variable}` 占位符动态填充、ICIO/CRISPE/RASCEF 等结构化框架建模，并可绑定至特定 `app_id`。模板内容经平台校验（如变量完整性、长度 ≤6144 字符），确保跨环境一致生效。

- **智能层（自动优化）**：在 `prompt` 主题下，平台提供两类自动化能力：
  - **Prompt 自动优化**：对原始 prompt 进行语义重组、角色强化与安全边界注入，适合无 Prompt 工程经验的开发者；
  - **Prompt 反馈优化**：基于 5–10 条高质量样例（query-answer pairs）和 ≥20 条评测数据，自动生成带 few-shot 示例与格式约束的高精度 prompt，专用于分类、JSON 结构化等确定性任务。

> ⚠️ 注意：已停用的 Prompt 样例库功能，其少样本引导能力由 **RAG 表格库**承接——即通过知识库召回相关样例片段注入 prompt 上下文，而非静态维护样例集合。新项目必须迁移，存量项目需按指引完成替换。

## 关键参数和配置

| 参数 | 说明 | 使用场景 | 约束 |
|------|------|----------|------|
| `promptTemplateId` | 模板唯一 ID，用于 API 调用或应用绑定 | 模板调用、应用配置 | 必填；控制台模板卡片可复制 |
| `workspaceId` | 所有 prompt 资源（模板、RAG 库）的归属空间 ID | 创建/调用模板、关联 RAG | 必填；跨 workspace 不可见 |
| `variables` | 模板声明的变量名数组（只读） | 填充前校验输入完整性 | 由 `GetPromptTemplate` 接口返回 |
| `has_thoughts=true` | 启用后在响应中返回 `thoughts` 字段，展示 RAG 召回/样例匹配过程 | 调试 prompt 效果与检索逻辑 | 仅调试有效，非生产必需 |
| `retrieval_config.top_k` | RAG 表格库召回片段数（默认 5，上限 10） | 配合 RAG 使用的 prompt 场景 | 影响 token 消耗与延迟，建议按精度需求权衡 |

> 🌐 所有 prompt 相关能力（模板、优化、RAG 注入）**仅支持华北2（北京）地域**，跨地域调用将失败。

## 面向开发者，简洁实用

- ✅ **优先用模板**：避免硬编码 prompt。在控制台「提示词」页创建模板，再在应用配置中“使用 prompt 创建应用”，自动注入并支持变量替换。
- ✅ **结构化优于自由发挥**：对业务强约束场景（如金融报告生成、医疗术语解释），采用 CRISPE 或 RASCEF 框架组织 prompt，明确 Role、Action、Steps、Persona、Examples。
- ✅ **少样本 ≠ 样例库**：不再新建 Prompt 样例库；改用 RAG 表格库上传结构化问答对，或直接在反馈优化中上传样例数据驱动 prompt 生成。
- ✅ **调试必开 `has_thoughts`**：调用 `InvokeApplication` 时添加该参数，查看 `thoughts.retrieved_chunks` 或 `thoughts.optimized_prompt`，快速定位 prompt 失效原因。
- ✅ **长度严守红线**：模板内容 ≤6144 字符；单次请求 `messages` 总 token ≤模型 context length（如 qwen-max 为 32768）；超长将静默截断，不报错。

> 💡 提示工程的终点不是“写得更巧”，而是“管得更稳”——通过模板版本化、RAG 动态增强、反馈闭环优化，让 prompt 成为可测试、可部署、可审计的工程资产。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


