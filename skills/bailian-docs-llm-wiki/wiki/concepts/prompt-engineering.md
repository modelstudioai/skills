# Prompt 工程

Prompt 工程是百炼平台中系统化设计、验证与优化大语言模型输入指令（Prompt）的方法论与实践体系，旨在通过结构化表达、变量控制、样例引导和反馈迭代等手段，稳定提升模型输出的准确性、一致性与业务适配性。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）与工作流应用**：Prompt 是应用行为的“第一层定义”。开发者可在创建智能体时直接填写基础提示词（如“你是一名金融合规顾问，请用简明条款式语言回答…”），或绑定预置/自定义 Prompt 模板，实现角色设定、任务约束与输出格式的标准化；模板中的 `${variable}` 可动态注入用户输入、知识库召回结果或工具返回值，支撑个性化响应。
  
- **RAG 增强场景**：Prompt 不再孤立存在，而是与知识库深度协同。在知识库配置中，可通过 Prompt 模板控制检索后内容的拼装逻辑（例如：“请基于以下{retrieved_chunks}，严格按‘规则→例外→示例’三段式作答”），确保 RAG 输出结构可控、语义对齐。

- **Agenteval 质量闭环**：Prompt 工程进入可观测与可度量阶段。通过 Trace 沉淀真实对话样本 → 构建带标签的评测集 → 使用 LLM 或 Code 评估器自动打分 → 基于人工反馈（问题现象 + 期望行为）触发 Prompt 智能优化，形成“调试→评测→优化→验证”的持续改进循环。

- **[多模态](multimodal.md)生成任务**：Prompt 工程延伸至图文、音视频领域。文生图需同时配置 `prompt` 与 `negative_prompt`，并启用 `prompt_extend: true`；文生视频须遵循“主体+场景+运动”公式化结构；所有[多模态](multimodal.md) Prompt 均需规避文学化修辞，采用口语化、分句式、具象化表达。

- **本地 RAG 集成与 AppFlow 渠道部署**：Prompt 是连接云端能力与业务前端的关键粘合剂。在本地部署方案中，Prompt 作为 `chat.py` 的核心配置项，统一控制温度、上下文轮数与输出长度；在 AppFlow 网站/企微挂件中，Prompt 决定助手人格与应答边界，直接影响终端用户体验。

> ⚠️ 注意：Prompt 样例库（few-shot）功能已下线，官方明确要求迁移至 RAG 表格库；所有 Prompt 相关能力（模板、优化、RAG 拼装）仅支持华北2（北京）地域。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一标识符 | 控制台模板卡片上直接复制；调用 `GetPromptTemplate` 接口可获取其 `content` 与 `variables` 列表，必须严格匹配填入变量值。 |
| `variables` | 模板中声明的变量名（如 `["user_query", "product_name"]`） | 变量替换需在 SDK/API 调用前完成，不可留空或错位；建议使用 JSON Schema 校验输入结构。 |
| `has_thoughts=true` | 启用调试日志输出 | 仅限 API 调用时设置，响应中 `thoughts` 字段将返回 RAG 召回详情、片段相似度及拼装过程，用于根因分析。 |
| `temperature` / `top_p` | 控制输出随机性与多样性 | 生产环境推荐设为 `0.1–0.5`（`temperature`）与 `0.7–0.9`（`top_p`），兼顾稳定性与自然度；该参数作用于模型推理层，独立于 Prompt 内容。 |
| `enable_thinking` | 启用思维链（CoT）模式 | 仅当模型原生支持（如 `qwen3.7-max`）且 Prompt 中包含明确推理指令（如“请逐步分析…”）时生效；需配合 `thinking_budget` 控制推理 token 消耗。 |

- **结构化框架推荐**：对模糊需求，优先采用 ICIO（Identity, Context, Instruction, Output format）或 CRISPE（Capacity, Role, Insight, Statement, Personality, Experiment）框架组织 Prompt，例如：<br>`你是一名电商客服专家（Role），当前用户咨询退货政策（Context）。请先确认订单是否满足7天无理由条件（Instruction），再分点列出处理步骤、时效与注意事项（Output format）。`

## 面向开发者，简洁实用

- ✅ **立即上手**：控制台 → [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) → 创建模板 → 使用变量语法 → 绑定到智能体应用 → 发布即生效。
- ✅ **快速优化**：粘贴低效 Prompt 至 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面 → 一键生成增强版 → 复制测试 → 保存为新模板。
- ✅ **闭环提效**：开启 Agenteval 观测 → 导出失败 Trace → 创建评测集 → 配置 LLM 评估器 → 运行评测 → 选中问题样本 → 提交结构化反馈 → 获取优化 Prompt → 替换线上模板。
- ❌ **避免踩坑**：勿使用已弃用的 Prompt 样例库；勿跨地域调用 Prompt 接口；勿在 Prompt 中硬编码敏感信息；模板内容不计入模型 token 限额，但过长会影响可维护性（控制台编辑框上限 6144 字符）。

Prompt 工程不是一次性配置，而是贯穿 AI 应用生命周期的持续实践——从第一行指令的设计，到每一次用户反馈的转化，都是让大模型真正“听懂业务”的关键一步。

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [llm application](../guides/llm-application.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)


