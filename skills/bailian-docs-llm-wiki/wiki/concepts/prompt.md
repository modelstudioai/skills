# 提示词工程

提示词工程（Prompt Engineering）是百炼平台上系统化设计、优化与管理大语言模型输入指令（Prompt）的方法论与技术实践，旨在通过结构化表达、上下文注入、约束控制与反馈迭代等手段，稳定提升模型输出的相关性、准确性、安全性与格式合规性。

## 在百炼平台的不同场景中，这个概念如何使用

提示词工程在百炼平台并非单一功能模块，而是贯穿于多个核心能力的底层实践范式，具体体现为：

- **模板化开发**：通过预置或自定义 Prompt 模板（如营销文案生成、摘要抽取），将工程经验固化为可复用资产；支持 ICIO、CRISPE、RASCEF 等主流框架结构，便于团队协作与版本管理。  
- **智能体（Agent 2.0）构建**：系统提示词（system prompt）是 Agent 的“角色设定”与“行为契约”，直接影响其工具调用规划、反思深度与安全边界；`enable_thinking` 参数需配合高质量提示词才能发挥效用。  
- **工作流（Workflow）编排**：每个 AI 节点的 Prompt 是流程逻辑的关键控制点，可结合上游节点输出动态拼接变量（如 `${knowledge_retrieval_result}`），实现 RAG 增强、多步推理等复杂链路。  
- **评测与优化闭环（Agenteval）**：利用 Agenteval 的可观测性追踪 Prompt 实际执行路径，通过多版本对比、人工反馈+LLM 反思、基于 query/answer 样例的反馈式优化，驱动 Prompt 持续演进。  
- **RAG 替代方案落地**：原 Prompt 样例库（Few-shot）已下线，其能力由 RAG 表格库承接——此时提示词工程重点转向设计能高效激活知识片段的检索增强型 Prompt（例如明确指令“仅基于以下召回内容回答，禁止编造”）。  

> ⚠️ 注意：所有 Prompt 功能当前仅支持华北2（北京）地域。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 必填；从控制台创建后复制，或调用 `CreatePromptTemplate` 接口获取响应中的 ID。 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "platform"]`） | 调用前必须传入完整变量值；不可运行时增删，建议在模板设计阶段预留扩展字段。 |
| `recall_count` | RAG 表格库召回片段数（替代原样例库 `top_k`），默认 5，最大 10 | 生产环境建议设为 3–5，平衡效果与 Token 消耗；超 5 后边际收益递减明显。 |
| `has_thoughts` | 设为 `true` 时返回 `thoughts` 字段（含 RAG 召回详情、工具调用逻辑等） | **仅调试启用**；生产请求务必关闭，避免泄露内部信息并节省 Token。 |
| `temperature` | 控制输出随机性（范围 `[0, 2)`），影响确定性任务稳定性 | 通用生成建议 `0.3–0.7`；工具调用、格式校验等强确定性场景推荐 `0.0–0.3`。 |
| `system_prompt` | Agent 或工作流 AI 节点的系统级指令 | 需明确角色、目标、约束（如“不编造”“只用中文”“输出 JSON 格式”），避免模糊表述。 |

## 面向开发者，简洁实用

- ✅ **优先用模板，而非硬编码**：所有重复使用的 Prompt 逻辑，务必封装为模板（`promptTemplateId`），便于统一维护、灰度发布与 AB 测试。  
- ✅ **RAG 场景下，Prompt = 检索器 + 生成器的粘合剂**：在 Prompt 中显式引用召回内容（如“参考以下信息：{{retrieved_text}}”），并添加拒答指令（“若信息不足，请回答‘暂无相关信息’”）。  
- ✅ **调试必开 `has_thoughts`，上线必关**：快速定位 RAG 是否召回、Agent 是否误调工具、模型是否忽略约束。  
- ✅ **优化不是玄学，要数据驱动**：用 Agenteval 创建评测集（≥20 条真实业务样本），搭配 LLM 评估器量化改进效果，避免主观判断。  
- ❌ **不要依赖已下线的 Prompt 样例库**：立即迁移至 RAG 表格库，旧代码中 `top_k` 相关逻辑需替换为 `recall_count` 并重构 Prompt 结构。  
- ❌ **避免过长 Prompt**：模板内容 + 变量填充 + RAG 召回文本总 token 数应 ≤ 模型上下文上限的 80%（如 `qwen-max` 为 32K，则控制在 26K 内），预留空间给模型思考与输出。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [agenteval](../guides/agenteval.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)


