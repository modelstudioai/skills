# 提示词工程

提示词工程（Prompt Engineering）是指通过系统性设计、迭代与优化输入文本（prompt），精准引导大模型生成符合预期目标的输出结果的技术实践。它不是简单的“写一句话”，而是融合任务分析、结构建模、约束表达与效果验证的工程化方法，是百炼平台上连接开发者意图与模型能力的核心桥梁。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，提示词工程贯穿于多个核心能力层，具体体现为：

- **基础模型调用（`/v1/chat/completions`）**：以 `messages` 数组形式组织 prompt，推荐将角色设定、任务指令、格式要求、示例（few-shot）统一写入 `system` 消息；平台支持 `enable_prompt_optimization=true` 自动重写模糊或冗余表述，提升稳定性（需满足 `system` 内容 ≥20 字符且无强禁止改写指令）。

- **智能体应用（Agent 2.0）**：提示词作为 Agent 的“大脑指令”，定义其身份、能力边界与响应风格；配合 `agent context` 动态注入知识库、记忆或外部数据，形成“静态 prompt + 动态上下文”的复合输入，支撑自主规划与[工具调用](tool-calling.md)。

- **工作流应用（Workflow）**：各节点（如大模型节点、意图分类节点）均支持在参数中直接配置 prompt 模板，并可通过 `${变量名}` 语法实现动态拼接（如 `${开始/query}` + `${知识库/result}`），使提示词具备上下文感知与流程编排能力。

- **旧版 Flow Agent（Agent 1.0 / Legacy）**：提供基于样例反馈的 Prompt 自动优化能力——上传初始 prompt、样例数据（few-shot）和评测数据后，平台自动搜索更优 prompt 变体并给出量化评分，结果可导出复用或一键创建应用。

- **多模态生成（文生图/文生视频）**：提示词工程延伸至视觉语义建模，需按「主体+场景+风格+镜头语言」分层构造正向 prompt，并利用 `negative_prompt` 显式排除干扰元素；万相系列模型还支持 `prompt_extend: true`，由大模型自动扩写增强表现力。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 |
|------|----------|------|------|
| `messages` | 基础 API、工作流大模型节点 | array | 必填。标准 OpenAI 兼容格式，建议 `system` 消息承载核心指令，`user` 消息承载实时输入。 |
| `enable_prompt_optimization` | 基础 API（同步调用） | boolean | 默认 `false`。设为 `true` 启用平台级 prompt 重写（去歧义、补约束），仅对有效 `system` 消息生效。响应头 `x-bailian-prompt-optimized` 标识是否触发。 |
| `context_sources` | Agent 应用 | array | 定义动态上下文来源（RAG/记忆/Connector/ParseX），与 prompt 协同构成完整输入，受 `max_context_tokens` 截断控制。 |
| `prompt` / `negative_prompt` | 文生图/文生视频节点 | string | 多模态任务必填字段，直接影响生成质量；支持 `prompt_extend: true` 触发大模型智能扩写。 |
| 样例数据 & 评测数据 | Flow Agent（旧版）反馈优化 | file / list | 用于驱动 prompt 迭代：样例数据指导 few-shot 构建，评测数据提供客观评估依据（二者严格隔离，防过拟合）。 |

> ⚠️ 注意：所有 prompt 相关内容均计入模型上下文 token 总量（如 `messages` 总长上限 32768 tokens），超限将被截断并返回 `400 Bad Request`；动态注入的上下文（如 RAG 结果）同样占用该配额。

## 面向开发者，简洁实用

- ✅ **起步建议**：从结构化三要素开始——`system` 中明确「你是谁（角色）」「要做什么（任务）」「输出什么样（格式/约束）」；避免模糊表述（如“请友好回答”），改用可验证指令（如“用中文、不超过100字、以‘温馨提示：’开头”）。

- ✅ **调试技巧**：  
  - 对比测试：固定 `temperature=0` 和 `top_p=1`，排除随机性干扰；  
  - 分步验证：先测试纯 prompt 效果，再逐步加入 knowledge、memory 等 context；  
  - 利用样例库：直接复用 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的基准模板，微调适配业务。

- ✅ **进阶实践**：  
  - 在工作流中用 `${节点名/变量名}` 实现 prompt 动态组装，构建条件化响应逻辑；  
  - 对强格式需求（如 JSON Schema），在 prompt 中显式声明 schema 并启用 `response_format={"type": "json_object"}`（部分模型支持）；  
  - 关键业务场景慎用 `enable_prompt_optimization`，优先通过人工精调保障确定性。

- ❌ **避坑提醒**：  
  - 不要在 `system` 消息中混入用户私有数据（如 ID、手机号），避免被优化器误处理或泄露；  
  - `enable_prompt_optimization=true` 时，若 `system` 含“不得修改”类指令，平台仍会执行优化，可能导致行为偏差；  
  - Flow Agent（旧版）已停止功能迭代，新项目请优先选用 Agent 2.0 或工作流应用。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [agent context](../guides/agent-context.md)
- [agent legacy](../guides/agent-legacy.md)
- [use cases](../guides/use-cases.md)


