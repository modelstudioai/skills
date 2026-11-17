# Prompt 工程

Prompt 工程是指在百炼平台上，通过系统性设计、验证与优化提示词（[prompt](../guides/prompt.md)），以精准引导大模型生成符合业务预期的结构化、可控、高一致性输出的技术实践。它不是简单的文本拼接，而是融合任务建模、角色设定、示例约束、格式规范与模型行为理解的工程化方法。

## 在百炼平台的不同场景中如何使用

- **基础 API 调用**：在 `/v1/chat/completions` 接口中，通过 `messages` 数组组织 [prompt](../guides/prompt.md) —— `system` 消息定义全局指令（如“你是一名金融合规顾问，仅基于给定条款作答”），`user` 消息承载具体请求，`assistant` 消息可预置参考回复，实现少样本（few-shot）引导；在 `/v1/completions` 接口中，则直接传入结构化纯文本 [prompt](../guides/prompt.md)（适用于补全、摘要等非对话任务）。

- **LLM 应用构建（Flow Agent）**：在智能体、工作流或文件问答类应用中，Prompt 是核心配置项。开发者在控制台编辑「系统 Prompt」字段，定义角色、能力边界、输出格式（如 JSON Schema）、禁止行为（如“不可编造数据”）及 RAG 上下文注入规则；该 prompt 将被自动注入到每次模型调用中，并与工具调用、记忆管理、知识检索等节点协同生效。

- **Prompt 自动优化（Legacy & Governance）**：面向确定性任务（如分类、提取），可通过「提示词管理 > 反馈优化」上传输入-输出样例与评测集，由平台驱动多轮 prompt 生成与模型评测，输出最优 prompt 版本；Agent 治理模块进一步支持基于线上 Trace 数据或评测结果的闭环优化，提供多版本对比与一键采纳。

- **RAG 场景增强**：在文件问答或知识库集成中，Prompt 需显式声明如何融合检索结果（如“请严格依据以下【参考资料】回答，未提及内容不得臆测”），并配合 `history_rounds`、`top_k` 等参数控制上下文可见范围，避免幻觉。

- **安全与治理嵌入**：Prompt 工程与平台安全体系深度耦合——默认防护会自动检测 prompt 中的越狱、提示注入等风险；高级策略可强制插入安全指令（如“若用户要求生成违法内容，请返回标准拒绝话术”），实现 prompt 层面的主动防御。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 推荐值 |
|------|----------|------|--------|
| `messages`（含 `system`/`user`/`assistant`） | `/v1/chat/completions` | 最佳实践格式；`system` 内容即核心 prompt，长度建议 ≤512 字符以保障模型遵循度 | `system`: 角色+约束+格式；`user`: 清晰任务描述；`assistant`: 1–2 个高质量示例 |
| `prompt`（字符串） | `/v1/completions` | 适用于非对话补全任务；不支持 role 分隔，需自行拼接指令与输入 | 使用 `\n\n` 显式分隔指令与输入，避免歧义 |
| `temperature` | 全场景通用 | 控制输出随机性；值越高，prompt 意图越易漂移 | 生产环境设 `0.1–0.5`；调试阶段可临时提至 `0.7` 探索多样性 |
| `max_tokens` | 全场景通用 | 限制模型输出长度；过小导致截断，过大增加成本与延迟 | 根据输出目标设定：JSON 结构化输出建议 `256–512`；长摘要可设 `2048` |
| `model`（如 `qwen-plus`） | 全场景必填 | 不同模型对 prompt 的解析能力差异显著（如 `qwen-turbo` 对长 system 指令支持较弱） | 优先选用 `qwen-plus`（平衡效果与成本）；高精度场景选 `qwen-max` |

> ⚠️ 注意：  
> - `system` 消息在旧版模型（如 `qwen-turbo` v2023.12）中可能被忽略，务必在控制台调试验证；  
> - 避免在 prompt 中使用 `{variable}` 类未声明占位符——百炼不提供模板渲染，该行为无定义且不可靠；  
> - 单次请求总 token 数不得超过模型 context length 的 90%，超限将静默截断，建议提前估算。

## 面向开发者的实用建议

- **从模板起步**：直接复用「Prompt 样例库」中经验证的客服、代码、摘要等场景模板，再按需微调，而非从零构造；  
- **分层设计 prompt**：第一层（`system`）定义身份与原则，第二层（`user`）明确当前任务与输入，第三层（`assistant`）提供格式锚点；  
- **验证先于部署**：所有 prompt 修改后，必须在控制台「调试器」中用典型输入测试 3–5 次，重点检查格式一致性、约束遵守度、边界 case 处理；  
- **绑定模型迭代**：Prompt 与模型强耦合，`qwen-turbo` 上优化出的 prompt 切勿直接用于 `qwen-max` 应用，跨模型迁移前需人工回归验证；  
- **纳入可观测闭环**：开启「应用观测」后，可追踪每次 prompt 实际注入内容、模型响应 [Token](token.md) 消耗与 TTFT（首 token 延迟），快速定位 prompt 过长或指令失效问题。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [agent legacy](../guides/agent-legacy.md)
- [application use cases](../guides/application-use-cases.md)
- [agent governance](../guides/agent-governance.md)


