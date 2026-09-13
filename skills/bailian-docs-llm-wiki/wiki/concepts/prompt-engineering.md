# Prompt 工程

Prompt 工程是系统性设计、迭代与优化模型输入（Prompt）以稳定提升大语言模型输出质量、可控性与业务适配性的工程实践方法。它不是一次性指令编写，而是融合任务建模、模板结构化、变量注入、自动优化与效果验证的闭环工作流。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型调用**：通过 `POST /v3/services/{service_id}/call` 直接传入结构化 Prompt（如 `"你是一名客服专家，请基于以下知识回答用户问题：{{knowledge}}\n用户问：{{query}}"`），配合 `variables` 动态填充，实现轻量级任务定制。  
- **LLM 应用构建**：在智能体或工作流应用中，Prompt 是应用的核心配置项——控制台中可为每个节点（如“意图识别”“摘要生成”）独立设置 Prompt 模板，并与 RAG 检索结果、工具调用返回值自动拼接，形成多阶段上下文链。  
- **Prompt 自动优化**：对支持的模型（如 `qwen-max`、`qwen-plus`），启用 `enable_optimization: true` 后，平台基于历史调用反馈与效果指标（如人工评分、格式合规率）在线重写 Prompt，无需人工干预即可持续提效。  
- **评测驱动调优**：在应用评测（Application Evaluation）或模型评测（Model Evaluation）中，Prompt 作为关键变量参与 A/B 测试——可批量对比不同 Prompt 版本在相同数据集上的准确率、幻觉率等指标，定位优化方向。  
- **[多模态](multi-modal.md)与实时场景**：在 `qwen3.5-omni-plus-realtime` 等实时音视频模型中，Prompt 需严格遵循时序约束（如分段注入语音转文本结果 + 历史对话摘要），并配合 `system` 角色指令控制响应风格与延迟敏感度。

## 关键参数和配置

- `prompt`：必需字符串，支持纯文本或 Jinja2 模板语法（如 `{{system}}\n{{history}}\n{{user}}`），最大长度 32768 字符；禁止使用 `{% include %}` 等外部引入语句。  
- `variables`：可选对象，用于运行时安全填充模板变量（如 `{"query": "杭州天气", "knowledge": "今日多云，15–22℃"}`）；变量名不可与保留字段（`system`、`history`、`tools`）冲突。  
- `enable_optimization`：布尔值，默认 `false`；设为 `true` 时触发平台级 Prompt 自动优化（仅限白名单模型且账户已开通权限）。  
- `template_id`：可选字符串，引用控制台已发布的 Prompt 模板 ID，实现跨应用/跨团队复用与版本管理。  
- `render_only`（调试专用）：调用 `/v3/prompt/render` 接口时启用，仅返回变量渲染后的最终 Prompt 文本，不触发模型推理，用于快速验证模板逻辑。

> 提示：所有 Prompt 渲染后总长度（含变量展开）不得超过目标模型的 context 长度（如 `qwen-max` 为 32K tokens），建议在正式调用前先执行渲染预检。

## 面向开发者，简洁实用

- ✅ **起步建议**：从控制台「Prompt 模板」创建一个带 `{{input}}` 变量的基础模板，再通过 SDK 调用 `call` 接口传入 `template_id` 和 `variables`，避免硬编码。  
- ✅ **调试必做**：每次修改模板后，先调用 `/v3/prompt/render` 查看实际渲染结果，确认变量填充无空值、格式无错位。  
- ✅ **优化进阶**：对高价值场景（如客服应答、合同审核），开启 `enable_optimization` 并配合应用评测收集人工反馈，让平台自动收敛最优 Prompt。  
- ❌ **避坑提醒**：勿在模板中使用复杂逻辑（如嵌套循环）、禁止动态加载外部内容；`system` 指令需前置且简明，避免与 `user` 指令语义重叠。  
- 📊 **效果度量**：将 Prompt 版本号写入请求 `metadata` 字段，在应用评测报告中按版本聚合分析指标，建立 Prompt 迭代基线。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [application evaluation](../guides/application-evaluation.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


