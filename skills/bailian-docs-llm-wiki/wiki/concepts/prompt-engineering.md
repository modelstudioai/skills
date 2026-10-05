# Prompt 工程

Prompt 工程是系统性设计、验证与优化大模型输入指令（[prompt](../guides/prompt.md)）的方法论与实践过程，旨在通过结构化表达任务目标、角色设定、约束条件和示例样本，显著提升模型输出的准确性、一致性与可控性。它不仅是文本生成的起点，更是连接业务逻辑与模型能力的核心桥梁。

## 在百炼平台的不同场景中如何使用

- **基础模型调用**：在 `/v1/chat/completions` API 中，通过 `prompt_template_id` + `variables` 组合复用预定义模板，避免硬编码 [prompt](../guides/prompt.md)；支持 Markdown 编写、变量插值（`{{query}}`）与条件块（`{% if lang == "en" %}`），适用于标准化问答、摘要、翻译等任务。  
- **LLM 应用开发**：在「智能体应用」或「工作流应用」中，[prompt](../guides/prompt.md) 作为应用配置项直接嵌入，可与工具调用、记忆管理、RAG 检索结果动态组合；Agent 2.0 支持将 prompt 与工具描述协同优化，增强指令对工具意图的理解。  
- **多模态生成**：文生图（万相）、文生视频（万相3.0、Vidu）等场景中，prompt 工程体现为结构化提示词公式——如 `[分镜1（0-3秒）：主角奔跑+城市街景+快速平移+电影感]`，需兼顾主体、场景、运动、美学等维度，并配合 `negative_prompt` 和 `prompt_extend` 等参数实现精细化控制。  
- **RAG 增强场景**：在文件问答或知识库应用中，prompt 工程聚焦于“检索后提示”（post-retrieval prompt）设计，例如明确要求模型“仅基于以下文档片段回答，未提及内容请拒答”，有效抑制幻觉并提升答案可信度。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 使用建议 |
|--------|------|------|----------|
| `prompt_template_id` | string | 已发布模板的唯一 ID | 必填（若使用模板）；建议在控制台「Prompt 实验室」中统一管理版本 |
| `variables` | object | JSON 格式键值对，用于填充模板变量 | 仅支持一级键访问（如 `{"user_input": "北京天气"}`），不支持嵌套路径 |
| `enable_optimization` | boolean | 启用基于用户反馈的自动 prompt 微调 | 需项目开通「Prompt 实验室」权限，且累计 ≥50 条有效“不满意”反馈才触发优化 |
| `max_prompt_tokens` | integer | 显式限制渲染后 prompt 的最大 token 数 | 建议设为模型 context 长度的 70%~80%，预留足够空间给响应 |
| `extra_body.prompt_extend`（文生图/视频） | boolean | 是否启用平台智能扩展提示词 | V2 默认 `true`，适合提示词较简略时使用；生产环境建议关闭以保障确定性 |

> ⚠️ 注意：`enable_optimization` 替代旧版 `optimize_level`；变量插值不支持表达式（如 `{{items[0].name}}` 无效）；模板渲染前最大长度为 8192 字符。

## 面向开发者的实用建议

- **从框架入手**：采用六要素 Prompt 框架（背景、目的、风格、语气、受众、输出格式）快速构建高质量初稿，再迭代压缩冗余描述。  
- **必做预览验证**：每次修改模板后，务必点击控制台「预览渲染结果」，确认变量正确解析、条件逻辑生效、无语法错误。  
- **区分场景选模式**：  
  - 稳定性优先 → 关闭 `enable_optimization`，手动 A/B 测试不同 prompt 版本；  
  - 快速上线 → 启用 `prompt_extend`（文生图/视频）或 `enable_thinking`（支持模型）辅助生成；  
  - RAG 场景 → 在 prompt 中显式声明“依据以下检索结果回答”，并设置拒答兜底句式。  
- **监控与闭环**：上线后关注 `prompt_template_id` 对应的「反馈率」与「采纳率」指标，将高频“不满意”样本归因至 prompt 设计缺陷（如歧义指令、缺失约束），而非单纯调参。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


