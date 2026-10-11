# Prompt 工程

Prompt 工程是指系统性设计、验证、迭代和管理提示词（Prompt）的技术实践，旨在通过结构化方法提升大语言模型在特定任务上的准确性、稳定性、可控性与可解释性。它超越简单指令输入，涵盖模板构建、上下文注入、角色设定、约束强化、反馈驱动优化等全生命周期环节，是百炼平台上构建高质量 LLM 应用的核心工程能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：Prompt 工程直接体现为系统提示词（System Prompt）的设计与调优。Agent 2.0 支持将 Prompt 与工具定义、记忆机制、反思逻辑深度耦合；通过 `agenteval` 的多版本对比与调试反馈优化，可基于真实 Trace 数据定向改进 Prompt 对工具调用、错误恢复、多步规划的引导效果。

- **工作流（Workflow）应用**：Prompt 以「大模型节点」或「智能体节点」的配置项形式嵌入流程。开发者可复用资产中心托管的 Prompt 模板（`asset://...` URI），或在节点内直接编写结构化 Prompt（如采用 CRISPE 或 RASCEF 框架），配合 `enable_thinking` 和 `thinking_budget` 参数控制推理深度。

- **高代码应用**：Prompt 工程完全由开发者掌控。可通过 SDK 调用 `GetPromptTemplate` 获取已优化模板，动态填充变量后传入 `chat.completions.create()`；也可结合 `agenteval` 导出的评测集与人工反馈，用 Python 脚本批量生成/评估 Prompt 变体，实现 CI/CD 式 Prompt 迭代。

- **RAG 增强场景**：虽样例库已弃用，但 Prompt 工程仍关键作用于 RAG 流程——例如在知识库节点前插入重写 Prompt（“请根据以下问题提炼核心实体与意图，输出简洁关键词”），或在最终生成节点中设计融合指令（“严格依据召回文档片段作答，未提及内容不得编造”），显著提升答案忠实度。

- **可观测与评测闭环**：`agenteval` 将 Prompt 视为可量化资产：通过观测 Trace 中的 `prompt_tokens`、`prompt_content` 字段定位冗余或歧义；利用 LLM 评估器对不同 Prompt 版本的输出做语义评分；再基于高分样本反向提炼优化规则，形成“观测 → 评测 → 优化”正向飞轮。

## 关键参数和配置

| 参数 | 说明 | 使用建议 |
|------|------|----------|
| `workspaceId` | 所有 Prompt 相关操作的命名空间标识 | 必填；确保模板、RAG 表格库、评测集归属同一 workspace 才能联动生效 |
| `promptTemplateId` | 模板唯一 ID（控制台卡片右下角可复制） | 自定义模板推荐命名含业务含义（如 `qa_finance_v2`），便于团队协作识别 |
| `variables` | 模板中声明的占位符列表（如 `["user_query", "product_name"]`） | 运行时必须提供完整变量值，缺失将导致渲染失败；建议在 SDK 调用前校验 |
| `has_thoughts=true` | API 请求头或 query 参数 | 仅调试阶段开启，用于查看模型内部思考链路（如 RAG 检索关键词、工具选择依据） |
| `recall_count` / `max_retrieval_count` | RAG 表格库召回片段数（默认 5，上限 10） | 平衡效果与 Token 成本：复杂问答可设为 8–10；简单匹配建议 3–5 |
| `temperature` | 控制生成随机性（范围 0.0–2.0） | Prompt 工程中建议：确定性任务（如格式转换）设为 0.0–0.3；创意类任务设为 0.7–1.0 |

> ⚠️ 注意：所有 Prompt 功能**仅支持华北2（北京）地域**；模板编辑框最大字符数为 **6144**，超长逻辑请拆分为多个模板或通过变量注入外部内容。

## 面向开发者，简洁实用

- **起步推荐路径**：  
  1. 控制台 → [提示词市场](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt) 复用预置模板 → 修改变量并调试；  
  2. 同一 workspace 下创建 RAG 表格库 → 在 Prompt 中加入 `{{rag_context}}` 占位符；  
  3. 发布应用后，开启 `agenteval` 观测 → 导出低分 Trace → 提交至「反馈优化」生成新 Prompt。

- **避坑指南**：  
  - ❌ 不要依赖已停服的 Prompt 样例库，新项目一律使用 RAG 表格库；  
  - ❌ 避免在 Prompt 中硬编码敏感信息（如 API Key），应通过环境变量或 MCP 工具注入；  
  - ✅ 所有自定义 Prompt 模板均应存入**资产中心**，打上 `v1.0.0` 等语义化版本号，便于回滚与灰度；  
  - ✅ 利用 `agenteval` 的标签体系，为典型 Prompt 失败案例打标（如 `#hallucination`、`#format_error`），加速根因分析。

- **SDK 快速集成示例（Python）**：  
  ```python
  from alibabacloud_bailian20231219 import models as bailian_models
  client = BailianClient(...)
  # 获取模板并渲染
  template = client.get_prompt_template(
      workspace_id="ws-xxx",
      prompt_template_id="pt-yyy"
  )
  rendered = template.content.format(
      user_query="如何申请发票？",
      product_name="百炼API服务"
  )
  # 调用模型（自动启用 thinking）
  response = client.chat_completions_create(
      model="qwen-max",
      messages=[{"role": "user", "content": rendered}],
      enable_thinking=True,
      extra_params={"has_thoughts": "true"}  # 调试时启用
  )
  ```

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)
- [asset center page](../guides/asset-center-page.md)


