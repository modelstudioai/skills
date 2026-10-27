# Prompt 工程

Prompt 工程是系统化设计、构建、测试与优化大语言模型输入指令（Prompt）的方法论与实践体系，旨在通过结构化表达、知识注入、角色设定、示例引导和自动迭代等手段，稳定提升模型输出的准确性、一致性、安全性与业务适配性。它不是一次性文本编写，而是覆盖模板管理、RAG增强、反馈驱动优化和多模态适配的全生命周期工程实践。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）构建**：在零代码/低代码 Agent 配置中，Prompt 工程体现为「系统提示词」的结构化编写（如采用 CRISPE 或 RASCEF 框架），并结合 `context` 机制动态注入 RAG 检索结果、历史记忆或外部数据，使 Agent 具备可解释、可调试、可复现的推理行为。
- **工作流（Workflow）编排**：在大模型节点中，Prompt 以模板形式被调用，支持变量填充（如 `{{input.question}}`）与多轮上下文拼接；配合 `enable_thinking` 参数开启思维链，Prompt 工程进一步延伸至推理路径显式建模。
- **多模态生成任务**：文生图、文生视频等场景需专用 Prompt 工程——例如万相3.0要求正向 Prompt 精确描述主体、风格、构图，负向 Prompt 明确排除干扰元素，且受 `size`、`negative_prompt` 字符长度等硬性参数约束。
- **资产中心复用**：Prompt 模板作为一类核心资产（`asset_type=prompt_template`），可通过 `asset_id` 直接调用，支持跨应用共享与版本管理；调用时需严格匹配模板声明的 `variables`，不可动态新增字段。
- **RAG 增强替代路径**：传统少样本样例库已停用，Prompt 工程能力已收敛至 RAG 表格库——通过结构化表格（如 FAQ 表、产品参数表）替代人工构造样例，由检索策略（`recall_count`、`score_threshold`）和重排逻辑保障知识注入质量。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一标识（32位十六进制字符串） | 控制台创建后可见；API 调用 `GetPromptTemplate` 必填，用于获取 `content` 和 `variables` |
| `variables` | 模板中预定义的动态占位符列表（如 `["query", "product_id"]`） | 调用前必须完整提供，缺失或多余字段将导致 400 错误；不支持运行时扩展 |
| `recall_count`（RAG 表格库） | 每次检索召回的知识片段数 | 默认 5，最大 10；在应用配置页调整，影响 [prompt](../guides/prompt.md) 上下文长度与响应速度平衡 |
| `max_tokens`（图片/视频生成） | 正向/负向 Prompt 总字符上限 | 单字段建议 ≤1024；超长将被截断，导致语义丢失；需在模板编辑时实时关注右下角计数器 |
| `workspaceId` | 业务空间 ID | 所有 Prompt 相关 API（模板、RAG、优化）均强制要求；非华北2（北京）地域调用将直接失败 |

> ⚠️ 注意：所有 Prompt 工程能力（模板、自动优化、反馈优化、RAG 表格库）**仅限华北2（北京）地域可用**；跨地域请求返回 `403 Forbidden`。

## 面向开发者，简洁实用

- ✅ **优先用模板，而非硬编码 Prompt**：在控制台创建模板 → 获取 `promptTemplateId` → SDK 调用 `GetPromptTemplate` → 填充 `variables` → 生成最终 Prompt。避免在代码中拼接字符串。
- ✅ **RAG 表格库 = 新一代 Prompt 工程基础设施**：停止维护样例库；将业务知识整理为 Excel 表格（列名即变量），上传至 RAG 表格库，配置召回策略，在 Agent 或 Workflow 中一键绑定。
- ✅ **自动优化免费且安全**：对原始 Prompt 调用 `/v1/prompt/optimization` 接口，无需训练数据，不存储输入，即时返回增强版 Prompt；适合快速验证基础指令有效性。
- ✅ **反馈优化用于高精度场景**：准备 5–10 条典型输入输出样例 + ≥20 条评测数据 → 选择 `qwen-max` 作为优化模型 → 启动优化 → 保存为新模板。适用于客服话术、合同审查等强业务规则场景。
- ✅ **调试必开 `debug: true` 和 `has_thoughts: true`**：在 API 请求中启用，响应中将返回实际注入的 Prompt 内容、召回知识片段、token 统计及思考过程，直击问题根因。
- ❌ **不要跨地域调用**：检查 `region_id` 是否为 `cn-beijing`；SDK 初始化时显式指定。
- ❌ **不要超出模板容量**：单模板 `content` 最大 6144 字符；图片生成类 Prompt 单字段建议 ≤1024 字符。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [asset center page](../guides/asset-center-page.md)
- [agent context](../guides/agent-context.md)


