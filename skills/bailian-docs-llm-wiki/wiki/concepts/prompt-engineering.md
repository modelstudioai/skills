# Prompt 工程

Prompt 工程是指在百炼平台上系统性设计、验证、优化和复用提示词（Prompt）的方法论与实践体系，旨在通过结构化表达、变量抽象、反馈闭环和资产化管理，显著提升大模型输出的准确性、一致性、可控性与业务适配度。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调试与体验**：在「模型体验」界面中，Prompt 工程体现为对输入文本的精细化构造——开发者可快速尝试不同表述、角色设定或约束指令，并结合 `temperature`/`top_p` 等参数观察输出变化，形成初步 [prompt](../guides/prompt.md) 迭代闭环。  
- **应用开发与部署**：在「应用开发」中，Prompt 工程落地为模板化能力——通过「Prompt 管理」创建带占位符（如 `{{input}}`、`{{context}}`）的可复用模板，绑定至 API 端点后，由变量注入驱动多场景复用（如客服问答、合同摘要、代码解释）。  
- **RAG 与智能体构建**：在 RAG 应用中，Prompt 工程决定检索结果如何被有效整合——需显式设计系统提示（`system_prompt`）引导模型“仅依据以下知识作答”，并控制上下文拼接格式；在智能体工作流中，各节点的 Prompt 需定义清晰的输入/输出契约与错误处理逻辑。  
- **资产中心统一治理**：Prompt 模板作为一类核心 AI 资产，在「资产中心」中支持版本管理、权限控制、标签分类与跨项目共享，实现从单点优化到组织级沉淀的升级。  
- **生产环境持续优化**：启用 `enable_optimization=true` 后，系统基于真实调用日志与人工标注（“有用/无用”）自动重写低效 Prompt，适用于已发布至生产环境的模板，形成数据驱动的 [prompt](../guides/prompt.md) 自进化能力。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 推荐值/注意事项 |
|--------|------|------|----------------|
| `prompt_template_id` | string | 指定预存 Prompt 模板 ID；为空时使用默认模板 | 建议在生产环境显式指定，避免隐式依赖变更 |
| `variables` | object | 模板中占位符对应的键值对，如 `{"input": "总结下文", "context": "..."}` | 变量值需经安全过滤，禁止传入可执行内容或外部 URL |
| `enable_optimization` | boolean | 是否启用实时自动优化（语义重写+结构精简） | v3.2+ 默认关闭；仅对 `visibility=public` 或 `project` 且标记为“生产环境”的模板生效；需 ≥50 条有效反馈样本 |
| `system_prompt` | string | （可选）全局行为约束，独立于用户输入，用于定义角色、格式、禁令等 | 企业级应用强烈建议设置，例如 `"你是一名银行合规客服，不提供投资建议，所有回答必须引用最新监管文件编号"` |
| `max_tokens` / `temperature` 等 | — | 属于模型层采样参数，不影响 Prompt 解析逻辑，但共同决定最终输出质量 | 与 Prompt 协同调优：高 `temperature` 下需更强约束性 Prompt；长输出任务需预留足够 token 给 Prompt 本身 |

> ⚠️ 注意：Prompt 总长度（含变量展开后）不得超过 8192 token；超长将被静默截断并返回警告头 `X-Prompt-Truncated: true`。

## 面向开发者，简洁实用

- ✅ **起步最快方式**：进入控制台「资产中心」→ 搜索“客服”“摘要”等关键词 → 复用已审核的 Prompt 样例 → 修改变量后一键部署到 API。  
- ✅ **模板开发规范**：  
  - 使用 `{{variable}}` 占位符，避免硬编码；  
  - 在 `system_prompt` 中声明角色、边界与失败兜底逻辑（如“若信息不足，请明确回复‘暂无相关信息’”）；  
  - 为多轮对话设计 `messages` 数组，首条 `role=user` 内容为完整 Prompt 模板，后续轮次保持上下文连贯。  
- ✅ **调试技巧**：  
  - 在「模型体验」页粘贴模板 + 示例变量，快速验证渲染效果；  
  - 开启 `enable_optimization` 并标注 20+ 条反馈后，查看「Prompt 管理」页的“优化建议”卡片获取改写参考。  
- ✅ **避坑提醒**：  
  - 不要在 Prompt 中嵌入 `curl`、Python 代码或 `<script>` 标签——会被安全网关拦截；  
  - 避免模糊指令（如“请好好回答”），改用具体动作（如“分三点列出，每点不超过20字”）；  
  - RAG 场景中，`retrieval_config` 返回的 chunk 需在 Prompt 中显式标注来源（如 `[来源：2024年报P12]`），否则模型易幻觉。  

Prompt 工程不是一次性配置，而是贯穿模型选型、应用上线与线上迭代的持续实践——善用模板、反馈、资产化与自动化，让每一次提示都更接近业务预期。

## 关联主题页

- [prompt](../guides/prompt.md)
- [asset center page](../guides/asset-center-page.md)
- [model experience](../guides/model-experience.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)


