# Prompt 工程

Prompt 工程是指在百炼平台上，通过系统性设计、验证与优化结构化提示（`messages`），以精准引导大模型生成符合业务预期输出的技术实践。它不是简单的文本拼接，而是融合任务建模、角色设定、示例控制、约束注入与反馈迭代的工程化方法。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型调用**：使用 `messages` 数组（含 `system`/`user`/`assistant` 角色）构建可复现、高确定性的输入，例如用 `system` 指令限定输出格式，用 `user` 提供结构化输入，避免模糊指令。
- **LLM 应用开发（智能体/工作流）**：通过 `prompt_template` 字段注入 Jinja2 模板，实现变量动态填充（如 `{{input}}`、`{{context}}`），支持多节点上下文传递与条件分支逻辑。
- **旧版 Flow Agent（Agent 1.0）**：作为核心驱动机制，支持基于 I/O 样例的自动反馈优化（Feedback Optimization），系统自动选取样例、构造评测 prompt 并迭代生成更优版本。
- **RAG 与文件问答**：Prompt 工程与检索结果深度耦合——需显式设计 prompt 结构（如“根据以下文档片段回答…”），并配合 `retrieval_config` 控制召回质量，防止幻觉。
- **多模态生成（文生图/视频）**：虽非纯文本模型，但万相（WanX）等模型仍依赖高质量 Prompt 描述构图、风格、时长等关键要素，需遵循专用指南（如帧率、分辨率、seed 稳定性控制）。

## 关键参数和配置

| 参数 | 类型 | 说明 | 推荐实践 |
|------|------|------|----------|
| `messages` | array | **必填**，结构化 prompt 输入；每个元素含 `role`（`"system"`/`"user"`/`"assistant"`）和 `content`；`system` 优先级最高，用于全局角色/约束 | `system` 内容应简洁明确（≤500 字），避免敏感信息；`user` 中可嵌入 JSON Schema 或 XML 标签提升解析鲁棒性 |
| `enable_prompt_optimization` | boolean | 启用平台级自动优化（v3.2+），基于任务类型与历史效果动态重写 `messages` | 生产环境建议开启；调试时通过响应头 `X-Prompt-Optimized` 查看实际下发内容 |
| `prompt_template` | string | LLM 应用中使用的 Jinja2 模板字符串，支持 `{{input}}`、`{{context}}` 等占位符 | 避免深层嵌套逻辑；模板中需对变量做 `|e` 转义（如 `{{input\|e}}`）防止 XSS 或解析失败 |
| `stop` | array<string> | 指定生成终止 token（如 `["\n\n", "<|eot_id|>"]`），用于精确截断输出 | 对需要严格格式（如 JSON、代码块）的场景必设，避免模型续写无关内容 |
| `temperature` | number | 控制输出随机性（0.0–1.0）；**Qwen 系列默认 0.8，但生产推荐显式设为 0.1–0.3 提升确定性** | 不要依赖默认值；高确定性任务（如抽取、分类）设 `0.1`；创意生成任务可设 `0.7` |

> ⚠️ 注意：已弃用 `prompt`（string）字段；所有新开发必须使用 `messages`；`system` 消息不可为空，且禁止包含 PII 等敏感数据。

## 面向开发者，简洁实用

- **起步模板**（复制即用）：
  ```json
  {
    "model_id": "qwen-max",
    "messages": [
      {"role": "system", "content": "你是一名严谨的数据分析师，只输出标准JSON，字段为：summary（字符串）、key_insights（字符串数组）、confidence（0.0–1.0）"},
      {"role": "user", "content": "分析以下销售数据：{{data}}"}
    ],
    "temperature": 0.2,
    "stop": ["<|eot_id|>"],
    "enable_prompt_optimization": true
  }
  ```

- **避坑清单**：
  - ✅ 使用 `messages` 而非 `prompt`；  
  - ✅ `system` 消息精炼，不超 300 字；  
  - ✅ 所有用户输入变量在 `prompt_template` 中用 `|e` 转义；  
  - ✅ 启用 `enable_prompt_optimization` 并检查 `X-Prompt-Optimized` 响应头；  
  - ❌ 不在 `system` 中写示例（应放 `user` 或 `assistant`）；  
  - ❌ 不在 prompt 中硬编码 API Key、[Token](token.md) 等密钥；  
  - ❌ 不依赖 `temperature` 默认值，始终显式声明。

- **进阶提效**：  
  - 复用 [Prompt 样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的垂直模板（客服/法律/教育），替换占位符后直接集成；  
  - 对高价值任务（如合同审核），用旧版 Flow Agent 的 Feedback Optimization 功能，上传 5–10 条 I/O 样例 + ≥20 条评测集，一键生成鲁棒 prompt；  
  - 在工作流应用中，将 prompt 拆分为多个 `LLM` 节点，分别处理「意图识别→知识检索→结果生成」，比单一大 prompt 更可控。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [agent legacy](../guides/agent-legacy.md)
- [use cases](../guides/use-cases.md)
- [flow agent api](../api/flow-agent-api.md)


