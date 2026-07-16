# 函数调用（Function Calling）

函数调用（Function Calling）是让大模型在推理过程中根据用户输入，自主判断并"调用"外部工具（自定义函数、内置能力或插件）以获取实时信息、执行精确计算或操作外部系统的能力。它是弥补大模型原生局限、构建 Agent 与复杂应用的核心机制。

## 在百炼平台的使用场景

百炼在多个层面暴露了 Function Calling 能力：

- **文本 / 视觉生成模型**：所有 Qwen3 及以上通用文本与视觉理解模型均支持自定义工具调用。以 `qwen3.7-plus` 为代表的旗舰模型工具调用完整、上下文长（1M），适合 AI 编程与 Agent 开发；效果确认后可切到 `qwen3.6-flash` 降本，功能与上下文保持一致。
- **实时多模态（Omni-Realtime API）**：基于 WebSocket 的实时音视频对话同样支持工具调用。客户端通过 `session.update` 事件在会话中声明工具，模型触发调用后由 `response.function_call_arguments.done` 服务端事件返回调用参数，客户端执行后再用 `conversation.item.create` 事件回传工具结果。
- **应用构建（智能体 / 工作流）**：新版智能体（Agent 2.0）将知识库、MCP、插件等能力统一抽象为"工具"，由智能体自主规划调用顺序，形成"规划-执行-反思"链路。工作流应用则把工具作为固定节点按编排顺序执行，不由模型主动规划。
- **插件（Plug-in）与 Assistant API**：插件是工具集合，本质也是工具调用。智能体应用 / Assistant API 中，模型依据工具名称与描述判断是否调用；无需调用时直接生成结果。

## 内置工具与自定义工具

- **自定义工具（Function Calling）**：开发者自行定义工具名称、描述与参数结构，模型据此决定何时调用、如何填参，应用侧执行后将结果回填模型生成最终回复。
- **内置工具**：联网搜索、代码解释器、网页抓取等由平台预置，无需复杂配置即可开启，是 Function Calling 的开箱即用形态。

## 关键参数与配置

- **模型选型**：推荐具备强工具调用能力的模型（如千问-Max / `qwen3.7-plus` 系列）。
- **思考模式**：可通过 `enable_thinking` 开启（Responses API 用 `reasoning.effort` 控制），配合工具调用提升规划质量。
- **ReAct 最大轮次**：智能体中取值 1-50，限制单次会话内工具调用的最大次数，防止无限循环。
- **实时 API 工具配置**：通过 `session.update` 的 `tools` 字段声明可用工具；工具调用结果需经 `conversation.item.create` 回传。
- **插件调用**：通过 Assistant API 调用时需正确传递工具 ID（如 `calculator`、`code_interpreter`），且每个智能体应用最多添加 10 个工具。

## 开发建议

- 优先用内置工具满足通用需求（搜索、计算、代码执行），减少自定义成本。
- 自定义工具时，工具名称与描述要清晰准确，直接影响模型是否正确触发调用。
- 需要精确、可控流程时用工作流把工具固化为节点；需要动态规划时用智能体让模型自主调用。
- 旧版智能体的自定义插件有 5 秒超时限制，设计工具时注意执行时长。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [model experience](../guides/model-experience.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)


