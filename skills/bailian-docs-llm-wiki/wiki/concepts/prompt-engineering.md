# 提示工程

提示工程（Prompt Engineering）是百炼平台上系统化设计、优化与管理大语言模型输入指令（Prompt）的方法论与实践体系，旨在通过结构化表达、上下文控制、约束注入与反馈迭代等手段，精准引导模型行为，提升输出的准确性、一致性、安全性与业务适配性。

## 在百炼平台的不同场景中，这个概念如何使用

提示工程在百炼平台并非单一功能模块，而是贯穿模型调用、应用构建与持续优化全链路的核心实践范式：

- **基础模型调用**：直接通过 `input.messages` 中的 `system` 和 `user` 消息构造 Prompt，需遵循清晰角色设定、明确任务目标、限定输出格式（如 JSON Schema）、注入领域约束（如“仅基于给定文档回答”）。推荐使用 ICIO（Identity-Context-Instruction-Output）或 RASCEF（Role-Action-Steps-Constraints-Examples-Format）等结构化框架组织内容，尤其适用于 `qwen-max`、`qwen3.8-omni-flash-realtime` 等强推理模型。

- **智能体（Agent）应用**：系统提示词（System Prompt）是 Agent 的“大脑指令”，定义其身份、能力边界、工具调用规范及反思逻辑。Agent 2.0 支持将知识库、MCP 工具等统一为 Prompt 可调度资源，此时提示工程需协同工具描述（Tool Description）编写，确保模型能准确理解并触发对应能力。

- **工作流（Workflow）节点**：在“大模型节点”中配置用户提示词时，可引用上游节点输出（如 `${知识库节点/retrieved_content}`），实现动态 Prompt 拼装；结合条件判断与循环节点，可构建多阶段提示链（如“先摘要→再对比→最后生成建议”），体现流程化提示设计思想。

- **RAG 增强场景**：Prompt 不再孤立存在，而是与知识库召回结果深度耦合。需在 Prompt 中显式声明检索意图（如“请严格依据以下参考内容作答”），并合理设计拼接模板（如 `参考内容：${retrieved_text}\n\n问题：${query}\n\n回答：`），避免幻觉。原样例库（Few-shot）能力已下线，全部由 RAG 表格库承接，`recall_count` 参数即为此类 Prompt 动态扩展的关键控制点。

- **多模态生成**：文生图（万相）、文生视频（Vidu/万相3.0）等场景需区分正向提示词（`prompt`）与负向提示词（`negative_prompt`），并利用 `prompt_extend: true` 启用智能扩写，本质是平台侧对提示工程的自动化增强。

- **可观测与优化闭环（[agenteval](../guides/agenteval.md)）**：通过 `agenteval` 模块采集真实 Trace 数据（含原始 Prompt、模型响应、工具调用、RAG 召回片段），可定位 Prompt 失效根因（如上下文截断、指令歧义、约束缺失），驱动基于人工反馈或评测失败样本的定向优化，形成“调试→评估→优化→验证”的工程化迭代。

## 关键参数和配置

| 参数 | 说明 | 使用场景 | 注意事项 |
|------|------|----------|----------|
| `promptTemplateId` | 预置或自定义 Prompt 模板唯一标识 | 控制台创建/调用模板、API 获取模板内容 | 必填；仅华北2（北京）地域可用 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "platform"]`） | 模板化调用时动态注入业务变量 | 由 `GetPromptTemplate` 返回，不可运行时增删 |
| `recall_count` | RAG 表格库召回片段数（替代原样例库 `top_k`） | RAG 增强型 Prompt 构建 | 默认 5，最大 10；影响 [Token](token.md) 消耗与精度平衡 |
| `has_thoughts` | 请求级开关，启用后返回 `thoughts` 字段（含 RAG 召回详情等） | 调试与归因分析 | 生产环境建议关闭以节省 [Token](token.md) |
| `prompt` / `negative_prompt` | 文生图核心输入字段 | 万相、Vidu 等图像模型 | `negative_prompt` 仅万相支持；`prompt_extend` 默认开启，显著提升质量 |
| `enable_thinking` | 开启模型思考链输出（返回 `reasoning_content`） | qwen3.8-omni-flash-realtime、DeepSeek、Kimi 等支持模型 | 用于调试与可解释性分析，非所有模型支持 |

## 面向开发者，简洁实用

- ✅ **起步就结构化**：新写 Prompt 时，优先套用 ICIO 或 RASCEF 框架，5 秒内完成基础骨架（例如：`Role: 你是一名电商客服专家；Instruction: 根据用户问题和商品描述，生成不超过 50 字的友好回复；Output: 仅返回回复文本，不加任何前缀`）。
- ✅ **模板化 > 硬编码**：业务中重复使用的 Prompt（如营销文案生成、合同条款提取），务必创建 Prompt 模板并复用 `promptTemplateId`，避免代码中散落字符串。
- ✅ **RAG 必配 `recall_count`**：启用知识库时，显式设置 `recall_count=5`（默认值），若效果不佳，可逐步调至 8–10 并监控 [Token](token.md) 成本；切勿依赖未声明的隐式召回。
- ✅ **调试必开 `has_thoughts`**：本地调试 RAG 或 Agent 应用时，在请求中添加 `"has_thoughts": true`，快速查看实际拼入的上下文与召回内容，精准定位信息丢失点。
- ❌ **禁用已下线能力**：立即移除代码/配置中对 `prompt sample library`（样例库）的任何引用，全部迁移至 RAG 表格库；继续使用将导致功能失效。
- ⚠️ **温度值慎设为 0**：`temperature=0` 在部分模型（如 `qwen-max`）下可能返回空响应，生产环境推荐 `temperature=0.1` + `top_p=0.95` 组合，兼顾确定性与鲁棒性。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [agenteval](../guides/agenteval.md)
- [start using](../guides/start-using.md)
- [use cases](../guides/use-cases.md)


