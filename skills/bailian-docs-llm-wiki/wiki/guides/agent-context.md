# agent context

`agent context` 是百炼平台中用于增强 Agent 推理能力的核心上下文机制，它将外部知识、历史记忆、数据连接器及结构化解析能力统一注入 Agent 的执行环境。该机制不依赖模型自身参数，而是通过运行时动态注入方式影响 LLM 的 [prompt](prompt.md) 构建与决策路径。其设计目标是解耦“能力扩展”与“模型选型”，使同一 Agent 可灵活适配不同模型。

## 支持的模型与功能

当前 `agent context` 全量支持百炼平台所有可部署的 Agent 模型（含 Qwen 系列、Qwen2-Agents、以及第三方兼容模型），但部分高级功能需模型具备 tool-calling 或 structured output 能力。具体支持范围详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 文档中关于模型兼容性的说明。其中，Memory 功能在 Qwen2-Agents v1.2+ 中默认启用；而 ParseX 的 schema-aware 解析能力仅在支持 JSON Schema 输出的模型上生效，如 Qwen2.5-7B-Instruct（需开启 `response_format: { "type": "json_object" }`）。

## 关键参数

`agent context` 通过以下核心参数控制行为：

- `context_sources`: 数组，指定上下文来源类型，如 `["knowledge", "memory", "connector", "parsex"]`  
- `context_config`: 对象，按来源类型配置参数，例如：
  - `knowledge.max_chunks`: 控制 RAG 检索返回的最大文档块数（默认 3）
  - `memory.window_size`: 限制会话级记忆回溯轮数（默认 10）
  - `parsex.schema`: 定义结构化解析目标 schema（必须为合法 JSON Schema）
- `context_injection_strategy`: 可选 `"prepend"`（默认）或 `"inject"`，决定上下文插入 [prompt](prompt.md) 的位置

详细参数定义与默认值请参考 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的配置章节。

## 使用方式

1. 在创建或更新 Agent 时，于 `agent_config.context` 字段中声明上下文配置；
2. 若启用 `knowledge`，需提前绑定知识库 ID；启用 `memory` 需确保已开启会话状态管理；
3. `parsex` 需配合 `input_schema` 和 `output_schema` 显式声明输入/输出结构，并在调用时传入原始非结构化文本；
4. 所有上下文内容均在每次 `run` 请求时实时注入，不缓存至模型权重中。

完整示例与 SDK 调用代码见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的快速开始部分。

## 限制和注意事项

- 单次请求中 `context_sources` 总长度（含所有注入文本）不得超过 32,768 token，超限将触发截断并返回警告日志；
- `memory` 与 `connector` 同时启用时，若 connector 返回数据含时间敏感字段（如 `updated_at`），可能与 memory 的时序窗口冲突，导致逻辑不一致；
- > **注意**：原始文档 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中提及 “connector 支持异步预加载”，但该特性已在 v2.4.0 版本中移除，实际行为为同步阻塞加载，最新行为以 [Connector 概览](../../raw/agent-context/overview.md) 为准；
- `parsex` 当前不支持嵌套过深（>5 层）或含循环引用的 schema，解析失败将退化为原始文本透传；
- 所有 context 注入内容均参与计费（按 token 计），建议通过 `max_chunks` 和 `window_size` 主动约束规模。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


